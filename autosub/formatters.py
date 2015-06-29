import json
import pysrt

def srt_formatter(subtitles, show_before=0, show_after=0):
    f = pysrt.SubRipFile()
    for (rng, text) in subtitles:
        item = pysrt.SubRipItem()
        item.text = text
        start, end = rng
        item.start.seconds = max(0, start - show_before)
        item.end.seconds = end + show_after
        f.append(item)
    return '\n'.join(map(str, f))
        
def json_formatter(subtitles):
    subtitle_dicts = map(lambda (r, t): {'start': r[0], 'end': r[1], 'content': t}, subtitles)
    return json.dumps(subtitle_dicts)

FORMATTERS = {
    'srt': srt_formatter,
    'json': json_formatter,
}
