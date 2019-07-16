import sys
import pymysql.cursors
from testsql import *
import MainWindow

def main():
    user = 'root'
    passwd = 'bi960902@'
    DB = 'tsql'

    conn = pymysql.connect(host='localhost', user=user,
                           password=passwd,
                           db=DB,
                           charset='utf8'
                           )

    insertData(conn)

if __name__ == "__main__":
    main()

