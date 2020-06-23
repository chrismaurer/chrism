for moo in ["ADD", "DELETE", "UPDATE", "FILL", "FFILL", "REJECT", "TCR", "TCR_ACK", "PENDING", "RESTATED", "CHGREJECT"]:
       pass


import time
import pyscreenshot

while True:
   while time.localtime()[3] in range(9, 10) or time.localtime()[3] in range(16, 17):
       pyscreenshot.grab_to_file(r"C:\tt\startup_test_" + "-".join([str(time.localtime()[3]), str(time.localtime()[4]), str(time.localtime()[5])]) + ".png")
       time.sleep(30)

import time
import pyscreenshot
scrnshot_count = 1
while True:
    if time.localtime()[3] == 10 and time.localtime()[4] == 29:
        while scrnshot_count <= 6:
            time.sleep(15)
            pyscreenshot.grab_to_file(r"C:\tt\dayend_test_" + str(scrnshot_count) + ".png")
            scrnshot_count += 1
        break
    else:
        time.sleep(20)




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
               pricedata = priceSession.getPrices(contract, timeout=90)
       pyscreenshot.grab_to_file(r"C:\tt\screenshot_end_subscribe_" + "-".join([str(time.localtime()[3]), str(time.localtime()[4]), str(time.localtime()[5])]) + ".png")
   time.sleep(360)


python
f = open(r'/var/log/debesys/OC_ose.log', 'r')
all_client_ips = []
for line in f.readlines():
    exid, uexid, exectype, client_ip = None, None, None, None
    date = " ".join(line.split(" ")[0:1])
    if date == "2020-06-16":
        if "MaurDC-Ko" in line and "SEGMENT" not in line and "Account.name" not in line and "CUSTOMER_DEFAULTS" not in line:
            for elem in line.split(" "):
                if elem.startswith("client_ip"):
                    client_ip = elem.split("=")[-1].replace("\"", "")
                    client_ip = client_ip.replace("\n", "")
            if client_ip is None:
                print "ERROR - client_ip MISSING: {}".format(line)
            else:
                if len(all_client_ips) == 0:
                    all_client_ips.append(client_ip)
                elif client_ip not in all_client_ips:
                    print "ERROR - Mismatched client_ip {}".format(client_ip)
                    all_client_ips.append(client_ip)

if len(all_client_ips) > 1:
    for client_ip in all_client_ips:
        print client_ip

f.close()





python
f = open(r'/var/log/debesys/OC_hkex.log', 'r')
all_uexids = []
all_exids = []
uexid_dups = []
exid_dups = []
uexid_missing = []
exid_missing = []
uexid_missing_idx = []
exid_missing_idx = []
for line in f.readlines():
   exid, uexid, exectype = None, None, None
   date = " ".join(line.split(" ")[0:1])
   if date == "2020-01-22":
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
               uexid_missing.append(" + ".join([exectype, ordstatus]))
               if " + ".join([exectype, ordstatus]) not in uexid_missing_idx:
                   uexid_missing_idx.append(" + ".join([exectype, ordstatus]))
           if " unique_exec_id=" in line and " exec_id=" not in line:
               exid_missing.append(" + ".join([exectype, ordstatus]))
               if " + ".join([exectype, ordstatus]) not in uexid_missing_idx:
                   exid_missing_idx.append(" + ".join([exectype, ordstatus]))
           if uexid is not None:
               if uexid not in all_uexids:
                   all_uexids.append(uexid)
               else:
                   if uexid not in uexid_dups:
                       uexid_dups.append(uexid)
           if exid is not None:
               if exid not in all_exids:
                   all_exids.append(exid)
               else:
                   if exid not in exid_dups:
                       exid_dups.append(exid)

print "\n\n\nRESULT\n----\nFound a total of {0} unique_exec_ids\n----\nThe following is a list of possible duplicates, followed by a list of EXEC TYPES that are missing unique_exec_id:".format(str(len(all_uexids)))
for uexid_dup in uexid_dups:
    if ":" in uexid_dup:
        print uexid_dup
    else:
        if uexid_dups.count(uexid_dup) > 2:
            print uexid_dup

print "-"*50

for exid_dup in exid_dups:
    if ":" in exid_dup:
        print exid_dup
    else:
        if exid_dups.count(exid_dup) > 2:
            print exid_dup

print "-"*50

for nouexid_exectype in uexid_missing_idx:
   print nouexid_exectype, ":", uexid_missing.count(nouexid_exectype)

print "-"*50

for noexid_exectype in exid_missing_idx:
   print noexid_exectype, ":", exid_missing.count(noexid_exectype)

f.close()
exit()
grep -v -e MEMORY -e PENDING -e unique_exec_id /var/log/debesys/OC_hkex.log | grep -c "2020-01-22.*ExecutionReport.* exec_id="
grep -v -e MEMORY -e PENDING -e exec_id /var/log/debesys/OC_hkex.log | grep -c "2020-01-22.*ExecutionReport.* unique_exec_id="
grep -v -e MEMORY -e PENDING /var/log/debesys/OC_hkex.log | grep -c "2020-01-22.*ExecutionReport.* exec_id="
grep -v -e MEMORY -e PENDING /var/log/debesys/OC_hkex.log | grep -c "2020-01-22.*ExecutionReport.* exec_id=0"




import time
from pyrate.ttapi.manager import Manager
from pyrate.ttapi.order import TTAPIOrder
from ttapi import aenums, cppclient
priceSession = Manager().getPriceSession()
orderSession = Manager().getOrderFillSession()
allCustDefaults = Manager().getCustomers()
ordSrv = Manager().getOrderServer()
priceSrv = Manager().getPriceServer()
products = priceSession.getProducts(prodName='NK', prodType=aenums.TT_PROD_FUTURE)
product = products[0]
contracts = priceSession.getContracts(product)#, contractKeys="FUT_NK225M_1704")
contract = contracts[9]
custDefaults = allCustDefaults[-1]
pricey = 50250
order_attempt_count = 1
while True:
   if order_attempt_count > 3:
       break
   time.sleep(5)
   try:
       for enum, price in priceSession.getPrices(contract, timeout=90).items():
           if "SRS_STATUS" in str(enum):
               curr_trading_status = price.value
   except:
       pass
   if curr_trading_status == 8:
       pyscreenshot.grab_to_file(r"C:\tt\screenshot_" + str(curr_trading_status) + "_" + "-".join([str(time.localtime()[3]), str(time.localtime()[4]), str(time.localtime()[5])]) + "_halftick.png")
       time.sleep(5)



import time
import pyscreenshot
import requests
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
pricey = None
while True:
   try:
       products = priceSession.getProducts(prodType=aenums.TT_PROD_FUTURE)
       for product in products:
           contracts = priceSession.getContracts(product)#, contractKeys=["394016", "459552"])
           trading = False
           for contract in contracts:
               curr_trading_status = None
               if trading:
                   break
               else:
                   for enum, price in priceSession.getPrices(contract, timeout=90).items():
                       if "SRS_STATUS" in str(enum):
                           curr_trading_status = price.value
                           if curr_trading_status == 2 or curr_trading_status == 6 or curr_trading_status < 0 or curr_trading_status is None:
                               trading = True
                               break
                           else:
                               settlement_price = None
                               for enum, price in priceSession.getPrices(contract, timeout=90).items():
                                   if "SETTL" in str(enum):
                                       settlement_price = price.value
                               if settlement_price is None:
                                   if "FUTURE" in str(product):
                                       settlement_price = 50000
                                   else:
                                       settlement_price = 0
                               pricey = settlement_price
                               depth_level = 1
                               while depth_level <= 1:
                                   for i in range(0, 2):
                                       side = aenums.TT_BUY
                                       custDefaults = custDefaults0
                                       kwantiteh = 1
                                       if i == 1:
                                           side = aenums.TT_SELL
                                           custDefaults = custDefaults1
                                           kwantiteh = 1
                                           if create_depth:
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
                               time.sleep(1)
                   for enum, price in priceSession.getPrices(contract, timeout=90).items():
                       if "INDICATIVE" in str(enum) and "PRC" in str(enum):
                           logfile = open(r"C:\tt\indprc.log", "a")
                           logfile.write(str([str("-".join([str(time.localtime()[0]), str(time.localtime()[1]), str(time.localtime()[2])])), str(":".join([str(time.localtime()[3]), str(time.localtime()[4]), str(time.localtime()[5])])), str(contract.seriesKey), str(enum), str(price.value)]))
                           pyscreenshot.grab_to_file(r"C:\tt\equilibrium_prc_test_" + ":".join([str(time.localtime()[3]), str(time.localtime()[4]), str(time.localtime()[5])]) + ".png")
                           pricey = None
                           logfile.close()
   except:
       print "ERROR"
   time.sleep(60)



import time
import requests
import json
from pyrate.ttapi.manager import Manager
from ttapi import aenums
slackurl = 'https://hooks.slack.com/services/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'
headers = {'content-type': 'application/json'}
priceSession = Manager().getPriceSession()
while True:
   products_in_preopen = []
   try:
       products = priceSession.getProducts(prodType=aenums.TT_PROD_FUTURE)
       for product in products:
           contracts = priceSession.getContracts(product)#, contractKeys=["394016", "459552"])
           trading = False
           status_sent = False
           for contract in contracts:
               if status_sent:
                   break
               curr_trading_status = None
               if trading:
                   break
               else:
                   prices = priceSession.getPrices(contract, timeout=90)
                   for enum, price in prices.items():
                       if "SRS_STATUS" in str(enum):
                           curr_trading_status = price.value
                           if curr_trading_status != 8:
                               trading = True
                               break
                           else:
                               products_in_preopen.append(product.prod_chr)
                               status_sent = True
           time.sleep(1)
   except:
       print contract, prices
       pass
   if len(products_in_preopen) > 0:
       text_block = "<@U0502QW1P> {0} The following products are now in Pre-Open {1}".format(":".join([str(time.localtime()[3]).zfill(2), str(time.localtime()[4]).zfill(2), str(time.localtime()[5]).zfill(2)]), str(products_in_preopen))
       payload = {"channel": "#cmtest", "username": "webhookbot", "text": text_block}
       json_data = json.dumps(payload)
       requests.post(url=slackurl, data=json_data, headers=headers)
   time.sleep(60)




python
f = open(r'/var/log/debesys/parsed_B45J1TT007.log', 'r')
all_uexids = []
all_exids = []
uexid_dups = []
exid_dups = []
uexid_missing = []
exid_missing = []
uexid_missing_idx = []
exid_missing_idx = []
order_id, uexid, exectype = None, None, None
for line in f.readlines():
    if order_id is not None:
        if order_id in line:
            if "MO31" in line:
                print line
                order_id = None
    if "2019-Mar" in line:
       date = line.split(" ")[2]
       if date == "2019-Mar-14":
           if "BD6" in line:
               for elem in line.split(" "):
                   if elem.startswith("ex_customer_s=}order_number_u"):
                       order_id = elem.split("=")[-1]

f.close()

python
nos_count = 0
tcr_count = 0
orders_list = []
orders_list.append("73e5ea44-1073-4e80-b1ea-a314a0e2c125")
f = open(r'/var/log/debesys/OC_ose.log', 'r')
for line in f.readlines():
    date, time, msgtype, exch_ord_status, exec_id, ord_status, ord_type, sec_order_id, trade_id = None, None, None, None, None, None, None, None, None
    for order_num in orders_list:
        if order_num in line:
            if any(msg in line for msg in ["NewOrderSingle", "TradeCaptureReport"]):
                if "NewOrderSingle" in line:
                    nos_count += 1
                elif "TradeCaptureReport" in line:
                    tcr_count += 1
                date = line.split(" ")[0]
                time = line.split(" ")[1]
                msgtype = line.split(" ")[11]
                if date == "2020-01-10":
                    print line

print "Total NewOrderSingles = {}".format(nos_count)
print "Total TradeCaptureReports = {}".format(tcr_count)

f.close()

import os
list_of_markets = []
list_of_psdu_enabled_markets = []
market_schedules = []
price_server_and_uploader_schedule = {}
cronfiles = os.listdir(r"/home/cmaurer/cron_files")
for cronfile in cronfiles:
    if cronfile.startswith("ps_"):
        market_name = cronfile.split("_")[1]
    elif "_ps_" in cronfile:
        market_name = cronfile.split("_ps_")[0]
        if market_name not in list_of_markets:
            list_of_markets.append(market_name)

for market_name in list_of_markets:
    for cronfile in cronfiles:
        if '_'.join(["pdsu", market_name]) in cronfile:
            if market_name not in list_of_psdu_enabled_markets:
                list_of_psdu_enabled_markets.append(market_name)

for market_name in list_of_markets:
    if market_name not in list_of_psdu_enabled_markets:
        print market_name

for market_name in list_of_markets:
    price_server_and_uploader_schedule.update({market_name: None})
    dictionary = {}
    for cronfile in cronfiles:
        if market_name in cronfile:
            schedule_type = "ps" if "_ps_" in cronfile else "pdsu"
            schedule_file = open(cronfile, 'r')
            for line in schedule_file.readlines():
                if "root" in line:
                    schedule_data = line.split(' ')
            dictionary.update({'_'.join([schedule_type, schedule_data[-2]]): schedule_data[4] + ' @ ' + ':'.join([schedule_data[1], schedule_data[0]])})
            schedule_file.close()
    price_server_and_uploader_schedule[market_name] = dictionary

for item in price_server_and_uploader_schedule:
    table_row = []
    table_row.append(item)
    if 'ps_start' in price_server_and_uploader_schedule[item]:
        table_row.append(price_server_and_uploader_schedule[item]['ps_start'])
    else:
        table_row.append("#")
    if 'ps_stop' in price_server_and_uploader_schedule[item]:
        table_row.append(price_server_and_uploader_schedule[item]['ps_stop'])
    else:
        table_row.append("#")
    if 'pdsu_start' in price_server_and_uploader_schedule[item]:
        table_row.append(price_server_and_uploader_schedule[item]['pdsu_start'])
    else:
        table_row.append("#")
    if 'pdsu_stop' in price_server_and_uploader_schedule[item]:
        table_row.append(price_server_and_uploader_schedule[item]['pdsu_stop'])
    else:
        table_row.append("#")
    print table_row

    print ','.join([price_server_and_uploader_schedule[item], price_server_and_uploader_schedule[item]['ps_start'], price_server_and_uploader_schedule[item]['ps_stop'], price_server_and_uploader_schedule[item]['pdsu_start'], price_server_and_uploader_schedule[item]['pdsu_stop']])

