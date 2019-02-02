'''
   (C) 2019 Raryel C. Souza
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from pathlib import Path
from autosub import Autosub
from pyqtautosub.util.srtparser import SRTParser
from pyqtautosub.util.util import MyUtil
import os


class Thread_Exec_Autosub(QThread):
    signalLockGUI = pyqtSignal()
    signalResetGUI = pyqtSignal()
    signalProgress = pyqtSignal(str, int)
    signalProgressFileYofN = pyqtSignal(str)
    signalErrorMsg = pyqtSignal(str)

    def __init__(self, objParamAutosub):
        self.objParamAutosub = objParamAutosub
        self.running = True
        QThread.__init__(self)

    def __updateProgressFileYofN(self, currentIndex, countFiles ):
        self.signalProgressFileYofN.emit("File " + str(currentIndex+1) + " of " +str(countFiles))

    def listenerProgress(self, string, percent):
        self.signalProgress.emit(string, percent)

    def __generatePathOutputFile(self, sourceFile):
        #extract the filename without extension from the path
        base = os.path.basename(sourceFile)
        #[0] is filename, [1] is file extension
        fileName = os.path.splitext(base)[0]

        #the output file has same name as input file, located on output Folder
        #with extension .srt
        pathOutputFolder = Path(self.objParamAutosub.outputFolder)
        outputFileSRT = pathOutputFolder / (fileName + ".srt")
        outputFileTXT = pathOutputFolder / (fileName + ".txt")
        return [outputFileSRT, outputFileTXT]

    def __runAutosubForMedia(self, index, langCode):
        sourceFile = self.objParamAutosub.listFiles[index]
        outputFiles = self.__generatePathOutputFile(sourceFile)
        outputFileSRT = outputFiles[0]
        outputFileTXT = outputFiles[1]

        #run autosub
        fOutput = Autosub.generate_subtitles(source_path = sourceFile,
                                    output = outputFileSRT,
                                    src_language = langCode,
                                    dst_language = langCode,
                                    listener_progress = self.listenerProgress)
        #if nothing was returned
        if not fOutput:
            self.signalErrorMsg.emit("Error! Unable to generate subtitles for file " + sourceFile + ".")
        elif fOutput != -1:
            #if the operation was not canceled

            #updated the progress message
            self.listenerProgress("Finished", 100)

            #parses the .srt subtitle file and export text to .txt file
            SRTParser.extractTextFromSRT(str(outputFileSRT))

            #open both SRT and TXT output files
            MyUtil.open_file(outputFileTXT)
            MyUtil.open_file(outputFileSRT)

    def __loopSelectedFiles(self):
        self.signalLockGUI.emit()

        langCode = self.objParamAutosub.langCode

        #if output directory does not exist, creates it
        pathOutputFolder = Path(self.objParamAutosub.outputFolder)

        if not os.path.exists(pathOutputFolder):
            os.mkdir(pathOutputFolder)
        #if there the output file is not a directory
        if not os.path.isdir(pathOutputFolder):
            #force the user to select a different output directory
            self.signalErrorMsg.emit("Error! Invalid output folder. Please choose another one.")
        else:
            #go ahead with autosub process
            nFiles = len(self.objParamAutosub.listFiles)
            for i in range(nFiles):
                self.__updateProgressFileYofN(i, nFiles)
                self.__runAutosubForMedia(i, langCode)

            self.signalResetGUI.emit()

    def run(self):
        self.__loopSelectedFiles()
        self.running = False

    def cancel(self):
        Autosub.cancel_operation()
