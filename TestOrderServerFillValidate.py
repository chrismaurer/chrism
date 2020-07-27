#~ TestCaseName: TestOrderServerFillValidate
#~TestCaseSummary: Test Order Server Fill Validation by choosing a random contract and 
#                  Validating Fill Data. This test is meant to be repeated many times in succession.
#~Exchange/Simulator/Both: Both
#~Pyrate Version: 2.0

'''Validates RQ_Requirements 102937 and 102956: Send Fill and Order Status To Trading Application Upon Receipt Of Dedicated Trade Information Broadcast

Detail RQ_Requirements
102938,102974,103000,102971,103003,102964,102993,102946,102949,102947,102984,
102983,102963,102975,102999,102977,103006,102978,103005,102948,103007,102944,
102945,102965,102989,102966,102990,102967,102991,102968,102986,102969,102987,
102970,102988,102972,103004,102981,102941,102958,102992,102996,102994,102960,
102997,102976,102985,102959,102998,102942,102957,102995,102980,103001,102943,
102979,103002,102961,102982
TESTCASE PCR 107616.'''

__author__ = 'Chris Maurer (chris.maurer@tradingtechnologies.com)'
__version__ = '1.10'

import logging
import time

from ttapi import aenums

from pyrate.builder import Builder
from pyrate.ttapi.manager import TTAPIManager

from om.predicates import IsBroadcastType

from sgx.lib.FillsLib import generateFill#, getBD4message, getBD4Spreadmessage
from sgx.lib.OMValidation.MessageValidator import validateBD4
from sgx.lib.Exceptions import SGXException

log = logging.getLogger(__name__)

class TestOrderServerFillValidate():

    @classmethod
    def setUpClass(cls):
        cls.bd4Msg = IsBroadcastType('BD4')
        cls.omPipe = TTAPIManager().getPacketPipe()
        cls.omPipe.clear()

    def validateFill(self):
#------Create a Fill
#    try:
        closeOrder, fillValidation1, fillValidation2 = generateFill(getFill=True, partial=False, callbax=True, custTotal=1, noMkt=True)
#    except:
#        log.error('Unable to create the fill.')
#        raise SGXException('Unable to create the fill.')
#------Call getBD4Spreadmessage if it's a Spread Trade, else call getBD4message
        if fillValidation2 == None:
#        try:
            message = self.getBD4message(closeOrder, fillValidation1['orderData'], fillValidation1['fillData'])
#        except:
#            log.error('Unable to retrieve BD4 messages from OMPipe.')
#            raise SGXException('Unable to retrieve BD4 messages from OMPipe.')
            validateBD4(fillValidation1['orderData'], fillValidation1['fillData'], message)
        else:
#        try:
            messagesLeg1, messagesLeg2 = self.getBD4Spreadmessage(closeOrder, fillValidation1['orderDataLeg1'], fillValidation1['fillDataLeg1'], fillValidation2['orderDataLeg2'], fillValidation2['fillDataLeg2'])
#        except:
#            log.error('Unable to retrieve BD4 messages from OMPipe.')
#            raise SGXException('Unable to retrieve BD4 messages from OMPipe.')
            log.info('### Validating Spread Leg 1 ###')
            validateBD4(fillValidation1['orderDataLeg1'], fillValidation1['fillDataLeg1'], messagesLeg1)
            log.info('### Validating Spread Leg 2 ###')
            validateBD4(fillValidation2['orderDataLeg2'], fillValidation2['fillDataLeg2'], messagesLeg2)

    def getBD4message(self, closeOrder, orderCallback, fillCallback):
        '''This function invokes PacketPipe, grabs the BD4 message  
    
        and returns the data.
        
        This function expects to be passed the following:
        
        orderCallback = OnOrderFilled
        fillCallback = OnFillRecord'''

        bd4Msg = self.bd4Msg
        print '------------------------------'
        print self.omPipe.peek()
        print '------------------------------'
#------Capture PacketPipe messages for CLOSE order.
        foundFill = False
        if closeOrder:
            status, messages = self.omPipe.wait_for([bd4Msg, bd4Msg, bd4Msg, bd4Msg], timeout = 30)
        else:
            status, messages = self.omPipe.wait_for([bd4Msg], timeout = 30)
        if status == 'TIMEOUT':
            log.error('OMPipe %s' % (status))
            raise SGXException('OMPipe %s' % (status))
        elif len(messages) == 0:
            log.error('Unable to find transaction no. %s in the BD4 messages.' % (fillCallback.transaction_no))
            raise SGXException('Unable to find fill transaction in the BD4 messages.')
        for m in messages:
            if str(fillCallback.transaction_no) == (str(m.directed_trade.cl_trade_api.trade_number_i)):
                foundFill = True
                message = m
                break
        else:
            while foundFill == False:
                status, messages = self.omPipe.wait_for(bd4Msg, timeout = 15)
                if status == 'TIMEOUT':
                    log.error('OMPipe %s' % (status))
                    raise SGXException('OMPipe %s' % (status))
                else:
                    continue
        return message
        print '\nStill continuing, even though return statement has already been reached.\n'
        self.omPipe.clear()
    
    def getBD4Spreadmessage(self, closeOrder, orderCallbackLeg1, fillCallbackLeg1, orderCallbackLeg2, fillCallbackLeg2):
        '''This function invokes PacketPipe, grabs the BD4 messages  
    
        for Spreads and returns the data.
        
        This function expects to be passed the following:
        
        orderCallbackLeg1 = OnOrderFilled for Leg 1 of the Spread
        fillCallbackLeg1 = OnFillRecord for Leg 1 of the Spread
        orderCallbackLeg2 = OnOrderFilled for Leg 2 of the Spread
        fillCallbackLeg2 = OnFillRecord for Leg 2 of the Spread'''

        bd4Msg = self.bd4Msg
    
#------Capture PacketPipe messages for SPREADS.
        messagesLeg1 = None
        messagesLeg2 = None
        foundLeg1 = False
        foundLeg2 = False
        status, messages = self.omPipe.wait_for([bd4Msg, bd4Msg, bd4Msg, bd4Msg], timeout = 45)
        if status == 'TIMEOUT':
            log.error('OMPipe %s' % (status))
            raise SGXException('OMPipe %s' % (status))
        elif len(messages) == 0:
            log.error('Unable to find all transactions in the BD4 messages.')# % (fillCallback.transaction_no))
            raise SGXException('Unable to find all transactions in the BD4 messages.')
        for m in messages:
            if str(fillCallbackLeg1.transaction_no) == (str(m.directed_trade.cl_trade_api.trade_number_i)):
                foundLeg1 = True
                messagesLeg1 = m
            if str(fillCallbackLeg2.transaction_no) == (str(m.directed_trade.cl_trade_api.trade_number_i)):
                foundLeg2 = True
                messagesLeg2 = m
            if foundLeg1 == True and foundLeg2 == True:
                foundFill = True
                break
        else:
            while foundFill == False:
                status, messages = self.omPipe.wait_for(bd4Msg, timeout = 30)
                if status == 'TIMEOUT':
                    log.error('OMPipe %s' % (status))
                    raise SGXException('OMPipe %s' % (status))
                else:
                    continue
        return messagesLeg1, messagesLeg2

    def testRun(self):
        log.info(' Starting TestOrderServerFillValidate '.center(70, '*'))
        i = 1
        while i <= 15:
            log.info(' Beginning Test Pass #%s '.center(20, '#') % (i))
            self.validateFill()
            time.sleep(12)
            i += 1
        log.info(' TestOrderServerFillValidate Complete '.center(70, '*'))

if __name__ == '__main__':
    from pyrate import driver
    name = 'sgx.order_server.fills.TestOrderServerFillValidate'
    driver.run([name])