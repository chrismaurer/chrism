import datetime
import time
from pyrate.builder import Builder
from pyrate.ttapi.manager import Manager
from pyrate.ttapi.order import TTAPIOrder
from pyrate.ttapi.customer import TTAPICustomer
from ttapi import aenums, cppclient
from ttapi.client.type_converters import date2_ttDate
from captain.controlled import controlled_name_type, ControlledName
from captain.lib.controlled_types import Tif
priceSession = Manager().getPriceSession()
orderSession = Manager().getOrderFillSession()
custDefaults = Manager().getCustomer()
ordSrv = Manager().getOrderServer()
priceSrv = Manager().getPriceServer()
tiffies = ('GTD', 'GTC', 'GTDATE', 'GIS')#, 'FOK')
restr = (None, aenums.TT_FOK_ORDER_RES, aenums.TT_IOC_ORDER_RES)
products = priceSession.getProducts(prodType=aenums.TT_PROD_FUTURE, prodName="EY")
time.sleep(60)
for product in products:
    contracts = priceSession.getContracts(product, contractKeys=["00B0KS00EYZ", "00B0LW00EYZ", "00B0IX00EYZ"])
    for contract in contracts:
        settlement_price = None
        for enum, price in priceSession.getPrices(contract).items():
            if "SETTL" in str(enum):
                settlement_price = price.value
        if settlement_price is None:
            if "FUTURE" in str(product):
                settlement_price = 100
            elif "OPTION" in str(product):
                settlement_price = 15
            else:
                settlement_price = 15
        pricey = settlement_price
        for tiffy in tiffies:
            restriction = None
            if tiffy == 'IOC':
                restriction = aenums.TT_IOC_ORDER_RES
                tiffy = 'GTD'
            if tiffy == 'FOK':
                restriction = aenums.TT_FOK_ORDER_RES
                tiffy = 'GTD'
            pricey = (cppclient.TTTick.PriceIntToInt(pricey, contract, +1))
            stop_pricey = (cppclient.TTTick.PriceIntToInt(pricey, contract, -2))
            orderParams = dict(acct_type=cppclient.AEnum_Account.TT_ACCT_AGENT_1, order_qty=500, buy_sell=aenums.TT_SELL, order_action=aenums.TT_ORDER_ACTION_ADD, limit_prc=pricey, order_type=aenums.TT_LIMIT_ORDER, tif=tiffy, srs=contract, exchange_clearing_account=custDefaults.exchange_clearing_account)#, stop_prc=stop_pricey)
            newOrder = TTAPIOrder()
            newOrder.setFields(**orderParams)
            # newOrder.order_flags = aenums.TT_IF_TOUCHED_MOD_CODE
            if restriction is not None:
                newOrder.order_restrict = restriction
            if tiffy == 'GTDATE':
                newOrder.order_exp_date = date2_ttDate(datetime.datetime(year=time.localtime()[0], month=time.localtime()[1], day=time.localtime()[2]))
                newOrder2 = TTAPIOrder()
                newOrder2.setFields(**orderParams)
                newOrder2.order_exp_date = date2_ttDate(datetime.datetime(year=time.localtime()[0], month=time.localtime()[1], day=time.localtime()[2]+1))
                orderSession.send(newOrder2)
            # if tiffy == 'IOC':
            #     newOrder.order_restrict = aenums.TT_IOC_ORDER_RES
            #     # newOrder.tiffy = 'GTD'
            # if tiffy == 'FOK':
            #     newOrder.order_restrict = aenums.TT_FOK_ORDER_RES
            #     # newOrder.tiffy = 'GTD'
            orderSession.send(newOrder)


exit()



    # break

