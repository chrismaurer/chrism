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
max_detailed_depth = 3
prev_trading_status = None
curr_trading_status = None
pricey = 70000
products = priceSession.getProducts(prodName='MY', prodType=aenums.TT_PROD_FUTURE)
product = products[0]
contracts = priceSession.getContracts(product, contractKeys=["MYX18", "MYH19"])
while True:
    while curr_trading_status == prev_trading_status:
        for contract in contracts:
            try:
                for enum, price in priceSession.getPrices(contract).items():
                    if "SRS_STATUS" in str(enum):
                        curr_trading_status = price.value
            except:
                pass
        time.sleep(15)
    orderSession.deleteMyOrders()
    for contract in contracts:
        try:
            for enum, price in priceSession.getPrices(contract).items():
                if "SETTL" in str(enum):
                    pricey = price.value
                elif "SRS_STATUS" in str(enum):
                    curr_trading_status = price.value
        except:
            pass
        if pricey is None:
            pricey = 70000
        else:
            if pricey is not None:
                dd = 1
                while dd <= max_detailed_depth:
                    for side in [aenums.TT_SELL, aenums.TT_BUY]:
                        depth_level = 1
                        order_prc = pricey
                        while depth_level <= 7:
                            if depth_level > 1:
                                if "SELL" in str(side):
                                    order_prc = (cppclient.TTTick.PriceIntToInt(order_prc, contract, +1))
                                else:
                                    order_prc = (cppclient.TTTick.PriceIntToInt(order_prc, contract, -1))
                            if depth_level == 7:
                                orderParams = dict(order_qty=80, buy_sell=side, order_action=aenums.TT_ORDER_ACTION_ADD, order_type=aenums.TT_MARKET_ORDER, tif="GTD", srs=contract, exchange_clearing_account=custDefaults.exchange_clearing_account, free_text=custDefaults.free_text, acct_type=cppclient.AEnum_Account.TT_ACCT_AGENT_1)
                            else:
                                orderParams = dict(order_qty=40, buy_sell=side, order_action=aenums.TT_ORDER_ACTION_ADD, limit_prc=order_prc, order_type=aenums.TT_LIMIT_ORDER, tif="GTD", srs=contract, exchange_clearing_account=custDefaults.exchange_clearing_account, free_text=custDefaults.free_text, acct_type=cppclient.AEnum_Account.TT_ACCT_AGENT_1)
                            newOrder = TTAPIOrder()
                            newOrder.setFields(**orderParams)
                            orderSession.send(newOrder)
                            depth_level += 1
                    dd += 1
                buy_cross_order_prc = (cppclient.TTTick.PriceIntToInt(pricey, contract, +3))
                sell_cross_order_prc = (cppclient.TTTick.PriceIntToInt(pricey, contract, -3))
                for side in [aenums.TT_SELL, aenums.TT_BUY]:
                    order_prc = sell_cross_order_prc if "SELL" in str(side) else buy_cross_order_prc
                    orderParams = dict(order_qty=40, buy_sell=side, order_action=aenums.TT_ORDER_ACTION_ADD, limit_prc=order_prc, order_type=aenums.TT_LIMIT_ORDER, tif="GTD", srs=contract, exchange_clearing_account=custDefaults.exchange_clearing_account, free_text=custDefaults.free_text, acct_type=cppclient.AEnum_Account.TT_ACCT_AGENT_1)
                    crossOrder = TTAPIOrder()
                    crossOrder.setFields(**orderParams)
                    orderSession.send(crossOrder)
    time.sleep(2)
    pyscreenshot.grab_to_file(r"C:\tt\screenshot_" + str(curr_trading_status) + "_" + "-".join([str(time.localtime()[3]), str(time.localtime()[4]), str(time.localtime()[5])]) + "_ADD.png")
    time.sleep(2)
    pyscreenshot.grab_to_file(r"C:\tt\screenshot_" + str(curr_trading_status) + "_" + "-".join([str(time.localtime()[3]), str(time.localtime()[4]), str(time.localtime()[5])]) + "_ADDED.png")
    time.sleep(45)
    try:
        for enum, price in priceSession.getPrices(contract).items():
            if "SRS_STATUS" in str(enum):
                prev_trading_status = price.value
    except:
        pass

