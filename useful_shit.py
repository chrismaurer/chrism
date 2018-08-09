for moo in ["ADD", "DELETE", "UPDATE", "FILL", "FFILL", "REJECT", "TCR", "TCR_ACK", "PENDING", "RESTATED", "CHGREJECT"]:
        pass


import time
import pyscreenshot

while True:
    while time.localtime()[3] in range(5, 8) or time.localtime()[3] in range(16, 17):
        pyscreenshot.grab_to_file(r"C:\tt\screenshot_" + "-".join([str(time.localtime()[3]), str(time.localtime()[4]), str(time.localtime()[5])]) + ".png")
        time.sleep(300)





import time
import pyscreenshot
from pyrate.ttapi.manager import Manager
priceSession = Manager().getPriceSession()
priceSrv = Manager().getPriceServer()

while True:
    if time.localtime()[3] == 7 and time.localtime()[4] in range(0, 5):
        pyscreenshot.grab_to_file(r"C:\tt\screenshot_start_subscribe_" + "-".join([str(time.localtime()[3]), str(time.localtime()[4]), str(time.localtime()[5])]) + ".png")
        products = priceSession.getProducts()
        for product in products:
            contracts = priceSession.getContracts(product)
            for contract in contracts:
                print contract
                pricedata = priceSession.getPrices(contract)
        pyscreenshot.grab_to_file(r"C:\tt\screenshot_end_subscribe_" + "-".join([str(time.localtime()[3]), str(time.localtime()[4]), str(time.localtime()[5])]) + ".png")
    time.sleep(360)




