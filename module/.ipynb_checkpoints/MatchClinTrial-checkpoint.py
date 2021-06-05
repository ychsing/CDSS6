import re as __re
import numpy as __np
import module.models as models

def EGFR_sim(EGFR_patient_info, EGFR_criteria):
    EGFR_criteria_list = EGFR_criteria.split(',')
    if len(EGFR_criteria_list)==1 and str(EGFR_criteria_list[0]) in EGFR_patient_info : 
        return 1
    else:
        n = 0
        for egfr in EGFR_criteria_list:
            egfr = str(egfr)
            if egfr in EGFR_patient_info:
                n+=1
        EGFR_patient_info_len = EGFR_patient_info.split(',')
        if len(EGFR_patient_info_len) == n:
            return 1
        else:
            return n/len(EGFR_criteria_list)
        
def stage_sim(stage_patient_info, stage_criteria):
    stage_criteria_list = stage_criteria.split(',')
    if stage_patient_info in stage_criteria_list:
        return 1
    else:
        return 0

def histo_sim(histo_patient_info, histo_criteria):
    histo_criteria_list = histo_criteria.split(',')
    output = 0
    if histo_criteria == 'NSCLC':
        for hist in ['ADC','Sqcc','LCC']:
            if hist == histo_patient_info:
                return 1
        return output
    for histo in histo_criteria_list:
        if histo == histo_patient_info:
            return 1
    return output

def age_match(age_patient_info, age_criteria):
    lower = age_criteria[0]
    upper = age_criteria[1]
    if age_patient_info == '-' or age_patient_info == '':
        return 0
    if int(age_patient_info)>=lower and int(age_patient_info)<=upper:
        return 1
    else:
        return 0
    
def ECOG_match(ECOG_patient_info, ECOG_criteria):
    lower = ECOG_criteria[0]
    upper = ECOG_criteria[1]
    if ECOG_patient_info == '-' or ECOG_patient_info == '':
        return 0
    if int(ECOG_patient_info)>=lower and int(ECOG_patient_info)<=upper:
        return 1
    else:
        return 0
    
def size_match(size_patient_info, size_criteria):
    lower = size_criteria[0]
    upper = size_criteria[1]
    if size_patient_info == '-' or size_patient_info == '':
        return 0
    if int(size_patient_info)>=lower and int(size_patient_info)<=upper:
        return 1
    else:
        return 0
    
def pair_ClinicalTrial(soap, report, manual_input, criteria):
    patient_info = models.phenotype_9(soap, report)
    patient_info.update(manual_input)
    patient_info_list = list(patient_info.values())
    criteria_id = [i for i in range(len(criteria)) if criteria[i]!='']
    a = 0
    b = len(criteria_id)
    p,c = '',''
    process_id = {1:histo_sim,2:size_match,3:stage_sim,4:EGFR_sim,14:age_match,33:ECOG_match}
    for i in criteria_id:
        p = patient_info_list[i]
        c = criteria[i]
        if i in process_id.keys():
            a+=process_id[i](p,c)
        else:
            if str(p)==str(c):
                a+=1
    return '{} %'.format(__np.around(a/b*100,2))