import time
from pyrate.builder import Builder
from pyrate.ttapi.manager import Manager
from pyrate.ttapi.order import TTAPIOrder
from ttapi import aenums, cppclient
from captain.controlled import controlled_name_type, ControlledName
from captain.lib.controlled_types import Tif
priceSession = Manager().getPriceSession()
orderSession = Manager().getOrderFillSession()
allCustDefaults = Manager().getCustomers()
custDefaults = allCustDefaults[0]
ordSrv = Manager().getOrderServer()
priceSrv = Manager().getPriceServer()
missing_products = []
# product_list = ["CH", "EY", "FB", "GD", "ID", "IN", "INB", "ING", "INI", "IU", "JG", "MD", "MY", "ND", "NS", "NU", "PH", "SGP", "ST", "TH", "TU", "TW", "UJ", "UY"]
product_list = ["A50", "AAC", "ABC", "ACC", "AIA", "ALC", "ALI", "AMC", "AVI", "BAI", "BCL", "BCM", "BEA", "BOC", "BYD", "CCB", "CCC", "CCE", "CCS", "CDA", "CGN", "CHB", "CHO", "CHQ", "CHT", "CHU", "CIT", "CKH", "CKP", "CLI", "CLP", "CMB", "CNC", "COG", "COL", "CPA", "CPC", "CPI", "CRC", "CRG", "CRL", "CRR", "CS3", "CSA", "CSB", "CSE", "CTB", "CTC", "CTS", "CTY", "DFM", "DIG", "ESP", "EVG", "FIA", "FIH", "FOS", "GAC", "GAH", "GLX", "GOM", "GWM", "HAI", "HCF", "HEC", "HEH", "HEX", "HGN", "HKB", "HKE", "HKG", "HLB", "HLD", "HNP", "HSB", "ICB", "JXC", "KLE", "KSO", "LEN", "LIF", "LNK", "MEN", "MGM", "MSB", "MTA", "MTR", "NBM", "NCL", "NWD", "PAI", "PEC", "PIC", "PIN", "PLE", "POL", "RFP", "SAN", "SHK", "SMC", "SNO", "SOA", "SOH", "STC", "SUN", "SWA", "TCH", "TRF", "WHB", "WHL", "WWC", "XAB", "XBC", "XCC", "XIC", "YZC", "ZJM"]
# product_list = ["PTCD", "TBGA", "TBGO", "TBKE", "TGAB", "TGCN", "TGSB", "TLGA", "TLGO", "TLKE"]
for product in product_list:
    products = priceSession.getProducts(prodName=product, prodType=aenums.TT_PROD_OPTION)
    if len(products) == 0:
        missing_products.append(product)
    else:
        contract_counter = 0
        contracts = priceSession.getContracts(products)
        for contract in contracts:
            if contract_counter <= 1:
                pricey = None
                for enum, price in priceSession.getPrices(contract).items():
                    if "SETTL" in str(enum):
                        pricey = price.value
                    elif "LAST_TRD_PRC" in str(enum):
                        pricey = price.value
                    elif "OPEN_PRC" in str(enum):
                        pricey = price.value
                if pricey is None:
                    pricey = 100
                for i in range(0, 2):
                    side = aenums.TT_BUY
                    if i == 1:
                        side = aenums.TT_SELL
                        pricey = (cppclient.TTTick.PriceIntToInt(pricey, contract, +1))
                    orderParams = dict(order_qty=100, buy_sell=side, order_action=aenums.TT_ORDER_ACTION_ADD, limit_prc=pricey, order_type=aenums.TT_LIMIT_ORDER, tif="GTD", srs=contract, exchange_clearing_account=custDefaults.exchange_clearing_account, free_text=custDefaults.free_text, acct_type=cppclient.AEnum_Account.TT_ACCT_AGENT_1)
                    newOrder = TTAPIOrder()
                    newOrder.setFields(**orderParams)
                    orderSession.send(newOrder)
            contract_counter += 1

