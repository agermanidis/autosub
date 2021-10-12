# @FileName: 
# @Time    : 2021/10/11
# @Author  : Dorad, cug.xia@gmail.com
# @Blog    : https://blog.cuger.cn


from PyQt5.QtWidgets import QDialog, QMessageBox
from pytranscriber.gui.proxy import Ui_Dialog
from pytranscriber.util.util import MyUtil


class Ctr_Proxy(QDialog):
    def __init__(self, proxy=None):
        super(Ctr_Proxy, self).__init__()
        self.objGUI = Ui_Dialog()
        self.objGUI.setupUi(self)
        if not proxy:
            self.__checkNone()
        else:
            self.__checkHTTP(proxy)
        self.objGUI.pushButtonTest.clicked.connect(self.__test)

    def __checkNone(self):
        self.objGUI.radioButtonNone.setChecked(True)
        self.objGUI.lineEditHttpProxy.setEnabled(False)
        self.objGUI.pushButtonTest.setEnabled(False)

    def __checkHTTP(self, proxy=None):
        self.objGUI.radioButtonHTTP.setChecked(True)
        self.objGUI.lineEditHttpProxy.setEnabled(True)
        self.objGUI.pushButtonTest.setEnabled(True)
        self.objGUI.lineEditHttpProxy.setText(str(proxy))

    def __test(self):
        proxy = self.objGUI.lineEditHttpProxy.text()
        if not proxy:
            return False
        if not MyUtil.is_internet_connected(proxies={
            'http': proxy,
            'https': proxy
        }):
            # error
            msgBox = QMessageBox.critical(self, 'Error', 'Error connecting to Google.')
        else:
            msgBox = QMessageBox.information(self, 'Success', 'Successfully connected to Google.')
