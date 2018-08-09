import datetime
from pyrate.builder import Builder
from pyrate.ttapi.manager import Manager
from pyrate.ttapi.order import TTAPIOrder
from ttapi import aenums, cppclient
from ttapi.client.type_converters import date2_ttDate
from captain.controlled import controlled_name_type, ControlledName
from captain.lib.controlled_types import Tif
priceSession = Manager().getPriceSession()
orderSession = Manager().getOrderFillSession()
custDefaults = Manager().getCustomer()
ordSrv = Manager().getOrderServer()
priceSrv = Manager().getPriceServer()
pricey=12000
tiffies = ('GTD', 'GTDATE')#'IOC', 'FOK',
restr = (None, aenums.TT_FOK_ORDER_RES, aenums.TT_IOC_ORDER_RES)
products = priceSession.getProducts(prodType=aenums.TT_PROD_FUTURE)
for product in products:
    if "FUTURE" not in str(product.prod_type):
        pricey=3
    contracts = priceSession.getContracts(product)#, contractKeys=["NKH22", ])
    for contract in contracts:
        for tiffy in tiffies:
            restriction = None
            if tiffy == 'IOC':
                restriction = aenums.TT_IOC_ORDER_RES
                tiffy = 'GTD'
            if tiffy == 'FOK':
                restriction = aenums.TT_FOK_ORDER_RES
                tiffy = 'GTD'
            pricey = (cppclient.TTTick.PriceIntToInt(pricey, contract, +1))
            orderParams = dict(order_qty=10, buy_sell=aenums.TT_SELL, order_action=aenums.TT_ORDER_ACTION_ADD, limit_prc=pricey, order_type=aenums.TT_LIMIT_ORDER, tif=tiffy, srs=contract, exchange_clearing_account=custDefaults.exchange_clearing_account, free_text=custDefaults.free_text)
            newOrder = TTAPIOrder()
            newOrder.setFields(**orderParams)
            if tiffy == 'GTDATE':
                newOrder.order_exp_date = date2_ttDate(datetime.datetime(year=2018, month=8, day=8))
            if tiffy == 'IOC':
                newOrder.order_restrict = aenums.TT_IOC_ORDER_RES
                # newOrder.tiffy = 'GTD'
            if tiffy == 'FOK':
                newOrder.order_restrict = aenums.TT_FOK_ORDER_RES
                # newOrder.tiffy = 'GTD'
            orderSession.send(newOrder)
        break




    # break

