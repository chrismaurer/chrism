#~ TestCaseName: TestChangeOfCalendarDate
#~TestCaseSummary: Test Order Server Fill Download during a single Clearing Date when Calendar date
#~                 has changed.
#~TO DO: Fix test code so that it is not dependent on a hard-coded Exchange ID!
#~Exchange/Simulator/Both: Both
#~Pyrate Version: 2.0

'''TESTCASE 124696: Verify download of Fills occuring across Calendar dates but within same Clearing Date.'''

__author__ = 'Chris Maurer (chris.maurer@tradingtechnologies.com)'
__version__ = '1.3'

import logging
import time
import os

from pyrate import util
from pyrate.builder import Builder
from pyrate.ttapi.manager import TTAPIManager
from pyrate import pipe
from pyrate.pipe.common import AnyFilter

from ttapi.cppclient import CTTFillConsumer

from tocom.lib.Exceptions import TOCOMException
from tocom.lib.OMSimpleOrder import OMSimpleOrder
from tocom.lib.TTAPIValidator import validateFill

log = logging.getLogger(__name__)

class TestChangeOfCalendarDate():

    @classmethod
    def setUpClass(cls):
        cls.fillSession = TTAPIManager().getFillSession()
        cls.orderSession = TTAPIManager().getOrderSession()
        cls.prcSrv = TTAPIManager().getPriceServer()
        cls.ordSrv = TTAPIManager().getOrderServer()
        cls.filSrv = TTAPIManager().getFillServer()
        cls.fillsList = []
        cls.fillRecs = []

    def createOrders(self):
        counter = 0
        while True:
            if counter >= 8: break
            messages = OMSimpleOrder(getFill=True, f_callbax=True)
            self.fillsList.append(messages['fillData'])
            counter += 1

    def downloadFills(self):
        netPos = []
        self.fillRecs = []
        CTTFillConsumer.RequestFillsToday(self.fillSession.consumer,323,1)
        while True:
            try:
                fillDownload = self.fillSession.wait('OnFillRecord', timeout=10)
                dLoadedFill = fillDownload['OnFillRecord'][0]['cpFill']
                for fill in self.fillsList:
                    if dLoadedFill.site_order_key == fill.site_order_key:
                        self.fillRecs.append(dLoadedFill)
            except:
                log.info('Fill download complete.')
                break

    def validateFills(self):
        validationPassed = True
        for fillRec in self.fillRecs:
            for fill in self.fillsList:
                if fill.site_order_key == fillRec.site_order_key:
                    #iSession will not be validated in this test, so the value is being
                    #copied from downloaded fill into generated fill here to prevent
                    #misleading validation errors.
                    fill.iSession = fillRec.iSession
                    #DEF 124501: When fills are re-downloaded from the Exchange, Acct, Clearing Mbr and Account# are wrong.
#                    fill.acct = fillRec.acct
#                    fill.user_name = fillRec.user_name
                    log.info('... Validating Fill %s ...' % (fill.site_order_key))
                    fillIndex = self.fillsList.index(fill)
                    genFill = self.fillsList.pop(fillIndex)
                    validationPassed = validateFill(genFill, fillRec) and validationPassed

        return validationPassed

    def checkData(self):
        if len(self.fillsList) != 0:
            log.error('The following Fill(s) went missing during the order server restart:')
            for missingFill in self.fillsList:
                log.error('%s' % (missingFill.site_order_key))
            return False
        else:
            log.info('((( All Fills persisted during the change of Calendar day. )))')
            return True

    def clearDatfiles(self):
        rootDir = util.readRegistryValue(self.prcSrv.ip,\
                                            r"HKEY_LOCAL_MACHINE\SOFTWARE\Trading Technologies\Installation", "INSTALLROOT")
        installDrive = str(rootDir).rstrip(r':\tt')
        datfilesDir = util.readRegistryValue(self.prcSrv.ip,\
                                            r'HKEY_LOCAL_MACHINE\SOFTWARE\Trading Technologies\Installation', 'DATFILEDIR')
        datfilesPath = r'\\' + self.prcSrv.ip + '\\' + installDrive + '$' + str(datfilesDir).lstrip(str(installDrive + ':'))
        targetFiles = ['_bof', '_fills', 'Store']
        for filename in os.listdir(datfilesPath):
            for targetFile in targetFiles:
                if targetFile in filename:
                    log.info('Deleting %s' % (str(datfilesPath + '\\' + filename)))
                    os.remove(datfilesPath + '\\' + filename)

    def testRun(self):
        log.info(' TestChangeOfCalendarDate '.center(80, '*'))
        testPassed = True
#        time.sleep(5160)
        self.createOrders()
        self.ordSrv.stop()
        self.filSrv.stop()
        time.sleep(8)
#        time.sleep(240)
        self.clearDatfiles()
        self.ordSrv.start(timeout=180)
        self.filSrv.start()
        time.sleep(3)
        self.downloadFills()
        validation1 = self.validateFills()
        validation2 = self.checkData()
        testPassed = True if all([validation1, validation2]) else False
        if testPassed == True:
            log.info('Test Passed.')
        elif testPassed == False:
            log.error('Test FAILED due to previous errors!')
        else:
            log.error('Unable to get Validation results.')
            raise TOCOMException('Unable to get Validation results.')
        time.sleep(1)
        self.orderSession.deleteAllOrders()
        log.info(' TestChangeOfCalendarDate '.center(80, '*'))

if __name__ == '__main__':
    from pyrate import driver
    name = 'tocom.fill_server.TestChangeOfCalendarDate'
    driver.run([name])