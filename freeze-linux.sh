#!/bin/bash

pipenv shell
pyinstaller main.py --path="$(pwd)" --add-binary="ffmpeg:." --add-data="pytranscriber/gui/*.qm:pytranscriber/gui/" --onefile --clean