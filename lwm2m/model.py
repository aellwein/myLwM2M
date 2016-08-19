# -*- coding: utf-8 -*-
#
# This file is a part of etero project.
#
# Copyright (c) 2016 Alexander Ellwein <etero@ellwein.net>
#
# etero is free software, this file is published under the MIT license as
# described in the accompanying LICENSE file.

import json

import logging
import os

log = logging.getLogger("model")


class JsonModelLoader:
    """
    This model loader is able to load LWM2M data model from a JSON file.
    """

    @staticmethod
    def load(fname=os.path.join(os.path.dirname(__file__), "lwm2m-model.json")):
        """
        Loads a LwM2M data model from JSON file with given name.
        :param fname: file name of JSON file
        :return: model object
        """
        with open(fname) as f:
            j = json.load(f)
        return j


class DataModel:
    """
    This object describes objects and resources structure which are understood by LwM2M server and client.
    The data model is used in order to parse and validate initial LwM2M client's data. The LwM2M data model is
    the common contract between server and client and therefore both client's and server's models have to be
    in sync with each other.
    """
    required_global_keys = (("lwm2m_version", str), ("ts_version", str), ("objects", dict))
    required_object_keys = (
        ("id", int), ("name", str), ("multiple", bool), ("mandatory", bool), ("urn", str), ("resources", dict))
    required_resource_keys = (
        ("id", int), ("name", str), ("operations", str), ("multiple", bool), ("mandatory", bool), ("type", str))
    valid_operations = ("R", "RW", "W", "E", "B")
    valid_types = ("string", "integer", "opaque", "time", "boolean", "objlink", "float")

    def __init__(self, model):
        """
        Creates a new LwM2M data model.
        """
        self._model = dict()
        self._data = dict()
        self._lwm2m_version = None
        self._ts_version = None
        self._validate_and_set(model)

    def _check_global_properties(self, c):
        for k in self.required_global_keys:
            assert k[0] in c, "global property '%s' is missing" % k[0]
            assert isinstance(c[k[0]], k[1]), "property '%s' is not of type %s" % (k[0], k[1])

    def _check_if_objects_empty(self, c):
        assert len(c["objects"]) > 0, "'objects' property may not be empty"

    def _check_if_resources_empty(self, obj):
        assert len(obj["resources"]) > 0, "'resources' property may not be empty"

    def _check_object_properties(self, obj_key, obj):
        for k in self.required_object_keys:
            assert k[0] in obj, "property '%s' is missing in object '%s'" % (k[0], obj_key)
            assert isinstance(obj[k[0]], k[1]), "property '%s' of object '%s' is not of type %s" % (k[0], obj_key, k[1])

    def _check_resource_properties(self, obj_key, res_key, res):
        for k in self.required_resource_keys:
            assert k[0] in res, "property '%s' is missing in resource '%s' of object '%s'" % (k[0], res_key, obj_key)
            assert isinstance(res[k[0]], k[1]), "property '%s' in resource '%s' of object '%s' is not of type %s" % (
                k[0], res_key, obj_key, k[1])

    def _check_operations(self, op, obj_key, res_key):
        assert op in self.valid_operations, "Invalid operations '%s' in object '%s', resource '%s'. Operations must be one of %s" % (
            op, obj_key, res_key, str(self.valid_operations))

    def _check_type(self, op, _type, obj_key, res_key):
        if op != "E":
            assert _type in self.valid_types, "object %s, resource %s: invalid type %s. Type must be one of %s" % (
                obj_key, res_key, _type, str(self.valid_types))

    def _validate_and_set(self, c):
        """
        Validate data definition content for required properties and correct types.
        :param c: data definition content
        """
        self._check_global_properties(c)
        self._check_if_objects_empty(c)
        for obj in c["objects"]:
            self._check_object_properties(obj, c["objects"][obj])
            self._check_if_resources_empty(c["objects"][obj])

            for res in c["objects"][obj]["resources"]:
                self._check_resource_properties(obj, res, c["objects"][obj]["resources"][res])
                self._check_operations(c["objects"][obj]["resources"][res]["operations"], obj, res)
                self._check_type(c["objects"][obj]["resources"][res]["operations"],
                                 c["objects"][obj]["resources"][res]["type"], obj, res)
            self._model[obj] = c["objects"][obj]

    def get_model(self):
        """
        :return: Data model content
        """
        return self._model
