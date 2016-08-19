# -*- coding: utf-8 -*-
#
# This file is a part of etero project.
#
# Copyright (c) 2016 Alexander Ellwein <etero@ellwein.net>
#
# etero is free software, this file is published under the MIT license as
# described in the accompanying LICENSE file.

import hashlib
import os

from abc import ABCMeta, abstractmethod


class Hasher(metaclass=ABCMeta):
    """
    The hasher object calculates a unique hash sum for a given string.
    """

    @abstractmethod
    def _seed(self):
        """
        :return: random seed which can be used within lifetime of this hasher.
        """
        pass

    @abstractmethod
    def hash_for(self, string):
        """
        Returns the hash sum for the given string
        :param string:
        :return:
        """
        pass


class Sha256Hasher(Hasher):
    """
    This implementation uses cryptographic hashes (SHA-256) for uniqueness.
    """

    def __init__(self, seed=None):
        """
        Creates a hasher with a given seed for uniqueness.
        :param seed:
        """
        self.seed = seed if seed else os.urandom(30)

    def _seed(self):
        return self.seed

    def hash_for(self, string):
        assert string and isinstance(string, str), "string argument is required"
        h = hashlib.new("sha256")
        h.update(string.encode())
        h.update(self._seed())
        return h.hexdigest()
