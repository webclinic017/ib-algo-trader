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

    def set_order(self, contract, order):
        self.contract = contract
        self.order = order

    @iswrapper
    def nextValidId(self, orderId:int):
        print("setting nextValidOrderId: %d", orderId)
        self.nextValidOrderId = orderId
        #here is where you start using api
        self.reqMarketDataType(4)
        self.reqMktData(1000, self.contract, "", False, False, [])
        self.placeOrder(self.nextValidOrderId, self.contract, self.order)


    @iswrapper
    def error(self, reqId:TickerId, errorCode:int, errorString:str):
        print("Error. Id: " , reqId, " Code: " , errorCode , " Msg: " , errorString)

    @iswrapper
    def tickPrice(self, reqId: TickerId , tickType: TickType, price: float,
                  attrib:TickAttrib):
        print("Tick Price. Ticker Id:", reqId, "tickType:", tickType, "Price:", price)
        #this will disconnect and end this program because loop finishes
        self.done = True

def main(contract, order):
    app = TestApp()
    app.set_order(contract, order)
    app.connect("127.0.0.1", 7497, clientId=100)
    print("serverVersion:%s connectionTime:%s" % (app.serverVersion(),
                                                app.twsConnectionTime()))
    app.run()

if __name__ == "__main__":
    main()