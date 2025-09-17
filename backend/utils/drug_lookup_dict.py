import json

DRUG_DICT = {}


def init_drug_dict():
    # for now it look in /data folder
    global DRUG_DICT
    print("Building drug dictionary from FDA data...")
    with open("../data/drug-ndc-0001-of-0001.json", "r") as f:
        fda_data = json.load(f)
        DRUG_DICT = build_drug_dict(fda_data)
    print(f"Loaded {len(DRUG_DICT)} drug/ingredient entries into DRUG_DICT.")


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
    global DRUG_DICT
    drug_dict= {}

    results = fda_data.get("results", [])
    for record in results:
        # Brand name
        brand = record.get("brand_name")
        if brand:
            drug_dict[brand.upper()] = {
                "brand_name": brand,
                "product_ndc": record.get("product_ndc"),
                "labeler_name": record.get("labeler_name"),
                "active_ingredients": record.get("active_ingredients", []),
                "dosage_form": record.get("dosage_form"),
                "product_type": record.get("product_type"),
                "brand_name_base": record.get("brand_name_base"),
                # "pharm_Class": record.get("pharm_class"),
            }

        # Generic name
        generic = record.get("generic_name")
        if generic:
            drug_dict[generic.upper()] = {
                "generic_name": generic,
                "product_ndc": record.get("product_ndc"),
                "labeler_name": record.get("labeler_name"),
                "active_ingredients": record.get("active_ingredients", []),
                "dosage_form": record.get("dosage_form"),
                "product_type": record.get("product_type"),
                "brand_name_base": record.get("brand_name_base"),
                # "pharm_Class": record.get("pharm_class"),
            }

        # Active ingredients
        for ing in record.get("active_ingredients", []):
            ing_name = ing.get("name")
            if ing_name:
                drug_dict[ing_name.upper()] = {
                    "ITS_INGREDIENT": True,
                    "record": record
                }

    return drug_dict