"""
Defines subtitle formatters used by autosub.
"""

# -*- coding: utf-8 -*-


import json

import pysrt
import six


def srt_formatter(subtitles, padding_before=0, padding_after=0):
    """
    Serialize a list of subtitles according to the SRT format, with optional time padding.
    """
    sub_rip_file = pysrt.SubRipFile()
    for i, ((start, end), text) in enumerate(subtitles, start=1):
        item = pysrt.SubRipItem()
        item.index = i
        item.text = six.text_type(text)
        item.start.seconds = max(0, start - padding_before)
        item.end.seconds = end + padding_after
        sub_rip_file.append(item)
    return '\n'.join(six.text_type(item) for item in sub_rip_file)


def vtt_formatter(subtitles, padding_before=0, padding_after=0):
    """
    Serialize a list of subtitles according to the VTT format, with optional time padding.
    """
    text = srt_formatter(subtitles, padding_before, padding_after)
    text = 'WEBVTT\n\n' + text.replace(',', '.')
    return text


def json_formatter(subtitles):
    """
    Serialize a list of subtitles as a JSON blob.
    """
    subtitle_dicts = [
        {
            'start': start,
            'end': end,
            'content': text,
        }
        for ((start, end), text)
        in subtitles
    ]
    return json.dumps(subtitle_dicts)


def raw_formatter(subtitles):
    """
    Serialize a list of subtitles as a newline-delimited string.
    """
    return ' '.join(text for (_rng, text) in subtitles)


FORMATTERS = {
    'srt': srt_formatter,
    'vtt': vtt_formatter,
    'json': json_formatter,
    'raw': raw_formatter,
}
