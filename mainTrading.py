from bitmex import BitMEX
from mainDialog import *

import logging
import time
import os, sys


API_KEY, API_SECRET = MyWindow.login_cmd()

bitmex = BitMEX(apiKey=API_KEY, apiSecret=API_SECRET,base_url='https://testnet.bitmex.com/api/v1/')


