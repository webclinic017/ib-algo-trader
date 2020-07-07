"""
    Deprecated do not use

"""

# Interactive Brokers functions to import data

def read_positions(): #read all accounts positions and return DataFrame with information

    from ibapi import wrapper
    from ibapi.client import EClient
    from ibapi.wrapper import EWrapper
    from ibapi.common import TickerId
    import pandas as pd
    import time

    class ib_class(wrapper.EWrapper, EClient):
        def __init__(self):
            wrapper.EWrapper.__init__(self)
            EClient.__init__(self, wrapper=self)
            self.all_positions = pd.DataFrame([], columns = ['Account','Symbol', 'Quantity', 'Average Cost', 'Sec Type'])

        def error(self, reqId:TickerId, errorCode:int, errorString:str):
            if reqId > -1:
                print("Error. Id: " , reqId, " Code: " , errorCode , " Msg: " , errorString)

        def position(self, account, contract, pos, avgCost):
            index = str(account)+str(contract.symbol)
            self.all_positions.loc[index]=account,contract.symbol,pos,avgCost,contract.secType

        def positionEnd(self):
            self.disconnect()

    ib_api = ib_class()
    ib_api.connect("127.0.0.1", 7497, 10)
    ib_api.reqPositions()
    current_positions = ib_api.all_positions
    ib_api.run()

    return(current_positions)


def read_navs(): #read all accounts NAVs

    from ibapi.client import EClient
    from ibapi.wrapper import EWrapper
    from ibapi.common import TickerId
    import pandas as pd
    import time

    class ib_class(EWrapper, EClient):
        def __init__(self):
            EClient.__init__(self, self)
            self.all_accounts = pd.DataFrame([], columns = ['reqId','Account', 'Tag', 'Value' , 'Currency'])

        def error(self, reqId:TickerId, errorCode:int, errorString:str):
            if reqId > -1:
                print("Error. Id: " , reqId, " Code: " , errorCode , " Msg: " , errorString)

        def accountSummary(self, reqId, account, tag, value, currency):
            if tag == 'NetLiquidationByCurrency':
                index = str(account)
                self.all_accounts.loc[index]=reqId, account, tag, value, currency

        def accountSummaryEnd(self, reqId:int):
                self.disconnect()

    ib_api = ib_class()
    ib_api.connect("127.0.0.1", 7497, 10)
    ib_api.reqAccountSummary(9001,"All","$LEDGER")
    current_nav = ib_api.all_accounts
    ib_api.run()

    return(current_nav)

if __name__ == "__main__":
    all_positions = read_positions()
    print(all_positions)