#!/usr/bin/env python

from setuptools import find_packages, setup
import versioneer

install_requires = [
    "astropy>=1.2",
    "lxml>=2.3, <4.0",
    'iso8601',
    'orderedmultidict',
    'pytz',
    'six',
]

setup(
    name="voevent-parse",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    package_data={'voeventparse': ['tests/resources/*.xml']},
    description="Convenience routines for parsing and manipulation of "
                "VOEvent XML packets.",
    author="Tim Staley",
    author_email="github@timstaley.co.uk",
    url="https://github.com/timstaley/voevent-parse",
    install_requires=install_requires,
)
