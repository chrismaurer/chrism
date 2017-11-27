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
product_list = ["PTCD", "TBGA", "TBGO", "TBKE", "TGAB", "TGCN", "TGSB", "TLGA", "TLGO", "TLKE"]
for product in product_list:
    products = priceSession.getProducts(prodName=product)
    contracts = priceSession.getContracts(products)
    contract = contracts[0]
    pricey = None
    for enum, price in priceSession.getPrices(contract).items():
        if "SETTL" in str(enum):
            pricey = price.value
        elif "LAST_TRD_PRC" in str(enum):
            pricey = price.value
        elif "OPEN_PRC" in str(enum):
            pricey = price.value
    if pricey is None:
        pricey = 300
    for i in range(0, 2):
        side = aenums.TT_BUY
        if i == 1:
            side = aenums.TT_SELL
            pricey = (cppclient.TTTick.PriceIntToInt(pricey, contract, +1))
        orderParams = dict(order_qty=100, buy_sell=side, order_action=aenums.TT_ORDER_ACTION_ADD, limit_prc=pricey, order_type=aenums.TT_LIMIT_ORDER, tif="GTD", srs=contract, exchange_clearing_account=custDefaults.exchange_clearing_account, free_text=custDefaults.free_text, acct_type=cppclient.AEnum_Account.TT_ACCT_AGENT_1)
        newOrder = TTAPIOrder()
        newOrder.setFields(**orderParams)
        orderSession.send(newOrder)

