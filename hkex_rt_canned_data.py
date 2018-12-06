# ~TestCaseName: logfile_analiser
# ~TestCaseSummary: This program reads logfiles from C:\logs and returns any unexpected messages

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

    def parse_logfile_1a(self):

        order_book_ids = ['54792098', '132085', '463857', '3672082', '6754210', '12193698', '14225320', '4262943',
                          '462763', '399318', '21368738', '4294840226', '3934548', '8587221', '8591318', '4294707157']

        logfile = self.optmenu()

        scenario_counter = 1
        for order_book_id in order_book_ids:
            inputfile = open(logfile, 'r')
            if scenario_counter == 13:
                scenario_counter += 1
            print '\n\n', '-'*40, 'Session 1 - Test case 1, Scenario', scenario_counter,\
                ': Interpretation of Reference Data', '-'*40, '\n\n'
            in_file = False
            for line in inputfile.readlines():
                if 'msgType:30' in line and 'id:%s' % order_book_id in line:
                    print line
                    in_file = True
                elif 'msg_type=30' in line and '_id=%s' % order_book_id in line:
                    print line
                    in_file = True

            if not in_file:
                print 'order_book_id %s Not Found!' % order_book_id

            scenario_counter += 1
            inputfile.close()

    def parse_logfile_1b(self):

        order_book_ids = ['0', ]

        logfile = self.optmenu()

        # total_count = 8
        for order_book_id in order_book_ids:
            print '\n\n', '-' * 40, 'Session 1 - Test case 1, Scenario 13: Ref Data (Next Day Effective Series)', \
                '-' * 40, '\n\n'
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if 'msgType:30' in line and 'id:%s' % order_book_id in line and 'HSI15000R9' in line:
                    print line
                    in_file = True
                elif 'msg_type=30' in line and '_id=%s' % order_book_id in line and 'HSI15000R9' in line:
                    print line
                    in_file = True

            if not in_file:
                print 'order_book_id %s Not Found!' % order_book_id

            inputfile.close()

    def parse_logfile_1c(self):

        order_book_ids = ['0', ]

        logfile = self.optmenu()

        for order_book_id in order_book_ids:
            print '\n\n', '-'*40, 'Session 1 - Test case 1, Scenario 18: Ref Data (Next Day Effective Series)', \
                '-'*40, '\n\n'
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if 'msgType:30' in line and 'id:%s' % order_book_id in line and 'CPA9.25C9' in line:
                    print line
                    in_file = True
                elif 'msg_type=30' in line and '_id=%s' % order_book_id in line and 'CPA9.25C9' in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % order_book_id

            inputfile.close()

    # def parse_logfile_3aaa(self):
    #
    #     order_book_ids = ['63603457721892920', '63603457721892919']
    #
    #     logfile = self.optmenu()
    #
    #     for order_book_id in order_book_ids:
    #         print '\n\n', '-'*40, '1.1 C, Trade and Trade Amend', '-'*40, '\n\n'
    #         inputfile = open(logfile, 'r')
    #         found = False
    #         in_file = False
    #         for line in inputfile.readlines():
    #             if not found:
    #                 if '[tid:%s]' % order_book_id in line:
    #                     found = True
    #                     in_file = True
    #             if found:
    #                 if '[tid:' in line and '[tid:%s]' % order_book_id not in line:
    #                     found = False
    #                 elif ('tradeadjustment' in line or '[tid:%s]' % order_book_id in line):
    #                     print line
    #
    #         if not in_file:
    #             print 'Trade ID %s Not Found!' % order_book_id
    #
    #             inputfile.close()

    def parse_logfile_2(self):

        obid_states = [['0', '1', '15'], ['0', '2', '9'], ['0', '3', '15'], ['1118114', '4', '0'],
                       ['1118114', '4', '25'], ['1118114', '4', '0'], ['266148', '4', '25'],
                       ['0', '2', '6'], ['266148', '4', '25'], ['266148', '4', '0'], ['0', '2', '4'],
                       ['0', '2', '19'], ['0', '2', '18'], ['790434', '4', '28'], ['0', '1', '7'],
                       ['0', '1', '6'], ['0', '1', '9']]

        logfile = self.optmenu()

        for obid_state in obid_states:
            inputfile = open(logfile, 'r')
            print '\n\n', '-' * 40, 'Session 1 - Test case 2, Scenario', obid_states.index(
                obid_state) + 1, ': Sec. A Interpretation of Status Data: Market Status', '-' * 40, '\n\n'
            in_file = False
            for line in inputfile.readlines():
                if all(obID_mkt_values in line for obID_mkt_values in obid_state):
                    if 'HandleMarketStatus' in line and 'obId:%s' % obid_state[0] in line and \
                       'l:%s' % obid_state[1] in line and 's:%s' % obid_state[2] in line:
                        print line
                        in_file = True
                    elif 'Market Status Received' in line and 'o:%s' % obid_state[0] in line and \
                         'l:%s' % obid_state[1] in line and 's:%s' % obid_state[2] in line:
                        print line
                        in_file = True
                    elif 'message_type=320' in line and 'order_book_id=%s' % obid_state[0] in line and \
                         'level=%s' % obid_state[1] in line and 'state=%s' % obid_state[2] in line:
                        print line
                        in_file = True

            if not in_file:
                print 'order_book_id %s Not Found!' % obid_state

            inputfile.close()

        #     def parse_logfile_5(self):
        #
        # #        order_book_ids = ['5181346', '656373', '331181', '19531733', '55185314', '56823714', '135074', 
        #           '5836706', '855071', '16060718']
        #         order_book_ids = ['16060718',]
        #
        #         logfile = self.optmenu()
        #
        #         total_count = 10
        #         for order_book_id in order_book_ids:
        #             print '\n\n', '-'*40, '1.3 Session 2 (Refresh), Section 1: Ref Data', '-'*40, '\n\n'
        #             inputfile = open(logfile, 'r')
        #             found = False
        #             count = 10
        #             in_file = False
        #             for line in inputfile.readlines():
        #                 if 'msgType' in line or 'msg_type' in line and '%s]' % order_book_id in line:
        #                     print line
        #                     in_file = True
        #                     count += 1
        #
        #                 inputfile.close()
        #
        #             if not in_file:
        #                 inputfile = open(logfile, 'r')
        #                 for line in inputfile.readlines():
        #                     if '[id:%s]' % order_book_id in line or '[combObId:%s]' % order_book_id in line:
        #                         if 'msgType301' in line or 'msgType302' in line or 'msgType304' in line:
        #                             print line
        #                             in_file = True
        #
        #             if not in_file:
        #                 print 'order_book_id %s Not Found!' % order_book_id

    def parse_logfile_3(self):

        order_book_ids = ['36833042', '592317', '136328', '31983579', '18940948', '11012086']

        logfile = self.optmenu()

        for order_book_id in order_book_ids:
            inputfile = open(logfile, 'r')
            print '\n\n', '-' * 40, 'Session 1 - Test case 3, Scenario', order_book_ids.index(order_book_id)+1, \
                ': Interpretation of Status Data: Series Status', '-' * 40, \
                '\n\n'
            in_file = False
            for line in inputfile.readlines():
                if 'Series Status Received' in line and 'obId:%s' % order_book_id in line:
                    print line
                    in_file = True
                elif 'HandleSeriesStatus' in line and 'obId:%s' % order_book_id in line:
                    print line
                    in_file = True
                elif 'message_type=321' in line and 'order_book_id=%s' % order_book_id in line:  # and \
                    # 'state=%s' % obid_state[1] in line:
                    print line
                    in_file = True

            if not in_file:
                print 'order_book_id %s Not Found!' % order_book_id

            inputfile.close()

    def parse_logfile_04(self):

        commodity_codes = [['4103', 'N'], ['5256', 'N'], ['2038', 'Y']]

        logfile = self.optmenu()

        for commodity_code in commodity_codes:
            inputfile = open(logfile, 'r')
            print '\n\n', '-' * 40, 'Session 1 - Test case 4, Scenario', commodity_codes.index(commodity_code)+1, \
                ': Interpretation of Status Data: Commodity Status', \
                '-' * 40, '\n\n'
            in_file = False
            for line in inputfile.readlines():
                if 'Commodity Status Received [code:%s]' % commodity_code[0] and \
                   '[suspended:%s]' % commodity_code[1] in line:
                    print line
                    in_file = True
                elif 'Commodity Status Received [code=%s]' % commodity_code[0] and \
                     '[suspended:%s]' % commodity_code[1] in line:
                    print line
                    in_file = True

            if not in_file:
                print 'commodity_code %s Not Found!' % commodity_code

            inputfile.close()

    def parse_logfile_05(self):

        order_book_ids = ['44306344', ]

        logfile = self.optmenu()

        for order_book_id in order_book_ids:
            inputfile = open(logfile, 'r')
            print '\n\n', '-' * 40, 'Session 1 - Test case 5: Interpretation of Order Book Data: Quote Request', \
                '-' * 40, '\n\n'
            in_file = False
            for line in inputfile.readlines():
                if 'quoterequest' in line and order_book_id in line:
                    print line
                    in_file = True

            if not in_file:
                print 'order_book_id %s Not Found!' % order_book_id

            inputfile.close()

    def parse_logfile_08(self):

        obid_prcs = [['987044', '22505'], ['1183652', '19200'], ['17960868', '19300'], ['57411540', '-2147483648)']]

        logfile = self.optmenu()

        for obid_prc in obid_prcs:
            inputfile = open(logfile, 'r')
            print '\n\n', '-' * 40, \
                'Session 1 - Test case 8, Scenario', obid_prcs.index(obid_prc)+1, \
                ': Interpretation of Trade and Price Data : Calculated Opening Price', \
                '-' * 40, '\n\n'
            in_file = False
            for line in inputfile.readlines():
                if "Calculated Opening Price" in line and 'id:%s' % obid_prc[0] in line:  # and \
                   # 'px:%s' % obid_prc[1] in line:
                    print line
                    in_file = True
                elif "Calculated Opening Price" in line and 'order_book_id=%s' % obid_prc[0] in line:  # and \
                     # 'px=%s' % obid_prc[1] in line:
                    print line
                    in_file = True

            if not in_file:
                print 'order_book_id %s Not Found!' % obid_prc

            inputfile.close()

    def parse_logfile_10(self):

        alerts = [['102', ''],
                  ['1', 'Welcome to OMDD market rehearsal'],
                  ['2', 'Start of Volatility Control Mechanism cool-off period: [HSIN8]'],
                  ['3', 'Start of Volatility Control Mechanism cool-off period: [HSIN8]'],
                  ['412', 'Start of Volatility Control Mechanism cool-off period: [MCHN8]'],
                  ['413', 'Start of Volatility Control Mechanism cool-off period: [MCHN8]'],
                  ['420', 'Start of Volatility Control Mechanism cool-off period: [MHIN8]'],
                  ['421', 'Start of Volatility Control Mechanism cool-off period: [MHIN8]']]

        logfile = self.optmenu()

        for alert in alerts:
            inputfile = open(logfile, 'r')
            print '\n\n', '-' * 40, 'Session 1 - Test case 10, Scenario', alerts.index(alert)+1, \
                ': Interpretation of News : Market Alert', '-' * 40, '\n\n'
            in_file = False
            for line in inputfile.readlines():
                if 'Market Alert' in line and 'altId:%s' % alert[0] in line and 'hdr:%s' % alert[1] in line:
                    print line
                    in_file = True

            if not in_file:
                print 'Market Alert %s Not Found!' % alert

            inputfile.close()

    def parse_logfile_131d(self):

        order_book_ids = ['1707937', ]

        logfile = self.optmenu()

        print '\n\n', '-' * 40, '\n\n', 'Session 1 - Test case 13, Section D: Full Order Book Scenario 1 - D', \
                      '-'*40, '\n\n'
        for order_book_id in order_book_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if 'Add Order [id:%s]' % order_book_id in line:
                    print line
                    in_file = True
                elif 'Add Order [order_book_id=%s]' % order_book_id in line:
                    print line
                    in_file = True
                elif 'Clear Orderbook [id:%s]' % order_book_id in line:
                    print line
                    in_file = True
                elif 'Clear Orderbook' in line and 'order_book_id=%s' % order_book_id in line:
                    print line
                    in_file = True

            if not in_file:
                print 'order_book_id %s Not Found!' % order_book_id

            inputfile.close()

    def parse_logfile_132c(self):

        order_book_ids = ['2166689', ]

        logfile = self.optmenu()

        print '\n\n', '-' * 40, '\n\n', 'Session 1 - Test case 13, Section D: Full Order Book Scenario 2 - C', \
                      '-'*40, '\n\n'
        for order_book_id in order_book_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if 'Add Order [id:%s]' % order_book_id in line:
                    print line
                    in_file = True
                elif 'Add Order [order_book_id=%s]' % order_book_id in line:
                    print line
                    in_file = True
                elif 'Clear Orderbook [id:%s]' % order_book_id in line:
                    print line
                    in_file = True
                elif 'Clear Orderbook' in line and 'order_book_id=%s' % order_book_id in line:
                    print line
                    in_file = True

            if not in_file:
                print 'order_book_id %s Not Found!' % order_book_id

            inputfile.close()

    def parse_logfile_133d(self):

        order_book_ids = ['3280801', ]

        logfile = self.optmenu()

        print '\n\n', '-' * 40, '\n\n', 'Session 1 - Test case 13, Section D: Full Order Book Scenario 3 - D', \
                      '-'*40, '\n\n'
        for order_book_id in order_book_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if 'Add Order [id:%s]' % order_book_id in line:
                    print line
                    in_file = True
                elif 'Add Order [order_book_id=%s]' % order_book_id in line:
                    print line
                    in_file = True
                elif 'Clear Orderbook [id:%s]' % order_book_id in line:
                    print line
                    in_file = True
                elif 'Clear Orderbook' in line and 'order_book_id=%s' % order_book_id in line:
                    print line
                    in_file = True

            if not in_file:
                print 'order_book_id %s Not Found!' % order_book_id

            inputfile.close()

    def parse_logfile_134d(self):

        order_book_ids = ['7021031017850875263',
                          '7021031017850875262',
                          '7021031017850875261',
                          '7021031017850875267',
                          '7021031017850875255',
                          '7021031017850875256',
                          '7021031017850906719']

        logfile = self.optmenu()

        print '\n\n', '-' * 40, '\n\n', 'Session 1 - Test case 13, Section D: Full Order Book Scenario 4 - D', \
                      '-'*40, '\n\n'
        for order_book_id in order_book_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if 'id:7409569' in line and 'oid:%s' % order_book_id in line:
                    print line
                    in_file = True
                elif 'order_book_id=7409569' and 'order_id=%s' % order_book_id in line:
                    print line
                    in_file = True

            if not in_file:
                print 'order_book_id %s Not Found!' % order_book_id

            inputfile.close()

    def parse_logfile_135d(self):

        order_book_ids = ['7021031017850875267', ]

        logfile = self.optmenu()

        print '\n\n', '-' * 40, '\n\n', 'Session 1 - Test case 13, Section D: Full Order Book Scenario 5 - D', \
                      '-'*40, '\n\n'
        for order_book_id in order_book_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if 'id:8327073' in line and 'oid:%s' % order_book_id in line:
                    print line
                    in_file = True
                elif 'order_book_id=8327073' and 'order_id=%s' % order_book_id in line:
                    print line
                    in_file = True

            if not in_file:
                print 'order_book_id %s Not Found!' % order_book_id

            inputfile.close()

    def parse_logfile_136c(self):

        order_book_ids = ['7021031017850875264', '7021031017850875265', '7021031017850875267']

        logfile = self.optmenu()

        print '\n\n', '-' * 40, '\n\n', 'Session 1 - Test case 13, Section D: Full Order Book Scenario 6 - C', \
                      '-'*40, '\n\n'
        for order_book_id in order_book_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if 'id:462753' in line and 'oid:%s' % order_book_id in line:
                    print line
                    in_file = True
                elif 'order_book_id=462753' and 'order_id=%s' % order_book_id in line:
                    print line
                    in_file = True

            if not in_file:
                print 'order_book_id %s Not Found!' % order_book_id

            inputfile.close()

    def parse_logfile_137d(self):

        order_book_ids = ['7021031022145834324', '7021031022145834323', '7021031022145834322', '7021031022145834317']

        logfile = self.optmenu()

        print '\n\n', '-' * 40, '\n\n', 'Session 1 - Test case 13, Section D: Full Order Book Scenario 7 - D', \
                      '-'*40, '\n\n'
        for order_book_id in order_book_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if 'id:136173' in line and 'oid:%s' % order_book_id in line:
                    print line
                    in_file = True
                elif 'order_book_id=136173' and 'order_id=%s' % order_book_id in line:
                    print line
                    in_file = True

            if not in_file:
                print 'order_book_id %s Not Found!' % order_book_id

            inputfile.close()

    def parse_logfile_138d(self):

        order_book_ids = ['7021031022145834316', '7021031022145834317']

        logfile = self.optmenu()

        print '\n\n', '-' * 40, '\n\n', 'Session 1 - Test case 13, Section D: Full Order Book Scenario 8 - D', \
                      '-'*40, '\n\n'
        for order_book_id in order_book_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if 'id:660461' in line and 'oid:%s' % order_book_id in line:
                    print line
                    in_file = True
                elif 'order_book_id=660461' and 'order_id=%s' % order_book_id in line:
                    print line
                    in_file = True

            if not in_file:
                print 'order_book_id %s Not Found!' % order_book_id

            inputfile.close()

    def parse_logfile_139d(self):

        order_book_ids = ['7021031022145834316', '7021031022145834332']

        logfile = self.optmenu()

        print '\n\n', '-' * 40, '\n\n', 'Session 1 - Test case 13, Section D: Full Order Book Scenario 9 - D', \
                      '-'*40, '\n\n'
        for order_book_id in order_book_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if 'id:201709' in line and 'oid:%s' % order_book_id in line:
                    print line
                    in_file = True
                elif 'order_book_id=201709' and 'order_id=%s' % order_book_id in line:
                    print line
                    in_file = True

            if not in_file:
                print 'order_book_id %s Not Found!' % order_book_id

            inputfile.close()

    def parse_logfile_1310d(self):

        order_book_ids = ['7021031022145834318', '7021031022145834319']

        logfile = self.optmenu()

        print '\n\n', '-' * 40, '\n\n', 'Session 1 - Test case 13, Section D: Full Order Book Scenario 10 - D', \
                      '-'*40, '\n\n'
        for order_book_id in order_book_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if 'id:1119213' in line and 'oid:%s' % order_book_id in line:
                    print line
                    in_file = True
                elif 'order_book_id=1119213' and 'order_id=%s' % order_book_id in line:
                    print line
                    in_file = True

            if not in_file:
                print 'order_book_id %s Not Found!' % order_book_id

            inputfile.close()

    def parse_logfile_1311d(self):

        order_book_ids = ['7021031017850906684', '7021031017850906716', '7021031017850906715', '7021031017850906689']

        logfile = self.optmenu()

        print '\n\n', '-' * 40, '\n\n', 'Session 1 - Test case 13, Section D: Full Order Book Scenario 11 - D', \
                      '-'*40, '\n\n'
        for order_book_id in order_book_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if 'id:3411873' in line and 'oid:%s' % order_book_id in line:
                    print line
                    in_file = True
                elif 'order_book_id=3411873' and 'order_id=%s' % order_book_id in line:
                    print line
                    in_file = True

            if not in_file:
                print 'order_book_id %s Not Found!' % order_book_id

            inputfile.close()

    def parse_logfile_1312d(self):

        order_book_ids = ['7021031017850906712', '7021031017850906709', '7021031017850906713', '7021031017850906717']

        logfile = self.optmenu()

        print '\n\n', '-' * 40, '\n\n', 'Session 1 - Test case 13, Section D: Full Order Book Scenario 12 - D', \
                      '-'*40, '\n\n'
        for order_book_id in order_book_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if 'id:4722593' in line and 'oid:%s' % order_book_id in line:
                    print line
                    in_file = True
                elif 'order_book_id=4722593' and 'order_id=%s' % order_book_id in line:
                    print line
                    in_file = True

            if not in_file:
                print 'order_book_id %s Not Found!' % order_book_id

            inputfile.close()

    def parse_logfile_1313d(self):

        order_book_ids = ['7021031017850870803', '7021031017850870806', '7021031017850870808', '7021031017850870809',
                          '7021031017850870810', '7021031017850870812', '7021031017850870814', '7021031017850870816',
                          '7021031017850870818', '7021031017850870820', '7021031017850870834']

        logfile = self.optmenu()

        print '\n\n', '-' * 40, '\n\n', 'Session 1 - Test case 13, Section D: Full Order Book Scenario 13 - D', \
                      '-'*40, '\n\n'
        for order_book_id in order_book_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if 'id:50991010' in line and 'oid:%s' % order_book_id in line:
                    print line
                    in_file = True
                elif 'order_book_id=50991010' and 'order_id=%s' % order_book_id in line:
                    print line
                    in_file = True

            if not in_file:
                print 'order_book_id %s Not Found!' % order_book_id

            inputfile.close()

    def parse_logfile_1314d(self):

        order_book_ids = ['7021031017850875208', '7021031017850875207', '7021031017850875206', '7021031017850875203',
                          '7021031017850875202', '7021031017850875201', '7021031017850875200', '7021031017850875199',
                          '7021031017850875198', '7021031017850875197', '7021031017850875196']

        logfile = self.optmenu()

        print '\n\n', '-' * 40, '\n\n', 'Session 1 - Test case 13, Section D: Full Order Book Scenario 14 - D', \
                      '-'*40, '\n\n'
        for order_book_id in order_book_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if 'id:52432802' in line and 'oid:%s' % order_book_id in line:
                    print line
                    in_file = True
                elif 'order_book_id=52432802' and 'order_id=%s' % order_book_id in line:
                    print line
                    in_file = True

            if not in_file:
                print 'order_book_id %s Not Found!' % order_book_id

            inputfile.close()

    def parse_logfile_1315d(self):

        order_book_ids = ['7021031017850870802', '7021031017850870804', '7021031017850870805', '7021031017850870807',
                          '7021031017850870811', '7021031017850870813', '7021031017850870815', '7021031017850870817',
                          '7021031017850870819', '7021031017850870821', '7021031017850870835', '7021031017850870836']

        logfile = self.optmenu()

        print '\n\n', '-' * 40, '\n\n', 'Session 1 - Test case 13, Section D: Full Order Book Scenario 15 - D', \
                      '-'*40, '\n\n'
        for order_book_id in order_book_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if 'id:855970' in line and 'oid:%s' % order_book_id in line:
                    print line
                    in_file = True
                elif 'order_book_id=855970' and 'order_id=%s' % order_book_id in line:
                    print line
                    in_file = True

            if not in_file:
                print 'order_book_id %s Not Found!' % order_book_id

            inputfile.close()

    def parse_logfile_1316d(self):

        order_book_ids = ['7021031017850875174',
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

        print '\n\n', '-' * 40, '\n\n', 'Session 1 - Test case 13, Section D: Full Order Book Scenario 16 - D', \
                      '-'*40, '\n\n'
        for order_book_id in order_book_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if 'id:6360994' in line and 'oid:%s' % order_book_id in line:
                    print line
                    in_file = True
                elif 'order_book_id=6360994' and 'order_id=%s' % order_book_id in line:
                    print line
                    in_file = True

            if not in_file:
                print 'order_book_id %s Not Found!' % order_book_id

            inputfile.close()

    def parse_logfile_1317d(self):

        order_book_ids = ['7021031017850870837',
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

        print '\n\n', '-' * 40, '\n\n', 'Session 1 - Test case 13, Section D: Full Order Book Scenario 17 - D', \
                      '-'*40, '\n\n'
        for order_book_id in order_book_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if 'id:50597794' in line and 'oid:%s' % order_book_id in line:
                    print line
                    in_file = True
                elif 'order_book_id=50597794' and 'order_id=%s' % order_book_id in line:
                    print line
                    in_file = True

            if not in_file:
                print 'order_book_id %s Not Found!' % order_book_id

            inputfile.close()

    def parse_logfile_1318d(self):

        order_book_ids = ['46600098', ]

        logfile = self.optmenu()

        print '\n\n', '-' * 40, '\n\n', 'Session 1 - Test case 13, Section D: Full Order Book Scenario 18 - D', \
                      '-'*40, '\n\n'
        for order_book_id in order_book_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if 'Add Order [id:%s]' % order_book_id in line:
                    print line
                    in_file = True
                elif 'Add Order [order_book_id=%s]' % order_book_id in line:
                    print line
                    in_file = True
                elif 'Clear Orderbook [id:%s]' % order_book_id in line:
                    print line
                    in_file = True
                elif 'Clear Orderbook' in line and 'order_book_id=%s' % order_book_id in line:
                    print line
                    in_file = True

            if not in_file:
                print 'order_book_id %s Not Found!' % order_book_id

            inputfile.close()

    def parse_logfile_1319d(self):

        order_book_ids = ['7021031017850870841',
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

        print '\n\n', '-' * 40, '\n\n', 'Session 1 - Test case 13, Section D: Full Order Book Scenario 19 - D', \
                      '-'*40, '\n\n'
        for order_book_id in order_book_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if 'id:50663330' in line and 'oid:%s' % order_book_id in line:
                    print line
                    in_file = True
                elif 'order_book_id=50663330' and 'order_id=%s' % order_book_id in line:
                    print line
                    in_file = True

            if not in_file:
                print 'order_book_id %s Not Found!' % order_book_id

            inputfile.close()

    def parse_logfile_1320c(self):

        order_book_ids = ['266148', ]

        logfile = self.optmenu()

        print '\n\n', '-' * 40, '\n\n', 'Session 1 - Test case 13, Section D: Full Order Book Scenario 20 - C', \
                      '-'*40, '\n\n'
        for order_book_id in order_book_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if 'Add Order [id:%s]' % order_book_id in line:
                    print line
                    in_file = True
                elif 'Add Order [order_book_id=%s]' % order_book_id in line:
                    print line
                    in_file = True
                elif 'Clear Orderbook [id:%s]' % order_book_id in line:
                    print line
                    in_file = True
                elif 'Clear Orderbook' in line and 'order_book_id=%s' % order_book_id in line:
                    print line
                    in_file = True

            if not in_file:
                print 'order_book_id %s Not Found!' % order_book_id

            inputfile.close()

    def parse_logfile_1321d(self):

        order_book_ids = ['4294840226', ]

        logfile = self.optmenu()

        print '\n\n', '-' * 40, '\n\n', 'Session 1 - Test case 13, Section D: Full Order Book Scenario 21 - D', \
                      '-'*40, '\n\n'
        for order_book_id in order_book_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if 'Add Order [id:%s]' % order_book_id in line:
                    print line
                    in_file = True
                elif 'Add Order [order_book_id=%s]' % order_book_id in line:
                    print line
                    in_file = True
                elif 'Clear Orderbook [id:%s]' % order_book_id in line:
                    print line
                    in_file = True
                elif 'Clear Orderbook' in line and 'order_book_id=%s' % order_book_id in line:
                    print line
                    in_file = True

            if not in_file:
                print 'order_book_id %s Not Found!' % order_book_id

            inputfile.close()

    def parse_logfile_1322d(self):

        order_book_ids = ['4294840225', ]

        logfile = self.optmenu()

        print '\n\n', '-' * 40, '\n\n', 'Session 1 - Test case 13, Section D: Full Order Book Scenario 22 - D', \
                      '-'*40, '\n\n'
        for order_book_id in order_book_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if 'Add Order [id:%s]' % order_book_id in line:
                    print line
                    in_file = True
                elif 'Add Order [order_book_id=%s]' % order_book_id in line:
                    print line
                    in_file = True
                elif 'Clear Orderbook [id:%s]' % order_book_id in line:
                    print line
                    in_file = True
                elif 'Clear Orderbook' in line and 'order_book_id=%s' % order_book_id in line:
                    print line
                    in_file = True

            if not in_file:
                print 'order_book_id %s Not Found!' % order_book_id

            inputfile.close()

    def parse_logfile_1323d(self):

        order_book_ids = ['7021030738677990946',
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

        print '\n\n', '-' * 40, '\n\n', 'Session 1 - Test case 13, Section D: Full Order Book Scenario 23 - D', \
                      '-'*40, '\n\n'
        for order_book_id in order_book_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if 'id:331684' in line and 'oid:%s' % order_book_id in line:
                    print line
                    in_file = True
                elif 'order_book_id=331684' and 'order_id=%s' % order_book_id in line:
                    print line
                    in_file = True

            if not in_file:
                print 'order_book_id %s Not Found!' % order_book_id

            inputfile.close()

    def parse_logfile_1324c(self):

        order_book_ids = ['7021031017850903065', '7021031017850903066']

        logfile = self.optmenu()

        print '\n\n', '-' * 40, '\n\n', 'Session 1 - Test case 13, Section D: Full Order Book Scenario 24 - C', \
                      '-'*40, '\n\n'
        for order_book_id in order_book_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if 'id:1118114' in line and 'oid:%s' % order_book_id in line:
                    print line
                    in_file = True
                elif 'order_book_id=1118114' and 'order_id=%s' % order_book_id in line:
                    print line
                    in_file = True

            if not in_file:
                print 'order_book_id %s Not Found!' % order_book_id

            inputfile.close()

    def parse_logfile_1325d(self):

        order_book_ids = ['1183650', ]

        logfile = self.optmenu()

        print '\n\n', '-' * 40, '\n\n', 'Session 1 - Test case 13, Section D: Full Order Book Scenario 25 - D', \
                      '-'*40, '\n\n'
        for order_book_id in order_book_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if 'Add Order [id:%s]' % order_book_id in line:
                    print line
                    in_file = True
                elif 'Add Order [order_book_id=%s]' % order_book_id in line:
                    print line
                    in_file = True
                elif 'Clear Orderbook [id:%s]' % order_book_id in line:
                    print line
                    in_file = True
                elif 'Clear Orderbook' in line and 'order_book_id=%s' % order_book_id in line:
                    print line
                    in_file = True

            if not in_file:
                print 'order_book_id %s Not Found!' % order_book_id

            inputfile.close()

    def parse_logfile_1326d(self):

        order_book_ids = ['7021031017850904464', '7021031017850904463']

        logfile = self.optmenu()

        print '\n\n', '-' * 40, '\n\n', 'Session 1 - Test case 13, Section D: Full Order Book Scenario 26 - D', \
                      '-'*40, '\n\n'
        for order_book_id in order_book_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if 'id:35655585' in line and 'oid:%s' % order_book_id in line:
                    print line
                    in_file = True
                elif 'order_book_id=35655585' and 'order_id=%s' % order_book_id in line:
                    print line
                    in_file = True

            if not in_file:
                print 'order_book_id %s Not Found!' % order_book_id

            inputfile.close()

    def parse_logfile_1327d(self):

        order_book_ids = ['593832', ]

        logfile = self.optmenu()

        print '\n\n', '-' * 40, '\n\n', 'Session 1 - Test case 13, Section D: Full Order Book Scenario 27 - D', \
                      '-'*40, '\n\n'
        for order_book_id in order_book_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if 'Add Order [id:%s]' % order_book_id in line:
                    print line
                    in_file = True
                elif 'Add Order [order_book_id=%s]' % order_book_id in line:
                    print line
                    in_file = True
                elif 'Clear Orderbook [id:%s]' % order_book_id in line:
                    print line
                    in_file = True
                elif 'Clear Orderbook' in line and 'order_book_id=%s' % order_book_id in line:
                    print line
                    in_file = True

            if not in_file:
                print 'order_book_id %s Not Found!' % order_book_id

            inputfile.close()

    def parse_logfile_1328c(self):

        order_book_ids = ['44371880', ]

        logfile = self.optmenu()

        print '\n\n', '-' * 40, '\n\n', 'Session 1 - Test case 13, Section D: Full Order Book Scenario 28 - C', \
                      '-'*40, '\n\n'
        for order_book_id in order_book_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if 'Add Order [id:%s]' % order_book_id in line:
                    print line
                    in_file = True
                elif 'Add Order [order_book_id=%s]' % order_book_id in line:
                    print line
                    in_file = True
                elif 'Clear Orderbook [id:%s]' % order_book_id in line:
                    print line
                    in_file = True
                elif 'Clear Orderbook' in line and 'order_book_id=%s' % order_book_id in line:
                    print line
                    in_file = True

            if not in_file:
                print 'order_book_id %s Not Found!' % order_book_id

            inputfile.close()

    def parse_logfile_1329d(self):

        order_book_ids = ['7021031017850906717', '7021031017850906713']

        logfile = self.optmenu()

        print '\n\n', '-' * 40, '\n\n', 'Session 1 - Test case 13, Section D: Full Order Book Scenario 29 - D', \
                      '-'*40, '\n\n'
        for order_book_id in order_book_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if 'id:7606177' in line and 'oid:%s' % order_book_id in line:
                    print line
                    in_file = True
                elif 'order_book_id=7606177' and 'order_id=%s' % order_book_id in line:
                    print line
                    in_file = True

            if not in_file:
                print 'order_book_id %s Not Found!' % order_book_id

            inputfile.close()

    def parse_logfile_1330d(self):

        order_book_ids = ['7021031017850886884',
                          '7021031017850886879',
                          '7021031017850886878',
                          '7021031017850886880',
                          '7021031017850886881',
                          '7021031017850886882',
                          '7021031017850886883']

        logfile = self.optmenu()

        print '\n\n', '-' * 40, '\n\n', 'Session 1 - Test case 13, Section D: Full Order Book Scenario 30 - D', \
                      '-'*40, '\n\n'
        for order_book_id in order_book_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if 'id:21368738' in line and 'oid:%s' % order_book_id in line:
                    print line
                    in_file = True
                elif 'order_book_id=21368738' and 'order_id=%s' % order_book_id in line:
                    print line
                    in_file = True

            if not in_file:
                print 'order_book_id %s Not Found!' % order_book_id

            inputfile.close()

    def parse_logfile_16a(self):

        trade_ids = ['7021031022145830913',
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

        print '\n\n', '-' * 40, 'Session 1 - Test case 16, Scenario 1: Interpretation of Trade and Trade Amendment', \
                      '-'*40, '\n\n'
        for trade_id in trade_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if '[id:328693]' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line
                elif '[order_book_id=328693]' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % trade_id

            inputfile.close()

    def parse_logfile_16b(self):

        trade_ids = ['7021030734383022129',
                     '7021030734383022134',
                     '7021030734383022141']

        logfile = self.optmenu()

        print '\n\n', '-' * 40, 'Session 1 - Test case 16, Scenario 2: Interpretation of Trade and Trade Amendment', \
                      '-'*40, '\n\n'
        for trade_id in trade_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if '[id:1050581]' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line
                elif '[order_book_id=1050581]' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % trade_id

            inputfile.close()

    def parse_logfile_16bc(self):

        trade_ids = ['7021030734383022144', ]

        logfile = self.optmenu()

        print '\n\n', '-' * 40, 'Session 1 - Test case 16, Scenario 3: Interpretation of Trade and Trade Amendment', \
                      '-'*40, '\n\n'
        for trade_id in trade_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if '[id:2426837]' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line
                elif '[order_book_id=2426837]' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % trade_id

            inputfile.close()

    def parse_logfile_16d(self):

        trade_ids = ['7021031017850863654',
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

        print '\n\n', '-' * 40, 'Session 1 - Test case 16, Scenario 4: Interpretation of Trade and Trade Amendment', \
                      '-'*40, '\n\n'
        for trade_id in trade_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if '[id:3280801]' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line
                elif '[order_book_id=3280801]' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % trade_id

            inputfile.close()

    def parse_logfile_16e(self):

        trade_ids = ['7021031017850863635',
                     '7021031017850863636',
                     '7021031017850863637']

        logfile = self.optmenu()

        print '\n\n', '-' * 40, 'Session 1 - Test case 16, Scenario 5: Interpretation of Trade and Trade Amendment', \
                      '-'*40, '\n\n'
        for trade_id in trade_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if '[id:1445794]' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line
                elif '[order_book_id=1445794]' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % trade_id

            inputfile.close()

    def parse_logfile_16f(self):

        trade_ids = ['7021031022145830960', '7021031022145830963']

        logfile = self.optmenu()

        print '\n\n', '-' * 40, 'Session 1 - Test case 16, Scenario 6: Interpretation of Trade and Trade Amendment', \
                      '-'*40, '\n\n'
        for trade_id in trade_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if '[id:660461]' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line
                elif '[order_book_id=660461]' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % trade_id

            inputfile.close()

    def parse_logfile_16g(self):

        trade_ids = ['7021031022145830958', '7021031022145830961', '7021031022145830964']

        logfile = self.optmenu()

        print '\n\n', '-' * 40, 'Session 1 - Test case 16, Scenario 7: Interpretation of Trade and Trade Amendment', \
                      '-'*40, '\n\n'
        for trade_id in trade_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if '[id:201709]' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line
                elif '[order_book_id=201709]' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % trade_id

            inputfile.close()

    def parse_logfile_16h(self):

        trade_ids = ['7021031017850863644',
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

        print '\n\n', '-' * 40, 'Session 1 - Test case 16, Scenario 8: Interpretation of Trade and Trade Amendment', \
                      '-'*40, '\n\n'
        for trade_id in trade_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if '[id:3411873]' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line
                elif '[order_book_id=3411873]' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % trade_id

            inputfile.close()

    def parse_logfile_16i(self):

        trade_ids = ['7021031017850863685', '7021031017850863691', '7021031017850863697', '7021031017850863703']

        logfile = self.optmenu()

        print '\n\n', '-' * 40, 'Session 1 - Test case 16, Scenario 9: Interpretation of Trade and Trade Amendment', \
                      '-'*40, '\n\n'
        for trade_id in trade_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if '[id:3215265]' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line
                elif '[order_book_id=3215265]' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % trade_id

            inputfile.close()

    def parse_logfile_16j(self):

        trade_ids = ['7021031017850863617',
                     '7021031017850863617',
                     '7021031017850863617',
                     '7021031017850863617',
                     '7021031017850863617']

        logfile = self.optmenu()

        print '\n\n', '-' * 40, 'Session 1 - Test case 16, Scenario 10: Interpretation of Trade and Trade Amendment', \
                      '-'*40, '\n\n'
        for trade_id in trade_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if '[id:855970]' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line
                elif '[order_book_id=855970]' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % trade_id

            inputfile.close()

    def parse_logfile_16k(self):

        trade_ids = ['7021030738677989383',
                     '7021030738677989383',
                     '7021030738677989383',
                     '7021030738677989383',
                     '7021030738677989383']

        logfile = self.optmenu()

        print '\n\n', '-' * 40, 'Session 1 - Test case 16, Scenario 11: Interpretation of Trade and Trade Amendment', \
                      '-'*40, '\n\n'
        for trade_id in trade_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if '[id:921508]' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line
                elif '[order_book_id=921508]' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % trade_id

            inputfile.close()

    def parse_logfile_16l(self):

        trade_ids = ['7021031017850863640',
                     '7021031017850863641',
                     '7021031017850863642',
                     '7021031017850863643']

        logfile = self.optmenu()

        print '\n\n', '-' * 40, 'Session 1 - Test case 16, Scenario 12: Interpretation of Trade and Trade Amendment', \
                      '-'*40, '\n\n'
        for trade_id in trade_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if '[id:1183650]' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line
                elif '[order_book_id=1183650]' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % trade_id

            inputfile.close()

    def parse_logfile_16m(self):

        trade_ids = ['7021031017850863658',
                     '7021031017850863658',
                     '7021031017850863658',
                     '7021031017850863658',
                     '7021031017850863658',
                     '7021031017850863658',
                     '7021031017850863658',
                     '7021031017850863658',
                     '7021031017850863658']

        logfile = self.optmenu()

        print '\n\n', '-' * 40, 'Session 1 - Test case 16, Scenario 13: Interpretation of Trade and Trade Amendment', \
                      '-'*40, '\n\n'
        for trade_id in trade_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if '[id:46993314]' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line
                elif '[order_book_id=46993314]' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % trade_id

            inputfile.close()

    def parse_logfile_16n(self):

        trade_ids = ['7021031017850863645', ]

        logfile = self.optmenu()

        print '\n\n', '-' * 40, 'Session 1 - Test case 16, Scenario 14: Interpretation of Trade and Trade Amendment', \
                      '-'*40, '\n\n'
        for trade_id in trade_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if '[id:7606177]' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line
                elif '[order_book_id=7606177]' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % trade_id

            inputfile.close()

    def parse_logfile_16o(self):

        trade_ids = ['7021030738677989413', '7021030738677989422', '7021030738677989431']

        logfile = self.optmenu()

        print '\n\n', '-' * 40, 'Session 1 - Test case 16, Scenario 15: Interpretation of Trade and Trade Amendment', \
                      '-'*40, '\n\n'
        for trade_id in trade_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if '[id:3542948]' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line
                elif '[order_book_id=3542948]' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % trade_id

            inputfile.close()

    def parse_logfile_16p(self):

        trade_ids = ['7021031017850863676', '7021031017850863677']

        logfile = self.optmenu()

        print '\n\n', '-' * 40, 'Session 1 - Test case 16, Scenario 16: Interpretation of Trade and Trade Amendment', \
                      '-'*40, '\n\n'
        for trade_id in trade_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if '[id:21368738]' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line
                elif '[order_book_id=21368738]' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % trade_id

            inputfile.close()

    def parse_logfile_17a(self):

        trade_ids = ['7021030734383022081', '7021030734383022082']

        logfile = self.optmenu()

        print '\n\n', '-' * 40, 'Session 1 - Test case 17, Scenario 1: Interpretation of Trade and Trade Amendment', \
                      '-'*40, '\n\n'
        for trade_id in trade_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if '[id:11995093]' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line
                elif '[order_book_id=11995093]' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % trade_id

            inputfile.close()

    def parse_logfile_17b(self):

        trade_ids = ['7021030734383022150', ]

        logfile = self.optmenu()

        print '\n\n', '-' * 40, 'Session 1 - Test case 17, Scenario 2: Interpretation of Trade and Trade Amendment', \
                      '-'*40, '\n\n'
        for trade_id in trade_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if '[id:10684373]' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line
                elif '[order_book_id=10684373]' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % trade_id

            inputfile.close()

    def parse_logfile_17c(self):

        trade_ids = ['7021030734383022128', ]

        logfile = self.optmenu()

        print '\n\n', '-' * 40, 'Session 1 - Test case 17, Scenario 3: Interpretation of Trade and Trade Amendment', \
                      '-'*40, '\n\n'
        for trade_id in trade_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if '[id:4294707157]' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line
                elif '[order_book_id=4294707157]' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % trade_id

            inputfile.close()

    def parse_logfile_17d(self):

        trade_ids = ['7021030734383022083',
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

        print '\n\n', '-' * 40, 'Session 1 - Test case 17, Scenario 4: Interpretation of Trade and Trade Amendment', \
                      '-'*40, '\n\n'
        for trade_id in trade_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if '[id:1771400]' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line
                elif '[order_book_id=1771400]' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % trade_id

            inputfile.close()

    def parse_logfile_17e(self):

        trade_ids = ['7021030734383022130', '7021030734383022136', '7021030734383022143']

        logfile = self.optmenu()

        print '\n\n', '-' * 40, 'Session 1 - Test case 17, Scenario 5: Interpretation of Trade and Trade Amendment', \
                      '-'*40, '\n\n'
        for trade_id in trade_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if '[id:1181653]' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line
                elif '[order_book_id=1181653]' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % trade_id

            inputfile.close()

    def parse_logfile_17f(self):

        trade_ids = ['7021030734383022149', ]

        logfile = self.optmenu()

        print '\n\n', '-' * 40, 'Session 1 - Test case 17, Scenario 6: Interpretation of Trade and Trade Amendment', \
                      '-'*40, '\n\n'
        for trade_id in trade_ids:
            inputfile = open(logfile, 'r')
            in_file = False
            for line in inputfile.readlines():
                if '[id:7407573]' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line
                elif '[order_book_id=7407573]' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and 'trade_id=%s' % trade_id in line:
                    in_file = True
                    print line
                elif 'TradeAmendment' in line and '[tid:%s]' % trade_id in line:
                    in_file = True
                    print line

            if not in_file:
                print 'Trade ID %s Not Found!' % trade_id

            inputfile.close()

    def run_tests(self):

        self.parse_logfile_1a()
        self.parse_logfile_1b()
        self.parse_logfile_1c()
        # self.parse_logfile_2()
        self.parse_logfile_3()
        self.parse_logfile_04()
        # self.parse_logfile_05()
        self.parse_logfile_08()
        self.parse_logfile_10()
        self.parse_logfile_131d()
        self.parse_logfile_132c()
        self.parse_logfile_133d()
        self.parse_logfile_134d()
        self.parse_logfile_135d()
        self.parse_logfile_136c()
        self.parse_logfile_137d()
        self.parse_logfile_138d()
        self.parse_logfile_139d()
        self.parse_logfile_1310d()
        self.parse_logfile_1311d()
        self.parse_logfile_1312d()
        self.parse_logfile_1313d()
        self.parse_logfile_1314d()
        self.parse_logfile_1315d()
        self.parse_logfile_1316d()
        self.parse_logfile_1317d()
        self.parse_logfile_1318d()
        self.parse_logfile_1319d()
        self.parse_logfile_1320c()
        self.parse_logfile_1321d()
        self.parse_logfile_1322d()
        self.parse_logfile_1323d()
        self.parse_logfile_1324c()
        self.parse_logfile_1325d()
        self.parse_logfile_1326d()
        self.parse_logfile_1327d()
        self.parse_logfile_1328c()
        self.parse_logfile_1329d()
        self.parse_logfile_1330d()
        self.parse_logfile_16a()
        self.parse_logfile_16b()
        self.parse_logfile_16bc()
        self.parse_logfile_16d()
        self.parse_logfile_16e()
        self.parse_logfile_16f()
        self.parse_logfile_16g()
        self.parse_logfile_16h()
        self.parse_logfile_16i()
        self.parse_logfile_16j()
        self.parse_logfile_16k()
        self.parse_logfile_16l()
        self.parse_logfile_16m()
        self.parse_logfile_16n()
        self.parse_logfile_16o()
        self.parse_logfile_16p()
        self.parse_logfile_17a()
        self.parse_logfile_17b()
        self.parse_logfile_17c()
        self.parse_logfile_17d()
        self.parse_logfile_17e()
        self.parse_logfile_17f()


logRead = logfile_analiser()
logRead.optmenu()
# logRead.parseLogfile()
# logRead.parseLogfile2()
# logRead.parseLogfile3()
# logRead.parseLogfile4()
logRead.run_tests()
# logRead.parseLogfile6()
