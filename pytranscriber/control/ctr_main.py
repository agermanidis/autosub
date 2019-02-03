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

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from pathlib import Path
from pytranscriber.model.param_autosub import Param_Autosub
from pytranscriber.util.util import MyUtil
from pytranscriber.control.thread_exec_autosub import Thread_Exec_Autosub
from pytranscriber.control.thread_cancel_autosub import Thread_Cancel_Autosub
from pytranscriber.gui.gui import Ui_window
import os


class Ctr_Main():

    def __init__(self):
        import sys
        app = QtWidgets.QApplication(sys.argv)
        window = QtWidgets.QMainWindow()
        self.objGUI = Ui_window()
        self.objGUI.setupUi(window)
        self.__initGUI()
        window.show()
        sys.exit(app.exec_())



    def __initGUI(self):

        #language selection list
        list_languages =  [ "en - English", "af - Afrikaans", "ar - Arabic", "az - Azerbaijani", "be - Belarusian", "bg - Bulgarian", "bn - Bengali", "bs - Bosnian", "ca - Catalan", "ceb -Cebuano", "cs - Czech", "cy - Welsh", "da - Danish", "de - German", "el - Greek", "eo - Esperanto", "es - Spanish", "et - Estonian", "eu - Basque", "fa - Persian", "fi - Finnish", "fr - French", "ga - Irish", "gl - Galician", "gu -Gujarati", "ha - Hausa", "hi - Hindi", "hmn - Hmong", "hr - Croatian", "ht Haitian Creole", "hu - Hungarian", "hy - Armenian", "id - Indonesian", "ig - Igbo", "is - Icelandic", "it - Italian", "iw - Hebrew", "ja - Japanese", "jw - Javanese", "ka - Georgian", "kk - Kazakh", "km - Khmer", "kn - Kannada", "ko - Korean", "la - Latin", "lo - Lao", "lt - Lithuanian", "lv - Latvian", "mg - Malagasy", "mi - Maori", "mk - Macedonian", "ml - Malayalam", "mn - Mongolian", "mr - Marathi", "ms - Malay", "mt - Maltese", "my - Myanmar (Burmese)", "ne - Nepali", "nl - Dutch", "no - Norwegian", "ny - Chichewa", "pa - Punjabi", "pl - Polish", "pt - Portuguese", "ro - Romanian", "ru - Russian", "si - Sinhala", "sk - Slovak", "sl - Slovenian", "so - Somali", "sq - Albanian", "sr - Serbian", "st - Sesotho", "su - Sudanese", "sv - Swedish", "sw - Swahili", "ta - Tamil", "te - Telugu", "tg - Tajik", "th - Thai", "tl - Filipino", "tr - Turkish", "uk - Ukrainian", "ur - Urdu", "uz - Uzbek", "vi - Vietnamese", "yi - Yiddish", "yo - Yoruba", "zh-CN - Chinese (Simplified)", "zh-TW - Chinese (Traditional)", "zu - Zulu" ]

        self.objGUI.cbSelectLang.addItems(list_languages)
        self.__listenerProgress("", 0)

        #default output folder at user desktop
        userHome = Path.home()
        pathOutputFolder = userHome / 'Desktop' / 'pyTranscriber'
        self.objGUI.qleOutputFolder.setText(str(pathOutputFolder))

        self.objGUI.bRemoveFile.setEnabled(False)

        self.objGUI.bCancel.hide()

        #button listeners
        self.objGUI.bConvert.clicked.connect(self.__listenerBExec)
        self.objGUI.bCancel.clicked.connect(self.__listenerBCancel)
        self.objGUI.bRemoveFile.clicked.connect(self.__listenerBRemove)
        self.objGUI.bSelectOutputFolder.clicked.connect(self.__listenerBSelectOuputFolder)
        self.objGUI.bOpenOutputFolder.clicked.connect(self.__listenerBOpenOutputFolder)
        self.objGUI.bSelectMedia.clicked.connect(self.__listenerBSelectMedia)

        self.objGUI.actionLicense.triggered.connect(self.__listenerBLicense)
        self.objGUI.actionAbout_pyTranscriber.triggered.connect(self.__listenerBAboutpyTranscriber)

    def __resetGUI(self):

        self.__resetProgressBar()

        self.objGUI.qlwListFilesSelected.clear()
        self.objGUI.bConvert.setEnabled(False)
        self.objGUI.bRemoveFile.setEnabled(False)

        self.objGUI.bSelectMedia.setEnabled(True)
        self.objGUI.bSelectOutputFolder.setEnabled(True)
        self.objGUI.cbSelectLang.setEnabled(True)

        self.objGUI.bCancel.hide()

    def __lockButtonsDuringOperation(self):
        self.objGUI.bConvert.setEnabled(False)
        self.objGUI.bRemoveFile.setEnabled(False)
        self.objGUI.bSelectMedia.setEnabled(False)
        self.objGUI.bSelectOutputFolder.setEnabled(False)
        self.objGUI.cbSelectLang.setEnabled(False)
        QtCore.QCoreApplication.processEvents()

    def __listenerProgress(self, str, percent):
        self.objGUI.labelCurrentOperation.setText(str)
        self.objGUI.progressBar.setProperty("value", percent)
        QtCore.QCoreApplication.processEvents()

    def __setProgressBarIndefinite(self):
        self.objGUI.progressBar.setMinimum(0)
        self.objGUI.progressBar.setMaximum(0)
        self.objGUI.progressBar.setValue(0)

    def __resetProgressBar(self):
        self.objGUI.progressBar.setMinimum(0)
        self.objGUI.progressBar.setMaximum(100)
        self.objGUI.progressBar.setValue(0)
        self.__listenerProgress("", 0)

    def __updateProgressFileYofN(self, str):
        self.objGUI.labelProgressFileIndex.setText(str)
        QtCore.QCoreApplication.processEvents()

    def __listenerBSelectOuputFolder(self):
        fSelectDir = QFileDialog.getExistingDirectory(self.objGUI.centralwidget)
        if fSelectDir:
            self.objGUI.qleOutputFolder.setText(fSelectDir)

    def __listenerBSelectMedia(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self.objGUI.centralwidget, "Select media", "","All Media Files (*.mp3 *.mp4 *.wav *.m4a *.wma);", options=options)

        if files:
            self.objGUI.qlwListFilesSelected.addItems(files)

            #enable the convert button only if list of files is not empty
            self.objGUI.bConvert.setEnabled(True)
            self.objGUI.bRemoveFile.setEnabled(True)

    def __listenerBExec(self):
        if not MyUtil.is_internet_connected():
            self.__showErrorMessage("Error! You need to have internet connection to use pyTranscriber!")
        else:
            #extracts the two letter lang_code from the string on language selection
            selectedLanguage = self.objGUI.cbSelectLang.currentText()
            indexDash = selectedLanguage.index("-")
            langCode = selectedLanguage[:indexDash-1]

            listFiles = []
            for i in range(self.objGUI.qlwListFilesSelected.count()):
                listFiles.append(str(self.objGUI.qlwListFilesSelected.item(i).text()))

            outputFolder = self.objGUI.qleOutputFolder.text()
            objParamAutosub = Param_Autosub(listFiles, outputFolder, langCode)

            #execute the main process in separate thread to avoid gui lock
            self.thread_exec = Thread_Exec_Autosub(objParamAutosub)

            #connect signals from work thread to gui controls
            self.thread_exec.signalLockGUI.connect(self.__lockButtonsDuringOperation)
            self.thread_exec.signalResetGUI.connect(self.__resetGUI)
            self.thread_exec.signalProgress.connect(self.__listenerProgress)
            self.thread_exec.signalProgressFileYofN.connect(self.__updateProgressFileYofN)
            self.thread_exec.signalErrorMsg.connect(self.__showErrorMessage)

            self.thread_exec.start()

            #Show the cancel button
            self.objGUI.bCancel.show()
            self.objGUI.bCancel.setEnabled(True)

    def __listenerBCancel(self):
        self.objGUI.bCancel.setEnabled(False)
        self.thread_cancel = Thread_Cancel_Autosub(self.thread_exec)

        #Only if worker thread is running
        if self.thread_exec and self.thread_exec.isRunning():
            #reset progress indicator
            self.__listenerProgress("Cancelling", 0)
            self.__setProgressBarIndefinite()
            self.__updateProgressFileYofN("")

            #connect the terminate signal to resetGUI
            self.thread_cancel.signalTerminated.connect(self.__resetGUI)
            #run the cancel autosub operation in new thread
            #to avoid progressbar freezing
            self.thread_cancel.start()
            self.thread_exec = None

    def __listenerBRemove(self):
        indexSelected = self.objGUI.qlwListFilesSelected.currentRow()
        if indexSelected >= 0:
            self.objGUI.qlwListFilesSelected.takeItem(indexSelected)

        #if no items left disables the remove and convert button
        if self.objGUI.qlwListFilesSelected.count() == 0:
            self.objGUI.bRemoveFile.setEnabled(False)
            self.objGUI.bConvert.setEnabled(False)

    def __listenerBOpenOutputFolder(self):
        pathOutputFolder = Path(self.objGUI.qleOutputFolder.text())

        #if folder exists and is valid directory
        if os.path.exists(pathOutputFolder) and os.path.isdir(pathOutputFolder):
            MyUtil.open_file(pathOutputFolder)
        else:
            self.__showErrorMessage("Error! Invalid output folder.")

    def __listenerBLicense(self):
        self.__showInfoMessage("<html><body><a href=\"https://www.gnu.org/licenses/gpl-3.0.html\">GPL License</a><br><br>"
                + "Copyright (C) 2019 Raryel C. Souza <raryel.costa at gmail.com><br>"
                + "<br>This program is free software: you can redistribute it and/or modify<br>"
                + "it under the terms of the GNU General Public License as published by<br>"
                + "the Free Software Foundation, either version 3 of the License, or<br>"
                + " any later version<br>"
                + "<br>"
                + "This program is distributed in the hope that it will be useful,<br>"
                + "but WITHOUT ANY WARRANTY; without even the implied warranty of<br>"
                + "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the<br>"
                + "GNU General Public License for more details.<br>"
                + "<br>"
                + "You should have received a copy of the GNU General Public License<br>"
                + "along with this program.  If not, see <a href=\"https://www.gnu.org/licenses\">www.gnu.org/licenses</a>."
                + "</body></html>", "License")

    def __listenerBAboutpyTranscriber(self):
        self.__showInfoMessage("<html><body>"
                + "<a href=\"https://github.com/raryelcostasouza/pyTranscriber\">pyTranscriber</a> is an application that can be used "
                + "to generate <b>automatic transcription / automatic subtitles </b>"
                + "for audio/video files through a friendly graphical user interface. "
                +"<br><br>"
                + "The hard work of speech recognition is made by the <a href=\"https://cloud.google.com/speech/\">Google Speech Recognition API</a> "
                + "using <a href=\"https://github.com/agermanidis/autosub\">Autosub</a>"
                + "</body></html>", "About pyTranscriber")


    def __showInfoMessage(self, info_msg, title):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setWindowTitle(title)
        msg.setText(info_msg)
        msg.exec()

    def __showErrorMessage(self, errorMsg):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)

        msg.setWindowTitle("Error!")
        msg.setText(errorMsg)
        msg.exec()
