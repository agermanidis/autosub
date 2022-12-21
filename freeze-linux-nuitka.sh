#!/bin/bash

pipenv shell
nuitka3 --enable-plugin=pyqt5 --include-data-files="ffmpeg"="./" --include-data-files="pytranscriber/gui/*.qm"="pytranscriber/gui/"  main.py --onefile