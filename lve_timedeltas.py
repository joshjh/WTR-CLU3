__author__ = 'josh'

import datetime
import openbook


SP_Lve_records = openbook.openbook('test-data/Absence-Details.xls', sheet_type='LVE')

class LR:
    def __init__(self, whois):
        self.whois = whois
        self.LEAVE_VAL = []

    def add_vals(self, Fromdate, Todate):
        self.LEAVE_VAL.append(Fromdate)
        self.LEAVE_VAL.append(Todate)

# controlled by list of processed LRs.  Name of LRs that are processed append to processed_records to not repeat
lrs = []
processed_records = []
output = []
for x in SP_Lve_records:

    # identifier from the record loaded first
    this_record = x.whois

    # see if we did the record already, if not, create the object, then look through the entire SP_Lve_Records list
    # appending the leave dates that relate to the record we have selected.
    if this_record not in processed_records:
        processed_records.append(this_record)
        new_records_object = LR(this_record)
        for y in SP_Lve_records:
            if new_records_object.whois == y.whois:
                new_records_object.add_vals(y.Actual_Date_From, y.Actual_Date_To)

        # finally append the processed records to the final list of LR objects.
        lrs.append(new_records_object)

    else:
        pass

# process the list of LR objects, completing the TimeDelta Calculations
for lr in lrs:
    #stupid excel dates hack
    year_zero = datetime.datetime(1899, 12, 30)
    # this line selects when we are going to start the block modification.
    mod_startdate = datetime.datetime(2015, 8, 1)
    # the number of days needs to run up for the length of each record
    running_days = 0
    # process entries in pairs.  Start of leave and finish.  Range increments in two, always selecting the start
    # date, then the next value which will be the leave date.
    for x in range(0, len(lr.LEAVE_VAL), 2):
        #
        int_start_time = lr.LEAVE_VAL[x]
        int_stop_time = lr.LEAVE_VAL[x+1]
        # put the excel dates into a useful format for timedelta
        startdate_date = year_zero + datetime.timedelta(days=int_start_time)
        stopdate_date = year_zero + datetime.timedelta(days=int_stop_time)
        # subtract the startdate from the stopdate gives the timedelta(days) difference.
        delta = stopdate_date - startdate_date
        # add it to the running total, then repeat until the end of the lr.LEAVE_VAL list.
        running_days += delta.days
        # Append the  record to output for printing.
    output.append((lr.whois, mod_startdate, mod_startdate + datetime.timedelta(days=running_days), running_days))

output = sorted(output)
for x in output:
    print('record for ', x[0][:], ' stop here: ', x[1], 'start here ', x[2], ' totals ', x[3], 'days')

print ('total processed record {}'.format(len(output)))
