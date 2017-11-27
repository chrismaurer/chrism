import os, shutil, subprocess
from ttapi import aenums, cppclient
from pyrate.manager import Manager
from pyrate.ttapi.predicates import OrderTableAddPred
from pyrate.ttapi.order import TTAPIOrder
ps = Manager.getPriceSession()
os = Manager.getOrderSession()
p = ps.getProducts()[10]
c = ps.getContracts(p)[0]
orderParams = dict(order_action=aenums.TT_ORDER_ACTION_ADD,srs=c,order_qty=25,tif='GTC',buy_sell=aenums.TT_BUY,order_type=aenums.TT_LIMIT_ORDER,limit_prc=10000,acct_type=cppclient.AEnum_Account.TT_ACCT_AGENT_1,user_name='CHRIS',exchange_clearing_account='DIRECT')
myOrder = TTAPIOrder()
myOrder.setFields(**orderParams)
callbacks = os.sendAndWait(myOrder, filters='OnOrderTableAdd')
orderCallback = callbacks['OnOrderTableAdd'][0]['order']
