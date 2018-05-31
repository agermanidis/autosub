#!/usr/bin/env python3

"""
Usage:
  autosub3.py -h | --help
  autosub3.py --list-formats
  autosub3.py --list-languages
  autosub3.py [options] <source>

Options:
  -h --help                         Show this screen
  -q --quiet                        Do NOT show progress bar
  -C --concurrency=<concurrency>    Number of concurrent API requests to make [default: 10]
  -o --output=<output>              Output path for subtitles (by default, subtitles are saved in the same directory and
                                    name as the source path)
  -F --format=<format>              Destination subtitle format [default: srt]
  -S --src-language=<language>      Language spoken in source file [default: en]
  --list-formats                    List all available subtitle formats
  --list-languages                  List all available source languages
"""

import audioop
import json
import math
import multiprocessing
import os
import sys
import tempfile
import wave
from json import JSONDecodeError
from typing import List

import docopt
import ffmpeg
import requests
from progressbar import Percentage, Bar, ETA

from autosub3.constants import LANGUAGE_CODES, GOOGLE_SPEECH_API_KEY, GOOGLE_SPEECH_API_URL
from autosub3.formatters import FORMATTERS
from autosub3.optional_progressbar import OptionalProgressBar

DEFAULT_SUBTITLE_FORMAT = 'srt'
DEFAULT_CONCURRENCY = 10
DEFAULT_SRC_LANGUAGE = 'en'
DEFAULT_DST_LANGUAGE = 'en'


def percentile(arr: List, percent: float):
    if not arr:
        raise RuntimeError('array cannot be empty')

    arr = sorted(arr)
    k = (len(arr) - 1) * percent
    f = math.floor(k)
    c = math.ceil(k)

    if f == c:
        return arr[int(k)]

    d0 = arr[int(f)] * (c - k)
    d1 = arr[int(c)] * (k - f)
    return d0 + d1


class FLACConverter(object):
    def __init__(self, source_path, include_before=0.25, include_after=0.25):
        self.source_path = source_path
        self.include_before = include_before
        self.include_after = include_after

    def __call__(self, region):
        try:
            start, end = region
            start = max(0, start - self.include_before)
            end += self.include_after
            temp = tempfile.NamedTemporaryFile(suffix='.flac')
            stream = ffmpeg.input(self.source_path)
            stream = ffmpeg.output(stream, temp.name, ss=start, t=end - start, loglevel='error')
            ffmpeg.run(stream, overwrite_output=True)
            return temp.read()

        except KeyboardInterrupt:
            return


class SpeechRecognizer(object):
    def __init__(self, language='en', rate=44100, retries=3, api_key=GOOGLE_SPEECH_API_KEY):
        self.language = language
        self.rate = rate
        self.api_key = api_key
        self.retries = retries

    def __call__(self, data):
        try:
            for i in range(self.retries):
                url = GOOGLE_SPEECH_API_URL.format(lang=self.language, key=self.api_key)
                headers = {'Content-Type': 'audio/x-flac; rate=%d' % self.rate}

                try:
                    resp = requests.post(url, data=data, headers=headers)
                except requests.exceptions.ConnectionError:
                    continue

                for line in resp.content.decode().split('\n'):
                    try:
                        line = json.loads(line)
                        line = line['result'][0]['alternative'][0]['transcript']
                        return line[:1].upper() + line[1:]
                    except (IndexError, JSONDecodeError, KeyError):
                        # no result
                        continue

        except KeyboardInterrupt:
            return


def extract_audio(filename, channels=1, rate=16000):
    temp = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    if not os.path.isfile(filename):
        raise RuntimeError('The given file does not exist: {0}'.format(filename))
    stream = ffmpeg.input(filename)
    stream = ffmpeg.output(stream, temp.name, ac=channels, ar=rate, loglevel='error')
    ffmpeg.run(stream, overwrite_output=True)
    return temp.name, rate


def find_speech_regions(filename, frame_width=4096, min_region_size=0.5, max_region_size=6):
    reader = wave.open(filename)
    sample_width = reader.getsampwidth()
    rate = reader.getframerate()
    n_channels = reader.getnchannels()
    chunk_duration = float(frame_width) / rate

    n_chunks = int(math.ceil(reader.getnframes() * 1.0 / frame_width))
    energies = []

    for i in range(n_chunks):
        chunk = reader.readframes(frame_width)
        energies.append(audioop.rms(chunk, sample_width * n_channels))

    threshold = percentile(energies, 0.2)

    elapsed_time = 0

    regions = []
    region_start = None

    for energy in energies:
        is_silence = energy <= threshold
        max_exceeded = region_start and elapsed_time - region_start >= max_region_size
        if (max_exceeded or is_silence) and region_start:
            if elapsed_time - region_start >= min_region_size:
                regions.append((region_start, elapsed_time))
                region_start = None
        elif (not region_start) and (not is_silence):
            region_start = elapsed_time
        elapsed_time += chunk_duration

    return regions


def main():
    version = open('VERSION', 'r').read()
    args = docopt.docopt(__doc__, version=version)

    if args['--list-formats']:
        for subtitle_format in FORMATTERS.keys():
            print('{format}'.format(format=subtitle_format))
        return 0

    if args['--list-languages']:
        for code, language in sorted(LANGUAGE_CODES.items()):
            print('{code}\t{language}'.format(code=code, language=language))
        return 0

    if args['--format'] not in FORMATTERS.keys():
        print(
            'Subtitle format not supported. '
            'Run with --list-formats to see all supported formats.'
        )
        return 1

    if args['--src-language'] not in LANGUAGE_CODES.keys():
        print(
            'Source language not supported. '
            'Run with --list-languages to see all supported languages.'
        )
        return 1

    verbose = not args['--quiet']
    try:
        subtitle_file_path = generate_subtitles(args['<source>'],
                                                concurrency=int(args['--concurrency']),
                                                src_language=args['--src-language'],
                                                subtitle_file_format=args['--format'],
                                                output=args['--output'],
                                                verbose=verbose)
        print('Subtitles file created at {subtitle_file_path}'.format(subtitle_file_path=subtitle_file_path))
    except KeyboardInterrupt:
        return 1

    return 0


def generate_subtitles(source_path, *,
                       concurrency=DEFAULT_CONCURRENCY,
                       src_language=DEFAULT_SRC_LANGUAGE,
                       subtitle_file_format=DEFAULT_SUBTITLE_FORMAT,
                       output=None,
                       verbose=False):
    audio_filename, audio_rate = extract_audio(source_path)
    regions = find_speech_regions(audio_filename)
    pool = multiprocessing.Pool(concurrency)
    converter = FLACConverter(source_path=audio_filename)
    recognizer = SpeechRecognizer(language=src_language,
                                  rate=audio_rate,
                                  api_key=GOOGLE_SPEECH_API_KEY)

    transcripts = []
    if regions:
        widgets = ['Converting speech regions to FLAC files: ', Percentage(), ' ', Bar(), ' ', ETA()]
        p_bar = OptionalProgressBar(verbose=verbose, widgets=widgets, maxval=len(regions))

        try:
            p_bar.start()
            extracted_regions = []
            for i, extracted_region in enumerate(pool.imap(converter, regions)):
                extracted_regions.append(extracted_region)
                p_bar.update(i)
            p_bar.finish()

            widgets = ['Performing speech recognition: ', Percentage(), ' ', Bar(), ' ', ETA()]
            p_bar = OptionalProgressBar(verbose=verbose, widgets=widgets, maxval=len(regions)).start()

            for i, transcript in enumerate(pool.imap(recognizer, extracted_regions)):
                transcripts.append(transcript)
                p_bar.update(i)
            p_bar.finish()
        except KeyboardInterrupt:
            p_bar.finish()
            pool.terminate()
            pool.join()
            print('Cancelling transcription')
            raise

    timed_subtitles = [(r, t) for r, t in zip(regions, transcripts) if t]
    formatter = FORMATTERS.get(subtitle_file_format)
    formatted_subtitles = formatter(timed_subtitles)

    destination = output
    if not destination:
        base, ext = os.path.splitext(source_path)
        destination = '{base}.{format}'.format(base=base, format=subtitle_file_format)

    with open(destination, 'wb') as f:
        f.write(formatted_subtitles.encode('utf-8'))

    os.remove(audio_filename)

    return destination


if __name__ == '__main__':
    sys.exit(main())
