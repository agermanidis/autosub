# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pyQtAutosub.ui'
#
# Created by: PyQt5 UI code generator 5.12.dev1812231618
#
# WARNING! All changes made in this file will be lost!
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

from PyQt5 import QtCore, QtGui, QtWidgets
from ctr_main import Ctr_Main
import multiprocessing

class Ui_window(object):
    def setupUi(self, window):
        window.setObjectName("window")
        window.resize(1045, 418)
        self.centralwidget = QtWidgets.QWidget(window)
        self.centralwidget.setObjectName("centralwidget")
        self.bSelectMedia = QtWidgets.QPushButton(self.centralwidget)
        self.bSelectMedia.setGeometry(QtCore.QRect(10, 10, 141, 34))
        self.bSelectMedia.setObjectName("bSelectMedia")
        self.cbSelectLang = QtWidgets.QComboBox(self.centralwidget)
        self.cbSelectLang.setGeometry(QtCore.QRect(550, 230, 111, 32))
        self.cbSelectLang.setObjectName("cbSelectLang")
        self.cbSelectLang.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
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
        self.bOpenOutputFolder = QtWidgets.QPushButton(self.centralwidget)
        self.bOpenOutputFolder.setGeometry(QtCore.QRect(560, 270, 191, 34))
        self.bOpenOutputFolder.setObjectName("bOpenOutputFolder")
        self.bSelectOutputFolder = QtWidgets.QPushButton(self.centralwidget)
        self.bSelectOutputFolder.setGeometry(QtCore.QRect(10, 180, 141, 34))
        self.bSelectOutputFolder.setObjectName("bSelectOutputFolder")
        self.qleOutputFolder = QtWidgets.QLineEdit(self.centralwidget)
        self.qleOutputFolder.setGeometry(QtCore.QRect(160, 180, 861, 32))
        self.qleOutputFolder.setObjectName("qleOutputFolder")
        self.qleOutputFolder.setReadOnly(True)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(160, 10, 871, 161))
        self.groupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBox.setFlat(False)
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName("groupBox")
        self.qlwListFilesSelected = QtWidgets.QListWidget(self.groupBox)
        self.qlwListFilesSelected.setGeometry(QtCore.QRect(10, 30, 851, 121))
        self.qlwListFilesSelected.setObjectName("qlwListFilesSelected")
        self.bRemoveFile = QtWidgets.QPushButton(self.centralwidget)
        self.bRemoveFile.setGeometry(QtCore.QRect(10, 50, 141, 34))
        self.bRemoveFile.setObjectName("bRemoveFile")
        self.labelProgressFileIndex = QtWidgets.QLabel(self.centralwidget)
        self.labelProgressFileIndex.setGeometry(QtCore.QRect(30, 330, 131, 41))
        self.labelProgressFileIndex.setText("")
        self.labelProgressFileIndex.setObjectName("labelProgressFileIndex")
        window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1045, 32))
        self.menubar.setObjectName("menubar")
        window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(window)
        self.statusbar.setObjectName("statusbar")
        window.setStatusBar(self.statusbar)

        self.ctrMain = Ctr_Main(self)

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

if __name__ == "__main__":
    import sys
    multiprocessing.freeze_support()
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_window()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())
