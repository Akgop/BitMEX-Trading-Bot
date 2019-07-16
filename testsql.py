import pymysql.cursors
import bitmexTr1

def insertData(conn):
    '''curs = conn.cursor()
    sql = "select * from position_board"
    curs.execute(sql)
    sql = """insert into position_board(wallet, Leverage, Current_Price, 1USD, Contracts_Max, Contracts_Open, Contracts_Ratio, Entry_Price, Unrealised_PNL)
          values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    curs.execute(sql, (pb[0], pb[8], pb[1], pb[2], pb[3], pb[4], pb[5], pb[6], pb[7]))
    conn.commit()'''



def getData(conn):
    curs = conn.cursor()
    sql = "select * from position_board"
    curs.execute(sql)
    rows = curs.fetchall()
    print(rows)
