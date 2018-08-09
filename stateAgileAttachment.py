from pyrate.ttapi.manager import Manager
from pyrate.ttapi.order import TTAPIOrder
from ttapi import aenums, cppclient
priceSession = Manager().getPriceSession()
priceSrv = Manager().getPriceServer()
products = priceSession.getProducts()
contracts_missing_agile = []
for product in products:
    contracts = priceSession.getContracts(product)
    for contract in contracts:
        if 1027 not in contract.RetrieveAttachmentIDs():
            contracts_missing_agile.append(contract)

if len(contracts_missing_agile) > 0:
    print "These contracts did not pass the test:\n", contracts_missing_agile


        break
    break
