import sys
import datetime, time
sys.path.insert(0, '../../../extralibrary/TWS API/samples/Python')

from pathlib import Path
import pandas as pd
import numpy as np
from ibapi.contract import *
import IB_ReqMarketData as ib_reqmarket
import IB_CustomOrder as ib_order
import IB_CurrentPositions as ib_positions
import IB_OpenOrders as ib_openorder
from IB_OrderType import OrderType

accountID = "DU2422130"
ticker = "SPY"

contract = Contract()
contract.symbol = ticker
contract.secType = "STK"
contract.currency = "USD"
contract.exchange = "SMART"
contract.primaryExchange = 'NASDAQ'

threshold_price = 316.5

while True:
# for i in range(2):
    print(f"\n")
    print(datetime.datetime.today().strftime("%d/%m/%Y %H:%M:%S"))

    all_positions = ib_positions.main()
    df_positions = pd.DataFrame(all_positions,
                                columns=['account', 'symbol', 'position',
                                         'avgCost'])
    df_positions = df_positions[df_positions['account'].isin([accountID])]

    ### If current price is above threshold_price & has no positions
    ### then buy (or cover), otherwise do nothing
    ### If current price is below threshold_price, & has no positions
    ### then do nothing, otherwise sell (or short)

    shares = df_positions[df_positions['symbol'].isin([ticker])]['position'].sum()
    price = ib_reqmarket.main(ticker)
    print(f"Current value is {price}, threshold: {threshold_price}")

    if price == -1:
        print("breaking...")
        break

    if price > threshold_price:
        if shares > 0:
            print(f"Position: {ticker}, Shares: {shares} --- Do nothing.")
            pass
        else:
            # Check for open positions before buying.
            if not ib_openorder.main():
                market_buy = OrderType(type='market', order="BUY", quantity="100").get_order()
                ib_order.main(contract, market_buy)
                print(f"Position: {ticker}, Shares: {shares} --- Buying (or Covering) 100 Shares.")
    else:
        if shares < 0:
            print(f"Position: {ticker}, Shares: {shares} --- Do nothing.")
            pass

        else:
            # Check for open positions before buying.
            if not ib_openorder.main():
                market_sell = OrderType(type='market', order="SELL", quantity="100").get_order()
                ib_order.main(contract, market_sell)
                print(f"Position: {ticker}, Shares: {shares} --- Selling (or Shorting) 100 Shares.")

    time.sleep(10)