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
custDefaults = allCustDefaults[0]
ordSrv = Manager().getOrderServer()
priceSrv = Manager().getPriceServer()
# product_list = ["CH", "EY", "FB", "GD", "ID", "IN", "INB", "ING", "INI", "IU", "JG", "MD", "MY", "ND", "NS", "NU", "PH", "SGP", "ST", "TH", "TU", "TW", "UJ", "UY"]
# for product in product_list:
products = priceSession.getProducts(prodType=aenums.TT_PROD_FSPREAD)#prodName=product)
for product in products:
    contracts = priceSession.getContracts(product)
    contract = contracts[-2]
    pricey = None
    for enum, price in priceSession.getPrices(contract).items():
        if "SETTL" in str(enum):
            pricey = price.value
        elif "LAST_TRD_PRC" in str(enum):
            pricey = price.value
        elif "OPEN_PRC" in str(enum):
            pricey = price.value
    if pricey is None:
        pricey = 30000
    depth_level = 1
    while depth_level <= 1:
        orderParams = dict(order_qty=100, buy_sell=aenums.TT_BUY, order_action=aenums.TT_ORDER_ACTION_ADD, limit_prc=pricey, order_type=aenums.TT_LIMIT_ORDER, tif="GTC", srs=contract, exchange_clearing_account=custDefaults.exchange_clearing_account, free_text=custDefaults.free_text, acct_type=cppclient.AEnum_Account.TT_ACCT_AGENT_1)
        newOrder = TTAPIOrder()
        newOrder.setFields(**orderParams)
        orderSession.send(newOrder)
        depth_level += 1
    time.sleep(3)

