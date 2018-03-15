import pandas as pd
import numpy as np
import time
from datetime import datetime
from ib.ext.EWrapperMsgGenerator import updateAccountTime
from ib.ext.Contract import Contract
from ib.ext.EClientSocket import EClientSocket
from ib.ext.ScannerSubscription import ScannerSubscription
from ib.opt import Connection, message

accountName = 'DU958186'
callback = EWrapperMsgGenerator
tws=EClientSocket(callback)
host=''
port=7497
clientId=100

tws.eConnect(host,port,clientId)

