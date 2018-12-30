#!/usr/bin/env python
from __future__ import absolute_import, print_function, unicode_literals

import argparse
import audioop
import json
import math
import multiprocessing
import os
import requests
import subprocess
import sys
import tempfile
import wave

from googleapiclient.discovery import build
from progressbar import ProgressBar, Percentage, Bar, ETA
from autosub.metadata import *
from autosub.constants import (
    LANGUAGE_CODES, GOOGLE_SPEECH_API_KEY, GOOGLE_SPEECH_API_URL,
    DEFAULT_CONCURRENCY, DEFAULT_SRC_LANGUAGE, DEFAULT_DST_LANGUAGE, DEFAULT_SUBTITLE_FORMAT
)
from autosub.formatters import FORMATTERS


def percentile(arr, percent):
    arr   = sorted(arr)
    index = (len(arr) - 1) * percent
    floor = math.floor(index)
    ceil  = math.ceil(index)

    if floor == ceil:
        return arr[int(index)]

    low_value  = arr[int(floor)] * (ceil - index)
    high_value = arr[int(ceil)] * (index - floor)

    return low_value + high_value


def is_same_language(lang1, lang2):
    return lang1.split("-")[0] == lang2.split("-")[0]


class ConsoleHelpFormatter(argparse.HelpFormatter):
    def _split_lines(self, text, width):
        return argparse.HelpFormatter._split_lines(self, text, width=70)


class FLACConverter(object):
    def __init__(self, source_path, include_before=0.25, include_after=0.25):
        self.source_path    = source_path
        self.include_before = include_before
        self.include_after  = include_after

    def __call__(self, region):
        try:
            start, end = region
            start      = max(0, start - self.include_before)
            end       += self.include_after

            temp    = tempfile.NamedTemporaryFile(suffix='.flac', delete=False)
            command = ["ffmpeg", "-ss", str(start), "-t", str(end - start),
                       "-y", "-i", self.source_path,
                       "-loglevel", "error", temp.name]
            use_shell = True if os.name == "nt" else False

            subprocess.check_output(command, stdin=open(os.devnull), shell=use_shell)

            return temp.read()

        except KeyboardInterrupt:
            return None


class SpeechRecognizer(object):
    def __init__(self, language=DEFAULT_SRC_LANGUAGE, rate=44100, retries=3, api_key=GOOGLE_SPEECH_API_KEY):
        self.language = language
        self.rate     = rate
        self.api_key  = api_key
        self.retries  = retries

    def __call__(self, data):
        try:
            for i in range(self.retries):
                url     = GOOGLE_SPEECH_API_URL.format(lang=self.language, key=self.api_key)
                headers = {"Content-Type": "audio/x-flac; rate=%d" % self.rate}

                try:
                    resp = requests.post(url, data=data, headers=headers)
                except requests.exceptions.ConnectionError:
                    continue

                for line in resp.content.decode('utf-8').split("\n"):
                    try:
                        line = json.loads(line)
                        line = line['result'][0]['alternative'][0]['transcript']
                        return line[:1].upper() + line[1:]
                    except:
                        # no result
                        continue
        except KeyboardInterrupt:
            return None


class Translator(object):
    def __init__(self, language, api_key, src, dst):
        self.language = language
        self.api_key  = api_key
        self.service  = build('translate', 'v2', developerKey=self.api_key)
        self.src      = src
        self.dst      = dst

    def __call__(self, sentence):
        try:
            if not sentence:
                return None

            result = self.service.translations().list(
                source=self.src,
                target=self.dst,
                q=[sentence]
            ).execute()

            if 'translations' in result and result['translations'] and \
                'translatedText' in result['translations'][0]:
                return result['translations'][0]['translatedText']

            return None
        except KeyboardInterrupt:
            return None


def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    if os.name == "nt":
        if ".exe" != program[-4:]:
            program = program + ".exe"

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path     = path.strip('"')
            exe_file = os.path.join(path, program)

            if is_exe(exe_file):
                return exe_file
    return None


def extract_audio(filename, channels=1, rate=16000):
    temp = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)

    if not os.path.isfile(filename):
        print("The given file does not exist: {}.".format(filename))
        raise Exception("Invalid filepath: {}.".format(filename))

    if not which("ffmpeg"):
        print("ffmpeg: Executable not found on machine.")
        raise Exception("Dependency not found: ffmpeg.")

    command = ["ffmpeg", "-y", "-i", filename,
               "-ac", str(channels), "-ar", str(rate),
               "-loglevel", "error", temp.name]
    use_shell = True if os.name == "nt" else False

    subprocess.check_output(command, stdin=open(os.devnull), shell=use_shell)

    return temp.name, rate


def find_speech_regions(filename, frame_width=4096, min_region_size=0.5, max_region_size=6):
    reader         = wave.open(filename)
    sample_width   = reader.getsampwidth()
    rate           = reader.getframerate()
    n_channels     = reader.getnchannels()
    chunk_duration = float(frame_width) / rate
    n_chunks       = int(math.ceil(reader.getnframes()*1.0 / frame_width))
    energies       = []

    for i in range(n_chunks):
        chunk = reader.readframes(frame_width)
        energies.append(audioop.rms(chunk, sample_width * n_channels))

    threshold    = percentile(energies, 0.2)
    elapsed_time = 0
    regions      = []
    region_start = None

    for energy in energies:
        is_silence   = energy <= threshold
        max_exceeded = region_start and elapsed_time - region_start >= max_region_size

        if (max_exceeded or is_silence) and region_start:
            if elapsed_time - region_start >= min_region_size:
                regions.append((region_start, elapsed_time))
                region_start = None
        elif (not region_start) and (not is_silence):
            region_start = elapsed_time

        elapsed_time += chunk_duration

    return regions


def generate_subtitles(source_path, output=None, concurrency=DEFAULT_CONCURRENCY, src_language=DEFAULT_SRC_LANGUAGE, dst_language=DEFAULT_DST_LANGUAGE, subtitle_file_format=DEFAULT_SUBTITLE_FORMAT, api_key=None):
    audio_filename, audio_rate = extract_audio(source_path)

    regions     = find_speech_regions(audio_filename)
    pool        = multiprocessing.Pool(concurrency)
    converter   = FLACConverter(source_path=audio_filename)
    recognizer  = SpeechRecognizer(language=src_language, rate=audio_rate, api_key=GOOGLE_SPEECH_API_KEY)
    transcripts = []

    if regions:
        try:
            widgets           = ["Converting speech regions to FLAC files: ", Percentage(), ' ', Bar(), ' ', ETA()]
            pbar              = ProgressBar(widgets=widgets, maxval=len(regions)).start()
            extracted_regions = []

            for i, extracted_region in enumerate(pool.imap(converter, regions)):
                extracted_regions.append(extracted_region)
                pbar.update(i)
            pbar.finish()

            widgets = ["Performing speech recognition: ", Percentage(), ' ', Bar(), ' ', ETA()]
            pbar    = ProgressBar(widgets=widgets, maxval=len(regions)).start()

            for i, transcript in enumerate(pool.imap(recognizer, extracted_regions)):
                transcripts.append(transcript)
                pbar.update(i)
            pbar.finish()

            if not is_same_language(src_language, dst_language):
                if api_key:
                    google_translate_api_key = api_key
                    translator               = Translator(dst_language, google_translate_api_key, dst=dst_language, src=src_language)
                    prompt                   = "Translating from {0} to {1}: ".format(src_language, dst_language)
                    widgets                  = [prompt, Percentage(), ' ', Bar(), ' ', ETA()]
                    pbar                     = ProgressBar(widgets=widgets, maxval=len(regions)).start()
                    translated_transcripts   = []

                    for i, transcript in enumerate(pool.imap(translator, transcripts)):
                        translated_transcripts.append(transcript)
                        pbar.update(i)
                    pbar.finish()

                    transcripts = translated_transcripts
                else:
                    print("Error: Subtitle translation requires specified Google Translate API key. See --help for further information.")
                    return 1

        except KeyboardInterrupt:
            pbar.finish()
            pool.terminate()
            pool.join()
            print("Cancelling transcription.")
            return 1

    timed_subtitles     = [(r, t) for r, t in zip(regions, transcripts) if t]
    formatter           = FORMATTERS.get(subtitle_file_format)
    formatted_subtitles = formatter(timed_subtitles)

    dest = output

    if not dest:
        base, ext = os.path.splitext(source_path)
        dest      = "{base}.{locale}.{format}".format(base=base, locale=dst_language, format=subtitle_file_format)

    with open(dest, 'wb') as output_file:
        output_file.write(formatted_subtitles.encode("utf-8"))

    os.remove(audio_filename)

    return dest


def validate(args):
    if args.format not in FORMATTERS.keys():
        print("Subtitle format not supported. Run with --list-formats to see all supported formats.")
        return False

    if args.src_language not in LANGUAGE_CODES.keys():
        print("Source language not supported. Run with --list-languages to see all supported languages.")
        return False

    if args.dst_language not in LANGUAGE_CODES.keys():
        print("Destination language not supported. Run with --list-languages to see all supported languages.")
        return False

    if not args.source_path:
        print("Error: You need to specify a source path.")
        return False

    return True


def main():
    parser = argparse.ArgumentParser(
        prog=metadata.name,
        usage='\n  %(prog)s [options] <source_path>',
        description=metadata.description,
        formatter_class=ConsoleHelpFormatter,
        add_help=False
    )

    pgroup = parser.add_argument_group('Required')
    ogroup = parser.add_argument_group('Options')

    pgroup.add_argument(
        'source_path',
        nargs='?',
        help="The path to the video or audio file needs to generate subtitle."
    )

    ogroup.add_argument(
        '-C', '--concurrency',
        metavar='<number>',
        type=int,
        default=DEFAULT_CONCURRENCY,
        help="Number of concurrent API requests to make (default: %(default)s)."
    )

    ogroup.add_argument(
        '-o', '--output',
        metavar='<path>',
        help="The output path for subtitle file. The default is in the same directory and the name is same as the source path."
    )

    ogroup.add_argument(
        '-F', '--format',
        metavar='<format>',
        default=DEFAULT_SUBTITLE_FORMAT,
        help="Destination subtitle format (default: %(default)s)."
    )

    ogroup.add_argument(
        '-S', '--src-language',
        metavar='<locale>',
        default=DEFAULT_SRC_LANGUAGE,
        help="Locale of language spoken in source file (default: %(default)s)."
    )

    ogroup.add_argument(
        '-D', '--dst-language',
        metavar='<locale>',
        default=DEFAULT_DST_LANGUAGE,
        help="Locale of desired language for the subtitles (default: %(default)s)."
    )

    ogroup.add_argument(
        '-K', '--api-key',
        metavar='<key>',
        help="The Google Translate API key to be used. Required for subtitle translation."
    )

    ogroup.add_argument(
        '-h', '--help',
        action='help',
        help="Show %(prog)s help message and exit."
    )

    ogroup.add_argument(
        '-V', '--version',
        action='version',
        version='%(prog)s ' + metadata.version + ' by ' + metadata.author + ' <' + metadata.author_email + '>',
        help="Show %(prog)s version and exit."
    )

    ogroup.add_argument(
        '--list-formats',
        action='store_true',
        help="List all available subtitle formats."
    )

    ogroup.add_argument(
        '--list-languages',
        action='store_true',
        help="List all available source/destination languages."
    )

    args = parser.parse_args()

    if args.list_formats:
        print("List of formats:")

        for subtitle_format in FORMATTERS.keys():
            print("{format}".format(format=subtitle_format))

        return 0

    if args.list_languages:
        print("List of all languages:")

        for code, language in sorted(LANGUAGE_CODES.items()):
            print("{code}\t{language}".format(code=code, language=language))

        return 0

    if not validate(args):
        return 1

    try:
        subtitle_file_path = generate_subtitles(
            source_path=args.source_path,
            output=args.output,
            concurrency=args.concurrency,
            src_language=args.src_language,
            dst_language=args.dst_language,
            subtitle_file_format=args.format,
            api_key=args.api_key
        )

        print("Subtitles file created at \"{}\"".format(subtitle_file_path))
    except KeyboardInterrupt:
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
