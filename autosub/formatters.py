# -*- coding: utf-8 -*-
import sys
import json

import pysrt

text_type = unicode if sys.version_info < (3,) else str


def force_unicode(s, encoding="utf-8"):
    if isinstance(s, text_type):
        return s
    return s.decode(encoding)


def srt_formatter(subtitles, show_before=0, show_after=0):
    f = pysrt.SubRipFile()
    for (rng, text) in subtitles:
        item = pysrt.SubRipItem()
        item.text = force_unicode(text)
        start, end = rng
        item.start.seconds = max(0, start - show_before)
        item.end.seconds = end + show_after
        f.append(item)
    return '\n'.join(map(unicode, f))
        
def json_formatter(subtitles):
    subtitle_dicts = map(lambda (r, t): {'start': r[0], 'end': r[1], 'content': t}, subtitles)
    return json.dumps(subtitle_dicts)

def raw_formatter(subtitles):
    return ' '.join(map(lambda (rng, text): text, subtitles))

FORMATTERS = {
    'srt': srt_formatter,
    'json': json_formatter,
    'raw': raw_formatter,
}
