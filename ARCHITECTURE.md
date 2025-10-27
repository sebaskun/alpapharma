# Architecture

## Overview

This project is an **Applicant Tracking System (ATS)** tailored for pharmaceutical specialists. It employs a multi-stage pipeline to extract and classify pharmaceutical entities from candidate CVs.

## Core Pipeline

### Process (Short Version)

1. **Text Extraction**: Use *PyMuPDF* to extract text from the PDF file.
2. **Chunking**: Split text into manageable sections, first by paragraphs, then by sentences with **spaCy** (`en_core_web_sm`).
3. **Entity Candidates**: Focus on nouns as potential pharmaceutical entities.
4. **Filtering**: Apply a blacklist to remove irrelevant entities (e.g., state names, credentials, business terms).
5. **Context Clarification**:

   * Build a dictionary mapping each word to its sentence context (`word_to_sentence`).
   * Send the dictionary to an LLM (Gemini or OpenAI) for contextual classification.
   * LLM returns a refined dictionary marking whether each word is a valid pharmaceutical entity in context.
6. **Vector Matching**:

   * Use the **SapBERT** model (`cambridgeltl/SapBERT-from-PubMedBERT-fulltext`) with FDA drug data to build a vector store.
   * First, check for direct matches against a curated FDA drug dictionary.
   * If no match, query the vector store. Accept entities if similarity distance is within threshold.

### Pros & Cons

* **Pros**: FDA dataset ensures high precision for approved brand/generic drugs.
* **Cons**: Research drugs not yet registered won’t match, limiting coverage in production scenarios.

### Result

Final output: **A list of pharmaceutical entities enriched with FDA metadata.**

## Data Flow

```
PDF → Text → Tokens → Blacklist → LLM → Drug Dictionary → VectorStore → Results
```

## Key Components

### Backend (`backend/`)

* **FastAPI**: REST API endpoints
* **PDF Parser**: Text extraction and pre-processing
* **LLM Handler**: Contextual entity disambiguation (multi-provider)
* **Vector Store**: Semantic similarity search with SapBERT
* **Drug Dictionary**: FDA dataset indexing for exact matching

### Frontend (`frontend/`)

* **Vue 3**: Reactive UI
* **File Upload**: PDF input for processing
* **Results Display**: Categorized pharmaceutical entities
* **Entity Details**: FDA metadata presentation
* **Concept**: A simple branded interface (*AlphaPharma*) where users upload CVs, wait for analysis, and receive entity results.

## Entity Classification

* **FDA Dataset**: Covers brand names, generic names, and active ingredients.
* **Vector Store**: Embeddings built from FDA dataset for similarity search.

---
## small test