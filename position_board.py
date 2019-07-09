import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import random
from PyQt5 import uic

form_class = uic.loadUiType("table_test.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setTableBanner()

    def setTableBanner(self):
        self.tableWidget.setItem(0, 0, QTableWidgetItem("Wallet"))
        self.tableWidget.setItem(0, 1, QTableWidgetItem("Leverage"))
        self.tableWidget.setItem(0, 2, QTableWidgetItem("Current_Price"))
        self.tableWidget.setItem(0, 3, QTableWidgetItem("1USD"))
        self.tableWidget.setItem(0, 4, QTableWidgetItem("Contracts_Max"))
        self.tableWidget.setItem(0, 5, QTableWidgetItem("Contracts_Open"))
        self.tableWidget.setItem(0, 6, QTableWidgetItem("Contracts_Ratio"))
        self.tableWidget.setItem(0, 7, QTableWidgetItem("Entry_Price"))
        self.tableWidget.setItem(0, 8, QTableWidgetItem("Unrealised_PNL"))

        self.tableWidget.setItem(1, 0, QTableWidgetItem("지갑잔고"))
        self.tableWidget.setItem(1, 1, QTableWidgetItem("레버리지"))
        self.tableWidget.setItem(1, 2, QTableWidgetItem("현재가"))
        self.tableWidget.setItem(1, 3, QTableWidgetItem("1USD"))
        self.tableWidget.setItem(1, 4, QTableWidgetItem("주문가능수량"))
        self.tableWidget.setItem(1, 5, QTableWidgetItem("현재보유수량"))
        self.tableWidget.setItem(1, 6, QTableWidgetItem("보유비율"))
        self.tableWidget.setItem(1, 7, QTableWidgetItem("진입가격"))
        self.tableWidget.setItem(1, 8, QTableWidgetItem("평가손익"))

    



if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()
