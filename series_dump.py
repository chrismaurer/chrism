# tick_test.py

import time
from pyrate.manager import Manager
from ttapi import aenums, cppclient
ps1 = Manager.getPriceSession()
elements = ('seriesKey', 'seriesName', 'longSeriesName')
output_file = open("c:\\tt\\" + ps1.exchangeName + "_contract_report.csv", "w")
all_contracts_ticking1 = {}
pp1 = ps1.getProducts()
for p1 in pp1:
    cc1 = ps1.getContracts(p1)
    for c1 in cc1:
        contract_ticking1 = []
        contract_key = []
        for elem in elements:
            contract_ticking1.append(elem + ': ' + str(getattr(c1, elem)))
        contract_key = []
        contract_key.append(str(p1.prod_chr))
        contract_key.append(str(p1.prod_type).split('_')[-1])
        if 'TT_NO_CALL_PUT_CODE' not in str(c1.callput):
            contract_key.append(str(c1.callput))
        if c1.strike > 0:
            contract_key.append(str(c1.strike))
        all_contracts_ticking1['_'.join(contract_key)] = contract_ticking1

for k in all_contracts_ticking1.keys():
    output_file.write(k + ", " + str(all_contracts_ticking1[k]) + "\n")

time.sleep(4)
output_file.close()
time.sleep(4)
