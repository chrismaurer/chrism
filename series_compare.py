# tick_test.py

import time
from pyrate.manager import Manager
from ttapi import aenums, cppclient
ps1 = Manager.getPriceSessions()[0]
ps2 = Manager.getPriceSessions()[1]

elements = ('seriesKey', 'longSeriesName')
output_file = open("c:\\tt\\" + ps1.exchangeName + "_contract_report.txt", "w")
products = ['CGAS', 'CKER', 'CRUD', 'GASO', 'GDCD', 'GOLD', 'GSOL', 'KERO', 'M-GD', 'M-PT', 'PALL', 'PLAT', 'RSS3', 'SILV', 'TGAB', 'TGCN', 'TGSB']

for prod in products:
    pp1 = ps1.getProducts(prodName=prod, prodType=aenums.TT_PROD_FUTURE)
    pp2 = ps2.getProducts(prodName=prod, prodType=aenums.TT_PROD_FUTURE)
    all_contracts_ticking1 = {}
    all_contracts_ticking2 = {}
    for p1 in pp1:
        cc1 = ps1.getContracts(p1)
        c1 = cc1[2]
        contract_ticking1 = []
        contract_key = []
        # contract_ticking1.append('' + str(cppclient.CTTPriceConsumer.GetDescription(p1)))
        for elem in elements:
            contract_ticking1.append(elem + ': ' + str(getattr(c1, elem)))
        # contract_ticking1.append('pointValue: ' + str(cppclient.CTTPriceConsumer.GetPointValue(p1)))
        contract_key = []
        contract_key.append(str(p1.prod_chr))
        contract_key.append(str(p1.prod_type).lstrip('TT_PROD_'))
        contract_key.append(c1.seriesKey.split('_')[-1])
        if 'TT_NO_CALL_PUT_CODE' not in str(c1.callput):
            contract_key.append(str(c1.callput))
        if c1.strike > 0:
            contract_key.append(str(c1.strike))
        all_contracts_ticking1['_'.join(contract_key)] = contract_ticking1
    for p2 in pp2:
        cc2 = ps2.getContracts(p2)
        c2 = cc2[2]
        contract_ticking2 = []
        # contract_ticking1.append('' + str(cppclient.CTTPriceConsumer.GetDescription(p1)))
        for elem in elements:
            contract_ticking2.append(elem + ': ' + str(getattr(c2, elem)))
        # contract_ticking2.append('pointValue: ' + str(cppclient.CTTPriceConsumer.GetPointValue(p2)))
        contract_key = []
        contract_key.append(p2.prod_chr)
        contract_key.append(str(p2.prod_type).lstrip('TT_PROD_'))
        if 'FSPREAD' in str(p2.prod_type):
            contract_key.append('-'.join([''.join(list(c2.longSeriesName.split('_')[-1].split('/')[0])[0:4]), ''.join(list(c2.longSeriesName.split('_')[-1].split('/')[1])[0:4])]))
        else:
            contract_key.append(''.join(list(c2.seriesName.split('_')[-1])[0:4]))
        if 'TT_NO_CALL_PUT_CODE' not in str(c2.callput):
            contract_key.append(str(c2.callput))
        if c2.strike > 0:
            contract_key.append(str(c2.strike))
        all_contracts_ticking2['_'.join(contract_key)] = contract_ticking2
    for k in all_contracts_ticking1.keys():
        if all_contracts_ticking2.has_key(k):
            if not all_contracts_ticking1[k] == all_contracts_ticking2[k]:
                output_file.write("\n\n")
                output_file.write(k + ", " + str(cppclient.CTTPriceConsumer.GetDescription(p1)) + ", " + p1.prod_chr + ", " + p2.prod_chr + ", " + str(str(all_contracts_ticking1[k]).replace("[", "")).replace("]", "") + ", " + str(str(all_contracts_ticking2[k]).replace("[", "")).replace("]", "") + "\n")

output_file.close()
time.sleep(4)