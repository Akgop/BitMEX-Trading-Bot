from bitmex import BitMEX

import logging
import time
import datetime
import os, sys
import numpy as np
import config

from configparser import ConfigParser

myconfig = ConfigParser()
myconfig.read('trading.conf')

MODE         = myconfig.get('DEFAULT', 'Mode')
API_KEY      = myconfig.get(MODE, 'API_KEY')
API_SECRET   = myconfig.get(MODE, 'API_SECRET')
BASE_URL     = myconfig.get(MODE, 'BASE_URL')
checkprice   = float(myconfig.get('DEFAULT', 'Buy'))
checkprice_2 = float(myconfig.get('DEFAULT', 'Sell'))
dry_run      = True if myconfig.get('DEFAULT', 'dry_run') == 'yes' else False


bitmex = BitMEX(apiKey=API_KEY, apiSecret=API_SECRET, base_url=BASE_URL)

#로그 기록 변수
logger = logging.getLogger()

#로그
def setup_logger():
    # Prints logger info to terminal
    logger.setLevel(logging.DEBUG)  # Change this to DEBUG if you want a lot more info
    ch = logging.StreamHandler()

    fh = logging.FileHandler('user.log', mode='a', encoding=None, delay=False)
    fh.setLevel(logging.CRITICAL)
    # create formatter
    formatter = logging.Formatter("%(filename)s %(lineno)s %(message)s")
    formatter_fh = logging.Formatter("%(asctime)s %(filename)s %(lineno)s %(message)s")
    # add formatter to ch
    ch.setFormatter(formatter)
    fh.setFormatter(formatter_fh)

    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger

#내 System00 <-의 시간
def set_time():
    #system00 이라는 점. 01, 02 등으로 바꾸어 주면됨.
    system_number = '00'
    format_day = '%Y-%m-%d'
    time_now = datetime.datetime.now()  #.hour는 int형이다.
    now_date = time_now.strftime(format_day)
    now_time = system_number + ':00'    #뒤에 :00은 minute이다.
    #시작시간인거지.
    system_time_json = now_date + ' ' + now_time

    #일단 종료시간 30분으로 정해놈
    exit_time = '19:27'
    exit_time_json = now_date + ' ' + exit_time
    return system_time_json, system_number, exit_time_json

#내 잔고
def get_my_wallet():
    try:
        um = bitmex.user_margin()
    except Exception as e:
        logger.error("margin error occured {}".format(e))
        return 0, 0
    try:
        wallet = um['walletBalance'] / 100000000
    except Exception as e:
        logger.error("margin error occured {}".format(e))
    return wallet

#현재가
def get_cur_price():
    try:
        inst = bitmex.instrument(count=1, reverse=True)
    except Exception as e:
        logger.error("instrument error occured {}".format(e))
        return 0, 0
    try:
        cur_price = inst[0]['lastPrice']
        logger.info("cur_price : {}".format(cur_price))
    except Exception as e:
        logger.error("instrument error occured {}".format(e))

    return cur_price

#현재보유수량, 보유수량평균
def get_pos():
    try:
        pos = bitmex.position()
    except Exception as e:
        logger.error("position error occured {}".format(e))
        return 0, 0
    #현재보유수량
    #con_open = None
    #avg_entry_price = None
    try:
        if pos[0]['currentQty'] is not 0:
            con_open = pos[0]['currentQty']
    except Exception as e:
        logger.error("position error occured {}".format(e))
    #보유수량평균
    try:
        if pos[0]['avgEntryPrice'] is not 0:
            avg_entry_price = pos[0]['avgEntryPrice']
    except Exception as e:
        logger.error("position error occured {}".format(e))

    return con_open, avg_entry_price

#보유비율
def get_con_ratio(con_max, con_open):
    if con_open is None:
        con_ratio = None
    else:
        con_ratio = abs(con_max / con_open)
    return con_ratio

#평가 손익
def get_unrealised_pnl(con_open, avg_entry_price, cur_price):
    if con_open is None or avg_entry_price is None:
        un_pnl = None
    else:
        un_pnl = abs(con_open * ((1 / avg_entry_price) - (1 / cur_price)))
    return un_pnl

#내 보유 상태
def get_my_position(con_open):
    if con_open is None:
        my_position = None
    else:
        if con_open > 0:
            my_position = "Buy"
        elif con_open < 0:
            my_position = "Sell"
    return my_position

#%K, OHLC
def get_trade_bucket_1h(cur_price):
    try:
        st = set_time()
        system_time_json = st[0]
        tb = bitmex.trade_bucketed(binSize='1h', count=530, endTime=system_time_json)
    except Exception as e:
        logger.error("trade/bucketed error occured {}".format(e))
        return 0, 0
    #percent K
    try:
        noises = np.zeros(10)
        for i in range(0, 10):
            noises[i] = 1 - abs((tb[i * 24]['open'] - tb[i * 24]['close']) /
                                (tb[i * 24]['high'] - tb[i * 24]['low']))
        avg_noise = np.mean(noises)
        pk = 1 - avg_noise
    except Exception as e:
        logger.error("trade/bucketed error occured {}".format(e))
    #OHLC
    try:
        start_price = tb[0]['close']
        open_price = tb[0]['open']
        high_price = tb[0]['high']
        low_price = tb[0]['low']
    except Exception as e:
        logger.error("trade/bucketed error occured {}".format(e))
    #ma_score
    try:
        close_price = np.zeros(22)
        sum = 0
        ma_flag_buy = 0
        ma_flag_sell = 0
        for i in range(0, 22):
            close_price[i] = tb[i*24]['close']
            sum = sum + close_price[i]
            avg_result = sum/(i+1)
            if i >= 2:
                if cur_price >= avg_result:
                    ma_flag_buy = ma_flag_buy + 1
                else:
                    ma_flag_sell = ma_flag_sell - 1
        ma_flag_buy = ma_flag_buy/20
        ma_flag_sell = abs(ma_flag_sell/20)
    except Exception as e:
        logger.error("trade/bucketed error occured {}".format(e))

    return pk, start_price, open_price, high_price, low_price, ma_flag_buy, ma_flag_sell

#매도,매수 개수
def get_con_ready(con_open, ma_score_buy, ma_score_sell):
    cr_buy = con_open * (1/24) * ma_score_buy
    cr_buy = round(cr_buy)
    cr_sell = con_open * (1/24) * ma_score_sell
    cr_sell = round(cr_sell)
    return cr_buy, cr_sell


def position_board(leverage):
    posi = get_pos()
    wallet = get_my_wallet()
    cur_price = get_cur_price()
    usd1 = round(1/cur_price, 8)
    con_max = (wallet * leverage) / usd1
    con_open = posi[0]
    con_ratio = get_con_ratio(con_max, con_open)
    avg_entry_price = posi[1]
    un_pnl = get_unrealised_pnl(con_open, avg_entry_price, cur_price)

    return wallet, leverage, cur_price, usd1, con_max, con_open, con_ratio, avg_entry_price, un_pnl

def system_board():
    posi = get_pos()
    st = set_time()

    system_name = 'System' + st[1]
    start_time = st[0]
    exit_time = st[2]
    con_open = posi[0]
    my_position = get_my_position(con_open)


    return system_name, start_time, my_position, con_open, exit_time

def system_logic():
    st = set_time()
    pb = position_board(config.leverage)
    trb = get_trade_bucket_1h(pb[2])

    system_name = 'System'+st[1]
    start_time = st[0]
    start_price = trb[1]
    open_price = trb[2]
    high_price = trb[3]
    low_price = trb[4]
    high_low_price = high_price-low_price
    percent_k = trb[0]
    cal = high_low_price*percent_k
    buy_target = round(start_price+cal)
    sell_target = round(start_price-cal)
    ma_score_buy = trb[5]
    ma_score_sell = trb[6]
    con_ready_buy, con_ready_sell = get_con_ready(pb[4], ma_score_buy, ma_score_sell)

    logger.info(": {}".format(system_name))
    logger.info("ma_buy : {}".format(ma_score_buy))
    logger.info("매수개수 : {}".format(con_ready_buy))
    logger.info("ma_sell : {}".format(ma_score_sell))
    logger.info("매도개수 : {}".format(con_ready_sell))
    logger.info("close price : {}".format(start_price))
    logger.info("매수진입가격 : {}".format(buy_target))
    logger.info("매도진입가격 : {}".format(sell_target))

    return system_name, start_time, start_price, open_price, high_price, low_price, high_low_price, percent_k, buy_target, sell_target, ma_score_buy, ma_score_sell, con_ready_buy, con_ready_sell


# e_orders = [{'orderID': xxx, 'entry_price': xxx, 'price':0, 'orderQty': 0, 'status' : 'None', 'child':'None'}]
# c_orders = {'orderID': yyy, 'price': 0, 'orderQty': 0, 'status': 'None'}

#
#system_Name제대로 나온다
#ma_score는 좀더 두고봐야함
#주문 제대로 들어가는 것 까지만 확인했다 2019-07-24
#ma_score 제대로 나오는것 확인 2019-08-01
#

#실제 프로그램 돌아가는 main이라 봐도 무방
def monitoringTr(orders):

    #변수 세팅
    pb = position_board(config.leverage)
    sb = system_board()
    sl = system_logic()
    cur_price = pb[2]
    start_time = sb[1]
    exit_time = sb[4]

    #현재 시간 세팅
    format = '%Y-%m-%d %H:%M'
    time_now = datetime.datetime.now()
    now = time_now.strftime(format)

    #
    # Step1. 주문
    #
    #주문이 들어가지않았고, 준비상태이면

    for order in orders:
        if order['orderID'] == 'None' and order['status'] == 'Ready':
            #현재가격이 buy_target보다 크면 매수 조건 대로 시장가 주문을 넣음
            if cur_price > order['buy_target'] and order['buyQty'] != 0:
                #주문 정보 = resp
                resp = bitmex.place_market_order(quantity=order['buyQty'])
                time.sleep(0.1)
                #주문 ID와 상태 업데이트
                orderID = resp.get('orderID', 'None')
                if orderID != 'None':
                    order['orderID'] = orderID
                    order['status'] = resp['ordStatus']
                    order['clOrdID'] = resp['clOrdID']
                    print(order['clOrdID'])
                    print(order['status'])
                else:
                    order['status'] = 'Rejected'
                    print('place order cmd error')
            #현재 가격이 sell_target보다 작으면 매도 조건이 됨. 주문을 넣음
            elif cur_price < order['sell_target'] and order['sellQty'] != 0:
                #주문정보 = resp
                resp = bitmex.place_market_order(quantity=order['sellQty'])
                time.sleep(0.1)
                #주문 ID와 상태 업데이트
                orderID = resp.get('orderID', 'None')
                if orderID != 'None':
                    order['orderID'] = orderID
                    order['status'] = resp['ordStatus']
                    order['clOrdID'] = resp['clOrdID']
                    print(order['clOrdID'])
                    print(order['status'])
                else:
                    order['status'] = 'Rejected'
                    print('place order cmd error')
            else:
                #조건이 이도저도 아닌경우
                print("cur_price doesn't fit the conditions")

    #
    # Step2. 주문 정보 조회.
    #
    #주문들 정보 불러오기.
    get_orders = bitmex.http_open_orders(isTerminated=True)
    time.sleep(0.1)

    for order in orders:
        print(order['clOrdID'])

    #
    # Step3. 반대 주문 넣기
    #
    for order in orders:
        for ord in get_orders:
            #clOrdID로 구분해서 정확히 찾아옴
            if order['clOrdID'] == ord['clOrdID']:
                #청산시간이 되었다면
                if now == exit_time:
                    c_order = dict()
                    if ord['side'] == 'Sell':
                        c_order['ordQty'] = ord['orderQty']
                    elif ord['side'] == 'Buy':
                        c_order['ordQty'] = (ord['orderQty'])*(-1)
                    #반대주문으로 청산을 해버린다
                    resp = bitmex.place_market_order(quantity=c_order['ordQty'])
                    time.sleep(0.1)
                    orderID = resp.get('orderID', 'None')
                    c_order['orderID'] = orderID
                    c_order['status'] = resp['ordStatus']
                    c_order['clOrdID'] = resp['clOrdID']
                    #
                    # Step4. 원래 처음 상태로 초기화
                    #
                    order['clOrdID'] = 'None'
                    order['orderID'] = 'None'
                    order['status']  = 'Ready'
                    time.sleep(60)







def main_tradingTr():
    sl = system_logic()

    e_orders = [
        {'buy_target': sl[8],
         'sell_target' : sl[9],
         'orderID': 'None',
         'buyQty' : sl[12],
         'sellQty' : (-sl[13]),
         'status': 'Ready',
         'clOrdID' : 'None'}
    ]

    while True:
        sys.stdout.write("-----\n")
        sys.stdout.flush()
        monitoringTr(e_orders)
        time.sleep(10)




def main_setup():
    logger = setup_logger()

if __name__ == "__main__":

    main_setup()
    main_tradingTr()
