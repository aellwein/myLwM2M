#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is a part of myLwM2M project.
#
# Copyright (c) 2015 Alexander Ellwein <myLwM2M@ellwein.net>,
#
# myLwM2M is free software, this file is published under the MIT license as
# described in the accompanying LICENSE file.

import pytest
import aiocoap
from aiocoap.numbers.codes import Code
import asyncio
from lwm2m.persistence import InMemoryPersistence, Hasher
from lwm2m.server import Server


@pytest.fixture
def server():
        persistence = InMemoryPersistence
        hasher = Hasher(b"123")
        return Server(persistence, hasher)


def test_server_contains_site_with_rd_resource(server):
    assert server == server.site._resources[(Server.get_path(),)]


def test_post_without_endpoint_leads_to_bad_request_response(server):
    message = aiocoap.Message()
    response = server.render_post(message)
    assert Code.BAD_REQUEST == asyncio.get_event_loop().run_until_complete(response).code


def test_post_without_payload_leads_to_bad_request_response(server):
    message = aiocoap.Message()
    message.opt.uri_query = ["ep=endpoint"]
    response = server.render_post(message)
    assert Code.BAD_REQUEST == asyncio.get_event_loop().run_until_complete(response).code


def test_client_is_persisted_after_registration(server):
    message = aiocoap.Message()
    message.opt.uri_query = ["ep=endpoint"]
    message.payload = b"</3>,</0/1>"
    response = server.render_post(message)
    assert Code.CREATED == asyncio.get_event_loop().run_until_complete(response).code