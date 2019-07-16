import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from time import sleep
import bitmexTr1


position_board = uic.loadUiType("MainWindow.ui")[0]
system_board = uic.loadUiType("TableWindow.ui")[0]
system_logic = uic.loadUiType("System_Logic.ui")[0]


class Position_Board(QMainWindow, position_board):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.button_Leverage.clicked.connect(self.btn_clicked)

    def btn_clicked(self):
        # leverage 받아오기
        leverage=float("%s"%(self.lineEdit_Leverage.text()))
        pb = bitmexTr1.set_position_board(leverage)

        # UI에 띄우기
        self.val_Wallet.setText(str('%.8f' % pb[0]))
        self.val_Current_Price.setText(str(pb[1]))
        self.val_1USD.setText(str('%.8f' % pb[2]))
        self.val_Contracts_Max.setText(str('%.8f' % pb[3]))
        self.val_Contracts_Open.setText(str('%.8f' % pb[4]))
        self.val_Contracts_Ratio.setText(str('%.8f' % pb[5]))
        self.val_Entry_Price.setText(str(pb[6]))
        self.val_Unrealised_PNL.setText(str('%.8f' % pb[7]))
        self.val_Current_Price.repaint()


class System_Board(QMainWindow, system_board):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.tableWidget.setColumnWidth(0, 200)
        self.tableWidget.setColumnWidth(1, 400)
        self.tableWidget.setColumnWidth(2, 200)
        self.tableWidget.setColumnWidth(3, 200)
        self.tableWidget.setColumnWidth(4, 200)
        self.tableWidget.setColumnWidth(5, 230)
        self.tableWidget.setColumnWidth(6, 200)
        self.tableWidget.setColumnWidth(7, 200)
        self.tableWidget.setColumnWidth(8, 200)
        self.setSystemBoard()

    def setSystemBoard(self):
        sb = bitmexTr1.set_system_board()
        self.tableWidget.setItem(0, 1, QTableWidgetItem(sb[0]))
        self.tableWidget.setItem(0, 2, QTableWidgetItem(sb[1]))
        self.tableWidget.setItem(0, 3, QTableWidgetItem(sb[2]))
        self.tableWidget.setItem(0, 4, QTableWidgetItem(sb[3]))
        self.tableWidget.setItem(0, 5, QTableWidgetItem(sb[4]))

class System_Logic(QMainWindow, system_logic):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.tableWidget2.setColumnWidth(0, 350)
        self.tableWidget2.setColumnWidth(1, 400)
        self.tableWidget2.setColumnWidth(2, 350)
        self.tableWidget2.setColumnWidth(3, 350)
        self.tableWidget2.setColumnWidth(4, 350)
        self.tableWidget2.setColumnWidth(5, 350)
        self.tableWidget2.setColumnWidth(6, 350)
        self.tableWidget2.setColumnWidth(7, 350)
        self.tableWidget2.setColumnWidth(8, 350)
        self.tableWidget2.setColumnWidth(9, 350)
        self.tableWidget2.setColumnWidth(10, 350)
        self.tableWidget2.setColumnWidth(11, 350)
        self.setTableWidgetData() #데이터 삽입 함수

    def setTableWidgetData(self):
        self.tableWidget2.setItem(0, 0, QTableWidgetItem("여기에 입력"))




if __name__=="__main__":
    app = QApplication(sys.argv)
    pbWindow = Position_Board()
    sbWindow = System_Board()
    slWindow = System_Logic()
    pbWindow.show()
    sbWindow.show()
    slWindow.show()
    app.exec_()

