#!/usr/bin/env python
# Setup script for python-decontractors
# by Thomas Perl <thp.io/about>

from setuptools import setup

import re

contracts_py = open('contracts/__init__.py').read()
metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", contracts_py))
docstrings = re.findall('"""(.*)"""', contracts_py)

# Metadata fields extracted from decontractors.py
AUTHOR_EMAIL = metadata['author']
VERSION = metadata['version']
WEBSITE = metadata['website']
LICENSE = metadata['license']
DESCRIPTION = docstrings[0]

# Extract name and e-mail ("Firstname Lastname <mail@example.org>")
AUTHOR, EMAIL = re.match(r'(.*) <(.*)>', AUTHOR_EMAIL).groups()

setup(name='contracts',
    version=VERSION,
    description=DESCRIPTION,
    long_description=open('README.md').read(),
    keywords='dbc contract testing',
    author=AUTHOR,
    author_email=EMAIL,
    license=LICENSE,
    url=WEBSITE,
    packages=['contracts'],
    zip_safe=False,
    test_suite='nose.collector',
    tests_require=['nose'],
)
