#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is a part of etero project.
#
# Copyright (c) 2016 Alexander Ellwein <etero@ellwein.net>
#
# etero is free software, this file is published under the MIT license as
# described in the accompanying LICENSE file.

import logging

from lwm2m.model import DataModel, ModelLoader

log = logging.getLogger("client")


class Client:
    def __init__(self, model=None):
        log.info("__init__()")
        self.model = model if model else DataModel(ModelLoader.load_json())


def main():
    log.setLevel(logging.DEBUG)
    client = Client()


if __name__ == '__main__':
    main()
