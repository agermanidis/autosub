# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pyQtAutosub.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from threading import Thread
from PyQt5 import QtCore, QtGui, QtWidgets
from autosub import generate_subtitles

class Ui_window(object):
    def setupUi(self, window):
        window.setObjectName("window")
        window.resize(661, 593)
        self.centralwidget = QtWidgets.QWidget(window)
        self.centralwidget.setObjectName("centralwidget")
        self.listFilesToConvert = QtWidgets.QListView(self.centralwidget)
        self.listFilesToConvert.setGeometry(QtCore.QRect(160, 10, 491, 151))
        self.listFilesToConvert.setObjectName("listFilesToConvert")
        self.bSelectMedia = QtWidgets.QPushButton(self.centralwidget)
        self.bSelectMedia.setGeometry(QtCore.QRect(10, 10, 141, 34))
        self.bSelectMedia.setObjectName("bSelectMedia")
        self.cbSelectLang = QtWidgets.QComboBox(self.centralwidget)
        self.cbSelectLang.setGeometry(QtCore.QRect(160, 180, 491, 32))
        self.cbSelectLang.setObjectName("cbSelectLang")
        self.labelSelectLang = QtWidgets.QLabel(self.centralwidget)
        self.labelSelectLang.setGeometry(QtCore.QRect(40, 180, 101, 41))
        self.labelSelectLang.setObjectName("labelSelectLang")
        self.bConvert = QtWidgets.QPushButton(self.centralwidget)
        self.bConvert.setGeometry(QtCore.QRect(240, 230, 141, 34))
        self.bConvert.setObjectName("bConvert")
        self.textOutput = QtWidgets.QTextBrowser(self.centralwidget)
        self.textOutput.setGeometry(QtCore.QRect(20, 280, 631, 201))
        self.textOutput.setObjectName("textOutput")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(30, 490, 621, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.labelCurrentOperation = QtWidgets.QLabel(self.centralwidget)
        self.labelCurrentOperation.setGeometry(QtCore.QRect(30, 500, 121, 41))
        self.labelCurrentOperation.setObjectName("labelCurrentOperation")
        window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 661, 30))
        self.menubar.setObjectName("menubar")
        window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(window)
        self.statusbar.setObjectName("statusbar")
        window.setStatusBar(self.statusbar)

        self.bConvert.clicked.connect(self.listenerBConvert)

        self.retranslateUi(window)
        QtCore.QMetaObject.connectSlotsByName(window)

    def retranslateUi(self, window):
        _translate = QtCore.QCoreApplication.translate
        window.setWindowTitle(_translate("window", "pyQtAutosub"))
        self.bSelectMedia.setText(_translate("window", "Select media file(s)"))
        self.labelSelectLang.setText(_translate("window", "Audio Language"))
        self.bConvert.setText(_translate("window", "Convert"))
        self.labelCurrentOperation.setText(_translate("window", "Current Operation"))

    def listenerProgress(self, str, percent):
        self.progressBar.setProperty("value", percent)
        self.labelCurrentOperation.setText(str)

        #print(str, " ",percent, "%")
        #print(str, percent)

    def execAutosub(self):
        new_subtitle_file_path = generate_subtitles("Empty-Basket.mp3", listener_progress = self.listenerProgress)

    def listenerBConvert(self):
        thread = Thread(target = self.execAutosub)
        thread.start()
        thread.join()
        print("thread finished...exiting")

        #print ("Button Convert")




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_window()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())
