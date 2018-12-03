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



python
f = open(r'/var/log/debesys/OC_ose.log', 'r')
all_uexids = []
dups = []
uexid_missing = []
uexid_missing_idx = []
for line in f.readlines():
    exid, uexid, exectype = None, None, None
    date = " ".join(line.split(" ")[0:1])
    if date == "2018-11-20":
        if " exec_id=" in line and "PENDING" not in line and "OBDL" not in line:
            for elem in line.split(" "):
                if elem.startswith("exec_id"):
                    exid = elem.split("=")[-1].replace("\"", "")
                    exid = exid.replace("\n", "")
                if elem.startswith("unique_exec_id"):
                    uexid = elem.split("=")[-1].replace("\"", "")
                    uexid = uexid.replace("\n", "")
                if elem.startswith("exec_type"):
                    exectype = elem.split("=")[-1].replace("\"", "")
                    exectype = exectype.replace("\n", "")
                if elem.startswith("ord_status"):
                    ordstatus = elem.split("=")[-1].replace("\"", "")
                    ordstatus = ordstatus.replace("\n", "")
            if " exec_id=" in line and " unique_exec_id=" not in line:
                print line
                uexid_missing.append(" + ".join([exectype, ordstatus]))
                if " + ".join([exectype, ordstatus]) not in uexid_missing_idx:
                    uexid_missing_idx.append(" + ".join([exectype, ordstatus]))
            if uexid is not None:
                if uexid in all_uexids:
                    if uexid not in dups:
                        dups.append(uexid)
                else:
                    all_uexids.append(uexid)

print "\n\n\nRESULT\n----\nFound a total of {0} unique_exec_ids\n----\nThe following is a list of possible duplicates, followed by a list of EXEC TYPES that are missing unique_exec_id:".format(str(len(all_uexids)))
for dup in dups:
    print dup

for nouexid_exectype in uexid_missing_idx:
    print nouexid_exectype, ":", uexid_missing.count(nouexid_exectype)

f.close()
exit()
grep -v -e MEMORY -e PENDING -e unique_exec_id /var/log/debesys/OC_ose.log | grep -c "2018-11-20.*ExecutionReport.* exec_id="
grep -v -e MEMORY -e PENDING /var/log/debesys/OC_ose.log | grep -c "2018-11-20.*ExecutionReport.* exec_id="

