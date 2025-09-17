import json

DRUG_DICT = {}
NDC_DICT = {}


def init_drug_dict():
    # for now it look in /data folder
    global DRUG_DICT, NDC_DICT
    print("Building drug dictionaries from FDA data...")
    with open("../data/drug-ndc-0001-of-0001.json", "r") as f:
        fda_data = json.load(f)
        build_drug_dict(fda_data)
    print(f"Loaded {len(DRUG_DICT)} drug/ingredient entries into DRUG_DICT.")
    print(f"Loaded {len(NDC_DICT)} drug/ingredient entries into NDC_DICT.")


def build_drug_dict(fda_data: dict):
    """
    Builds a dictionary of drugs and ingredients from FDA dataset.
    
    Structure:
    {
        "MUCINEX CHILDRENS MIGHTY CHEWS COUGH NIGHTTIME": { ... full FDA record ... },
        "DEXTROMETHORPHAN HYDROBROMIDE": { ... FDA record ... },
        "DOXYLAMINE SUCCINATE": { ... FDA record ... },
        ...
    }
    """
    global DRUG_DICT, NDC_DICT

    results = fda_data.get("results", [])
    for record in results:
        # Brand name
        brand = record.get("brand_name")
        if brand:
            DRUG_DICT[brand.upper()] = {
                "is_ingredient": False,
                "record": record
            }

        # Generic name
        generic = record.get("generic_name")
        if generic:
            DRUG_DICT[generic.upper()] = {
                "is_ingredient": False,
                "record": record
            }

        # Active ingredients
        for ing in record.get("active_ingredients", []):
            ing_name = ing.get("name")
            if ing_name:
                DRUG_DICT[ing_name.upper()] = {
                    "is_ingredient": True,
                    "record": record
                }

        # ndc_dict
        product_ndc = record.get("product_ndc")
        if product_ndc:
            NDC_DICT[product_ndc] = record