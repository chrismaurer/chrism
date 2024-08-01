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




python
import os
oc_log = None
for filename in os.listdir('/var/log/debesys'):
    if filename.startswith('OC_'):
        if 'log' in filename and '-' not in filename:
            oc_log = '/var/log/debesys/' + filename

f = open(oc_log, 'r')
for line in f.readlines():
    if "Updated, id=" in line or "Updating Account" in line or "ProcessTTUSRiskGroup" in line:
        risk_record = line.split(" ")
        date = risk_record[0]
        time = risk_record[1]

target_records = ['131657', ]
print_out = False
print "Updated at {} {}\n".format(date, time)
for item in risk_record:
    if "=" in item:
        key, value = item.split("=")[0], item.split("=")[1]
        if key == "account_id" or key == "id":
            print_out = True
        if key == "id" and value not in target_records:
            print_out = False
        if print_out:
            if value != "false":
                key_value_pair = "\n" + " = ".join([key, value]) +  "\n---------------" if key == "id" else " = ".join([key, value])
                print key_value_pair

f.close()

exit()





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
all_exec_types = ["OrderCancelReject", "EXEC_TYPE_SUSPENDED", "EXEC_TYPE_REJECTED", "EXEC_TYPE_TRADE", "EXEC_TYPE_CANCELED", "EXEC_TYPE_REPLACED", "EXEC_TYPE_NEW"]
f = open(r'/var/log/debesys/OC_eex_derivative.log', 'r')
for line in f.readlines():
    OrderCancelReject = False
    exec_type = None
    date = " ".join(line.split(" ")[0:1])
    if date == "2021-11-16":
        if ("ExecutionReport" in line or "OrderCancelReject" in line) and "user_id=9587" in line:
            if "OrderCancelReject" in line:
                exec_type = "OrderCancelReject"
            else:
                for elem in line.split(" "):
                    if elem.startswith("exec_type="):
                        exec_type = elem.split("=")[-1].replace("\"", "")
    if exec_type is not None:
        if any(target_exec_type in exec_type for target_exec_type in all_exec_types):
            if "PENDING" not in exec_type:
                print("h4." + exec_type + "\n")
                partyparty = None
                for elem in line.split(" "):
                    if elem == "parties":
                        partyparty = []
                    if partyparty is not None:
                        if elem == "}":
                            partyparty.append("\\" + elem)
                            if "PARTY_ROLE_INVESTMENT_DECISION_MAKER" in str(partyparty) or "PARTY_ROLE_EXECUTING_TRADER" in str(partyparty):
                                print(" ".join(partyparty))
                            partyparty = None
                        else:
                            if elem == "{":
                                partyparty.append("\\" + elem)
                            else:
                                partyparty.append(elem)
                print("\n{code}" + line + "{code}\n")

f.close()

f = open(r'/var/log/debesys/OC_tfx.log', 'r')
for line in f.readlines():
    if "Removing expired DAY order" in line:
        for order in orders_list:
            if order in line:
                orders_list.pop(orders_list.index(order))
                print order

f.close()

if len(all_client_ips) > 1:
    for client_ip in all_client_ips:
        print client_ip

f.close()


python
f = open(r'/var/log/debesys/OC_hkex.log', 'r')
f = open(r'/var/log/debesys/OC_ose.log', 'r')
for line in f.readlines():
    if '8319a0cf-af0a-4b86-9f76-e3217a58ebf0' in line:
        for elem in line.split(" "):
            elem_list = elem.split("=")
            try:
                print("{} = {}".format(elem_list[0], elem_list[1]))
            except IndexError:
                print elem_list
        print '- ' * 30

f.close()
exit()




python
f = open(r'/var/log/debesys/OC_tfx.log-20201209-1607538002', 'r')
all_uexids = []
all_exids = []
uexid_dups = []
exid_dups = []
uexid_missing = []
exid_missing = []
uexid_missing_idx = []
exid_missing_idx = []
skip_lines = ("_inl.h", "MEMORY", "otcs", "otc(s)", "NUMA", "(keyed", "deleted order(s)", "deleted orders")
for line in f.readlines():
    exid, uexid, exectype, ordstatus, trdstatus, trdtype, transtype, ordid = None, None, None, None, None, None, None, None
    date = " ".join(line.split(" ")[0:1])
    if date == "2020-12-07":
       if any(msg in line for msg in ["ExecutionReport", "OrderFillUpdateResp", "TradeCaptureReport",
                                      "OrderCancelReplaceRequest", "OrderCancelReject", "NewOrderSingle",
                                      "OrderCancelRequest", "NewTradeCapture", "TradeReport"]):
           if any(skip_line in line for skip_line in skip_lines):
               pass
           else:
               if "PENDING" not in line and "OBDL" not in line:
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
                       if elem.startswith("trd_type"):
                           trdtype = elem.split("=")[-1].replace("\"", "")
                           trdtype = trdtype.replace("\n", "")
                       if elem.startswith("ord_status"):
                           ordstatus = elem.split("=")[-1].replace("\"", "")
                           ordstatus = ordstatus.replace("\n", "")
                       if elem.startswith("trans_type"):
                           transtype = elem.split("=")[-1].replace("\"", "")
                           transtype = transtype.replace("\n", "")
                       if elem.startswith("trd_status"):
                           trdstatus = elem.split("=")[-1].replace("\"", "")
                           trdstatus = trdstatus.replace("\n", "")
                       if elem.startswith("secondary_order_id"):
                           ordid = elem.split("=")[-1].replace("\"", "")
                           ordid = ordid.replace("\n", "")
                   if trdtype is None:
                       trdtype = "None"
                   if trdstatus is None:
                       trdstatus = "None"
                   if transtype is None:
                       transtype = "None"
                   transaction_type = exectype if exectype is not None else trdtype
                   if exectype is None and trdtype == "None":
                       transaction_type = transtype
                   status = ordstatus if ordstatus is not None else trdstatus
                   if " exec_id=" in line and " unique_exec_id=" not in line:
                       uexid_missing.append(" + ".join([transaction_type, status]))
                       if " + ".join([transaction_type, status]) not in uexid_missing_idx:
                           uexid_missing_idx.append(" + ".join([transaction_type, status]))
                   if " unique_exec_id=" in line and " exec_id=" not in line:
                       exid_missing.append(" + ".join([transaction_type, status]))
                       if " + ".join([transaction_type, status]) not in uexid_missing_idx:
                           exid_missing_idx.append(" + ".join([transaction_type, status]))
                   if uexid is not None:
                       if uexid not in all_uexids:
                           all_uexids.append(uexid)
                       else:
                           if uexid not in uexid_dups:
                               uexid_dups.append(uexid)
                   else:
                       uexid_missing.append(" + ".join([transaction_type, status]))
                       if " + ".join([transaction_type, status]) not in uexid_missing_idx:
                           uexid_missing_idx.append(" + ".join([transaction_type, status]))
                   if exid is not None:
                       if exid not in all_exids:
                           all_exids.append(exid)
                       else:
                           if exid not in exid_dups:
                               exid_dups.append(exid)
                   else:
                       exid_missing.append(" + ".join([transaction_type, status]))
                       if " + ".join([transaction_type, status]) not in exid_missing_idx:
                           exid_missing_idx.append(" + ".join([transaction_type, status]))
                   print ordid






python
f = open(r'/var/log/debesys/OC_tfx.log-20201209-1607538002', 'r')
all_uexids = []
all_exids = []
uexid_dups = []
exid_dups = []
uexid_missing = []
exid_missing = []
uexid_missing_idx = []
exid_missing_idx = []
skip_lines = ("_inl.h", "MEMORY", "otcs", "otc(s)", "NUMA", "(keyed", "deleted order(s)", "deleted orders")
for line in f.readlines():
   exid, uexid, exectype = None, None, None
   date = " ".join(line.split(" ")[0:1])
   if date == "2021-03-03":
       if any(msg in line for msg in ["ExecutionReport", "OrderFillUpdateResp", "TradeCaptureReport",
                                      "OrderCancelReplaceRequest", "OrderCancelReject", "NewOrderSingle",
                                      "OrderCancelRequest", "NewTradeCapture", "TradeReport"]):
           if any(skip_line in line for skip_line in skip_lines):
               pass
           else:
               if "PENDING" not in line and "OBDL" not in line:
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
                   if ordstatus == "ORD_STATUS_PENDING_CANCEL":
                       print line

f.close()

print "\n\n\nRESULT\n----\nFound a total of {0} unique_exec_ids\n----\nThe following is a list of possible duplicates, followed by a list of EXEC TYPES that are missing unique_exec_id:".format(str(len(all_uexids)))
for uexid_dup in uexid_dups:
    if ":" in uexid_dup:
        print uexid_dup
    else:
        if uexid_dups.count(uexid_dup) > 1:
            print uexid_dup

print "-"*50

for exid_dup in exid_dups:
    if ":" in exid_dup:
        print exid_dup
    else:
        if exid_dups.count(exid_dup) > 1:
            print exid_dup

print "-"*50

for nouexid_exectype in uexid_missing_idx:
   print nouexid_exectype, ":", uexid_missing.count(nouexid_exectype)

print "-"*50

for noexid_exectype in exid_missing_idx:
   print noexid_exectype, ":", exid_missing.count(noexid_exectype)

f.close()
exit()
1


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
import time
nos_count = 0
tcr_count = 0
orders_list = []
orders_list.append("c8dcf790-2d3c-4952-85f5-f70a90e79442")
f = open(r'/var/log/debesys/OC_tfx.log', 'r')
for line in f.readlines():
    date, time, msgtype, exch_ord_status, exec_type, trade_id = None, None, None, None, None, None
    expire_date, ord_status, ord_type = "None", "None", "None"
    for order_num in orders_list:
        if order_num in line:
            msgtype = line.split(" ")[13] if line.split(" ")[13] == "ExecutionReport" else line.split(" ")[15]
            if msgtype not in ["PriceReasonability", ]:
                for elem in line.split(" "):
                    if elem.startswith("expire_date"):
                        expire_date = elem.split("=")[-1].replace('000000000', '')
                        # expire_date = time.strftime("%D", time.localtime(expire_date))
                    if elem.startswith("ord_status"):
                        ord_status = elem.split("=")[-1]
                    if elem.startswith("ord_type"):
                        ord_type = elem.split("=")[-1]
                print(" - ".join([msgtype, ord_type, ord_status, expire_date]))

f.close()

python
f = open(r'/var/log/debesys/OC_jpx.log-20210817-1629197401', 'r')
results = {}
for line in f.readlines():
    date, time, msgtype, exch_ord_status, exec_id, ord_status, ord_type, sec_order_id, order_id = None, None, None, None, None, None, None, None, None
    if "ExecutionReport" in line:
        date = line.split(" ")[0]
        time = line.split(" ")[1]
        msgtype = line.split(" ")[13]
        if date == "2021-08-17" and msgtype == "ExecutionReport":
            if time.split(":")[0] == "10" and int(time.split(":")[1]) > 40 and int(time.split(":")[1]) < 44:
                for elem in line.split(" "):
                    if elem.startswith("ord_status="):
                        ord_status = elem.split("=")[-1]
                    elif elem.startswith("secondary_order_id="):
                        sec_order_id = elem.split("=")[-1]
                    elif elem.startswith("exch_ord_status="):
                        exch_ord_status = elem.split("=")[-1]
                    elif elem.startswith("ord_type="):
                        ord_type = elem.split("=")[-1]
                    elif elem.startswith("exec_id="):
                        exec_id = elem.split("=")[-1]
                    elif elem.startswith("order_id="):
                        order_id = elem.split("=")[-1]
                if order_id not in results:
                    results[order_id] = []
                if ord_status == "ORD_STATUS_PENDING_NEW":
                    results[order_id].append("ORD_STATUS_PENDING_NEW")
                elif ord_status == "ORD_STATUS_NEW":
                    results[order_id].append("ORD_STATUS_NEW")
                elif ord_status == "ORD_STATUS_REJECTED":
                    results[order_id].append("ORD_STATUS_REJECTED")
                elif ord_status == "ORD_STATUS_FILLED":
                    results[order_id].append("ORD_STATUS_FILLED")

f.close()
for item in results.iteritems():
    print(item)


print 'Number offor moo in ["ADD", "DELETE", "UPDATE", "FILL", "FFILL", "REJECT", "TCR", "TCR_ACK", "PENDING", "RESTATED", "CHGREJECT"]:
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




python
import os
oc_log = None
for filename in os.listdir('/var/log/debesys'):
    if filename.startswith('OC_'):
        if 'log' in filename and '-' not in filename:
            oc_log = '/var/log/debesys/' + filename

f = open(oc_log, 'r')
for line in f.readlines():
    if "Updated, id=" in line or "Updating Account" in line or "ProcessTTUSRiskGroup" in line:
        risk_record = line.split(" ")
        date = risk_record[0]
        time = risk_record[1]

target_records = ['131657', ]
print_out = False
print "Updated at {} {}\n".format(date, time)
for item in risk_record:
    if "=" in item:
        key, value = item.split("=")[0], item.split("=")[1]
        if key == "account_id" or key == "id":
            print_out = True
        if key == "id" and value not in target_records:
            print_out = False
        if print_out:
            if value != "false":
                key_value_pair = "\n" + " = ".join([key, value]) +  "\n---------------" if key == "id" else " = ".join([key, value])
                print key_value_pair

f.close()

exit()





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
orders_list = []
f = open(r'/var/log/debesys/OC_tfx.log', 'r')
for line in f.readlines():
    exid, uexid, exectype, client_ip = None, None, None, None
    date = " ".join(line.split(" ")[0:1])
    if date == "2021-03-03":
        if "ExecutionReport" in line and "ORD_STATUS_FILLED" in line:
            for elem in line.split(" "):
                if elem.startswith("order_id"):
                    order_id = elem.split("=")[-1].replace("\"", "")
                    order_id = order_id.replace("\n", "")
                    if order_id not in orders_list:
                        orders_list.append(order_id)

f.close()

f = open(r'/var/log/debesys/OC_tfx.log', 'r')
for line in f.readlines():
    if "Removing expired DAY order" in line:
        for order in orders_list:
            if order in line:
                orders_list.pop(orders_list.index(order))
                print order

f.close()

if len(all_client_ips) > 1:
    for client_ip in all_client_ips:
        print client_ip

f.close()


python
f = open(r'/var/log/debesys/OC_hkex.log', 'r')
f = open(r'/var/log/debesys/OC_ose.log', 'r')
for line in f.readlines():
    if '8319a0cf-af0a-4b86-9f76-e3217a58ebf0' in line:
        for elem in line.split(" "):
            elem_list = elem.split("=")
            try:
                print("{} = {}".format(elem_list[0], elem_list[1]))
            except IndexError:
                print elem_list
        print '- ' * 30

f.close()
exit()




python
f = open(r'/var/log/debesys/OC_tfx.log-20201209-1607538002', 'r')
all_uexids = []
all_exids = []
uexid_dups = []
exid_dups = []
uexid_missing = []
exid_missing = []
uexid_missing_idx = []
exid_missing_idx = []
skip_lines = ("_inl.h", "MEMORY", "otcs", "otc(s)", "NUMA", "(keyed", "deleted order(s)", "deleted orders")
for line in f.readlines():
    exid, uexid, exectype, ordstatus, trdstatus, trdtype, transtype, ordid = None, None, None, None, None, None, None, None
    date = " ".join(line.split(" ")[0:1])
    if date == "2020-12-07":
       if any(msg in line for msg in ["ExecutionReport", "OrderFillUpdateResp", "TradeCaptureReport",
                                      "OrderCancelReplaceRequest", "OrderCancelReject", "NewOrderSingle",
                                      "OrderCancelRequest", "NewTradeCapture", "TradeReport"]):
           if any(skip_line in line for skip_line in skip_lines):
               pass
           else:
               if "PENDING" not in line and "OBDL" not in line:
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
                       if elem.startswith("trd_type"):
                           trdtype = elem.split("=")[-1].replace("\"", "")
                           trdtype = trdtype.replace("\n", "")
                       if elem.startswith("ord_status"):
                           ordstatus = elem.split("=")[-1].replace("\"", "")
                           ordstatus = ordstatus.replace("\n", "")
                       if elem.startswith("trans_type"):
                           transtype = elem.split("=")[-1].replace("\"", "")
                           transtype = transtype.replace("\n", "")
                       if elem.startswith("trd_status"):
                           trdstatus = elem.split("=")[-1].replace("\"", "")
                           trdstatus = trdstatus.replace("\n", "")
                       if elem.startswith("secondary_order_id"):
                           ordid = elem.split("=")[-1].replace("\"", "")
                           ordid = ordid.replace("\n", "")
                   if trdtype is None:
                       trdtype = "None"
                   if trdstatus is None:
                       trdstatus = "None"
                   if transtype is None:
                       transtype = "None"
                   transaction_type = exectype if exectype is not None else trdtype
                   if exectype is None and trdtype == "None":
                       transaction_type = transtype
                   status = ordstatus if ordstatus is not None else trdstatus
                   if " exec_id=" in line and " unique_exec_id=" not in line:
                       uexid_missing.append(" + ".join([transaction_type, status]))
                       if " + ".join([transaction_type, status]) not in uexid_missing_idx:
                           uexid_missing_idx.append(" + ".join([transaction_type, status]))
                   if " unique_exec_id=" in line and " exec_id=" not in line:
                       exid_missing.append(" + ".join([transaction_type, status]))
                       if " + ".join([transaction_type, status]) not in uexid_missing_idx:
                           exid_missing_idx.append(" + ".join([transaction_type, status]))
                   if uexid is not None:
                       if uexid not in all_uexids:
                           all_uexids.append(uexid)
                       else:
                           if uexid not in uexid_dups:
                               uexid_dups.append(uexid)
                   else:
                       uexid_missing.append(" + ".join([transaction_type, status]))
                       if " + ".join([transaction_type, status]) not in uexid_missing_idx:
                           uexid_missing_idx.append(" + ".join([transaction_type, status]))
                   if exid is not None:
                       if exid not in all_exids:
                           all_exids.append(exid)
                       else:
                           if exid not in exid_dups:
                               exid_dups.append(exid)
                   else:
                       exid_missing.append(" + ".join([transaction_type, status]))
                       if " + ".join([transaction_type, status]) not in exid_missing_idx:
                           exid_missing_idx.append(" + ".join([transaction_type, status]))
                   print ordid






python
f = open(r'/var/log/debesys/OC_tfx.log-20201209-1607538002', 'r')
all_uexids = []
all_exids = []
uexid_dups = []
exid_dups = []
uexid_missing = []
exid_missing = []
uexid_missing_idx = []
exid_missing_idx = []
skip_lines = ("_inl.h", "MEMORY", "otcs", "otc(s)", "NUMA", "(keyed", "deleted order(s)", "deleted orders")
for line in f.readlines():
   exid, uexid, exectype = None, None, None
   date = " ".join(line.split(" ")[0:1])
   if date == "2021-03-03":
       if any(msg in line for msg in ["ExecutionReport", "OrderFillUpdateResp", "TradeCaptureReport",
                                      "OrderCancelReplaceRequest", "OrderCancelReject", "NewOrderSingle",
                                      "OrderCancelRequest", "NewTradeCapture", "TradeReport"]):
           if any(skip_line in line for skip_line in skip_lines):
               pass
           else:
               if "PENDING" not in line and "OBDL" not in line:
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
                   if ordstatus == "ORD_STATUS_PENDING_CANCEL":
                       print line

f.close()

print "\n\n\nRESULT\n----\nFound a total of {0} unique_exec_ids\n----\nThe following is a list of possible duplicates, followed by a list of EXEC TYPES that are missing unique_exec_id:".format(str(len(all_uexids)))
for uexid_dup in uexid_dups:
    if ":" in uexid_dup:
        print uexid_dup
    else:
        if uexid_dups.count(uexid_dup) > 1:
            print uexid_dup

print "-"*50

for exid_dup in exid_dups:
    if ":" in exid_dup:
        print exid_dup
    else:
        if exid_dups.count(exid_dup) > 1:
            print exid_dup

print "-"*50

for nouexid_exectype in uexid_missing_idx:
   print nouexid_exectype, ":", uexid_missing.count(nouexid_exectype)

print "-"*50

for noexid_exectype in exid_missing_idx:
   print noexid_exectype, ":", exid_missing.count(noexid_exectype)

f.close()
exit()
1


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
import time
nos_count = 0
tcr_count = 0
orders_list = []
orders_list.append("c8dcf790-2d3c-4952-85f5-f70a90e79442")
f = open(r'/var/log/debesys/OC_tfx.log', 'r')
for line in f.readlines():
    date, time, msgtype, exch_ord_status, exec_type, trade_id = None, None, None, None, None, None
    expire_date, ord_status, ord_type = "None", "None", "None"
    for order_num in orders_list:
        if order_num in line:
            msgtype = line.split(" ")[13] if line.split(" ")[13] == "ExecutionReport" else line.split(" ")[15]
            if msgtype not in ["PriceReasonability", ]:
                for elem in line.split(" "):
                    if elem.startswith("expire_date"):
                        expire_date = elem.split("=")[-1].replace('000000000', '')
                        # expire_date = time.strftime("%D", time.localtime(expire_date))
                    if elem.startswith("ord_status"):
                        ord_status = elem.split("=")[-1]
                    if elem.startswith("ord_type"):
                        ord_type = elem.split("=")[-1]
                print(" - ".join([msgtype, ord_type, ord_status, expire_date]))

f.close()

python
f = open(r'/var/log/debesys/OC_jpx.log-20210817-1629197401', 'r')
results = {}
for line in f.readlines():
    date, time, msgtype, exch_ord_status, exec_id, ord_status, ord_type, sec_order_id, order_id = None, None, None, None, None, None, None, None, None
    if "ExecutionReport" in line:
        date = line.split(" ")[0]
        time = line.split(" ")[1]
        msgtype = line.split(" ")[13]
        if date == "2021-08-17" and msgtype == "ExecutionReport":
            if time.split(":")[0] == "10" and int(time.split(":")[1]) > 40 and int(time.split(":")[1]) < 44:
                for elem in line.split(" "):
                    if elem.startswith("ord_status="):
                        ord_status = elem.split("=")[-1]
                    elif elem.startswith("secondary_order_id="):
                        sec_order_id = elem.split("=")[-1]
                    elif elem.startswith("exch_ord_status="):
                        exch_ord_status = elem.split("=")[-1]
                    elif elem.startswith("ord_type="):
                        ord_type = elem.split("=")[-1]
                    elif elem.startswith("exec_id="):
                        exec_id = elem.split("=")[-1]
                    elif elem.startswith("order_id="):
                        order_id = elem.split("=")[-1]
                if order_id not in results:
                    results[order_id] = []
                if ord_status == "ORD_STATUS_PENDING_NEW":
                    results[order_id].append("ORD_STATUS_PENDING_NEW")
                elif ord_status == "ORD_STATUS_NEW":
                    results[order_id].append("ORD_STATUS_NEW")
                elif ord_status == "ORD_STATUS_REJECTED":
                    results[order_id].append("ORD_STATUS_REJECTED")
                elif ord_status == "ORD_STATUS_FILLED":
                    results[order_id].append("ORD_STATUS_FILLED")

f.close()
for item in results.iteritems():
    print(item)


print 'Number of orders with \"removed from orderbook\" message:', len(removed_from_orderbook_orders)
print 'Number of orders filled:', len(filled_orders)
print 'The following filled orders do not have the \"removed from orderbook\" message:'
for fill_order in filled_orders:
    if fill_order not in removed_from_orderbook_orders:
        print fill_order

print 'Number of orders canceled:', len(canceled_orders)
print 'The following canceled orders do not have the \"removed from orderbook\" message:'
for cancel_order in canceled_orders:
    if cancel_order not in removed_from_orderbook_orders:
        print cancel_order

print 'The following orders have the \"removed from orderbook\" message but their status seems inconsistent:'
for removed_from_orderbook_order in removed_from_orderbook_orders:
    if removed_from_orderbook_order not in canceled_orders and removed_from_orderbook_order not in filled_orders:
        print removed_from_orderbook_order

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


#####################################################


python
from datetime import date, datetime
import os
logfile_path = r'/var/log/debesys/'
all_logfiles = os.listdir(logfile_path)
all_prod_info = []
tick_table_match_patterns = {}
tick_table_match_discrepancies = []
for logfile in all_logfiles:
    if 'pdsu_krx.log' in logfile:
        f = open(logfile_path + logfile, 'r')
        for line in f.readlines():
            if 'OnProductInfo:' in line and 'OnProductInfo: Leg' not in line:
                symbol, product_type_id, security_id, tick_table = None, None, None, None
                try:
                    datestamp = line.split(" | ")[0]
                    logtime = line.split(" | ")[1]
                    msgtype = line.split(" | ")[11]
                    for elem in line.split(" | "):
                        if elem.startswith("name="):
                            symbol = elem.split("symbol=")[-1].split(" ")[0]
                            product_type_id = elem.split("symbol=")[-1].split(" ")[-1].split("=")[-1]
                        elif elem.startswith("security_id="):
                            security_id = elem.split("=")[-1]
                        elif elem.startswith("tick_table="):
                            tick_table = elem.split("=")[-1]
                    try:
                        if security_id is not None:
                            all_prod_info.append("#".join([symbol, product_type_id, security_id, tick_table]))
                    except:
                        print(line)
                        break
                except:
                    print("ERROR! line:", line)
                    break
        f.close()

for prod_info in all_prod_info:
    prod_info_list = prod_info.split("#")
    key = "-".join(prod_info_list[0:2]).replace("\"", "")
    if key not in tick_table_match_patterns:
        tick_table_match_patterns[key] = prod_info_list[-1]
    else:
        if prod_info_list[-1] != str(tick_table_match_patterns[key]):
            tick_table_match_discrepancies.append(prod_info_list)

if len(tick_table_match_discrepancies) > 0:
    print("ERROR! {} Tick Table Discrepancies detected!")
    for tick_table_match_discrepancy in tick_table_match_discrepancies:
        print(tick_table_match_discrepancy)


for line in f.readlines():
    date, logtime, exch_ord_status, exec_id, exec_type, ord_status, order_id, ord_type, secondary_order_id, secondary_cl_ord_id, trade_id = None, None, None, None, None, None, None, None, None, None, None
    if any(msg in line for msg in ["secondary_cl_ord_id", ]):
        try:
            date = line.split(" ")[0]
            logtime = line.split(" ")[1]
            msgtype = line.split(" ")[11]
            if date == "2020-04-03" and "ERROR" not in line:
                for elem in line.split(" "):
                    if elem.startswith("ord_status="):
                        ord_status = elem.split("=")[-1]
                    elif elem.startswith("secondary_order_id="):
                        secondary_order_id = elem.split("=")[-1]
                    elif elem.startswith("secondary_cl_ord_id="):
                        secondary_cl_ord_id = elem.split("=")[-1]
                    elif elem.startswith("exch_ord_status="):
                        exch_ord_status = elem.split("=")[-1]
                    elif elem.startswith("ord_type="):
                        ord_type = elem.split("=")[-1]
                    elif elem.startswith("exec_id="):
                        exec_id = elem.split("=")[-1]
                    elif elem.startswith("exec_type="):
                        exec_type = elem.split("=")[-1]
                    elif elem.startswith("order_id="):
                        order_id = elem.split("=")[-1]
                    elif elem.startswith("trade_id="):
                        trade_id = elem.split("=")[-1]
                if len(secondary_cl_ord_id.replace("\"", "")) != 13:
                    counter =+ 1
                    incorrect_clordids.append(": ".join([order_id, secondary_cl_ord_id]))
        except IndexError:
            pass

f.close()
print "Found {} orders".format(counter)
print incorrect_clordids




print 'Number of orders with \"removed from orderbook\" message:', len(removed_from_orderbook_orders)
print 'Number of orders filled:', len(filled_orders)
print 'The following filled orders do not have the \"removed from orderbook\" message:'
for fill_order in filled_orders:
    if fill_order not in removed_from_orderbook_orders:
        print fill_order

print 'Number of orders canceled:', len(canceled_orders)
print 'The following canceled orders do not have the \"removed from orderbook\" message:'
for cancel_order in canceled_orders:
    if cancel_order not in removed_from_orderbook_orders:
        print cancel_order

print 'The following orders have the \"removed from orderbook\" message but their status seems inconsistent:'
for removed_from_orderbook_order in removed_from_orderbook_orders:
    if removed_from_orderbook_order not in canceled_orders and removed_from_orderbook_order not in filled_orders:
        print removed_from_orderbook_order



# DEB-116742 pse: Reset field defaults for legacy pdsu/pse architecture

python
import os
import gzip

logfile_dir = r'/var/log/debesys/'
logfiles = os.listdir(logfile_dir)
for logfile in logfiles:
    logfilename = "".join((logfile_dir, logfile))
    if 'pdsu' in logfilename:
        testfile = logfilename
        if '.gz' in logfilename:
            print('Unzipping {}'.format(logfilename))
            input = gzip.GzipFile(logfilename, 'rb')
            s = input.read()
            input.close()
            output = open(logfilename.replace('.gz', ''), 'wb')
            output.write(s)
            output.close()
            print('Done')
            testfile = logfilename.replace('.gz', '')


        logfile_output = open(testfile, 'r')
        for line in logfile_output:
           if 'New instrument' in line:
               instrument_identifier = None
               new_instrument_data = line.split('New instrument')[1]
               for elem in new_instrument_data.split(' '):
                   if ':' in elem:
                       instrument_identifier = elem.split(':')[1]
                       break
               print('instrument_identifier =', instrument_identifier)
        logfile_output.close()




                   if elem.startswith('New instrument')[1]:
                       exid = elem.split("=")[-1].replace("\"", "")
                       exid = exid.replace("\n", "")



"""FIX MESSAGES, BITCH!!!"""
python
import os
logfile_path = r'/var/log/debesys/'
all_logfiles = os.listdir(logfile_path)
all_cl_ord_ids = []
dup_cl_ord_ids = []
for logfile in all_logfiles:
    if 'OC_tfx.log' in logfile:
        f = open(logfile_path + logfile, 'r')
        for line in f.readlines():
            cl_ord_id = None
            if "35=8" in line and "39=0" in line and "CassandraMessageStore" not in line:
                line = line.split(u'\u0001')
                try:
                    date = line[0].split(" ")[0]
                    logtime = line[0].split(" ")[1]
                    for elem in line:
                        if elem.startswith("11="):
                            cl_ord_id = elem.split("=")[-1]
                    try:
                        if cl_ord_id in all_cl_ord_ids:
                            dup_cl_ord_ids.append(cl_ord_id)
                        else:
                            all_cl_ord_ids.append(cl_ord_id)
                    except:
                        print(line)
                except:
                    print("ERROR! line:", line)
        f.close()

if len(dup_cl_ord_ids) > 0:
    print("ERROR! Duplicate ClOrdIDs detected!")
    for dup_cl_ord_id in dup_cl_ord_ids:
        print(dup_cl_ord_id)


import os, json, ast
logfile_path = r'/var/log/debesys/'
all_instruments = {}
all_logfiles = os.listdir(logfile_path)
for logfile in all_logfiles:
    if 'pdsu_sgx' in logfile and '.gz' not in logfile:
        f = open(logfile_path + logfile, 'r')
        for line in f.readlines():
            if 'PriceConversionFactor' in line and 'JSON:' in line:
                payload = line.split('JSON:')[1]
                output = json.loads(payload)
                for record in output['products'][0]['instruments']:
                    alias = record['instr']['a']
                    pcf_dict = ast.literal_eval(record['instr']['data'])
                    pcf = pcf_dict['PriceConversionFactor']
                    if alias not in all_instruments:
                        all_instruments[alias] = pcf

f.close()

import os
logfile = r'/var/log/debesys/OC_eurex.log-20210915-1631725801'
f = open(logfile, 'r')
for line in f.readlines():
    if 'ExecutionReport' in line and '4ce3ebbe-982e-41d4-8f82-132635582d95' in line:
        exec_type = None, None, None
        payload = line.split(' | ')
        date = payload[0].split(" ")[0]
        logtime = payload[0].split(" ")[1]
        if date in ('2021-06-30', '2021-06-31', '2021-07-01'):
            for elem in payload:
                if elem.startswith("instrumentName="):
                    instrumentName = elem.split("=")[-1]
                if elem.startswith("securityId="):
                    securityId = elem.split("=")[-1]
                elif elem.startswith("statsKey="):
                    statsKey = elem.split("=")[-1]
            if statsKey != securityId:
                stat_key_issues.append([securityId, statsKey, ":", date, logtime])

f.close()

if len(stat_key_issues) > 0:
    print("ERROR! {} statKey issues detected out of {} records tested!".format(len(stat_key_issues), counter))
    for stat_key_issue in stat_key_issues:
        print(stat_key_issue)

 orders with \"removed from orderbook\" message:', len(removed_from_orderbook_orders)
print 'Number of orders filled:', len(filled_orders)
print 'The following filled orders do not have the \"removed from orderbook\" message:'
for fill_order in filled_orders:
    if fill_order not in removed_from_orderbook_orders:
        print fill_order

print 'Number of orders canceled:', len(canceled_orders)
print 'The following canceled orders do not have the \"removed from orderbook\" message:'
for cancel_order in canceled_orders:
    if cancel_order not in removed_from_orderbook_orders:
        print cancel_order

print 'The following orders have the \"removed from orderbook\" message but their status seems inconsistent:'
for removed_from_orderbook_order in removed_from_orderbook_orders:
    if removed_from_orderbook_order not in canceled_orders and removed_from_orderbook_order not in filled_orders:
        print removed_from_orderbook_order

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


#####################################################


python
from datetime import date, datetime
import os
logfile_path = r'/var/log/debesys/'
all_logfiles = os.listdir(logfile_path)
all_prod_info = []
tick_table_match_patterns = {}
tick_table_match_discrepancies = []
for logfile in all_logfiles:
    if 'pdsu_krx.log' in logfile:
        f = open(logfile_path + logfile, 'r')
        for line in f.readlines():
            if 'OnProductInfo:' in line and 'OnProductInfo: Leg' not in line:
                symbol, product_type_id, security_id, tick_table = None, None, None, None
                try:
                    datestamp = line.split(" | ")[0]
                    logtime = line.split(" | ")[1]
                    msgtype = line.split(" | ")[11]
                    for elem in line.split(" | "):
                        if elem.startswith("name="):
                            symbol = elem.split("symbol=")[-1].split(" ")[0]
                            product_type_id = elem.split("symbol=")[-1].split(" ")[-1].split("=")[-1]
                        elif elem.startswith("security_id="):
                            security_id = elem.split("=")[-1]
                        elif elem.startswith("tick_table="):
                            tick_table = elem.split("=")[-1]
                    try:
                        if security_id is not None:
                            all_prod_info.append("#".join([symbol, product_type_id, security_id, tick_table]))
                    except:
                        print(line)
                        break
                except:
                    print("ERROR! line:", line)
                    break
        f.close()

for prod_info in all_prod_info:
    prod_info_list = prod_info.split("#")
    key = "-".join(prod_info_list[0:2]).replace("\"", "")
    if key not in tick_table_match_patterns:
        tick_table_match_patterns[key] = prod_info_list[-1]
    else:
        if prod_info_list[-1] != str(tick_table_match_patterns[key]):
            tick_table_match_discrepancies.append(prod_info_list)

if len(tick_table_match_discrepancies) > 0:
    print("ERROR! {} Tick Table Discrepancies detected!")
    for tick_table_match_discrepancy in tick_table_match_discrepancies:
        print(tick_table_match_discrepancy)


for line in f.readlines():
    date, logtime, exch_ord_status, exec_id, exec_type, ord_status, order_id, ord_type, secondary_order_id, secondary_cl_ord_id, trade_id = None, None, None, None, None, None, None, None, None, None, None
    if any(msg in line for msg in ["secondary_cl_ord_id", ]):
        try:
            date = line.split(" ")[0]
            logtime = line.split(" ")[1]
            msgtype = line.split(" ")[11]
            if date == "2020-04-03" and "ERROR" not in line:
                for elem in line.split(" "):
                    if elem.startswith("ord_status="):
                        ord_status = elem.split("=")[-1]
                    elif elem.startswith("secondary_order_id="):
                        secondary_order_id = elem.split("=")[-1]
                    elif elem.startswith("secondary_cl_ord_id="):
                        secondary_cl_ord_id = elem.split("=")[-1]
                    elif elem.startswith("exch_ord_status="):
                        exch_ord_status = elem.split("=")[-1]
                    elif elem.startswith("ord_type="):
                        ord_type = elem.split("=")[-1]
                    elif elem.startswith("exec_id="):
                        exec_id = elem.split("=")[-1]
                    elif elem.startswith("exec_type="):
                        exec_type = elem.split("=")[-1]
                    elif elem.startswith("order_id="):
                        order_id = elem.split("=")[-1]
                    elif elem.startswith("trade_id="):
                        trade_id = elem.split("=")[-1]
                if len(secondary_cl_ord_id.replace("\"", "")) != 13:
                    counter =+ 1
                    incorrect_clordids.append(": ".join([order_id, secondary_cl_ord_id]))
        except IndexError:
            pass

f.close()
print "Found {} orders".format(counter)
print incorrect_clordids




print 'Number of orders with \"removed from orderbook\" message:', len(removed_from_orderbook_orders)
print 'Number of orders filled:', len(filled_orders)
print 'The following filled orders do not have the \"removed from orderbook\" message:'
for fill_order in filled_orders:
    if fill_order not in removed_from_orderbook_orders:
        print fill_order

print 'Number of orders canceled:', len(canceled_orders)
print 'The following canceled orders do not have the \"removed from orderbook\" message:'
for cancel_order in canceled_orders:
    if cancel_order not in removed_from_orderbook_orders:
        print cancel_order

print 'The following orders have the \"removed from orderbook\" message but their status seems inconsistent:'
for removed_from_orderbook_order in removed_from_orderbook_orders:
    if removed_from_orderbook_order not in canceled_orders and removed_from_orderbook_order not in filled_orders:
        print removed_from_orderbook_order



# DEB-116742 pse: Reset field defaults for legacy pdsu/pse architecture

python
import os
import gzip

logfile_dir = r'/var/log/debesys/'
logfiles = os.listdir(logfile_dir)
for logfile in logfiles:
    logfilename = "".join((logfile_dir, logfile))
    if 'pdsu' in logfilename:
        testfile = logfilename
        if '.gz' in logfilename:
            print('Unzipping {}'.format(logfilename))
            input = gzip.GzipFile(logfilename, 'rb')
            s = input.read()
            input.close()
            output = open(logfilename.replace('.gz', ''), 'wb')
            output.write(s)
            output.close()
            print('Done')
            testfile = logfilename.replace('.gz', '')


        logfile_output = open(testfile, 'r')
        for line in logfile_output:
           if 'New instrument' in line:
               instrument_identifier = None
               new_instrument_data = line.split('New instrument')[1]
               for elem in new_instrument_data.split(' '):
                   if ':' in elem:
                       instrument_identifier = elem.split(':')[1]
                       break
               print('instrument_identifier =', instrument_identifier)
        logfile_output.close()




                   if elem.startswith('New instrument')[1]:
                       exid = elem.split("=")[-1].replace("\"", "")
                       exid = exid.replace("\n", "")



"""FIX MESSAGES, BITCH!!!"""
python
import os
logfile_path = r'/var/log/debesys/'
all_logfiles = os.listdir(logfile_path)
all_cl_ord_ids = []
dup_cl_ord_ids = []
for logfile in all_logfiles:
    if 'OC_tfx.log' in logfile:
        f = open(logfile_path + logfile, 'r')
        for line in f.readlines():
            cl_ord_id = None
            if "35=8" in line and "39=0" in line and "CassandraMessageStore" not in line:
                line = line.split(u'\u0001')
                try:
                    date = line[0].split(" ")[0]
                    logtime = line[0].split(" ")[1]
                    for elem in line:
                        if elem.startswith("11="):
                            cl_ord_id = elem.split("=")[-1]
                    try:
                        if cl_ord_id in all_cl_ord_ids:
                            dup_cl_ord_ids.append(cl_ord_id)
                        else:
                            all_cl_ord_ids.append(cl_ord_id)
                    except:
                        print(line)
                except:
                    print("ERROR! line:", line)
        f.close()

if len(dup_cl_ord_ids) > 0:
    print("ERROR! Duplicate ClOrdIDs detected!")
    for dup_cl_ord_id in dup_cl_ord_ids:
        print(dup_cl_ord_id)


import os, json, ast
logfile_path = r'/var/log/debesys/'
all_instruments = {}
all_logfiles = os.listdir(logfile_path)
for logfile in all_logfiles:
    if 'pdsu_sgx' in logfile and '.gz' not in logfile:
        f = open(logfile_path + logfile, 'r')
        for line in f.readlines():
            if 'PriceConversionFactor' in line and 'JSON:' in line:
                payload = line.split('JSON:')[1]
                output = json.loads(payload)
                for record in output['products'][0]['instruments']:
                    alias = record['instr']['a']
                    pcf_dict = ast.literal_eval(record['instr']['data'])
                    pcf = pcf_dict['PriceConversionFactor']
                    if alias not in all_instruments:
                        all_instruments[alias] = pcf

f.close()


# Detect OrderBookID change
import os
logfile_path = r'/var/log/debesys/'
all_instruments = {}
changed = []
all_logfiles = os.listdir(logfile_path)
for logfile in all_logfiles:
    if 'mds_tfex_dev' in logfile and '.gz' not in logfile:
        f = open(logfile_path + logfile, 'r')
        for line in f.readlines():
            if 'OnInstrumentDefinition' in line:
                date = line.split(" ")[0]
                logtime = line.split(" ")[1]
                for elem in line.split(" "):
                    if elem.startswith("indesc="):
                        order_book_id = elem.split("=")[-1]
                    elif elem.startswith("name="):
                        name = elem.split("=")[-1]
                        name = name.replace("\n", "")
                if name in all_instruments:
                    if all_instruments[name] != order_book_id:
                        if name not in changed:
                            print("{} {}, {} orderBookId change - old: {} new: {}".format(date, logtime, name, all_instruments[name], order_book_id))
                            changed.append(name)
                else:
                    all_instruments[name] = order_book_id

f.close()

# Detect OrderBookID change
import os
logfile_path = r'/var/log/debesys/'
all_instruments = {}
changed = []
all_logfiles = os.listdir(logfile_path)
for logfile in all_logfiles:
    if 'mds_tfex_dev' in logfile and '.gz' not in logfile:
        f = open(logfile_path + logfile, 'r')
        for line in f.readlines():
            if 'OnInstrumentDefinition' in line:
                date = line.split(" ")[0]
                logtime = line.split(" ")[1]
                for elem in line.split(" "):
                    if elem.startswith("indesc="):
                        order_book_id = elem.split("=")[-1]
                    elif elem.startswith("name="):
                        name = elem.split("=")[-1]
                        name = name.replace("\n", "")
                if name in all_instruments:
                    if all_instruments[name] != order_book_id:
                        if name not in changed:
                            print("{} {}, {} orderBookId change - old: {} new: {}".format(date, logtime, name, all_instruments[name], order_book_id))
                            changed.append(name)
                else:
                    all_instruments[name] = order_book_id

f.close()

# Detect Tick Size change
import os
logfile_path = r'/var/log/debesys/'
all_instruments = {}
changed = []
all_logfiles = os.listdir(logfile_path)
for logfile in all_logfiles:
    if 'mds_tfex_dev' in logfile and '.gz' not in logfile:
        f = open(logfile_path + logfile, 'r')
        for line in f.readlines():
            if 'Instrument Download' in line and 'alias: \"JRF' in line:
                date = line.split(" ")[0]
                logtime = line.split(" ")[1]
                line_list = line.split(" ")
                for elem in line_list:
                    if elem == "tickSize:":
                        tickSize_idx = line_list.index(elem)
                        tickSize = line_list[tickSize_idx + 1]
                    elif elem == "Proto=name:":
                        name_idx = line_list.index(elem)
                        name = line_list[name_idx + 1]
                        name = name.replace("\"", "")
                if name in all_instruments:
                    if all_instruments[name] != tickSize:
                        if name not in changed:
                            print("{} {}, {} tickSize change - old: {} new: {}".format(date, logtime, name, all_instruments[name], tickSize))
                            changed.append(name)
                else:
                    all_instruments[name] = tickSize

f.close()


import os
logfile = r'/var/log/debesys/mds_jpx.log'
all_instruments = {}
f = open(logfile, 'r')
counter = 0
for line in f.readlines():
    if 'SendtoPds' in line:
        counter += 1
        securityId = None
        payload = line.split(',')
        date = payload[0].split(" ")[0]
        logtime = payload[0].split(" ")[1]
        if date in ('2021-09-18', '2021-09-19', ):
            for elem in payload:
                if elem.split(":")[0].replace('"', '') == ("excht"):
                    securityId = elem.split(":")[-1].replace('"', '')
        if securityId:
            if securityId in bbb:
                bbb.remove(securityId)

f.close()

if len(stat_key_issues) > 0:
    print("ERROR! {} statKey issues detected out of {} records tested!".format(len(stat_key_issues), counter))
    for stat_key_issue in stat_key_issues:
        print(stat_key_issue)


listy_list = ["KEF DB HITEK", "KEF DB HITEK", "KEF DB HITEK", "FUT 1EKS6000 DB HiTek FUT 2206", "FUT 1EKT6000 DB HiTek FUT 2306", "KEF DB HITEK", "KEF DB HITEK", "FUT 1EKS9000 DB HiTek FUT 2209", "FUT 1EKSC000 DB HiTek FUT 2212", "FUT 1EKTC000 DB HiTek FUT 2312", "KEF DB HITEK", "FUT 1B5S6000 DaelimInd Futures 2206", "FUT 1B5SC000 DaelimInd Futures 2212", "KEF HYUNDAI ENGINEERING & CONSTRUCTION", "KEF HYUNDAI ENGINEERING & CONSTRUCTION", "KEF HYUNDAI ENGINEERING & CONSTRUCTION", "FUT 1BNS6000 HyundaiEng FUT 2206", "FUT 1BNT6000 HyundaiEng FUT 2306", "KEF HYUNDAI ENGINEERING & CONSTRUCTION", "KEF HYUNDAI ENGINEERING & CONSTRUCTION", "FUT 1BNS9000 HyundaiEng FUT 2209", "FUT 1BNSC000 HyundaiEng FUT 2212", "FUT 1BNTC000 HyundaiEng FUT 2312", "KEF HYUNDAI ENGINEERING & CONSTRUCTION", "KEF SK HYNIX INC", "KEF SK HYNIX INC", "KEF SK HYNIX INC", "FUT 150S6000 SK hynix FUT 2206", "FUT 150T6000 SK hynix FUT 2306", "KEF SK HYNIX INC", "KEF SK HYNIX INC", "FUT 150S9000 SK hynix FUT 2209", "FUT 150SC000 SK hynix FUT 2212", "FUT 150TC000 SK hynix FUT 2312", "KEF SK HYNIX INC", "KEF HITE-JINRO", "KEF HITE-JINRO", "KEF HITE-JINRO", "FUT 1BKS6000 HITEJINRO FUT 2206", "FUT 1BKT6000 HITEJINRO FUT 2306", "KEF HITE-JINRO", "KEF HITE-JINRO", "FUT 1BKS9000 HITEJINRO FUT 2209", "FUT 1BKSC000 HITEJINRO FUT 2212", "FUT 1BKTC000 HITEJINRO FUT 2312", "KEF HITE-JINRO", "KEF HANWHA", "KEF HANWHA", "KEF HANWHA", "FUT 1C9S6000 HANWHA FUT 2206", "FUT 1C9T6000 HANWHA FUT 2306", "KEF HANWHA", "KEF HANWHA", "FUT 1C9S9000 HANWHA FUT 2209", "FUT 1C9SC000 HANWHA FUT 2212", "FUT 1C9TC000 HANWHA FUT 2312", "KEF HANWHA", "KEF KIA CORPORATION", "KEF KIA CORPORATION", "KEF KIA CORPORATION", "FUT 119S6000 KIA CORPOR FUT 2206", "FUT 119T6000 KIA CORPOR FUT 2306", "KEF KIA CORPORATION", "KEF KIA CORPORATION", "FUT 119S9000 KIA CORPOR FUT 2209", "FUT 119SC000 KIA CORPOR FUT 2212", "FUT 119TC000 KIA CORPOR FUT 2312", "KEF KIA CORPORATION", "KEF SAM CHUN DANG PHARM", "KEF SAM CHUN DANG PHARM", "KEF SAM CHUN DANG PHARM", "FUT 1F4S6000 SCD FUT 2206", "FUT 1F4T6000 SCD FUT 2306", "KEF SAM CHUN DANG PHARM", "KEF SAM CHUN DANG PHARM", "FUT 1F4S9000 SCD FUT 2209", "FUT 1F4SC000 SCD FUT 2212", "FUT 1F4TC000 SCD FUT 2312", "KEF SAM CHUN DANG PHARM", "KEF SAMSUNG FIRE & MARINE INSURANCE", "KEF SAMSUNG FIRE & MARINE INSURANCE", "KEF SAMSUNG FIRE & MARINE INSURANCE", "FUT 1CTS6000 SamsungF&M FUT 2206", "FUT 1CTT6000 SamsungF&M FUT 2306", "KEF SAMSUNG FIRE & MARINE INSURANCE", "KEF SAMSUNG FIRE & MARINE INSURANCE", "FUT 1CTS9000 SamsungF&M FUT 2209", "FUT 1CTSC000 SamsungF&M FUT 2212", "FUT 1CTTC000 SamsungF&M FUT 2312", "KEF SAMSUNG FIRE & MARINE INSURANCE", "KEF YUHAN", "KEF YUHAN", "KEF YUHAN", "FUT 1D6S6000 Yuhan FUT 2206", "FUT 1D6T6000 Yuhan FUT 2306", "KEF YUHAN", "KEF YUHAN", "FUT 1D6S9000 Yuhan FUT 2209", "FUT 1D6SC000 Yuhan FUT 2212", "FUT 1D6TC000 Yuhan FUT 2312", "KEF YUHAN"]
for list_item in listy_list:
    list_item = list_item.lower()
    match = False
    list_item_list = list_item.split(" ")[1:]
    krx_data = open(r'/Users/cmaurer/Derivatives_Table.csv', 'r')
    for line in krx_data.readlines():
        description = line.split(',')[-2].lower()
        description = description.replace("krx derivatives futures ", "")
        description = description.replace("krx derivatives options ", "")
        symbol = line.split(',')[-3]
        symbol = symbol.replace("KRDRVOP", "")
        symbol = symbol.replace("KRDRVFU", "")
        if any(i in list_item_list for i in description):
            print(",".join([line.split(',')[-2], symbol]))
    krx_data.close()



dates = open(r'/Users/cmaurer/nse_holidays.csv', 'r')
month_codes = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
for line in dates.readlines():
    holiday = line.split(",")[1]
    datelist = holiday.split("-")
    import_date = ("/".join((month_codes[datelist[1]], datelist[0], datelist[2])))
    print(",".join((line.split(",")[0], import_date, line.split(",")[2])))

dates.close()

moops = ["BRF", "BTF", "CCA", "CEA", "CHA", "CKA", "CNA", "CNF", "CNO", "CS1", "CZA", "DF1", "DQA", "E4F", "EG1", "EXF", "F1F", "FE1", "FF1", "FXF", "G2F", "GDF", "GTF", "LV1", "LVF", "MX1", "MX4", "MXF", "NYA", "OQ1", "PX1", "PY1", "PZ1", "QA1", "QM1", "QWF", "QX1", "QXF", "RHF", "RHO", "RTF", "RTO", "SHF", "SOF", "SPF", "T5F", "TEO", "TFO", "TGF", "TGO", "TJF", "TX1", "TX4", "UDF", "UNF", "XAF", "XBF", "XEF", "XIF", "XJF", "ZEF", "ZFF"]
moops.sort()
counter = 0
listo = []
while len(moops) > 0:
    try:
        listo.append(moops.pop(0))
        if counter == 14:
            print(listo)
            listo = []
            counter = 0
        else:
            counter += 1
    except:
        print(listo)

print(listo)

TradeReportReq = {1: 'possDup', 2: 'member', 3: 'user', 4: 'tradingMember', 5: 'clearingMember', 6: 'actingUser',
                  7: 'account', 501: 'traderId'}
TradeReportDataInPrivate = {1: 'validityTime', 2: 'waitForOtherSide', 3: 'clientTradeReportId', 4: 'combTradeId',
                            5: 'orderBook', 6: 'orderQty', 7: 'price', 8: 'isBid', 9: 'ownMember', 10: 'ownUser',
                            11: 'counterpartyMember', 12: 'counterPartyUser', 13: 'publicRFQId',
                            15: 'ownClearingMember', 17: 'counterpartyClearingMember', 18: 'ownOwnerType',
                            19: 'counterpartyOwnerType', 20: 'ownInfoText', 21: 'counterpartyInfoText',
                            22: 'ownMessageRef', 23: 'counterpartyMessageRef', 24: 'ownAccount',
                            25: 'counterpartyAccount', 26: 'ownIsAggressor', 27: 'counterpartyIsAggressor',
                            28: 'updateLastTradePrice', 29: 'updateHighLow', 30: 'updateVolumeTurnover',
                            31: 'timeOfTrade', 32: 'referenceTradeId', 33: 'externalProtocolData',
                            501: 'ownTraderId', 502: 'counterpartyTraderId', 503: 'isNvdr', 504: 'isTtf',
                            505: 'tradeReportType', 506: 'numberSettlementDays', 507: 'counterpartyIsNvdr',
                            508: 'counterpartyIsTtf', 510: 'ownOpenClose', 511: 'counterpartyOpenClose'}

logline = '09:53:12.029 [40](0x7fde17ff7700) [V] SEND:EmapiTradeReportReq: 29=[1=F|2=0162|3=D0162_CU1_TR|4="|5="|6="|7=cmaurer01|8=[[2=T|3=1661817677846|5=75878|6=444000000|7=37000000|8=T|9=0162|10=D0162_CU1_TR|11=0162|18=101|22=1661817677846|24=cmaurer01|501=D9999|505=TFEX_EURF_EFP|510=1]]|501=D9999]'

emapi_messages = logline.split('EmapiTradeReportReq: ')[1]






da124s = open(r'/Users/cmaurer/da124_issue_uat.csv', 'r')
da124_report = open(r'/Users/cmaurer/da124_report_uat.csv', 'w')
month_codes = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
da124 = False
for line in da124s.readlines():
    if 'DQ124' in line:
        output = None
        da124 = False
        output = [line.split(',')[0], line.split(',')[2].replace('\n', ''), line.split(',')[1]]
        dq124_datestamp = [int(line.split(',')[0].split('-')[0])]
        dq124_datestamp.append(int(month_codes[line.split(',')[0].split('-')[1]]))
        dq124_datestamp.append(int(line.split(',')[0].split('-')[2]))
        dq124_timestamp = [int(line.split(',')[1].split(':')[0])]
        dq124_timestamp.append(int(line.split(',')[1].split(':')[1]))
        dq124_timestamp.append(int(line.split(',')[1].split(':')[2].split('.')[0]))
        dq124_datestamp.extend(dq124_timestamp)
        dq124_datestamp.extend([0, 0, 0])
    if 'DA124' in line:
        if not da124:
            output.extend([line.split(',')[2].replace('\n', ''), line.split(',')[1]])
            da124_datestamp = [int(line.split(',')[0].split('-')[0])]
            da124_datestamp.append(int(month_codes[line.split(',')[0].split('-')[1]]))
            da124_datestamp.append(int(line.split(',')[0].split('-')[2]))
            da124_timestamp = [int(line.split(',')[1].split(':')[0])]
            da124_timestamp.append(int(line.split(',')[1].split(':')[1]))
            da124_timestamp.append(int(line.split(',')[1].split(':')[2].split('.')[0]))
            da124_datestamp.extend(da124_timestamp)
            da124_datestamp.extend([0, 0, 0])
            # print(da124_datestamp)
            da124 = True
            output.append(str(time.mktime(da124_datestamp)-time.mktime(dq124_datestamp)))
            output.append('\n')
        print(output)
        da124_report.write(str(','.join(output)))

da124_report.close()
da124s.close()


"""Get HKEX Underlying Type UnderlyingType undType"""
logfile = r'/Users/cmaurer/ps_hkex.log-20230614-1686801001'
underlying_type_translator = {'1': 'Stock', '2': 'FX', '3': 'Interest Rate', '4': 'Energy',
                              '5': 'Soft and Agrics', '6': 'Metals', '7': 'Equities', '8': 'Currency Index',
                              '9': 'Interest Rates', '10': 'Energy Index', '11': 'Softs and Agrics Index',
                              '12': 'Metal Index', '': "None"}
underlying_types = []
f = open(logfile, 'r')
for line in f.readlines():
    if 'msg_type=301' in line and 'symbol' in line:
        commodity_name, underlying_type, symbol = None, None, None
        payload = line.split('] [')
        for elem in payload:
            if elem.startswith("symbol="):
                symbol = "".join(list(elem.split("=")[-1])[:4]).lstrip("\"")
            if elem.startswith("comName="):
                commodity_name = elem.split("=")[-1]
            if elem.startswith("undType="):
                underlying_type = elem.split("=")[-1].rstrip(']\n')
            commodity_name = "" if commodity_name is None else commodity_name
            underlying_type = "" if underlying_type is None else underlying_type
            symbol = "" if symbol is None else symbol
            if [commodity_name, underlying_type, symbol] != [None, None, None]:
                if commodity_name not in str(underlying_types):
                    underlying_types.append([commodity_name, symbol, underlying_type_translator[underlying_type]])

underlying_types.sort()
for underlying_type in underlying_types:
    if "None" not in underlying_type:
        print(",".join((underlying_type[1], underlying_type[2])))

f.close()
