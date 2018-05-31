#!/usr/bin/env python3

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = open('VERSION', 'r').read()
long_description = (
    'autosub3 is a utility for automatic speech recognition and subtitle generation. It takes a video or an audio '
    'file as input, performs voice activity detection to find speech regions, makes parallel requests to Google Web '
    'Speech API to generate transcriptions for those regions, and finally saves the resulting subtitles to disk. It '
    'can currently produce subtitles in either the SRT, VTT format or simple JSON.'
)

setup(
    name='autosub3',
    version=version,
    description='Auto-generates subtitles for any video or audio file',
    long_description=long_description,
    author='Henry Wu',
    author_email='henry40408@gmail.com',
    url='https://github.com/henry40408/autosub3',
    packages=['autosub3'],
    entry_points={
        'console_scripts': [
            'autosub3 = autosub3:main',
        ],
    },
    install_requires=[
        'google-api-python-client>=1.4.2',
        'requests>=2.3.0',
        'pysrt>=1.0.1',
        'progressbar2>=3.34.3',
        'docopt>=0.6.2',
        'ffmpeg-python>=0.1.11'
    ],
    license=open("LICENSE").read(),
    python_requires='>=3.6.5'
)
