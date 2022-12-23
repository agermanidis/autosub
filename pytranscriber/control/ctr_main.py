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
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QDialog, QActionGroup
from PyQt5.QtCore import Qt
from pathlib import Path
from pytranscriber.model.param_autosub import Param_Autosub
from pytranscriber.util.util import MyUtil
from pytranscriber.control.thread_exec_autosub import Thread_Exec_Autosub
from pytranscriber.control.thread_cancel_autosub import Thread_Cancel_Autosub
from pytranscriber.gui.gui import Ui_window
import os
import sys
from pathlib import PurePath


class Ctr_Main():
    proxy = {
        'http': None,
        'https': None
    }

    def __init__(self):
        import sys
        app = QtWidgets.QApplication(sys.argv)
        window = QtWidgets.QMainWindow()
        self.objGUI = Ui_window()
        self.objGUI.setupUi(window)
        self.__initGUI(window)
        window.setFixedSize(window.size())
        window.show()
        sys.exit(app.exec_())

    def __initGUI(self, window):

        # language selection list
        list_languages = ["en-US - English (United States)",
                          "cmn-Hans-CN - Chinese (Simplified, China)",                          
                          "cmn-Hant-TW - Chinese (Traditional, Taiwan)",
                          "yue-Hant-HK - Cantonese (Traditional, HK)",
                          "en-AU - English (Australia)",                          
                          "en-CA - English (Canada)",
                          "en-GB - English (United Kingdom)",
                          "en-HK - English (Hong Kong)",
                          "en-IN - English (India)",
                          "en-GB - English (Ireland)",
                          "en-NZ - English (New Zealand)",
                          "en-PH - English (Philippines)",
                          "en-SG - English (Singapore)",
                          "af - Afrikaans",
                          "ar - Arabic",
                          'ar-DZ - Arabic (Algeria)',
                          'ar-EG - Arabic (Egypt)',
                          'ar-IQ - Arabic (Iraq)',
                          'ar-IS - Arabic (Israel)',
                          'ar-JO - Arabic (Jordan)',
                          'ar-KW - Arabic (Kuwait)',
                          'ar-LB - Arabic (Lebanon)',
                          'ar-MA - Arabic (Morocco)',
                          'ar-OM - Arabic (Oman)',
                          'ar-QA - Arabic (Qatar)',
                          'ar-SA - Arabic (Saudi Arabia)',
                          'ar-PS - Arabic (State of Palestine)',
                          'ar-TN - Arabic (Tunisia)',
                          'ar-AE - Arabic (United Arab Emirates)',
                          'ar-YE - Arabic (Yemen)',
                          "az - Azerbaijani",
                          "be - Belarusian",
                          "bg - Bulgarian",
                          "bn - Bengali",
                          "bs - Bosnian",
                          "ca - Catalan",
                          "ceb -Cebuano",
                          "cs - Czech",
                          "cy - Welsh",
                          "da - Danish",
                          "de - German",
                          'de-AT - German (Austria)',
                          'de-CH - German (Switzerland)',
                          "el - Greek",
                          "eo - Esperanto",
                          'es-ES - Spanish (Spain)',
                          'es-AR - Spanish (Argentina)',
                          'es-BO - Spanish (Bolivia)',
                          'es-CL - Spanish (Chile)',
                          'es-CO - Spanish (Colombia)',
                          'es-CR - Spanish (Costa Rica)',
                          'es-DO - Spanish (Dominican Republic)',
                          'es-EC - Spanish (Ecuador)',
                          'es-GT - Spanish (Guatemala)',
                          'es-HN - Spanish (Honduras)',
                          'es-MX - Spanish (Mexico)',
                          'es-NI - Spanish (Nicaragua)',
                          'es-PA - Spanish (Panama)',
                          'es-PE - Spanish (Peru)',
                          'es-PR - Spanish (Puerto Rico)',
                          'es-PY - Spanish (Paraguay)',
                          'es-SV - Spanish (El Salvador)',
                          'es-UY - Spanish (Uruguay)',
                          'es-US - Spanish (United States)',
                          'es-VE - Spanish (Venezuela)',
                          "et - Estonian",
                          "eu - Basque",
                          "fa - Persian",
                          'fil-PH - Filipino (Philippines)',
                          "fi - Finnish",
                          "fr - French",
                          'fr-BE - French (Belgium)',
                          'fr-CA - French (Canada)',
                          'fr-CH - French (Switzerland)',
                          "ga - Irish",
                          "gl - Galician",
                          "gu -Gujarati",
                          "ha - Hausa",
                          "hi - Hindi",
                          "hmn - Hmong",
                          "hr - Croatian",
                          "ht - Haitian Creole",
                          "hu - Hungarian",
                          "hy - Armenian",
                          "id - Indonesian",
                          "ig - Igbo",
                          "is - Icelandic",
                          "it - Italian",
                          'it-CH - Italian (Switzerland)',
                          "iw - Hebrew",
                          "ja - Japanese",
                          "jw - Javanese",
                          "ka - Georgian",
                          "kk - Kazakh",
                          "km - Khmer",
                          "kn - Kannada",
                          "ko - Korean",
                          "la - Latin",
                          "lo - Lao",
                          "lt - Lithuanian",
                          "lv - Latvian",
                          "mg - Malagasy",
                          "mi - Maori",
                          "mk - Macedonian",
                          "ml - Malayalam",
                          "mn - Mongolian",
                          "mr - Marathi",
                          "ms - Malay",
                          "mt - Maltese",
                          "my - Myanmar (Burmese)",
                          "ne - Nepali",
                          "nl - Dutch",
                          "no - Norwegian",
                          "ny - Chichewa",
                          "pa - Punjabi",
                          "pl - Polish",
                          "pt-BR - Portuguese (Brazil)",
                          "pt-PT - Portuguese (Portugal)",
                          "ro - Romanian",
                          "ru - Russian",
                          "si - Sinhala",
                          "sk - Slovak",
                          "sl - Slovenian",
                          "so - Somali",
                          "sq - Albanian",
                          "sr - Serbian",
                          "st - Sesotho",
                          "su - Sudanese",
                          "sv - Swedish",
                          "sw - Swahili",
                          "ta - Tamil",
                          'ta-IN - Tamil (India)',
                          'ta-MY - Tamil (Malaysia)',
                          'ta-SG - Tamil (Singapore)',
                          'ta-LK - Tamil (Sri Lanka)',
                          "te - Telugu",
                          "tg - Tajik",
                          "th - Thai",
                          "tl - Filipino",
                          "tr - Turkish",
                          "uk - Ukrainian",
                          "ur - Urdu",
                          "uz - Uzbek",
                          "vi - Vietnamese",
                          "yi - Yiddish",
                          "yo - Yoruba",
                          "zu - Zulu"]

        self.objGUI.cbSelectLang.addItems(list_languages)
        self.__listenerProgress("", 0)

        # default output folder at user desktop
        userHome = Path.home()
        pathOutputFolder = userHome / 'Desktop' / 'pyTranscriber'

        self.objGUI.qleOutputFolder.setText(str(pathOutputFolder))

        self.objGUI.bRemoveFile.setEnabled(False)

        self.objGUI.bCancel.hide()

        # button listeners
        self.objGUI.bConvert.clicked.connect(self.__listenerBExec)
        self.objGUI.bCancel.clicked.connect(self.__listenerBCancel)
        self.objGUI.bRemoveFile.clicked.connect(self.__listenerBRemove)
        self.objGUI.bSelectOutputFolder.clicked.connect(self.__listenerBSelectOuputFolder)
        self.objGUI.bOpenOutputFolder.clicked.connect(self.__listenerBOpenOutputFolder)
        self.objGUI.bSelectMedia.clicked.connect(self.__listenerBSelectMedia)

        self.objGUI.actionProxy.triggered.connect(self.__setProxy)
        self.objGUI.actionLicense.triggered.connect(self.__listenerBLicense)
        self.objGUI.actionDonation.triggered.connect(self.__listenerBDonation)
        self.objGUI.actionAbout_pyTranscriber.triggered.connect(self.__listenerBAboutpyTranscriber)
        
        self.__initLanguageMenu(window)
        self.objGUI.action_group.triggered.connect(self.__listenerChangeLanguage)
        
    def __initLanguageMenu(self, window):
        self.objGUI.actionEnglish.setCheckable(True)
        self.objGUI.actionEnglish.setChecked(True)
        self.objGUI.actionChineseTraditional.setCheckable(True)
        self.objGUI.actionChineseSimplified.setCheckable(True)
        self.objGUI.actionPortuguese.setCheckable(True)
        
        #set up of the actiongroup
        self.objGUI.action_group = QActionGroup(window)
        self.objGUI.action_group.addAction(self.objGUI.actionEnglish)
        self.objGUI.action_group.addAction(self.objGUI.actionChineseTraditional)
        self.objGUI.action_group.addAction(self.objGUI.actionChineseSimplified)
        self.objGUI.action_group.addAction(self.objGUI.actionPortuguese)

        self.objGUI.trans = QtCore.QTranslator(window)
        self.objGUI.mainWindow = window        
    
    #listener change language selected
    def __listenerChangeLanguage(self, event):
        #get the label of the selected language
        currentLang = event.text()
        
        #if it was a valid event
        if currentLang:
            currentDir = PurePath(__file__).parent.parent.parent    
            pathLangFile = currentDir.joinpath('pytranscriber').joinpath('gui').joinpath(currentLang)
            self.objGUI.trans.load(str(pathLangFile))
            
            QtWidgets.QApplication.instance().installTranslator(self.objGUI.trans)
        else:
            QtWidgets.QApplication.instance().removeTranslator(self.trans)
        
        #refresh UI with translation
        self.objGUI.retranslateUi(self.objGUI.mainWindow)

    def __resetGUIAfterSuccess(self):
        self.__resetGUIAfterCancel()

        self.objGUI.qlwListFilesSelected.clear()
        self.objGUI.bConvert.setEnabled(False)
        self.objGUI.bRemoveFile.setEnabled(False)

    def __resetGUIAfterCancel(self):

        self.__resetProgressBar()

        self.objGUI.bSelectMedia.setEnabled(True)
        self.objGUI.bSelectOutputFolder.setEnabled(True)
        self.objGUI.cbSelectLang.setEnabled(True)
        self.objGUI.chbxOpenOutputFilesAuto.setEnabled(True)

        self.objGUI.bCancel.hide()
        self.objGUI.bConvert.setEnabled(True)
        self.objGUI.bRemoveFile.setEnabled(True)

    def __lockButtonsDuringOperation(self):
        self.objGUI.bConvert.setEnabled(False)
        self.objGUI.bRemoveFile.setEnabled(False)
        self.objGUI.bSelectMedia.setEnabled(False)
        self.objGUI.bSelectOutputFolder.setEnabled(False)
        self.objGUI.cbSelectLang.setEnabled(False)
        self.objGUI.chbxOpenOutputFilesAuto.setEnabled(False)
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
        # options = QFileDialog.Options()
        options = QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self.objGUI.centralwidget, "Select media", "",
                                                "All Media Files (*.mp3 *.mp4 *.wav *.m4a *.wma *.ogg *.ogv *.mkv *.webm *.ts)")

        if files:
            self.objGUI.qlwListFilesSelected.addItems(files)

            # enable the convert button only if list of files is not empty
            self.objGUI.bConvert.setEnabled(True)
            self.objGUI.bRemoveFile.setEnabled(True)

    def __listenerBExec(self):
        if not MyUtil.is_internet_connected(Ctr_Main.proxy):
            self.__showErrorMessage(
                "Error! Cannot reach Google Speech Servers. \n\n1) Please make sure you are connected to the internet. \n2) If you are in China or other place that blocks access to Google servers: please install and enable a desktop-wide VPN app like Windscribe before trying to use pyTranscriber!")
        else:
            # extracts the two letter lang_code from the string on language selection
            selectedLanguage = self.objGUI.cbSelectLang.currentText()
            indexSpace = selectedLanguage.index(" ")
            langCode = selectedLanguage[:indexSpace]

            listFiles = []
            for i in range(self.objGUI.qlwListFilesSelected.count()):
                listFiles.append(str(self.objGUI.qlwListFilesSelected.item(i).text()))

            outputFolder = self.objGUI.qleOutputFolder.text()

            if self.objGUI.chbxOpenOutputFilesAuto.checkState() == Qt.Checked:
                boolOpenOutputFilesAuto = True
            else:
                boolOpenOutputFilesAuto = False

            objParamAutosub = Param_Autosub(listFiles, outputFolder, langCode,
                                            boolOpenOutputFilesAuto, Ctr_Main.proxy)

            # execute the main process in separate thread to avoid gui lock
            self.thread_exec = Thread_Exec_Autosub(objParamAutosub)

            # connect signals from work thread to gui controls
            self.thread_exec.signalLockGUI.connect(self.__lockButtonsDuringOperation)
            self.thread_exec.signalResetGUIAfterSuccess.connect(self.__resetGUIAfterSuccess)
            self.thread_exec.signalResetGUIAfterCancel.connect(self.__resetGUIAfterCancel)
            self.thread_exec.signalProgress.connect(self.__listenerProgress)
            self.thread_exec.signalProgressFileYofN.connect(self.__updateProgressFileYofN)
            self.thread_exec.signalErrorMsg.connect(self.__showErrorMessage)
            self.thread_exec.start()

            # Show the cancel button
            self.objGUI.bCancel.show()
            self.objGUI.bCancel.setEnabled(True)

    def __listenerBCancel(self):
        self.objGUI.bCancel.setEnabled(False)
        self.thread_cancel = Thread_Cancel_Autosub(self.thread_exec)

        # Only if worker thread is running
        if self.thread_exec and self.thread_exec.isRunning():
            # reset progress indicator
            self.__listenerProgress("Cancelling", 0)
            self.__setProgressBarIndefinite()
            self.__updateProgressFileYofN("")

            # connect the terminate signal to resetGUI
            self.thread_cancel.signalTerminated.connect(self.__resetGUIAfterCancel)
            # run the cancel autosub operation in new thread
            # to avoid progressbar freezing
            self.thread_cancel.start()
            self.thread_exec = None

    def __listenerBRemove(self):
        indexSelected = self.objGUI.qlwListFilesSelected.currentRow()
        if indexSelected >= 0:
            self.objGUI.qlwListFilesSelected.takeItem(indexSelected)

        # if no items left disables the remove and convert button
        if self.objGUI.qlwListFilesSelected.count() == 0:
            self.objGUI.bRemoveFile.setEnabled(False)
            self.objGUI.bConvert.setEnabled(False)

    def __listenerBOpenOutputFolder(self):
        pathOutputFolder = Path(self.objGUI.qleOutputFolder.text())

        # if folder exists and is valid directory
        if os.path.exists(pathOutputFolder) and os.path.isdir(pathOutputFolder):
            MyUtil.open_file(pathOutputFolder)
        else:
            self.__showErrorMessage("Error! Invalid output folder.")

    def __setProxy(self):
        from pytranscriber.control.ctr_proxy import Ctr_Proxy
        dialog = Ctr_Proxy(Ctr_Main.proxy['http'])
        result = dialog.exec_()
        if (result == QDialog.Accepted and dialog.objGUI.radioButtonHTTP.isChecked()):
            proxy = dialog.objGUI.lineEditHttpProxy.text()
            Ctr_Main.proxy = {
                'http': proxy,
                'https': proxy
            }
        elif (result == QDialog.Accepted and dialog.objGUI.radioButtonNone.isChecked()):
            Ctr_Main.proxy = {
                'http': None,
                'https': None
            }

    def __listenerBLicense(self):
        self.__showInfoMessage(
            "<html><body><a href=\"https://www.gnu.org/licenses/gpl-3.0.html\">GPL License</a><br><br>"
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

    def __listenerBDonation(self):
        self.__showInfoMessage("<html><body>"
                + "pyTranscriber is developed as a hobby, so donations of any value are welcomed."
                + "<br><br>If you feel that this software has been useful and would like to contribute for it to continue improving and have more and bugfixes and features like support to other Speech Recognition Engines (like Vosk and Mozilla Deep Speech) you can either join our <a href=\"https://github.com/sponsors/raryelcostasouza\">funding campaign at Github Sponsors</a> or make a <a href=\"https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=YHB854YHPJCU8&item_name=Donation+pyTranscriber&currency_code=BRL\">Paypal donation</a>."
                + "<br><br>Thanks in advance!"
                + "</body></html>", "Funding")

    def __listenerBAboutpyTranscriber(self):
        self.__showInfoMessage("<html><body>"
                               + "<a href=\"https://github.com/raryelcostasouza/pyTranscriber\">pyTranscriber</a> is an application that can be used "
                               + "to generate <b>automatic transcription / automatic subtitles </b>"
                               + "for audio/video files through a friendly graphical user interface. "
                               + "<br><br>"
                               + "The hard work of speech recognition is made by the <a href=\"https://cloud.google.com/speech/\">Google Speech Recognition API</a> "
                               + "using <a href=\"https://github.com/agermanidis/autosub\">Autosub</a>"
                               + "<br><br>pyTranscriber is developed as a hobby, so donations of any value are welcomed."
                               + "<br><br>If you feel that this software has been useful and would like to contribute for it to continue improving and have more and bugfixes and features like support to other Speech Recognition Engines (like Vosk and Mozilla Deep Speech) you can either join our <a href=\"https://github.com/sponsors/raryelcostasouza\">funding campaign at Github Sponsors</a> or make a <a href=\"https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=YHB854YHPJCU8&item_name=Donation+pyTranscriber&currency_code=BRL\">Paypal donation</a>."
                               + "<br><br>Thanks in advance!"
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
