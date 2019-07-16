from bitmex import BitMEX

import logging
import datetime
import time
import os, sys

from configparser import ConfigParser

myconfig = ConfigParser()
myconfig.read('trading_example.conf')

MODE         = myconfig.get('DEFAULT', 'Mode')
API_KEY      = myconfig.get(MODE, 'API_KEY')
API_SECRET   = myconfig.get(MODE, 'API_SECRET')
BASE_URL     = myconfig.get(MODE, 'BASE_URL')
checkprice   = float(myconfig.get('DEFAULT', 'Buy'))
checkprice_2 = float(myconfig.get('DEFAULT', 'Sell'))
dry_run      = True if myconfig.get('DEFAULT', 'dry_run') == 'yes' else False


bitmex = BitMEX(apiKey=API_KEY, apiSecret=API_SECRET, base_url=BASE_URL)


class Functions(object):
    def __init__(self):
        self.leverage = 0

    def set_leverage(self, leverage):
        self.leverage = leverage

    def get_leverage(self):
        return self.leverage

    def get_wallet_balance(self):
        """get my wallet"""
        gm = bitmex.get_margin()
        wallet_balance = gm['walletBalance'] / 100000000
        return wallet_balance

    def get_current_price(self):
        """get current price(last price)"""
        inst = bitmex.instruments(count=100, reverse=False)
        cur_Price = inst[0]['lastPrice']
        return cur_Price

    def get_1USD(self, cur_Price):
        """calculate 1USD"""
        USD_1 = round(1 / cur_Price, 8)
        return USD_1

    def get_contracts_max(self, wallet_balance, USD_1):
        """calculate contracts max(주문가능수량)"""
        con_max = ((wallet_balance * self.leverage) / USD_1)
        return con_max

    def get_contracts_open(self):
        """get contracts open(현재 보유수량)"""
        pos = bitmex.positions()
        if pos is None:
            con_open = "None"
        else:
            con_open = pos[0]['currentQty']
        return con_open

    def get_contracts_ratio(self, con_open, con_max):
        """get contracts ratio(현재 보유비율)"""
        con_ratio = (abs(con_open) / con_max)
        return con_ratio

    def get_avg_entry_price(self):
        """get entry price"""
        pos = bitmex.positions()
        if pos is None:
            avg_entry_price = "None"
        else:
            avg_entry_price = pos[0]['avgEntryPrice']
            if avg_entry_price is None:
                avg_entry_price = "None"
        return avg_entry_price

    def get_unrealised_pnl(self):
        """get unreal pnl"""
        gm = bitmex.get_margin()
        unreal_PNL = gm['unrealisedPnl'] / 100000000
        return unreal_PNL

    def get_time(self):
        '''start-time, end-time'''
        format = '%Y-%m-%d %H:%M'
        start_time = datetime.datetime.now()
        exit_time = start_time + datetime.timedelta(hours=23, minutes=40)
        st = start_time.strftime(format)
        et = exit_time.strftime(format)
        return st, et

    def get_entry_price(self):
        order = bitmex.order(1,True)
        if order is None:
            entry_price = "None"
        else:
            entry_price = order[0]['price']
            if entry_price is None:
                entry_price = "None"
        return entry_price

    def get_position(self):
        order = bitmex.order(1,True)
        side = order[0]['side']
        return side

    def get_open_price_X(self, st):
        st, et = self.get_time()
        inst = bitmex.instruments(1, False, st)
        op = inst[0]['prevPrice24h']
        return op

    def get_high_price_X(self, st):
        st, et = self.get_time()
        inst = bitmex.instruments(1, False, st)
        hp = inst[0]['highPrice']
        return hp

    def get_low_price_X(self, st):
        st, et = self.get_time()
        inst = bitmex.instruments(1, False, st)
        lp = inst[0]['lowPrice']
        return lp


