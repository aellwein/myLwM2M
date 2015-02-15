#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is a part of myLwM2M project.
#
# Copyright (c) 2015 Alexander Ellwein <mylwm2m@ellwein.net>,
#
# myLwM2M is free software, this file is published under the MIT license as
# described in the accompanying LICENSE file.

import unittest
from lwm2m.persistence import InMemoryPersistence, Hasher


class HasherTest(unittest.TestCase):
    def test_create_same_hash_for_same_string(self):
        hasher = Hasher(b"123")
        hash1 = hasher.hash_for("endpoint")
        hash2 = hasher.hash_for("endpoint")
        self.assertEqual(hash1, hash2)


class InMemoryPersistenceTest(unittest.TestCase):
    def setUp(self):
        self.persistence = InMemoryPersistence(Hasher(b"123"))

    def test_created_persistence_has_no_clients(self):
        self.assertEqual(0, len([x for x in self.persistence.client_iterator()]))

    def test_lookup_client_by_location(self):
        self.assertFalse(self.persistence.has_client_with_location("location"))

    def test_lookup_client_by_endpoint_name(self):
        self.assertFalse(self.persistence.has_client_with_endpoint_name("endpoint"))

    def test_put_and_lookup_client_by_location(self):
        client = "client"
        self.persistence.put_client_by_location("location", client)
        self.assertTrue(self.persistence.has_client_with_location("location"))

    def test_put_and_lookup_client_by_location2(self):
        client = "client"
        self.persistence.put_client_by_endpoint_name("endpoint", client)
        self.assertTrue(self.persistence.has_client_with_location(Hasher(b"123").hash_for("endpoint")))

    def test_put_and_lookup_client_by_endpoint_name(self):
        client = "client"
        self.persistence.put_client_by_endpoint_name("endpoint", client)
        self.assertTrue(self.persistence.has_client_with_endpoint_name("endpoint"))

    def test_put_and_lookup_client_by_endpoint_name2(self):
        client = "client"
        self.persistence.put_client_by_location(Hasher(b"123").hash_for("endpoint"), client)
        self.assertTrue(self.persistence.has_client_with_endpoint_name("endpoint"))

    def test_get_and_put_client_by_location(self):
        client = "client"
        self.persistence.put_client_by_location("location", client)
        self.assertEqual(client, self.persistence.get_client_for_location("location"))

    def test_get_and_put_client_by_endpoint_name(self):
        client = "client"
        self.persistence.put_client_by_endpoint_name("endpoint", client)
        self.assertEqual(client, self.persistence.get_client_for_endpoint_name("endpoint"))

    def test_delete_client_by_endpoint_name(self):
        client = "client"
        self.persistence.put_client_by_endpoint_name("endpoint", client)
        self.persistence.delete_client_by_endpoint_name("endpoint")
        self.assertEqual(0, len([x for x in self.persistence.client_iterator()]))

    def test_delete_client_by_location(self):
        client = "client"
        self.persistence.put_client_by_endpoint_name("endpoint", client)
        self.persistence.delete_client_by_location(Hasher(b"123").hash_for("endpoint"))
        self.assertEqual(0, len([x for x in self.persistence.client_iterator()]))

    def test_client_iterator(self):
        self.persistence.put_client_by_endpoint_name("endpoint1", "client1")
        self.persistence.put_client_by_endpoint_name("endpoint2", "client2")
        self.assertEqual(2, len([x for x in self.persistence.client_iterator()]))

if __name__ == '__main__':
    unittest.main()