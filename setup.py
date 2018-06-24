#!/usr/bin/env python

from setuptools import find_packages, setup
import versioneer

install_requires = [
    "astropy>=1.2",
    "lxml>=2.3",
    'iso8601',
    'orderedmultidict',
    'pytz',
    'six',
]

test_requires = [
    'pytest>3',
    'coverage'
]

extras_require = {
    'test': test_requires,
    'all': test_requires,
}

setup(
    name="voevent-parse",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    package_data={'voeventparse': ['fixtures/*.xml']},
    description="Convenience routines for parsing and manipulation of "
                "VOEvent XML packets.",
    author="Tim Staley",
    author_email="github@timstaley.co.uk",
    url="https://github.com/timstaley/voevent-parse",
    install_requires=install_requires,
    extras_require=extras_require,
)
