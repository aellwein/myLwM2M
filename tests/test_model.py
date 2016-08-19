# -*- coding: utf-8 -*-
#
# This file is a part of etero project.
#
# Copyright (c) 2016 Alexander Ellwein <etero@ellwein.net>
#
# etero is free software, this file is published under the MIT license as
# described in the accompanying LICENSE file.

import pytest

from lwm2m.model import DataModel, JsonModelLoader


@pytest.fixture
def model():
    return JsonModelLoader.load()


def test_load_model_from_json_file(model):
    m = DataModel(model)
    assert len(m.get_model()) > 0, "model may not be empty"


def test_set_model_content_without_any_globally_required_property():
    _required = ("lwm2m_version", "ts_version", "objects")
    for r in _required:
        m = model()
        del m[r]
        with pytest.raises(AssertionError):
            DataModel(m)


def test_set_model_content_with_empty_objects(model):
    model["objects"] = {}
    with pytest.raises(AssertionError):
        DataModel(model)


def test_set_model_content_without_any_required_object_property():
    _required = ("id", "name", "multiple", "mandatory", "urn", "resources")
    for r in _required:
        m = model()
        del m["objects"]["0"][r]
        with pytest.raises(AssertionError):
            DataModel(m)


def test_set_model_content_with_empty_resources(model):
    model["objects"]["0"]["resources"] = {}
    with pytest.raises(AssertionError):
        DataModel(model)


def test_set_model_content_without_any_required_resource_property():
    _required = ("id", "name", "operations", "multiple", "mandatory", "type")
    for r in _required:
        m = model()
        del m["objects"]["0"]["resources"]["0"][r]
        with pytest.raises(AssertionError):
            DataModel(m)
