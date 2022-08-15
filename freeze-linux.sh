#!/bin/bash

pipenv shell
pyinstaller main.py --path="$(pwd)" --add-binary="ffmpeg:." --onefile --clean