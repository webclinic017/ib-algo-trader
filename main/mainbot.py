import sys
import datetime, time
sys.path.insert(0, '../../../extralibrary/TWS API/samples/Python')

from pathlib import Path
import pandas as pd
import numpy as np
from ibapi.contract import *
from Testbed.OrderSamples import OrderSamples
import IB_ReqMarketData as ib_reqmarket
import IB_custom_order as ib_order

class data_file:
    """
    Writes to csv, current time and ticker price
    """
    def __init__(self, ticker, price):
        self.ticker = ticker
        self.price = price
        self.data_path = './data_historical/'
        self.data_file = 'data_{}.csv'.format(ticker)
        self.check = False

    def check_data_file(self):
        config = Path(self.data_path + self.data_file)
        if config.is_file():
            self.check = True
        else:
            self.check = False

    def write_to_data(self):
        if self.check:
            df = pd.read_csv(Path('./data_historical/') / 'data_{}.csv'.format(self.ticker))
            df = df.append({'date': datetime.datetime.now(), 'price': self.price}, ignore_index=True)
            df.to_csv(Path('./data_historical/') / 'data_{}.csv'.format(self.ticker), index=False)

        else:
            df = pd.DataFrame(columns=['date', 'price'])
            df = df.append({'date': datetime.datetime.now(), 'price': self.price}, ignore_index=True)
            df.to_csv(Path('./data_historical/') / 'data_{}.csv'.format(self.ticker), index=False)




def order_type(**kwargs):

    def check(params, kwarg_params):
        for param in params:
            if param not in kwarg_params:
                print("Missing params: {0}".format(param))
                return False
            else:
                pass
        return True

    """
    :param kwargs:
    type : ["limit", "market"]
    order : ["BUY", "SELL"]
    quantity : amount, int
    limit : limit amount, int
    """
    if 'type' in kwargs:
        if kwargs['type'] == 'limit':
            params = ['order', 'quantity', 'limit']
            if check(params, kwargs):
                return OrderSamples.LimitOrder(kwargs['order'], kwargs['quantity'], kwargs['limit'])

        elif kwargs['type'] == 'market':
            params = ['order', 'quantity']
            if check(params, kwargs):
                return OrderSamples.MarketOrder(kwargs['order'], kwargs['quantity'])
    else:
        print('Missing param: type')

def main():
    ticker = "SPY"

    contract = Contract()
    contract.symbol = ticker
    contract.secType = "STK"
    contract.currency = "USD"
    contract.exchange = "SMART"
    contract.primaryExchange = 'NASDAQ'

    limit_order = order_type(type="limit", order="BUY", quantity="100", limit=74)
    market_order = order_type(type="market", order="BUY", quantity="100")

    for i in range(2):
        price = ib_reqmarket.main(ticker)

        data_historical = data_file(ticker,price)
        data_historical.check_data_file()
        data_historical.write_to_data()

        if price > 72:
            ib_order.main(contract, market_order)
            print("Current value is", price, "Buying 100 shares.")
        else:
            print("Current value is", price, "Do nothing.")
        time.sleep(3)


if __name__ == '__main__':
    main()