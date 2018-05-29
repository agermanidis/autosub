# autosub3

> Auto-generated subtitles for any video

autosub3 is a utility for automatic speech recognition and subtitle generation. It takes a video or an audio file as input, performs voice activity detection to find speech regions, makes parallel requests to Google Web Speech API to generate transcriptions for those regions, and finally saves the resulting subtitles to disk. It can currently produce subtitles in either the SRT, VTT format or simple JSON.

### Installation

1. Install [ffmpeg](https://www.ffmpeg.org/).
2. Run `pip install autosub`.

### Usage

```
$ autosub3 -h
Usage:
  autosub3.py -h | --help
  autosub3.py --list-formats
  autosub3.py --list-languages
  autosub3.py [options] <source>

Options:
  -h --help                         Show this screen
  -C --concurrency=<concurrency>    Number of concurrent API requests to make [default: 10]
  -o --output=<output>              Output path for subtitles (by default, subtitles are saved in the same directory and name as the source path)
  -F --format=<format>              Destination subtitle format [default: srt]
  -S --src-language=<language>      Language spoken in source file [default: en]
  --list-formats                    List all available subtitle formats
  --list-languages                  List all available source languages
```

### License

MIT
