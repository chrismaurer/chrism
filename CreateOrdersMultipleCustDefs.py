import time
from pyrate.ttapi.manager import Manager
from pyrate.ttapi.order import TTAPIOrder
from ttapi import aenums, cppclient
priceSession = Manager().getPriceSession()
orderSession0 = Manager().getOrderFillSessions()[-1]
orderSession1 = Manager().getOrderFillSessions()[-1]
custDefaults0 = Manager().getCustomers()
custDefaults1 = Manager().getCustomers()[0]
ordSrv = Manager().getOrderServer()
priceSrv = Manager().getPriceServer()
create_depth = False1
products = priceSession.getProducts(prodName="JGBM", prodType=aenums.TT_PROD_FUTURE)
product = products[0]
contracts = priceSession.getContracts(product)
contract = contracts[1]
pricey = None
settlement_price = None
acct_types = []
for aenum in dir(aenums):
    if "ACCT" in aenum:
        if "GIVEUP_3" not in aenum and "REQUEST" not in aenum:
            if not any(acct in aenum for acct in ["_4", "_5", "_6", "_7", "_8", "_9", "GIVEUP_3", "REQUEST", "MARKETMAKER", "UNALLOCATED", "CLEARING", "CUSTOMER", "MEMBER", "OTHER", "NONE"]):
                acct_types.append(aenum)

giveup_field_vals = ["GU", ""]
fft2_field_vals = ["FFT2", ""]
fft3_field_vals = ["FFT3", ""]

for enum, price in priceSession.getPrices(contract).items():
    if "SETTL" in str(enum):
        settlement_price = price.value

if settlement_price is None:
    if "FUTURE" in str(product):
        settlement_price = 30000
    else:
        settlement_price = 0

pricey = settlement_price

custDefaults = custDefaults0[0]

kwantiteh = 1
for acct_type in acct_types:
    for giveup_field_val in giveup_field_vals:
        for fft2_field_val in fft2_field_vals:
            for fft3_field_val in fft3_field_vals:
                side = aenums.TT_BUY
                kwantiteh += 1
                orderParams = dict(order_qty=kwantiteh, buy_sell=aenums.TT_BUY, order_action=aenums.TT_ORDER_ACTION_ADD, limit_prc=pricey, order_type=aenums.TT_LIMIT_ORDER, tif="GTD", srs=contract, exchange_clearing_account=custDefaults.exchange_clearing_account, clearing_mbr=giveup_field_val, exchange_sub_account=fft2_field_val, free_text=fft3_field_val, acct_type=getattr(aenums, acct_type))
                newOrder = TTAPIOrder()
                newOrder.setFields(**orderParams)
                time.sleep(0.5)
                orderSession0.send(newOrder)


    #             break
    #         break
    #     break
    # break

