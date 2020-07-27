#~TestCaseName: TestCreatePositions
#~Exchange/Simulator/Both: Both
#~Pyrate Version: 2.0

'''TESTCASE 122044: Create Automated Tests for Price Depth.'''

__author__ = 'Chris Maurer (chris.maurer@tradingtechnologies.com)'
__version__ = '1.2'

import logging
import time
import os

from pyrate.builder import Builder
from pyrate.ttapi.manager import TTAPIManager
from pyrate.ttapi.order import TTAPIOrder
from pyrate.ttapi.keygen import generateSiteOrderKey

from ttapi import aenums, cppclient
from ttapi.cppclient_26_75 import AEnum_PriceIds

from sgx.lib.OMSimpleOrder import OMSimpleOrder
from sgx.lib.Timestamp import getDateStamp

log = logging.getLogger(__name__)

class TestCreatePositions():

    @classmethod
    def setUpClass(cls):
        cls.priceSession = TTAPIManager().getPriceSession()
        cls.orderSession = TTAPIManager().getOrderSession()
        cls.custDefauts = TTAPIManager().getCustomer()
        cls.ordSrv = TTAPIManager().getOrderServer()
        cls.priceSrv = TTAPIManager().getPriceServer()

    def submitSeedOrder(self, scenarioType):
        self.myOrder = OMSimpleOrder(o_callbax=True, specifiQty=100)#, prod='EY')
        time.sleep(1)
        log.info('Deleting seed order')
        self.orderSession.deleteAllOrders()

    def getFilled(self, side='SELL'):
        products = self.priceSession.getProducts()
        for product in products:
            contracts = self.priceSession.getContracts(product)
            for contract in contracts:
                if str(self.myOrder.srs.seriesKey) == str(contract.seriesKey):
                    break
                else:
                    continue
            if str(self.myOrder.srs.seriesKey) == str(contract.seriesKey):
                break
            else:
                continue
        orderParams = dict(order_qty=10,\
                           acct=cppclient.AEnum_Account.TT_ACCT_AGENT_1,\
                           order_action=aenums.TT_ORDER_ACTION_ADD,\
                           limit_prc=self.myOrder.limit_prc,\
                           order_type=aenums.TT_LIMIT_ORDER,\
                           srs=contract,\
                           free_text0=self.custDefauts.account,\
                           free_text2=self.custDefauts.fft2)
        depthLevel = 1
        while depthLevel <= numOfDepthLevels:
            orderCounter = 1
            if side == 'BUY':
                pricey = (cppclient.TTTick.PriceIntToInt(pricey, contract, -1))
            else:
                pricey = (cppclient.TTTick.PriceIntToInt(pricey, contract, +1))
            log.info('sending %s %s-lot %s order for %s @ %s' % (numOfOrders, orderParams['order_qty'], side, contract.seriesKey, pricey))
            depthLevel += 1
            while orderCounter <= numOfOrders:
                newOrder = TTAPIOrder()
                newOrder.setFields(**orderParams)
                if side == 'BUY':
                    newOrder.setFields(buy_sell=aenums.TT_BUY)
                else:
                    newOrder.setFields(buy_sell=aenums.TT_SELL)
                newOrder.setFields(site_order_key=generateSiteOrderKey())
                newOrder.setFields(limit_prc=pricey)
                self.orderSession.send(newOrder)
                orderCounter += 1
        
    def testRun(self):
        log.info(' Starting TestCreatePositions '.center(70, '*'))
        self.submitSeedOrder()
        self.getFilled()
        log.info(' TestCreatePositions Complete '.center(70, '*'))

if __name__ == '__main__':
    from pyrate import driver
    name = 'sgx.price_server.ttapi.TestCreatePositions'
    driver.run([name])