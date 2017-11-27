#~TestCaseName: TestCreatePositions
#~Exchange/Simulator/Both: Both
#~Pyrate Version: 2.0

import datetime
from pyrate.builder import Builder
from pyrate.ttapi.manager import Manager
from pyrate.ttapi.order import TTAPIOrder
from ttapi import aenums, cppclient
from captain.controlled import controlled_name_type, ControlledName
from captain.lib.controlled_types import Tif
priceSession = Manager().getPriceSession()
orderSession = Manager().getOrderFillSession()
custDefaults = Manager().getCustomer()
ordSrv = Manager().getOrderServer()
priceSrv = Manager().getPriceServer()
pricey=12000
tiffies = ('GTD', 'GTC', 'GTDATE')
products = priceSession.getProducts()
for product in products:
    if "FUTURE" not in str(product.prod_type):
        pricey=3
    contracts = priceSession.getContracts(product)
    for contract in contracts:
        for tiffy in tiffies:
            orderParams = dict(order_qty=1000, buy_sell=aenums.TT_SELL, order_action=aenums.TT_ORDER_ACTION_ADD, limit_prc=pricey, order_type=aenums.TT_LIMIT_ORDER, tif=tiffy, srs=contract, exchange_clearing_account=custDefaults.exchange_clearing_account, free_text=custDefaults.free_text)
            newOrder = TTAPIOrder()
            newOrder.setFields(**orderParams)
            orderSession.send(newOrder)
        break
    break

