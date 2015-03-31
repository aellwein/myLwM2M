#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is a part of myLwM2M project.
#
# Copyright (c) 2015 Alexander Ellwein <mylwm2m@ellwein.net>,
#
# myLwM2M is free software, this file is published under the MIT license as
# described in the accompanying LICENSE file.

import logging
import asyncio
import os
import re
import aiocoap
from aiocoap.numbers.codes import Code
import aiocoap.resource as resource
from lwm2m.persistence import InMemoryPersistence, Hasher

logging.basicConfig(level=logging.INFO)
logging.getLogger("myLwM2M-server").setLevel(logging.DEBUG)


class Server(resource.Resource):
    log = logging.getLogger("myLwM2M-server")

    ENDPOINT = "ep"
    LIFETIME = "lt"
    BINDING_MODE = "b"
    SMS = "sms"
    LWM2M_VERSION = "lwm2m"
    DEFAULT_VERSION = "1.0"
    DEFAULT_LIFETIME = 86400
    CLEANER_PERIOD_SECONDS = 10

    def __init__(self, client_persistence, hasher):
        self.log.debug("creating server instance")
        self.client_persistence = client_persistence
        self.hasher = hasher
        self.site = resource.Site()
        self.site.add_resource((self.get_path(),), self)

    @staticmethod
    def get_path():
        return "rd"

    @asyncio.coroutine
    def render_post(self, request):
        """
        This method is called on client registration.
        :param request:
        :return:
        """
        opts = dict(x.split("=") for x in request.opt.uri_query)
        self.log.debug("POST called with options %s" % opts)

        if self.ENDPOINT not in opts:
            # endpoint name is the only required
            return Server.bad_request(b"endpoint name is required")

        client = dict()
        client["endpoint"] = opts[Server.ENDPOINT]
        client["lifetime"] = self._get_lifetime(opts, Server.DEFAULT_LIFETIME)

        client["lwm2m_version"] = opts[Server.LWM2M_VERSION] if Server.LWM2M_VERSION in opts else Server.DEFAULT_VERSION
        client["sms"] = opts[Server.SMS] if Server.SMS in opts else None
        client["binding_mode"] = Server.get_binding_mode(
            opts[Server.BINDING_MODE]) if Server.BINDING_MODE in opts else "U"
        payload = request.payload.decode()
        if payload == "":
            return Server.bad_request(b"payload must contain object links")
        client["objects"] = Server.get_object_links(request.payload.decode())

        location = self.hasher.hash_for(opts[Server.ENDPOINT])
        client["location"] = location
        client["time"] = asyncio.get_event_loop().time()

        # add a client
        self.client_persistence.put_client_by_location(location, client)

        # add resource for registration
        self.site.add_resource((Server.get_path(), location), self)

        response = aiocoap.Message(code=Code.CREATED)
        response.opt.location_path = [Server.get_path().encode(), location.encode()]
        return response

    def _get_lifetime(self, opts, default_lifetime):
        # handle lifetime
        if self.LIFETIME in opts:
            try:
                lifetime = int(opts[Server.LIFETIME])
            except ValueError:
                return Server.bad_request(b"non-numeric lifetime value")

            if lifetime <= 0:
                return Server.bad_request(b"lifetime value out of range")
            else:
                return lifetime
        else:
            return default_lifetime

    def _remove_client(self, location):
        self.site.remove_resource((Server.get_path(), location))
        self.client_persistence.delete_client_by_location(location)

    @staticmethod
    def get_binding_mode(bmode):
        modes = ["U", "UQ", "S", "SQ", "US", "UQS"]
        return bmode if bmode in modes else "U"

    @staticmethod
    def get_object_links(payload):
        objs = dict()
        for link in payload.split(","):
            m = re.match("^<(/(\d+))(/(\d+))*>.*$", link)
            # TODO links may come in another format, refer to spec
            if m.group(4) is not None:
                obj_id = str(m.group(2))
                instance_id = str(m.group(4))
                if obj_id in objs:
                    objs[obj_id][instance_id] = instance_id
                else:
                    objs[obj_id] = {instance_id: instance_id}
            else:
                obj_id = str(m.group(2))
                if obj_id in objs:
                    objs[obj_id]["0"] = "0"
                else:
                    objs[obj_id] = {"0": "0"}
        return objs

    @staticmethod
    def bad_request(payload=None):
        response = aiocoap.Message(code=Code.BAD_REQUEST)
        if payload is not None:
            response.payload = payload
        return response

    @asyncio.coroutine
    def render_put(self, request):
        location = request.opt.uri_path[-1]
        self.log.debug("PUT called for location %s" % location)
        opts = dict(x.split("=") for x in request.opt.uri_query)
        client = self.client_persistence.get_client_for_location(location)
        client["time"] = asyncio.get_event_loop().time()
        client["lifetime"] = self._get_lifetime(opts, client["lifetime"])
        client["binding_mode"] = Server.get_binding_mode(
            opts[Server.BINDING_MODE]) if Server.BINDING_MODE in opts else client["binding_mode"]
        client["sms"] = opts[Server.SMS] if Server.SMS in opts else client["sms"]
        payload = request.payload.decode()
        if payload != "":
            client["objects"] = Server.get_object_links(payload)

        response = aiocoap.Message(code=Code.CHANGED)
        return response

    @asyncio.coroutine
    def render_delete(self, request):
        location = request.opt.uri_path[-1]
        self.log.debug("DELETE called for location %s" % location)
        self._remove_client(location)
        response = aiocoap.Message(code=Code.DELETED)
        return response

    def cleaner(self):
        self.log.debug("running periodic cleaner")
        to_delete = list()
        for client in self.client_persistence.client_iterator():
            time = asyncio.get_event_loop().time()
            if time - client["time"] > client["lifetime"]:
                to_delete.append(client["location"])
        for location in to_delete:
            self.log.debug("removing dead client (location %s)" % location)
            self._remove_client(location)
        # reschedule the cleaner
        asyncio.get_event_loop().call_later(Server.CLEANER_PERIOD_SECONDS, self.cleaner)

    def start(self):
        asyncio.async(aiocoap.Context.create_server_context(self.site))
        asyncio.get_event_loop().call_later(Server.CLEANER_PERIOD_SECONDS, self.cleaner)
        try:
            asyncio.get_event_loop().run_forever()
        except KeyboardInterrupt:
            self.log.debug("server stopped")


def main():
    hasher = Hasher(os.urandom(30))
    Server(InMemoryPersistence(hasher), hasher).start()


if __name__ == '__main__':
    main()