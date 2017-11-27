import time
import pyscreenshot
from pyrate.ttapi.manager import Manager
priceSession = Manager().getPriceSession()
allCustDefaults = Manager().getCustomers()
ordSrv = Manager().getOrderServer()
priceSrv = Manager().getPriceServer()
products = priceSession.getProducts(prodName='GASO')
product = products[0]
contracts = priceSession.getContracts(product)
contract = contracts[0]
run_now = True
prev_trading_status = None
curr_trading_status = None
pricey = None
screenshot_counter = 100
print "Contract:", contract
while run_now is True:
    time.sleep(5)
    try:
        for enum, price in priceSession.getPrices(contract).items():
            if "SRS_STATUS" in str(enum):
                curr_trading_status = price.value
                if prev_trading_status is None:
                    prev_trading_status = price.value
    except:
        pass
    screenshot_counter = 100 if curr_trading_status == prev_trading_status else 1
    while screenshot_counter <= 5:
        print "CHECK:", prev_trading_status, curr_trading_status
        pyscreenshot.grab_to_file(r"C:\tt\screenshot_" + str(curr_trading_status) + "_" + "-".join([str(time.localtime()[3]), str(time.localtime()[4]), str(time.localtime()[5])]) + ".png")
        screenshot_counter += 1
        time.sleep(7)
    prev_trading_status = curr_trading_status

