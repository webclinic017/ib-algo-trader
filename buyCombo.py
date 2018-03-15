#! /usr/bin/env python
# -*- coding: utf-8 -*-

from ib.ext.Order import Order
from ib.ext.Contract import Contract
from ib.ext.ContractDetails import ContractDetails
from ib.ext.ComboLeg import ComboLeg
from ib.opt import ibConnection, message
from time import sleep
import pprint
import pickle
import pdb

#-- globals  ------------------------------------------------------------------

conId = -1
nextOrderId = -1

#-- message handlers  ---------------------------------------------------------

# print all messages from TWS
def watcher(msg):
    print msg

def NextValidIdHandler(msg):
    global nextOrderId
    nextOrderId = msg.orderId

def ContractDetailsHandler(msg):
    global contractDetails
    contractDetails = msg.contractDetails

#-- factories -----------------------------------------------------------------

def makeOptContract(sym, exp, strike, right):
    newOptContract = Contract()
    newOptContract.m_symbol = sym
    newOptContract.m_secType = 'OPT'
    newOptContract.m_expiry = exp
    newOptContract.m_strike = strike
    newOptContract.m_right = right
    newOptContract.m_multiplier = 100
    newOptContract.m_exchange = 'SMART'
    newOptContract.m_currency = 'USD'
    return newOptContract

def makeComboLeg(conId, action):
    newComboLeg = ComboLeg()
    newComboLeg.m_conId = conId
    newComboLeg.m_ratio = 1
    newComboLeg.m_action = action
    newComboLeg.m_exchange = 'SMART'
    newComboLeg.m_openClose = '0'
    return newComboLeg

def makeBagContract(sym, legs):
    newBagContract = Contract()
    newBagContract.m_symbol = sym
    newBagContract.m_secType = 'BAG'
    newBagContract.m_exchange = 'SMART'
    newBagContract.m_currency = 'USD'
    newBagContract.m_comboLegs = legs
    return newBagContract

def makeOrder(action, qty, price):
    newOrder = Order()
    newOrder.m_action = action
    newOrder.m_totalQuantity = qty
    newOrder.m_orderType = 'LMT'
    newOrder.m_lmtPrice = price
    newOrder.m_tif = ''
    newOrder.m_parentId = 0
    newOrder.m_discretionaryAmt = 0
    newOrder.m_transmit = True
    return newOrder

#-- utilities  ----------------------------------------------------------------

def getConId(contract):
    global contractDetails

    con.reqContractDetails(contract)

    # wait for TWS message to come back to message handler
    contractDetails = ContractDetails()
    while contractDetails.m_conid == 0:
        sleep(1)

    return contractDetails.m_conid

#-- main  ---------------------------------------------------------------------

if __name__ == '__main__':

    con = ibConnection()
    con.registerAll(watcher)
    con.register(NextValidIdHandler, 'NextValidId')
    con.register(ContractDetailsHandler, 'ContractDetails')
    con.connect()

    con.setServerLogLevel(5)

    # we're going to place an order for an IBM calendar spread:
    # SELL OCT 07 105 CALL, BUY JAN 08 105 CALL

    # define the contract for each leg
    shortLeg = makeOptContract('IBM', '200710', 105, 'CALL')
    longLeg = makeOptContract('IBM', '200801', 105, 'CALL')

    # get the contract ID for each leg
    shortConId = getConId(shortLeg)
    longConId = getConId(longLeg)

    # instantiate each leg
    shortLeg = makeComboLeg(shortConId, 'SELL')
    longLeg = makeComboLeg(longConId, 'BUY')

    #pdb.set_trace()

    # build a bag with these legs
    calendarBagContract = makeBagContract('IBM', [shortLeg, longLeg])

    print calendarBagContract
    print calendarBagContract.__dict__

    # build order to buy 1 spread at $1.66
    buyOrder = makeOrder('BUY', 1, 1.66)

    # buy!  buy!  buy!
    con.placeOrder(nextOrderId, calendarBagContract, buyOrder)

    #p1 = pickle.dumps(calendarBagContract)
    #pprint.pprint(p1)
    #print "\n\n"+p1

    # watch the messages for a bit
    sleep(100)
    

