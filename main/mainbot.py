from ibapi.contract import *

import sys
sys.path.insert(0, '../../../extralibrary/TWS API/samples/Python')
from Testbed.OrderSamples import OrderSamples


import IB_ReqMarketData as ib_reqmarket
import IB_custom_order as ib_order

import time


def check(params, kwarg_params):
    for param in params:
        if param not in kwarg_params:
            print("Missing params: {0}".format(param))
            return False
        else:
            pass
    return True


def order_type(**kwargs):
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
    contract = Contract()
    contract.symbol = "XLK"
    contract.secType = "STK"
    contract.currency = "USD"
    contract.exchange = "SMART"
    contract.primaryExchange = 'NASDAQ'

    limit_order = order_type(type="limit", order="BUY", quantity="100", limit=74)
    market_order = order_type(type="market", order="BUY", quantity="100")

    for i in range(2):
        price = ib_reqmarket.main("XLK")
        if price > 72:
            ib_order.main(contract, market_order)
            print("Current value is", price, "Buying 100 shares.")
        else:
            print("Current value is", price, "Do nothing.")
        time.sleep(3)


if __name__ == '__main__':
    main()
