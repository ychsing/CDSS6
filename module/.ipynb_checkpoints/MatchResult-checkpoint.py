import module.MatchClinTrial as MCT

def __json_parser(patient_json, criteria_json):
    soap = patient_json["pathology_report"]["soap"]
    report = patient_json["pathology_report"]["soap"]
    manual_input = patient_json["manual_input"]
    return soap, report, manual_input

def get_result(patient_json, criteria_json):
    soap, report, manual_input = __json_parser(patient_json, criteria_json)
    output = []
    for k,v in criteria_json.items():
        score =  MCT.pair_ClinicalTrial(soap, report, manual_input, v)
        output.append("{}'s match prob : {}".format(k,score))
    return output