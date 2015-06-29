#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='autosub',
    version='0.2',
    description='Auto-generates subtitles for any video or audio file',
    author='Anastasis Germanidis',
    author_email='agermanidis@gmail.com',
    url='https://github.com/agermanidis/autosub',
    packages=['autosub'],
    scripts=['bin/autosub'],
    install_requires=[
        'goslate>=1.4.0',
        'requests>=2.3.0',
        'pysrt>=1.0.1',
        'progressbar>=2.3'
    ],
    license="MIT"
)
