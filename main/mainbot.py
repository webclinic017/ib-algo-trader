from ib.opt import ibConnection, message
from ib.ext.Contract import Contract
from time import sleep


def my_callback_handler(msg):
    inside_mkt_bid = ''
    inside_mkt_ask = ''

    if msg.field == 1:
        inside_mkt_bid = msg.price
        print('bid', inside_mkt_bid)
    elif msg.field == 2:
        inside_mkt_ask = msg.price
        print('ask', inside_mkt_ask)

def getbids(n):
    # n = 'ticker'
    tws = ibConnection(port=7497, clientId=100)
    tws.register(my_callback_handler, message.tickSize, message.tickPrice)
    tws.connect()

    c = Contract()
    c.m_symbol = n
    c.m_secType = "OPT"
    c.m_exchange = "SMART"
    c.m_currency = "USD"

    showbids = tws.reqMktData(1,c,"",False)
    print(showbids)
    tws.disconnect()

getbids('SPY')