import fitz
import re
import spacy
from spacy.tokens import Span

from fastapi import UploadFile
from utils.drug_lookup_dict import DRUG_DICT
from utils.vectorstore_handler import ChromaManager


VECTOR_STORE = ChromaManager()
nlp = spacy.load("en_core_web_sm")

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


def extract_candidates(text: str):
    """
    Extract candidate multi-word phrases from text using noun chunks.
    Keeps chunks whose head token is NOUN/PROPN.
    Processes text paragraph by paragraph to avoid cross-paragraph chunks.
    """
    candidates = set()
    paragraphs = text.split('\n')

    for para in paragraphs:
        if not para.strip():
            continue
        doc = nlp(para)

        for chunk in doc.noun_chunks:
            head = chunk.root
            if head.pos_ in {"NOUN", "PROPN"}:
                candidate = chunk.text.strip()
                if candidate and not candidate.isdigit():
                    candidates.add(candidate)

    return list(candidates)



def scan_text_for_entities(text: str):
    found_entities = []
    # Simple word-based scanning (can later improve with fuzzy/vectorstore)
    tokens = extract_candidates(text)
    seen = set()

    for token in tokens:
        print(f"Processing token: {token}")
        key = token.upper().strip()
        if key in seen:
            continue

        if key in DRUG_DICT:
            seen.add(key)
            found_entities.append({
                "name": token,
                "source": "exact_match",
                "info": DRUG_DICT[key]
            })
            print(f" - Found exact match in drug dict: {token}")
            
        else:
            # check first word by word
            found = False
            for word in token.split(" "):
                if word.upper().strip() in seen:
                    seen.add(key)
                    continue
                
                if word.upper().strip() in DRUG_DICT:
                    
                    # double check context with vectorstore
                    query_results = VECTOR_STORE.query(token, n_results=1)  # to log
                    if query_results["distances"][0][0] > 50:
                        print(f" - Exact match {word} found but high distance {query_results['distances'][0][0]} in token: {token}")
                        continue
                    
                    found_entities.append({
                        "name": word,
                        "source": "exact_match_partial",
                        "distance": query_results["distances"][0][0],
                        "info": DRUG_DICT[word.upper().strip()]
                    })
                    print(f" - Found partial exact match {word} in vector store with distance {query_results['distances'][0][0]} in token: {token}")
                    found = True
                    seen.add(key)
                    break
            if found:
                continue

            # Use vector store to find similar drugs
            query_results = VECTOR_STORE.query(token, n_results=1)
            if query_results and query_results.get("documents"):
                seen.add(key)
                if query_results["distances"][0][0] > 50:
                    continue
                found_entities.append({
                    "name": token,
                    "source": "vectorstore",
                    "info": query_results["documents"][0]
                })
                print(f" - Found match {token} in vector store with distance {query_results['distances'][0][0]}")
                # break

    return found_entities
