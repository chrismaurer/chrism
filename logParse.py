#~TestCaseName: logParse
#~TestCaseSummary: This program reads logfiles from C:\logs and returns any unexpected messages

'''.'''

__author__ = 'Chris Maurer (chris.maurer@tradingtechnologies.com)'
__version__ = '1.1'

import os
import logging
from optparse import OptionParser

log = logging.getLogger(__name__)

class logParse():

    def optmenu(self):
        parser = OptionParser()
        parser.add_option('-f', '--file', dest='filename',
                          help='logfile to be read', metavar='filename')
        parser.add_option('-t', '--top', dest='topN',
                          help='The "Top n" number of peak TPS / RTT values to be returned',
                          metavar='integer')
        optmenu, args = parser.parse_args()
        if optmenu.topN == None:
            self.topN = 5
        else:
            self.topN = int(optmenu.topN)
        return optmenu.filename

    def parseLogfile(self):
        RTTdict = {}
        transDict = {}
        timeStampList = []
        filename = self.optmenu()
        logfile = filename
        resultsFile = os.getcwd() + '\\' + 'results.csv'
        inputFile = open(logfile, 'r')
        outputFile = open(resultsFile, 'w')
        rec = 0
        for line in inputFile.readlines():
            if 'RTT=' in line:
                output = line.split(' ')
#                for o in output:
#                    print o, '['+str(output.index(o))+']'
#                break
                timestamp = output[1]
                timestamp = str(timestamp).split('.')[0]
                tto = output[11]
                sok = output[-2]
                rtt = output[-1].split('=')[-1]
                rtt = rtt.rstrip('\n')
                outputFile.write(','.join([timestamp,rtt,sok])+'\n')
                timeStampList.append(timestamp)
                RTTdict[int(rtt)] = timestamp, sok.rstrip(',')
                transDict[rec] = timestamp, tto, sok.rstrip(','), int(rtt)
                rec+=1
        inputFile.close()
        outputFile.close()
        self.transDict = transDict

    def calcPeakTPS(self):
        transDict = self.transDict
        transList = transDict.values()
        TPSdict = {}
        timeStampList = []
        uniqTimeStamps = []
        peakTimeList = []
        for t in transList:
            timeStampList.append(t[0])
        for timeStamp in timeStampList:
            if timeStamp not in uniqTimeStamps:
                uniqTimeStamps.append(timeStamp)
        for uniqTimeStamp in uniqTimeStamps:
            TPSdict[uniqTimeStamp] = timeStampList.count(uniqTimeStamp)
        TPSlist = TPSdict.values()
        TPSlist.sort(reverse=True)
        peakTPSlist = TPSlist[0:self.topN]
        if self.topN > 1:
            print '\nTop %s Peak TPS values\n-------------------------' % (self.topN)
        else:
            print '\nTop Peak TPS value\n-------------------------'
        for peakVal in peakTPSlist:
            for idx in TPSdict.items():
                if peakVal in idx:
                    if idx[0] not in peakTimeList:
                        peakTPStime = TPSdict.items()[TPSdict.items().index(idx)][0]
                        peakTimeList.append(peakTPStime)
                        print '%s TPS @ %s' % (peakVal, peakTPStime)
                        break

    def calcPeakRTT(self):
        transDict = self.transDict
        transList = transDict.values()
        RTTlist = []
        sokList = []
        for t in transList:
            RTTlist.append(t[-1])
        RTTlist.sort(reverse=True)
        peakRTTlist = RTTlist[0:self.topN]
        if self.topN > 1:
            print '\nTop %s Peak RTT values\n-------------------------' % (self.topN)
        else:
            print '\nTop Peak RTT value\n-------------------------'
        for peakVal in peakRTTlist:
            for trans in transList:
                if peakVal in trans:
                    if trans[-2] not in sokList:
                        timestamp = trans[0]
                        siteOrderKey = trans[-2]
                        print '%s RTT @ %s, sok = %s' % (peakVal, timestamp, siteOrderKey)
                        sokList.append(trans[-2])
                        break

logRead = logParse()
logRead.optmenu()
logRead.parseLogfile()
logRead.calcPeakTPS()
logRead.calcPeakRTT()

