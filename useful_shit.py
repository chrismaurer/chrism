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




q = open(r'/var/log/debesys/OC_sgx.log', 'r')
all_uexids = []
dups = []
for line in q.readlines():
    if "ExecutionReport" in line and "exec_id" in line:
        for elem in line.split(" "):
            date = " ".join(line.split(" ")[0:2])
            if elem.startswith("exec_id"):
                exid = elem.split("=")[-1].replace("\"", "")
                exid = exid.replace("\n", "")
            if elem.startswith("unique_exec_id"):
                uexid = elem.split("=")[-1].replace("\"", "")
                uexid = uexid.replace("\n", "")
        print " ".join([date, exid, uexid])
        if uexid not in all_uexids:
            all_uexids.append(uexid)
        else:
            if uexid in all_uexids and uexid not in dups:
                dups.append(uexid)
q.close()
