from pyrate.ttapi.manager import Manager
from pyrate.ttapi.order import TTAPIOrder
from ttapi import aenums, cppclient
priceSession = Manager().getPriceSession()
priceSrv = Manager().getPriceServer()
products = priceSession.getProducts()
missing_agile = []
for product in products:
    contracts = priceSession.getContracts(product)
    for contract in contracts:
        if 1080 not in contract.RetrieveAttachmentIDs():
            missing_agile.append(" ".join([product.prod_chr, str(product.prod_type).replace("TT_PROD_", ""), contract.seriesKey, "\n"]))

if len(missing_agile) > 0:
    logfile = open(r"c:\tt\agile_text.log", "w")
    print "\n\n\nThe following contracts are missing the agile attachment:\n\n"
    for instrument in missing_agile:
        logfile.write(instrument)
    logfile.close()


