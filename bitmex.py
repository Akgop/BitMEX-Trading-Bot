#implement your logic here

from __future__ import absolute_import
import requests
import time
import datetime
import json
import base64
import uuid
import logging

from auth.APIKeyAuthWithExpires import APIKeyAuthWithExpires
from utils import constants, errors

class BitMEX(object):

    #생성자
    def __init__(self, apiKey=None, apiSecret=None, base_url=None):
        self.logger = logging.getLogger('root')
        self.base_url = base_url    #URL
        self.symbol = 'XBTUSD'      #통화
        self.postOnly = True        #true = 지정가
        self.orderIDPrefix = 'bitTraining_'
        self.shouldWSAuth = True

        if(apiKey is None):
            raise Exception("Please set an API key and Secret to get started. See " +
                            "https://github.com/BitMEX/sample-market-maker/#getting-started for more information."
                            )

        self.apiKey = apiKey        #apiKey 대입
        self.apiSecret = apiSecret  #apiSecret 대입
        if len(self.orderIDPrefix) > 13:
            raise ValueError("settings.ORDERID_PREFIX must be at most 13 characters long!")
        self.retries = 0        #initialize counter

        # Prepare HTTPS session
        self.session = requests.Session()
        # These headers are always sent
        self.session.headers.update({'user-agent': 'liquidbot-' + constants.VERSION})
        self.session.headers.update({'content-type': 'application/json'})
        self.session.headers.update({'accept': 'application/json'})

        self.timeout = 7


