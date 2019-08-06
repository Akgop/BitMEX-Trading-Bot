from update_sql import *
from bitmexTr1 import *


import time
import datetime
import os, sys
import logging
import copy

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



#실제 프로그램 돌아가는 main이라 봐도 무방 (HTTP REQ : 주문넣기(1회), 주문확인(6회), 주문청산(1회))
def monitoringTr(orders):
    #변수 세팅
    my_ord = dict()
    func = Functions()
    system_time_json, system_number, exit_time_json = func.set_time()

    #position http request 실행 (HTTP REQ 1회 발생), 현재가 sql에 저장하고 받아옴 system00d에서만 10초마다 불러올것.
    cur_price = fetch_current_price()
    print(cur_price)

    #현재 시간 세팅
    format = '%Y-%m-%d %H:%M'
    time_now = datetime.datetime.now()
    now = time_now.strftime(format)
    print(exit_time_json, " ", now)
    #
    # Step1. 주문
    #
    #주문이 들어가지않았고, 준비상태이면
    #주문이 1개지만 list이기때문에 for문 사용.    (HTTP REQUEST : 주문 도합 1회)
    for order in orders:
        if order['orderID'] is 'None' and order['status'] is 'Ready':
            #현재가격이 buy_target보다 크면 매수 조건 대로 시장가 주문을 넣음
            if cur_price > order['buy_target'] and order['buyQty'] != 0:
                #주문 정보 = resp   (HTTP REQ : 1회)
                resp = func.bitmex.place_market_order(quantity=order['buyQty'])
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
                #주문정보 = resp    (HTTP REQ : 1회)
                resp = func.bitmex.place_market_order(quantity=order['sellQty'])
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
    # Step 2. 주문 청산하기
    #
    for order in orders:
        #주문이 체결된 경우.
        if order['clOrdID'] is not 'None':
            #
            # Step 2-1 : 시간청산
            #
            #my_ord dict 가 비어있는 경우 my_ord dict를 채워줌.
            if not bool(my_ord):
                get_orders = func.bitmex.http_open_orders(isTerminated=True)
                for ord in get_orders:
                    if order['clOrdID'] == ord['clOrdID']:
                        my_ord = copy.deepcopy(ord)

            if 'clOrdID' in my_ord:
                if order['clOrdID'] == my_ord['clOrdID']:
                    print(my_ord)
                    print(order)
                    if now == exit_time_json:
                        c_order = dict()
                        if my_ord['side'] == 'Sell':
                            c_order['ordQty'] = my_ord['orderQty']
                        elif my_ord['side'] == 'Buy':
                            c_order['ordQty'] = (my_ord['orderQty']) * (-1)
                        # 반대주문으로 청산을 해버린다
                        print(c_order)
                        resp = func.bitmex.place_market_order(quantity=c_order['ordQty'])
                        time.sleep(0.1)
                        orderID = resp.get('orderID', 'None')
                        c_order['orderID'] = orderID
                        c_order['status'] = resp['ordStatus']
                        c_order['clOrdID'] = resp['clOrdID']
                        #
                        # Step 3. 주문상태 초기화.
                        #
                        order['clOrdID'] = 'None'
                        order['orderID'] = 'None'
                        order['status'] = 'Ready'
                        time.sleep(60)
            else:
                print("Key error : no clOrdID")

    '''
    #
    # Step2. 주문 정보 조회.
    #
    # 주문들 정보 불러오기.   (HTTP REQ : 1회)
    get_orders = func.bitmex.http_open_orders(isTerminated=True)
    time.sleep(0.1)

    #
    # Step3. 반대 주문 넣기
    #
    for order in orders:
        for ord in get_orders:
            #clOrdID로 구분해서 정확히 찾아옴
            if order['clOrdID'] == ord['clOrdID']:
                #청산시간이 되었다면
                if now == exit_time_json:
                    c_order = dict()
                    if ord['side'] == 'Sell':
                        c_order['ordQty'] = ord['orderQty']
                    elif ord['side'] == 'Buy':
                        c_order['ordQty'] = (ord['orderQty'])*(-1)
                    #반대주문으로 청산을 해버린다
                    resp = func.bitmex.place_market_order(quantity=c_order['ordQty'])
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
                    time.sleep(60)'''


#맨 처음(초기화면이라고 볼 수 있음.), 주문정보 세팅하는 함수 (HTTP REQ : user/margin, 총 1회)
def set_order():
    #sql 에서 정보 가져와서 buy,sell target 정해줌
    system_name, endTime, open_price, close_price, high_price, low_price, buy_flag, sell_flag, percent_k = fetch_trade_bucketed_data()
    high_low_price = float(high_price) - float(low_price)
    cal = high_low_price * float(percent_k)
    start_price = float(close_price)
    ma_score_buy = float(buy_flag)
    ma_score_sell = float(sell_flag)

    buy_target = round(start_price + cal)
    sell_target = round(start_price - cal)

    #매수 매도 수량 정해줌 con_open, ma_score_buy, ma_score_sell
    func = Functions()
    wallet = func.get_my_wallet()
    cur_price = fetch_current_price()
    usd1 = func.get_1usd(cur_price)
    con_max = func.get_con_max(wallet,usd1)
    cr_buy, cr_sell = func.get_con_ready(con_max, ma_score_buy, ma_score_sell)

    e_orders = [
        {'buy_target': buy_target,
         'sell_target': sell_target,
         'orderID': 'None',
         'buyQty': cr_buy,
         'sellQty': (-cr_sell),
         'status': 'Ready',
         'clOrdID': 'None'}
    ]

    logger.info("내 잔고: {}".format(wallet))
    logger.info("매수진입 가격: {}".format(buy_target))
    logger.info("매수진입 개수: {}".format(cr_buy))
    logger.info("매도진입 가격: {}".format(sell_target))
    logger.info("매도진입 개수: {}".format(cr_sell))
    logger.info("주문가능수량: {}".format(con_max))

    return e_orders

#무한으로 트레이딩 시스템 돌리는 메인함수
def main_tradingTr():
    e_orders = set_order()

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
