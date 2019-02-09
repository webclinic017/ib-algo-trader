import re
import ib
from ib.ext.Contract import Contract
from ib.opt import ibConnection, message
from time import sleep

class Downloader(object):
    field4price = ''

    def __init__(self):
        self.tws = ibConnection('localhost', 4001, 0)
        self.tws.register(self.tickPriceHandler, 'TickPrice')
        self.tws.connect()
        self._reqId = 2 # current request id

    def tickPriceHandler(self,msg):
        if msg.field == 4:
            self.field4price = msg.price
            #print '[debug]', msg

    def requestData(self,contract):
        self.tws.reqMktData(self._reqId, contract, '', 1)
        self._reqId+=1

def makeOptContract(sym, exp, strike, right):
    """ exp should be in (year/month/day) """
    newOptContract = Contract()
    newOptContract.m_symbol = sym
    newOptContract.m_secType = 'OPT'
    newOptContract.m_expiry = exp
    newOptContract.m_strike = strike
    newOptContract.m_right = right
    newOptContract.m_multiplier = 100
    newOptContract.m_exchange = 'SMART'
    newOptContract.m_primaryExch = 'SMART'
    newOptContract.m_currency = 'USD'
    return newOptContract

if __name__=='__main__':
    dl = Downloader()
    c = Contract()
    c.m_symbol = 'SPY'
    c.m_secType = 'STK'
    c.m_exchange = 'SMART'
    c.m_currency = 'USD'

    #c = makeOptContract('SPY', '20190219', 270, 'CALL')

    dl.requestData(c)
    sleep(3)
    print('Price - field 4: ', dl.field4price)