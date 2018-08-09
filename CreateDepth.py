import time
from pyrate.builder import Builder
from pyrate.ttapi.manager import Manager
from pyrate.ttapi.order import TTAPIOrder
from ttapi import aenums, cppclient
from captain.controlled import controlled_name_type, ControlledName
from captain.lib.controlled_types import Tif
priceSession = Manager().getPriceSession()
orderSession = Manager().getOrderFillSession()
allCustDefaults = Manager().getCustomers()
ordSrv = Manager().getOrderServer()
priceSrv = Manager().getPriceServer()
list_of_products = ["XPB", ]#"AIR", "CSP", "VNK", "XPB", "SNP", "ACC", "CPI", "COL", "GLX", "GAH", "LNK", "SAN", "MIU"]
for name_of_product in list_of_products:
    products = priceSession.getProducts(prodName=name_of_product)#, prodType=aenums.TT_PROD_FUTURE)
    custDefaults = allCustDefaults[0]
    for product in products:
        pricey = None
        found_price = None
        if "STOCK" not in str(product.prod_type):
            if "FUTURE" not in str(product.prod_type):
                pricey = 3
            contracts = priceSession.getContracts(product)
            for contract in contracts:
                for enum, price in priceSession.getPrices(contract).items():
                    if "SETTL" in str(enum):
                        found_price = price.value
                    elif "LAST_TRD_PRC" in str(enum):
                        found_price = price.value
                    elif "OPEN_PRC" in str(enum):
                        found_price = price.value
                    if "SRS_STATUS" in str(enum):
                        trading_status = price.value
                pricey = 100 if found_price is None and "HKEx" in priceSession.exchangeName else found_price
                if pricey is not None and trading_status != 6:
                    for side in [aenums.TT_SELL, aenums.TT_BUY]:
                        depth_level = 1
                        pricey = 100 if found_price is None and "HKEx" in priceSession.exchangeName else found_price
                        while depth_level <= 1:
                            if "SELL" in str(side):
                                pricey = (cppclient.TTTick.PriceIntToInt(pricey, contract, +1))
                            else:
                                pricey = pricey#(cppclient.TTTick.PriceIntToInt(pricey, contract, -1))
                            orderParams = dict(order_qty=1, buy_sell=side, order_action=aenums.TT_ORDER_ACTION_ADD, limit_prc=pricey, order_type=aenums.TT_LIMIT_ORDER, tif="GTD", srs=contract, exchange_clearing_account=custDefaults.exchange_clearing_account, free_text=custDefaults.free_text, acct_type=cppclient.AEnum_Account.TT_ACCT_AGENT_1)
                            newOrder = TTAPIOrder()
                            newOrder.setFields(**orderParams)
                            orderSession.send(newOrder)
                            depth_level += 1
                break
#        break

