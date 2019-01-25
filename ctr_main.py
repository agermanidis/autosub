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
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from pathlib import Path
from autosub import generate_subtitles
from srtparser import SRTParser
from param_autosub import Param_Autosub
from util import MyUtil
from worker_thread import Worker_Thread
import os

class Ctr_Main():

    def __init__(self, objGUI):
        self.objGUI = objGUI
        self.initGUI()

    def initGUI(self):

        #language selection list
        list_languages =  [ "en - English", "af - Afrikaans", "ar - Arabic", "az - Azerbaijani", "be - Belarusian", "bg - Bulgarian", "bn - Bengali", "bs - Bosnian", "ca - Catalan", "ceb -Cebuano", "cs - Czech", "cy - Welsh", "da - Danish", "de - German", "el - Greek", "eo - Esperanto", "es - Spanish", "et - Estonian", "eu - Basque", "fa - Persian", "fi - Finnish", "fr - French", "ga - Irish", "gl - Galician", "gu -Gujarati", "ha - Hausa", "hi - Hindi", "hmn - Hmong", "hr - Croatian", "ht Haitian Creole", "hu - Hungarian", "hy - Armenian", "id - Indonesian", "ig - Igbo", "is - Icelandic", "it - Italian", "iw - Hebrew", "ja - Japanese", "jw - Javanese", "ka - Georgian", "kk - Kazakh", "km - Khmer", "kn - Kannada", "ko - Korean", "la - Latin", "lo - Lao", "lt - Lithuanian", "lv - Latvian", "mg - Malagasy", "mi - Maori", "mk - Macedonian", "ml - Malayalam", "mn - Mongolian", "mr - Marathi", "ms - Malay", "mt - Maltese", "my - Myanmar (Burmese)", "ne - Nepali", "nl - Dutch", "no - Norwegian", "ny - Chichewa", "pa - Punjabi", "pl - Polish", "pt - Portuguese", "ro - Romanian", "ru - Russian", "si - Sinhala", "sk - Slovak", "sl - Slovenian", "so - Somali", "sq - Albanian", "sr - Serbian", "st - Sesotho", "su - Sudanese", "sv - Swedish", "sw - Swahili", "ta - Tamil", "te - Telugu", "tg - Tajik", "th - Thai", "tl - Filipino", "tr - Turkish", "uk - Ukrainian", "ur - Urdu", "uz - Uzbek", "vi - Vietnamese", "yi - Yiddish", "yo - Yoruba", "zh-CN - Chinese (Simplified)", "zh-TW - Chinese (Traditional)", "zu - Zulu" ]

        self.objGUI.cbSelectLang.addItems(list_languages)
        self.listenerProgress("", 0)

        #default output folder at user desktop
        userHome = Path.home()
        pathOutputFolder = userHome / 'Desktop' / 'pyQtAutosub'
        self.objGUI.qleOutputFolder.setText(str(pathOutputFolder))

        self.objGUI.bRemoveFile.setEnabled(False)

        #button listeners
        self.objGUI.bConvert.clicked.connect(self.listenerBExec)
        self.objGUI.bRemoveFile.clicked.connect(self.listenerBRemove)
        self.objGUI.bSelectOutputFolder.clicked.connect(self.listenerBSelectOuputFolder)
        self.objGUI.bOpenOutputFolder.clicked.connect(self.listenerBOpenOutputFolder)
        self.objGUI.bSelectMedia.clicked.connect(self.listenerBSelectMedia)

    def resetGUI(self):
        self.objGUI.qlwListFilesSelected.clear()
        self.objGUI.bConvert.setEnabled(False)
        self.objGUI.bRemoveFile.setEnabled(False)

        self.objGUI.bSelectMedia.setEnabled(True)
        self.objGUI.bSelectOutputFolder.setEnabled(True)
        self.objGUI.cbSelectLang.setEnabled(True)

    def lockButtonsDuringOperation(self):
        self.objGUI.bConvert.setEnabled(False)
        self.objGUI.bRemoveFile.setEnabled(False)
        self.objGUI.bSelectMedia.setEnabled(False)
        self.objGUI.bSelectOutputFolder.setEnabled(False)
        self.objGUI.cbSelectLang.setEnabled(False)
        QtCore.QCoreApplication.processEvents()

    def listenerProgress(self, str, percent):
        self.objGUI.labelCurrentOperation.setText(str)
        self.objGUI.progressBar.setProperty("value", percent)
        QtCore.QCoreApplication.processEvents()

    def updateProgressFileYofN(self, str):
        self.objGUI.labelProgressFileIndex.setText(str)
        QtCore.QCoreApplication.processEvents()

    def listenerBSelectOuputFolder(self):
        fSelectDir = QFileDialog.getExistingDirectory(self.objGUI.centralwidget)
        if fSelectDir:
            self.objGUI.qleOutputFolder.setText(fSelectDir)

    def listenerBSelectMedia(self):
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self.objGUI.centralwidget, "Select media", "","All Media Files (*.mp3 *.mp4 *.wav *.m4a *.wma);", options=options)

        if files:
            self.objGUI.qlwListFilesSelected.addItems(files)

            #enable the convert button only if list of files is not empty
            self.objGUI.bConvert.setEnabled(True)
            self.objGUI.bRemoveFile.setEnabled(True)

    def listenerBExec(self):
        #execute the main process in separate thread to avoid gui lock

        #extracts the two letter lang_code from the string on language selection
        selectedLanguage = self.objGUI.cbSelectLang.currentText()
        indexDash = selectedLanguage.index("-")
        langCode = selectedLanguage[:indexDash-1]

        listFiles = []
        for i in range(self.objGUI.qlwListFilesSelected.count()):
            listFiles.append(str(self.objGUI.qlwListFilesSelected.item(i).text()))

        outputFolder = self.objGUI.qleOutputFolder.text()
        objParamAutosub = Param_Autosub(listFiles, outputFolder, langCode)
        self.wt = Worker_Thread(objParamAutosub)

        #connect signals from work thread to gui controls
        self.wt.signalLockGUI.connect(self.lockButtonsDuringOperation)
        self.wt.signalResetGUI.connect(self.resetGUI)
        self.wt.signalProgress.connect(self.listenerProgress)
        self.wt.signalProgressFileYofN.connect(self.updateProgressFileYofN)
        self.wt.signalErrorMsg.connect(self.showErrorMessage)

        self.wt.start()

    def listenerBRemove(self):
        indexSelected = self.objGUI.qlwListFilesSelected.currentRow()
        if indexSelected >= 0:
            self.objGUI.qlwListFilesSelected.takeItem(indexSelected)

        #if no items left disables the remove and convert button
        if self.objGUI.qlwListFilesSelected.count() == 0:
            self.objGUI.bRemoveFile.setEnabled(False)
            self.objGUI.bConvert.setEnabled(False)

    def listenerBOpenOutputFolder(self):
        pathOutputFolder = Path(self.objGUI.qleOutputFolder.text())

        #if folder exists and is valid directory
        if os.path.exists(pathOutputFolder) and os.path.isdir(pathOutputFolder):
            MyUtil.open_file(pathOutputFolder)
        else:
            self.showErrorMessage("Error! Invalid output folder.")

    def showErrorMessage(self, errorMsg):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)

        msg.setWindowTitle("Error!")
        msg.setText(errorMsg)
        msg.exec()
