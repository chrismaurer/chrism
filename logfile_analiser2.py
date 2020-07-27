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

        OrderBookIDs = ['0',]

        logfile = self.optmenu()

        total_count = 8
        for OrderBookID in OrderBookIDs:
            print '-'*40, '1.1 A, Section 1: Ref Data (Next Day Effective Series)', '-'*40
            inputFile = open(logfile, 'rb')
            found = False
            count = 0
            in_file = False
            for line in inputFile.readlines():
                if found:
                    if count == total_count or 'DERIVATIVES_' in line:
                        found = False
                if not found:
                    if 'Contract Created' in line or 'DERIVATIVES_NON_SOM_SERIES_DEFINITIONS' in line:
                        if '[id:%s]' % OrderBookID in line and 'HSIQ4' in line:
                            count = 0
                            found = True
                if found:
                    if count < total_count and '[id:%s]' % OrderBookID in line:
                        print line
                        in_file = True
                        count += 1

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile2(self):

        logfile = self.optmenu()

        total_count = 4
        print '.'*40, '1.6 C, Test Case 8: Market Alert', '.'*40
        inputFile = open(logfile, 'rb')
        in_file = False
        found = False
        count = 0
        for line in inputFile.readlines():
            if 'marketalert' in line and '[SESSION 5 - PART I]' in line:
                found = True
                in_file = True
            if 'marketalert' in line:
                print line
            count += 1

        if not in_file:
            print 'Market Alert Messages Not Found!'
    
        inputFile.close()

    def parseLogfile3(self):

       OrderBookIDs = ['6358831714613149778',
                       '6358831714613154242',
                       '6358831714613158706',
                       '6358831714613137822',
                       '6358831714613142286',
                       '6358831714613144471',
                       '6358831714613148935',
                       '6358831714613153399',
                       '6358831714613157863',
                       '6358831714613140535',
                       '6358831714613147184',
                       '6358831714613151648',
                       '6358831714613156112',
                       '6358831714613160576',
                       '6358831714613137940',
                       '6358831714613141041',
                       '6358831714613142404',
                       '6358831714613144589',
                       '6358831714613147690',
                       '6358831714613149053',
                       '6358831714613152154',
                       '6358831714613153517',
                       '6358831714613156618',
                       '6358831714613157981',
                       '6358831714613161082',
                       '6358831714613137978',
                       '6358831714613142442',
                       '6358831714613144627',
                       '6358831714613149091',
                       '6358831714613153555',
                       '6358831714613158019',
                       '6358831714613141240',
                       '6358831714613147889',
                       '6358831714613152353',
                       '6358831714613156817',
                       '6358831714613139754',
                       '6358831714613141739',
                       '6358831714613144218',
                       '6358831714613146403',
                       '6358831714613148388',
                       '6358831714613150867',
                       '6358831714613152852',
                       '6358831714613155331',
                       '6358831714613157316',
                       '6358831714613159795',
                       '6358831714613140766',
                       '6358831714613147415',
                       '6358831714613151879',
                       '6358831714613156343',
                       '6358831714613160807',
                       '6358831714613137906',
                       '6358831714613142370',
                       '6358831714613144555',
                       '6358831714613149019',
                       '6358831714613153483',
                       '6358831714613157947',
                       '6358831714613139644',
                       '6358831714613144108',
                       '6358831714613146293',
                       '6358831714613150757',
                       '6358831714613155221',
                       '6358831714613159685',
                       '6358831714613140172',
                       '6358831714613146821',
                       '6358831714613151285',
                       '6358831714613155749',
                       '6358831714613160213',
                       '6358831714613140373',
                       '6358831714613147022',
                       '6358831714613151486',
                       '6358831714613155950',
                       '6358831714613160414',
                       '6358831714613141583',
                       '6358831714613148232',
                       '6358831714613152696',
                       '6358831714613157160',
                       '6358831714613139252',
                       '6358831714613143716',
                       '6358831714613145901',
                       '6358831714613150365',
                       '6358831714613154829',
                       '6358831714613159293']

       logfile = self.optmenu()

       for OrderBookID in OrderBookIDs:
           print '^'*40, '1.6 C, Test Case 11: Agg / Full Order Book', '^'*40
           inputFile = open(logfile, 'r')
           in_file = False
           for line in inputFile.readlines():
               if '[side:' in line and '[oid:%s]' % OrderBookID in line:
                   print line
                   in_file = True

           if not in_file:
               print 'OrderBookID %s Not Found!' % OrderBookID

           inputFile.close()

    def parseLogfile3a(self):

       # OrderBookIDs =  ['6358831714613161143',
       #                  '6358831714613156886',
       #                  '6358831714613156679',
       #                  '6358831714613152422',
       #                  '6358831714613152215',
       #                  '6358831714613147958',
       #                  '6358831714613147751',
       #                  '6358831714613141309',
       #                  '6358831714613141102',
       #                  '6358831714613157082',
       #                  '6358831714613152618',
       #                  '6358831714613148154',
       #                  '6358831714613141505',
       #                  '6358831714613160725',
       #                  '6358831714613156261',
       #                  '6358831714613151797',
       #                  '6358831714613147333',
       #                  '6358831714613140684',
       #                  '6358831714613159195',
       #                  '6358831714613154731',
       #                  '6358831714613150267',
       #                  '6358831714613145803',
       #                  '6358831714613143618',
       #                  '6358831714613139154',
       #                  '6358831714613160675',
       #                  '6358831714613156211',
       #                  '6358831714613151747',
       #                  '6358831714613147283',
       #                  '6358831714613140634',
       #                  '6358831714613160983',
       #                  '6358831714613156519',
       #                  '6358831714613152055',
       #                  '6358831714613147591',
       #                  '6358831714613140942',
       #                  '6358831714613156994',
       #                  '6358831714613152530',
       #                  '6358831714613148066',
       #                  '6358831714613141417',
       #                  '6358831714613158583',
       #                  '6358831714613154119',
       #                  '6358831714613149655',
       #                  '6358831714613145191',
       #                  '6358831714613143006',
       #                  '6358831714613138542',
       #                  '6358831714613158779',
       #                  '6358831714613154315',
       #                  '6358831714613149851',
       #                  '6358831714613145387',
       #                  '6358831714613143202',
       #                  '6358831714613138738',
       #                  '6358831714613160382',
       #                  '6358831714613155918',
       #                  '6358831714613151454',
       #                  '6358831714613146990',
       #                  '6358831714613140341',
       #                  '6358831714613157377',
       #                  '6358831714613152913',
       #                  '6358831714613148449',
       #                  '6358831714613141800',
       #                  '6358831714613150693',
       #                  '6358831714613155157',
       #                  '6358831714613159621',
       #                  '6358831714613140453',
       #                  '6358831714613147102',
       #                  '6358831714613151566',
       #                  '6358831714613156030',
       #                  '6358831714613160494']

       OrderBookIDs =  ['6358831714613150693']

       logfile = self.optmenu()

       for OrderBookID in OrderBookIDs:
           print '^'*40, '1.6 C, Test Case 11: Agg / Full Order Book - SOM (p.375)', '^'*40
           inputFile = open(logfile, 'r')
           in_file = False
           for line in inputFile.readlines():
               if 'Add Order [id:8258864] [oid:%s]' % OrderBookID in line:
                   print line
                   in_file = True

           if not in_file:
               print 'OrderBookID %s Not Found!' % OrderBookID

           inputFile.close()

    def parseLogfile4(self):

        OrderBookIDs = ['63588064559107415',]

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, '1.6 C, Test Case 12: Trade and Trade Amend (p.377)', '^'*40
            inputFile = open(logfile, 'rb')
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
                print 'Trade ID %s Not Found!' % OrderBookID
        
            inputFile.close()

    def parseLogfile4a(self):

        OrderBookIDs = ['63588060264139326',]

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '^'*40, '1.6 C, Test Case 12: Trade and Trade Amend - SOM (p.381)', '^'*40
            inputFile = open(logfile, 'rb')
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
                print 'Trade ID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile5(self):

#        OrderBookIDs = ['5181346', '656373', '331181', '19531733', '55185314', '56823714', '135074', '5836706', '855071', '16060718']
        OrderBookIDs = ['5245703',]

        logfile = self.optmenu()

        total_count = 10
        for OrderBookID in OrderBookIDs:
            print '-'*40, '1.6 D, Test Case 1: Ref Data', '-'*40
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

    def parseLogfile6(self):

        OrderBookIDs = ['21956958',]

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '-'*40, '1.6 D, Test Case 7: Series Status Data', '-'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if 'Series Status Received [obId:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile7(self):

        logfile = self.optmenu()

        print '.'*40, '1.6 D, Test Case 7: Market Alert', '.'*40
        inputFile = open(logfile, 'rb')
        in_file = False
        found = False
        for line in inputFile.readlines():
            if not found:
                if 'marketalert' in line and '[SESSION 5 - PART II]' in line:
                    found = True
                    in_file = True
            if found:
                if 'Market Alert' in line:
                    print line
                else:
                    found = False

        if not in_file:
            print 'Market Alert Messages Not Found!'
    
        inputFile.close()

    def parseLogfile8(self):

        OrderBookIDs = ['6360365812506719900',]

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '-'*40, '1.6 D, Test Case 7: Order Book Data', '-'*40
            inputFile = open(logfile, 'r')
            in_file = False
            for line in inputFile.readlines():
                if 'Add Order [id:4589918] [oid:%s]' % OrderBookID in line:
                    print line
                    in_file = True

            if not in_file:
                print 'OrderBookID %s Not Found!' % OrderBookID

            inputFile.close()

    def parseLogfile9(self):

       OrderBookIDs =  ['6361949929589480942',]

       logfile = self.optmenu()

       for OrderBookID in OrderBookIDs:
           print '^'*40, '1.7 A, TC 2: Special Trading Arrangement - SOM (p.404)', '^'*40
           inputFile = open(logfile, 'r')
           in_file = False
           for line in inputFile.readlines():
               if 'Add Order [id:4589918] [oid:%s]' % OrderBookID in line:
                   print line
                   in_file = True

           if not in_file:
               print 'OrderBookID %s Not Found!' % OrderBookID

           inputFile.close()

    def parseLogfile10(self):

       OrderBookIDs =  ['6361553830525603794', '6361553830525603949']

       logfile = self.optmenu()

       for OrderBookID in OrderBookIDs:
           print '^'*40, '1.7 B, TC 2: Special Trading Arrangement - SOM (p.408)', '^'*40
           inputFile = open(logfile, 'r')
           in_file = False
           for line in inputFile.readlines():
               if 'Add Order [id:1051515] [oid:%s]' % OrderBookID in line:
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
logRead.parseLogfile3a()
logRead.parseLogfile4()
logRead.parseLogfile4a()
# logRead.parseLogfile5()
# logRead.parseLogfile6()
# logRead.parseLogfile7()
# logRead.parseLogfile8()
# logRead.parseLogfile9()
# logRead.parseLogfile10()