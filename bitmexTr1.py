from bitmex import BitMEX

import logging
import datetime
import numpy as np
import config

from configparser import ConfigParser

# 로그 기록 변수
logger = logging.getLogger()


class Functions(object):

    # 생성자. leverage setting, bitmex함수 불러오기.
    def __init__(self):
        myconfig = ConfigParser()
        myconfig.read('trading.conf')

        MODE = myconfig.get('DEFAULT', 'Mode')
        API_KEY = myconfig.get(MODE, 'API_KEY')
        API_SECRET = myconfig.get(MODE, 'API_SECRET')
        BASE_URL = myconfig.get(MODE, 'BASE_URL')

        self.leverage = config.leverage
        self.bitmex = BitMEX(apiKey=API_KEY, apiSecret=API_SECRET, base_url=BASE_URL)

    # 내 System00 <-의 시간 [그냥 계산]
    def set_time(self):
        # system00 이라는 점. 01, 02 등으로 바꾸어 주면됨.
        system_number = '00'
        format_day = '%Y-%m-%d'
        time_now = datetime.datetime.now()  # .hour는 int형이다.
        now_date = time_now.strftime(format_day)
        now_time = system_number + ':00'  # 뒤에 :00은 minute이다.
        # 시작시간인거지.
        system_time_json = now_date + ' ' + now_time

        #exit time <- 시간청산 할때 쓰임
        exit_time = '23:59'
        exit_time_json = now_date + ' ' + exit_time
        return system_time_json, system_number, exit_time_json

    # 내 잔고  (HTTP REQUEST -> user/margin)
    def get_my_wallet(self):
        try:
            um = self.bitmex.user_margin()
        except Exception as e:
            logger.error("margin error occured {}".format(e))
            return 0, 0
        try:
            wallet = um['walletBalance'] / 100000000
        except Exception as e:
            logger.error("margin error occured {}".format(e))
        return wallet

    #1USD   [그냥 계산]
    def get_1usd(self,cur_price):
        usd1 = 1/cur_price
        return usd1

    #주문가능수량 [그냥 계산]
    def get_con_max(self, wallet, usd1):
        con_max = (wallet*self.leverage)/usd1
        return con_max

    # 현재보유수량, 보유수량평균    (HTTP REQUEST -> position)
    def get_pos(self):
        try:
            pos = self.bitmex.position()
        except Exception as e:
            logger.error("position error occured {}".format(e))
            return 0, 0
        # 현재보유수량
        # con_open = None
        # avg_entry_price = None
        try:
            if pos[0]['currentQty'] is not 0:
                con_open = pos[0]['currentQty']
        except Exception as e:
            logger.error("position error occured {}".format(e))
        # 보유수량평균
        try:
            if pos[0]['avgEntryPrice'] is not 0:
                avg_entry_price = pos[0]['avgEntryPrice']
        except Exception as e:
            logger.error("position error occured {}".format(e))

        return con_open, avg_entry_price

    # 보유비율   [그냥 계산]
    def get_con_ratio(self, con_max, con_open):
        if con_open is None:
            con_ratio = None
        else:
            con_ratio = abs(con_max / con_open)
        return con_ratio

    # 평가 손익  [그냥 계산]
    def get_unrealised_pnl(self, con_open, avg_entry_price, cur_price):
        if con_open is None or avg_entry_price is None:
            un_pnl = None
        else:
            un_pnl = abs(con_open * ((1 / avg_entry_price) - (1 / cur_price)))
        return un_pnl

    # 내 보유 상태   [그냥 계산]
    def get_my_position(self, con_open):
        if con_open is None:
            my_position = None
        else:
            if con_open > 0:
                my_position = "Buy"
            elif con_open < 0:
                my_position = "Sell"
        return my_position

    # 매도,매수 개수  [그냥 계산]
    def get_con_ready(self, con_max, ma_score_buy, ma_score_sell):
        cr_buy = con_max * (1 / 24) * ma_score_buy
        cr_buy = round(cr_buy)
        cr_sell = con_max * (1 / 24) * ma_score_sell
        cr_sell = round(cr_sell)
        if cr_sell < 1:
            cr_sell = 1
        if cr_buy < 1:
            cr_buy = 1
        return cr_buy, cr_sell





