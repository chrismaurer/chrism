from pyrate.ttapi.manager import Manager
from pyrate.ttapi.order import TTAPIOrder
from ttapi import aenums, cppclient
priceSession = Manager().getPriceSession()
priceSrv = Manager().getPriceServer()
products = priceSession.getProducts()
for product in products:
    contracts = priceSession.getContracts(product)
    for contract in contracts:
        for agile_id in contract.RetrieveAttachmentIDs():
            print agile_id
        break
    break
