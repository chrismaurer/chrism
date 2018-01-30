#~TestCaseName: TestCreatePositions
#~Exchange/Simulator/Both: Both
#~Pyrate Version: 2.0

import time
from pyrate.builder import Builder
from pyrate.ttapi.predicates import CallbackType
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
products = priceSession.getProducts(prodName='ZARB')
product = products[0]
contracts = priceSession.getContracts(product)
contract = contracts[0]
custDefaults = allCustDefaults[0]
run_now = True
prev_trading_status = None
curr_trading_status = None
while run_now is True:
    time.sleep(20)
    for enum, price in priceSession.getPrices(contract).items():
        if "SETTL" in str(enum):
            settlement_price = price.value
        if "SRS_STATUS" in str(enum):
            curr_trading_status = price.value
    if curr_trading_status == prev_trading_status or curr_trading_status is None:
        pass
    else:
        if "FUTURE" not in str(product.prod_type):
            pricey = 10000
        else:
            pricey = settlement_price
            CallbackType('OnOrderStatus')
cbks = CallbackType('OnOrderStatus')
orderParams = dict(order_qty=100, buy_sell=aenums.TT_BUY, order_action=aenums.TT_ORDER_ACTION_ADD, limit_prc=pricey, order_type=aenums.TT_LIMIT_ORDER, tif="GTD", srs=contract, exchange_clearing_account=custDefaults.exchange_clearing_account, free_text=custDefaults.free_text, acct_type=cppclient.AEnum_Account.TT_ACCT_AGENT_1)
newOrder = TTAPIOrder()
newOrder.setFields(**orderParams)
myOrder = orderSession.sendAndWait(newOrder, cbks)
sok = myOrder[0]['order'].site_order_key

working_orders = orderSession.allOpenOrders()
for working_order in working_orders:
    if working_order.site_order_key == sok:
        break
