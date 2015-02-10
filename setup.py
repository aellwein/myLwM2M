#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name="lepton",
    version="1.0.0",
    description="Lightweight M2M lwm2m written in Python",
    author="Alexander Ellwein",
    author_email="lepton@ellwein.net",
    license="MIT License",
    install_requires=["aiocoap==0.1"]
)