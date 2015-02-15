#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is a part of myLwM2M project.
#
# Copyright (c) 2015 Alexander Ellwein <mylwm2m@ellwein.net>,
#
# myLwM2M is free software, this file is published under the MIT license as
# described in the accompanying LICENSE file.

import hashlib


class Hasher(object):
    def __init__(self, seed):
        self.seed = seed

    def hash_for(self, string):
        assert string is not None
        h = hashlib.new("sha1")
        h.update(string.encode())
        h.update(self.seed)
        return h.hexdigest()


class ClientPersistence(object):
    def has_client_with_location(self, location):
        raise NotImplementedError("implemented by a subclass")

    def has_client_with_endpoint_name(self, endpoint):
        raise NotImplementedError("implemented by a subclass")

    def get_client_for_endpoint_name(self, endpoint):
        raise NotImplementedError("implemented by a subclass")

    def get_client_for_location(self, location):
        raise NotImplementedError("implemented by a subclass")

    def put_client_by_endpoint_name(self, endpoint, client):
        raise NotImplementedError("implemented by a subclass")

    def put_client_by_location(self, location, client):
        raise NotImplementedError("implemented by a subclass")

    def delete_client_by_location(self, location):
        raise NotImplementedError("implemented by a subclass")

    def delete_client_by_endpoint_name(self, endpoint):
        raise NotImplementedError("implemented by a subclass")

    def client_iterator(self):
        raise NotImplementedError("implemented by a subclass")


class InMemoryPersistence(ClientPersistence):
    def __init__(self, hasher):
        self.hasher = hasher
        self.clients = dict()

    def has_client_with_location(self, location):
        return location in self.clients

    def has_client_with_endpoint_name(self, endpoint):
        location = self.hasher.hash_for(endpoint)
        return location in self.clients

    def get_client_for_endpoint_name(self, endpoint):
        location = self.hasher.hash_for(endpoint)
        return self.clients[location]

    def get_client_for_location(self, location):
        return self.clients[location]

    def put_client_by_endpoint_name(self, endpoint, client):
        location = self.hasher.hash_for(endpoint)
        self.clients[location] = client

    def put_client_by_location(self, location, client):
        self.clients[location] = client

    def delete_client_by_endpoint_name(self, endpoint):
        location = self.hasher.hash_for(endpoint)
        del self.clients[location]

    def delete_client_by_location(self, location):
        del self.clients[location]

    def client_iterator(self):
        for k, v in self.clients.items():
            yield v