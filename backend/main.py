from fastapi import FastAPI, UploadFile
from utils.drug_lookup_dict import init_drug_dict
from utils.vectorstore_handler import ChromaManager

app = FastAPI()

# initialize utils
init_drug_dict()

# Initialize vectorstore
VECTOR_STORE = ChromaManager()



# api.py
from services.pdf_parser import load_pdf_text_from_upload, scan_text_for_entities
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



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)