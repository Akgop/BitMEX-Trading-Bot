

import logging

import os, sys
from functions import *


logger = logging.getLogger()

def setup_logger():
    # Prints logger info to terminal
    logger.setLevel(logging.DEBUG)  # Change this to DEBUG if you want a lot more info
    ch = logging.StreamHandler()

    fh = logging.FileHandler('user.log', mode='a', encoding=None, delay=False)
    fh.setLevel(logging.INFO)
    # create formatter
    formatter = logging.Formatter("%(filename)s %(lineno)s %(message)s")
    formatter_fh = logging.Formatter("%(asctime)s %(filename)s %(lineno)s %(message)s")
    # add formatter to ch
    ch.setFormatter(formatter)
    fh.setFormatter(formatter_fh)

    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger

def set_position_board(leverage):
    """send Data to position_board ui"""
    func = Functions()
    func.set_leverage(leverage)
    wallet_balance = func.get_wallet_balance()
    cur_Price = func.get_current_price()
    USD_1 = func.get_1USD(cur_Price)
    con_max = func.get_contracts_max(wallet_balance,USD_1)
    con_open = func.get_contracts_open()
    con_ratio = func.get_contracts_ratio(con_open,con_max)
    avg_entry_price = func.get_entry_price()
    unreal_PNL = func.get_unrealised_pnl()

    return wallet_balance, cur_Price, USD_1, con_max, con_open, con_ratio, avg_entry_price, unreal_PNL

def set_system_board():
    func = Functions()
    st, et = func.get_time()
    con_open = func.get_contracts_open()
    entry_price = func.get_entry_price()
    position = func.get_position()

    return st, position, con_open, entry_price, et

def set_system_logic():
    func = Functions()
    st, et = func.get_time()
    open_price = func.get_open_price_X(st)
    high_price = func.get_high_price_X(st)
    low_price = func.get_low_price_X(st)

    return open_price, high_price, low_price

a = set_system_logic()
print(a[0])
print(a[1])
print(a[2])