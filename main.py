__author__ = 'josh'
import getopt
import sys
from openbook import *
import error_log
from datetime import datetime, timedelta
from CLU_FIXED_VALUES import *
import os
import re
import miles

def excel_timehack(excel_date_integer):
    """ This function takes a excel date integer and will return python datetime objects"""
    try:
        year_zero = datetime(1899, 12, 30)
        dt = year_zero + timedelta(days=int(excel_date_integer))
        return dt
    except ValueError as e:
        print('got bad date passed: ', excel_date_integer)


def alw_compare(allow_obj, sp_obj):
    # compare allowance database GYH(M) to USR GYH(M)
    if allow_obj.GYH_T_Mileage_To_Nominated_Address in ('N/A', 'N', 'No'):
        pass

    elif allow_obj.GYH_T_Mileage_To_Nominated_Address != sp_obj.Perm_GYH_Mileage:
        print(bcolors.FAIL + 'found mismatch between allowance DB GYH_T :{} and USR GYH_T {}'.format
        (allow_obj.GYH_T_Mileage_To_Nominated_Address, sp_obj.Perm_GYH_Mileage) + bcolors.ENDC)

    # if division by 10 gives a remainder, the gyh(t) mileage was not rounded
    try:
        if allow_obj.GYH_T_Mileage_To_Nominated_Address % 10 != 0:
            print(bcolors.FAIL + 'incorrect rounding: {} for allowance DB GYH_T mileage'.format
            (allow_obj.GYH_T_Mileage_To_Nominated_Address) + bcolors.ENDC)
    except TypeError as e:
        pass

    if allow_obj.Live_Onboard == 'No' and sp_obj.Perm_SLA_Charged != '':
        print(bcolors.FAIL + 'does not have live onboard in ALWDB but Perm SLA is {}'.format
        (sp_obj.Perm_SLA_Charged) + bcolors.ENDC)

    if allow_obj.Live_Onboard not in ('No', 'N') and allow_obj.Live_Onboard != '' and sp_obj.Perm_SLA_Charged == '':
        print(bcolors.FAIL + 'does live onboard in ALWDB but Perm SLA is {}'.format(sp_obj.Perm_SLA_Charged)
              + bcolors.ENDC)

    if allow_obj.Live_Onboard == 'Yes':
        if sp_obj.Grade in FIX_VALUES_JUNIOR_RATES_RANKS and sp_obj.Perm_SLA_Charged != FIX_VALUES_JR[
            'Perm_SLA_Charged']:
            print(bcolors.OKBLUE + 'Perm SLA is {} should be {}'.format(sp_obj.Perm_SLA_Charged,
                                                                        FIX_VALUES_JR['Perm_SLA_Charged'])
                  + bcolors.ENDC)
        if sp_obj.Grade in FIX_VALUES_SENIOR_RATES_RANKS and sp_obj.Perm_SLA_Charged != FIX_VALUES_SR[
            'Perm_SLA_Charged']:
            print(bcolors.OKBLUE + 'Perm SLA is {} should be {}'.format(sp_obj.Perm_SLA_Charged,
                                                                        FIX_VALUES_SR['Perm_SLA_Charged'])
                  + bcolors.ENDC)
        if sp_obj.Grade in FIX_VALUES_JUNIOR_GRUNTERS_RANKS and sp_obj.Perm_SLA_Charged != FIX_VALUES_GRUNTER_JO[
            'Perm_SLA_Charged']:
            print(bcolors.OKBLUE + 'Perm SLA is {} should be {}'.format(sp_obj.Perm_SLA_Charged,
                                                                        FIX_VALUES_GRUNTER_JO['Perm_SLA_Charged'])
                  + bcolors.ENDC)
        if sp_obj.Grade in FIX_VALUES_GRUNTER_SO and sp_obj.Perm_SLA_Charged != FIX_VALUES_GRUNTER_SO[
            'Perm_SLA_Charged']:
            print(bcolors.OKBLUE + 'Perm SLA is {} should be G4Z'.format(sp_obj.Perm_SLA_Charged,
                                                                         FIX_VALUES_GRUNTER_SO['Perm_SLA_Charged'],
                                                                         + bcolors.ENDC))

    if allow_obj.Live_Onboard not in ('Y', 'N'):
        print(bcolors.FAIL + 'Live Onboard Flag MISSING or corrupt/invalid' + bcolors.ENDC)
    # print(allow_obj.__dict__)

    try:
        int(allow_obj.Annual_GYH_T_and_HDT_Documention_Check)
        doc_check_anniversary = excel_timehack(allow_obj.Annual_GYH_T_and_HDT_Documention_Check)
        today = datetime.today()
        if doc_check_anniversary < today - timedelta(days=365):
            print(bcolors.FAIL + 'OOD annual GYH/HTD check' + bcolors.ENDC)

    except ValueError:
        print(bcolors.FAIL + 'annual GYH/HTD check date not set' + bcolors.ENDC)
    if GMAPS:
        postcode_check(allow_obj, errors)


def postcode_check(allow_obj, errors):
    # pull out postcode from the allowance object, then run it through the Python Miles Module against the global postcode
    # PS is postcode pulled from GYH_T_address line in allowance object
    ps = allow_obj.Full_GYH_T_POSTCODE
    if not str(ps).upper() in ('', 'NA', 'N/A', 'N'):
        try:
            gmaps_distance = round(miles.get_mileage('PL22BG', ps), -1)  # return rounded mileage
            print(bcolors.OKGREEN + ' matched GMAPS: {} to ALLOWDB {}'.format(gmaps_distance,
                                                                              allow_obj.GYH_T_Mileage_To_Nominated_Address) + bcolors.ENDC)
            if gmaps_distance < 5:
                print(bcolors.FAIL + 'GYH Mileage Rounding FAIL' + bcolors.ENDC)
            else:
                if allow_obj.GYH_T_Mileage_To_Nominated_Address != gmaps_distance:
                    print(bcolors.FAIL + 'GMAPS mileage {} != allowance db mileage {}'.format(gmaps_distance,
                                                                                              allow_obj.GYH_T_Mileage_To_Nominated_Address) + bcolors.ENDC)
        except TypeError:  # TypeError is returned when miles.get_mileage drops out on postcode check
            pass


def usr_run(SP_object, SP_allow_db):
    __check_fixed_values__(SP_object, errors)
    __check_against_ALW__(SP_object, SP_allow_db, errors)
    __check_acting_local__(SP_object, errors)
    __check_pscat_sfa__(SP_object, errors)
    __check_against_accomp_status__(SP_object, errors)
    __check_gyh_rounding__(SP_object, errors)
    if WARRANTS:
        __get_warrants__(SP_object)


def __check_gyh_rounding__(SP_object, errors):
    try:
        if SP_object.Perm_GYH_Mileage % 10 != 0:
            print(bcolors.FAIL + 'incorrect rounding: {} for USR GYH_T mileage'.format
            (SP_object.Perm_GYH_Mileage) + bcolors.ENDC)
    except TypeError:
        # non integer entries, whitespace and blank values will not work with %
        pass


def __check_against_accomp_status__(SP_object, errors):
    if SP_object.Perm_GYH_Mileage != '' and SP_object.Perm_Accomp_Status not in ('US, VS'):
        print(bcolors.OKBLUE + 'SP {} {} gets GYH T - possibly wrong Accompanied Status {}'.format(SP_object.whois,
                                                                                                   SP_object.Assignment_Number,
                                                                                                   SP_object.Perm_Accomp_Status) + bcolors.ENDC)

    if SP_object.SFA_Occupied != '' and SP_object.Perm_Accomp_Status not in ('A'):
        print(bcolors.OKBLUE + 'SP {} {} has SFA charge - possibly wrong Accompanied Status {}'.format(SP_object.whois,
                                                                                                       SP_object.Assignment_Number,
                                                                                                       SP_object.Perm_Accomp_Status) + bcolors.ENDC)


def __check_pscat_sfa__(SP_object, errors):
    if SP_object.SFA_Occupied != '' and SP_object.Marital_Status in ('Category 5', 'Category 4', 'Category 3'):
        print(bcolors.OKBLUE + 'SP {} {} is PS Cat {} and has MQ Charges'.format(SP_object.whois,
                                                                                 SP_object.Assignment_Number,
                                                                                 SP_object.Marital_Status) + bcolors.ENDC)

    if SP_object.SFA_Occupied != '' and SP_object.Perm_GYH_Mileage != '':
        print(bcolors.OKBLUE + 'SP {} {} gets GYH T and occupies SFA?'.format(SP_object.whois,
                                                                              SP_object.Assignment_Number) + bcolors.ENDC)


def __check_acting_local__(SP_object, errors):
    if SP_object.Acting_Paid_Rank != '':
        print(bcolors.OKBLUE + 'SP {} {} is Acting Local {} and should be in Supervisors Log'.format(SP_object.whois,
                                                                                                     SP_object.Assignment_Number,
                                                                                                     SP_object.Acting_Paid_Rank) + bcolors.ENDC)


def __check_fixed_values__(SP_object, errors):
    SP_object_dict = SP_object.__dict__
    if SP_object.whois == ('TRIUMPH', 'OFFICER OF THE DAY|1560669'):
        pass
    else:

        if SP_object.Temp_Allowance_Location in ('ASSLQU', 'INTRANSIT', 'GBR'):
            print(bcolors.OKBLUE + '--- ASSESS {} {} should be in the LANDED LOG'.format
            (SP_object.whois, SP_object.Assignment_Number) + bcolors.ENDC)
            # allow for multiple organisations with Hasler.

        if SP_object.Organization not in FIX_VALUES_ORGANISATIONS:
            print(bcolors.OKBLUE + 'Organisation for Service Person: ', SP_object.whois, 'is: ',
                  SP_object.Organization, 'should be one of: ', str(FIX_VALUES_ORGANISATIONS) + bcolors.ENDC)

        for key in SP_object_dict:

            # determine the correct map to use
            # Fixed values imported from CLU_FIXED_VALUES for ease of reading/modication
            if SP_object.Grade in FIX_VALUES_JUNIOR_RATES_RANKS:

                if key in ('Perm_SLA_Charged', 'Perm_SLA_Occupied'):
                    pass

                elif key in FIX_VALUES_JR and SP_object_dict[key] != FIX_VALUES_JR[key]:
                    print(bcolors.OKBLUE + key, ' for Service Person: ', SP_object.whois, 'is: ',
                          SP_object_dict[key], 'should be: ', FIX_VALUES_JR[key] + bcolors.ENDC)

            elif SP_object.Grade in FIX_VALUES_SENIOR_RATES_RANKS:

                if key in ('Perm_SLA_Charged', 'Perm_SLA_Occupied'):
                    pass

                elif key in FIX_VALUES_SR:
                    if SP_object_dict[key] != FIX_VALUES_SR[key]:
                        print(bcolors.OKBLUE, key, ' for Service Person: ', SP_object.whois, 'is: ',
                              SP_object_dict[key], 'should be: ', FIX_VALUES_SR[key] + bcolors.ENDC)

            elif SP_object.Grade in FIX_VALUES_JUNIOR_GRUNTERS_RANKS:

                if key in ('Perm_SLA_Charged', 'Perm_SLA_Occupied'):
                    pass
                elif key in FIX_VALUES_GRUNTER_JO:
                    if SP_object_dict[key] != FIX_VALUES_GRUNTER_JO[key]:
                        print(bcolors.OKBLUE + key, ' for Service Person: ', SP_object.whois, 'is: ',
                              SP_object_dict[key], 'should be: ', FIX_VALUES_GRUNTER_JO[key] + bcolors.ENDC)
            else:

                if key in ('Perm_SLA_Charged', 'Perm_SLA_Occupied'):
                    pass

                elif key in FIX_VALUES_GRUNTER_SO:
                    if SP_object_dict[key] != FIX_VALUES_GRUNTER_SO[key]:
                        print(bcolors.OKBLUE + key, ' for Service Person: ', SP_object.whois, 'is: ',
                              SP_object_dict[key], 'should be: ', FIX_VALUES_GRUNTER_SO[key] + bcolors.ENDC)


def __get_warrants__(sp_object):
    leave_year_end = datetime(2017, 4, 1)
    # CATCH errors for non_fav dates (stub accounts etc)
    try:
        int_time = int(sp_object.FAV_Date)
    except ValueError:
        print('no FAD date found for {}'.format(sp_object.whois))

    # stupid excel date integer formats run from 01-01-1900
    year_zero = datetime(1899, 12, 30)
    warrants = 0

    # if end of year, we for the twelve month period (leave year end - 1 year, and one period of 36 days
    if END_OF_YEAR:
        running_time = leave_year_end - timedelta(days=366) + timedelta(days=36)
    # for new joiners, we need to go from the start of entitlement.  This should really be SP.startdate
    else:
        running_time = datetime.today() + timedelta(days=36)
    # test if inttime got set.
    try:
        int_time
        fav_date = year_zero + timedelta(days=int_time)

        while running_time < leave_year_end and running_time < fav_date:
            warrants += 1
            running_time += timedelta(days=36)

    except NameError:
        pass

    if END_OF_YEAR == 1:
        print('has {} warrants to leave year ending {}'.format(warrants, leave_year_end))
    else:
        print('has {} warrants to from today'.format(warrants, leave_year_end))


def __check_against_ALW__(SP_object, SP_allow_db, errors):
    '''
    :param SP_object: service person object
    :return: process of errors against the AP database object
    '''
    # we get one SP at a time, but all the allowance database.  We need to match just one of the allowance database
    # lines for each SP
    caught_flag = 0
    if SP_object.whois == ('TRIUMPH', 'OFFICER OF THE DAY|1560669'):
        pass
    else:
        # loop through the whole SP_allow_db to match a record by service number with the single SP object
        for x in range(len(SP_allow_db)):
            # cut to 8 chars to allow for -2 service numbers
            if str(SP_allow_db[x].Service_No)[:8] == str(SP_object.Assignment_Number)[:8]:
                print('Matched {} to {} in allowance DB'.format(SP_allow_db[x].Service_No, SP_object.Assignment_Number))
                caught_flag = 1
                # if we have a match we can pass the single SP_allow object, and SP object and error recorded to
                # The ALW_interpreter fuction to do the error checking.
                alw_compare(SP_allow_db[x], SP_object)

        if caught_flag == 0:
            caught_error = 'ERROR: cannot match ' + str(SP_object.whois) + 'to allowance database entry!'
            errors.held_errors(caught_error)

def main():
    # create an error log object passed to each function for recording errors

    f_found_files = []
    for root, dirs, files in os.walk('test-data'):

        #  the below uses consistant naming traits through re.search to pull out files of different types from
        # the folder test-data and assign the file path to f_***

        for file in files:
            # f_tasbat = re.search('TASBAT', file)
            f_usr = re.search('-Unit Status Report', file)
            f_allowdb = re.search('Allowance_Database', file)
            # to do f_landedlog

            if f_usr and os.path.isfile('test-data/' + f_usr.string) and 'usr' not in f_found_files:
                print(bcolors.OKGREEN + 'USR found file: {}, executing'.format(f_usr.string) + bcolors.ENDC)
                SP_object_list = openbook('test-data/' + f_usr.string, sheet_type='USR')
                f_found_files.append('usr')

            if f_allowdb and os.path.isfile('test-data/' + f_allowdb.string) and 'alw' not in f_found_files:
                print(bcolors.OKGREEN + 'Allowance DB found file: {}, executing'.format(
                    f_allowdb.string) + bcolors.ENDC)
                SP_allow_db = openbook('test-data/' + f_allowdb.string, sheet_type='ALW')
                f_found_files.append('alw')

    # no crash on missing test-data
    if len(f_found_files) == 0:
        errors.held_errors('NO DATA FOUND TO PROCESS')
        sys.exit(errors.dump_held_errors())

        # main loop through each person object generated from the USR.  Missing out persons without assignment number.
        # SP_object_list would be undefined if we didn't have sys.exit() on len(found_files) above, and no data was found

    for x in range(len(SP_object_list)):
        if SP_object_list[x].Assignment_Number != '':
            print(bcolors.BOLD + '\nIDENTIFIED ANOMOLIES FOR SP {} {}'.format(SP_object_list[x].whois,
                                                                              str(SP_object_list[
                                                                                      x].Assignment_Number)[
                                                                              :8]) + bcolors.ENDC)
            # the main call for the USR to check the current object
            usr_run(SP_object_list[x], SP_allow_db)

        else:
            errors.held_errors('SP: ' + SP_object_list[x].whois[0] + ' ' + SP_object_list[x].whois[1] +
                               ' is a unarrived entity')
    #drop global collected errors
    errors.dump_held_errors()

    # pointless .py code line counter
    clu_lines = 0
    for root, dirs, files in os.walk('./'):
        for i in files:
            pyfile = re.search('.py$', i)
            try:
                with open(pyfile.string) as f:
                    clu_lines += len(f.readlines())
                    f.close()
            except (TypeError, AttributeError):
                pass

    print('CLU is now {} lines of code'.format(clu_lines))
    print(len(f_found_files))

if __name__ == '__main__':
    # default to use gmaps where no --nogmaps is given gmaps=True
    # define global switches for gmaps use, warrants.
    GMAPS = True
    WARRANTS = False
    END_OF_YEAR = False
    errors = error_log.held_errors()
    try:
        opts, args = getopt.getopt(sys.argv[1:],'-h', ['nogmaps', 'warrants', 'endyear'])
        for o, a in opts:
            if o == '--nogmaps':
                GMAPS = False
            if o == '--warrants':
                WARRANTS = True
            if o == '--endyear':
                END_OF_YEAR = True
            if o == '-h':
                print(' OPTIONS ARE\n --warrants (calculate warrant entitlement) --nogmaps (do not use gmaps)')
                sys.exit()
        main()
    except getopt.GetoptError:
        print(' OPTIONS ARE\n --warrants (calculate warrant entitlement) --nogmaps (do not use gmaps)')