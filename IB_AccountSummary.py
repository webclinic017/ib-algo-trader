from ibapi import wrapper
from ibapi.client import EClient
from ibapi.utils import iswrapper #just for decorator
from ibapi.common import *

class TestApp(wrapper.EWrapper, EClient):
    def __init__(self):
        wrapper.EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)

    @iswrapper
    def nextValidId(self, orderId:int):
        print("setting nextValidOrderId: %d", orderId)
        self.nextValidOrderId = orderId
        # here is where you start using api
        self.reqAccountSummary(9002, "All", "$LEDGER")

    @iswrapper
    def error(self, reqId:TickerId, errorCode:int, errorString:str):
        print("Error. Id: " , reqId, " Code: " , errorCode , " Msg: " , errorString)

    @iswrapper
    def accountSummary(self, reqId:int, account:str, tag:str, value:str, currency:str):
        print("Acct Summary. ReqId:" , reqId , "Acct:", account,
            "Tag: ", tag, "Value:", value, "Currency:", currency)

    @iswrapper
    def accountSummaryEnd(self, reqId:int):
        print("AccountSummaryEnd. Req Id: ", reqId)
        # now we can disconnect
        self.disconnect()

def main():
    app = TestApp()
    app.connect("127.0.0.1", 7497, clientId=100)
    app.run()

if __name__ == "__main__":
    main()