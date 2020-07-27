#~TestCaseName: pyrate_log_analiser
#~TestCaseSummary: This program reads logfiles from C:\logs and returns any unexpected messages

'''.'''

__author__ = 'Chris Maurer (chris.maurer@tradingtechnologies.com)'
__version__ = '1.1'

import os
import logging
from optparse import OptionParser

log = logging.getLogger(__name__)

class pyrate_log_analiser():

    def optmenu(self):
        parser = OptionParser()
        parser.add_option('-f', '--file', dest='filename',
                          help='logfile to be read', metavar='filename')
#        parser.add_option('-t', '--top', dest='topN',
#                          help='The "Top n" number of peak TPS / RTT values to be returned',
#                          metavar='integer')
        optmenu, args = parser.parse_args()
#        if optmenu.topN == None:
#            self.topN = 5
#        else:
#            self.topN = int(optmenu.topN)
        return optmenu.filename

    def parseLogfile(self):
        pyrate_log = self.optmenu()
#        resultsFile = os.getcwd() + '\\' + 'results.csv'
        inputFile = open(pyrate_log, 'r')
#        outputFile = open(resultsFile, 'w')
        counter = 1
        for line in inputFile.readlines():
            if counter == 12:
                break
            if 'DEBUG | commontests.utils' in line:
                print line
                counter += 1
            elif 'icaptain | nose.failure:Failure' in line:
                print line
                counter += 1
            elif 'INFO | icaptain | Executing' in line:
                print line
                counter += 1
            elif 'WARNING | icaptain | Timeout waiting for an OnServerUp' in line:
                print line
                counter += 1
#                output = line.split(' ')
##                for o in output:
##                    print o, '['+str(output.index(o))+']'
##                break
#                timestamp = output[1]
#                timestamp = str(timestamp).split('.')[0]
#                tto = output[11]
#                sok = output[-2]
#                rtt = output[-1].split('=')[-1]
#                rtt = rtt.rstrip('\n')
#                outputFile.write(','.join([timestamp,rtt,sok])+'\n')
#                timeStampList.append(timestamp)
#                RTTdict[int(rtt)] = timestamp, sok.rstrip(',')
#                transDict[rec] = timestamp, tto, sok.rstrip(','), int(rtt)
#                rec+=1
#        inputFile.close()
#        outputFile.close()
#        self.transDict = transDict

logRead = pyrate_log_analiser()
logRead.optmenu()
logRead.parseLogfile()

