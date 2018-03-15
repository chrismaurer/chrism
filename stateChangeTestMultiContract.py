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
products = priceSession.getProducts(prodName='NK225', prodType=aenums.TT_PROD_FUTURE)
run_now = True
while run_now is True:
    prod = products[0]
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
        orderSession.deleteMyOrders()
        for product in products:
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
                        for side in [aenums.TT_BUY, aenums.TT_SELL, aenums.TT_SELL]:
                            ordqty = 60 if "SELL" in str(side) else 100
                            orderParams = dict(order_qty=ordqty, buy_sell=side, order_action=aenums.TT_ORDER_ACTION_ADD, limit_prc=pricey, order_type=aenums.TT_LIMIT_ORDER, tif="GTD", srs=contract, exchange_clearing_account=custDefaults.exchange_clearing_account, free_text=custDefaults.free_text, acct_type=cppclient.AEnum_Account.TT_ACCT_AGENT_1)
                            if "SELL" in str(side):
                                pricey = (cppclient.TTTick.PriceIntToInt(pricey, contract, -1))
                                orderParams = dict(order_qty=ordqty, buy_sell=side, order_action=aenums.TT_ORDER_ACTION_ADD, limit_prc=pricey, order_type=aenums.TT_LIMIT_ORDER, tif="GTD", srs=contract, exchange_clearing_account=custDefaults.exchange_clearing_account, free_text=custDefaults.free_text, acct_type=cppclient.AEnum_Account.TT_ACCT_AGENT_1)
                            else:
                                orderParams = dict(order_qty=ordqty, buy_sell=side, order_action=aenums.TT_ORDER_ACTION_ADD, limit_prc=pricey, order_type=aenums.TT_LIMIT_ORDER, tif="GTD", srs=contract, exchange_clearing_account=custDefaults.exchange_clearing_account, free_text=custDefaults.free_text, acct_type=cppclient.AEnum_Account.TT_ACCT_AGENT_1)
                            newOrder = TTAPIOrder()
                            newOrder.setFields(**orderParams)
                            orderSession.send(newOrder)
                            for enum, price in priceSession.getPrices(contr).items():
                                if "SRS_STATUS" in str(enum):
                                    if price.value != 2:
                                        depth_level = 1
                                        while depth_level <= 3:
                                            for side in [aenums.TT_SELL, aenums.TT_BUY]:
                                                if "SELL" in str(side):
                                                    pricey = (cppclient.TTTick.PriceIntToInt(pricey, contract, -1))
                                                else:
                                                    pricey = (cppclient.TTTick.PriceIntToInt(pricey, contract, +1))
                                                orderParams = dict(order_qty=40, buy_sell=side, order_action=aenums.TT_ORDER_ACTION_ADD, limit_prc=pricey, order_type=aenums.TT_LIMIT_ORDER, tif="GTD", srs=contract, exchange_clearing_account=custDefaults.exchange_clearing_account, free_text=custDefaults.free_text, acct_type=cppclient.AEnum_Account.TT_ACCT_AGENT_1)
                                                newOrder = TTAPIOrder()
                                                newOrder.setFields(**orderParams)
                                                orderSession.send(newOrder)
                                                depth_level += 1
                    pyscreenshot.grab_to_file(r"C:\tt\screenshot_" + str(curr_trading_status) + "_" + "-".join([str(time.localtime()[3]), str(time.localtime()[4]), str(time.localtime()[5])]) + "_ADD.png")
                    #orderSession.deleteMyOrders()
                    # time.sleep(1)
                    # pyscreenshot.grab_to_file(r"C:\tt\screenshot_" + str(curr_trading_status) + "_" + "-".join([str(time.localtime()[3]), str(time.localtime()[4]), str(time.localtime()[5])]) + "_DELETE.png")
            prev_trading_status = curr_trading_status


