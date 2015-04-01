#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is a part of myLwM2M project.
#
# Copyright (c) 2015 Alexander Ellwein <mylwm2m@ellwein.net>,
#
# myLwM2M is free software, this file is published under the MIT license as
# described in the accompanying LICENSE file.

from lwm2m.persistence import InMemoryPersistence, Hasher
import pytest


def test_create_same_hash_for_same_string():
    hasher = Hasher(b"123")
    hash1 = hasher.hash_for("endpoint")
    hash2 = hasher.hash_for("endpoint")
    assert hash1 == hash2

@pytest.fixture
def persistence():
    return InMemoryPersistence(Hasher(b"123"))


def test_created_persistence_has_no_clients(persistence):
    assert 0 == len([x for x in persistence.client_iterator()])


def test_lookup_client_by_location(persistence):
    assert persistence.has_client_with_location("location") is False


def test_lookup_client_by_endpoint_name(persistence):
    assert persistence.has_client_with_endpoint_name("endpoint") is False


def test_put_and_lookup_client_by_location(persistence):
    client = "client"
    persistence.put_client_by_location("location", client)
    assert persistence.has_client_with_location("location") is True


def test_put_and_lookup_client_by_location2(persistence):
    client = "client"
    persistence.put_client_by_endpoint_name("endpoint", client)
    assert persistence.has_client_with_location(Hasher(b"123").hash_for("endpoint")) is True


def test_put_and_lookup_client_by_endpoint_name(persistence):
    client = "client"
    persistence.put_client_by_endpoint_name("endpoint", client)
    assert persistence.has_client_with_endpoint_name("endpoint") is True


def test_put_and_lookup_client_by_endpoint_name2(persistence):
    client = "client"
    persistence.put_client_by_location(Hasher(b"123").hash_for("endpoint"), client)
    assert persistence.has_client_with_endpoint_name("endpoint") is True


def test_get_and_put_client_by_location(persistence):
    client = "client"
    persistence.put_client_by_location("location", client)
    assert client == persistence.get_client_for_location("location")


def test_get_and_put_client_by_endpoint_name(persistence):
    client = "client"
    persistence.put_client_by_endpoint_name("endpoint", client)
    assert client == persistence.get_client_for_endpoint_name("endpoint")


def test_delete_client_by_endpoint_name(persistence):
    client = "client"
    persistence.put_client_by_endpoint_name("endpoint", client)
    persistence.delete_client_by_endpoint_name("endpoint")
    assert 0 == len([x for x in persistence.client_iterator()])


def test_delete_client_by_location(persistence):
    client = "client"
    persistence.put_client_by_endpoint_name("endpoint", client)
    persistence.delete_client_by_location(Hasher(b"123").hash_for("endpoint"))
    assert 0 == len([x for x in persistence.client_iterator()])


def test_client_iterator(persistence):
    persistence.put_client_by_endpoint_name("endpoint1", "client1")
    persistence.put_client_by_endpoint_name("endpoint2", "client2")
    assert 2 == len([x for x in persistence.client_iterator()])
