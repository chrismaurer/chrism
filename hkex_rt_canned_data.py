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

    def parseLogfile1a(self):

        OrderBookIDs = ['54792098', '132085', '463857', '3672082', '6754210', '12193698', '14225320', '4262943', '462763', '399318', '21368738', '4294840226']

        logfile = self.optmenu()

        total_count = 10
        for OrderBookID in OrderBookIDs:
            print '\n\n', '-'*40, 'Session 1 - Test case 1, Scenario', OrderBookIDs.index(OrderBookID)+1,': Interpretation of Reference Data', '-'*40, '\n\n'
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

    def parseLogfile1b(self):

        OrderBookIDs = ['0',]

        logfile = self.optmenu()

        total_count = 8
        for OrderBookID in OrderBookIDs:
            print '\n\n', '-'*40, 'Session 1 - Test case 1, Scenario 13: Ref Data (Next Day Effective Series)', '-'*40, '\n\n'
            inputFile = open(logfile, 'r')
            found = False
            count = 0
            in_file = False
            for line in inputFile.readlines():
                if 'Contract Created' in line or '_DEFINITIONS' in line:
                    if '[id:%s]' % OrderBookID in line and 'HSI15000R9' in line:
                        count = 0
                        found = True
                if found:
                    if 'msgType' in line and '[id:%s]' % OrderBookID in line and 'HSI15000R9' in line:
                        print line
                        in_file = True
                        count += 1

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

            inputFile.close()

    # def parseLogfile3aaa(self):
    #
    #     OrderBookIDs = ['63603457721892920', '63603457721892919']
    #
    #     logfile = self.optmenu()
    #
    #     for OrderBookID in OrderBookIDs:
    #         print '\n\n', '-'*40, '1.1 C, Trade and Trade Amend', '-'*40, '\n\n'
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

    def parseLogfile2(self):

        obID_states = [['0', '1'], ['0', '2'], ['0', '3'], ['1118114', '4'], ['1118114', '6730'], ['1118114', '6731'],
                       ['266148', '6827'], ['0', '6841'], ['266148', '7220'], ['266148', '7228'], ['0', '6996'],
                       ['0', '6635'], ['0', '7362'], ['790434', '8058'], ['0', '39091'], ['0', '38875'], ['0', '42965']]

        logfile = self.optmenu()

        for obID_state in obID_states:
            print '\n\n', '-'*40, 'Session 1 - Test case 2, Scenario', OrderBookIDs.index(obID_state)+1,': Sec. A Interpretation of Status Data: Market Status', '-'*40, '\n\n'
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if all(obID_mkt_values in line for obID_mkt_values in obID_state):
                    if 'HandleMarketStatus' in line and 'obId:%s' % obID_state[0] in line and 'st:%s' % obID_state[1] in line:
                        print line
                        in_file = True
                    elif 'Market Status Received' in line and 'o:%s' % obID_state in line and 'st:%s' % obID_state[1] in line:
                        print line
                        in_file = True
                    elif 'msgType320' in line:
                        print line
                        in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % obID_state

            inputFile.close()

#     def parseLogfile5(self):
#
# #        OrderBookIDs = ['5181346', '656373', '331181', '19531733', '55185314', '56823714', '135074', '5836706', '855071', '16060718']
#         OrderBookIDs = ['16060718',]
#
#         logfile = self.optmenu()
#
#         total_count = 10
#         for OrderBookID in OrderBookIDs:
#             print '\n\n', '-'*40, '1.3 Session 2 (Refresh), Section 1: Ref Data', '-'*40, '\n\n'
#             inputFile = open(logfile, 'r')
#             found = False
#             count = 10
#             in_file = False
#             for line in inputFile.readlines():
#                 if 'msgType' in line and '%s]' % OrderBookID in line:
#                     print line
#                     in_file = True
#                     count += 1
#
#             inputFile.close()
#
#             if not in_file:
#                 inputFile = open(logfile, 'r')
#                 for line in inputFile.readlines():
#                     if '[id:%s]' % OrderBookID in line or '[combObId:%s]' % OrderBookID in line:
#                         if 'msgType301' in line or 'msgType302' in line or 'msgType304' in line:
#                             print line
#                             in_file = True
#
#             if not in_file:
#                 print 'OrderBookID %s Not Found!' % OrderBookID

    def parseLogfile3(self):

        OrderBookIDs = ['36833042', '592317', '136328']

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

    def parseLogfile04(self):

        OrderBookIDs = ['4103', '5256', '2038']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '\n\n', '-'*40, 'Session 1 - Test case 4: Interpretation of Status Data: Commodity Status', '-'*40, '\n\n'
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if 'Commodity Status Received [code:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile05(self):

        OrderBookIDs = ['44306344', ]

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '\n\n', '-'*40, 'Session 1 - Test case 5: Interpretation of Order Book Data: Quote Request', '-'*40, '\n\n'
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if 'quoterequest' in line and OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile08(self):

        obID_prcs = [['987044', '22505'], ['1183652', '19200'], ['17960868', '19300']]

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

    def parseLogfile10(self):

        alerts = [['102', ], ['102', ], ['1', 'Welcome to OMDD market rehearsal'],
                  ['2', 'Start of Volatility Control Mechanism cool-off period: [HSIN8]'],
                  ['3', 'Start of Volatility Control Mechanism cool-off period: [HSIN8]'],
                  ['412', 'Start of Volatility Control Mechanism cool-off period: [MCHN8]'],
                  ['413', 'Start of Volatility Control Mechanism cool-off period: [MCHN8]'],
                  ['420', 'Start of Volatility Control Mechanism cool-off period: [MHIN8]'],
                  ['421', 'Start of Volatility Control Mechanism cool-off period: [MHIN8]']]

        logfile = self.optmenu()

        for alert in alerts:
            print '\n\n', '-'*40, 'Session 1 - Test case 10: Interpretation of News : Market Alert', '-'*40, '\n\n'
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if all(alert_values in line for alert_values in alert):
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % alerts

            inputFile.close()

    def parseLogfile131d(self):

        OrderBookIDs = ['1707937', ]

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 13: Section D: Full Order Book Scenario 1 - D', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if '[id:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile132c(self):

        OrderBookIDs = ['2166689', ]

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 13: Section D: Full Order Book Scenario 2 - C', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if '[id:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile133d(self):

        OrderBookIDs = ['3280801', ]

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 13: Section D: Full Order Book Scenario 3 - D', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if '[id:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile134d(self):

        OrderBookIDs = ['7021031017850875263',
                        '7021031017850875262',
                        '7021031017850875261',
                        '7021031017850875267',
                        '7021031017850875255',
                        '7021031017850875256',
                        '7021031017850906719']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 13: Section D: Full Order Book Scenario 4 - D', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if 'Add Order [id:7409569] [oid:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile135d(self):

        OrderBookIDs =  ['7021031017850875267', ]

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 13: Section D: Full Order Book Scenario 5 - D', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if 'Add Order [id:8327073] [oid:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile136c(self):

        OrderBookIDs =  ['7021031017850875264', '7021031017850875265', '7021031017850875267']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 13: Section D: Full Order Book Scenario 6 - C', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if 'Add Order [id:462753] [oid:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile137d(self):

        OrderBookIDs =  ['7021031022145834324', '7021031022145834323', '7021031022145834322', '7021031022145834317']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 13: Section D: Full Order Book Scenario 7 - D', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if 'Add Order [id:136173] [oid:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile138d(self):

        OrderBookIDs =  ['7021031022145834316', '7021031022145834317']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 13: Section D: Full Order Book Scenario 8 - D', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if 'Add Order [id:660461] [oid:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile139d(self):

        OrderBookIDs =  ['7021031022145834316', '7021031022145834332']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 13: Section D: Full Order Book Scenario 9 - D', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if 'Add Order [id:201709] [oid:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile1310d(self):

        OrderBookIDs =  ['7021031022145834318', '7021031022145834319']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 13: Section D: Full Order Book Scenario 10 - D', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if 'Add Order [id:1119213] [oid:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile1311d(self):

        OrderBookIDs =  ['7021031017850906684', '7021031017850906716', '7021031017850906715', '7021031017850906689']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 13: Section D: Full Order Book Scenario 11 - D', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if 'Add Order [id:3411873] [oid:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile1312d(self):

        OrderBookIDs =  ['7021031017850906712', '7021031017850906709', '7021031017850906713', '7021031017850906717']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 13: Section D: Full Order Book Scenario 12 - D', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if 'Add Order [id:4722593] [oid:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile1313d(self):

        OrderBookIDs =  ['7021031017850870803', '7021031017850870806', '7021031017850870808', '7021031017850870809',
                         '7021031017850870810', '7021031017850870812', '7021031017850870814', '7021031017850870816',
                         '7021031017850870818', '7021031017850870820']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 13: Section D: Full Order Book Scenario 13 - D', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if 'Add Order [id:50991010] [oid:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile1314d(self):

        OrderBookIDs =  ['7021031017850875208', '7021031017850875207', '7021031017850875206', '7021031017850875203',
                         '7021031017850875202', '7021031017850875201', '7021031017850875200', '7021031017850875199',
                         '7021031017850875198', '7021031017850875197', '7021031017850875196']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 13: Section D: Full Order Book Scenario 14 - D', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if 'Add Order [id:52432802] [oid:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile1315d(self):

        OrderBookIDs =  ['7021031017850870802', '7021031017850870804', '7021031017850870805', '7021031017850870807',
                         '7021031017850870811', '7021031017850870813', '7021031017850870815', '7021031017850870817',
                         '7021031017850870819', '7021031017850870821', '7021031017850870835', '7021031017850870836']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 13: Section D: Full Order Book Scenario 15 - D', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if 'Add Order [id:855970] [oid:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile1316d(self):

        OrderBookIDs = ['7021031017850875174',
                        '7021031017850875173',
                        '7021031017850875172',
                        '7021031017850875171',
                        '7021031017850875170',
                        '7021031017850875169',
                        '7021031017850875168',
                        '7021031017850875167',
                        '7021031017850875166',
                        '7021031017850875165']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 13: Section D: Full Order Book Scenario 16 - D', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if 'Add Order [id:6360994] [oid:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile1317d(self):

        OrderBookIDs = ['7021031017850870837',
                        '7021031017850870838',
                        '7021031017850870839',
                        '7021031017850870840',
                        '7021031017850870842',
                        '7021031017850870844',
                        '7021031017850870847',
                        '7021031017850870848',
                        '7021031017850870850',
                        '7021031017850870852',
                        '7021031017850870870',
                        '7021031017850870874',
                        '7021031017850870879',
                        '7021031017850870880',
                        '7021031017850870882',
                        '7021031017850870883',
                        '7021031017850870884',
                        '7021031017850870885',
                        '7021031017850870886',
                        '7021031017850870887']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 13: Section D: Full Order Book Scenario 17 - D', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if 'Add Order [id:50597794] [oid:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile1318d(self):

        OrderBookIDs = ['46600098', ]

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 13: Section D: Full Order Book Scenario 18 - D', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if '[id:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile1319d(self):

        OrderBookIDs = ['7021031017850870841',
                        '7021031017850870843',
                        '7021031017850870845',
                        '7021031017850870846',
                        '7021031017850870849',
                        '7021031017850870851',
                        '7021031017850870853',
                        '7021031017850870856',
                        '7021031017850870858',
                        '7021031017850870859',
                        '7021031017850870863',
                        '7021031017850870864',
                        '7021031017850870872',
                        '7021031017850870873',
                        '7021031017850870875',
                        '7021031017850870876',
                        '7021031017850870877',
                        '7021031017850870878',
                        '7021031017850870881',
                        '7021031017850870888']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 13: Section D: Full Order Book Scenario 19 - D', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if 'Add Order [id:50663330] [oid:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile1320c(self):

        OrderBookIDs = ['266148', ]

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 13: Section D: Full Order Book Scenario 20 - C', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if '[id:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile1321d(self):

        OrderBookIDs = ['4294840226', ]

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 13: Section D: Full Order Book Scenario 21 - D', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if '[id:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile1322d(self):

        OrderBookIDs = ['4294840225', ]

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 13: Section D: Full Order Book Scenario 22 - D', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if '[id:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile1323d(self):

        OrderBookIDs = ['7021030738677990946',
                        '7021030738677990945',
                        '7021030738677990956',
                        '7021030738677990955',
                        '7021030738677990954',
                        '7021030738677990953',
                        '7021030738677990952',
                        '7021030738677990951',
                        '7021030738677990950',
                        '7021030738677990942']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 13: Section D: Full Order Book Scenario 23 - D', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if 'Add Order [id:331684] [oid:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile1324c(self):

        OrderBookIDs = ['7021031017850903065', '7021031017850903066']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 13: Section D: Full Order Book Scenario 24 - C', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if 'Add Order [id:1118114] [oid:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile1325d(self):

        OrderBookIDs = ['1183650', ]

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 13: Section D: Full Order Book Scenario 25 - D', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if '[id:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile1326d(self):

        OrderBookIDs = ['7021031017850904464', '7021031017850904463']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 13: Section D: Full Order Book Scenario 26 - D', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if 'Add Order [id:35655585] [oid:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile1327d(self):

        OrderBookIDs = ['593832', ]

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 13: Section D: Full Order Book Scenario 27 - D', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if '[id:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile1328c(self):

        OrderBookIDs = ['44371880', ]

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 13: Section D: Full Order Book Scenario 28 - C', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if '[id:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile1329d(self):

        OrderBookIDs = ['7021031017850906717', '7021031017850906713']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 13: Section D: Full Order Book Scenario 29 - D', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if 'Add Order [id:7606177] [oid:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile1330d(self):

        OrderBookIDs = ['7021031017850886884',
                        '7021031017850886879',
                        '7021031017850886878',
                        '7021031017850886880',
                        '7021031017850886881',
                        '7021031017850886882',
                        '7021031017850886883']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, 'Session 1 - Test case 13: Section D: Full Order Book Scenario 30 - D', '^'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if 'Add Order [id:21368738] [oid:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

        inputFile.close()

    def parseLogfile16a(self):

        TradeIDs = ['7021031022145830913',
                    '7021031022145830914',
                    '7021031022145830915',
                    '7021031022145830916',
                    '7021031022145830917',
                    '7021031022145830918',
                    '7021031022145830919',
                    '7021031022145830920',
                    '7021031022145830921',
                    '7021031022145830922',
                    '7021031022145830923',
                    '7021031022145830924',
                    '7021031022145830925',
                    '7021031022145830926',
                    '7021031022145830927',
                    '7021031022145830928',
                    '7021031022145830929',
                    '7021031022145830930',
                    '7021031022145830931',
                    '7021031022145830932',
                    '7021031022145830933',
                    '7021031022145830934',
                    '7021031022145830935',
                    '7021031022145830936',
                    '7021031022145830937',
                    '7021031022145830938',
                    '7021031022145830939',
                    '7021031022145830940',
                    '7021031022145830941',
                    '7021031022145830942',
                    '7021031022145830943',
                    '7021031022145830944',
                    '7021031022145830945',
                    '7021031022145830946',
                    '7021031022145830947',
                    '7021031022145830948',
                    '7021031022145830949',
                    '7021031022145830950',
                    '7021031022145830951',
                    '7021031022145830952',
                    '7021031022145830953',
                    '7021031022145830954',
                    '7021031022145830955',
                    '7021031022145830956',
                    '7021031022145830957']

        logfile = self.optmenu()

        for TradeID in TradeIDs:
            print '\n\n', '-'*40, 'Session 1 - Test Case 16: Scenario 1 Interpretation of Trade and Trade Amendment', '-'*40, '\n\n'
            inputFile = open(logfile, 'r')
            # found = False
            in_file = False
            for line in inputFile.readlines():
                # if not found:
                if ['id:328693'] in line and '[tid:%s]' % TradeID in line:
                    # found = True
                    in_file = True
                # if found:
                #     if '[tid:' in line and '[tid:%s]' % OrderBookID not in line:
                #         found = False
                #     elif ('tradeadjustment' in line or '[tid:%s]' % OrderBookID in line):
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile16b(self):

        TradeIDs = ['7021030734383022129',
                    '7021030734383022134',
                    '7021030734383022141']

        logfile = self.optmenu()

        for TradeID in TradeIDs:
            print '\n\n', '-'*40, 'Session 1 - Test Case 16: Scenario 2 Interpretation of Trade and Trade Amendment', '-'*40, '\n\n'
            inputFile = open(logfile, 'r')
            # found = False
            in_file = False
            for line in inputFile.readlines():
                # if not found:
                if ['id:1050581'] in line and '[tid:%s]' % TradeID in line:
                    # found = True
                    in_file = True
                # if found:
                #     if '[tid:' in line and '[tid:%s]' % OrderBookID not in line:
                #         found = False
                #     elif ('tradeadjustment' in line or '[tid:%s]' % OrderBookID in line):
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile16bc(self):

        TradeIDs = ['7021030734383022144', ]

        logfile = self.optmenu()

        for TradeID in TradeIDs:
            print '\n\n', '-'*40, 'Session 1 - Test Case 16: Scenario 3 Interpretation of Trade and Trade Amendment', '-'*40, '\n\n'
            inputFile = open(logfile, 'r')
            # found = False
            in_file = False
            for line in inputFile.readlines():
                # if not found:
                if ['id:2426837'] in line and '[tid:%s]' % TradeID in line:
                    # found = True
                    in_file = True
                # if found:
                #     if '[tid:' in line and '[tid:%s]' % OrderBookID not in line:
                #         found = False
                #     elif ('tradeadjustment' in line or '[tid:%s]' % OrderBookID in line):
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile16d(self):

        TradeIDs = ['7021031017850863654',
                    '7021031017850863711',
                    '7021031017850863712',
                    '7021031017850863713',
                    '7021031017850863714',
                    '7021031017850863715',
                    '7021031017850863716',
                    '7021031017850863717',
                    '7021031017850863718',
                    '7021031017850863719',
                    '7021031017850863720',
                    '7021031017850863721',
                    '7021031017850863722',
                    '7021031017850863723',
                    '7021031017850863724',
                    '7021031017850863725']

        logfile = self.optmenu()

        for TradeID in TradeIDs:
            print '\n\n', '-'*40, 'Session 1 - Test Case 16: Scenario 4 Interpretation of Trade and Trade Amendment', '-'*40, '\n\n'
            inputFile = open(logfile, 'r')
            # found = False
            in_file = False
            for line in inputFile.readlines():
                # if not found:
                if ['id:3280801'] in line and '[tid:%s]' % TradeID in line:
                    # found = True
                    in_file = True
                # if found:
                #     if '[tid:' in line and '[tid:%s]' % OrderBookID not in line:
                #         found = False
                #     elif ('tradeadjustment' in line or '[tid:%s]' % OrderBookID in line):
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile16e(self):

        TradeIDs = ['7021031017850863635',
                    '7021031017850863636',
                    '7021031017850863637']

        logfile = self.optmenu()

        for TradeID in TradeIDs:
            print '\n\n', '-'*40, 'Session 1 - Test Case 16: Scenario 5 Interpretation of Trade and Trade Amendment', '-'*40, '\n\n'
            inputFile = open(logfile, 'r')
            # found = False
            in_file = False
            for line in inputFile.readlines():
                # if not found:
                if ['id:1445794'] in line and '[tid:%s]' % TradeID in line:
                    # found = True
                    in_file = True
                # if found:
                #     if '[tid:' in line and '[tid:%s]' % OrderBookID not in line:
                #         found = False
                #     elif ('tradeadjustment' in line or '[tid:%s]' % OrderBookID in line):
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile16f(self):

        TradeIDs = ['7021031022145830960', '7021031022145830963']

        logfile = self.optmenu()

        for TradeID in TradeIDs:
            print '\n\n', '-'*40, 'Session 1 - Test Case 16: Scenario 6 Interpretation of Trade and Trade Amendment', '-'*40, '\n\n'
            inputFile = open(logfile, 'r')
            # found = False
            in_file = False
            for line in inputFile.readlines():
                # if not found:
                if ['id:660461'] in line and '[tid:%s]' % TradeID in line:
                    # found = True
                    in_file = True
                # if found:
                #     if '[tid:' in line and '[tid:%s]' % OrderBookID not in line:
                #         found = False
                #     elif ('tradeadjustment' in line or '[tid:%s]' % OrderBookID in line):
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile16g(self):

        TradeIDs = ['7021031022145830958', '7021031022145830961', '7021031022145830964']

        logfile = self.optmenu()

        for TradeID in TradeIDs:
            print '\n\n', '-'*40, 'Session 1 - Test Case 16: Scenario 7 Interpretation of Trade and Trade Amendment', '-'*40, '\n\n'
            inputFile = open(logfile, 'r')
            # found = False
            in_file = False
            for line in inputFile.readlines():
                # if not found:
                if ['id:201709'] in line and '[tid:%s]' % TradeID in line:
                    # found = True
                    in_file = True
                # if found:
                #     if '[tid:' in line and '[tid:%s]' % OrderBookID not in line:
                #         found = False
                #     elif ('tradeadjustment' in line or '[tid:%s]' % OrderBookID in line):
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile16h(self):

        TradeIDs = ['7021031017850863644',
                    '7021031017850863681',
                    '7021031017850863682',
                    '7021031017850863683',
                    '7021031017850863684',
                    '7021031017850863686',
                    '7021031017850863690',
                    '7021031017850863692',
                    '7021031017850863696',
                    '7021031017850863698',
                    '7021031017850863702',
                    '7021031017850863704',
                    '7021031017850863708',
                    '7021031017850863709',
                    '7021031017850863710']

        logfile = self.optmenu()

        for TradeID in TradeIDs:
            print '\n\n', '-'*40, 'Session 1 - Test Case 16: Scenario 8 Interpretation of Trade and Trade Amendment', '-'*40, '\n\n'
            inputFile = open(logfile, 'r')
            # found = False
            in_file = False
            for line in inputFile.readlines():
                # if not found:
                if ['id:3411873'] in line and '[tid:%s]' % TradeID in line:
                    # found = True
                    in_file = True
                # if found:
                #     if '[tid:' in line and '[tid:%s]' % OrderBookID not in line:
                #         found = False
                #     elif ('tradeadjustment' in line or '[tid:%s]' % OrderBookID in line):
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile16i(self):

        TradeIDs = ['7021031017850863685', '7021031017850863691', '7021031017850863697', '7021031017850863703']

        logfile = self.optmenu()

        for TradeID in TradeIDs:
            print '\n\n', '-'*40, 'Session 1 - Test Case 16: Scenario 9 Interpretation of Trade and Trade Amendment', '-'*40, '\n\n'
            inputFile = open(logfile, 'r')
            # found = False
            in_file = False
            for line in inputFile.readlines():
                # if not found:
                if ['id:3215265'] in line and '[tid:%s]' % TradeID in line:
                    # found = True
                    in_file = True
                # if found:
                #     if '[tid:' in line and '[tid:%s]' % OrderBookID not in line:
                #         found = False
                #     elif ('tradeadjustment' in line or '[tid:%s]' % OrderBookID in line):
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile16j(self):

        TradeIDs = ['7021031017850863617',
                    '7021031017850863617',
                    '7021031017850863617',
                    '7021031017850863617',
                    '7021031017850863617']

        logfile = self.optmenu()

        for TradeID in TradeIDs:
            print '\n\n', '-'*40, 'Session 1 - Test Case 16: Scenario 10 Interpretation of Trade and Trade Amendment', '-'*40, '\n\n'
            inputFile = open(logfile, 'r')
            # found = False
            in_file = False
            for line in inputFile.readlines():
                # if not found:
                if ['id:855970'] in line and '[tid:%s]' % TradeID in line:
                    # found = True
                    in_file = True
                # if found:
                #     if '[tid:' in line and '[tid:%s]' % OrderBookID not in line:
                #         found = False
                #     elif ('tradeadjustment' in line or '[tid:%s]' % OrderBookID in line):
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile16k(self):

        TradeIDs = ['7021030738677989383',
                    '7021030738677989383',
                    '7021030738677989383',
                    '7021030738677989383',
                    '7021030738677989383']

        logfile = self.optmenu()

        for TradeID in TradeIDs:
            print '\n\n', '-'*40, 'Session 1 - Test Case 16: Scenario 11 Interpretation of Trade and Trade Amendment', '-'*40, '\n\n'
            inputFile = open(logfile, 'r')
            # found = False
            in_file = False
            for line in inputFile.readlines():
                # if not found:
                if ['id:921508'] in line and '[tid:%s]' % TradeID in line:
                    # found = True
                    in_file = True
                # if found:
                #     if '[tid:' in line and '[tid:%s]' % OrderBookID not in line:
                #         found = False
                #     elif ('tradeadjustment' in line or '[tid:%s]' % OrderBookID in line):
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile16l(self):

        TradeIDs = ['7021031017850863640',
                    '7021031017850863641',
                    '7021031017850863642',
                    '7021031017850863643']

        logfile = self.optmenu()

        for TradeID in TradeIDs:
            print '\n\n', '-'*40, 'Session 1 - Test Case 16: Scenario 12 Interpretation of Trade and Trade Amendment', '-'*40, '\n\n'
            inputFile = open(logfile, 'r')
            # found = False
            in_file = False
            for line in inputFile.readlines():
                # if not found:
                if ['id:1183650'] in line and '[tid:%s]' % TradeID in line:
                    # found = True
                    in_file = True
                # if found:
                #     if '[tid:' in line and '[tid:%s]' % OrderBookID not in line:
                #         found = False
                #     elif ('tradeadjustment' in line or '[tid:%s]' % OrderBookID in line):
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile16m(self):

        TradeIDs = ['7021031017850863658',
                    '7021031017850863658',
                    '7021031017850863658',
                    '7021031017850863658',
                    '7021031017850863658',
                    '7021031017850863658',
                    '7021031017850863658',
                    '7021031017850863658',
                    '7021031017850863658']

        logfile = self.optmenu()

        for TradeID in TradeIDs:
            print '\n\n', '-'*40, 'Session 1 - Test Case 16: Scenario 13 Interpretation of Trade and Trade Amendment', '-'*40, '\n\n'
            inputFile = open(logfile, 'r')
            # found = False
            in_file = False
            for line in inputFile.readlines():
                # if not found:
                if ['id:46993314'] in line and '[tid:%s]' % TradeID in line:
                    # found = True
                    in_file = True
                # if found:
                #     if '[tid:' in line and '[tid:%s]' % OrderBookID not in line:
                #         found = False
                #     elif ('tradeadjustment' in line or '[tid:%s]' % OrderBookID in line):
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile16n(self):

        TradeIDs = ['7021031017850863645', ]

        logfile = self.optmenu()

        for TradeID in TradeIDs:
            print '\n\n', '-'*40, 'Session 1 - Test Case 16: Scenario 14 Interpretation of Trade and Trade Amendment', '-'*40, '\n\n'
            inputFile = open(logfile, 'r')
            # found = False
            in_file = False
            for line in inputFile.readlines():
                # if not found:
                if ['id:7606177'] in line and '[tid:%s]' % TradeID in line:
                    # found = True
                    in_file = True
                # if found:
                #     if '[tid:' in line and '[tid:%s]' % OrderBookID not in line:
                #         found = False
                #     elif ('tradeadjustment' in line or '[tid:%s]' % OrderBookID in line):
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile16o(self):

        TradeIDs = ['7021030738677989413', '7021030738677989422', '7021030738677989431']

        logfile = self.optmenu()

        for TradeID in TradeIDs:
            print '\n\n', '-'*40, 'Session 1 - Test Case 16: Scenario 15 Interpretation of Trade and Trade Amendment', '-'*40, '\n\n'
            inputFile = open(logfile, 'r')
            # found = False
            in_file = False
            for line in inputFile.readlines():
                # if not found:
                if ['id:3542948'] in line and '[tid:%s]' % TradeID in line:
                    # found = True
                    in_file = True
                # if found:
                #     if '[tid:' in line and '[tid:%s]' % OrderBookID not in line:
                #         found = False
                #     elif ('tradeadjustment' in line or '[tid:%s]' % OrderBookID in line):
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile16p(self):

        TradeIDs = ['7021031017850863676', '7021031017850863677']

        logfile = self.optmenu()

        for TradeID in TradeIDs:
            print '\n\n', '-'*40, 'Session 1 - Test Case 16: Scenario 16 Interpretation of Trade and Trade Amendment', '-'*40, '\n\n'
            inputFile = open(logfile, 'r')
            # found = False
            in_file = False
            for line in inputFile.readlines():
                # if not found:
                if ['id:21368738'] in line and '[tid:%s]' % TradeID in line:
                    # found = True
                    in_file = True
                # if found:
                #     if '[tid:' in line and '[tid:%s]' % OrderBookID not in line:
                #         found = False
                #     elif ('tradeadjustment' in line or '[tid:%s]' % OrderBookID in line):
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile17a(self):

        TradeIDs = ['7021030734383022081', '7021030734383022082']

        logfile = self.optmenu()

        for TradeID in TradeIDs:
            print '\n\n', '-'*40, 'Session 1 - Test Case 17: Scenario 1 Interpretation of Trade and Trade Amendment', '-'*40, '\n\n'
            inputFile = open(logfile, 'r')
            # found = False
            in_file = False
            for line in inputFile.readlines():
                # if not found:
                if ['id:11995093'] in line and '[tid:%s]' % TradeID in line:
                    # found = True
                    in_file = True
                # if found:
                #     if '[tid:' in line and '[tid:%s]' % OrderBookID not in line:
                #         found = False
                #     elif ('tradeadjustment' in line or '[tid:%s]' % OrderBookID in line):
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile17b(self):

        TradeIDs = ['7021030734383022150', ]

        logfile = self.optmenu()

        for TradeID in TradeIDs:
            print '\n\n', '-'*40, 'Session 1 - Test Case 17: Scenario 2 Interpretation of Trade and Trade Amendment', '-'*40, '\n\n'
            inputFile = open(logfile, 'r')
            # found = False
            in_file = False
            for line in inputFile.readlines():
                # if not found:
                if ['id:10684373'] in line and '[tid:%s]' % TradeID in line:
                    # found = True
                    in_file = True
                # if found:
                #     if '[tid:' in line and '[tid:%s]' % OrderBookID not in line:
                #         found = False
                #     elif ('tradeadjustment' in line or '[tid:%s]' % OrderBookID in line):
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile17c(self):

        TradeIDs = ['7021030734383022128', ]

        logfile = self.optmenu()

        for TradeID in TradeIDs:
            print '\n\n', '-'*40, 'Session 1 - Test Case 17: Scenario 3 Interpretation of Trade and Trade Amendment', '-'*40, '\n\n'
            inputFile = open(logfile, 'r')
            # found = False
            in_file = False
            for line in inputFile.readlines():
                # if not found:
                if ['id:4294707157'] in line and '[tid:%s]' % TradeID in line:
                    # found = True
                    in_file = True
                # if found:
                #     if '[tid:' in line and '[tid:%s]' % OrderBookID not in line:
                #         found = False
                #     elif ('tradeadjustment' in line or '[tid:%s]' % OrderBookID in line):
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile17d(self):

        TradeIDs = ['7021030734383022083',
                    '7021030734383022084',
                    '7021030734383022085',
                    '7021030734383022086',
                    '7021030734383022087',
                    '7021030734383022088',
                    '7021030734383022089',
                    '7021030734383022090',
                    '7021030734383022091',
                    '7021030734383022092',
                    '7021030734383022093',
                    '7021030734383022094',
                    '7021030734383022095',
                    '7021030734383022096',
                    '7021030734383022097',
                    '7021030734383022098',
                    '7021030734383022099',
                    '7021030734383022100',
                    '7021030734383022101',
                    '7021030734383022102',
                    '7021030734383022103',
                    '7021030734383022104',
                    '7021030734383022105',
                    '7021030734383022106',
                    '7021030734383022107',
                    '7021030734383022108',
                    '7021030734383022109',
                    '7021030734383022110',
                    '7021030734383022111',
                    '7021030734383022112',
                    '7021030734383022113',
                    '7021030734383022114',
                    '7021030734383022115',
                    '7021030734383022116',
                    '7021030734383022117',
                    '7021030734383022118',
                    '7021030734383022119',
                    '7021030734383022120',
                    '7021030734383022121',
                    '7021030734383022122',
                    '7021030734383022123',
                    '7021030734383022124',
                    '7021030734383022125']

        logfile = self.optmenu()

        for TradeID in TradeIDs:
            print '\n\n', '-'*40, 'Session 1 - Test Case 17: Scenario 4 Interpretation of Trade and Trade Amendment', '-'*40, '\n\n'
            inputFile = open(logfile, 'r')
            # found = False
            in_file = False
            for line in inputFile.readlines():
                # if not found:
                if ['id:1771400'] in line and '[tid:%s]' % TradeID in line:
                    # found = True
                    in_file = True
                # if found:
                #     if '[tid:' in line and '[tid:%s]' % OrderBookID not in line:
                #         found = False
                #     elif ('tradeadjustment' in line or '[tid:%s]' % OrderBookID in line):
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile17e(self):

        TradeIDs = ['7021030734383022130', '7021030734383022136', '7021030734383022143']

        logfile = self.optmenu()

        for TradeID in TradeIDs:
            print '\n\n', '-'*40, 'Session 1 - Test Case 17: Scenario 5 Interpretation of Trade and Trade Amendment', '-'*40, '\n\n'
            inputFile = open(logfile, 'r')
            # found = False
            in_file = False
            for line in inputFile.readlines():
                # if not found:
                if ['id:1181653'] in line and '[tid:%s]' % TradeID in line:
                    # found = True
                    in_file = True
                # if found:
                #     if '[tid:' in line and '[tid:%s]' % OrderBookID not in line:
                #         found = False
                #     elif ('tradeadjustment' in line or '[tid:%s]' % OrderBookID in line):
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile17f(self):

        TradeIDs = ['7021030734383022149', ]

        logfile = self.optmenu()

        for TradeID in TradeIDs:
            print '\n\n', '-'*40, 'Session 1 - Test Case 17: Scenario 6 Interpretation of Trade and Trade Amendment', '-'*40, '\n\n'
            inputFile = open(logfile, 'r')
            # found = False
            in_file = False
            for line in inputFile.readlines():
                # if not found:
                if ['id:7407573'] in line and '[tid:%s]' % TradeID in line:
                    # found = True
                    in_file = True
                # if found:
                #     if '[tid:' in line and '[tid:%s]' % OrderBookID not in line:
                #         found = False
                #     elif ('tradeadjustment' in line or '[tid:%s]' % OrderBookID in line):
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % OrderBookID

            inputFile.close()

    def run_tests(self):

        self.parseLogfile1a()
        self.parseLogfile1b()
        self.parseLogfile2()
        self.parseLogfile3()
        self.parseLogfile04()
        self.parseLogfile05()
        self.parseLogfile08()
        self.parseLogfile10()
        self.parseLogfile131d()
        self.parseLogfile132c()
        self.parseLogfile133d()
        self.parseLogfile134d()
        self.parseLogfile135d()
        self.parseLogfile136c()
        self.parseLogfile137d()
        self.parseLogfile138d()
        self.parseLogfile139d()
        self.parseLogfile1310d()
        self.parseLogfile1311d()
        self.parseLogfile1312d()
        self.parseLogfile1313d()
        self.parseLogfile1314d()
        self.parseLogfile1315d()
        self.parseLogfile1316d()
        self.parseLogfile1317d()
        self.parseLogfile1318d()
        self.parseLogfile1319d()
        self.parseLogfile1320c()
        self.parseLogfile1321d()
        self.parseLogfile1322d()
        self.parseLogfile1323d()
        self.parseLogfile1324c()
        self.parseLogfile1325d()
        self.parseLogfile1326d()
        self.parseLogfile1327d()
        self.parseLogfile1328c()
        self.parseLogfile1329d()
        self.parseLogfile1330d()
        self.parseLogfile16a()
        self.parseLogfile16b()
        self.parseLogfile16bc()
        self.parseLogfile16d()
        self.parseLogfile16e()
        self.parseLogfile16f()
        self.parseLogfile16g()
        self.parseLogfile16h()
        self.parseLogfile16i()
        self.parseLogfile16j()
        self.parseLogfile16k()
        self.parseLogfile16l()
        self.parseLogfile16m()
        self.parseLogfile16n()
        self.parseLogfile16o()
        self.parseLogfile16p()
        self.parseLogfile17a()
        self.parseLogfile17b()
        self.parseLogfile17c()
        self.parseLogfile17d()
        self.parseLogfile17e()
        self.parseLogfile17f()

logRead = logfile_analiser()
logRead.optmenu()
# logRead.parseLogfile()
# logRead.parseLogfile2()
# logRead.parseLogfile3()
# logRead.parseLogfile4()
logRead.run_tests()
# logRead.parseLogfile6()
