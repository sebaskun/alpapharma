import fitz
import re
import spacy

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


def extract_candidates(text: str):
    """
    Extract candidate pharmaceutical terms using noun chunks.
    Uses blacklist filtering and LLM validation for ambiguous single words.
    """
    from utils.llm_handler import llm_validate_pharmaceutical_terms
    from utils.term_blacklist import should_exclude_term, clean_text
    from utils.drug_lookup_dict import DRUG_DICT

    candidates = set()
    word_to_sentence = {}
    multi_words = set()

    paragraphs = text.split('\n')

    for para in paragraphs:
        if not para.strip():
            continue
        doc = nlp(para)

        for chunk in doc.noun_chunks:
            head = chunk.root
            if head.pos_ in {"NOUN", "PROPN"}:
                candidate = clean_text(chunk.text.strip())
                if candidate and not candidate.isdigit():
                    if len(candidate.split()) == 1:

                        if should_exclude_term(candidate):
                            continue  # Skip blacklisted terms
                        else:
                            # Only ambiguous terms go to LLM with clean sentence context
                            clean_sentence = clean_text(chunk.root.sent.text.strip())
                            word_to_sentence[candidate] = clean_sentence
                    else:
                        # Check multi-word phrases for embedded drug names
                        words_in_phrase = re.split(r'[\s\-/,]+', candidate)
                        has_embedded_drug = False

                        for word in words_in_phrase:
                            word_clean = clean_text(word.strip())
                            if word_clean and word_clean.upper() in DRUG_DICT:
                                # Found embedded drug - add to LLM validation with full phrase context
                                clean_sentence = clean_text(chunk.root.sent.text.strip())
                                word_to_sentence[word_clean] = clean_sentence
                                has_embedded_drug = True

                        # If no embedded drugs found, add full phrase as regular multi-word candidate
                        if not has_embedded_drug:
                            multi_words.add(candidate)

    # Add all multi-word phrases without embedded drugs (low ambiguity)
    candidates.update(multi_words)

    # Batch validate single words and embedded drugs with LLM
    if word_to_sentence:
        validation_results = llm_validate_pharmaceutical_terms(word_to_sentence)
        for word, is_pharma in validation_results.items():
            if is_pharma:
                candidates.add(word)

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
                    "info": DRUG_DICT[query_results["documents"][0][0].upper()]
                })
                print(f" - Found match {token} in vector store with distance {query_results['distances'][0][0]}")
                # break

    return found_entities
