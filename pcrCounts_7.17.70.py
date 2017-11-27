# Filename: pcrCounts.py

'''Provide a quick summary of PCR counts in any Query.'''

__author__ = 'Chris Maurer (chris.maurer@tradingtechnologies.com)'
__version__ = '1.0'

import subprocess, time

datestring = '/'.join([str(time.localtime()[0]), str(time.localtime()[1]), str(time.localtime()[2]+4-time.localtime()[6]).zfill(2)])
barchart_list = []
barchart_list.append(datestring)

list_of_queries = ['TFX Gateway 7.17.70 - Scope',
                   'OSE Gateway 7.17.70 - Scope',
                   'TOCOM Gateway 7.17.70 - Scope',
                   'SGX Gateway 7.17.70 - Scope',
                   'HKEx 7.17.70 - Scope']

for query in list_of_queries:

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
    
    chartList = ['PCRs', str(ctNew), str(ctWrk), str(ctFix), str(ctNoFix), str(ctTest), str(ctTblk), str(ctClar), str(ctClsd), str(ctDup), str(ctRej), str(ctSub)]
    chartOutput = '|| ' + ' | '.join(chartList) + ' | '
    print '| {chart:title=' + (query.split(' '))[0] + '|subTitle=Total = ' + str((len(pcrList)/8)) + '}'
    print '|| PCR State || New || Working || Fixed || Not Fixed || Tested || TestBlocked || Clarification || Closed || Duplicate || Rejected || Submitted ||'
    print chartOutput + '\n{chart} '
    barchart_list.append(str((len(pcrList)/8)))
    barchart_list.append(str(ctFix))

'''Print Bar Chart'''
print '\n\\\\'
print '{chart:type=bar|dateFormat=MM.DD.yyyy|timePeriod=Week| dataOrientation=vertical|rangeAxisLowerBound=0|xLabel=Week Ending|yLabel=Number of PCRs|rangeAxisTickUnit=2|width=840} '
print '|| Week Ending || TFX Total || TFX Fixed || OSE Total || OSE Fixed || TOCOM Total || TOCOM Fixed || SGX Total || SGX Fixed || HKEx Total || HKEx Fixed ||'
print '| ' + ' | '.join(barchart_list) + ' |' + '\n{chart}' 