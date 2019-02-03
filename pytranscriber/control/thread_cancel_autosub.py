from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal


class Thread_Cancel_Autosub(QThread):
    signalTerminated = pyqtSignal()

    def __init__(self, pObjWT):
        self.objWT = pObjWT
        QThread.__init__(self)

    def run(self):
        self.objWT.cancel()
        self.signalTerminated.emit()
