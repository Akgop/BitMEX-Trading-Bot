
from bitmex import *

API_KEY    = 'lnniEngzI0Gt-_snI1T_OA3s'
API_SECRET = 'WmHRxZgwxhcqMDKTXdwamYnUK_6Y84bN6XWQOc2zCNhWvhsg'
BASE_URL   = 'https://testnet.bitmex.com/api/v1/'

bitmex = BitMEX(apiKey= API_KEY, apiSecret= API_SECRET, base_url=BASE_URL)
gm = bitmex.get_margin()
wallet_balance = gm['walletBalance']

print('Wallet Balance : ' , wallet_balance)
print('Levarage : ')        #적용배율 직접 입력
print('Current Price : ')   #현재시세 받아오기
print('1USD : ') # 1 / 현재가
print('Contracts Max : ')        # 주문가능수량 = (지갑잔고 * 레버리지 ) / 1USD
print('Contracts Open : ')       # 현재보유수량 받아오기
print('Contracts Ratio : ')      # 보유 비율 = abs(보유수량) / 주문가능수량
print('Entry Price : ')          # 진입가격 = 보유 포지션의 평균 진입가격
print('Unrealised PNL : ')       # 평가손익 = 지갑잔고 XBt증감,
                              # 매수 = 보유수량*((1/진입가격)-(1/현재가))
                              # 매도 = abs(보유수량)*((1/진입가격) - (1/현재가))
