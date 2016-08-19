#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is a part of etero project.
#
# Copyright (c) 2016 Alexander Ellwein <etero@ellwein.net>
#
# etero is free software, this file is published under the MIT license as
# described in the accompanying LICENSE file.

import asyncio
import logging

from aiocoap import Context
from aiocoap import resource

from lwm2m.hasher import Sha256Hasher
from lwm2m.persistence import InMemoryPersistence

log = logging.getLogger("server")


class Server(resource.Resource):
    """
    LWM2M Server implementation.
    """

    def __init__(self, hasher=None, persistence=None):
        self._hasher = hasher if hasher else Sha256Hasher()
        self._persistence = persistence if persistence else InMemoryPersistence(hasher)

    @asyncio.coroutine
    def run(self):
        self.context = yield from Context.create_server_context(self, )


def main():
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(Server().run())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()


if __name__ == '__main__':
    main()
