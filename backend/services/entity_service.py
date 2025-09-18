import re
from utils.drug_lookup_dict import DRUG_DICT, NDC_DICT


def get_entity_from_id(id: str):
    ndc_pattern = re.compile(r'^\d+[-\d]*$')

    if ndc_pattern.match(id):
        if id in NDC_DICT:
            return NDC_DICT[id]
    
    else:
        if id in DRUG_DICT:
            return DRUG_DICT[id.upper()]
        
    return {}