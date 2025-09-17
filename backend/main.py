import re
from fastapi import FastAPI, UploadFile, HTTPException
from utils.drug_lookup_dict import init_drug_dict
from utils.vectorstore_handler import ChromaManager
from services.pdf_parser import load_pdf_text_from_upload, scan_text_for_entities
from services.entity_service import get_entity_from_id

app = FastAPI()

# initialize utils
init_drug_dict()

# Initialize vectorstore
VECTOR_STORE = ChromaManager()


@app.post("/extract")
def extract_entities_from_pdf(file: UploadFile):
    # check if file is pdf
    if file.content_type != "application/pdf":
        return {"error": "Invalid file type. Please upload a PDF file."}
    
    text = load_pdf_text_from_upload(file)
    search = scan_text_for_entities(text)

    return {"search": search}

# Query vectorstore endpoint
@app.get("/query")
def query_vectorstore(term: str):
    results = VECTOR_STORE.query(term, n_results=5)
    return results

# Entity details endpoint
@app.get("/entity/{id_or_uri}")
def get_entity_details(id_or_uri: str):
    """
    Get detailed information about a drug or ingredient.
    """
    entity = get_entity_from_id(id_or_uri)
    if not entity:
        return HTTPException(status_code=404, detail=f"entity with id {id} not found")
    
    return entity



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)