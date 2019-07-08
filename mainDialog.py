import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

form_class_main = uic.loadUiType("OHLCV.ui")[0]
form_class_login = uic.loadUiType("loginDialog.ui")[0]

class MyWindow(QMainWindow, form_class_main):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)

        self.pushButton_login.clicked.connect(self.pushButtonClicked)

    def pushButtonClicked(self):
        dlg = Login_Page()
        dlg.exec_()
        apiKey = dlg.apiKey
        apiSecret = dlg.apiSecret
        BASE_URL = 'https://testnet.bitmex.com/api/v1/'
        return apiKey, apiSecret, BASE_URL

class Login_Page(QDialog, form_class_login):
    def __init__(self):
        super(Login_Page, self).__init__()
        self.setupUi(self)

        self.apiKey = None
        self.apiSecret = None

        self.Button_login.clicked.connect(self.login_cmd)

    def login_cmd(self):
        self.apiKey = self.lineEdit_api_key.text()
        self.apiSecret = self.lineEdit_api_secret.text()
        self.close()

app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()