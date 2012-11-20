#!/usr/bin/env python
# Setup script for pledge
# by Jason Horman <jhorman@gmail.com>

from setuptools import setup

import re

try:
    import multiprocessing
except ImportError:
    pass

# harddeal, hardeal, onus

pledge_py = open('pledge/__init__.py').read()
metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", pledge_py))

# Metadata fields extracted from decontractors.py
AUTHOR_EMAIL = metadata['author']
VERSION = metadata['version']
WEBSITE = metadata['website']
LICENSE = metadata['license']

# Extract name and e-mail ("Firstname Lastname <mail@example.org>")
AUTHOR, EMAIL = re.match(r'(.*) <(.*)>', AUTHOR_EMAIL).groups()

setup(name='pledge',
    version=VERSION,
    description='Lambda based design by contract (dbc)',
    keywords='dbc contract lambda testing',
    author=AUTHOR,
    author_email=EMAIL,
    license=LICENSE,
    url=WEBSITE,
    packages=['pledge'],
    zip_safe=False,
    test_suite='nose.collector',
    tests_require=['nose'],
)
