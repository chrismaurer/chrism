import time
import pyscreenshot
from pyrate.ttapi.manager import Manager
from pyrate.ttapi.order import TTAPIOrder
from ttapi import aenums, cppclient
priceSession = Manager().getPriceSession()
orderSession = Manager().getOrderFillSession()
allCustDefaults = Manager().getCustomers()
custDefaults = allCustDefaults[-1]
ordSrv = Manager().getOrderServer()
priceSrv = Manager().getPriceServer()
prev_trading_status = None
curr_trading_status = None
pricey = None
products = priceSession.getProducts()#prodName='ZCOA')
run_now = True
while run_now is True:
    prods = priceSession.getProducts(prodName='ZONG')
    prod = prods[0]
    contrs = priceSession.getContracts(prod)
    contr = contrs[0]
    try:
        for enum, price in priceSession.getPrices(contr).items():
            if "SRS_STATUS" in str(enum):
                curr_trading_status = price.value
    except:
        pass
    if curr_trading_status == prev_trading_status:
        prev_trading_status = curr_trading_status
        time.sleep(15)
    else:
        for product in products:
            if "ZONG" in str(product):# or "ZHPC" in str(product):
                contracts = priceSession.getContracts(product)#, contractKeys="FUT_NK225M_1704")
                for contract in contracts:
                    try:
                        for enum, price in priceSession.getPrices(contract).items():
                            if "SETTL" in str(enum):
                                pricey = price.value
                            elif "LAST_TRD_PRC" in str(enum):
                                pricey = price.value
                            elif "OPEN_PRC" in str(enum):
                                pricey = price.value
                    except:
                        pass
                    if pricey is None:
                        pricey = 10000
                    else:
                        if pricey is not None:
                            for side in [aenums.TT_BUY, aenums.TT_SELL]:
                                ordqty = 20 if "SELL" in str(side) else 200
                                orderParams = dict(order_qty=ordqty, buy_sell=side, order_action=aenums.TT_ORDER_ACTION_ADD, limit_prc=pricey, order_type=aenums.TT_LIMIT_ORDER, tif="GTC", srs=contract, exchange_clearing_account=custDefaults.exchange_clearing_account, free_text=custDefaults.free_text, acct_type=cppclient.AEnum_Account.TT_ACCT_AGENT_1)
                                if "SELL" in str(side):
                                    orderParams = dict(order_qty=ordqty, buy_sell=side, order_action=aenums.TT_ORDER_ACTION_ADD, order_type=aenums.TT_MARKET_ORDER, tif="GTD", srs=contract, exchange_clearing_account=custDefaults.exchange_clearing_account, free_text=custDefaults.free_text, acct_type=cppclient.AEnum_Account.TT_ACCT_AGENT_1)
                                else:
                                    orderParams = dict(order_qty=ordqty, buy_sell=side, order_action=aenums.TT_ORDER_ACTION_ADD, limit_prc=pricey, order_type=aenums.TT_LIMIT_ORDER, tif="GTC", srs=contract, exchange_clearing_account=custDefaults.exchange_clearing_account, free_text=custDefaults.free_text, acct_type=cppclient.AEnum_Account.TT_ACCT_AGENT_1)
                                newOrder = TTAPIOrder()
                                newOrder.setFields(**orderParams)
                                orderSession.send(newOrder)
                        pyscreenshot.grab_to_file(r"C:\tt\screenshot_" + str(curr_trading_status) + "_" + "-".join([str(time.localtime()[3]), str(time.localtime()[4]), str(time.localtime()[5])]) + "_ADD.png")
                        #orderSession.deleteMyOrders()
                        time.sleep(1)
                        pyscreenshot.grab_to_file(r"C:\tt\screenshot_" + str(curr_trading_status) + "_" + "-".join([str(time.localtime()[3]), str(time.localtime()[4]), str(time.localtime()[5])]) + "_DELETE.png")
                prev_trading_status = curr_trading_status


