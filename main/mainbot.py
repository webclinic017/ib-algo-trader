import IB_BuyOrder as ib_buy
import IB_ReqMarketData as ib_reqmarket

import time

for i in range(100):
    price = ib_reqmarket.main("XLK")
    if price > 285:
        ib_buy.main("XLK")
        print("Current value is ", price, "Buying 100 shares.")
    else:
        print("Current value is ", price, "Do nothing.")
    time.sleep(3)
