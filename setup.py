#!/usr/bin/env python
from __future__ import unicode_literals

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

metadata = {}

with open("autosub/metadata.py") as metafile:
    exec(metafile.read(), metadata)

setup(
    name=metadata['NAME'],
    version=metadata['VERSION'],
    description=metadata['DESCRIPTION'],
    long_description=metadata['LONG_DESCRIPTION'],
    author=metadata['AUTHOR'],
    author_email=metadata['AUTHOR_EMAIL'],
    url=metadata['HOMEPAGE'],
    packages=['autosub'],
    entry_points={
        'console_scripts': [
            'autosub = autosub:main',
        ],
    },
    install_requires=[
        'google-api-python-client>=1.4.2',
        'requests>=2.3.0',
        'pysrt>=1.0.1',
        'progressbar2>=3.34.3',
        'six>=1.11.0',
    ],
    license=open("LICENSE").read()
)
