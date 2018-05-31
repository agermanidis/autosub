import json

import pysrt


def srt_formatter(subtitles, show_before=0, show_after=0):
    sub_rip_file = pysrt.SubRipFile()
    for i, ((start, end), text) in enumerate(subtitles, start=1):
        item = pysrt.SubRipItem()
        item.index = i
        item.text = str(text)
        item.start.seconds = max(0, start - show_before)
        item.end.seconds = end + show_after
        sub_rip_file.append(item)
    return '\n'.join(str(item) for item in sub_rip_file)


def vtt_formatter(subtitles, show_before=0, show_after=0):
    text = srt_formatter(subtitles, show_before, show_after)
    text = 'WEBVTT\n\n' + text.replace(',', '.')
    return text


def json_formatter(subtitles):
    return json.dumps([{
        'start': start,
        'end': end,
        'content': text
    } for ((start, end), text) in subtitles])


def raw_formatter(subtitles):
    return ' '.join(text for (_rng, text) in subtitles)


FORMATTERS = {
    'srt': srt_formatter,
    'vtt': vtt_formatter,
    'json': json_formatter,
    'raw': raw_formatter,
}
