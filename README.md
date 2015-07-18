# Autosub <a href="https://pypi.python.org/pypi/autosub"><img src="https://img.shields.io/pypi/v/autosub.svg"></img></a> <a href="https://pypi.python.org/pypi/autosub"><img src="https://img.shields.io/pypi/dm/autosub.svg"></img></a>
### Auto-generated subtitles for any video

Autosub is a utility for automatic speech recognition and subtitle generation. It takes a video or an audio file as input, performs voice activity detection to find speech regions, makes parallel requests to Google Web Speech API to generate transcriptions for those regions, (optionally) translates them to a different language, and finally saves the resulting subtitles to disk. It supports a variety of input and output languages (to see which, run the utility with `--list-src-languages` and `--list-dst-languages` as arguments respectively) and can currently produce subtitles in either the SRT format or simple JSON.

### Installation

1. Install [ffmpeg](https://www.ffmpeg.org/).
2. Run `pip install autosub`.

### Usage

```
$ autosub -h
usage: autosub [-h] [-C CONCURRENCY] [-o OUTPUT] [-F FORMAT] [-S SRC_LANGUAGE]
               [-D DST_LANGUAGE] [--list-formats] [--list-src-languages]
               [--list-dst-languages]
               source_path

positional arguments:
  source_path           Path to the video or audio file

optional arguments:
  -h, --help            show this help message and exit
  -C CONCURRENCY, --concurrency CONCURRENCY
                        Number of concurrent API requests to make
  -o OUTPUT, --output OUTPUT
                        Output path for subtitles (by default, subtitles are
                        saved in the same directory and name as the source
                        path)
  -F FORMAT, --format FORMAT
                        Destination subtitle format
  -S SRC_LANGUAGE, --src-language SRC_LANGUAGE
                        Language spoken in source file
  -D DST_LANGUAGE, --dst-language DST_LANGUAGE
                        Desired language for the subtitles
  --list-formats        List all available subtitle formats
  --list-src-languages  List all available source languages
  --list-dst-languages  List all available destination languages
```

### License

MIT
