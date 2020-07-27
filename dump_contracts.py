# callbacks = os.sendAndWait(myOrder, filters='OnOrderTableAdd')
# orderCallback = callbacks['OnOrderTableAdd'][0]['order']

# os = Manager.getOrderSession()
#         orderParams = dict(order_action=aenums.TT_ORDER_ACTION_ADD,srs=c,order_qty=25,tif='GTC',buy_sell=aenums.TT_BUY,order_type=aenums.TT_LIMIT_ORDER,limit_prc=10000,acct_type=cppclient.AEnum_Account.TT_ACCT_AGENT_1,user_name='CHRIS',exchange_clearing_account='DIRECT')
#         myOrder = TTAPIOrder()
#         myOrder.setFields(**orderParams)
#



# import os, shutil, subprocess
# from ttapi import aenums, cppclient
# from pyrate.ttapi.order import TTAPIOrder
from pyrate.manager import Manager
ps = Manager.getPriceSession()
pp = ps.getProducts()

elements = dir(ps.getContracts(pp[0])[0])[-26:]
elements.remove("energy_qty")
elements.remove("get_differences")
elements.remove("round_lot_qty")
elements.remove("legs")

dump_contracts_output = file(r"c:\dump_contracts" + ps.exchangeName + ".csv", 'w')

dump_contracts_output.write(','.join(elements))
for p in pp:
    dump_contracts_output.write('#'*5 + p.prod_chr + '#'*5 + "\n")
    cc = ps.getContracts(p)
    for c in cc:
        contract_elems = []
        for elem in elements:
            contract_elems.append(getattr(c, elem))
        dump_contracts_output.write(str(contract_elems))
        dump_contracts_output.write("\n")

dump_contracts_output.close()



input_file = open("c:\\thrshPrices.txt", "r")
for line in input_file.readlines():
    search_string = line.split(",")[-1]
    search_string = search_string.rstrip("].\n")
    search_string = search_string.lstrip(" obid:")
    contract_dump = open("c:\\dump_contractsOSE.txt", "r")
    for contract in contract_dump.readlines():
        if search_string in contract:
            print search_string, "=", contract.split(",")[9]
    contract_dump.close()
input_file.close()


import time
from pyrate.manager import Manager
ps = Manager.getPriceSession()
pp = ps.getProducts()

dateElem = list(time.localtime(time.time()))
dateDay = str(dateElem[2]).zfill(02)
dateMnth = str(dateElem[1]).zfill(02)
dateYear = str(dateElem[0])
dateList = [dateYear, dateMnth, dateDay]
dateStamp = '-'.join(dateList)

contract_dict = {}
for p in pp:
    cc = ps.getContracts(p)
    for c in cc:
        contract_dict[c.seriesKey] = c.longSeriesName

input_file = open("c:\\thrshPrices.txt", "r")
output_file = open("c:\\tt\\logfiles\\" + ps.exchangeName + "_SIM_OMPriceBridge_" + dateStamp + "_converted.log", "w")
for input_line in input_file.readlines():
    search_string = input_line.split(":")[-1]
    search_string = search_string.rstrip("].\n")
    output_file.write(str(input_line.split(",")[0:-2]) + " " + contract_dict[str(search_string)])
time.sleep(4)
output_file.close()
