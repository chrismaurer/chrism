#~TestCaseName: logExceptions
#~TestCaseSummary: This is a library module for storing a master list of logfile exceptions

'''.'''

__author__ = 'Chris Maurer (chris.maurer@tradingtechnologies.com)'
__version__ = '1.1'

import re

def logExceptions():
    logExceptions = []
    exceptionFile = 'GW_log_filter-ALL.txt'
    f = file(exceptionFile, 'r')
    for line in f.readlines():
        logExceptions.append(re.compile('.*' + line + '.*', re.U ))
#        logExceptions.append(re.compile(line, re.I ))
    return logExceptions
