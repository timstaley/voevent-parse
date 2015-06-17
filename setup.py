#!/usr/bin/env python

from setuptools import setup

setup(
    name="voevent-parse",
    version="0.8.1",
    packages=['voeventparse', 'voeventparse.tests', 'voeventparse.tests.resources'],
    package_data={'voeventparse':['tests/resources/*.xml']},
    description="Convenience routines for parsing and manipulation of "
                "VOEvent XML packets.",
    author="Tim Staley",
    author_email="timstaley337@gmail.com",
    url="https://github.com/timstaley/voevent-parse",
    install_requires=["lxml>=2.3, <4.0",
                      'six'
                      ],
    test_suite='voeventparse.tests'
)
