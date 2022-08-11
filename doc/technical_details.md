<h1>For Developers - Technical Details</h1>

This app consists basically of a friendly pyQt5 graphical interface for a customized version of <a href="https://github.com/agermanidis/autosub">Autosub 0.4.0</a> that can run on Linux, Windows and MacOS. All the hard work of processing the audio and generating the subtitles is done by Autosub.

<h2>Dependencies</h2>

<ol>
<li>pip3 install pipenv
<li>pipenv install (install all dependencies from Pipfile)
<li>Download the static ffmpeg binary and put on project root folder or install system wide
</ol>

# How to run?
$ pipenv shell
$ python3 main.py


# How to edit the GUI?
Install Qt5 Designer and open the file pytranscriber/gui/gui.ui

# How to convert the .ui file (qt5designer project file) to .py?
$ pyuic5 gui.ui -o gui.py

# How to generate the python bundled binary package version with ffmpeg included?

# Linux:
$ pyinstaller main.py --path="$(pwd)" --add-binary="ffmpeg:." --onefile --clean

# Windows:
$ pyinstaller main.py --path=$pwd --add-binary="ffmpeg;." --onefile --clean

The output binary will be on subfolder dist/main and has all dependencies included. For more details check pyinstaller documentation

# On Linux how to generate a statically linked binary so it can run even on systems with older glibc installed?

As explained in <a href=https://github.com/pyinstaller/pyinstaller/wiki/FAQ>pyInstaller FAQ</a>:
> The executable that PyInstaller builds is not fully static, in that it still depends on the system libc. Under Linux, the ABI of GLIBC is backward compatible, but not forward compatible. So if you link against a newer GLIBC, you can't run the resulting executable on an older system.

> <b>Solution 1)</b>To compile the Python interpreter with its modules (and also probably bootloader) on the oldest system you have around, so that it gets linked with the oldest version of GLIBC.

> <b>Solution 2)</b> to use a tool like StaticX to create a fully-static bundled version of your PyInstaller application. StaticX bundles all dependencies, including libc and ld.so. (Python code :arrow_right: PyInstaller :arrow_right: StaticX :arrow_right: Fully-static application)"

<b>Install staticx and patchelf (dependency)</b>

$ pip3 install --user patchelf-wrapper
 
$ pip3 install --user staticx

<b>After generating the binary with pyinstaller, open the dist folder and run: </b>

$ staticx main main-static

The newly created main-static contains all library dependencies, including glibc, so it should be able to run even on very old systems.

Note: In my Manjaro system the first time I run this command I got an error related to "libmpdec.so.2 => not found". Installing the package <b>mpdecimal</b> on the package manager solved the issue.
