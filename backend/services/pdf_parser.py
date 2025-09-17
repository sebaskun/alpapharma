import fitz
import re
import spacy

from fastapi import UploadFile
from utils.drug_lookup_dict import DRUG_DICT
from utils.vectorstore_handler import ChromaManager


VECTOR_STORE = ChromaManager()


def load_pdf_text_from_upload(uploaded_file: UploadFile) -> str:
    """
    Extracts text directly from an uploaded PDF (in-memory).
    """
    file_bytes = uploaded_file.file.read()
    text = []
    # Open the PDF from bytes using fitz
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            page_text = page.get_text()
            if page_text:
                text.append(page_text)
    return "\n".join(text)


def exact_search(text: str, query: str) -> list[str]:
    """
    Performs a simple exact search for the query inside the text.
    Returns list of matched lines.
    """
    results = []
    for line in text.split("\n"):
        if query in line:
            results.append(line.strip())
    return results


def scan_text_for_entities(text: str):
    found_entities = []
    # Simple word-based scanning (can later improve with fuzzy/vectorstore)
    tokens = re.findall(r"\b[A-Za-z][A-Za-z0-9\- ]+\b", text)
    seen = set()

    for token in tokens:
        key = token.upper().strip()

        if key in DRUG_DICT and key not in seen:
            seen.add(key)
            found_entities.append({
                "name": token,
                "source": "exact_match",
                "info": DRUG_DICT[key]
            })

        elif key not in seen:
            print(f"Querying vector store for: {token}")
            # Use vector store to find similar drugs
            query_results = VECTOR_STORE.query(token, n_results=1)
            if query_results and query_results.get("documents"):
                seen.add(key)
                if query_results["distances"][0][0] > 86:
                    continue
                found_entities.append({
                    "name": token,
                    "source": "vectorstore",
                    "info": query_results["documents"][0]
                })
                # need to add distance filter
                print(f" - Found in vector store with distance {query_results['distances'][0][0]}")
                # break

    return found_entities

