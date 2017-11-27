# Filename: pcrCounts.py

'''Provide a wiki-markup formatted summary of 7.17.30 PCR counts.'''

__author__ = 'Chris Maurer (chris.maurer@tradingtechnologies.com)'
__version__ = '1.0'

import subprocess

'''Get name of MKS Query from user and write it to temp file (create temp file if necessary)'''

filename = r'C:\temp\pcrCounts.ini'
try:
    f = file(filename, 'r')
    hist = f.readline()
    f.close()
except:
    pass
    hist = None
askQuery = raw_input('Please enter the MKS query Name [%s] : ' % (hist))
if len(askQuery) > 0:
    f = file(filename, 'w')
    f.write(askQuery)
    f.close()

query = hist if len(askQuery) == 0 else askQuery

'''Get MKS Query data'''
pcrsCmd = 'im issues --fields=\"Summary,RQ_Contained By,ID,Feature,Description,RQ_Text,State,RQ_Category,RQ_Contains\" --fieldsDelim=";;" --query=\"%s\"' % (query)
stateCmd = 'im issues --fields=\"State\" --fieldsDelim=";;" --query=\"%s\"' % (query)
pcr_typeCmd = 'im issues --fields=\"Type\" --fieldsDelim=";;" --query=\"%s\"' % (query)

mksCols = ['Summary', 'Contained By', 'ID', 'Feature', 'Description', 'Text', 'State', 'Category', 'Contains']
fields = ['Summary', 'RQ_Contained By', 'ID', 'Feature', 'Description', 'RQ_Text', 'State', 'RQ_Category', 'RQ_Contains']
mksStates = ['Active','Analysis','Clarification','Closed','Closed - Duplicate','Closed - Rejected','Code Review','Deferred','DevBlocked','DevHold','Draft','Duplicate','Feature Complete','Fixed','New','Not Fixed','Open','Planning','Rejected','Released','Retired','Revised','SI Change Package','Submitted','Target','TestBlocked','Tested','Working']
fieldsStr = ','.join(fields)

'''Create lists of MKS Data to be consumed by user'''
pcrs = subprocess.Popen(pcrsCmd, stdout=subprocess.PIPE).communicate()
pcrDoc = str(pcrs)
pcrList = pcrDoc.split(';;')

pcrStates = subprocess.Popen(stateCmd, stdout=subprocess.PIPE).communicate()
stateDoc = str(pcrStates)
stateList = stateDoc.split('\\n')

pcrTypes = subprocess.Popen(pcr_typeCmd, stdout=subprocess.PIPE).communicate()
pcr_typeDoc = str(pcrTypes)
#pcr_typeList = pcr_typeDoc.split('\\n')

'''Initialise counters'''
ctNew, ctTblk, ctTest, ctClsd, ctRej, ctDup, ctSub, ctNoFix, ctFix, ctWrk, ctClar, ctDef, ctEnh, ctTest, ctTc = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0

'''Create Output'''
for state in stateList:
    if 'Submitted' in state: ctSub += 1
    if 'New' in state: ctNew += 1
    if 'Working' in state: ctWrk += 1
    if 'Fixed' in state and 'Not Fixed' not in state: ctFix += 1
    if 'Not Fixed' in state: ctNoFix += 1
    if 'Tested' in state: ctTest += 1
    if 'TestBlocked' in state: ctTblk += 1
    if 'Clarification' in state: ctClar += 1
    if 'Closed' in state: ctClsd += 1
    if 'Duplicate' in state: ctDup += 1
    if 'Rejected' in state: ctRej += 1

#for pcr_type in pcr_typeList:
#    if 'DEF' in pcr_type: ctDef += 1
#    if 'ENH' in pcr_type: ctEnh += 1
#    if 'TEST' in pcr_type: ctTest += 1
#    if 'TESTCASE' in pcr_type: ctTc += 1

print '\n\nMKS Query = %s' % (query)
print ''.center(70, '-')
print '\n     Total Number of Items in Scope: ' + str((len(pcrList)/8))

print 'Submitted = %s' % (ctSub)
print 'New = %s' % (ctNew)
print 'Working = %s' % (ctWrk)
print 'Fixed = %s' % (ctFix)
print 'Not Fixed = %s' % (ctNoFix)
print 'Tested = %s' % (ctTest)
print 'TestBlocked = %s' % (ctTblk)
print 'Clarification = %s' % (ctClar)
print 'Closed = %s' % (ctClsd)
print 'Duplicate = %s' % (ctDup)
print 'Rejected = %s' % (ctRej)
print '\n' + ''.center(70, '-')
print '\n     PCR Type Summary:'
print 'DEF = %s' % (ctDef)
print 'ENH = %s' % (ctEnh)
print 'TEST = %s' % (ctTest)
print 'TESTCASE = %s' % (ctTc)
print '\n' + ''.center(70, '-')
print '\n     For Copy-Pasting into Test Summary \"PCR Counts\":'
print '\n     (sequence = Closed, Tested, TestBlocked, Fixed, Not Fixed,\
       \n     New, Working, Rej/Dup, Total)'
print ctClsd
print ctTest
print ctTblk
print ctFix
print ctNoFix
print ctNew
print ctWrk
print ctRej + ctDup
print len(pcrList)/8
print '\n' + ''.center(70, '-')

print '\n     For Confluence Charting:'
chartList = ['PCRs', str(ctNew), str(ctWrk), str(ctFix), str(ctNoFix), str(ctTest), str(ctTblk), str(ctClar), str(ctClsd), str(ctDup), str(ctRej), str(ctSub)]
chartOutput = '|| ' + ' | '.join(chartList) + ' | '
print '| {chart:title=' + (query.split(' '))[0] + '|subTitle=Total = ' + str((len(pcrList)/8)) + '}'
print '|| PCR State || New || Working || Fixed || Not Fixed || Tested || TestBlocked || Clarification || Closed || Duplicate || Rejected || Submitted ||'
print chartOutput + '\n{chart} |'
raw_input('\nPress ENTER to continue...')