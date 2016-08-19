# -*- coding: utf-8 -*-
#
# This file is a part of etero project.
#
# Copyright (c) 2016 Alexander Ellwein <etero@ellwein.net>
#
# etero is free software, this file is published under the MIT license as
# described in the accompanying LICENSE file.

import os

from lwm2m.hasher import Sha256Hasher


def test_two_different_hashers_with_same_seed_produce_same_hash():
    u = os.urandom(30)
    h1 = Sha256Hasher(u)
    h2 = Sha256Hasher(u)
    assert h1.hash_for("teststring") == h2.hash_for("teststring"), "hashes must be the same"


def test_same_hasher_produces_always_a_same_hash_for_same_string():
    h1 = Sha256Hasher()
    h = h1.hash_for("teststring")
    for i in range(0, 1000):
        assert h == h1.hash_for("teststring"), "hash must always be the same"
