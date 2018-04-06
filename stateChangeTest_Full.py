import time
import pyscreenshot
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
products = priceSession.getProducts(prodName='MOTHE', prodType=aenums.TT_PROD_FUTURE)
product = products[0]
contracts = priceSession.getContracts(product)
contract = contracts[3]
custDefaults = allCustDefaults[0]
run_now = True
prev_trading_status = None
curr_trading_status = None
pricey = None
while run_now is True:
    for enum, price in priceSession.getPrices(contract).items():
        if "SETTL" in str(enum):
            pricey = price.value
        elif "LAST_TRD_PRC" in str(enum):
            pricey = price.value
        elif "SRS_STATUS" in str(enum):
            curr_trading_status = price.value
    if curr_trading_status == prev_trading_status:
        pass
    else:
        orderSession.deleteMyOrders()
        if "FUTURE" not in str(product.prod_type) and pricey is None:
            pricey = 150
        if pricey is None:
            pricey = 30000
        else:
            pricey = pricey
        order_qty = 100
        for side in [aenums.TT_BUY, aenums.TT_SELL]:
            orderParams = dict(order_qty=order_qty, buy_sell=side, order_action=aenums.TT_ORDER_ACTION_ADD, limit_prc=pricey, order_type=aenums.TT_LIMIT_ORDER, tif="GTD", srs=contract, exchange_clearing_account=custDefaults.exchange_clearing_account, free_text=custDefaults.free_text, acct_type=cppclient.AEnum_Account.TT_ACCT_AGENT_1)
            newOrder = TTAPIOrder()
            newOrder.setFields(**orderParams)
            myOrder = orderSession.sendAndWait(newOrder)
            if "BUY" in str(side):
                newOrder2 = TTAPIOrder()
                newOrder2.setFields(**orderParams)
                newOrder2.buy_sell = aenums.TT_SELL
                newOrder2.order_qty = 1
                orderSession.sendAndWait(newOrder2)
            time.sleep(3)
            pyscreenshot.grab_to_file(r"C:\tt\screenshot_" + str(curr_trading_status) + "_" + "-".join([str(time.localtime()[3]), str(time.localtime()[4]), str(time.localtime()[5])]) + "_ADD.png")
            pricey = (cppclient.TTTick.PriceIntToInt(pricey, contract, -1))
            order_qty += 5
        time.sleep(3)
        pyscreenshot.grab_to_file(r"C:\tt\screenshot_" + str(curr_trading_status) + "_" + "-".join([str(time.localtime()[3]), str(time.localtime()[4]), str(time.localtime()[5])]) + "_FILLDELETE.png")
        prev_trading_status = curr_trading_status
        time.sleep(15)


