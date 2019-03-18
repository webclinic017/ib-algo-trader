from ibapi import wrapper
from ibapi.client import EClient
from ibapi.utils import iswrapper #just for decorator
from ibapi.common import *
from ibapi.contract import *
from ibapi.ticktype import *

import sys
sys.path.insert(0, '../../../extralibrary/TWS API/samples/Python')
from Testbed.OrderSamples import OrderSamples

class TestApp(wrapper.EWrapper, EClient):
    def __init__(self):
        wrapper.EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)

    def set_stock_symbol(self,stock):
        self.stock_symbol = stock

    def set_limit_price(self, limit_price):
        self.limit_price = limit_price

    @iswrapper
    def nextValidId(self, orderId:int):
        print("setting nextValidOrderId: %d", orderId)
        self.nextValidOrderId = orderId
        #here is where you start using api
        contract = Contract()
        contract.symbol = self.stock_symbol
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        contract.primaryExchange = 'NASDAQ'
        self.reqMarketDataType(4)
        self.reqMktData(1002, contract, "", False, False, [])
        self.placeOrder(self.nextValidOrderId, contract, OrderSamples.LimitOrder("BUY", 100, self.limit_price))


    @iswrapper
    def error(self, reqId:TickerId, errorCode:int, errorString:str):
        print("Error. Id: " , reqId, " Code: " , errorCode , " Msg: " , errorString)

    @iswrapper
    def tickPrice(self, reqId: TickerId , tickType: TickType, price: float,
                  attrib:TickAttrib):
        print("Tick Price. Ticker Id:", reqId, "tickType:", tickType, "Price:", price)
        #this will disconnect and end this program because loop finishes
        self.done = True

def main(stock_symbol, limit_price):
    app = TestApp()
    app.set_stock_symbol(stock_symbol)
    app.set_limit_price(limit_price)
    app.connect("127.0.0.1", 7497, clientId=100)
    print("serverVersion:%s connectionTime:%s" % (app.serverVersion(),
                                                app.twsConnectionTime()))
    app.run()

if __name__ == "__main__":
    main()