from random import randint
from pyrate.ttapi.manager import Manager
from pyrate.ttapi.order import TTAPIOrder
from ttapi import aenums, cppclient
priceSession = Manager().getPriceSession()
orderSession = Manager().getOrderFillSession()
allCustDefaults = Manager().getCustomers()
custDefaults = allCustDefaults[0]
ordSrv = Manager().getOrderServer()
priceSrv = Manager().getPriceServer()
product_list = ["EY", ]
# product_list = ["CH", "EY", "FB", "GD", "ID", "IN", "INB", "ING", "INI", "IU", "JG", "MD", "MY", "ND", "NS", "NU", "PH", "SGP", "ST", "TH", "TU", "TW", "UJ", "UY"]
for product in product_list:
    products = priceSession.getProducts(prodName=product)
    contracts = priceSession.getContracts(products)
    contract = contracts[1]#(randint(0, len(contracts)-1))]
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
    depth_level = 1
    while depth_level <= 150:
        orderParams = dict(order_qty=3, buy_sell=aenums.TT_SELL, order_action=aenums.TT_ORDER_ACTION_ADD, limit_prc=pricey, order_type=aenums.TT_LIMIT_ORDER, tif="GTD", srs=contract, exchange_clearing_account=custDefaults.exchange_clearing_account, free_text=custDefaults.free_text, acct_type=cppclient.AEnum_Account.TT_ACCT_AGENT_1)
        newOrder = TTAPIOrder()
        newOrder.setFields(**orderParams)
        orderSession.send(newOrder)
        depth_level += 1

