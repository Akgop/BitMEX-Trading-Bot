import pymysql.cursors
from bitmexTr1 import *

#trade/bucketed내용 가져오기. system00d만 불러옴
def fetch_trade_bucketed_data():
    try:
        conn = pymysql.connect(host='localhost',
                               user='root',
                               password='bi960902@',
                               db='dtb',
                               use_unicode=True,
                               charset='utf8')
        curs = conn.cursor()
        sql = """select * from trade_bucketed_data WHERE system_Name = %s"""
        curs.execute(sql, ('System00d'))
        rows = curs.fetchall()
        system_name = rows[0][0]
        endTime = rows[0][1]
        open_price = rows[0][2]
        close_price = rows[0][3]
        high_price = rows[0][4]
        low_price = rows[0][5]
        buy_flag = rows[0][6]
        sell_flag = rows[0][7]
        percent_k = rows[0][8]
    finally:
        conn.close()
    return system_name, endTime, open_price, close_price, high_price, low_price, buy_flag, sell_flag, percent_k

#모든 프로그램에서는 이 함수를 사용하여 "현재가" 를 불러올 예정.
def fetch_current_price():
    try:
        conn = pymysql.connect(host='localhost',
                               user='root',
                               password='bi960902@',
                               db='dtb',
                               use_unicode=True,
                               charset='utf8')
        curs = conn.cursor()
        sql = """select * from get_current_price"""
        curs.execute(sql)
        rows = curs.fetchall()
        cp = float(rows[0][0])
    finally:
        conn.close()
    return cp