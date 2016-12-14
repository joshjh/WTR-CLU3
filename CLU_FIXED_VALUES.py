__author__ = 'josh'
# What should be::
FIX_POSTCODE = 'PL22BG'
POSTCODE_FORMATS = ['\w\w\d\w\d\w\w', '\w\d\w\d\w\w', '\w\d\d\w\w', '\w\d\d\d\w\w', '\w\w\d\d\w\w', '\w\w\d\d\d\w\w', '\w\w\d\d\w\w']

FIX_VALUES_ORGANISATIONS = ('HASLER COY',  'MTM HASLER COY MA7 MEDICAL WELFARE DISCIPLINE')

FIX_VALUES_JR = {'Temp_Allowance_Reason': '', 'Change_of_IBD_Reason': '', 'Perm_Allowance_Reason': 'P02', 'Gender': 'Male',
               'Type': 'Employee.Available for Assignment',  'PAYD/_LOS12/_GYH(S)': 'YNN',
              'Temp_Allowance_Location': '', 
               'Location': 'PLYMOUTH (HMS DRAKE)',  
               'Status': 'Active Assignment', 'Field_or_Shipboard': '',
               'Temp_Accomp_Status': '', 'Nationality': 'British',
               'Perm_Allowance_Location': 'GBR',  'Perm_HTD_Location': '',
               'Addressable_Rank': '', 'Temp_HTD_Location': '', 'Perm_SLA_Charged': 'G1Z',
               'Perm_Field_or_Shipboard': 'N', 'Temp_SLA_Charged': '', 'Temp_SLA_Occupied': '',
               'Perm_SLA_Occupied': ''}

FIX_VALUES_SR = {'Temp_Allowance_Reason': '', 'Change_of_IBD_Reason': '', 'Perm_Allowance_Reason': 'P02', 'Gender': 'Male',
               'Type': 'Employee.Available for Assignment',  'PAYD/_LOS12/_GYH(S)': 'YNN',
              'Temp_Allowance_Location': '', 
               'Location': 'PLYMOUTH (HMS DRAKE)',  
               'Status': 'Active Assignment', 'Field_or_Shipboard': '',
               'Temp_Accomp_Status': '', 'Nationality': 'British',
               'Perm_Allowance_Location': 'GBR', 'Organization': 'HASLER COY ', 'Perm_HTD_Location': '',
               'Addressable_Rank': '', 'Temp_HTD_Location': '', 'Perm_SLA_Charged': 'G1S',
               'Perm_Field_or_Shipboard': 'N', 'Temp_SLA_Charged': '', 'Temp_SLA_Occupied': '',
               'Perm_SLA_Occupied': ''}

FIX_VALUES_GRUNTER_JO = {'Temp_Allowance_Reason': '', 'Change_of_IBD_Reason': '', 'Perm_Allowance_Reason': 'P02', 'Gender': 'Male',
               'Type': 'Employee.Available for Assignment',  'PAYD/_LOS12/_GYH(S)': 'YNN',
              'Temp_Allowance_Location': '', 
               'Location': 'PLYMOUTH (HMS DRAKE)',  
               'Status': 'Active Assignment', 'Field_or_Shipboard': '',
               'Temp_Accomp_Status': '', 'Nationality': 'British',
               'Perm_Allowance_Location': 'GBR',  'Perm_HTD_Location': '',
               'Addressable_Rank': '', 'Temp_HTD_Location': '', 'Perm_SLA_Charged': 'G1JO',
               'Perm_Field_or_Shipboard': 'N', 'Temp_SLA_Charged': '', 'Temp_SLA_Occupied': '',
               'Perm_SLA_Occupied': ''}

FIX_VALUES_GRUNTER_SO = {'Temp_Allowance_Reason': '', 'Change_of_IBD_Reason': '', 'Perm_Allowance_Reason': 'P02', 'Gender': 'Male',
               'Type': 'Employee.Available for Assignment',  'PAYD/_LOS12/_GYH(S)': 'YNN',
              'Temp_Allowance_Location': '', 
               'Location': 'PLYMOUTH (HMS DRAKE)',  
               'Status': 'Active Assignment', 'Field_or_Shipboard': '',
               'Temp_Accomp_Status': '', 'Nationality': 'British',
               'Perm_Allowance_Location': 'GBR',  'Perm_HTD_Location': '',
               'Addressable_Rank': '', 'Temp_HTD_Location': '', 'Perm_SLA_Charged': 'G1SO',
               'Perm_Field_or_Shipboard': 'N', 'Temp_SLA_Charged': '', 'Temp_SLA_Occupied': '',
               'Perm_SLA_Occupied': ''}

FIX_VALUES_JUNIOR_RATES_RANKS = ('OR2|OR Main|01', 'OR4|OR Main|01', 'OR2|OR Main|02', 'OR4|OR Main|02')

FIX_VALUES_SENIOR_RATES_RANKS = ('OR6|OR Main|01', 'OR7|OR Main|01', 'OR8|OR Main|01', 'OR9|OR Main|01, OR6|OR Main|02',
                                     'OR7|OR Main|02', 'OR8|OR Main|02', 'OR9|OR Main|02', 'OR9|OR Main|01')
FIX_VALUES_JUNIOR_GRUNTERS_RANKS = ('OF1|OF Main|01', 'OF2|OF Main|01', 'OF1|OF Main|02', 'OF2|OF Main|02')

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'