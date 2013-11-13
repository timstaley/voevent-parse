#!/usr/bin/env python

from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="voevent-parse",
    version="0.5.1",
    packages=['voeparse', 'voeparse.tests', 'voeparse.tests.resources'],
    package_data={'voeparse':['tests/resources/*.xml']}, 
    description="Convenience routines for parsing and manipulation of "
                "VOEvent XML packets.",
    author="Tim Staley",
    author_email="timstaley337@gmail.com",
    url="https://github.com/timstaley/voevent-parse",
    install_requires=required,
    test_suite='voeparse.tests'
)
