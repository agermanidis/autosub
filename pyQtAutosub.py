# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pyQtAutosub.ui'
#
# Created by: PyQt5 UI code generator 5.12.dev1812231618
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from pathlib import Path
from autosub import generate_subtitles
from threading import Thread
from srtparser import SRTParser
import os
import platform
import subprocess

class Ui_window(object):
    def setupUi(self, window):
        window.setObjectName("window")
        window.resize(1045, 420)
        self.centralwidget = QtWidgets.QWidget(window)
        self.centralwidget.setObjectName("centralwidget")
        self.bSelectMedia = QtWidgets.QPushButton(self.centralwidget)
        self.bSelectMedia.setGeometry(QtCore.QRect(10, 10, 141, 34))
        self.bSelectMedia.setObjectName("bSelectMedia")
        self.bRemoveFile = QtWidgets.QPushButton(self.centralwidget)
        self.bRemoveFile.setGeometry(QtCore.QRect(10, 50, 141, 34))
        self.bRemoveFile.setObjectName("bRemoveFile")
        self.cbSelectLang = QtWidgets.QComboBox(self.centralwidget)
        self.cbSelectLang.setGeometry(QtCore.QRect(550, 230, 161, 32))
        self.cbSelectLang.setObjectName("cbSelectLang")
        self.labelSelectLang = QtWidgets.QLabel(self.centralwidget)
        self.labelSelectLang.setGeometry(QtCore.QRect(400, 230, 141, 31))
        self.labelSelectLang.setObjectName("labelSelectLang")
        self.bConvert = QtWidgets.QPushButton(self.centralwidget)
        self.bConvert.setEnabled(False)
        self.bConvert.setGeometry(QtCore.QRect(250, 270, 301, 34))
        self.bConvert.setObjectName("bConvert")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(20, 320, 1021, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.labelCurrentOperation = QtWidgets.QLabel(self.centralwidget)
        self.labelCurrentOperation.setGeometry(QtCore.QRect(170, 330, 871, 41))
        self.labelCurrentOperation.setText("")
        self.labelCurrentOperation.setObjectName("labelCurrentOperation")
        self.labelProgressFileIndex = QtWidgets.QLabel(self.centralwidget)
        self.labelProgressFileIndex.setGeometry(QtCore.QRect(30, 340, 121, 20))
        self.labelProgressFileIndex.setText("")
        self.labelProgressFileIndex.setObjectName("labelProgressFileIndex")
        self.bOpenOutputFolder = QtWidgets.QPushButton(self.centralwidget)
        self.bOpenOutputFolder.setGeometry(QtCore.QRect(560, 270, 191, 34))
        self.bOpenOutputFolder.setObjectName("bOpenOutputFolder")
        self.bSelectOutputFolder = QtWidgets.QPushButton(self.centralwidget)
        self.bSelectOutputFolder.setGeometry(QtCore.QRect(10, 180, 141, 34))
        self.bSelectOutputFolder.setObjectName("bSelectOutputFolder")
        self.qleOutputFolder = QtWidgets.QLineEdit(self.centralwidget)
        self.qleOutputFolder.setGeometry(QtCore.QRect(160, 180, 861, 32))
        self.qleOutputFolder.setObjectName("qleOutputFolder")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(160, 10, 871, 161))
        self.groupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBox.setFlat(False)
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName("groupBox")
        self.qlwListFilesSelected = QtWidgets.QListWidget(self.groupBox)
        self.qlwListFilesSelected.setGeometry(QtCore.QRect(10, 30, 851, 121))
        self.qlwListFilesSelected.setObjectName("qlwListFilesSelected")
        window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1045, 32))
        self.menubar.setObjectName("menubar")
        window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(window)
        self.statusbar.setObjectName("statusbar")
        window.setStatusBar(self.statusbar)

        self.initGUI()

        self.retranslateUi(window)
        QtCore.QMetaObject.connectSlotsByName(window)

    def retranslateUi(self, window):
        _translate = QtCore.QCoreApplication.translate
        window.setWindowTitle(_translate("window", "pyQtAutosub"))
        self.bSelectMedia.setText(_translate("window", "Select file(s)"))
        self.labelSelectLang.setText(_translate("window", "Audio Language"))
        self.bConvert.setText(_translate("window", "Transcribe Audio / Generate Subtitles"))
        self.bOpenOutputFolder.setText(_translate("window", "Open Output Folder"))
        self.bSelectOutputFolder.setText(_translate("window", "Output Location"))
        self.bRemoveFile.setText(_translate("window", "Remove file(s)"))
        self.groupBox.setTitle(_translate("window", "&List of files to generate subtitles/transcribe"))

    def initGUI(self):

        #language selection list

        list_languages =  [ "en - English", "af - Afrikaans", "ar - Arabic", "az - Azerbaijani", "be - Belarusian", "bg - Bulgarian", "bn - Bengali", "bs - Bosnian", "ca - Catalan", "ceb -Cebuano", "cs - Czech", "cy - Welsh", "da - Danish", "de - German", "el - Greek", "eo - Esperanto", "es - Spanish", "et - Estonian", "eu - Basque", "fa - Persian", "fi - Finnish", "fr - French", "ga - Irish", "gl - Galician", "gu -Gujarati", "ha - Hausa", "hi - Hindi", "hmn - Hmong", "hr - Croatian", "ht Haitian Creole", "hu - Hungarian", "hy - Armenian", "id - Indonesian", "ig - Igbo", "is - Icelandic", "it - Italian", "iw - Hebrew", "ja - Japanese", "jw - Javanese", "ka - Georgian", "kk - Kazakh", "km - Khmer", "kn - Kannada", "ko - Korean", "la - Latin", "lo - Lao", "lt - Lithuanian", "lv - Latvian", "mg - Malagasy", "mi - Maori", "mk - Macedonian", "ml - Malayalam", "mn - Mongolian", "mr - Marathi", "ms - Malay", "mt - Maltese", "my - Myanmar (Burmese)", "ne - Nepali", "nl - Dutch", "no - Norwegian", "ny - Chichewa", "pa - Punjabi", "pl - Polish", "pt - Portuguese", "ro - Romanian", "ru - Russian", "si - Sinhala", "sk - Slovak", "sl - Slovenian", "so - Somali", "sq - Albanian", "sr - Serbian", "st - Sesotho", "su - Sudanese", "sv - Swedish", "sw - Swahili", "ta - Tamil", "te - Telugu", "tg - Tajik", "th - Thai", "tl - Filipino", "tr - Turkish", "uk - Ukrainian", "ur - Urdu", "uz - Uzbek", "vi - Vietnamese", "yi - Yiddish", "yo - Yoruba", "zh-CN - Chinese (Simplified)", "zh-TW - Chinese (Traditional)", "zu - Zulu" ]

        self.cbSelectLang.addItems(list_languages)
        self.listenerProgress("", 0)

        #default output folder at user desktop
        userHome = Path.home()
        pathOutputFolder = userHome / 'Desktop' / 'pyQtAutosub'
        self.qleOutputFolder.setText(str(pathOutputFolder))

        self.bRemoveFile.setEnabled(False)

        #button listeners
        self.bConvert.clicked.connect(self.listenerBConvert)
        self.bRemoveFile.clicked.connect(self.listenerBRemove)
        self.bSelectOutputFolder.clicked.connect(self.selectOutputFolder)
        self.bOpenOutputFolder.clicked.connect(self.listenerBOpenOutputFolder)
        self.bSelectMedia.clicked.connect(self.openFileChooser)

    def resetGUI(self):
        self.qlwListFilesSelected.clear()
        self.bConvert.setEnabled(False)
        self.bRemoveFile.setEnabled(False)

        self.bSelectMedia.setEnabled(True)
        self.bSelectOutputFolder.setEnabled(True)

    def lockButtonsDuringOperation(self):
        self.bConvert.setEnabled(False)
        self.bRemoveFile.setEnabled(False)
        self.bSelectMedia.setEnabled(False)
        self.bSelectOutputFolder.setEnabled(False)

    def listenerProgress(self, str, percent):
        self.progressBar.setProperty("value", percent)
        self.labelCurrentOperation.setText(str)

    def updateProgressFileYofN(self, currentIndex, countFiles ):
        self.labelProgressFileIndex.setText("File " + str(currentIndex+1) + " of " +str(countFiles))

    def loopAutosub(self):
        self.lockButtonsDuringOperation()
        #extracts the two letter lang_code from the string on language selection
        selectedLanguage = self.cbSelectLang.currentText()
        indexDash = selectedLanguage.index("-")
        langCode = selectedLanguage[:indexDash-1]

        nFiles = self.qlwListFilesSelected.count()
        for i in range(nFiles):
            self.updateProgressFileYofN(i, nFiles)
            self.runAutosubForMediaFile(i, langCode)
        self.resetGUI()

    def runAutosubForMediaFile(self, index, langCode):
        sourceFile = self.qlwListFilesSelected.item(index).text()
        outputFiles = self.generatePathOutputFile(sourceFile)
        outputFileSRT = outputFiles[0]
        outputFileTXT = outputFiles[1]

        #if output directory does not exist, creates it
        pathOutputFolder = os.path.basename(self.qleOutputFolder.text())
        if not os.path.exists(pathOutputFolder):
            os.mkdir(pathOutputFolder)

        #run autosub
        fOutput = generate_subtitles(source_path = sourceFile, output = outputFileSRT, src_language = langCode, dst_language = langCode, listener_progress = self.listenerProgress)

        #if the operation was sucessful
        if fOutput:
            #updated the progress message
            self.listenerProgress("Finished", 100)

            #parses the .srt subtitle file and export text to .txt file
            SRTParser.extractTextFromSRT(str(outputFileSRT))

            #open both SRT and TXT output files
            self.open_file(outputFileTXT)
            self.open_file(outputFileSRT)

        else:
            showErrorMessage("Error! Unable to generate subtitles for file " + sourceFile + ".")

    def generatePathOutputFile(self, sourceFile):
        #extract the filename without extension from the path
        base = os.path.basename(sourceFile)
        #[0] is filename, [1] is file extension
        fileName = os.path.splitext(base)[0]

        #the output file has same name as input file, located on output Folder
        #with extension .srt
        pathOutputFolder = Path(self.qleOutputFolder.text())
        outputFileSRT = pathOutputFolder / (fileName + ".srt")
        outputFileTXT = pathOutputFolder / (fileName + ".txt")
        return [outputFileSRT, outputFileTXT]


    def selectOutputFolder(self):
        fSelectDir = QFileDialog.getExistingDirectory(self.centralwidget)
        if fSelectDir:
            self.qleOutputFolder.setText(fSelectDir)


    def openFileChooser(self):
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self.centralwidget, "Select output folder", "","All Media Files (*.mp3 *.mp4 *.wav *.m4a *.wma);", options=options)

        if files:
            self.qlwListFilesSelected.addItems(files)

            #enable the convert button only if list of files is not empty
            self.bConvert.setEnabled(True)
            self.bRemoveFile.setEnabled(True)

    def listenerBConvert(self):
        #execute the main process in separate thread to avoid gui lock
        thread = Thread(target = self.loopAutosub)
        thread.start()
        thread.join()

    def listenerBRemove(self):
        indexSelected = self.qlwListFilesSelected.currentRow()
        if indexSelected >= 0:
            self.qlwListFilesSelected.takeItem(indexSelected)

        #if no items left disables the remove and convert button
        if self.qlwListFilesSelected.count() == 0:
            self.bRemoveFile.setEnabled(False)
            self.bConvert.setEnabled(False)

    def listenerBOpenOutputFolder(self):
        pathOutputFolder = Path(self.qleOutputFolder.text())
        self.open_file(pathOutputFolder)

    def showErrorMessage(self, errorMsg):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Error)
        msg.setText(errorMsg)
        msg.setWindowTitle("Error!")

    def open_file(self, path):
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_window()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())
