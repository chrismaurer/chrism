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

        OrderBookIDs = ['MHI  00411130000000',]
#        OrderBookIDs = ['HHI  02210130011800', 'MHI  00411130000000', 'HB3  00412130000000', 'HSI  02311130019600', 'HKB  00611130007250', 'HSI  00410130000000']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '_-'*40
            inputFile = open(logfile, 'r')
            found = False
            count = 0
            for line in inputFile.readlines():
                if not found:
                    if OrderBookID in line:
                        count = 1
                        found = True
                if count in range(1,3):
                    print line
                    count += 1
                if count == 3:
                    found = False
                    count = 0

            inputFile.close()

    def parseLogfile2(self):

        OrderBookIDs = ['DS',]
#        OrderBookIDs = ['HHI  02210130011800', 'MHI  00411130000000', 'HB3  00412130000000', 'HSI  02311130019600', 'HKB  00611130007250', 'HSI  00410130000000']

        logfile = self.optmenu()

        for OrderBookID in OrderBookIDs:
            print '_-'*40
            inputFile = open(logfile, 'r')
            count = 0
            for line in inputFile.readlines():
                if OrderBookID in line:
                    count += 1

            inputFile.close()

            print 'count =', count

logRead = logfile_analiser()
logRead.optmenu()
logRead.parseLogfile()
#logRead.parseLogfile2()
    