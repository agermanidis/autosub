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
from pyqtautosub.model.param_autosub import Param_Autosub
from pyqtautosub.util.util import MyUtil
from pyqtautosub.control.thread_exec_autosub import Thread_Exec_Autosub
from pyqtautosub.control.thread_cancel_autosub import Thread_Cancel_Autosub
from pyqtautosub.gui.gui import Ui_window
import multiprocessing
import os


class Ctr_Main():

    def __init__(self):
        import sys
        app = QtWidgets.QApplication(sys.argv)
        window = QtWidgets.QMainWindow()
        self.objGUI = Ui_window()
        self.objGUI.setupUi(window)
        self.initGUI()
        window.show()
        sys.exit(app.exec_())



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

        self.objGUI.bCancel.hide()

        #button listeners
        self.objGUI.bConvert.clicked.connect(self.listenerBExec)
        self.objGUI.bCancel.clicked.connect(self.listenerBCancel)
        self.objGUI.bRemoveFile.clicked.connect(self.listenerBRemove)
        self.objGUI.bSelectOutputFolder.clicked.connect(self.listenerBSelectOuputFolder)
        self.objGUI.bOpenOutputFolder.clicked.connect(self.listenerBOpenOutputFolder)
        self.objGUI.bSelectMedia.clicked.connect(self.listenerBSelectMedia)

        self.objGUI.actionLicense.triggered.connect(self.listenerBLicense)
        self.objGUI.actionAbout_pyQtAutosub.triggered.connect(self.listenerBAboutpyQtAutosub)

    def resetGUI(self):

        self.resetProgressBar()

        self.objGUI.qlwListFilesSelected.clear()
        self.objGUI.bConvert.setEnabled(False)
        self.objGUI.bRemoveFile.setEnabled(False)

        self.objGUI.bSelectMedia.setEnabled(True)
        self.objGUI.bSelectOutputFolder.setEnabled(True)
        self.objGUI.cbSelectLang.setEnabled(True)

        self.objGUI.bCancel.hide()

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

    def setProgressBarIndefinite(self):
        self.objGUI.progressBar.setMinimum(0)
        self.objGUI.progressBar.setMaximum(0)
        self.objGUI.progressBar.setValue(0)

    def resetProgressBar(self):
        self.objGUI.progressBar.setMinimum(0)
        self.objGUI.progressBar.setMaximum(100)
        self.objGUI.progressBar.setValue(0)
        self.listenerProgress("", 0)

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
        if not MyUtil.is_internet_connected():
            self.showErrorMessage("Error! You need to have internet connection to use pyQtAutosub!")
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
            self.thread_exec.signalLockGUI.connect(self.lockButtonsDuringOperation)
            self.thread_exec.signalResetGUI.connect(self.resetGUI)
            self.thread_exec.signalProgress.connect(self.listenerProgress)
            self.thread_exec.signalProgressFileYofN.connect(self.updateProgressFileYofN)
            self.thread_exec.signalErrorMsg.connect(self.showErrorMessage)

            #self.thread_exec.setTerminationEnabled(True)
            self.thread_exec.start()

            #Show the cancel button
            self.objGUI.bCancel.show()
            self.objGUI.bCancel.setEnabled(True)

    def listenerBCancel(self):
        self.objGUI.bCancel.setEnabled(False)
        self.thread_cancel = Thread_Cancel_Autosub(self.thread_exec)

        #Only if worker thread is running
        if self.thread_exec and self.thread_exec.isRunning():
            #reset progress indicator
            self.listenerProgress("Cancelling", 0)
            self.setProgressBarIndefinite()
            self.updateProgressFileYofN("")

            #connect the terminate signal to resetGUI
            self.thread_cancel.signalTerminated.connect(self.resetGUI)
            #run the cancel autosub operation in new thread
            #to avoid progressbar freezing
            self.thread_cancel.start()
            self.thread_exec = None

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

    def listenerBLicense(self):
        self.showInfoMessage("<html><body><a href=\"https://www.gnu.org/licenses/gpl-3.0.html\">GPL License</a><br><br>"
                + "Copyright (C) 2019 Raryel C. Souza <raryel.costa at gmail.com><br>"
                + "This program is free software: you can redistribute it and/or modify<br>"
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
                + "along with this program.  If not, see <https://www.gnu.org/licenses/>."
                + "</body></html>", "License")

    def listenerBAboutpyQtAutosub(self):
        self.showInfoMessage("<html><body>"
                + "<a href=\"https://github.com/raryelcostasouza/pyQtAutosub\">pyQtAutosub</a> is a pyQt GUI for Autosub intended to support audio transcription<br><br>"
                + "<a href=\"https://github.com/agermanidis/autosub\">Autosub</a> is a command-line utility for auto-generating subtitles for any video/audio file<br>"
                + "using the <a href=\"https://cloud.google.com/speech/\">Google Cloud Speech API</a> <br>"
                + "</body></html>", "About pyQtAutosub")


    def showInfoMessage(self, info_msg, title):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setWindowTitle(title)
        msg.setText(info_msg)
        msg.exec()

    def showErrorMessage(self, errorMsg):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)

        msg.setWindowTitle("Error!")
        msg.setText(errorMsg)
        msg.exec()

if __name__ == '__main__':
    multiprocessing.freeze_support()
    sys.exit(main())
