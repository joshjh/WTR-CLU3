__author__ = 'josh'
import re

def tasbat_execute(tasbat):
    claim_no_format = 'P\d\d\d\d\d\d\d\d'
    processed_claims = []
    recoveries = 0

    for x in range(0, len(tasbat)):
        match = re.match(claim_no_format, str(tasbat[x].Misc_Ref_or_JPA_Claim_Number))
        if match and tasbat[x].Misc_Ref_or_JPA_Claim_Number not in processed_claims:
            processed_claims.append(tasbat[x].Misc_Ref_or_JPA_Claim_Number)
            if tasbat[x].UIN == 'N0198A':
               try:
                   if re.search(r'\d\d\d\d\d\d\d', tasbat[x].Misc_Ref2_or_JPA_Claim_Authority):
                       print('TASBAT: Claim {} by {} likely needs to be recovered'.format(tasbat[x].Misc_Ref_or_JPA_Claim_Number,
                                                                                          tasbat[x].whois[1]))
                       recoveries+=1
               except TypeError:
                   # if we get type-error, it's likely that the JPA_Claim_Authority is a integer:
                   try:
                       if re.search(r'\d\d\d\d\d\d\d', str(tasbat[x].Misc_Ref2_or_JPA_Claim_Authority)):
                            print('TASBAT: Claim {} by {} likely needs to be recovered'.format(tasbat[x].Misc_Ref_or_JPA_Claim_Number,
                                                                                          tasbat[x].whois[1]))
                            recoveries+=1
                   except:
                       print('Claim number {} whois: {} unrecongnised Claim Authority No!'.format())

    print('TASBAT scanned {} lines, suggested {} recoveries'.format(len(tasbat), recoveries))





