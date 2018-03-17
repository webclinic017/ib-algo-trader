from ib.opt import ibConnection, message
from ib.ext.Contract import Contract
from time import sleep

def fundamentalData_handler(msg):
    print(msg)

def error_handler(msg):
    print(msg)

tws = ibConnection(port=7496, clientId=100)
tws.register(error_handler, message.Error)
tws.register(fundamentalData_handler, message.fundamentalData)
tws.connect()

c = Contract()
c.m_symbol = 'AAPL'
c.m_secType = 'STK'
c.m_exchange = "SMART"
c.m_currency = "USD"

print("on it")

tws.reqMktData(897,c,"",False)
sleep(50)

tws.disconnect()