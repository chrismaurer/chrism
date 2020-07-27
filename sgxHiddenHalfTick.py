import time
import pyscreenshot
from pyrate.ttapi.manager import Manager
from pyrate.ttapi.order import TTAPIOrder
from ttapi import aenums, cppclient
priceSession = Manager().getPriceSession()
orderSession = Manager().getOrderFillSession()
allCustDefaults = Manager().getCustomers()
ordSrv = Manager().getOrderServer()
priceSrv = Manager().getPriceServer()
products = priceSession.getProducts(prodName='NK', prodType=aenums.TT_PROD_FUTURE)
product = products[0]
contracts = priceSession.getContracts(product)#, contractKeys="FUT_NK225M_1704")
contract = contracts[9]
custDefaults = allCustDefaults[-1]
pricey = 50250
order_attempt_count = 1
while True:
    if order_attempt_count > 3:
        break
    time.sleep(5)
    try:
        for enum, price in priceSession.getPrices(contract).items():
            if "SRS_STATUS" in str(enum):
                curr_trading_status = price.value
    except:
        pass
    if curr_trading_status == 8:
        for side in [aenums.TT_SELL, aenums.TT_BUY]:
            ordqty = 50 if "SELL" in str(side) else 100
            orderParams = dict(order_qty=ordqty, buy_sell=side, order_action=aenums.TT_ORDER_ACTION_ADD, limit_prc=pricey, order_type=aenums.TT_LIMIT_ORDER, tif="GTC", srs=contract, exchange_clearing_account=custDefaults.exchange_clearing_account, free_text=custDefaults.free_text, acct_type=cppclient.AEnum_Account.TT_ACCT_AGENT_1)
            newOrder = TTAPIOrder()
            newOrder.setFields(**orderParams)
            orderSession.send(newOrder)
        order_attempt_count += 1
        pricey += 50
        pyscreenshot.grab_to_file(r"C:\tt\screenshot_" + str(curr_trading_status) + "_" + "-".join([str(time.localtime()[3]), str(time.localtime()[4]), str(time.localtime()[5])]) + "_halftick.png")

