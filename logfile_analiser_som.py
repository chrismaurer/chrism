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

        OrderBookIDs = ['14551380', '12060010', '4294838229']

        logfile = self.optmenu()

        total_count = 16
        for OrderBookID in OrderBookIDs:
            print '-'*40, '1.1 A, Section 1: Ref Data', '-'*40
            inputFile = open(logfile, 'r')
            found = False
            count = 16
            in_file = False
            for line in inputFile.readlines():
                if 'msgType' in line and '%s]' % OrderBookID in line:
                    print line
                    in_file = True
                    count += 1

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile02(self):

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
                    if '%s]' % OrderBookID in line and 'RKB75.00X3' in line:
                        count = 0
                        found = True
                if found:
                    if 'msgType' in line and '[id:%s]' % OrderBookID in line and 'RKB75.00X3' in line:
                        print line
                        in_file = True
                        count += 1

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile03(self):

        OrderBookIDs = ['14355207', '13568241']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '-'*40, '1.1 A, Section 2: Series Status Data', '-'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if 'Series Status Received [obId:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile03a(self):

        OrderBookIDs = ['2211', '2289']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '-'*40, '1.1 A, Section 2: Commodity Status Data', '-'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if 'Commodity Status Received [code:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile04(self):

        OrderBookIDs = ['1771477',]

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '-'*40, '1.1 A, Section 3: Order Book Data', '-'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if 'quoterequest' in line and OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile05(self):

        OrderBookIDs = ['4294903765', '4294838229', '4294772693']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '-'*40, '1.1 B, Order Book Building TC 42-44', '-'*40
            inputFile = open(logfile, 'r')
            found = False
            in_file = False
            for line in inputFile.readlines():
                if not found:
                    if '[oid:%s]' % OrderBookID in line:
                        found = True
                        in_file = True
                if found:
                    if '[oid:' in line and '[oid:%s]' % OrderBookID not in line:
                        found = False
                    # if '[oid:' not in line and 'Deal Type' not in line:
                    #     found = False
                    # if ('Deal Type' in line or '[tid:%s]' % OrderBookID in line):
                    print line

            if in_file:
                print 'Order ID %s is not supposed to be logged!' % OrderBookID
            else:
                print 'Passed.'

            inputFile.close()

    def parseLogfile06(self):

        OrderBookIDs = ['6360365808211812479', '6360365808211812478', '6360365808211812477',
                        '6360365808211812476', '6360365808211812475', '6360365808211812470',
                        '6360365808211812469', '6360365808211812468', '6360365808211812467',
                        '6360365808211812466', '6360365808211812465']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '-'*40, '1.1 B, Order Book Building TC 50', '-'*40
            inputFile = open(logfile, 'r')
            found = False
            in_file = False
            for line in inputFile.readlines():
                if not found:
                    if '[oid:%s]' % OrderBookID in line:
                        found = True
                        in_file = True
                if found:
                    if '[oid:' in line and '[oid:%s]' % OrderBookID not in line:
                        found = False
                    # if '[oid:' not in line and 'Deal Type' not in line:
                    #     found = False
                    # if ('Deal Type' in line or '[tid:%s]' % OrderBookID in line):
                    print line

            if not in_file:
                print 'Order ID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile07(self):

        OrderBookIDs = ['15339412', '15404948', '15076219', '1771477', '2885589', '1837013',
                        '853973', '985045', '1116117', '1312725', '1443797', '1574869', '1705941']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '-'*40, '1.1 B, Order Book Building TC 51-63', '-'*40
            inputFile = open(logfile, 'r')
            found = False
            in_file = False
            for line in inputFile.readlines():
                if not found:
                    if 'Add Order [id:%s]' % OrderBookID in line:
                        found = True
                        in_file = True
                if found:
                    if '[oid:' in line and '[oid:%s]' % OrderBookID not in line:
                        found = False
                    # if '[oid:' not in line and 'Deal Type' not in line:
                    #     found = False
                    # if ('Deal Type' in line or '[tid:%s]' % OrderBookID in line):
                    print line

            if not in_file:
                print 'Order ID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile07a(self):

        OrderBookIDs = ['63603453426925640',]

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '-'*40, '1.1 C, Trade and Trade Amend, TC 33', '-'*40
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

    def parseLogfile07b(self):

        OrderBookIDs = ['63603453426925645',]

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '-'*40, '1.1 C, Trade and Trade Amend, TC 34', '-'*40
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

    def parseLogfile07c(self):

        OrderBookIDs = ['63603453426925652',]

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '-'*40, '1.1 C, Trade and Trade Amend, TC 35', '-'*40
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

    def parseLogfile08(self):

        OrderBookIDs = ['63603453426925569', '63603453426925570', '63603453426925571',
                        '63603453426925572', '63603453426925573', '63603453426925574',
                        '63603453426925575', '63603453426925576', '63603453426925577',
                        '63603453426925578', '63603453426925579', '63603453426925580',
                        '63603453426925581',
                        '63603453426925582', '63603453426925583', '63603453426925584',
                        '63603453426925585', '63603453426925586', '63603453426925587',
                        '63603453426925588', '63603453426925589', '63603453426925590',
                        '63603453426925591', '63603453426925592', '63603453426925593',
                        '63603453426925594', '63603453426925595', '63603453426925596',
                        '63603453426925597', '63603453426925598', '63603453426925599',
                        '63603453426925600', '63603453426925601', '63603453426925602',
                        '63603453426925603', '63603453426925604', '63603453426925605',
                        '63603453426925606', '63603453426925607', '63603453426925608',
                        '63603453426925609', '63603453426925611', '63603453426925612']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '-'*40, '1.1 C, Trade and Trade Amend, TC 36', '-'*40
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

    def parseLogfile09(self):

        OrderBookIDs = ['63603453426925641', '63603453426925646', '63603453426925653']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '-'*40, '1.1 C, Trade and Trade Amend, TC 37', '-'*40
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

    def parseLogfile10(self):

        OrderBookIDs = ['63603453426925642', '63603453426925647', '63603453426925654']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '-'*40, '1.1 C, Trade and Trade Amend, TC 38', '-'*40
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

    def parseLogfile11(self):

        OrderBookIDs = ['63603453426925667',]

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '-'*40, '1.1 C, Trade and Trade Amend, TC 39', '-'*40
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

    def parseLogfile12(self):

        OrderBookIDs = ['63603453426925637', '63603453426925638']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '-'*40, '1.1 C, Trade and Trade Amend, TC 40', '-'*40
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

    def parseLogfile13(self):

        OrderBookIDs = ['63603453426925661', ]

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '-'*40, '1.1 C, Trade and Trade Amend, TC 41', '-'*40
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

    def parseLogfile14(self):

        OrderBookIDs = ['63603453426925663', ]

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '-'*40, '1.1 C, Trade and Trade Amend, TC 42', '-'*40
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

    def parseLogfile18(self):

        OrderBookIDs = ['9110890', '10290538', '265083']

        logfile = self.optmenu()

        total_count = 10
        for OrderBookID in OrderBookIDs:
            print '-'*40, '1.3 Session 1 (Refresh), Section 1: Ref Data', '-'*40
            inputFile = open(logfile, 'r')
            found = False
            count = 10
            in_file = False
            for line in inputFile.readlines():
                if 'msgType' in line and '%s]' % OrderBookID in line and '29.01.2015 08' not in line:
                    print line
                    in_file = True
                    count += 1

            if not in_file:
                print 'Trade ID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile15(self):

        OrderBookIDs = ['6360763006787295501',
                        '6360763006787295502',
                        '6360763006787295504',
                        '6360763006787295506',
                        '6360763006787295507',
                        '6360763006787295508',
                        '6360763006787295509',
                        '6360763006787295510',
                        '6360763006787295511',
                        '6360763006787295512',
                        '6360763006787295513']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '-'*40, '1.3 Section 10, Order Book Building', '-'*40
            inputFile = open(logfile, 'r')
            found = False
            in_file = False
            for line in inputFile.readlines():
                if not found:
                    if '[oid:%s]' % OrderBookID in line:
                        found = True
                        in_file = True
                if found:
                    if '[oid:' in line and '[oid:%s]' % OrderBookID not in line:
                        found = False
                    # if '[oid:' not in line and 'Deal Type' not in line:
                    #     found = False
                    # if ('Deal Type' in line or '[tid:%s]' % OrderBookID in line):
                    print line

            if not in_file:
                print 'Order ID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile16(self):

        OrderBookIDs = ['63607576595529735',
                        '63607576595529737',
                        '63607576595529732',
                        '63607576595529738',
                        '63607576595529739',
                        '63607576595529729']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '-'*40, '1.4 Session 3 Data Recovery (Line Arb & Retrans) TC 4', '-'*40
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
                    if '[tid:' not in line and 'Deal Type' not in line:
                        found = False
                    if ('Deal Type' in line or '[tid:%s]' % OrderBookID in line):
                        print line

            if not in_file:
                print 'Order ID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile17(self):

        OrderBookIDs = ['1771477',]

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '-'*40, '1.2 1B Test Case 11: Status Data', '-'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if OrderBookID in line and 'HandleMarketStatus' in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile19(self):

        OrderBookIDs = ['657365',]

        logfile = self.optmenu()

        total_count = 10
        for OrderBookID in OrderBookIDs:
            print '-'*40, '1.3 Session 1 (Refresh), Section 1: Ref Data', '-'*40
            inputFile = open(logfile, 'r')
            found = False
            count = 10
            in_file = False
            for line in inputFile.readlines():
                if 'msgType' in line and '%s]' % OrderBookID in line and '29.01.2015 08' not in line:
                    print line
                    in_file = True
                    count += 1

            if not in_file:
                print 'Trade ID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile20(self):

        OrderBookIDs = ['1771477',]

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '-'*40, '1.4 Session 3 Data Recovery (Line Arb & Retrans) TC 2', '-'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if 'quoterequest' in line and OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

            inputFile.close()

logRead = logfile_analiser()
logRead.optmenu()
# logRead.parseLogfile()
# logRead.parseLogfile02()
# logRead.parseLogfile03()
# logRead.parseLogfile03a()
# logRead.parseLogfile04()
# logRead.parseLogfile05()
# logRead.parseLogfile06()
# logRead.parseLogfile07()
# logRead.parseLogfile07a()
# logRead.parseLogfile07b()
# logRead.parseLogfile07c()
# logRead.parseLogfile08()
# logRead.parseLogfile09()
# logRead.parseLogfile10()
# logRead.parseLogfile11()
# logRead.parseLogfile12()
# logRead.parseLogfile13()
# logRead.parseLogfile14()
# logRead.parseLogfile15()
# logRead.parseLogfile16()
# logRead.parseLogfile17()
# logRead.parseLogfile18()
logRead.parseLogfile19()
# logRead.parseLogfile20()