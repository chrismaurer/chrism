import logging
import time

from ttapi import aenums
from ttapi import cppclient

from pyrate import predicates
from pyrate.ttapi.order import TTAPIOrder
from pyrate.builder import Builder
from pyrate.gateway import Gateway
from pyrate.ttapi.testing import TestCase

from nose.tools import assert_equal
from nose.tools import assert_true
from nose.tools import assert_not_equal

from tests.sgx_org.order_server import utils
from tests.sgx_org.order_server.utils import callbackMapping

log = logging.getLogger(__name__)

AddCallbacks = callbackMapping['add'] 
ChangeCallbacks = callbackMapping['change']
DeleteCallbacks = callbackMapping['delete']
ReplaceCallbacks = callbackMapping['replace']
InquireCallbacks = callbackMapping['inquire']
UpdateCallbacks = callbackMapping['update']
PartialFillCallbacks = callbackMapping['partialfill']
#FullFillCallbacks= callbackMapping['fullfill']
IOCPartialFillCallbacks = callbackMapping['iocpartialfill']
RejectCallbacks = callbackMapping['reject']
s = 2

class TestSGXOrdersSmokeFUT(TestCase):
    
    def setUp(self):
        log.info(' BEGIN '.center(80, '='))
        TestCase.tearDown(self)
        
    def tearDown(self):
        time.sleep(1)
        TestCase.tearDown(self)
        log.info(' END '.center(80, '='))
    
    @classmethod
    def setUpClass(cls):
        cls._trader = Builder().testenv.exchTraders[0]
        cls._custDefaults = Builder().testenv.customers[0]
        
        # Finding a future contract        
        findContractsAndPrices = Builder().testenv.marketFinder.findContractsAndPrices
        contracts, prices = findContractsAndPrices(prodTypes=[aenums.TT_PROD_FSPREAD], depth=2)
        cls._contract = contracts[0]
        prices = prices[contracts[0].seriesKey]
        cls._price = prices[0]
        log.info('Smoke test will be run on future %s at price is %s' % (cls._contract.seriesName, cls._price))
        cls.os = Builder().testenv.gateway.orderServer
        cls._numOfExpectedFills = 2
        
    def testGTD_NoRestr(self):
        
        log.info('Starting GTD_NoRestr')
        
        self.step1()
        self.step2()
        self.step3()
        
    def testGTD_FOK(self):
        
        log.info('Starting GTD_FOK')
        
        self.step4()
        self.step5()
        self.step6()
        
    def testGTD_ICE(self):
        
        log.info('Starting GTD_ICE')
        
        self.step7()
        self.step8()
        self.step9()
        
    def testGTD_IOC(self):
        
        log.info('Starting GTD_IOC')
        
        self.step10()
        self.step11()
        self.step12()

    def testGTD_MOC(self):

        log.info('Starting GTD_MOC')

        self.step13()

    def testGTD_MOO(self):

        log.info('Starting GTD_MOO')

        self.step14()

    def testGTD_LOC(self):

        log.info('Starting GTD_LOC')

        self.step15()

    def testGTD_LOO(self):

        log.info('Starting GTD_LOO')

        self.step16()

    def testGTD_STOP(self):

        log.info('Starting GTD_STOP')

        self.step17()
        self.step18()
        self.step19()

    def testAAGTD_TSTOP(self):

        log.info('Starting GTD_TSTOP')

        self.step20()
        self.step21()
        self.step22()

    def testGTC_NORESTR(self):

        log.info('Starting GTC_NORESTR')

        self.step23()
        self.step24()
        self.step25()

    def testGTC_FOK(self):

        log.info('Starting GTC_FOK')

        self.step26()
        self.step27()
        self.step28()

    def testGTC_ICE(self):

        log.info('Starting GTC_ICE')

        self.step29()
        self.step30()
        self.step31()

    def testGTC_IOC(self):

        log.info('Starting GTC_IOC')

        self.step32()
        self.step33()
        self.step34()

    def testGTC_MOC(self):

        log.info('Starting GTC_MOC')

        self.step35()

    def testGTC_MOO(self):

        log.info('Starting GTC_MOO')

        self.step36()

    def testGTC_LOC(self):

        log.info('Starting GTC_LOC')

        self.step37()

    def testGTC_LOO(self):

        log.info('Starting GTC_LOO')

        self.step38()

    def testGTC_STOP(self):

        log.info('Starting GTC_STOP')

        self.step39()
        self.step40()
        self.step41()

    def testGTC_TSTOP(self):

        log.info('Starting GTC_TSTOP')

        self.step42()
        self.step43()
        self.step44()

    def purgeCallbackList(self):        
        Builder().testenv.gateway.pipe.output.clear()

    def sendAndValidate(self, order, orderCallBacks, actionToValidate=None, restingOrder=None, restingOrderCallBacks=None, restingOrderActionToValidate=None, numOfFillCallBacks=None):        
        order.populateTraderDetails(self._trader)
        order.populateCustomerDetails(self._custDefaults)
        retVal = self.orderServer().sendAndWait(order, orderCallBacks)
        assert_equal(retVal[0], "SUCCESS")
        
        actionAck = None
        if actionToValidate is not None:
            actionAck = retVal[1][actionToValidate]                
            #assert_equal(self.validateChangeInstance.validate(order, orderAck), True, "Validation Failed!!!")

        oppositeActionAck = None
        if restingOrder is not None and restingOrderCallBacks is not None:
            pred = predicates.createOrderPredicates(restingOrderCallBacks, restingOrder.site_order_key)
            status, msg = self.orderServer().wait(pred)
            assert_equal(status, "SUCCESS", "Callback status check failed!!")
           
            if restingOrderActionToValidate is not None:
                oppositeActionAck = msg[restingOrderActionToValidate]                
                #assert_equal(self.validateChangeInstance.validate(order, oppositeActionAck), True, "Validation Failed!!!")
            
        if numOfFillCallBacks is not None and numOfFillCallBacks is not 0:
            status, msg = Builder().testenv.gateway.fillServer.wait(["OnFillRecord"]*numOfFillCallBacks)
            assert_equal(status, "SUCCESS", "Callback status check failed!!")
        
        self.purgeCallbackList()
        
        if actionAck is not None and oppositeActionAck is not None:
            return Order(actionAck[0]), Order(oppositeActionAck[0])
        elif actionAck is not None:
            return Order(actionAck[0])
        
    def sendAndValidateReject(self, order, orderCallBacks = RejectCallbacks, neverGetCallbacks='OnOrderTableAdd'):                            
        retVal = self.orderServer().sendAndWait(order, orderCallBacks)
        assert_equal(retVal[0], "SUCCESS")
        orderStatus = retVal[1]['OnOrderStatus']        
        assert_true(len(orderStatus[0].msgTxt) > 0)
        assert_equal(orderStatus[0].routed.order_status, aenums.TT_ORDER_STATUS_REJECTED)
                
        pred = predicates.createOrderPredicates(neverGetCallbacks, order.site_order_key)        
        status = Builder().testenv.gateway.orderServer._cbkPipe.never_got(pred,5)
        assert_equal(status[0], "TIMEOUT")
        self.purgeCallbackList()   
        
        
    def del_orderbook(self):
        log.info('Deleting orderbook')
        #This function is frequently used right after order entry, so add a little time for SGX latency.
        #time.sleep(s)
         #Check that no orders exist            
        self.os.deleteMyOrders()
        #give us a couple of seconds to execute and clear the deletes
        time.sleep(s)
        for o in self.os.myOpenOrders():
            assert_not_equal(type(o), cppclient.Order)
        
        
    def orderServer(self):
        return Builder().testenv.gateway.orderServer  
    
    def step1(self):
        #Used in testGTD_NoRestr
        
        log.info('Entering a GTD NO_RESTR NOFILL BUY order')
        
        self._GTDbuy = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDbuy.setAction('Add')
        self._GTDbuy = self.sendAndValidate(self._GTDbuy, AddCallbacks, 'OnOrderTableAdd')
        
        log.info('Entering a GTD NO_RESTR NOFILL SELL order')
        
        self._tickup = cppclient.TTTick.PriceIntToInt(self._price, self._contract, 1)   
        self._GTDsell = Order(order_qty=50, limit_prc=self._tickup, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDsell.setAction('Add')
        self._GTDsell = self.sendAndValidate(self._GTDsell, AddCallbacks, 'OnOrderTableAdd')
        
        time.sleep(1)
        
        self.del_orderbook()
        
        
    def step2(self):
        #Used in testGTD_NoRestr
        
        log.info('Entering a GTD NO_RESTR FULLFILL BUY')
        
        self._GTDffillbuy = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDffillbuy.setAction('Add')
        self._GTDffillbuy = self.sendAndValidate(self._GTDffillbuy, AddCallbacks, 'OnOrderTableAdd')
        
        #time.sleep(1)
        
        log.info('Entering an opposing SELL order to fullfill the GTD NO_RESTR FULLFILL BUY')
        
        self._GTDfill = Order(order_qty =50, limit_prc=self._price, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDfill.setAction('Add')
        self._GTDfill = self.sendAndValidate(self._GTDfill, AddCallbacks+FullFillCallbacks, 'OnOrderTableAdd', self._GTDffillbuy, FullFillCallbacks, 'OnOrderTableDelete', self._numOfExpectedFills)
        self._GTDfill = None
        
        log.info('Entering a GTD NO_RESTR FULLFILL SELL')
        
        self._GTDffillsell = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDffillsell.setAction('Add')
        self._GTDffillsell = self.sendAndValidate(self._GTDffillsell, AddCallbacks, 'OnOrderTableAdd')
        
        #time.sleep(1)
        
        log.info('Entering an opposing BUY order to fullfill the GTD NO_RESTR FULLFILL SELL')
        
        self._tickup = cppclient.TTTick.PriceIntToInt(self._price, self._contract, 1) 
        self._GTDfill = Order(order_qty=50, limit_prc=self._tickup, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDfill.setAction('Add')
        self._GTDfill = self.sendAndValidate(self._GTDfill, AddCallbacks+FullFillCallbacks, 'OnOrderTableAdd', self._GTDffillsell, FullFillCallbacks, 'OnOrderTableDelete', self._numOfExpectedFills)
        
        time.sleep(1)
        
        self.del_orderbook()
        self._GTDfill = None
        
    def step3(self):
        #Used in testGTD_NoRestr
        
        log.info('Entering a GTD NO_RESTR PARTIALFILL BUY')
        
        self._GTDpartialbuy = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDpartialbuy.setAction('Add')
        self._GTDpartialbuy = self.sendAndValidate(self._GTDpartialbuy, AddCallbacks, 'OnOrderTableAdd')
        
        #time.sleep(1)
        
        log.info('Entering an opposing SELL order to partially fill the above BUY order')
        
        self._GTDfill = Order(order_qty=10, limit_prc=self._price, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDfill.setAction('Add')
        self._GTDfill = self.sendAndValidate(self._GTDfill, AddCallbacks+FullFillCallbacks, "OnOrderTableAdd", \
                                                                  self._GTDpartialbuy, PartialFillCallbacks, "OnOrderTableUpdate", self._numOfExpectedFills)
        
        self._GTDfill = None
        
        log.info('Entering a GTD NO_RESTR PARTIALFILL SELL')
        
        self._tickup = cppclient.TTTick.PriceIntToInt(self._price, self._contract, 1) 
        self._GTDpartialsell = Order(order_qty=50, limit_prc=self._tickup, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDpartialsell.setAction('Add')
        self._GTDpartialsell = self.sendAndValidate(self._GTDpartialsell, AddCallbacks, 'OnOrderTableAdd')
        
       # time.sleep(1)
        
        log.info('Entering an opposing BUY order to partially fill the above SELL order')
        
        self._GTDfill = Order(order_qty=10, limit_prc=self._tickup, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDfill.setAction('Add')
        self._GTDfill = self.sendAndValidate(self._GTDfill, AddCallbacks+FullFillCallbacks, 'OnOrderTableAdd', \
                                             self._GTDpartialsell, PartialFillCallbacks, 'OnOrderTableUpdate', self._numOfExpectedFills)
        time.sleep(1)
        
        self.del_orderbook()
        self._GTDfill = None
        
    def step4(self):
        #Used in testGTD_FOK
        
        log.info('Entering a GTD FOK NOFILL BUY')
        
        self._GTDfokbuy = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_FOK_ORDER_RES, srs=self._contract)
        self._GTDfokbuy.setAction('Add') 
        self._GTDfok = self.sendAndValidate(self._GTDfokbuy, RejectCallbacks)
        
        time.sleep(1)
        
        log.info('Entering a GTD FOK NOFILL SELL')
        
        self._GTDfoksell = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_FOK_ORDER_RES, srs=self._contract)
        self._GTDfoksell.setAction('Add')
        self.sendAndValidate(self._GTDfoksell, RejectCallbacks)
        
        #time.sleep(1)
        
        self.del_orderbook()
        
        
    def step5(self):
        #Used in testGTD_FOK
        
        log.info('Entering an opposing SELL order for the following GTD FOK FULLFILL BUY')
        
        self._GTDfill = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDfill.setAction('Add')
        self.sendAndValidate(self._GTDfill, AddCallbacks, 'OnOrderTableAdd')
        
        #time.sleep(1)
        
        log.info('Entering a GTD FOK FULLFILL BUY')
        
        time.sleep(1)
        
        GTDfokfullbuy = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_FOK_ORDER_RES, srs=self._contract)
        GTDfokfullbuy.setAction('Add')
        self.sendAndValidate(GTDfokfullbuy, AddCallbacks+FullFillCallbacks, 'OnOrderTableDelete', \
                                                   self._GTDfill, FullFillCallbacks, 'OnOrderTableDelete', self._numOfExpectedFills)
        
        #time.sleep(2)
        
        self._GTDfill = None
        self.del_orderbook()
        
        log.info('Entering an opposing BUY order for the GTD FOK FULLFILL SELL')
        
        self._GTDfill = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDfill.setAction('Add')
        self.sendAndValidate(self._GTDfill, AddCallbacks, 'OnOrderTableAdd')
        
        log.info('Entering a GTD FOK FULLFILL SELL')
        
        time.sleep(1)
        
        self._GTDfokfullsell = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_FOK_ORDER_RES, srs=self._contract)
        self._GTDfokfullsell.setAction('Add')
        self.sendAndValidate(self._GTDfokfullsell, AddCallbacks+FullFillCallbacks, 'OnOrderTableAdd', \
                                                    self._GTDfill, FullFillCallbacks, 'OnOrderTableDelete', self._numOfExpectedFills)
        
        #time.sleep(2)
        
        self._GTDfill = None
        self.del_orderbook()
        
    def step6(self):
        #Used in testGTD_FOK
        
        log.info('Entering an opposing SELL order for the GTD FOK PARTIALFILL BUY')
        
        self._GTDfill = Order(order_qty=20, limit_prc=self._price, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDfill.setAction('Add')
        self.sendAndValidate(self._GTDfill, AddCallbacks, 'OnOrderTableAdd')
        
        time.sleep(1)
        
        log.info('Entering a GTD FOK PARTIALFILL BUY')
        
        self._GTDfokpartialbuy = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_FOK_ORDER_RES, srs=self._contract)
        self._GTDfokpartialbuy.setAction('Add')
        
        self.sendAndValidate(self._GTDfokpartialbuy, RejectCallbacks)
        
        #time.sleep(2)
        
        self.del_orderbook()
        self._GTDfill = None
        
        log.info('Entering an opposing BUY order for the GTD FOK PARTIALFILL SELL')
        
        self._GTDfill = Order(order_qty=20, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDfill.setAction('Add')
        self.sendAndValidate(self._GTDfill, AddCallbacks, 'OnOrderTableAdd')
        
        time.sleep(1)
        
        log.info('Entering a GTD FOK PARTIALFILL SELL')
        
        self._GTDfokpartialsell = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_FOK_ORDER_RES, srs=self._contract)
        self._GTDfokpartialsell.setAction('Add')
        
        self.sendAndValidate(self._GTDfokpartialsell, RejectCallbacks)
        
        #time.sleep(2)
        
        self.del_orderbook()
        self._GTDfill = None
        
    def step7(self):
        #Used in testGTD_ICE
        
        log.info('Entering a GTD ICEBERG NOFILL BUY')
        
        self._GTDicebuy = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_ICEBERG_ORDER_RES, disclosed_qty=20, srs=self._contract)
        self._GTDicebuy.setAction('Add')
        self.sendAndValidate(self._GTDicebuy, AddCallbacks, 'OnOrderTableAdd')
        
        log.info('Entering a GTD ICEBERG NOFILL SELL')
        
        self._tickup = cppclient.TTTick.PriceIntToInt(self._price, self._contract, 1) 
        self._GTDicesell = Order(order_qty=50, limit_prc=self._tickup, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_ICEBERG_ORDER_RES, disclosed_qty=20, srs=self._contract)
        self._GTDicesell.setAction('Add')
        self.sendAndValidate(self._GTDicesell, AddCallbacks, 'OnOrderTableAdd')
        
        self.del_orderbook()
        
    def step8(self):
        #Used in testGTD_ICE
        
        log.info('Entering a GTD BUY to fill the following GTD ICEBERG FULLFILL SELL')
        
        self._GTDfill = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDfill.setAction('Add')
        self.sendAndValidate(self._GTDfill, AddCallbacks, 'OnOrderTableAdd')
        
        log.info('Entering a GTD ICEBERG FULLFILL SELL')
        
        self._GTDicefullsell = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_ICEBERG_ORDER_RES, disclosed_qty=20, srs=self._contract)
        self._GTDicefullsell.setAction('Add')
        self.sendAndValidate(self._GTDicefullsell, AddCallbacks+FullFillCallbacks, 'OnOrderTableAdd', self._GTDfill, FullFillCallbacks, 'OnOrderTableDelete', self._numOfExpectedFills)
        
        self._GTDfill = None
        
        log.info('Entering a GTD SELL to fill the following GTD ICEBERG FULLFILL BUY')
        
        self._GTDfill = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDfill.setAction('Add')
        self.sendAndValidate(self._GTDfill, AddCallbacks, 'OnOrderTableAdd')
        
        log.info('Entering a GTD ICEBERG FULLFILL BUY')
        
        self._GTDicefullbuy = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_ICEBERG_ORDER_RES, disclosed_qty=20, srs=self._contract)
        self._GTDicefullbuy.setAction('Add')
        self.sendAndValidate(self._GTDicefullbuy, AddCallbacks+FullFillCallbacks, 'OnOrderTableAdd', self._GTDfill, FullFillCallbacks, 'OnOrderTableDelete', self._numOfExpectedFills)
        
        self.del_orderbook()
        self._GTDfill = None
        
    def step9(self):
        #Used in testGTD_ICE
        
        log.info('Entering a GTD BUY to partially fill the following GTD ICEBERG PARTIALFILL SELL')
        
        self._GTDfill = Order(order_qty=10, limit_prc=self._price, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDfill.setAction('Add')
        self.sendAndValidate(self._GTDfill, AddCallbacks, 'OnOrderTableAdd')
        
        log.info('Entering a GTD ICEBERG PARTIALFILL BUY')
        
        self._GTDicepartialbuy = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_ICEBERG_ORDER_RES, disclosed_qty=20, srs=self._contract)
        self._GTDicepartialbuy.setAction('Add')
        self.sendAndValidate(self._GTDicepartialbuy, AddCallbacks+PartialFillCallbacks, 'OnOrderTableAdd', self._GTDfill, FullFillCallbacks, 'OnOrderTableDelete', self._numOfExpectedFills)
        
        self._GTDfill = None
        self.del_orderbook()
        
        log.info('Entering a GTD SELL to partially fill the following GTD ICEBERG PARTIALFILL BUY')
        
        self._GTDfill = Order(order_qty=10, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDfill.setAction('Add')
        self.sendAndValidate(self._GTDfill, AddCallbacks, 'OnOrderTableAdd')
        
        log.info('Entering a GTD ICEBERG PARTIALFILL SELL')
        
        self._GTDicepartialsell = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_ICEBERG_ORDER_RES, disclosed_qty=20, srs=self._contract)
        self._GTDicepartialsell.setAction('Add')
        self.sendAndValidate(self._GTDicepartialsell, AddCallbacks+PartialFillCallbacks, 'OnOrderTableUpdate', self._GTDfill, FullFillCallbacks, 'OnOrderTableDelete', self._numOfExpectedFills)
        
        self._GTDfill = None
        self.del_orderbook()
        
    def step10(self):
        #Used in testGTD_IOC
        
        log.info('Entering a GTD IOC NOFILL BUY')
        
        self._GTDiocbuy = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_IOC_ORDER_RES, srs=self._contract)
        self._GTDiocbuy.setAction('Add')
        self.sendAndValidate(self._GTDiocbuy, RejectCallbacks)
        
        time.sleep(1)
        
        log.info('Entering a GTD IOC NOFILL SELL')
        
        self._GTDiocsell = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_IOC_ORDER_RES, srs=self._contract)
        self._GTDiocsell.setAction('Add')
        self.sendAndValidate(self._GTDiocsell, RejectCallbacks)
        
        
        self.del_orderbook()
        
    def step11(self):
        #Used in testGTC_IOC
        
        log.info('Entering a GTD Limit order to full fill the following GTD IOC FULLFILL BUY')
        
        self._GTDfill = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDfill.setAction('Add')
        self.sendAndValidate(self._GTDfill, AddCallbacks, 'OnOrderTableAdd')
                             #AddCallbacks+FullFillCallbacks, 'OnOrderTableAdd', self._GTDiocfullbuy, FullFillCallbacks, 'OnOrderTableAdd', self._numOfExpectedFills)
        
        log.info('Entering a GTD IOC FULLFILL BUY')
        
        self._GTDiocfullbuy = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_IOC_ORDER_RES, srs=self._contract)
        self._GTDiocfullbuy.setAction('Add')
        self.sendAndValidate(self._GTDiocfullbuy, AddCallbacks+FullFillCallbacks, 'OnOrderTableAdd', self._GTDfill, FullFillCallbacks, 'OnOrderTableDelete', self._numOfExpectedFills)
        
        
        self.del_orderbook()
        self._GTDfill = None
        
        log.info('Entering a GTD Buy order to full fill the following GTD IOC FULLFILL SELL')
        
        self._GTDfill = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDfill.setAction('Add')
        self.sendAndValidate(self._GTDfill, AddCallbacks, 'OnOrderTableAdd')
                             #AddCallbacks+FullFillCallbacks, 'OnOrderTableAdd', self._GTDiocfullsell, FullFillCallbacks, 'OnOrderTableDelete', self.numOfExpectedFills)
        
        log.info('Entering a GTD IOC FULLFILL SELL')
        
        self._GTDiocfullsell = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_IOC_ORDER_RES, srs=self._contract)
        self._GTDiocfullsell.setAction('Add')
        self.sendAndValidate(self._GTDiocfullsell, AddCallbacks+FullFillCallbacks, 'OnOrderTableAdd', self._GTDfill, FullFillCallbacks, 'OnOrderTableDelete', self._numOfExpectedFills)
        
        self.del_orderbook()
        self._GTDfill = None
        
    def step12(self):#This is where the exchange closed
        #Used in GTD_IOC
        
        log.info('Entering a GTD Sell order to partially fill the following GTD IOC PARTIALFILL BUY')
        
        self._GTDfill = Order(order_qty=10, limit_prc=self._price, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDfill.setAction('Add')
        self.sendAndValidate(self._GTDfill, AddCallbacks, 'OnOrderTableAdd')
        
        log.info('Entering a GTD IOC PARTIALFILL BUY')
        
        self._GTDiocpartialbuy = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_IOC_ORDER_RES, srs=self._contract)
        self._GTDiocpartialbuy.setAction('Add')
        self.sendAndValidate(self._GTDiocpartialbuy, IOCPartialFillCallbacks, 'OnOrderTableAdd', self._GTDfill, FullFillCallbacks, 'OnOrderTableDelete', self._numOfExpectedFills)
        
        self.del_orderbook()
        self._GTDfill = None
#===========================================This is where I started coding "Blind".  The exchange went down so I'm just banging out the logic ==========================
        log.info('Entering a GTD Buy order to partially fill the following GTC IOC PARTIALFILL SELL')
        
        self._GTDfill = Order(order_qty=10, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDfill.setAction('Add')
        self.sendAndValidate(self._GTDfill, AddCallbacks, 'OnOrderTableAdd')
        
        log.info('Entering a GTD IOC PARTIALFILL SELL')
        
        self._GTDiocpartialsell = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_IOC_ORDER_RES, srs=self._contract)
        self._GTDiocpartialsell.setAction('Add')
        self.sendAndValidate(self._GTDiocpartialsell, IOCPartialFillCallbacks, 'OnOrderTableAdd', self._GTDfill, FullFillCallbacks, 'OnOrderTableDelete', self._numOfExpectedFills)
        
        self.del_orderbook()
        self._GTDfill = None

    def step13(self):
        #Used in GTD_MOC

        log.info('Entering a GTD MOC NOFILL BUY')

        self._GTDmocbuy = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_MARKET_ORDER, order_restrict=aenums.TT_MOC_ORDER_RES, srs=self._contract)
        self._GTDmocbuy.setAction('Add')
        self.sendAndValidate(self._GTDmocbuy, AddCallbacks, 'OnOrderTableAdd')

        log.info('Entering a GTD MOC NOFILL SELL')

        self._GTDmocsell = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_SELL, order_type=aenums.TT_MARKET_ORDER, order_restrict=aenums.TT_MOC_ORDER_RES, srs=self._contract)
        self._GTDmocsell.setAction('Add')
        self.sendAndValidate(self._GTDmocsell, AddCallbacks, 'OnOrderTableAdd')

        self.del_orderbook()


    def step14(self):
        #Used in GTD_MOO

        log.info('Entering a GTD MOO NOFILL BUY')

        self._GTDmoobuy = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_MARKET_ORDER, order_restrict=aenums.TT_MARKET_ON_OPEN_RES, srs=self._contract)
        self._GTDmoobuy.setAction('Add')
        self.sendAndValidate(self._GTDmoobuy, AddCallbacks, 'OnOrderTableAdd')

        log.info('Entering a GTD MOO NOFILL SELL')

        self._GTDmoosell = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_SELL, order_type=aenums.TT_MARKET_ORDER, order_restrict=aenums.TT_MARKET_ON_OPEN_RES, srs=self._contract)
        self._GTDmoosell.setAction('Add')
        self.sendAndValidate(self._GTDmoosell, AddCallbacks, 'OnOrderTableAdd')

        self.del_orderbook()

    def step15(self):
        #Used in GTD_LOC

        log.info('Entering a GTD LOC NOFILL BUY')

        self._GTDlocbuy = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_LIMIT_ON_CLOSE_RES, srs=self._contract)
        self._GTDlocbuy.setAction('Add')
        self.sendAndValidate(self._GTDlocbuy, AddCallbacks, 'OnOrderTableAdd')

        log.info('Entering a GTD LOC NOFILL SELL')

        self._GTDlocsell = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_LIMIT_ON_CLOSE_RES, srs=self._contract)
        self._GTDlocsell.setAction('Add')
        self.sendAndValidate(self._GTDlocsell, AddCallbacks, 'OnOrderTableAdd')

        self.del_orderbook()

    def step16(self):
        #Used in GTD_LOO

        log.info('Entering a GTD LOO NOFILL BUY')

        self._GTDloobuy = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_LIMIT_ON_OPEN_RES, srs=self._contract)
        self._GTDloobuy.setAction('Add')
        self.sendAndValidate(self._GTDloobuy, AddCallbacks, 'OnOrderTableAdd')

        log.info('Entering a GTD LOO NOFILL SELL')

        self._GTDloosell = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_LIMIT_ON_OPEN_RES, srs=self._contract)
        self._GTDloosell.setAction('Add')
        self.sendAndValidate(self._GTDloosell, AddCallbacks, 'OnOrderTableAdd')
        
        time.sleep(2)

        self.del_orderbook()

    def step17(self): #GTD STOP NOFILL BUY/SELL
        #Used in GTD_STOP

        log.info('Entering a GTD STOP NOFILL BUY')
        
        self._stopprice = cppclient.TTTick.PriceIntToInt(self._price, self._contract, 10)
        self._stop = cppclient.TTTick.PriceIntToInt(self._price, self._contract, 2)
        self._GTDstopbuy = Order(order_qty=50, limit_prc=self._stopprice, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, stop_prc=self._stop, order_flags=aenums.TT_STOP_MOD_CODE, srs=self._contract)
        self._GTDstopbuy.setAction('Add')
        self.sendAndValidate(self._GTDstopbuy, AddCallbacks, 'OnOrderTableAdd')

        log.info('Entering a GTD STOP NOFILL SELL')

        self._stopprice = cppclient.TTTick.PriceIntToInt(self._price, self._contract, -10)
        self._stop = cppclient.TTTick.PriceIntToInt(self._price, self._contract, -2)
        self._GTDstopsell = Order(order_qty=50, limit_prc=self._stopprice, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, stop_prc=self._stop, order_flags=aenums.TT_STOP_MOD_CODE, srs=self._contract)
        self._GTDstopsell.setAction('Add')
        self.sendAndValidate(self._GTDstopsell, AddCallbacks, 'OnOrderTableAdd')
        
        time.sleep(2)

        self.del_orderbook()

    def step18(self):
        #Used in GTD_STOP

        log.info('Entering a GTD STOP FULLFILL BUY')

        self._stopprice = cppclient.TTTick.PriceIntToInt(self._price, self._contract, 10)
        self._stop = cppclient.TTTick.PriceIntToInt(self._price, self._contract, 2)
        self._GTDstopfullbuy = Order(order_qty=50, limit_prc=self._stopprice, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, stop_prc=self._stop, order_flags=aenums.TT_STOP_MOD_CODE, srs=self._contract)
        self._GTDstopfullbuy.setAction('Add')
        self.sendAndValidate(self._GTDstopfullbuy, AddCallbacks, 'OnOrderTableAdd')

        log.info('Entering a GTD Buy order and a GTD Sell order to trigger the above GTD STOP FULLFILL BUY')

        self._GTDtriggerbuy = Order(order_qty=10, limit_prc=self._stop, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDtriggerbuy.setAction('Add')
        self.sendAndValidate(self._GTDtriggerbuy, AddCallbacks, 'OnOrderTableAdd')

        self._GTDtriggersell = Order(order_qty=10, limit_prc=self._stop, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDtriggersell.setAction('Add')
        self.sendAndValidate(self._GTDtriggersell, AddCallbacks+FullFillCallbacks, 'OnOrderTableAdd', self._GTDtriggerbuy, FullFillCallbacks, 'OnOrderTableDelete')
        
        time.sleep(1)
        
        log.info('Entering an opposing Sell order to full fill the GTD STOP FULLFILL BUY')

        self._GTDopposingsell = Order(order_qty=50, limit_prc=self._stopprice, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDopposingsell.setAction('Add')
        self.sendAndValidate(self._GTDopposingsell, AddCallbacks+FullFillCallbacks, 'OnOrderTableAdd', self._GTDstopfullbuy, FullFillCallbacks, 'OnOrderTableDelete', self._numOfExpectedFills)

        self.del_orderbook()
        self._GTDtriggerbuy = None
        self._GTDtriggersell = None
        self._GTDopposingsell = None

        log.info('Entering a GTD STOP FULLFILL SELL')

        self._stopprice = cppclient.TTTick.PriceIntToInt(self._price, self._contract, -10)
        self._stop = cppclient.TTTick.PriceIntToInt(self._price, self._contract, -2)
        self._GTDstopfullsell = Order(order_qty=50, limit_prc=self._stopprice, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, stop_prc=self._stop, order_flags=aenums.TT_STOP_MOD_CODE, srs=self._contract)
        self._GTDstopfullsell.setAction('Add')
        self.sendAndValidate(self._GTDstopfullsell, AddCallbacks, 'OnOrderTableAdd')

        time.sleep(1)
        
        log.info('Entering a GTD Buy order and a GTD Sell order to trigger the above GTD STOP FULLFILL SELL')

        self._GTDtriggerbuy = Order(order_qty=10, limit_prc=self._stop, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDtriggerbuy.setAction('Add')
        self.sendAndValidate(self._GTDtriggerbuy, AddCallbacks, 'OnOrderTableAdd')

        self._GTDtriggersell = Order(order_qty=10, limit_prc=self._stop, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDtriggersell.setAction('Add')
        self.sendAndValidate(self._GTDtriggersell, AddCallbacks+FullFillCallbacks, 'OnOrderTableAdd', self._GTDtriggerbuy, FullFillCallbacks, 'OnOrderTableDelete', self._numOfExpectedFills)

        log.info('Entering an opposing Buy order to full fill the GTD STOP FULLFILL SELL')

        self._GTDopposingbuy = Order(order_qty=50, limit_prc=self._stopprice, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDopposingbuy.setAction('Add')
        self.sendAndValidate(self._GTDopposingbuy, AddCallbacks+FullFillCallbacks, 'OnOrderTableAdd', self._GTDstopfullsell, FullFillCallbacks, 'OnOrderTableDelete', self._numOfExpectedFills)

        self.del_orderbook()
        self._GTDtriggerbuy = None
        self._GTDtriggersell = None
        self._GTDopposingbuy = None
        
    def step19(self):
        #Used in GTD_STOP

        log.info('Entering a GTD STOP PARTIALFILL BUY')
        
        self._stopprice = cppclient.TTTick.PriceIntToInt(self._price, self._contract, 10)
        self._stop = cppclient.TTTick.PriceIntToInt(self._price, self._contract, 2)
        self._GTDpartialstopbuy = Order(order_qty=50, limit_prc=self._stopprice, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, stop_prc=self._stop, order_flags=aenums.TT_STOP_MOD_CODE, srs=self._contract)
        self._GTDpartialstopbuy.setAction('Add')
        self.sendAndValidate(self._GTDpartialstopbuy, AddCallbacks, 'OnOrderTableAdd')

        log.info('Entering a GTD Buy order and a GTD Sell order to trigger the above GTD STOP PARTIALFILL BUY')

        self._GTDtriggerbuy = Order(order_qty=10, limit_prc=self._stop, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDtriggerbuy.setAction('Add')
        self.sendAndValidate(self._GTDtriggerbuy, AddCallbacks, 'OnOrderTableAdd')

        self._GTDtriggersell = Order(order_qty=10, limit_prc=self._stop, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDtriggersell.setAction('Add')
        self.sendAndValidate(self._GTDtriggersell, AddCallbacks, 'OnOrderTableAdd')

        log.info('Entering an opposing Sell order to partial fill the GTD STOP PARTIALFILL BUY')

        self._GTDopposingsell = Order(order_qty=10, limit_prc=self._stopprice, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDopposingsell.setAction('Add')
        self.sendAndValidate(self._GTDopposingsell, AddCallbacks+FullFillCallbacks, 'OnOrderTableAdd', self._GTDpartialstopbuy, PartialFillCallbacks, 'OnOrderTableUpdate', self._numOfExpectedFills)

        self.del_orderbook()
        self._GTDtriggerbuy = None
        self._GTDtriggersell = None
        self._GTDopposingsell = None
        
        log.info('Entering a GTD STOP PARTIALFILL SELL')

        self._stopprice = cppclient.TTTick.PriceIntToInt(self._price, self._contract, -10)
        self._stop = cppclient.TTTick.PriceIntToInt(self._price, self._contract, -2)
        self._GTDpartialstopsell = Order(order_qty=50, limit_prc=self._stopprice, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, stop_prc=self._stop, order_flags=aenums.TT_STOP_MOD_CODE, srs=self._contract)
        self._GTDpartialstopsell.setAction('Add')
        self.sendAndValidate(self._GTDpartialstopsell, AddCallbacks, 'OnOrderTableAdd')

        log.info('Entering a GTD Buy order and a GTD Sell order to trigger the above GTD STOP PARTIALFILL SELL')

        self._GTDtriggerbuy = Order(order_qty=10, limit_prc=self._stop, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDtriggerbuy.setAction('Add')
        self.sendAndValidate(self._GTDtriggerbuy, AddCallbacks, 'OnOrderTableAdd')

        self._GTDtriggersell = Order(order_qty=10, limit_prc=self._stop, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDtriggersell.setAction('Add')
        self.sendAndValidate(self._GTDtriggersell, AddCallbacks+FullFillCallbacks, 'OnOrderTableAdd', self._GTDtriggerbuy, FullFillCallbacks, 'OnOrderTableDelete', self._numOfExpectedFills)

        log.info('Entering an opposing Buy order to partial fill the GTD STOP PARTIALFILL SELL')

        self._GTDopposingbuy = Order(order_qty=10, limit_prc=self._stopprice, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDopposingbuy.setAction('Add')
        self.sendAndValidate(self._GTDopposingbuy, AddCallbacks+FullFillCallbacks, 'OnOrderTableAdd', self._GTDpartialstopsell, PartialFillCallbacks, 'OnOrderTableUpdate', self._numOfExpectedFills)

        self.del_orderbook()
        self._GTDtriggerbuy = None
        self._GTDtriggersell = None
        self._GTDopposingbuy = None

    def step20(self):
        #Used in GTD_TSTOP
        log.info('Entering a GTD TSTOP NOFILL BUY')
        #raw_input('About to input a TSTOP')
        
        #self._stop = cppclient.TTTick.PriceIntToInt(self._price, self._contract, -2)
        #self._GTDtstopbuy = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, order_flags=aenums.TT_STOP_MOD_CODE, srs=self._contract)
        #self._GTDtstopbuy.setAction('Add')
        #self.sendAndValidate(self._GTDtstopbuy, RejectCallbacks)
        #raw_input('Entered TSTOP')

        log.info('Entering a GTD TSTOP NOFILL BUY')
        log.info('Entering a GTD TSTOP NOFILL SELL')

    def step21(self):

        log.info('Entering a GTD TSTOP FULLFILL BUY')
        log.info('Entering a GTD TSTOP FULLFILL SELL')

    def step22(self):

        log.info('Entering a GTD TSTOP PARTIALFILL BUY')
        log.info('Entering a GTD TSTOP PARTIALFILL SELL')

    def step23(self):
        #Used in testGTC_NoRestr
        
        log.info('Entering a GTC NO_RESTR NOFILL BUY order')
        
        self._GTCbuy = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTCbuy.TIF('GTC')
        self._GTCbuy.setAction('Add')
        self._GTCbuy = self.sendAndValidate(self._GTCbuy, AddCallbacks, 'OnOrderTableAdd')
        
        log.info('Entering a GTC NO_RESTR NOFILL SELL order')
        
        self._tickup = cppclient.TTTick.PriceIntToInt(self._price, self._contract, 1)   
        self._GTCsell = Order(order_qty=50, limit_prc=self._tickup, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTCsell.TIF('GTC')
        self._GTCsell.setAction('Add')
        self._GTCsell = self.sendAndValidate(self._GTCsell, AddCallbacks, 'OnOrderTableAdd')
        
        self.del_orderbook()

    def step24(self):
        #Used in testGTC_NoRestr
        
        log.info('Entering a GTC NO_RESTR FULLFILL BUY')
        
        self._GTCffillbuy = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTCffillbuy.TIF('GTC')
        self._GTCffillbuy.setAction('Add')
        self.sendAndValidate(self._GTCffillbuy, AddCallbacks, 'OnOrderTableAdd')
        
        #time.sleep(1)
        
        log.info('Entering an opposing SELL order to fullfill the GTC NO_RESTR FULLFILL BUY')
        
        self._GTCfill = Order(order_qty =50, limit_prc=self._price, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTCfill.setAction('Add')
        self.sendAndValidate(self._GTCfill, AddCallbacks+FullFillCallbacks, 'OnOrderTableAdd', self._GTCffillbuy, FullFillCallbacks, 'OnOrderTableDelete', self._numOfExpectedFills)
        self._GTCfill = None
        
        log.info('Entering a GTC NO_RESTR FULLFILL SELL')
        
        self._GTCffillsell = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTCffillsell.TIF('GTC')
        self._GTCffillsell.setAction('Add')
        self.sendAndValidate(self._GTCffillsell, AddCallbacks, 'OnOrderTableAdd')
        
        #time.sleep(1)
        
        log.info('Entering an opposing BUY order to fullfill the GTC NO_RESTR FULLFILL SELL')
        
        self._tickup = cppclient.TTTick.PriceIntToInt(self._price, self._contract, 1) 
        self._GTCfill = Order(order_qty=50, limit_prc=self._tickup, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTCfill.setAction('Add')
        self.sendAndValidate(self._GTCfill, AddCallbacks+FullFillCallbacks, 'OnOrderTableAdd', self._GTCffillsell, FullFillCallbacks, 'OnOrderTableDelete', self._numOfExpectedFills)
        
        time.sleep(1)
        
        self.del_orderbook()
        self._GTDfill = None

    def step25(self):
        #Used in testGTC_NoRestr
        
        log.info('Entering a GTC NO_RESTR PARTIALFILL BUY')
        
        self._GTCpartialbuy = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTCpartialbuy.TIF('GTC')
        self._GTCpartialbuy.setAction('Add')
        self._GTCpartialbuy = self.sendAndValidate(self._GTCpartialbuy, AddCallbacks, 'OnOrderTableAdd')
        
        #time.sleep(1)
        
        log.info('Entering an opposing SELL order to partially fill the above BUY order')
        
        self._GTDfill = Order(order_qty=10, limit_prc=self._price, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDfill.setAction('Add')
        self._GTDfill = self.sendAndValidate(self._GTDfill, AddCallbacks+FullFillCallbacks, "OnOrderTableAdd", \
                                                                  self._GTCpartialbuy, PartialFillCallbacks, "OnOrderTableUpdate", self._numOfExpectedFills)
        
        self._GTDfill = None
        
        log.info('Entering a GTD NO_RESTR PARTIALFILL SELL')
        
        self._tickup = cppclient.TTTick.PriceIntToInt(self._price, self._contract, 1) 
        self._GTCpartialsell = Order(order_qty=50, limit_prc=self._tickup, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTCpartialsell.setAction('Add')
        self.sendAndValidate(self._GTCpartialsell, AddCallbacks, 'OnOrderTableAdd')
        
       # time.sleep(1)
        
        log.info('Entering an opposing BUY order to partially fill the above SELL order')
        
        self._GTDfill = Order(order_qty=10, limit_prc=self._tickup, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDfill.setAction('Add')
        self.sendAndValidate(self._GTDfill, AddCallbacks+FullFillCallbacks, 'OnOrderTableAdd', \
                                             self._GTCpartialsell, PartialFillCallbacks, 'OnOrderTableUpdate', self._numOfExpectedFills)
        time.sleep(1)
        
        self.del_orderbook()
        self._GTDfill = None

    def step26(self):
        #Used in testGTC_FOK
        
        log.info('Entering a GTC FOK NOFILL BUY')
        
        GTCfokbuy = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_FOK_ORDER_RES, srs=self._contract)
        GTCfokbuy.TIF('GTC')
        GTCfokbuy.setAction('Add')
        
        #if Builder().buildWithValidation:
                #utils.markForRejection(GTCfokbuy, utils.REJECT_ORDER, utils.REJECT_BY_EXCHANGE)
                
        self.sendAndValidate(GTCfokbuy, RejectCallbacks)
        
        #time.sleep(1)
        
        log.info('Entering a GTC FOK NOFILL SELL')
        
        self._GTCfoksell = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_FOK_ORDER_RES, srs=self._contract)
        self._GTCfoksell.TIF('GTC')
        self._GTCfoksell.setAction('Add')
        
        #if Builder().buildWithValidation:
                #utils.markForRejection(self._GTCfoksell, utils.REJECT_ORDER, utils.REJECT_BY_EXCHANGE)
                
        self.sendAndValidate(self._GTCfoksell, RejectCallbacks)
        
        #time.sleep(1)
        
        self.del_orderbook()

    def step27(self):
        #Used in testGTC_FOK
        
        log.info('Entering an opposing SELL order for the GTC FOK FULLFILL BUY')
        
        self._GTDfill = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDfill.setAction('Add')
        self.sendAndValidate(self._GTDfill, AddCallbacks, 'OnOrderTableAdd')
        
        #time.sleep(1)
        
        log.info('Entering a GTC FOK FULLFILL BUY')
        
        self._GTCfokfullbuy = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_FOK_ORDER_RES, srs=self._contract)
        self._GTCfokfullbuy.TIF('GTC')
        self._GTCfokfullbuy.setAction('Add')
        self.sendAndValidate(self._GTCfokfullbuy, AddCallbacks+FullFillCallbacks, 'OnOrderTableAdd', \
                                                   self._GTDfill, FullFillCallbacks, 'OnOrderTableDelete', self._numOfExpectedFills)
        
        #time.sleep(2)
        
        self._GTDfill = None
        self.del_orderbook()
        
        log.info('Entering an opposing BUY order for the GTC FOK FULLFILL SELL')
        
        self._GTDfill = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDfill.setAction('Add')
        self.sendAndValidate(self._GTDfill, AddCallbacks, 'OnOrderTableAdd')
        
        #time.sleep(1)
        
        log.info('Entering a GTC FOK FULLFILL SELL')
        
        self._GTCfokfullsell = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_FOK_ORDER_RES, srs=self._contract)
        self._GTCfokfullsell.TIF('GTC')
        self._GTCfokfullsell.setAction('Add')
        self.sendAndValidate(self._GTCfokfullsell, AddCallbacks+FullFillCallbacks, 'OnOrderTableAdd', \
                                                    self._GTDfill, FullFillCallbacks, 'OnOrderTableDelete', self._numOfExpectedFills)
        
        #time.sleep(2)
        
        self._GTDfill = None
        self.del_orderbook()

    def step28(self):
        #Used in testGTC_FOK
        
        log.info('Entering an opposing SELL order for the GTC FOK PARTIALFILL BUY')
        
        self._GTDfill = Order(order_qty=20, limit_prc=self._price, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDfill.setAction('Add')
        self.sendAndValidate(self._GTDfill, AddCallbacks, 'OnOrderTableAdd')
        
        log.info('Entering a GTC FOK PARTIALFILL BUY')
        
        self._GTCfokpartialbuy = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_FOK_ORDER_RES, srs=self._contract)
        self._GTCfokpartialbuy.TIF('GTC')
        self._GTCfokpartialbuy.setAction('Add')
        self.sendAndValidate(self._GTCfokpartialbuy, RejectCallbacks)
        
        #time.sleep(2)
        
        self.del_orderbook()
        self._GTDfill = None
        
        log.info('Entering an opposing BUY order for the GTC FOK PARTIALFILL SELL')
        
        self._GTDfill = Order(order_qty=20, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDfill.setAction('Add')
        self.sendAndValidate(self._GTDfill, AddCallbacks, 'OnOrderTableAdd')
        
        log.info('Entering a GTC FOK PARTIALFILL SELL')
        
        self._GTCfokpartialsell = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_FOK_ORDER_RES, srs=self._contract)
        self._GTCfokpartialsell.TIF('GTC')
        self._GTCfokpartialsell.setAction('Add')
        self.sendAndValidate(self._GTCfokpartialsell, RejectCallbacks)
        
        #time.sleep(2)
        
        self.del_orderbook()
        self._GTDfill = None

    def step29(self):
        #Used in testGTC_ICE
        
        log.info('Entering a GTC ICEBERG NOFILL BUY')
        
        self._GTCicebuy = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_ICEBERG_ORDER_RES, disclosed_qty=20, srs=self._contract)
        self._GTCicebuy.TIF('GTC')
        self._GTCicebuy.setAction('Add')
        self.sendAndValidate(self._GTCicebuy, AddCallbacks, 'OnOrderTableAdd')
        
        log.info('Entering a GTC ICEBERG NOFILL SELL')
        
        self._tickup = cppclient.TTTick.PriceIntToInt(self._price, self._contract, 1) 
        self._GTCicesell = Order(order_qty=50, limit_prc=self._tickup, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_ICEBERG_ORDER_RES, disclosed_qty=20, srs=self._contract)
        self._GTCicesell.TIF('GTC')
        self._GTCicesell.setAction('Add')
        self.sendAndValidate(self._GTCicesell, AddCallbacks, 'OnOrderTableAdd')
        
        self.del_orderbook()

    def step30(self):
        #Used in testGTC_ICE
        
        log.info('Entering a GTD BUY to fill the following GTC ICEBERG FULLFILL SELL')
        
        self._GTDfill = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDfill.setAction('Add')
        self.sendAndValidate(self._GTDfill, AddCallbacks, 'OnOrderTableAdd')
        
        log.info('Entering a GTC ICEBERG FULLFILL SELL')
        
        self._GTCicefullsell = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_ICEBERG_ORDER_RES, disclosed_qty=20, srs=self._contract)
        self._GTCicefullsell.TIF('GTC')
        self._GTCicefullsell.setAction('Add')
        self.sendAndValidate(self._GTCicefullsell, AddCallbacks+FullFillCallbacks, 'OnOrderTableAdd', self._GTDfill, FullFillCallbacks, 'OnOrderTableDelete', self._numOfExpectedFills)
        
        self._GTDfill = None
        
        log.info('Entering a GTD SELL to fill the following GTC ICEBERG FULLFILL BUY')
        
        self._GTDfill = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDfill.setAction('Add')
        self.sendAndValidate(self._GTDfill, AddCallbacks, 'OnOrderTableAdd')
        
        log.info('Entering a GTC ICEBERG FULLFILL BUY')
        
        self._GTCicefullbuy = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_ICEBERG_ORDER_RES, disclosed_qty=20, srs=self._contract)
        self._GTCicefullbuy.TIF('GTC')
        self._GTCicefullbuy.setAction('Add')
        self.sendAndValidate(self._GTCicefullbuy, AddCallbacks+FullFillCallbacks, 'OnOrderTableAdd', self._GTDfill, FullFillCallbacks, 'OnOrderTableDelete', self._numOfExpectedFills)
        
        self.del_orderbook()
        self._GTDfill = None

    def step31(self):
        #Used in testGTC_ICE
        
        log.info('Entering a GTD BUY to partially fill the following GTC ICEBERG PARTIALFILL SELL')
        
        self._GTDfill = Order(order_qty=10, limit_prc=self._price, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDfill.setAction('Add')
        self.sendAndValidate(self._GTDfill, AddCallbacks, 'OnOrderTableAdd')
        
        log.info('Entering a GTC ICEBERG PARTIALFILL BUY')
        
        self._GTCicepartialbuy = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_ICEBERG_ORDER_RES, disclosed_qty=20, srs=self._contract)
        self._GTCicepartialbuy.TIF('GTC')
        self._GTCicepartialbuy.setAction('Add')
        self.sendAndValidate(self._GTCicepartialbuy, AddCallbacks+PartialFillCallbacks, 'OnOrderTableAdd', self._GTDfill, FullFillCallbacks, 'OnOrderTableDelete', self._numOfExpectedFills)
        
        self._GTDfill = None
        self.del_orderbook()
        
        log.info('Entering a GTD SELL to partially fill the following GTC ICEBERG PARTIALFILL BUY')
        
        self._GTDfill = Order(order_qty=10, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDfill.setAction('Add')
        self.sendAndValidate(self._GTDfill, AddCallbacks, 'OnOrderTableAdd')
        
        log.info('Entering a GTC ICEBERG PARTIALFILL SELL')
        
        self._GTCicepartialsell = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_ICEBERG_ORDER_RES, disclosed_qty=20, srs=self._contract)
        self._GTCicepartialsell.TIF('GTC')
        self._GTCicepartialsell.setAction('Add')
        self.sendAndValidate(self._GTCicepartialsell, AddCallbacks+PartialFillCallbacks, 'OnOrderTableUpdate', self._GTDfill, FullFillCallbacks, 'OnOrderTableDelete', self._numOfExpectedFills)
        
        self._GTDfill = None
        self.del_orderbook()

    def step32(self):
        #Used in testGTC_IOC
        
        log.info('Entering a GTC IOC NOFILL BUY')
        
        self._GTCiocbuy = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_IOC_ORDER_RES, srs=self._contract)
        self._GTCiocbuy.TIF('GTC')
        self._GTCiocbuy.setAction('Add')
        self.sendAndValidate(self._GTCiocbuy, RejectCallbacks)
        
        time.sleep(1)
        
        log.info('Entering a GTC IOC NOFILL SELL')
        
        self._GTCiocsell = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_IOC_ORDER_RES, srs=self._contract)
        self._GTCiocsell.TIF('GTC')
        self._GTCiocsell.setAction('Add')
        self.sendAndValidate(self._GTCiocsell, RejectCallbacks)
        
        self.del_orderbook()

    def step33(self):
        #Used in testGTC_IOC
        
        log.info('Entering a GTD Limit order to full fill the following GTC IOC FULLFILL BUY')
        
        self._GTDfill = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDfill.setAction('Add')
        self.sendAndValidate(self._GTDfill, AddCallbacks, 'OnOrderTableAdd')
                             
        log.info('Entering a GTC IOC FULLFILL BUY')
        
        self._GTCiocfullbuy = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_IOC_ORDER_RES, srs=self._contract)
        self._GTCiocfullbuy.TIF('GTC')
        self._GTCiocfullbuy.setAction('Add')
        self.sendAndValidate(self._GTCiocfullbuy, AddCallbacks+FullFillCallbacks, 'OnOrderTableAdd', self._GTDfill, FullFillCallbacks, 'OnOrderTableDelete', self._numOfExpectedFills)
        
        
        self.del_orderbook()
        self._GTDfill = None
        
        log.info('Entering a GTD Buy order to full fill the following GTC IOC FULLFILL SELL')
        
        self._GTDfill = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDfill.setAction('Add')
        self.sendAndValidate(self._GTDfill, AddCallbacks, 'OnOrderTableAdd')
                             
        log.info('Entering a GTC IOC FULLFILL SELL')
        
        self._GTCiocfullsell = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_IOC_ORDER_RES, srs=self._contract)
        self._GTCiocfullsell.TIF('GTC')
        self._GTCiocfullsell.setAction('Add')
        self.sendAndValidate(self._GTCiocfullsell, AddCallbacks+FullFillCallbacks, 'OnOrderTableAdd', self._GTDfill, FullFillCallbacks, 'OnOrderTableDelete', self._numOfExpectedFills)
        
        self.del_orderbook()
        self._GTDfill = None

    def step34(self):
        #Used in GTC_IOC
        
        log.info('Entering a GTD Sell order to partially fill the following GTC IOC PARTIALFILL BUY')
        
        self._GTDfill = Order(order_qty=10, limit_prc=self._price, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDfill.setAction('Add')
        self.sendAndValidate(self._GTDfill, AddCallbacks, 'OnOrderTableAdd')
        
        log.info('Entering a GTC IOC PARTIALFILL BUY')
        
        GTCiocpartialbuy = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_IOC_ORDER_RES, srs=self._contract)
        GTCiocpartialbuy.TIF('GTC')
        GTCiocpartialbuy.setAction('Add')
        self.sendAndValidate(GTCiocpartialbuy, IOCPartialFillCallbacks, 'OnOrderTableAdd', self._GTDfill, FullFillCallbacks, 'OnOrderTableDelete', self._numOfExpectedFills)
        
        self.del_orderbook()
        self._GTDfill = None
#===========================================This is where I started coding "Blind".  The exchange went down so I'm just banging out the logic ==========================
        log.info('Entering a GTD Buy order to partially fill the following GTC IOC PARTIALFILL SELL')
        
        self._GTDfill = Order(order_qty=10, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDfill.setAction('Add')
        self.sendAndValidate(self._GTDfill, AddCallbacks, 'OnOrderTableAdd')
        
        log.info('Entering a GTC IOC PARTIALFILL SELL')
        
        self._GTCiocpartialsell = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_IOC_ORDER_RES, srs=self._contract)
        self._GTCiocpartialsell.TIF('GTC')
        self._GTCiocpartialsell.setAction('Add')
        self.sendAndValidate(self._GTCiocpartialsell, IOCPartialFillCallbacks, 'OnOrderTableAdd', self._GTDfill, FullFillCallbacks, 'OnOrderTableDelete', self._numOfExpectedFills)
        
        self.del_orderbook()
        self._GTDfill = None


    def step35(self):
        #Used in GTC_MOC

        log.info('Entering a GTC MOC NOFILL BUY')

        self._GTCmocbuy = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_MARKET_ORDER, order_restrict=aenums.TT_MOC_ORDER_RES, srs=self._contract)
        self._GTCmocbuy.TIF('GTC')
        self._GTCmocbuy.setAction('Add')
        self.sendAndValidate(self._GTCmocbuy, AddCallbacks, 'OnOrderTableAdd')

        log.info('Entering a GTC MOC NOFILL SELL')

        self._GTCmocsell = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_SELL, order_type=aenums.TT_MARKET_ORDER, order_restrict=aenums.TT_MOC_ORDER_RES, srs=self._contract)
        self._GTCmocsell.TIF('GTC')
        self._GTCmocsell.setAction('Add')
        self.sendAndValidate(self._GTCmocsell, AddCallbacks, 'OnOrderTableAdd')

        self.del_orderbook()


    def step36(self):
        #Used in GTC_MOO

        log.info('Entering a GTC MOO NOFILL BUY')

        self._GTCmoobuy = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_MARKET_ORDER, order_restrict=aenums.TT_MARKET_ON_OPEN_RES, srs=self._contract)
        self._GTCmoobuy.TIF('GTC')
        self._GTCmoobuy.setAction('Add')
        self.sendAndValidate(self._GTCmoobuy, AddCallbacks, 'OnOrderTableAdd')

        log.info('Entering a GTC MOO NOFILL SELL')

        self._GTCmoosell = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_SELL, order_type=aenums.TT_MARKET_ORDER, order_restrict=aenums.TT_MARKET_ON_OPEN_RES, srs=self._contract)
        self._GTCmoosell.TIF('GTC')
        self._GTCmoosell.setAction('Add')
        self.sendAndValidate(self._GTCmoosell, AddCallbacks, 'OnOrderTableAdd')

        self.del_orderbook()

    def step37(self):
        #Used in GTC_LOC

        log.info('Entering a GTC LOC NOFILL BUY')

        self._GTClocbuy = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_LIMIT_ON_CLOSE_RES, srs=self._contract)
        self._GTClocbuy.TIF('GTC')
        self._GTClocbuy.setAction('Add')
        self.sendAndValidate(self._GTClocbuy, AddCallbacks, 'OnOrderTableAdd')

        log.info('Entering a GTC LOC NOFILL BUY')

        self._GTClocsell = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_LIMIT_ON_CLOSE_RES, srs=self._contract)
        self._GTClocsell.TIF('GTC')
        self._GTClocsell.setAction('Add')
        self.sendAndValidate(self._GTClocsell, AddCallbacks, 'OnOrderTableAdd')

        self.del_orderbook()

    def step38(self):
        #Used in GTC_LOO

        log.info('Entring a GTC LOO NOFILL BUY')

        self._GTCloobuy = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_LIMIT_ON_OPEN_RES, srs=self._contract)
        self._GTCloobuy.TIF('GTC')
        self._GTCloobuy.setAction('Add')
        self.sendAndValidate(self._GTCloobuy, AddCallbacks, 'OnOrderTableAdd')

        log.info('Entering a GTC LOO NOFILL SELL')

        self._GTCloosell = Order(order_qty=50, limit_prc=self._price, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, order_restrict=aenums.TT_LIMIT_ON_OPEN_RES, srs=self._contract)
        self._GTCloosell.TIF('GTC')
        self._GTCloosell.setAction('Add')
        self.sendAndValidate(self._GTCloosell, AddCallbacks, 'OnOrderTableAdd')

    def step39(self): #GTC STOP NOFILL BUY/SELL
        #Used in GTC_STOP

        log.info('Entering a GTC STOP NOFILL BUY')
        
        self._stopprice = cppclient.TTTick.PriceIntToInt(self._price, self._contract, 10)
        self._stop = cppclient.TTTick.PriceIntToInt(self._price, self._contract, 2)
        self._GTCstopbuy = Order(order_qty=50, limit_prc=self._stopprice, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, stop_prc=self._stop, order_flags=aenums.TT_STOP_MOD_CODE, srs=self._contract)
        self._GTCstopbuy.TIF('GTC')
        self._GTCstopbuy.setAction('Add')
        self.sendAndValidate(self._GTCstopbuy, AddCallbacks, 'OnOrderTableAdd')

        log.info('Entering a GTC STOP NOFILL SELL')

        self._stopprice = cppclient.TTTick.PriceIntToInt(self._price, self._contract, -10)
        self._stop = cppclient.TTTick.PriceIntToInt(self._price, self._contract, -2)
        self._GTCstopsell = Order(order_qty=50, limit_prc=self._stopprice, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, stop_prc=self._stop, order_flags=aenums.TT_STOP_MOD_CODE, srs=self._contract)
        self._GTCstopsell.TIF('GTC')
        self._GTCstopsell.setAction('Add')
        self.sendAndValidate(self._GTCstopsell, AddCallbacks, 'OnOrderTableAdd')
        
        time.sleep(1)
        
        self.del_orderbook()

    def step40(self):
        #Used in GTC_STOP

        log.info('Entering a GTC STOP FULLFILL BUY')

        self._stopprice = cppclient.TTTick.PriceIntToInt(self._price, self._contract, 10)
        self._stop = cppclient.TTTick.PriceIntToInt(self._price, self._contract, 2)
        self._GTCstopfullbuy = Order(order_qty=50, limit_prc=self._stopprice, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, stop_prc=self._stop, order_flags=aenums.TT_STOP_MOD_CODE, srs=self._contract)
        self._GTCstopfullbuy.TIF('GTC')
        self._GTCstopfullbuy.setAction('Add')
        self.sendAndValidate(self._GTCstopfullbuy, AddCallbacks, 'OnOrderTableAdd')

        time.sleep(1)

        log.info('Entering a GTD Buy order and a GTD Sell order to trigger the above GTC STOP FULLFILL BUY')

        self._GTDtriggerbuy = Order(order_qty=10, limit_prc=self._stop, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDtriggerbuy.setAction('Add')
        self.sendAndValidate(self._GTDtriggerbuy, AddCallbacks, 'OnOrderTableAdd')

        self._GTDtriggersell = Order(order_qty=10, limit_prc=self._stop, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDtriggersell.setAction('Add')
        self.sendAndValidate(self._GTDtriggersell, AddCallbacks+FullFillCallbacks, 'OnOrderTableAdd', self._GTDtriggerbuy, FullFillCallbacks, 'OnOrderTableDelete')
        
        time.sleep(1)
        
        log.info('Entering an opposing Sell order to full fill the GTC STOP FULLFILL BUY')

        self._GTCopposingsell = Order(order_qty=50, limit_prc=self._stopprice, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTCopposingsell.TIF('GTC')
        self._GTCopposingsell.setAction('Add')
        self.sendAndValidate(self._GTCopposingsell, AddCallbacks+FullFillCallbacks, 'OnOrderTableAdd', self._GTCstopfullbuy, FullFillCallbacks, 'OnOrderTableDelete', self._numOfExpectedFills)
        
        time.sleep(1)
        
        self.del_orderbook()
        self._GTDtriggerbuy = None
        self._GTDtriggersell = None
        self._GTDopposingsell = None

        log.info('Entering a GTC STOP FULLFILL SELL')

        self._stopprice = cppclient.TTTick.PriceIntToInt(self._price, self._contract, -10)
        self._stop = cppclient.TTTick.PriceIntToInt(self._price, self._contract, -2)
        self._GTCstopfullsell = Order(order_qty=50, limit_prc=self._stopprice, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, stop_prc=self._stop, order_flags=aenums.TT_STOP_MOD_CODE, srs=self._contract)
        self._GTCstopfullsell.TIF('GTC')
        self._GTCstopfullsell.setAction('Add')
        self.sendAndValidate(self._GTCstopfullsell, AddCallbacks, 'OnOrderTableAdd')

        log.info('Entering a GTD Buy order and a GTD Sell order to trigger the above GTD STOP FULLFILL SELL')

        self._GTDtriggerbuy = Order(order_qty=10, limit_prc=self._stop, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDtriggerbuy.setAction('Add')
        self.sendAndValidate(self._GTDtriggerbuy, AddCallbacks, 'OnOrderTableAdd')

        self._GTDtriggersell = Order(order_qty=10, limit_prc=self._stop, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDtriggersell.setAction('Add')
        self.sendAndValidate(self._GTDtriggersell, AddCallbacks+FullFillCallbacks, 'OnOrderTableAdd', self._GTDtriggerbuy, FullFillCallbacks, 'OnOrderTableDelete', self._numOfExpectedFills)

        log.info('Entering an opposing Buy order to full fill the GTD STOP FULLFILL SELL')

        self._GTCopposingbuy = Order(order_qty=50, limit_prc=self._stopprice, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTCopposingbuy.TIF('GTC')
        self._GTCopposingbuy.setAction('Add')
        self.sendAndValidate(self._GTCopposingbuy, AddCallbacks+FullFillCallbacks, 'OnOrderTableAdd', self._GTCstopfullsell, FullFillCallbacks, 'OnOrderTableDelete', self._numOfExpectedFills)

        self.del_orderbook()
        self._GTDtriggerbuy = None
        self._GTDtriggersell = None
        self._GTCopposingbuy = None

    def step41(self):
        #Used in GTC_STOP

        log.info('Entering a GTC STOP PARTIALFILL BUY')
        
        self._stopprice = cppclient.TTTick.PriceIntToInt(self._price, self._contract, 10)
        self._stop = cppclient.TTTick.PriceIntToInt(self._price, self._contract, 2)
        self._GTCpartialstopbuy = Order(order_qty=50, limit_prc=self._stopprice, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, stop_prc=self._stop, order_flags=aenums.TT_STOP_MOD_CODE, srs=self._contract)
        self._GTCpartialstopbuy.TIF('GTC')
        self._GTCpartialstopbuy.setAction('Add')
        self.sendAndValidate(self._GTCpartialstopbuy, AddCallbacks, 'OnOrderTableAdd')

        log.info('Entering a GTD Buy order and a GTD Sell order to trigger the above GTD STOP PARTIALFILL BUY')

        self._GTDtriggerbuy = Order(order_qty=10, limit_prc=self._stop, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDtriggerbuy.setAction('Add')
        self.sendAndValidate(self._GTDtriggerbuy, AddCallbacks, 'OnOrderTableAdd')

        self._GTDtriggersell = Order(order_qty=10, limit_prc=self._stop, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDtriggersell.setAction('Add')
        self.sendAndValidate(self._GTDtriggersell, AddCallbacks, 'OnOrderTableAdd')

        log.info('Entering an opposing Sell order to partial fill the GTC STOP PARTIALFILL BUY')

        self._GTCopposingsell = Order(order_qty=10, limit_prc=self._stopprice, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTCopposingsell.TIF('GTC')
        self._GTCopposingsell.setAction('Add')
        self.sendAndValidate(self._GTCopposingsell, AddCallbacks+FullFillCallbacks, 'OnOrderTableAdd', self._GTCpartialstopbuy, PartialFillCallbacks, 'OnOrderTableUpdate', self._numOfExpectedFills)
        
        self.del_orderbook()
        self._GTDtriggerbuy = None
        self._GTDtriggersell = None
        self._GTCopposingsell = None

        log.info('Entering a GTC STOP PARTIALFILL SELL')

        self._stopprice = cppclient.TTTick.PriceIntToInt(self._price, self._contract, -10)
        self._stop = cppclient.TTTick.PriceIntToInt(self._price, self._contract, -2)
        self._GTCpartialstopsell = Order(order_qty=50, limit_prc=self._stopprice, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, stop_prc=self._stop, order_flags=aenums.TT_STOP_MOD_CODE, srs=self._contract)
        self._GTCpartialstopsell.setAction('Add')
        self.sendAndValidate(self._GTCpartialstopsell, AddCallbacks, 'OnOrderTableAdd')

        log.info('Entering a GTD Buy order and a GTD Sell order to trigger the above GTD STOP PARTIALFILL SELL')

        self._GTDtriggerbuy = Order(order_qty=10, limit_prc=self._stop, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDtriggerbuy.setAction('Add')
        self.sendAndValidate(self._GTDtriggerbuy, AddCallbacks, 'OnOrderTableAdd')

        self._GTDtriggersell = Order(order_qty=10, limit_prc=self._stop, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTDtriggersell.setAction('Add')
        self.sendAndValidate(self._GTDtriggersell, AddCallbacks+FullFillCallbacks, 'OnOrderTableAdd', self._GTDtriggerbuy, FullFillCallbacks, 'OnOrderTableDelete', self._numOfExpectedFills)

        log.info('Entering an opposing Buy order to partial fill the GTD STOP PARTIALFILL SELL')

        self._GTCopposingbuy = Order(order_qty=10, limit_prc=self._stopprice, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, srs=self._contract)
        self._GTCopposingbuy.TIF('GTC')
        self._GTCopposingbuy.setAction('Add')
        self.sendAndValidate(self._GTCopposingbuy, AddCallbacks+FullFillCallbacks, 'OnOrderTableAdd', self._GTCpartialstopsell, PartialFillCallbacks, 'OnOrderTableUpdate', self._numOfExpectedFills)

        self.del_orderbook()
        self._GTDtriggerbuy = None
        self._GTDtriggersell = None
        self._GTCopposingbuy = None

    def step42(self):
        #Used in GTC_TSTOP

        log.info('Entering a GTC TSTOP NOFILL BUY')
        log.info('Entering a GTC TSTOP NOFILL SELL')

    def step43(self):
        #Used in GTC_TSTOP

        log.info('Entering a GTC TSTOP FULLFILL BUY')
        log.info('Entering a GTC TSTOP FULLFILL SELL')

    def step44(self):
        #Used in GTC_TSTOP

        log.info('Entering a GTC TSTOP PARTIALFILL BUY')
        log.info('Entering a GTC TSTOP PARTIALFILL SELL')

if __name__ == '__main__':
    from tests import driver
    name = 'tt.tests.sgx_org.order_server.smoke.SGX_SMOKE2'
    driver.run([name])
        
        
    