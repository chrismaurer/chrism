#~Filename: getListOfJP-MaintDates.py

#import time
#
#startingDateInSecs = 1325203200 #starting date = 30-Dec-2011
#
#def printTFXDateList():
#    # creates a list of dates representing the 2nd Friday of each month, starting from 30-Dec-2011.
#    print 'TFX Maintenance Dates:'
#    dateInSecs = startingDateInSecs
#    while True:
##        '''Skip ahead 7 days'''
##        if time.gmtime(dateInSecs)[2] > 21: dateInSecs += 604800
#        '''Skip ahead 14 days'''
#        if time.gmtime(dateInSecs)[2] > 21: dateInSecs += 1209600
#        '''if dateInSecs tuple 'tm_mday' < 7: skip ahead 7 days'''
#        if time.gmtime(dateInSecs)[2] < 8: dateInSecs += 604800
#        '''if dateInSecs tuple 'tm_year' > current year: break'''
#        if time.gmtime(dateInSecs)[0] > time.gmtime()[0]: break
#        timeList=(str(time.gmtime(dateInSecs)[1]).zfill(02),\
#                  str(time.gmtime(dateInSecs)[2]).zfill(02),\
#                  str(time.gmtime(dateInSecs)[0]))
#        print '/'.join(timeList)
#        '''Skip ahead 14 days'''
#        dateInSecs+=1209600
#        '''Skip ahead 28 days'''
##        dateInSecs+=2419200
#
#def printTOCOMDateList():
#    # creates a list of dates representing the 1st and 3rd Friday of each month, starting from 30-Dec-2011.
#    print '\nTOCOM Maintenance Dates:'
#    dateInSecs = startingDateInSecs + 604800
#    while True:
##        '''Skip ahead 7 days'''
##        if time.gmtime(dateInSecs)[2] > 25: dateInSecs += 604800
##        '''Skip ahead 14 days'''
##        if time.gmtime(dateInSecs)[2] > 21: dateInSecs += 1209600
##        '''if dateInSecs tuple 'tm_mday' < 7: skip ahead 7 days'''
##        if time.gmtime(dateInSecs)[2] < 5: dateInSecs += 604800
##        '''if dateInSecs tuple 'tm_year' > current year: break'''
#        if time.gmtime(dateInSecs)[0] > time.gmtime()[0]: break
#        timeList=(str(time.gmtime(dateInSecs)[1]).zfill(02),\
#                  str(time.gmtime(dateInSecs)[2]).zfill(02),\
#                  str(time.gmtime(dateInSecs)[0]))
#        print '/'.join(timeList)
#        '''Skip ahead 14 days'''
#        dateInSecs+=1209600
#        if time.gmtime(dateInSecs)[0] > time.gmtime()[0]: break
#        timeList=(str(time.gmtime(dateInSecs)[1]).zfill(02),\
#                  str(time.gmtime(dateInSecs)[2]).zfill(02),\
#                  str(time.gmtime(dateInSecs)[0]))
##        '''Skip ahead 28 days'''
##        dateInSecs+=2419200
#        '''Skip ahead 7 days'''
#        if time.gmtime(dateInSecs)[2] > 26: dateInSecs += 604800
#
#printTFXDateList()
#printTOCOMDateList()


#
#def addDays(dateInSecs, numDays):
#    dateInSecs = dateInSecs + (86400 + numDays)
#    return dateInSecs
#
#while True:
#    dateInSecs = 1325289600
#    startingTime = raw_input\
#    ('\nStarting time is %s.\nEnter number of days to skip ahead (for \'none,\' enter 0, or to quit, enter \'q\'): ' %\
#     time.asctime((time.gmtime(dateInSecs))))
#    if startingTime == 'q':
#        print '\nGoodbye!'
#        time.sleep(1)
#        break
#    elif startingTime != '0':
#        while True:
#            yesNo = raw_input\
#            ('\nStarting time is now %s. Accept? (y/n/q): ' %\
#             time.asctime((time.gmtime(dateInSecs))))
#            if yesNo == 'q':
#                print '\nGoodbye!'
#                time.sleep(1)
#                break
#            elif yesNo == 'y':
#                dateInSecs = addDays(dateInSecs, startingTime)
#    else:
#        output = exchIDLookup(startingTime)
#        if output == None:
#            print '\n%s was not found. Please try again.' % (startingTime)
#        else:
#            outputList = output.split('"')
#            print '\nThe exchange ID for %s is %s ' % (startingTime, outputList[1])


import datetime                                                                 
from datetime import timedelta                                                  
origDate = datetime.date(2014,2,7)                                              
oneday = timedelta(days=1)                                                      
FRIDAY = 4                                                                   
nextMonth = (origDate.month % 12) + 1                                           
newDate = datetime.date(origDate.year, nextMonth, 8)                            
while newDate.weekday() != FRIDAY:                                           
    newDate += oneday                                                           
print newDate