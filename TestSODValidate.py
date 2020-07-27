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

log = logging.getLogger(__name__)

class TestSODValidate():
    
    @classmethod
    def setUpClass(cls):
        cls.fillSession = TTAPIManager().getFillSession()
        cls.netPos = []

    def downloadSession1Fills(self):
#-----Downloads today's fills from the Fill Server and writes them to session1FillFile.txt
        netPos = []
        fillRecs = []
        CTTFillConsumer.RequestFillsToday(self.fillSession.consumer,323,1)
        fillDownload = self.fillSession.wait('OnFillRecord', timeout=10)
        self.fillElements=list(dir(fillDownload['OnFillRecord'][0]['cpFill']))[-48:]
        self.fillElements.remove('confirm_rec')
        for fillElement in self.fillElements:
            if fillElement == 'srs': fillSrs = getattr(fillDownload['OnFillRecord'][0]['cpFill'],fillElement)
            if fillElement == 'long_qty': buyQty = getattr(fillDownload['OnFillRecord'][0]['cpFill'],fillElement)
            if fillElement == 'short_qty': sellQty = (0 - getattr(fillDownload['OnFillRecord'][0]['cpFill'],fillElement))
        netPos = buyQty + sellQty
        fillRecs.append([fillSrs,netPos])
        while True:
            try:
                fillDownload = self.fillSession.wait('OnFillRecord', timeout=10)
                for fillElement in self.fillElements:
                    if fillElement == 'srs': fillSrs = getattr(fillDownload['OnFillRecord'][0]['cpFill'],fillElement)
                    if fillElement == 'long_qty': buyQty = getattr(fillDownload['OnFillRecord'][0]['cpFill'],fillElement)
                    if fillElement == 'short_qty': sellQty = (0 - getattr(fillDownload['OnFillRecord'][0]['cpFill'],fillElement))
                netPos = buyQty + sellQty
                for fillRecList in fillRecs:
                    if fillSrs == fillRecList[0]:
                        print 'For %s, Adding %s to %s' % (fillSrs, netPos, fillRecList[1])
                        fillRecList[1] += netPos
                    else:
                        print 'Creating new entry for %s, netPos = %s' % (fillSrs, netPos)
                        fillRecs.append([fillSrs,netPos])
            except:
                log.info('Fill download complete.')
                break
        print '\t| Series\t|| Position |\n'
        print '-----------------------------------------------\n'
        for fillRec in fillRecs:
            print '\t| %s\t|| %s           |\n' % (fillRec[0], fillRec[1])

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
    
    def testRun(self):
        log.info(' TestSODValidate '.center(80, '*'))
        self.downloadSession1Fills()
#        self.downloadSession2Fills()
#        self.validateCrossSessionFills()
        log.info(' TestSODValidate '.center(80, '*'))

if __name__ == '__main__':
    from pyrate import driver
    name = 'tocom.fill_server.TestSODValidate'
    driver.run([name])