# -*- coding: utf-8 -*-
#
# This file is a part of etero project.
#
# Copyright (c) 2016 Alexander Ellwein <etero@ellwein.net>
#
# etero is free software, this file is published under the MIT license as
# described in the accompanying LICENSE file.

import pytest

from lwm2m.hasher import Sha256Hasher
from lwm2m.persistence import InMemoryPersistence


@pytest.fixture
def hasher():
    return Sha256Hasher()


@pytest.fixture
def persistence(hasher):
    return InMemoryPersistence(hasher)


def test_has_client_with_location(hasher, persistence):
    location = hasher.hash_for("myclient")
    assert persistence.has_client_with_location(location) is False
    persistence.put_client_for_location(location, dict())
    assert persistence.has_client_with_location(location)


def test_has_client_with_endpoint(persistence):
    assert persistence.has_client_with_endpoint_name("myclient") is False
    persistence.put_client_for_endpoint_name("myclient", dict())
    assert persistence.has_client_with_endpoint_name("myclient")


def test_get_client_for_location(hasher, persistence):
    location = hasher.hash_for("myclient")
    assert persistence.get_client_for_location(location) is None
    obj = dict()
    persistence.put_client_for_location(location, obj)
    assert id(persistence.get_client_for_location(location)) == id(obj), "the object is not the same"


def test_get_client_for_endpoint(persistence):
    assert persistence.get_client_for_endpoint_name("myclient") is None
    obj = dict()
    persistence.put_client_for_endpoint_name("myclient", obj)
    assert id(persistence.get_client_for_endpoint_name("myclient")) == id(obj), "the object is not the same"


def test_delete_client_for_location(hasher, persistence):
    location = hasher.hash_for("myclient")
    assert persistence.get_client_for_location(location) is None
    obj = dict()
    persistence.put_client_for_location(location, obj)
    assert id(persistence.get_client_for_location(location)) == id(obj), "the object is not the same"
    persistence.delete_client_for_location(location)
    assert persistence.get_client_for_location(location) is None


def test_delete_client_for_endpoint(persistence):
    assert persistence.get_client_for_endpoint_name("myclient") is None
    obj = dict()
    persistence.put_client_for_endpoint_name("myclient", obj)
    assert id(persistence.get_client_for_endpoint_name("myclient")) == id(obj), "the object is not the same"
    persistence.delete_client_for_endpoint_name("myclient")
    assert persistence.get_client_for_endpoint_name("myclient") is None
