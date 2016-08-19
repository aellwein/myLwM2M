#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools_behave import behave_test

setup(
    name="etero",
    version="0.0.0+git",
    url="https://bitbucket.org/aellwein/etero",
    author="Alexander Ellwein",
    author_email="etero@ellwein.net",
    setup_requires=["pytest-runner"],
    # TODO until behave 1.2.6 is released in PyPi
    tests_require=["behave==1.2.6.dev0", "pytest"],
    cmdclass={"behave_test": behave_test}
)
