from __future__ import absolute_import


from ttapi import aenums
from nose.tools import assert_raises
from pyrate.builder import Builder
from pyrate import PyrateAssertionError
from pyrate.ttapi.order import TTAPIOrder
from pyrate.ttapi.connection import *
from pyrate.ttapi.trader import TTAPITrader
from pyrate.ttapi.manager import TTAPIManager
from pyrate.ttapi.consumers import OrderConsumer, TradeConsumer, FillConsumer, LimitConsumer
from pyrate.ttapi.order_session import OrderSession
from pyrate.ttapi.connection import TTAPIConnection
from pyrate.ttapi.session import TTAPISession
from pyrate.ttapi.gateway import Gateway
from pyrate.ttapi.price_session import PriceSession
from tocom.lib import Order

from pyrate.ttapi.order_session import *
from om.predicates import IsTransType, IsBroadcastType

from pyrate.ttapi.server import OrderServer
from pyrate.pipe.generator import Pipe
from pyrate.server import Service
from pyrate.ttapi.server import TTAPIServer
from pyrate.ttapi.session import TTAPISession
import time

#The following is just test imports to help migrate to 2.0
#clear
from tocom.lib.OMValidation import MessageValidator
from tocom.lib.OrderValidation import OrderAddValidator
from tocom.lib import CallbackHandler
from tocom.lib import Exceptions
from tocom.lib import LogValidator
from tocom.lib import MDMPValidator
from tocom.lib import OMAPIMessageValidator
from tocom.lib import ProductTable
from tocom.lib import Timestamp
from tocom.lib import TOCOMConfigParser
from tocom.lib import TOCOMHostInfo
from tocom.lib import TTMStatus
from tocom.lib import UniversalFunctions
#not working
#from tocom.lib import OrderTestsBaseClass
#from tocom.lib import TOCOMProductInfo


from tocom.lib import Validator






TOCOM_CFG = "C:/Python26/Lib/site-packages/tocom/tocom.cfg"

class TestTTAPIOrder(object):

     @classmethod
     def setUpClass(cls):
         
        cls.builder = Builder()
        cls.builder.build(TOCOM_CFG)
        cls.priceSession = TTAPIManager().getPriceSession()
        cls.orderSession = TTAPIManager().getOrderSession()
        ##cls.gateway = TTAPIManager().getGateway()
        cls.trader = TTAPIManager().getTrader()
        
        
        cls.mo31 = 'MO31'
        cls.isM031 = IsTransType(cls.mo31)
        
        cls.bd4 = 'BD4'
        cls.isBD4 = IsBroadcastType(cls.bd4)
        print type(cls.isBD4)
        
     def testFillSeq(self):
        
        products = self.priceSession.getProducts()   
        contracts = self.priceSession.getContracts(products)
        contract = contracts[2]
        
        buy_order = TTAPIOrder()
        buy_data = dict(order_qty=10, acct=cppclient.AEnum_Account.TT_ACCT_AGENT_1, order_action=aenums.TT_ORDER_ACTION_ADD, limit_prc=1800,exch_member=self.trader.exchMember, exch_group=self.trader.exchGroup, exch_trader=self.trader.exchTrader, buy_sell=aenums.TT_BUY, order_type=aenums.TT_LIMIT_ORDER, srs=contract, free_text2="33G3312345", free_text0="33G")
        buy_order.setFields(**buy_data)
        
        sell_order = TTAPIOrder()
        sell_data = dict(order_qty=10, acct=cppclient.AEnum_Account.TT_ACCT_AGENT_1, order_action=aenums.TT_ORDER_ACTION_ADD, limit_prc=1800,exch_member=self.trader.exchMember, exch_group=self.trader.exchGroup, exch_trader=self.trader.exchTrader, buy_sell=aenums.TT_SELL, order_type=aenums.TT_LIMIT_ORDER, srs=contract, free_text2="33G3312345", free_text0="33G")
        sell_order.setFields(**sell_data)
        
        pipe = TTAPIManager().getPacketPipe()
        
        raw_input("Press enter")
        
        y = 5
        x = 0
        
        while x < y:
            
            pipe.clear()
            self.orderSession.send(sell_order)
           # time.sleep(1)
            self.orderSession.send(buy_order)
            
            status, messages = pipe.wait_for([self.isBD4, self.isBD4], timeout=10)
            print status
            sell_bd4 = messages[0]
            buy_bd4 = messages[1]
            
            print "###############"
            print "##"
            print "## Sell BD4 SEQUENCE #: %s" % sell_bd4.directed_trade.cl_trade_api.sequence_number_i
            print "##"
            print "## Buy BD4 SEQUENCE #: %s" % buy_bd4.directed_trade.cl_trade_api.sequence_number_i
            print "##"
            print "###############"
            
            x += 1
            
            #raw_input("Press enter for another iteration of orders")
            
        
        
        
        
#        self.orderSession.send(buy_order)
#        
#        
#        
#        status, messages = pipe.wait_for([self.isM031])
#        print status
#        
#        print messages[0].hv_order_trans.transaction_type
#        
#        
#        
#        raw_input("Press enter")
#        
#        pipe = TTAPIManager().getPacketPipe()
#        pipe.clear()
#        
#        self.orderSession.send(sell_order)
#        
#        status, messages = pipe.wait_for([self.isM031])
#        print status
#        
#        print messages[0].hv_order_trans.transaction_type
        
        
        
        
        
        
        
        
        
        
        
        #Good to here
#        raw_input("Press enter")
#        
#        pipe = TTAPIManager().getPacketPipe()
#        pipe.clear()
#        
#        self.orderSession.send(buy_order)
#        
#        
#        
#        status, messages = pipe.wait_for([self.isM031])
#        print status
#        
#        print messages[0].hv_order_trans.transaction_type
#        
#        
#        
#        raw_input("Press enter")
#        
#        pipe = TTAPIManager().getPacketPipe()
#        pipe.clear()
#        
#        self.orderSession.send(sell_order)
#        
#        status, messages = pipe.wait_for([self.isM031])
#        print status
#        
#        print messages[0].hv_order_trans.transaction_type
        
        
        
        
        
        
        
        
        