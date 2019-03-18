import IB_BuyOrder_Market as ib_buy_market
import IB_BuyOrder_Limit as ib_buy_limit
import IB_SellOrder_Market as _ib_sell_market

import IB_ReqMarketData as ib_reqmarket


import time

for i in range(2):
    price = ib_reqmarket.main("XLK")
    if price > 72:
        ib_buy_limit.main("XLK", 73)
        print("Current value is ", price, "Buying 100 shares.")
    else:
        print("Current value is ", price, "Do nothing.")
    time.sleep(3)
