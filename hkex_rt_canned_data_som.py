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

    def parseLogfile01a(self):

        OrderBookIDs = ['3934548', '8587221', '8591318', '4294707157']

        logfile = self.optmenu()

        total_count = 16
        for OrderBookID in OrderBookIDs:
            print '\n\n', '-'*40, 'Session 1 - Test case 1, Scenario', OrderBookIDs.index(OrderBookID)+14,': Interpretation of Reference Data', '-'*40, '\n\n'
            inputFile = open(logfile, 'r')
            found = False
            count = 16
            in_file = False
            for line in inputFile.readlines():
                if 'msgType' in line and '[id:%s]' % OrderBookID in line:
                    print line
                    in_file = True
                    count += 1

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile01b(self):

        OrderBookIDs = ['0',]

        logfile = self.optmenu()

        total_count = 8
        for OrderBookID in OrderBookIDs:
            print '\n\n', '-'*40, 'Session 1 - Test case 1, Scenario 18: Ref Data (Next Day Effective Series)', '-'*40, '\n\n'
            inputFile = open(logfile, 'r')
            found = False
            count = 0
            in_file = False
            for line in inputFile.readlines():
                if 'Contract Created' in line or '_DEFINITIONS' in line:
                    if '[id:%s]' % OrderBookID in line and 'CPA9.25C9' in line:
                        count = 0
                        found = True
                if found:
                    if 'msgType' in line and '[id:%s]' % OrderBookID in line or 'CPA9.25C9' in line:
                        print line
                        in_file = True
                        count += 1

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile03(self):

        OrderBookIDs = ['31983579', '18940948', '11012086']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '\n\n', '-'*40, 'Session 1 - Test case 3: Interpretation of Status Data: Series Status', '-'*40, '\n\n'
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

    def parseLogfile08(self):

        obID_prcs = [['57411540', '-2147483648)'], ]

        logfile = self.optmenu()

        for obID_prc in obID_prcs:
            print '\n\n', '-'*40, 'Session 1 - Test case 8: Interpretation of Trade and Price Data : Calculated Opening Price', '-'*40, '\n\n'
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if all(obID_prc_values in line for obID_prc_values in obID_prc):
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % obID_prc

            inputFile.close()

    def parseLogfile141d(self):

        OrderBookIDs = ['1771400', ]

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 14: Section D: Full Order Book Scenario 1 - D', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if '[id:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile142d(self):

        OrderBookIDs = ['1050581', ]

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 14: Section D: Full Order Book Scenario 2 - D', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if '[id:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile143d(self):

        OrderBookIDs = ['1181653', ]

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 14: Section D: Full Order Book Scenario 3 - D', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if '[id:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile144d(self):

        OrderBookIDs = ['7021030734383099705',
                        '7021030734383099704',
                        '7021030734383099703',
                        '7021030734383099702',
                        '7021030734383099701',
                        '7021030734383099700',
                        '7021030734383099699',
                        '7021030734383099698',
                        '7021030734383099697',
                        '7021030734383099696',
                        '7021030734383099695']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 14: Section D: Full Order Book Scenario 4 - D', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if 'Add Order [id:3867733] [oid:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile145d(self):

        OrderBookIDs = ['7021030734383099721',
                        '7021030734383099720',
                        '7021030734383099719',
                        '7021030734383099718',
                        '7021030734383099717',
                        '7021030734383099716',
                        '7021030734383099715',
                        '7021030734383099714',
                        '7021030734383099713',
                        '7021030734383099712',
                        '7021030734383099711']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 14: Section D: Full Order Book Scenario 5 - D', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if 'Add Order [id:1573973] [oid:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile146d(self):

        OrderBookIDs = ['7021030734383099734',
                        '7021030734383099732',
                        '7021030734383099731',
                        '7021030734383099730',
                        '7021030734383099736',
                        '7021030734383099728',
                        '7021030734383099727',
                        '7021030734383099726',
                        '7021030734383099725',
                        '7021030734383099724',
                        '7021030734383099723']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 14: Section D: Full Order Book Scenario 6 - D', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if 'Add Order [id:9372757] [oid:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile147d(self):

        OrderBookIDs = ['4294707157', ]

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 14: Section D: Full Order Book Scenario 7 - D', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if '[id:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile148d(self):

        OrderBookIDs = ['4294641621', ]

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 14: Section D: Full Order Book Scenario 8 - D', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if '[id:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile149d(self):

        OrderBookIDs = ['7021030734383099808',
                        '7021030734383099809',
                        '7021030734383099810',
                        '7021030734383099811',
                        '7021030734383099812',
                        '7021030734383099813',
                        '7021030734383099814',
                        '7021030734383099815',
                        '7021030734383099816',
                        '7021030734383099817',
                        '7021030734383099818',
                        '7021030734383099831',
                        '7021030734383099820',
                        '7021030734383099821',
                        '7021030734383099822',
                        '7021030734383099823',
                        '7021030734383099824',
                        '7021030734383099825',
                        '7021030734383099826',
                        '7021030734383099827',
                        '7021030734383099828',
                        '7021030734383099829',
                        '7021030734383099830']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 14: Section D: Full Order Book Scenario 9 - D', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if 'Add Order [id:5048277] [oid:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile1410d(self):

        OrderBookIDs = ['7021030734383099694', ]

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 14: Section D: Full Order Book Scenario 10 - D', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if 'Add Order [id:7604181] [oid:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile1411d(self):

        OrderBookIDs = ['7021030734383099743',
                        '7021030734383099722',
                        '7021030734383099729',
                        '7021030734383099733',
                        '7021030734383099735',
                        '7021030734383099737',
                        '7021030734383099738',
                        '7021030734383099739',
                        '7021030734383099740',
                        '7021030734383099741',
                        '7021030734383099742']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 14: Section D: Full Order Book Scenario 11 - D', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if 'Add Order [id:7276501] [oid:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile1412d(self):

        OrderBookIDs = ['7021030734383099762',
                        '7021030734383099763',
                        '7021030734383099764',
                        '7021030734383099765',
                        '7021030734383099766',
                        '7021030734383099767',
                        '7021030734383099768',
                        '7021030734383099769',
                        '7021030734383099770',
                        '7021030734383099771']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 14: Section D: Full Order Book Scenario 12 - D', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if 'Add Order [id:7407573] [oid:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile1413d(self):

        OrderBookIDs = ['7021030734383099706', ]

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 14: Section D: Full Order Book Scenario 13 - D', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if 'Add Order [id:3606485] [oid:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile1414d(self):

        OrderBookIDs = ['7021030734383099774',
                        '7021030734383099775',
                        '7021030734383099776',
                        '7021030734383099777',
                        '7021030734383099778',
                        '7021030734383099779',
                        '7021030734383099780',
                        '7021030734383099781',
                        '7021030734383099782',
                        '7021030734383099783',
                        '7021030734383099785']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 14: Section D: Full Order Book Scenario 14 - D', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if 'Add Order [id:10684373] [oid:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile1415d(self):

        OrderBookIDs = ['7021030734383099786',
                        '7021030734383099787',
                        '7021030734383099788',
                        '7021030734383099789',
                        '7021030734383099790',
                        '7021030734383099791',
                        '7021030734383099792',
                        '7021030734383099793',
                        '7021030734383099794',
                        '7021030734383099795',
                        '7021030734383099796',
                        '7021030734383099807',
                        '7021030734383099798',
                        '7021030734383099799',
                        '7021030734383099800',
                        '7021030734383099801',
                        '7021030734383099802',
                        '7021030734383099803',
                        '7021030734383099804',
                        '7021030734383099805',
                        '7021030734383099806']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 14: Section D: Full Order Book Scenario 15 - D', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if 'Add Order [id:5113813] [oid:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()


    # def parseLogfile05(self):
    #
    #     OrderBookIDs = ['4294903765', '4294838229', '4294772693']
    #
    #     logfile = self.optmenu()
    #
    #     for OrderBookID in OrderBookIDs:
    #         print '\n\n', '-'*40, '1.1 B, Order Book Building TC 42-44', '-'*40, '\n\n'
    #         inputFile = open(logfile, 'r')
    #         found = False
    #         in_file = False
    #         for line in inputFile.readlines():
    #             if not found:
    #                 if '[oid:%s]' % OrderBookID in line:
    #                     found = True
    #                     in_file = True
    #             if found:
    #                 if '[oid:' in line and '[oid:%s]' % OrderBookID not in line:
    #                     found = False
    #                 # if '[oid:' not in line and 'Deal Type' not in line:
    #                 #     found = False
    #                 # if ('Deal Type' in line or '[tid:%s]' % OrderBookID in line):
    #                 print line
    #
    #         if in_file:
    #             print 'Order ID %s is not supposed to be logged!' % OrderBookID
    #         else:
    #             print 'Passed.'
    #
    #         inputFile.close()
    #
    # def parseLogfile06(self):
    #
    #     OrderBookIDs = ['6360365808211812479', '6360365808211812478', '6360365808211812477',
    #                     '6360365808211812476', '6360365808211812475', '6360365808211812470',
    #                     '6360365808211812469', '6360365808211812468', '6360365808211812467',
    #                     '6360365808211812466', '6360365808211812465']
    #
    #     logfile = self.optmenu()
    #
    #     for OrderBookID in OrderBookIDs:
    #         print '\n\n', '-'*40, '1.1 B, Order Book Building TC 50', '-'*40, '\n\n'
    #         inputFile = open(logfile, 'r')
    #         found = False
    #         in_file = False
    #         for line in inputFile.readlines():
    #             if not found:
    #                 if '[oid:%s]' % OrderBookID in line:
    #                     found = True
    #                     in_file = True
    #             if found:
    #                 if '[oid:' in line and '[oid:%s]' % OrderBookID not in line:
    #                     found = False
    #                 # if '[oid:' not in line and 'Deal Type' not in line:
    #                 #     found = False
    #                 # if ('Deal Type' in line or '[tid:%s]' % OrderBookID in line):
    #                 print line
    #
    #         if not in_file:
    #             print 'Order ID %s Not Found!' % OrderBookID
    #
    #         inputFile.close()
    #
    # def parseLogfile07(self):
    #
    #     OrderBookIDs = ['15339412', '15404948', '15076219', '1771477', '2885589', '1837013',
    #                     '853973', '985045', '1116117', '1312725', '1443797', '1574869', '1705941']
    #
    #     logfile = self.optmenu()
    #
    #     for OrderBookID in OrderBookIDs:
    #         print '\n\n', '-'*40, '1.1 B, Order Book Building TC 51-63', '-'*40, '\n\n'
    #         inputFile = open(logfile, 'r')
    #         found = False
    #         in_file = False
    #         for line in inputFile.readlines():
    #             if not found:
    #                 if 'Add Order [id:%s]' % OrderBookID in line:
    #                     found = True
    #                     in_file = True
    #             if found:
    #                 if '[oid:' in line and '[oid:%s]' % OrderBookID not in line:
    #                     found = False
    #                 # if '[oid:' not in line and 'Deal Type' not in line:
    #                 #     found = False
    #                 # if ('Deal Type' in line or '[tid:%s]' % OrderBookID in line):
    #                 print line
    #
    #         if not in_file:
    #             print 'Order ID %s Not Found!' % OrderBookID
    #
    #         inputFile.close()
    #
    # def parseLogfile07a(self):
    #
    #     OrderBookIDs = ['63603453426925640',]
    #
    #     logfile = self.optmenu()
    #
    #     for OrderBookID in OrderBookIDs:
    #         print '\n\n', '-'*40, '1.1 C, Trade and Trade Amend, TC 33', '-'*40, '\n\n'
    #         inputFile = open(logfile, 'r')
    #         found = False
    #         in_file = False
    #         for line in inputFile.readlines():
    #             if not found:
    #                 if '[tid:%s]' % OrderBookID in line:
    #                     found = True
    #                     in_file = True
    #             if found:
    #                 if '[tid:' in line and '[tid:%s]' % OrderBookID not in line:
    #                     found = False
    #                 elif ('tradeadjustment' in line or '[tid:%s]' % OrderBookID in line):
    #                     print line
    #
    #         if not in_file:
    #             print 'Trade ID %s Not Found!' % OrderBookID
    #
    #         inputFile.close()
    #
    # def parseLogfile07b(self):
    #
    #     OrderBookIDs = ['63603453426925645',]
    #
    #     logfile = self.optmenu()
    #
    #     for OrderBookID in OrderBookIDs:
    #         print '\n\n', '-'*40, '1.1 C, Trade and Trade Amend, TC 34', '-'*40, '\n\n'
    #         inputFile = open(logfile, 'r')
    #         found = False
    #         in_file = False
    #         for line in inputFile.readlines():
    #             if not found:
    #                 if '[tid:%s]' % OrderBookID in line:
    #                     found = True
    #                     in_file = True
    #             if found:
    #                 if '[tid:' in line and '[tid:%s]' % OrderBookID not in line:
    #                     found = False
    #                 elif ('tradeadjustment' in line or '[tid:%s]' % OrderBookID in line):
    #                     print line
    #
    #         if not in_file:
    #             print 'Trade ID %s Not Found!' % OrderBookID
    #
    #         inputFile.close()
    #
    # def parseLogfile07c(self):
    #
    #     OrderBookIDs = ['63603453426925652',]
    #
    #     logfile = self.optmenu()
    #
    #     for OrderBookID in OrderBookIDs:
    #         print '\n\n', '-'*40, '1.1 C, Trade and Trade Amend, TC 35', '-'*40, '\n\n'
    #         inputFile = open(logfile, 'r')
    #         found = False
    #         in_file = False
    #         for line in inputFile.readlines():
    #             if not found:
    #                 if '[tid:%s]' % OrderBookID in line:
    #                     found = True
    #                     in_file = True
    #             if found:
    #                 if '[tid:' in line and '[tid:%s]' % OrderBookID not in line:
    #                     found = False
    #                 elif ('tradeadjustment' in line or '[tid:%s]' % OrderBookID in line):
    #                     print line
    #
    #         if not in_file:
    #             print 'Trade ID %s Not Found!' % OrderBookID
    #
    #         inputFile.close()
    #
    # def parseLogfile08(self):
    #
    #     OrderBookIDs = ['63603453426925569', '63603453426925570', '63603453426925571',
    #                     '63603453426925572', '63603453426925573', '63603453426925574',
    #                     '63603453426925575', '63603453426925576', '63603453426925577',
    #                     '63603453426925578', '63603453426925579', '63603453426925580',
    #                     '63603453426925581',
    #                     '63603453426925582', '63603453426925583', '63603453426925584',
    #                     '63603453426925585', '63603453426925586', '63603453426925587',
    #                     '63603453426925588', '63603453426925589', '63603453426925590',
    #                     '63603453426925591', '63603453426925592', '63603453426925593',
    #                     '63603453426925594', '63603453426925595', '63603453426925596',
    #                     '63603453426925597', '63603453426925598', '63603453426925599',
    #                     '63603453426925600', '63603453426925601', '63603453426925602',
    #                     '63603453426925603', '63603453426925604', '63603453426925605',
    #                     '63603453426925606', '63603453426925607', '63603453426925608',
    #                     '63603453426925609', '63603453426925611', '63603453426925612']
    #
    #     logfile = self.optmenu()
    #
    #     for OrderBookID in OrderBookIDs:
    #         print '\n\n', '-'*40, '1.1 C, Trade and Trade Amend, TC 36', '-'*40, '\n\n'
    #         inputFile = open(logfile, 'r')
    #         found = False
    #         in_file = False
    #         for line in inputFile.readlines():
    #             if not found:
    #                 if '[tid:%s]' % OrderBookID in line:
    #                     found = True
    #                     in_file = True
    #             if found:
    #                 if '[tid:' in line and '[tid:%s]' % OrderBookID not in line:
    #                     found = False
    #                 elif ('tradeadjustment' in line or '[tid:%s]' % OrderBookID in line):
    #                     print line
    #
    #         if not in_file:
    #             print 'Trade ID %s Not Found!' % OrderBookID
    #
    #         inputFile.close()
    #
    # def parseLogfile09(self):
    #
    #     OrderBookIDs = ['63603453426925641', '63603453426925646', '63603453426925653']
    #
    #     logfile = self.optmenu()
    #
    #     for OrderBookID in OrderBookIDs:
    #         print '\n\n', '-'*40, '1.1 C, Trade and Trade Amend, TC 37', '-'*40, '\n\n'
    #         inputFile = open(logfile, 'r')
    #         found = False
    #         in_file = False
    #         for line in inputFile.readlines():
    #             if not found:
    #                 if '[tid:%s]' % OrderBookID in line:
    #                     found = True
    #                     in_file = True
    #             if found:
    #                 if '[tid:' in line and '[tid:%s]' % OrderBookID not in line:
    #                     found = False
    #                 elif ('tradeadjustment' in line or '[tid:%s]' % OrderBookID in line):
    #                     print line
    #
    #         if not in_file:
    #             print 'Trade ID %s Not Found!' % OrderBookID
    #
    #         inputFile.close()
    #
    # def parseLogfile10(self):
    #
    #     OrderBookIDs = ['63603453426925642', '63603453426925647', '63603453426925654']
    #
    #     logfile = self.optmenu()
    #
    #     for OrderBookID in OrderBookIDs:
    #         print '\n\n', '-'*40, '1.1 C, Trade and Trade Amend, TC 38', '-'*40, '\n\n'
    #         inputFile = open(logfile, 'r')
    #         found = False
    #         in_file = False
    #         for line in inputFile.readlines():
    #             if not found:
    #                 if '[tid:%s]' % OrderBookID in line:
    #                     found = True
    #                     in_file = True
    #             if found:
    #                 if '[tid:' in line and '[tid:%s]' % OrderBookID not in line:
    #                     found = False
    #                 elif ('tradeadjustment' in line or '[tid:%s]' % OrderBookID in line):
    #                     print line
    #
    #         if not in_file:
    #             print 'Trade ID %s Not Found!' % OrderBookID
    #
    #         inputFile.close()
    #
    # def parseLogfile11(self):
    #
    #     OrderBookIDs = ['63603453426925667',]
    #
    #     logfile = self.optmenu()
    #
    #     for OrderBookID in OrderBookIDs:
    #         print '\n\n', '-'*40, '1.1 C, Trade and Trade Amend, TC 39', '-'*40, '\n\n'
    #         inputFile = open(logfile, 'r')
    #         found = False
    #         in_file = False
    #         for line in inputFile.readlines():
    #             if not found:
    #                 if '[tid:%s]' % OrderBookID in line:
    #                     found = True
    #                     in_file = True
    #             if found:
    #                 if '[tid:' in line and '[tid:%s]' % OrderBookID not in line:
    #                     found = False
    #                 elif ('tradeadjustment' in line or '[tid:%s]' % OrderBookID in line):
    #                     print line
    #
    #         if not in_file:
    #             print 'Trade ID %s Not Found!' % OrderBookID
    #
    #         inputFile.close()
    #
    # def parseLogfile12(self):
    #
    #     OrderBookIDs = ['63603453426925637', '63603453426925638']
    #
    #     logfile = self.optmenu()
    #
    #     for OrderBookID in OrderBookIDs:
    #         print '\n\n', '-'*40, '1.1 C, Trade and Trade Amend, TC 40', '-'*40, '\n\n'
    #         inputFile = open(logfile, 'r')
    #         found = False
    #         in_file = False
    #         for line in inputFile.readlines():
    #             if not found:
    #                 if '[tid:%s]' % OrderBookID in line:
    #                     found = True
    #                     in_file = True
    #             if found:
    #                 if '[tid:' in line and '[tid:%s]' % OrderBookID not in line:
    #                     found = False
    #                 elif ('tradeadjustment' in line or '[tid:%s]' % OrderBookID in line):
    #                     print line
    #
    #         if not in_file:
    #             print 'Trade ID %s Not Found!' % OrderBookID
    #
    #         inputFile.close()
    #
    # def parseLogfile13(self):
    #
    #     OrderBookIDs = ['63603453426925661', ]
    #
    #     logfile = self.optmenu()
    #
    #     for OrderBookID in OrderBookIDs:
    #         print '\n\n', '-'*40, '1.1 C, Trade and Trade Amend, TC 41', '-'*40, '\n\n'
    #         inputFile = open(logfile, 'r')
    #         found = False
    #         in_file = False
    #         for line in inputFile.readlines():
    #             if not found:
    #                 if '[tid:%s]' % OrderBookID in line:
    #                     found = True
    #                     in_file = True
    #             if found:
    #                 if '[tid:' in line and '[tid:%s]' % OrderBookID not in line:
    #                     found = False
    #                 elif ('tradeadjustment' in line or '[tid:%s]' % OrderBookID in line):
    #                     print line
    #
    #         if not in_file:
    #             print 'Trade ID %s Not Found!' % OrderBookID
    #
    #         inputFile.close()
    #
    # def parseLogfile14(self):
    #
    #     OrderBookIDs = ['63603453426925663', ]
    #
    #     logfile = self.optmenu()
    #
    #     for OrderBookID in OrderBookIDs:
    #         print '\n\n', '-'*40, '1.1 C, Trade and Trade Amend, TC 42', '-'*40, '\n\n'
    #         inputFile = open(logfile, 'r')
    #         found = False
    #         in_file = False
    #         for line in inputFile.readlines():
    #             if not found:
    #                 if '[tid:%s]' % OrderBookID in line:
    #                     found = True
    #                     in_file = True
    #             if found:
    #                 if '[tid:' in line and '[tid:%s]' % OrderBookID not in line:
    #                     found = False
    #                 elif ('tradeadjustment' in line or '[tid:%s]' % OrderBookID in line):
    #                     print line
    #
    #         if not in_file:
    #             print 'Trade ID %s Not Found!' % OrderBookID
    #
    #         inputFile.close()
    #
    # def parseLogfile18(self):
    #
    #     OrderBookIDs = ['9110890', '10290538', '265083']
    #
    #     logfile = self.optmenu()
    #
    #     total_count = 10
    #     for OrderBookID in OrderBookIDs:
    #         print '\n\n', '-'*40, '1.3 Session 1 (Refresh), Section 1: Ref Data', '-'*40, '\n\n'
    #         inputFile = open(logfile, 'r')
    #         found = False
    #         count = 10
    #         in_file = False
    #         for line in inputFile.readlines():
    #             if 'msgType' in line and '%s]' % OrderBookID in line and '29.01.2015 08' not in line:
    #                 print line
    #                 in_file = True
    #                 count += 1
    #
    #         if not in_file:
    #             print 'Trade ID %s Not Found!' % OrderBookID
    #
    #         inputFile.close()
    #
    # def parseLogfile15(self):
    #
    #     OrderBookIDs = ['6360763006787295501',
    #                     '6360763006787295502',
    #                     '6360763006787295504',
    #                     '6360763006787295506',
    #                     '6360763006787295507',
    #                     '6360763006787295508',
    #                     '6360763006787295509',
    #                     '6360763006787295510',
    #                     '6360763006787295511',
    #                     '6360763006787295512',
    #                     '6360763006787295513']
    #
    #     logfile = self.optmenu()
    #
    #     for OrderBookID in OrderBookIDs:
    #         print '\n\n', '-'*40, '1.3 Section 10, Order Book Building', '-'*40, '\n\n'
    #         inputFile = open(logfile, 'r')
    #         found = False
    #         in_file = False
    #         for line in inputFile.readlines():
    #             if not found:
    #                 if '[oid:%s]' % OrderBookID in line:
    #                     found = True
    #                     in_file = True
    #             if found:
    #                 if '[oid:' in line and '[oid:%s]' % OrderBookID not in line:
    #                     found = False
    #                 # if '[oid:' not in line and 'Deal Type' not in line:
    #                 #     found = False
    #                 # if ('Deal Type' in line or '[tid:%s]' % OrderBookID in line):
    #                 print line
    #
    #         if not in_file:
    #             print 'Order ID %s Not Found!' % OrderBookID
    #
    #         inputFile.close()
    #
    # def parseLogfile16(self):
    #
    #     OrderBookIDs = ['63607576595529735',
    #                     '63607576595529737',
    #                     '63607576595529732',
    #                     '63607576595529738',
    #                     '63607576595529739',
    #                     '63607576595529729']
    #
    #     logfile = self.optmenu()
    #
    #     for OrderBookID in OrderBookIDs:
    #         print '\n\n', '-'*40, '1.4 Session 3 Data Recovery (Line Arb & Retrans) TC 4', '-'*40, '\n\n'
    #         inputFile = open(logfile, 'r')
    #         found = False
    #         in_file = False
    #         for line in inputFile.readlines():
    #             if not found:
    #                 if '[tid:%s]' % OrderBookID in line:
    #                     found = True
    #                     in_file = True
    #             if found:
    #                 if '[tid:' in line and '[tid:%s]' % OrderBookID not in line:
    #                     found = False
    #                 if '[tid:' not in line and 'Deal Type' not in line:
    #                     found = False
    #                 if ('Deal Type' in line or '[tid:%s]' % OrderBookID in line):
    #                     print line
    #
    #         if not in_file:
    #             print 'Order ID %s Not Found!' % OrderBookID
    #
    #         inputFile.close()
    #
    # def parseLogfile17(self):
    #
    #     OrderBookIDs = ['1771477',]
    #
    #     logfile = self.optmenu()
    #
    #     for OrderBookID in OrderBookIDs:
    #         print '\n\n', '-'*40, '1.2 1B Test Case 11: Status Data', '-'*40, '\n\n'
    #         inputFile = open(logfile, 'r')
    #         in_file = False
    #         for line in inputFile.readlines():
    #             if OrderBookID in line and 'HandleMarketStatus' in line:
    #                 print line
    #                 in_file = True
    #
    #         if not in_file:
    #             print 'OrderBookID %s Not Found!' % OrderBookID
    #
    #         inputFile.close()
    #
    # def parseLogfile19(self):
    #
    #     OrderBookIDs = ['657365',]
    #
    #     logfile = self.optmenu()
    #
    #     total_count = 10
    #     for OrderBookID in OrderBookIDs:
    #         print '\n\n', '-'*40, '1.3 Session 1 (Refresh), Section 1: Ref Data', '-'*40, '\n\n'
    #         inputFile = open(logfile, 'r')
    #         found = False
    #         count = 10
    #         in_file = False
    #         for line in inputFile.readlines():
    #             if 'msgType' in line and '%s]' % OrderBookID in line and '29.01.2015 08' not in line:
    #                 print line
    #                 in_file = True
    #                 count += 1
    #
    #         if not in_file:
    #             print 'Trade ID %s Not Found!' % OrderBookID
    #
    #         inputFile.close()
    #
    # def parseLogfile20(self):
    #
    #     OrderBookIDs = ['1771477',]
    #
    #     logfile = self.optmenu()
    #
    #     for OrderBookID in OrderBookIDs:
    #         print '\n\n', '-'*40, '1.4 Session 3 Data Recovery (Line Arb & Retrans) TC 2', '-'*40, '\n\n'
    #         inputFile = open(logfile, 'r')
    #         in_file = False
    #         for line in inputFile.readlines():
    #             if 'quoterequest' in line and OrderBookID in line:
    #                 print line
    #                 in_file = True
    #
    #         if not in_file:
    #             print 'OrderBookID %s Not Found!' % OrderBookID
    #
    #         inputFile.close()
    #

    def run_tests(self):
        self.parseLogfile01a()
        self.parseLogfile01b()
        self.parseLogfile03()
        self.parseLogfile08()
        self.parseLogfile141d()
        self.parseLogfile142d()
        self.parseLogfile143d()
        self.parseLogfile144d()
        self.parseLogfile145d()
        self.parseLogfile146d()
        self.parseLogfile147d()
        self.parseLogfile148d()
        self.parseLogfile149d()
        self.parseLogfile1410d()
        self.parseLogfile1411d()
        self.parseLogfile1412d()
        self.parseLogfile1413d()
        self.parseLogfile1414d()
        self.parseLogfile1415d()

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
logRead.run_tests()
# logRead.parseLogfile20()