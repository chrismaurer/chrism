from pyrate.ttapi.manager import Manager
from pyrate.ttapi.order import TTAPIOrder
from ttapi import aenums, cppclient
priceSession = Manager().getPriceSession()
orderSession0 = Manager().getOrderFillSessions()[0]
orderSession1 = Manager().getOrderFillSessions()[-1]
custDefaults0 = Manager().getCustomers()[0]
custDefaults1 = Manager().getCustomers()[0]
ordSrv = Manager().getOrderServer()
priceSrv = Manager().getPriceServer()
create_depth = True
prod_list = ["ZARB", "ZADS", "ZAL", "ZAXS", "ZBHA", "ZBHE", "ZBHF", "ZBOB", "ZBPC", "ZCBK", "ZCEN", "ZCIP", "ZCOA", "ZDEW", "ZDLF", "ZHCL", "ZHDB", "ZHDF", "ZHND", "ZHPC", "ZHUV", "ZICI", "ZIDE", "ZIHF", "ZIIB", "ZINF", "ZITC", "ZJST", "ZJUS", "ZKMB", "ZLIC", "ZLPC", "ZLT", "ZMM", "ZMSI", "ZONG", "ZPNB", "ZRCA", "ZRCO", "ZREC", "ZREL", "ZRIL", "ZSBI", "ZSUN", "ZTAT", "ZTCS", "ZTTD", "ZTTM", "ZUNB", "ZYES"]
prod_type_list = ["FUTURE", ]#"FSPREAD"]  # , "OPTIONS", "OSTRATEGY"]
for instrument in prod_list:
    products = priceSession.getProducts(prodName=instrument)
    for product in products:
        print product
        if any(prod_type in str(product.prod_type) for prod_type in prod_type_list):
            contracts = priceSession.getContracts(product)
            for contract in contracts:
                print contract
                if len(contract.seriesKey) < 35:
                    pricey = None
                    settlement_price = None
                    for enum, price in priceSession.getPrices(contract).items():
                        if "SETTL" in str(enum):
                            settlement_price = price.value
                    if settlement_price is None:
                        if "FUTURE" in str(product):
                            settlement_price = 30000
                        else:
                            settlement_price = 0
                    pricey = settlement_price
                    depth_level = 1
                    while depth_level <= 1:
                        for i in range(0, 2):
                            side = aenums.TT_BUY
                            custDefaults = custDefaults0
                            kwantiteh = 800
                            if i == 1:
                                side = aenums.TT_SELL
                                custDefaults = custDefaults1
                                kwantiteh = 1
                                pricey = (cppclient.TTTick.PriceIntToInt(pricey, contract, +1))
                            orderParams = dict(order_qty=kwantiteh, buy_sell=side, order_action=aenums.TT_ORDER_ACTION_ADD, limit_prc=pricey, order_type=aenums.TT_LIMIT_ORDER, tif="GTC", srs=contract, exchange_clearing_account=custDefaults.exchange_clearing_account, clearing_mbr=custDefaults.exchange_sub_account, exchange_sub_account=custDefaults.exchange_sub_account, free_text=custDefaults.free_text, acct_type=cppclient.AEnum_Account.TT_ACCT_AGENT_1)
                            newOrder = TTAPIOrder()
                            newOrder.setFields(**orderParams)
                            if i == 0:
                                orderSession0.send(newOrder)
                            else:
                                orderSession0.send(newOrder)
                            depth_level += 1
                        if create_depth:
                            pricey = (cppclient.TTTick.PriceIntToInt(pricey, contract, +1))
                    break
                break

