'''TT to OMX Order Number Translator

This script takes an OM Gateway Order Number as input and returns the same Order Number in
OMX-Nasdaq native format.
'''

__author__ = 'Chris Maurer (chris.maurer@tradingtechnologies.com)'
__version__ = '1.3'

import time

def convertOrdNum(ordNum = '00000000:00000000'):
    ordNumStrList = []
    ordNumList = list(ordNum)
    ordNumList.remove(':')
    for n in range(0, (len(ordNumList)-1), 2):
        o = n + 1
        ordNumElem = '%s%s' % (ordNumList[n], ordNumList[o])
        ordNumStrList.append(ordNumElem)
        ordNumStrList.append(':')
    ordNumStrList.__delitem__(len(ordNumStrList)-1)
    ordNumFormat = ordNumStrList.__reversed__()
    ordNumOutput = ''.join(ordNumFormat)
    return ordNumOutput

while True:
    ordNum = raw_input('\nEnter the Exchange Order Number or "q" to quit: ')
    if ordNum == 'q':
        print '\nGoodbye!'
        time.sleep(1)
        break
    elif len(ordNum) < 17:
        print 'Your input was invalid, please check the order number and try again.'
    elif len(ordNum) > 17:
        print 'Your input was invalid, please check the order number and try again.'
    elif ordNum != 'q':
        print '\nOMX style order number: '
        print convertOrdNum(ordNum)
    else:
        break