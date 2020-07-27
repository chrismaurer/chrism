import time
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
create_depth = False
kwantiteh = 1
# prod_list = ["NAU", "NEA", "NEM", "NEXC", "NEXK", "NID", "NMD", "NJP", "NTW"]
# prod_list = ["NIFTY", "JGBL", "JGBM", "JGBLM", "JGBSL", "NK225", "NK225M"]
# prod_list = ["HSI", "CIN", "CTC", "HNP", "GDR", "HSB", "HSI", "HHN", "HHT", "HSN", "HST"]
# prod_list = ['KERO', 'GOLD', 'CGAS', 'CKER', 'M-GD', 'PLAT', 'TEPL', 'KENI', 'KERC', 'KERI']
# prod_list = ["HSW", "HHW", ]
# prod_list = ["WHG", "TIC", "SBO", "ANA", "SHZ"]
# prod_list = ['NTH', 'NPXJ', 'NLATA', 'NSP', 'NNZ', 'NEMEA', 'NJY', 'NHK']
# prod_list = ["NAU", "NCH", "NEAXC", "NEAXK", "NEA", "NEMEA", "NEXC", "NEXK", "NLATA", "NEM", "EM", "NHK", "NMD", "NID", "NJY", "NMY", "NNZ", "NPXJ", "NPC", "NPH", "NSG", "NSP", "NTH", "NVN"]
prod_list = ["JB", "JG", "KJ", "KU", "ND", "RT", "SY", "TF", "UC"]
# prod_list = ["YCDD", "YOCB", "YKEP", "YDBS", "YWIL", "YCAP", "YUOB", "YTBE", "YSTT", "YYZJ", "YGEN", "YARE"]
# prod_list = ["BZN", "BZNF", "PXN", "PXNF", "VC", "VCF"]
# prod_list = ["LUA", "LUZ", "LUC", "LUP", "LUN", "LUS"]
# prod_list = ["XBT/USDT", ]
# prod_list = ["EY", ]
# prod_list = ["MHI", "HSI", "HHN", "HHT", "HSN", "HST", "ALB"]
# prod_list = ["ZARB", "ZADS", "ZAL", "ZAXS", "ZBHA", "ZBHE", "ZBHF", "ZBOB", "ZBPC", "ZCBK", "ZCEN", "ZCIP", "ZCOA", "ZDEW", "ZDLF", "ZHCL", "ZHDB", "ZHDF", "ZHND", "ZHPC", "ZHUV", "ZICI", "ZIDE", "ZIHF", "ZIIB", "ZINF", "ZITC", "ZJST", "ZJUS", "ZKMB", "ZLIC", "ZLPC", "ZLT", "ZMM", "ZMSI", "ZONG", "ZPNB", "ZRCA", "ZRCO", "ZREC", "ZREL", "ZRIL", "ZSBI", "ZSUN", "ZTAT", "ZTCS", "ZTTD", "ZTTM", "ZUNB", "ZYES"]
for instrument in prod_list:
    products = priceSession.getProducts(prodName=instrument)
    for product in products:
        all_contracts = priceSession.getContracts(product)
        contracts = all_contracts[len(all_contracts)-4:]
        for contract in contracts:
            settlement_price = None
            high_price = None
            for enum, price in priceSession.getPrices(contract).items():
                if "SETTL" in str(enum):
                    settlement_price = price.value
                elif "CLOSE" in str(enum):
                    close_price = price.value
                elif "HIGH" in str(enum):
                    high_price = price.value
            pricey = settlement_price
            if settlement_price is None:
                pricey = high_price #5000 #order price 0.5000 for NAU Spread
                if pricey is None:
                    pricey = 300000
                if "FUTURE" not in str(product):
                    pricey = 20
            depth_level = 1
            while depth_level <= 1:
                for i in range(0, 2):
                    side = aenums.TT_BUY
                    custDefaults = custDefaults0
                    if i == 1:
                        side = aenums.TT_SELL
                        custDefaults = custDefaults1
                        if create_depth:
                            pricey = (cppclient.TTTick.PriceIntToInt(pricey, contract, +1))
                    # orderParams = dict(order_qty=kwantiteh, buy_sell=side, order_action=aenums.TT_ORDER_ACTION_ADD, limit_prc=pricey, order_type=aenums.TT_LIMIT_ORDER, tif="GTD", srs=contract, exchange_clearing_account="TM302", clearing_mbr=custDefaults.exchange_sub_account, exchange_sub_account=custDefaults.exchange_sub_account, free_text=custDefaults.free_text, acct_type=cppclient.AEnum_Account.TT_ACCT_AGENT_1)
                    orderParams = dict(order_qty=kwantiteh, buy_sell=side, order_action=aenums.TT_ORDER_ACTION_ADD, limit_prc=pricey, order_type=aenums.TT_LIMIT_ORDER, tif="GTD", srs=contract, exchange_clearing_account="TM061", clearing_mbr=custDefaults.exchange_sub_account, exchange_sub_account=custDefaults.exchange_sub_account, free_text=custDefaults.free_text, acct_type=cppclient.AEnum_Account.TT_ACCT_AGENT_1)
                    newOrder = TTAPIOrder()
                    newOrder.setFields(**orderParams)
                    if i == 0:
                        orderSession0.send(newOrder)
                    else:
                        orderSession0.send(newOrder)
                    # enable this to create an extra sell side order
                    # if i == 1:
                    #     newOrder2 = TTAPIOrder()
                    #     newOrder2.setFields(**orderParams)
                    #     newOrder2.order_qty = kwantiteh
                    #     orderSession0.send(newOrder2)
                    depth_level += 1
                    # if create_depth:
                    #     pricey = (cppclient.TTTick.PriceIntToInt(pricey, contract, +1))
                # print "pricey =", pricey
                # time.sleep(300)
                # break
            break

