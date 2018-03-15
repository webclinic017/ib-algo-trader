# ib_api_demo.py

from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.opt import Connection, message



def error_handler(msg):
    """Handles the capturing of error messages"""
    print("Server Error: %s" % msg)

def reply_handler(msg):
    """Handles of server replies"""
    print("Server Response: %s, %s" % (msg.typeName, msg))



def create_contract(symbol, sec_type, exch, prim_exch, curr):
    """Create a Contract object defining what will
    be purchased, at which exchange and in which currency.

    symbol - The ticker symbol for the contract
    sec_type - The security type for the contract ('STK' is 'stock')
    exch - The exchange to carry out the contract on
    prim_exch - The primary exchange to carry out the contract on
    curr - The currency in which to purchase the contract"""
    contract = Contract()
    contract.m_symbol = symbol
    contract.m_secType = sec_type
    contract.m_exchange = exch
    contract.m_primaryExch = prim_exch
    contract.m_currency = curr
    return contract

def makeOptContract(sym, exp, strike, right):
    """ exp should be in (year/month/day) """
    newOptContract = Contract()
    newOptContract.m_symbol = sym
    newOptContract.m_secType = 'OPT'
    newOptContract.m_expiry = exp
    newOptContract.m_strike = strike
    newOptContract.m_right = right
    newOptContract.m_multiplier = 100
    newOptContract.m_exchange = 'SMART'
    newOptContract.m_primaryExch = 'SMART'
    newOptContract.m_currency = 'USD'
    return newOptContract

def create_order(order_type, quantity, action, account):
    """Create an Order object (Market/Limit) to go long/short.

    order_type - 'MKT', 'LMT' for Market or Limit orders
    quantity - Integral number of assets to order
    action - 'BUY' or 'SELL'"""
    order = Order()
    order.m_orderType = order_type
    order.m_totalQuantity = quantity
    order.m_action = action
    order.m_account = account
    return order


if __name__ == "__main__":
    # Connect to the Trader Workstation (TWS) running on the
    # usual port of 7496, with a clientId of 100
    # (The clientId is chosen by us and we will need
    # separate IDs for both the execution connection and
    # market data connection)
    tws_conn = Connection.create(port=7497, clientId=100)
    tws_conn.connect()

    # Assign the error handling function defined above
    # to the TWS connection
    tws_conn.register(error_handler, 'Error')

    # Assign all of the server reply messages to the
    # reply_handler function defined above
    tws_conn.registerAll(reply_handler)

    # Create an order ID which is 'global' for this session. This
    # will need incrementing once new orders are submitted.
    order_id = 42

    # Create a contract in GOOG stock via SMART order routing
    #goog_contract = create_contract('AAPL', 'STK', 'SMART', 'SMART', 'USD')

    # Go long 100 shares of Google
    #goog_order = create_order('MKT', 10, 'BUY', 'DU958186')

    # Use the connection to the send the order to IB
    #tws_conn.placeOrder(order_id, goog_contract, goog_order)


    msft_option = makeOptContract('SPY', '20180615', 280, 'CALL')
    msft_order = create_order('MKT', 100, 'BUY', 'DU958186')
    tws_conn.placeOrder(order_id, msft_option, msft_order)

    #tws_conn.reqMktData(tickId, 'AAPL', False)


    # Disconnect from TWS
    tws_conn.disconnect()



