<h1>For Developers - Technical Details</h1>

This app consists basically of a friendly pyQt5 graphical interface for a customized version of <a href="https://github.com/agermanidis/autosub">Autosub 0.4.0</a> that can run on Linux, Windows and MacOS. All the hard work of processing the audio and generating the subtitles is done by Autosub.

<h2>Dependencies</h2>

<ol>
<li>pip3 install --user pyQt5
<li>pip3 install --user autosub
<li>pip3 install --user pyinstaller (only for generating bundled binary)
<li>Download the static ffmpeg binary and put on project root folder or install system wide
</ol>

# How to run?
$ python3 main.py

# How to edit the GUI?
Install Qt5 Designer and open the file pytranscriber/gui/gui.ui

# How to convert the .ui file (qt5designer project file) to .py?
$ pyuic5 gui.ui -o gui.py

# How to generate the python bundled binary package version?
$ pyinstaller --onefile main.py

Note: At least in my Manjaro system running latest python I need to add some extra parameters like as follows to be able to run the generated binary:
<br>
$ pyinstaller --onefile main.py --hidden-import='packaging.version' --hidden-import='packaging.specifiers' --hidden-import='packaging.requirements'


The output binary will be on subfolder dist/main and has all dependencies included. For more details check pyinstaller documentation
