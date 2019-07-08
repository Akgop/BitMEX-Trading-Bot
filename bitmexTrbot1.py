from bitmex import BitMEX

import logging
import time
import os, sys

from mainDialog import *

API_KEY, API_SECRET, BASE_URL = MyWindow.pushButtonClicked()


print(API_KEY, API_SECRET, BASE_URL)