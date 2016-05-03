#!/usr/bin/env python

from setuptools import setup
import versioneer

setup(
    name="voevent-parse",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=['voeventparse', 'voeventparse.tests', 'voeventparse.tests.resources'],
    package_data={'voeventparse':['tests/resources/*.xml']},
    description="Convenience routines for parsing and manipulation of "
                "VOEvent XML packets.",
    author="Tim Staley",
    author_email="timstaley337@gmail.com",
    url="https://github.com/timstaley/voevent-parse",
    install_requires=["lxml>=2.3, <4.0",
                      'six',
                      'iso8601',
                      ],
    test_suite='voeventparse.tests'
)
