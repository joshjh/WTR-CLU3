__author__ = 'josh'

import os
import re
import openbook
from CLU_FIXED_VALUES import bcolors



def load_tasbat():
    for root, dirs, files in os.walk('test-data'):
        f_found_files = []
        tasbats_to_process = []
        for file in files:
            f_tasbat = re.search('TASBAT', file)

            if f_tasbat and os.path.isfile('test-data/' + f_tasbat.string):
                print(bcolors.OKGREEN + 'TASBAT found file: {}, executing'.format(f_tasbat.string) + bcolors.ENDC)
                tasbats_to_process.append(openbook.openbook('test-data/' + f_tasbat.string, sheet_type='TASBAT'))
                # return a list of TASBAT objects
                return tasbats_to_process

def load_t_s_sheet():
    for root, dirs, files in os.walk('test-data'):
        f_found_files = []
        tds_to_process = []
        for file in files:
            f_tds = re.search('TDTS', file)

            if f_tds and os.path.isfile('test-data/' + f_tds.string):
                print(bcolors.OKGREEN + 'TASBAT found file: {}, executing'.format(f_tds.string) + bcolors.ENDC)
                tds_to_process.append(openbook.openbook('test-data/'+f_tds.string, sheet_type='TDS'))
                # return a list of TASBAT objects
                return tds_to_process

def strip_tasbats(tasbats_to_process):
    UIN = 'N7406A'
    ADMIT_SOURCES = 'GPC-DTMA-AIR', 'GPC-DTMA-AIR-RBS', 'GPC-DTMA-HOTELBOOKINGS', 'GPC-DTMA-HOTELCHARGES', \
                    'GPC-DTMA-RAIL','HIRE CAR', 'JPA'
    n7406_tasbats = []

    print('got tasbats to: ', len(tasbats_to_process))

    print(len(tasbats_to_process[0]))

    for x in range(0, len(tasbats_to_process[0])):
        # print(tasbats_to_process[0][x])
        if tasbats_to_process[0][x].UINorg == UIN \
                and tasbats_to_process[0][x].Misc_Ref2_or_JPA_Claim_Authority != 'NULL' and \
                        tasbats_to_process[0][x].Misc_Ref2_or_JPA_Claim_Authority != 'GYH Mileage in Same Theatre' and \
                        tasbats_to_process[0][x].Source in ADMIT_SOURCES:
            n7406_tasbats.append(tasbats_to_process[0][x])

    print('found {} N7406 entries'.format(len(n7406_tasbats)))
    for x in range(0, len(n7406_tasbats)):
        print('found line at {}'.format(n7406_tasbats[x].lineno))
    return n7406_tasbats

def strip_tds(tds):
    print('got t_s_sheets to: ', len(tds))
    pass


def main():
    # get lists of sheet objects to process...
    tasbats_to_process = load_tasbat()
    n7406_tasbats = strip_tasbats(tasbats_to_process)
    t_s_sheet = load_t_s_sheet()
    strip_tasbats(t_s_sheet)

main()

