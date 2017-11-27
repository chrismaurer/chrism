#~TestCaseName: logfile_analiser
#~TestCaseSummary: This program reads logfiles from C:\logs and returns any unexpected messages

'''.'''

__author__ = 'Chris Maurer (chris.maurer@tradingtechnologies.com)'
__version__ = '1.1'

import logging
from optparse import OptionParser

log = logging.getLogger(__name__)

class logfile_analiser():

    def optmenu(self):
        parser = OptionParser()
        parser.add_option('-f', '--file', dest='filename',
                          help='logfile to be read', metavar='filename')
        optmenu, args = parser.parse_args()
        return optmenu.filename

    def parseLogfile(self):

        OrderBookIDs = ['659370', '855071', '5574562', '132085', '265645', '16517077', '32182178', '37883810', '135074', '5836706', '855071', '16060718']

        logfile = self.optmenu()

        total_count = 10
        for OrderBookID in OrderBookIDs:
            print '-'*40, '1.1 A, Section 1: Ref Data', '-'*40
            inputFile = open(logfile, 'r')
            found = False
            count = 10
            in_file = False
            for line in inputFile.readlines():
                if 'msgType' in line and '[id:%s]' % OrderBookID in line:
                    print line
                    in_file = True
                    count += 1

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile2(self):

        OrderBookIDs = ['0',]

        logfile = self.optmenu()

        total_count = 8
        for OrderBookID in OrderBookIDs:
            print '-'*40, '1.1 A, Section 1: Ref Data (Next Day Effective Series)', '-'*40
            inputFile = open(logfile, 'r')
            found = False
            count = 0
            in_file = False
            for line in inputFile.readlines():
                if 'Contract Created' in line or '_DEFINITIONS' in line:
                    if '%s]' % OrderBookID in line and 'HSIQ4' in line:
                        count = 0
                        found = True
                if found:
                    if 'msgType' in line and '[id:%s]' % OrderBookID in line and 'HSIQ4' in line:
                        print line
                        in_file = True
                        count += 1

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile3(self):

        OrderBookIDs = ['63603457721892920', '63603457721892919']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '-'*40, '1.1 C, Trade and Trade Amend', '-'*40
            inputFile = open(logfile, 'r')
            found = False
            in_file = False
            for line in inputFile.readlines():
                if not found:
                    if '[tid:%s]' % OrderBookID in line:
                        found = True
                        in_file = True
                if found:
                    if '[tid:' in line and '[tid:%s]' % OrderBookID not in line:
                        found = False
                    elif ('tradeadjustment' in line or '[tid:%s]' % OrderBookID in line):
                        print line

            if not in_file:
                print 'Trade ID %s Not Found!' % OrderBookID
        
            inputFile.close()

    def parseLogfile4(self):

        OrderBookIDs = ['6229921', '397224']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '-'*40, '1.2 Test Case 11: Status Data', '-'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if OrderBookID in line:
                    if 'HandleMarketStatus' in line and 'obId:%s' % OrderBookID in line:
                        print line
                        in_file = True
                    elif 'Market Status Received' in line and 'o:%s' % OrderBookID in line:
                        print line
                        in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile5(self):

#        OrderBookIDs = ['5181346', '656373', '331181', '19531733', '55185314', '56823714', '135074', '5836706', '855071', '16060718']
        OrderBookIDs = ['16060718',]

        logfile = self.optmenu()

        total_count = 10
        for OrderBookID in OrderBookIDs:
            print '-'*40, '1.3 Session 2 (Refresh), Section 1: Ref Data', '-'*40
            inputFile = open(logfile, 'r')
            found = False
            count = 10
            in_file = False
            for line in inputFile.readlines():
                if 'msgType' in line and '%s]' % OrderBookID in line:
                    print line
                    in_file = True
                    count += 1

            inputFile.close()

            if not in_file:
                inputFile = open(logfile, 'r')
                for line in inputFile.readlines():
                    if '[id:%s]' % OrderBookID in line or '[combObId:%s]' % OrderBookID in line:
                        if 'msgType301' in line or 'msgType302' in line or 'msgType304' in line:
                            print line
                            in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

    def parseLogfile6(self):

        # OrderBookIDs = ['397218', '56758178', '4722593', '6229921', '41488290', '33755041', '659368', '397224',
        #                 '8458148', '37752740', '3018667', '135082', '19531733', '656373', '789933', '200622', '331700']
        OrderBookIDs = ['56758178', '6229921', '397224']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '-'*40, '1.3 Session 2 (Refresh), Section 2: Status Data', '-'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if 'HandleMarketStatus' in line and 'obId:%s' % OrderBookID in line:
                    print line
                    in_file = True
                elif 'Market Status Received' in line and 'o:%s' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

            inputFile.close()

logRead = logfile_analiser()
logRead.optmenu()
# logRead.parseLogfile()
# logRead.parseLogfile2()
# logRead.parseLogfile3()
# logRead.parseLogfile4()
logRead.parseLogfile5()
# logRead.parseLogfile6()
