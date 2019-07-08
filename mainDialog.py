import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

form_class = uic.loadUiType("MAINDIALOG.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.Button_login.clicked.connect(self.login_cmd)

    def login_cmd(self):
        apiKey = self.lineEdit_api_key.text()
        apiSecret = self.lineEdit_api_secret.text()

        print(apiKey, apiSecret)





app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()