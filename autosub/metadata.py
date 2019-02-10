#!/usr/bin/env python

NAME             = 'autosub'
VERSION          = '0.4.0'
DESCRIPTION      = 'Auto-generates subtitles for any video or audio file.'
LONG_DESCRIPTION = (
    'Autosub is a utility for automatic speech recognition and subtitle generation. '
    'It takes a video or an audio file as input, performs voice activity detection '
    'to find speech regions, makes parallel requests to Google Web Speech API to '
    'generate transcriptions for those regions, (optionally) translates them to a '
    'different language, and finally saves the resulting subtitles to disk. It '
    'supports a variety of input and output languages (to see which, run the '
    'utility with the argument --list-languages) and can currently produce '
    'subtitles in either the SRT format or simple JSON.'
)
AUTHOR       = 'Anastasis Germanidis'
AUTHOR_EMAIL = 'agermanidis@gmail.com'
HOMEPAGE     = 'https://github.com/agermanidis/autosub'
