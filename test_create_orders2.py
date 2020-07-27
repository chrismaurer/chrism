__author__ = "Chris"

from cumulus.utils.order import Order
from cumulus.utils.logger import logger
from cumulus.utils.marketfinder import MarketFinder
from cumulus.nimbus.utils.nimbus_driver import NimbusTest
import datetime
import calendar
import copy
import random
import requests
import ast
import time
import pyscreenshot


class OrderManagementTests(NimbusTest):
    @classmethod
    def setUpClass(cls):
        super(OrderManagementTests, cls).setUpClass()

        cls.tifs = [1, ]#, 15, 16, 17]
        # cls.tifs = [1, 2, 7]#, 15, 16, 17]
        cls.ord_qty = 1# 0.0001
        cls.fill_qty = [1, 10]

        intext = "int"
        env = "stage"
        cls.market = "TOCOM"

        pdsdomain = "int".join(["https://pds-", "-"]) if intext == "int" else "ext".join(["https://pds-", "-"])
        pds_url = env.join([pdsdomain, "-cert.trade.tt"])
        cls.base_url = pds_url

        cls.headers = {'content-type': 'application/json'}
        # cls.product_types = {"34": "FUT", "43": "MLEG", "51": "OPT", "77": "BOND", "200": "STRA", "203": "CUR"}
        cls.product_types = {"34": "FUT", }

        cls.instrs = {"1": ['LUA', '11302594805617986855', '1215'],
                      "2": ['LUZ', '8846007347493299364', '4000'],
                      "3": ['LUC', '16473594092097886368', '5000'],
                      "4": ['LUP', '12924318604365503460', '3000'],
                      "5": ['LUN', '12550962682482638548', '7000'],
                      "6": ['LUS', '17277779277941573289', '7000']}

    def setUp(self):
        super(OrderManagementTests, self).setUp()

        self.traderA.verifyLedger = False

    def tearDown(self):
        pass
        # self.cleanUpOrders()

        super(OrderManagementTests, self).tearDown()

    def setTradeablePriceAsLTP(self):
        price = self.instruments[0].getPrice("D")
        logger.step("Set LTP to {0}".format(price))
        self.traderMM.tradeAtPrice(self.instruments[0], price)

    def dateWithOffset(self, numDays=0):
        delta = datetime.datetime.today() + datetime.timedelta(numDays)
        if delta.weekday() in [5, 6]: ## date order in weekdays
           delta = datetime.datetime.today() + datetime.timedelta(numDays)
        return calendar.timegm(delta.utctimetuple()) * 1000000000

    def parse_pds_output(self, url):
        request = requests.get(url, headers=self.headers)
        output = request._content
        while ":false" in output:
            output = output.replace(":false", ":\"false\"")
        while ":true" in output:
            output = output.replace(":true", ":\"true\"")
        full_output = ast.literal_eval(output)
        try:
            output = full_output["instruments"]
        except:
            try:
                output = full_output["products"]
            except:
                try:
                    output = full_output["data"]["globalData"]["markets"]
                except:
                    try:
                        output = full_output["product"]
                    except:
                        try:
                            output = full_output["instrument"]
                        except:
                            try:
                                output = full_output["data"]["globalData"]["secExch"]
                            except:
                                try:
                                    output = full_output["records"]
                                except:
                                        output = full_output["answers"]


        return output

    def get_market_id(self, market):
        market_ids_url = self.base_url + "/api/1/systemdata?type=market"
        market_ids = self.parse_pds_output(market_ids_url)
        for market_id in market_ids:
            if market in str(market_id):
                return str(market_id["i"])
        else:
            print ("Market, \"{0}\" does not seem to exist.".format(market))


class OrdersLimitTests(OrderManagementTests):

    def test_limit_change_to_market(self):

        # instrument = MarketFinder.findEmptyInstruments(**{'count': '1', 'product': 'NK225M', 'producttype': 'FUT',
        #                                                   'market': 'OSE',
        #                                                   'instrument_id': '3544559326216540277', 'price': '22530'})[0]

        # instrument = MarketFinder.findEmptyInstruments(**{'count': '1', 'product': 'GASO', 'producttype': 'FUT',
        #                                                   'market': 'TOCOM',
        #                                                   'instrument_id': '17895660851143781838', 'price': '60000'})[0]

        # instrument = MarketFinder.findEmptyInstruments(**{'count': '1', 'product': 'CN', 'producttype': 'FUT',
        #                                                   'market': 'SGX',
        #                                                   'instrument_id': '16041635781975133655', 'price': '12000'})[0]

        # instrument = MarketFinder.findEmptyInstruments(**{'count': '1', 'product': 'CUS', 'producttype': 'FUT',
        #                                                   'market': 'HKEX',
        #                                                   'instrument_id': '368358492244337758', 'price': '6.5'})[0]

        instrument = MarketFinder.findEmptyInstruments(**{'count': '1', 'product': 'USDC/USDT', 'producttype': 'CUR',
                                                          'market': 'CoinFLEX',
                                                          'instrument_id': '18250187121216406085', 'price': '10'})[0]

        # ***********************************************************
        # logger.step("Trigger Circuit Breaker")
        # # ***********************************************************
        # tif = 1
        # order2 = Order(instrument=instrument, acct=self.traderA.accounts[0], price=80000, time_in_force=tif)
        # order3 = Order(instrument=instrument, acct=self.traderA.accounts[0], price=80000, time_in_force=tif, side=2, order_qty=9)
        # self.traderA.sendOrder(order2)
        # self.traderA.sendOrder(order3)

        # ***********************************************************
        logger.step("Submit a buy limit ioc order")
        # ***********************************************************
        # while True:
        tif = 2
        order1 = Order(instrument=instrument, acct=self.traderA.accounts[0], time_in_force=tif)
        order1.order_qty = self.ord_qty
        order1.price = instrument.getPrice("D-2")

        limit_ioc = self.traderA.sendOrder(order1)

        # ***********************************************************
        logger.step("Change the buy limit order to a market order")
        # ***********************************************************
        order1.ord_type = 1
        # order1.price = None
        self.traderA.changeOrder(order1)

    def test_two(self):

        prod_ids = ["LUA", "LUZ", "LUC", "LUP", "LUN", "LUS"]

        for prod_id in prod_ids:
            instrument = MarketFinder.findEmptyInstruments(**{'count': '1', 'product': prod_id, 'producttype': 'FUT',
                                                              'market': self.market})[0]

            # ***********************************************************
            logger.step("Submit a buy order")
            # ***********************************************************
            # while True:
            for tif in self.tifs:
                order1 = Order(instrument=instrument, acct=self.traderA.accounts[0], time_in_force=tif)
                order1.order_qty = self.ord_qty
                order1.price = instrument.getPrice("D-1")

                order2 = copy.copy(order1)
                randqty = random.randint(0, 1)
                pricey = instrument.getPrice("D+1")
                order2.price = pricey
                order2.order_qty = self.fill_qty[randqty]
                order2.side = 1

                if tif in [7, 17]:
                    offset = 0
                    while offset in range(0, 2):
                        order1.expire_date = self.dateWithOffset(offset)
                        order2.expire_date = self.dateWithOffset(offset)
                        self.traderA.sendOrderWithoutWait(order1)
                        offset += 1
                        self.traderA.sendOrderWithoutWait(order2)
                else:
                    self.traderA.sendOrderWithoutWait(order1)
                    self.traderA.sendOrderWithoutWait(order2)

    def test_three(self):

        list_of_instrument_ids = ["7284629404662656959", "6735905620185754973"]

        for instrument_id in list_of_instrument_ids:
            instrument = MarketFinder.findEmptyInstruments(**{'count': '1', 'product': 'NK', 'producttype': 'MLEG',
                                                              'market': 'SGX',
                                                              'instrument_id': instrument_id, 'price': '10'})[0]

            # ***********************************************************
            logger.step("Submit a buy order")
            # ***********************************************************
            # while True:
            for tif in self.tifs:
                order1 = Order(instrument=instrument, acct=self.traderA.accounts[0], time_in_force=tif)
                order1.order_qty = self.ord_qty
                order1.price = instrument.getPrice("D-1")

                order2 = copy.copy(order1)
                randqty = random.randint(0, 1)
                pricey = instrument.getPrice("D+1")
                order2.price = pricey
                order2.order_qty = self.fill_qty[randqty]
                order2.side = 1

                if tif in [7, 17]:
                    offset = 0
                    while offset in range(0, 2):
                        order1.expire_date = self.dateWithOffset(offset)
                        order2.expire_date = self.dateWithOffset(offset)
                        self.traderA.sendOrderWithoutWait(order1)
                        offset += 1
                        self.traderA.sendOrderWithoutWait(order2)
                else:
                    self.traderA.sendOrderWithoutWait(order1)
                    self.traderA.sendOrderWithoutWait(order2)

    def test_four(self):

        # list_of_instrument_ids = ["6144993593498678090", "6268349978426710672"]
        #
        # for instrument_id in list_of_instrument_ids:
        instrument = MarketFinder.findEmptyInstruments(**{'count': '1', 'product': 'NK225', 'producttype': 'FUT',
                                                          'market': 'OSE',
                                                          'instrument_id': '16464418280204365135', 'price': '19600'})[0]

        # ***********************************************************
        logger.step("Submit a buy order")
        # ***********************************************************
        # while True:
        tif = 1
        parties = [{"party_id": "0", "party_role": 90}, {"party_id": "CRZ", "party_role": 6}, {"party_id": "MAU", "party_role": 88}]
        for q in range(0, 1):
            order1 = Order(instrument=instrument, acct=self.traderA.accounts[0], time_in_force=tif)
            order1.order_qty = self.ord_qty
            order1.price = instrument.getPrice("D")
            order1.updateParties(parties)

            self.traderA.sendOrder(order1)
            q += 1

    def test_five(self):

        instruments = MarketFinder.findEmptyInstruments(**self.testDefaults.instruments[0])
        instrument = instruments[0]

        # ***********************************************************
        logger.step("Create a sell order")
        # ***********************************************************
        # while True:
        # for tif in self.tifs:
        tif = 2
        qty = 0.0005
        order1 = Order(instrument=instrument, acct=self.traderMM.accounts[0], time_in_force=tif, side=2)
        order1.order_qty = float(qty)
        order1.price = 82
        self.traderA.sendOrder(order1)

        # ***********************************************************
        logger.step("Create a buy order to cross the sell")
        # ***********************************************************
        qty = 0.0003
        order2 = Order(instrument=instrument, acct=self.traderMM.accounts[0], time_in_force=tif, side=1)
        order2.order_qty = float(qty)
        order2.price = 81
        self.traderA.sendOrder(order2)

        # ***********************************************************
        logger.step("Delete the remaining partially-filled sell order")
        # ***********************************************************
        self.traderA.deleteOrder(order1)

        time.sleep(0.85)
        # qty += 0.0001

    def test_orders_on_all_instruments(self):

        number_of_instruments_per_product = 1

        for product_type in self.product_types:
            products_url = self.base_url + "/api/1/products?marketIds=" + self.get_market_id(self.market) + "&productTypeIds=" + product_type
            print products_url
            products = self.parse_pds_output(products_url)
            prod_type = self.product_types[product_type]

            for product in products:
                prod_url = self.base_url + "/api/1/products/" + str(product["i"]) + "?slim=false"
                prod = self.parse_pds_output(prod_url)
                instr_list_url = self.base_url + "/api/1/instruments?productIds=" + str(prod["i"])
                instrument_list = self.parse_pds_output(instr_list_url)
                instr_counter = 1000
                for instrument_object in instrument_list:

                    # ins = {}
                    # ins["instrumentId"] = instrument_object["i"]
                    # ins["marketId"] = instrument_object["m"]
                    # ins["securityType"] = instrument_object["pt"]
                    # # self.instrument = ins
                    # initialTradeData = self.traderA.getTradeData(ins)

                    if self.market == "KRX":
                        if any(prod in instrument_object["a"] for prod in ["K2I", "K2F"]):
                            if prod_type == "FUT":
                                pricey = 286
                            elif prod_type == "OPT":
                                pricey = 33
                            else:
                                pricey = -25
                        elif "MKI" in instrument_object["a"]:
                            if prod_type == "FUT":
                                pricey = 275
                            elif prod_type == "OPT":
                                pricey = 33
                            else:
                                pricey = -2
                        elif "KQI" in instrument_object["a"]:
                            if prod_type == "FUT":
                                pricey = 1170
                            elif prod_type == "OPT":
                                pricey = 33
                            else:
                                pricey = -25
                        elif "XI3" in instrument_object["a"]:
                            if prod_type == "FUT":
                                pricey = 1400
                            elif prod_type == "OPT":
                                pricey = 33
                            else:
                                pricey = -25
                        else:
                            if prod_type == "FUT":
                                pricey = 1118
                            elif prod_type == "OPT":
                                pricey = 32
                            else:
                                # pricey = -25  # KRX
                                pricey = -5
                    else:
                        if prod_type == "FUT":
                            pricey = 300
                        elif prod_type == "OPT":
                            pricey = 35
                        else:
                            pricey = 85
                    try:
                        instrument = MarketFinder.findEmptyInstruments(**{'count': '1',
                                                                          'producttype': prod_type,
                                                                          'market': self.market,
                                                                          'instrument_id': str(instrument_object["i"]),
                                                                          'price': str(pricey)})[0]
                        initialTradeData = self.traderA.getTradeData(instrument)
                        print instrument

                        # order1 = Order(instrument=instrument, acct=self.traderA.accounts[0], time_in_force=1)
                        # order1.order_qty = self.ord_qty
                        # order1.price = instrument.getPrice("D") if initialTradeData["settle"] is None else initialTradeData["settle"]
                        #
                        # order2 = Order(instrument=instrument, acct=self.traderA.accounts[0], time_in_force=1)
                        # order2.order_qty = self.ord_qty
                        # order2.side = 2
                        # order2.price = instrument.getPrice("D") if initialTradeData["settle"] is None else initialTradeData["settle"]
                        #
                        # self.traderA.sendOrderWithoutWait(order1)
                        # # self.traderA.sendOrderWithoutWait(order2)
                    except:
                        pass
                    if instr_counter == number_of_instruments_per_product:
                        break
                    else:
                        instr_counter += 1

    def test_orders_on_all_markets(self):

        target_prods = {'ASX': ['BB', 'IR'],
                        'B3': ['DAP', 'OC1'],
                        'CFE': ['VX', 'VXT'],
                        'Eurex': ['FGBL', 'FGBM'],
                        'Euronext': ['jFCE', ],
                        'ICE': ['BRN', 'EC'],
                        'ICE_L': ['I', 'L'],
                        'IDEM': ['FIB', 'MINI', 'MIBO', 'FCAP', 'PRY', 'ISP', 'US'],
                        'LSE': ['TLKOD', 'OSX', 'OSEBX', 'FI100', 'OBOSX'],
                        'MEFF': ['A3M', 'FIE', 'FIEM'],
                        'TFX': ['EY', ],
                        'TFEX': ['GF10', 'GF50', 'BANK']}

        number_of_instruments_per_product = 1

        market_ids_url = self.base_url + "/api/1/systemdata?type=market"
        market_ids = self.parse_pds_output(market_ids_url)
        all_markets = [market_ids[m_id]['n'] for m_id in range(len(market_ids))]

        for mkt in all_markets:
            tiffy = 2 if mkt =="CoinFLEX" else 1
            if mkt in ("Coinbase", ):
                self.product_types = {"203": "CUR", }
            elif mkt in ("KCG", "NFI"):
                self.product_types = {"77": "BOND", }
            else:
                self.product_types = {"34": "FUT", }
            prod_list = target_prods[mkt] if mkt in target_prods else []
            if "_DEV" not in mkt and "_Dev" not in mkt:
                self.market = mkt

                for product_type in self.product_types:
                    if len(prod_list) > 0:
                        products_url = self.base_url + "/api/1/productsearch?query=" + prod_list[0] + "&marketIds=" + self.get_market_id(self.market) + "&productTypeIds=" + product_type
                    else:
                        products_url = self.base_url + "/api/1/products?marketIds=" + self.get_market_id(self.market) + "&productTypeIds=" + product_type
                    print products_url
                    products = self.parse_pds_output(products_url)
                    prod_type = self.product_types[product_type]

                    for product in products:
                        prod_url = self.base_url + "/api/1/products/" + str(product["i"]) + "?slim=false"
                        prod = self.parse_pds_output(prod_url)
                        instr_list_url = self.base_url + "/api/1/instruments?productIds=" + str(prod["i"])
                        instrument_list = self.parse_pds_output(instr_list_url)
                        instr_counter = 0
                        for instrument_object in instrument_list:

                            if instr_counter != 0:

                                if prod_type == "FUT":
                                    pricey = 300 if self.market in ("SGX", "NDAQ_EU") else 98
                                elif prod_type == "OPT":
                                    pricey = 35
                                else:
                                    pricey = 85
                                try:
                                    # instrument = MarketFinder.findEmptyInstruments(**{'count': '1',
                                    #                                                   'producttype': prod_type,
                                    #                                                   'market': self.market,
                                    #                                                   'product': prod['s']})[0]
                                    instrument = MarketFinder.findEmptyInstruments(**{'count': '1',
                                                                                      'producttype': prod_type,
                                                                                      'market': self.market,
                                                                                      'instrument_id': str(instrument_object["i"]),
                                                                                      'price': str(pricey)})[0]
                                    initialTradeData = self.traderA.getTradeData(instrument)

                                    order1 = Order(instrument=instrument, acct=self.traderA.accounts[0], time_in_force=tiffy)
                                    order1.order_qty = self.ord_qty
                                    if "203" in self.product_types:
                                        order1.time_in_force = 2
                                    order1.price = instrument.getPrice("D") if initialTradeData["settle"] is None or int(initialTradeData["settle"]) == 0 else initialTradeData["settle"]

                                    order2 = Order(instrument=instrument, acct=self.traderA.accounts[0], time_in_force=tiffy)
                                    order2.order_qty = self.ord_qty
                                    order2.side = 2
                                    order2.price = instrument.getPrice("D") if initialTradeData["settle"] is None or int(initialTradeData["settle"]) == 0 else initialTradeData["settle"]

                                    self.traderA.sendOrderWithoutWait(order1)
                                    # self.traderA.sendOrderWithoutWait(order2)
                                except:
                                    pass
                            if instr_counter == number_of_instruments_per_product:
                                break
                            else:
                                instr_counter += 1
                        break

    def test_create_lots_of_orders(self):

        instruments = MarketFinder.findEmptyInstruments(**self.testDefaults.instruments[0])
        instrument = instruments[0]

        # ***********************************************************
        logger.step("Submit a buy order")
        # ***********************************************************
        q = 1
        while q in range(0, 400):
            order1 = Order(instrument=instrument, acct=self.traderA.accounts[0])
            order1.order_qty = self.ord_qty
            order1.price = instrument.getPrice("D")
            self.traderA.sendOrderWithoutWait(order1)
            q += 1
            time.sleep(0.15)

    def test_create_orders_on_lots_of_accounts(self):

        instruments = MarketFinder.findEmptyInstruments(**self.testDefaults.instruments[0])
        instrument = instruments[0]

        while True:
            # ***********************************************************
            logger.step("Submit a buy order")
            # ***********************************************************
            q = 0
            while q in range(0, len(self.traderA.accounts)):
                order1 = Order(instrument=instrument, acct=self.traderA.accounts[q])
                order1.order_qty = self.ord_qty
                order1.price = instrument.getPrice("D")
                self.traderA.sendOrderWithoutWait(order1)
                q += 1
                time.sleep(0.15)
            print "STINK!"

    def test_order_add_delete(self):

        instruments = MarketFinder.findEmptyInstruments(**self.testDefaults.instruments[0])
        instrument = instruments[0]

        q = 1
        while q in range(0, 2):

            # ***********************************************************
            logger.step("Submit one order one each side of the market")
            # ***********************************************************
            order1 = Order(instrument=instrument, acct=self.traderA.accounts[0])
            order1.order_qty = self.ord_qty
            order1.price = instrument.getPrice("D")
            order2 = Order(instrument=instrument, acct=self.traderA.accounts[0], side=2)
            order2.order_qty = self.ord_qty
            order2.price = instrument.getPrice("D+1")
            self.traderA.sendOrder(order1)
            self.traderA.sendOrder(order2)

            # ***********************************************************
            logger.step("Delete the orders")
            # ***********************************************************
            self.traderA.deleteOrder(order1)
            self.traderA.deleteOrder(order2)

            self.traderA.removeOrderFromDeletedRejectedList(order1)
            self.traderA.removeOrderFromDeletedRejectedList(order2)

            q += 1
            time.sleep(0.1)
            if q == 2:
                time.sleep(5000)

    def test_instrument_states(self):

        testtimes ={"07:00:0": "ONLINE",
                    "08:00:0": "M_PRE_OPEN_NO_J-NET",
                    "08:20:0": "M_PRE_OPEN",
                    "08:44:0": "M_PRE_OPEN_NCP",
                    "08:45:0": "M_ZARABA",
                    "08:53:0": "TEST",
                    "09:00:0": "M_ZARABA",
                    "11:00:0": "A_ZARABA_E",
                    "11:02:0": "A_ZARABA_E",
                    "11:02:3": "A_ZARABA_E",
                    "11:07:0": "A_ZARABA_E",
                    "11:10:0": "A_ZARABA_E",
                    "11:30:0": "A_ZARABA_E",
                    "11:35:0": "A_ZARABA_E",
                    "11:35:3": "A_ZARABA_E",
                    "11:40:0": "A_ZARABA_E",
                    "12:05:0": "A_ZARABA_E",
                    "12:30:0": "A_ZARABA_E",
                    "15:00:0": "A_ZARABA_E",
                    "15:02:0": "A_ZARABA_E",
                    "15:02:3": "A_ZARABA_E",
                    "15:07:0": "A_ZARABA_E",
                    "15:07:3": "A_ZARABA_E",
                    "15:10:0": "A_PRE_CLOSE",
                    "15:12:3": "A_PRE_CLOSE",
                    "15:15:0": "A_AUCTION_CLOSING",
                    "15:15:3": "A_AUCTION_CLOSING2",
                    "15:18:0": "A_AUCTION_CLOSING2",
                    "15:20:0": "A_AUCTION_END",
                    "15:20:3": "A_CALC_SP",
                    "15:23:0": "A_CALC_SP",
                    "15:25:0": "A_COLLECT_TRADE",
                    "15:30:0": "A_COLLECT_TRADE",
                    "15:38:0": "A_CALC_SP",
                    "15:41:0": "A_COLLECT_TRADE",
                    "16:00:0": "J-NET_END",
                    "16:03:0": "DAY_END",
                    "16:13:0": "Order_Remove",
                    "16:15:0": "N_PRE_OPEN",
                    "16:29:0": "N_PRE_OPEN_NCP",
                    "16:30:0": "N_ZARABA",
                    "18:55:0": "N_ZARABA",
                    "18:59:0": "N_ZARABA",
                    "19:00:0": "N_ZARABA",
                    "19:00:3": "N_ZARABA",
                    "19:05:0": "N_ZARABA",
                    "05:25:0": "N_PRE_CLOSE",
                    "05:29:0": "N_PRE_CLOSE_NCP",
                    "05:30:0": "N_AUCTION_CLOSING",
                    "05:30:3": "N_AUCTION_CLOSING2",
                    "05:35:0": "N_AUCTION_END",
                    "05:40:0": "N_CLOSE",
                    "05:45:0": "CLOSE",
                    "06:00:0": "OFFLINE"}

        instruments = MarketFinder.findEmptyInstruments(**self.testDefaults.instruments[0])
        instrument = instruments[0]

        while True:
            timenow = []
            for elem in time.localtime()[3:5]:
                timenow.append(str("%02d" % elem))

            sec = list(str(time.localtime()[5]))[0]
            seconds = "0" if time.localtime()[5] < 10 else sec
            timenow.append(seconds)

            check_testtime = ":".join(timenow)

            if check_testtime in testtimes:

                try:
                    # ***********************************************************
                    logger.step("Order Add")
                    # ***********************************************************
                    order1 = Order(instrument=instrument, acct=self.traderA.accounts[0], order_qty=10)
                    order1.price = instrument.getPrice("D")
                    self.traderA.sendOrder(order1, verifyBookie=False)
                except:
                    pass

                try:
                    # ***********************************************************
                    logger.step("Order Modify Prc, Qty Increase")
                    # ***********************************************************
                    order1.price = instrument.tickUp(order1.price, 2)
                    order1.order_qty = 15
                    self.traderA.changeOrder(order1, verifyBookie=False)
                except:
                    pass

                try:
                    # ***********************************************************
                    logger.step("Order Modify Prc, Qty Decrease")
                    # ***********************************************************
                    order1.price = instrument.tickDown(order1.price, 2)
                    order1.order_qty = 10
                    self.traderA.changeOrder(order1, verifyBookie=False)
                except:
                    pass

                try:
                    # ***********************************************************
                    logger.step("Order Cancel")
                    # ***********************************************************
                    self.traderA.deleteOrder(order1)
                except:
                    pass

                # ***********************************************************
                logger.step("Order Match")
                # ***********************************************************
                order1 = Order(instrument=instrument, acct=self.traderA.accounts[0])
                order1.order_qty = 1
                order1.price = instrument.getPrice("D")
                order2 = Order(instrument=instrument, acct=self.traderA.accounts[0], side=2)
                order2.order_qty = 1
                order2.price = instrument.getPrice("D")
                self.traderA.sendOrderWithoutWait(order1)
                self.traderA.sendOrderWithoutWait(order2)

                time_list = []
                for elem in time.localtime()[:6]:
                    time_list.append(str(elem))
                time.sleep(2)
                im = pyscreenshot.grab((1, 10, 1080, 1280))
                im.save(r"/Users/cmaurer/instrument_states_test/" + "-".join(time_list) + "_" + testtimes[check_testtime] + ".png")

            else:
                time.sleep(2)

    def test_create_orders_at_all_prices(self):

        instruments = MarketFinder.findEmptyInstruments(**self.testDefaults.instruments[0])
        instrument = instruments[0]

        aaa = 1
        while aaa <= 30:
            # ***********************************************************
            logger.step("Submit a buy order")
            # ***********************************************************
            target_number_of_orders = 100 / instrument.ticksize
            order_count = 1
            order_price = instrument.getPrice("D")
            while order_count in range(0, int(target_number_of_orders) + 1):
                order_price = instrument.tickDown(order_price, 1)
                order1 = Order(instrument=instrument, acct=self.traderA.accounts[0])
                order1.order_qty = self.ord_qty
                order1.price = order_price
                self.traderA.sendOrder(order1)
                order_count += 1
            aaa += 1

    def test_setup_pnl_orders(self):

        for instr in self.instrs:

            product = self.instrs[instr][0]
            instrument_id = self.instrs[instr][1]
            price = self.instrs[instr][2]

            print "product, instrument_id, price =", product, instrument_id, price

            instrument = MarketFinder.findEmptyInstruments(**{'count': '1', 'product': product, 'producttype': 'FUT',
                                                              'market': 'HKEX',
                                                              'instrument_id': instrument_id, 'price': price})[0]

            # ***********************************************************
            logger.step("Submit a {0} buy order".format(instr))
            # ***********************************************************
            for tif in self.tifs:
                order1 = Order(instrument=instrument, acct=self.traderA.accounts[0], time_in_force=tif)
                order2 = Order(instrument=instrument, acct=self.traderA.accounts[0], time_in_force=tif, side=2)

                order1.order_qty = self.ord_qty
                order1.price = instrument.getPrice("D")
                order2.order_qty = self.ord_qty
                order2.price = instrument.getPrice("D+1")
                if tif in [7, 17]:
                    offset = 0
                    while offset in range(0, 2):
                        order1.expire_date = self.dateWithOffset(offset)
                        self.traderA.sendOrder(order1)
                        order2.expire_date = self.dateWithOffset(offset)
                        self.traderA.sendOrder(order2)
                        offset += 1
                else:
                    self.traderA.sendOrder(order1)
                    self.traderA.sendOrder(order2)
