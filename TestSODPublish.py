#~ TestCaseName: TestSODValidate
#~TestCaseSummary: Test Order Server Fill Validation by choosing a random product /from Market Finder/ and 
#                  Validating Fill Data. This test is meant to be repeated many times in succession.
#                  Due to time and resource constraints, the work required to run the test in a loop
#                  will be completed at a later time. For now this test will be run multiple times via
#                  manual testing, as "computer-assisted testing."
#~Exchange/Simulator/Both: Both
#~Pyrate Version: 2.0

'''Tests Fills and SODs across multiple trading sessions.'''

__author__ = 'Chris Maurer (chris.maurer@tradingtechnologies.com)'
__version__ = '1.0'

import logging
import time

from pyrate.builder import Builder
from pyrate.ttapi.manager import TTAPIManager
from pyrate import pipe
from pyrate.pipe.common import AnyFilter

from ttapi.cppclient import CTTFillConsumer
from ttapi.cppclient import TTFillSource

log = logging.getLogger(__name__)

class TestSODValidate():
    
    @classmethod
    def setUpClass(cls):
        cls.fillSession = TTAPIManager().getFillSession()

    def downloadSession1Fills(self):
#-----Downloads today's fills from the Fill Server and writes them to session1FillFile.txt
        fillFile = file('session1FillFile.txt', 'a')
        CTTFillConsumer.RequestFillsToday(self.fillSession.consumer,323,1)
        fillDownload = self.fillSession.wait('OnFillRecord', timeout=10)
        self.fillElements=list(dir(fillDownload['OnFillRecord'][0]['cpFill']))[-48:]
        self.fillElements.remove('confirm_rec')
        for fillElement in self.fillElements:
            fillFile.write(str(getattr(fillDownload['OnFillRecord'][0]['cpFill'],fillElement))+',')
        fillFile.write('\n')
        while True:
            try:
                fillDownload = self.fillSession.wait('OnFillRecord', timeout=10)
                for fillElement in self.fillElements:
                    fillFile.write(str(getattr(fillDownload['OnFillRecord'][0]['cpFill'],fillElement))+',')
                fillFile.write('\n')
            except:
                break
        fillFile.close()

    def downloadSession2Fills(self):
#-----Reads session1FillFile.txt, Downloads today's fills from the Fill Server
        fillFile = file('session2FillFile.txt', 'a')
        CTTFillConsumer.RequestFillsToday(self.fillSession.consumer,323,1)
        fillDownload = self.fillSession.wait('OnFillRecord', timeout=10)
        self.fillElements=list(dir(fillDownload['OnFillRecord'][0]['cpFill']))[-48:]
        self.fillElements.remove('confirm_rec')
        for fillElement in self.fillElements:
            fillFile.write(str(getattr(fillDownload['OnFillRecord'][0]['cpFill'],fillElement))+',')
        fillFile.write('\n')
        while True:
            try:
                fillDownload = self.fillSession.wait('OnFillRecord', timeout=10)
                for fillElement in self.fillElements:
                    fillFile.write(str(getattr(fillDownload['OnFillRecord'][0]['cpFill'],fillElement))+',')
                fillFile.write('\n')
            except:
                break
        fillFile.close()

    def validateCrossSessionFills(self):
        session1Fills = file('session1FillFile.txt', 'r')
        session2Fills = file('session2FillFile.txt', 'r')
        for line in session1Fills.readlines():
            lineList = str(line).split('/n')
            lineListStr = str(lineList).split(',')
            session1FillsDict = dict.fromkeys(self.fillElements)
            for k in session1FillsDict:
                if str(k) == 'acct': session1FillsDict[k] = str(lineListStr[0]).lstrip('[\'')
                elif str(k) == 'buy_sell': session1FillsDict[k] = lineListStr[1]
                elif str(k) == 'exch_group': session1FillsDict[k] = lineListStr[7]
                elif str(k) == 'exch_member': session1FillsDict[k] = lineListStr[8]
                elif str(k) == 'exch_trader': session1FillsDict[k] = lineListStr[9]
                elif str(k) == 'exchange_order_id': session1FillsDict[k] = lineListStr[10]
                elif str(k) == 'fee_code': session1FillsDict[k] = lineListStr[12]
                elif str(k) == 'fillKey': session1FillsDict[k] = lineListStr[13]
                elif str(k) == 'fill_cmb_code': session1FillsDict[k] = lineListStr[14]
                elif str(k) == 'free_text0': session1FillsDict[k] = lineListStr[15]
                elif str(k) == 'free_text1': session1FillsDict[k] = lineListStr[16]
                elif str(k) == 'free_text2': session1FillsDict[k] = lineListStr[17]
                elif str(k) == 'giveup_mbr': session1FillsDict[k] = lineListStr[18]
                elif str(k) == 'clearing_mbr': session1FillsDict[k] = lineListStr[18]
                elif str(k) == 'group_id': session1FillsDict[k] = lineListStr[19]
                elif str(k) == 'iSession': session1FillsDict[k] = lineListStr[20]
                elif str(k) == 'long_qty': session1FillsDict[k] = lineListStr[21]
                elif str(k) == 'match_prc': session1FillsDict[k] = lineListStr[22]
                elif str(k) == 'member_id': session1FillsDict[k] = lineListStr[23]
                elif str(k) == 'open_close': session1FillsDict[k] = lineListStr[24]
                elif str(k) == 'order_date': session1FillsDict[k] = lineListStr[25]
                elif str(k) == 'order_no': session1FillsDict[k] = lineListStr[27]
                elif str(k) == 'order_restrict': session1FillsDict[k] = lineListStr[28]
                elif str(k) == 'trans_time': session1FillsDict[k] = lineListStr[29]
                elif str(k) == 'order_type': session1FillsDict[k] = lineListStr[30]
                elif str(k) == 'partial_fill': session1FillsDict[k] = lineListStr[32]
                elif str(k) == 'record_no': session1FillsDict[k] = lineListStr[33]
                elif str(k) == 'site_order_key': session1FillsDict[k] = lineListStr[35]
                elif str(k) == 'source': session1FillsDict[k] = lineListStr[36]
                elif str(k) == 'srs': session1FillsDict[k] = lineListStr[38]
                elif str(k) == 'trader_id': session1FillsDict[k] = lineListStr[39]
                elif str(k) == 'trans_date': session1FillsDict[k] = lineListStr[42]
                elif str(k) == 'order_time': session1FillsDict[k] = lineListStr[43]
                elif str(k) == 'transaction_no': session1FillsDict[k] = lineListStr[44]
                elif str(k) == 'user_name': session1FillsDict[k] = lineListStr[45]
                elif str(k) == 'wrk_qty': session1FillsDict[k] = lineListStr[46]
                elif str(k) == 'trans_code': session1FillsDict[k] = lineListStr[2]
                elif str(k) == 'origin': session1FillsDict[k] = lineListStr[3]
                elif str(k) == 'subUserId': session1FillsDict[k] = lineListStr[4]
                elif str(k) == 'cash_prc': session1FillsDict[k] = lineListStr[5]
                elif str(k) == 'order_flags': session1FillsDict[k] = lineListStr[6]
                elif str(k) == 'cti_code': session1FillsDict[k] = lineListStr[11]
                elif str(k) == 'cntr_clg': session1FillsDict[k] = lineListStr[26]
                elif str(k) == 'short_qty': session1FillsDict[k] = lineListStr[31]
                elif str(k) == 'cntr_party': session1FillsDict[k] = lineListStr[34]
                elif str(k) == 'fee_amount': session1FillsDict[k] = lineListStr[37]
                elif str(k) == 'source_id': session1FillsDict[k] = lineListStr[40]
                elif str(k) == 'unknown1': session1FillsDict[k] = lineListStr[41]
                elif str(k) == 'unknown2': session1FillsDict[k] = lineListStr[42]
#        session2lines = session2Fills.readlines()
#        session2FillsDict = dict.fromkeys(self.fillElements,session2lines)
        print '\nlen(lineListStr) = %s\n' % (len(lineListStr))
        print '\n---------------- session1FillsDict: -------------------\n'
        print session1FillsDict
#        print '\n---------------- session2FillsDict: -------------------\n'
#        print session2FillsDict
#        print '\n-------------------------------------------------------\n'
    
    def testRun(self):
        log.info(' TestSODValidate '.center(80, '*'))
        self.downloadSession1Fills()
#        self.downloadSession2Fills()
        self.validateCrossSessionFills()
        log.info(' TestSODValidate '.center(80, '*'))

if __name__ == '__main__':
    from pyrate import driver
    name = 'tocom.fill_server.TestSODValidate'
    driver.run([name])