
from bitmex import *

API_KEY    = 'lnniEngzI0Gt-_snI1T_OA3s'
API_SECRET = 'WmHRxZgwxhcqMDKTXdwamYnUK_6Y84bN6XWQOc2zCNhWvhsg'
BASE_URL   = 'https://testnet.bitmex.com/api/v1/'

bitmex = BitMEX(apiKey= API_KEY, apiSecret= API_SECRET, base_url=BASE_URL)

inst = bitmex.instruments(count=100, reverse=False)

low_price = inst[0]['lowPrice']   #24시간 이전부터 지금까기 최저가
high_price = inst[0]['highPrice'] #24시간 이전부터 지금까지 최고가
last_price = inst[0]['lastPrice'] #현재가

ob = bitmex.order(count=1, reverse=True)

side = ob[0]['side']
print(side)
