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
product_list = ["MCH", ]
products = priceSession.getProducts(prodName=product_list[0], prodType=aenums.TT_PROD_FUTURE)
product = products[0]
contracts = priceSession.getContracts(products, contractKeys=["397224", ])
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

orderParams = dict(order_qty=1, buy_sell=aenums.TT_BUY, order_action=aenums.TT_ORDER_ACTION_ADD, limit_prc=pricey, order_type=aenums.TT_LIMIT_ORDER, tif="GTD", srs=contract, exchange_clearing_account=custDefaults.exchange_clearing_account, free_text=custDefaults.free_text, acct_type=cppclient.AEnum_Account.TT_ACCT_AGENT_1)

newOrderA1 = TTAPIOrder()

newOrderA2 = TTAPIOrder()

newOrderB1 = TTAPIOrder()

newOrderB2 = TTAPIOrder()

newOrderC1 = TTAPIOrder()

newOrderD1 = TTAPIOrder()

newOrderA1.setFields(**orderParams)

newOrderA2.setFields(**orderParams)

newOrderA1.limit_prc = 20000

newOrderA2.limit_prc = 20000

newOrderA2.buy_sell = aenums.TT_SELL

newOrderB1.setFields(**orderParams)

newOrderB2.setFields(**orderParams)

newOrderB1.limit_prc = 20500

newOrderB2.limit_prc = 20500

newOrderB2.buy_sell = aenums.TT_SELL

newOrderC1.setFields(**orderParams)

newOrderC1.limit_prc = 21001

newOrderD1.setFields(**orderParams)

newOrderD1.limit_prc = 21001

newOrderD1.buy_sell = aenums.TT_SELL

orderSession.send(newOrderA1)

orderSession.send(newOrderA2)

time.sleep(180)

orderSession.send(newOrderB1)

orderSession.send(newOrderB2)

time.sleep(120)

orderSession.send(newOrderC1)

time.sleep(60)

orderSession.send(newOrderD1)

