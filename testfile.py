
from bitmex import *

API_KEY    = 'lnniEngzI0Gt-_snI1T_OA3s'
API_SECRET = 'WmHRxZgwxhcqMDKTXdwamYnUK_6Y84bN6XWQOc2zCNhWvhsg'
BASE_URL   = 'https://testnet.bitmex.com/api/v1/'

bitmex = BitMEX(apiKey= API_KEY, apiSecret= API_SECRET, base_url=BASE_URL)
gm = bitmex.get_margin()
wallet_balance = gm["walletBalance"]
margin_balance = gm['marginBalance']

print('Wallet Balance : ' , wallet_balance)
print('Margin Balance : ' , margin_balance)
