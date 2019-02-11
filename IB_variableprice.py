import sys
sys.path.insert(0, '../../extralibrary/TWS API/samples/Python')


from Testbed.OrderSamples import OrderSamples
from ibapi import wrapper
from ibapi.client import EClient
from ibapi.common import *
from ibapi.contract import *
from ibapi.ticktype import *
from ibapi.utils import iswrapper  # just for decorator
from time import sleep


class TestApp(wrapper.EWrapper, EClient):
    def __init__(self, stock_ticker):
        wrapper.EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)
        self.bank = 0
        self.stock_ticker = stock_ticker

    @iswrapper
    def nextValidId(self, orderId:int):
        print("setting nextValidOrderId: %d", orderId)
        self.nextValidOrderId = orderId
        #here is where you start using api
        contract = Contract()
        contract.symbol = self.stock_ticker
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        self.reqMarketDataType(4)
        self.reqMktData(1101, contract, "", False, False , [])

    @iswrapper
    def error(self, reqId:TickerId, errorCode:int, errorString:str):
        print("Error. Id: " , reqId, " Code: " , errorCode , " Msg: " , errorString)

    @iswrapper
    def tickPrice(self, reqId: TickerId , tickType: TickType, price: float,
                  attrib:TickAttrib):
        print("Tick Price. Ticker Id:", reqId, "tickType:", tickType, "Price:", price)
        #this will disconnect and end this program because loop finishes
        self.done = True
        self.bank = price

    def print_bank(self):
        return self.bank



def main():

    stock_contract = Contract()
    stock_contract.symbol = 'SPY'
    stock_contract.secType = 'STK'
    stock_contract.exchange = 'SMART'
    stock_contract.currency = 'USD'
    stock_contract.primaryExchange = 'NASDAQ'

    app = TestApp('SPY')
    app.connect("localhost", 7497, clientId=100)
    print("serverVersion:%s connectionTime:%s" % (app.serverVersion(),
                                                app.twsConnectionTime()))
    #app.reqContractDetails(1101+1, stock_contract)
    app.placeOrder(1101+9, stock_contract, OrderSamples.LimitOrder("BUY", 100, 271))
    app.run()
    dolla = app.print_bank()
    return dolla


if __name__ == "__main__":
    main()

