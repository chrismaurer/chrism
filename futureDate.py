import time, calendar, datetime
current_year = time.localtime()[0]
#
'''Prints the last business day of each month'''

google_format = True

if google_format:
    print "Subject,Start Date,All Day Event"

last_business_days = []

for month in range(1,13):

   last_date_of_month = calendar.monthrange(current_year, month)[1]
   last_day_of_month_datestamp = datetime.date(current_year, month, last_date_of_month)
   last_weekday_of_month = datetime.date.weekday(last_day_of_month_datestamp)

   # if last weekday of month is Sat or Sun
   if last_weekday_of_month in range(5,7):
       # get sum of 4 (Fri) minus last weekday of month int (i.e. -1 or -2)
       last_date_of_month = last_date_of_month + (4 - last_weekday_of_month)
       last_day_of_month_datestamp = datetime.date(current_year, month, last_date_of_month)

   last_business_day_of_month = '/'.join([str(last_day_of_month_datestamp).split('-')[1],
                                          str(last_day_of_month_datestamp).split('-')[2],
                                          str(last_day_of_month_datestamp).split('-')[0]])
   last_business_days.append(last_business_day_of_month)

if not google_format:
    print '-'*10
    print 'Last'
    print 'Business'
    print 'Day of'
    print 'Each Month'
    print '-'*10
for last_business_day in last_business_days:
    if google_format:
        print "HKEx Maintenance," + last_business_day + ",True"
    else:
        print last_business_day


# '''Prints the first and third Friday of each month'''
#
# current_year = time.localtime()[0]
# first_and_third_fridays = []
#
# for month in range(1,13):
#
# #    last_date_of_month = calendar.monthrange(current_year, month)[1]
#    first_day_of_month_datestamp = datetime.date(current_year, month, 1)
#    first_weekday_of_month = datetime.date.weekday(first_day_of_month_datestamp)
#
#    if first_weekday_of_month == 4:
#        friday1 = first_day_of_month_datestamp
#        friday2 = friday1 + datetime.timedelta(14)
#    elif first_weekday_of_month > 4:
#        friday1 = first_day_of_month_datestamp - datetime.timedelta(first_weekday_of_month - 4)
#        if datetime.date.timetuple(friday1)[1] < month:
#            friday1 = friday1 + datetime.timedelta(7)
#        friday2 = friday1 + datetime.timedelta(14)
#    elif first_weekday_of_month < 4:
#        friday1 = first_day_of_month_datestamp + datetime.timedelta(4 - first_weekday_of_month)
#        friday2 = friday1 + datetime.timedelta(14)
#
#    for friday_date in [friday1, friday2]:
#        datestamp = '/'.join([str(friday_date).split('-')[1],
#                              str(friday_date).split('-')[2],
#                              str(friday_date).split('-')[0]])
#
#        first_and_third_fridays.append(datestamp)
#
# if not google_format:
#     print '-'*10
#     print 'First'
#     print 'and Third'
#     print 'Friday of'
#     print 'Each Month'
#     print '-'*10
# for first_and_third_friday in first_and_third_fridays:
#     if google_format:
#         print "TOCOM Maintenance," + first_and_third_friday + ",True"
#     else:
#         print first_and_third_friday

'''Prints the second Friday of each month'''

current_year = time.localtime()[0]
second_fridays = []

for month in range(1,13):

#    last_date_of_month = calendar.monthrange(current_year, month)[1]
    first_day_of_month_datestamp = datetime.date(current_year, month, 1)
    first_weekday_of_month = datetime.date.weekday(first_day_of_month_datestamp)

    if first_weekday_of_month == 4:
        friday1 = first_day_of_month_datestamp + datetime.timedelta(14)
    elif first_weekday_of_month > 4:
        friday1 = first_day_of_month_datestamp - datetime.timedelta(first_weekday_of_month - 4)
        if datetime.date.timetuple(friday1)[1] < month:
            friday1 = friday1 + datetime.timedelta(7)
        friday1 = friday1 + datetime.timedelta(7)
    elif first_weekday_of_month < 4:
        friday1 = first_day_of_month_datestamp + datetime.timedelta(4 - first_weekday_of_month)
        friday1 = friday1 + datetime.timedelta(7)


    datestamp = '/'.join([str(friday1).split('-')[1],
                          str(friday1).split('-')[2],
                          str(friday1).split('-')[0]])

    second_fridays.append(datestamp)

if not google_format:
    print '-'*10
    print 'Second'
    print 'Friday of'
    print 'Each Month'
    print '-'*10
for second_friday in second_fridays:
    if google_format:
        print "TFX Maintenance," + second_friday + ",True"
    else:
        print second_friday