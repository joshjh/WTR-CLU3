__author__ = 'josh'
""" Opens a excel workbook and indexes the respective rows """

import xlrd
import datetime
import sys

class SP:
     def __init__(self, last_name, position):
         self.whois = (last_name, position)

     def setvalues(self, values):
         for attr in values:
             setattr(self, attr, values[attr])

class AP:
     def __init__(self, NAME, Service_No):
         self.whois = (NAME, Service_No)

     def setvalues(self, values):
         for attr in values:
             setattr(self, attr, values[attr])

def openbook(workbook, sheet_type='USR'):
    """
    opens the workbook and creates class SP.  Returns SP with all attributes for each line in the Excel Sheet
    """
    try:

        openedbook = xlrd.open_workbook(workbook)
        if sheet_type == 'USR':
            sheet = openedbook.sheet_by_name('Full USR')
        elif sheet_type == 'ALW':
            sheet = openedbook.sheet_by_name('HASLER STAFF')
            sheet2= openedbook.sheet_by_name('MA7 Allowance')
        elif sheet_type == 'LVE':
            sheet = openedbook.sheet_by_name('Absence Details')
            header = sheet.row_values(4)
        elif sheet_type == 'APR':
            sheet = openedbook.sheet_by_name('2015')
        elif sheet_type == 'MT':
            sheet = openedbook.sheet_by_name('Departures 2015')
            header = sheet.row_values(1)
        elif sheet_type == 'OBIEE_GYH_T':
            sheet = openedbook.sheet_by_name('Sheet1')
            header = sheet.row_values(2)
        elif sheet_type == 'TASBAT':
            sheet = openedbook.sheet_by_name('G46')
            header = sheet.row_values(0)
        elif sheet_type == 'TDS':
            sheet = openedbook.sheet_by_name('TDTS Spreadsheet 2016-17')
            header = sheet.row_values(0)
        # if header was not defined above, we will set it to the top line (0)
    except xlrd.XLRDError:
        quitstring = 'BAD/CORRUPTED FILE {}, OR FILE OPENED IN EDITOR WHILST PARSING TYPE {}'.format(workbook, sheet_type)
        #bugout - unrecoverable
        sys.exit('CONTROLLED STOP. :: ' + quitstring)
    try:
        header

    except NameError:
        header = sheet.row_values(0)

    for index in range(len(header)):

        if sheet_type in ('ALW', 'TASBAT'):
            header[index] = header[index].replace(' ', '_')
            header[index] = header[index].replace('(', '_')
            header[index] = header[index].replace(')', '_')
            header[index] = header[index].replace('__', '_')
            # print (header[index])

        else:
            header[index] = header[index].replace(' ', '_')

    unit = []
    if sheet_type == 'USR':
        for x in range(1, sheet.nrows):
            sp_dictionary = dict(zip(header, sheet.row_values(x)))
            SP_object = SP(sp_dictionary['Last_Name'], sp_dictionary['Position'])
            SP_object.setvalues(sp_dictionary)
            unit.append(SP_object)

            # now we have multiple tabs in the allowance db so this will need to be re-written.
    elif sheet_type == 'ALW':
        for x in range(1, sheet.nrows):
            al_dictionary = dict(zip(header, sheet.row_values(x)))
            AL_object = SP(al_dictionary['NAME'], al_dictionary['Service_No'])
            AL_object.setvalues(al_dictionary)
            unit.append(AL_object)
        for x in range(1, sheet2.nrows):
            al_dictionary = dict(zip(header, sheet2.row_values(x)))
            AL_object = SP(al_dictionary['NAME'], al_dictionary['Service_No'])
            AL_object.setvalues(al_dictionary)
            unit.append(AL_object)

    elif sheet_type == 'LVE':
        for x in range(5, sheet.nrows):
            lve_dictionary = dict(zip(header, sheet.row_values(x)))
            lve_object = SP(lve_dictionary['Full_Name'], lve_dictionary['Employee_Number'])
            lve_object.setvalues(lve_dictionary)
            unit.append(lve_object)

    elif sheet_type == 'APR':
        for x in range(1, sheet.nrows):
            apr_dictionary = dict(zip(header, sheet.row_values(x)))
            apr_object = SP(apr_dictionary['Name'], apr_dictionary['Service_Number'])
            apr_object.setvalues(apr_dictionary)
            unit.append(apr_object)

    elif sheet_type == 'MT':
        for x in range(2, sheet.nrows):
            mt_dictionary = dict(zip(header, sheet.row_values(x)))
            mt_dictionary['Rank'] = sheet.cell_value(x,0)
            mt_object = SP(mt_dictionary['Name'], mt_dictionary['Service_No'])
            mt_object.setvalues(mt_dictionary)
            unit.append(mt_object)

    elif sheet_type == 'OBIEE_GYH_T':
        for x in range(3, sheet.nrows):
            gyh_t_dictionary = dict(zip(header, sheet.row_values(x)))
            gyh_t_object = SP(gyh_t_dictionary['Surname'], gyh_t_dictionary['Service_Number'])
            gyh_t_object.setvalues(gyh_t_dictionary)
            unit.append(gyh_t_object)

    elif sheet_type == 'TASBAT':
        for x in range(1, sheet.nrows):
            tasbat_dictionary = dict(zip(header, sheet.row_values(x)))
            tasbat_object = SP(tasbat_dictionary['Misc_Ref_or_JPA_Claim_Number'], tasbat_dictionary['FullName'])
            tasbat_object.setvalues(tasbat_dictionary)
            #this is a bit naughty.
            tasbat_object.__setattr__('lineno', x+1)
            unit.append(tasbat_object)

    return unit

# maybe depricated, keeping for now, might be useful
def fix_date(ex_date):
    # ex_date is the integer stupid excel date
    year_zero = datetime.date(1899, 12, 30)
    # put the excel dates into a useful format for timedelta
    useful_date = year_zero + datetime.timedelta(days=ex_date)
    return useful_date

