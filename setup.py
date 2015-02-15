#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name="myLwM2M",
    version="1.0.0",
    description="Lightweight M2M server written in Python",
    author="Alexander Ellwein",
    author_email="mylwm2m@ellwein.net",
    license="MIT License",
    install_requires=["aiocoap"]
)