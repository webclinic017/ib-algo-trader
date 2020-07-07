import sys
from ibapi.order import Order

class OrderSamples:
    """ <summary>
    #/ A Market order is an order to buy or sell at the market bid or offer price. A market order may increase the likelihood of a fill
    #/ and the speed of execution, but unlike the Limit order a Market order provides no price protection and may fill at a price far
    #/ lower/higher than the current displayed bid/ask.
    #/ Products: BOND, CFD, EFP, CASH, FUND, FUT, FOP, OPT, STK, WAR
    </summary>"""

    @staticmethod
    def MarketOrder(action: str, quantity: float):
        # ! [market]
        order = Order()
        order.action = action
        order.orderType = "MKT"
        order.totalQuantity = quantity
        # ! [market]
        return order

    """ <summary>
    #/ A Limit order is an order to buy or sell at a specified price or better. The Limit order ensures that if the order fills, 
    #/ it will not fill at a price less favorable than your limit price, but it does not guarantee a fill.
    #/ Products: BOND, CFD, CASH, FUT, FOP, OPT, STK, WAR
    </summary>"""

    @staticmethod
    def LimitOrder(action: str, quantity: float, limitPrice: float):
        # ! [limitorder]
        order = Order()
        order.action = action
        order.orderType = "LMT"
        order.totalQuantity = quantity
        order.lmtPrice = limitPrice
        # ! [limitorder]
        return order

class OrderType:
    req_keys = {
        'market': ['type', 'order', 'quantity'],
        'limit': ['type', 'order', 'quantity', 'limit']
    }

    def __init__(self, **kwargs):
        if 'type' not in kwargs:
            raise ValueError(f"Missing arg: {'type'}")

        for k in kwargs.keys():
            self.__setattr__(k, kwargs[k])

        acceptable_order_types = ['market', 'limit']
        if self.__dict__['type'] not in acceptable_order_types:
            raise ValueError(f"type not valid: {self.__dict__['type']}")

        self._order = None
        self._type = self.__dict__['type']

    def set_params(self, **kwargs):
        for k in kwargs.keys():
            self.__setattr__(k, kwargs[k])

    def get_order(self):
        for j in self.req_keys[self._type]:
            if j not in self.__dict__:
                raise ValueError("Missing config argument", j)

        if self._type == 'market':
            return OrderSamples.MarketOrder(self.__dict__['order'],
                                            self.__dict__['quantity'])

        if self._type == 'limit':
            return OrderSamples.LimitOrder(self.__dict__['order'],
                                           self.__dict__['quantity'],
                                           self.__dict__['limit'])

if __name__ == "__main__":
    market_order = OrderType(type='market', order="BUY", quantity="100").get_order()