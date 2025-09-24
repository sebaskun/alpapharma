# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AlpaPharma is an AI-powered Applicant Tracking System (ATS) that extracts pharmaceutical entities (drugs, ingredients, compounds) from specialist CVs using multi-stage validation with LLMs and vector similarity search.

## Development Commands

### Backend (Python/FastAPI)

```bash
cd backend

# Environment setup
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Start development server
python main.py
# Server runs on http://localhost:8000

# Run tests (if present)
pytest

# Environment configuration
cp .env.example .env
# Edit .env to add API keys (GOOGLE_API_KEY or OPENAI_API_KEY)
```

### Frontend (Vue 3/TypeScript)

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
# Server runs on http://localhost:5173

# Build for production
npm run build

# Preview production build
npm run preview
```

## Architecture Overview

### Data Flow Pipeline
```
PDF → Text Extraction → Entity Candidates → Blacklist Filter → LLM Validation → Drug Dictionary → Vector Store → Results
```

### Core Components

**Backend (`backend/`)**
- `main.py` - FastAPI application with CORS middleware for frontend communication
- `services/pdf_parser.py` - PDF text extraction using PyMuPDF and entity extraction using spaCy
- `services/entity_service.py` - Entity information retrieval and metadata handling
- `utils/llm_handler.py` - Multi-provider LLM integration (Google Gemini/OpenAI) for contextual validation
- `utils/vectorstore_handler.py` - ChromaDB interface with SapBERT embeddings
- `utils/drug_lookup_dict.py` - FDA dataset dictionary for exact matching
- `utils/term_blacklist.py` - Filtering logic to exclude non-pharmaceutical terms

**Frontend (`frontend/`)**
- Vue 3 + TypeScript + Tailwind CSS
- Single-page application for PDF upload and results display
- Uses Vite for build tooling

### Key Technologies
- **LLM Integration**: Google Gemini (preferred) or OpenAI for contextual validation
- **NLP**: spaCy with `en_core_web_sm` model for entity extraction
- **Vector Search**: ChromaDB with SapBERT embeddings for semantic similarity
- **PDF Processing**: PyMuPDF (fitz) for text extraction
- **Web Framework**: FastAPI with automatic OpenAPI documentation

### External Dependencies
- **FDA Dataset**: `drug-ndc-0001-of-0001.json` in `/data` directory
- **Vector Store**: Pre-built ChromaDB store in `/chroma_store` directory
- **spaCy Models**: Download with `python -m spacy download en_core_web_sm`

### API Endpoints
- `POST /extract` - Upload PDF and extract pharmaceutical entities
- `GET /entity/{id}` - Get FDA metadata for specific entity
- `GET /query` - Direct vector store querying for development
- `GET /health` - Health check endpoint
- `GET /version` - System version and feature information

### Environment Configuration
The system supports dual LLM providers configured via environment variables:
- `GOOGLE_API_KEY` - Google Gemini API key (recommended for faster responses)
- `OPENAI_API_KEY` - OpenAI API key (fallback option)
- `LLM_PROVIDER` - Set to "gemini" or "openai"

### Entity Processing Strategy
1. Extract noun chunks from PDF text using spaCy
2. Filter candidates using pharmaceutical term blacklist
3. Build word-to-sentence context mapping
4. Use LLM to validate ambiguous pharmaceutical terms in context
5. Check exact matches against FDA drug dictionary
6. Use vector similarity search for semantic matching with SapBERT embeddings
7. Return matched entities with FDA metadata

### Testing and Quality
- Uses pytest for backend testing (pytest available in virtual environment)
- No test files currently exist - tests should be created in `backend/tests/` directory
- Frontend uses Vue 3 composition API with TypeScript for type safety

### Project Structure Requirements
```
pharma_challenge/
├── backend/           # Python FastAPI backend
├── frontend/          # Vue 3 frontend
├── data/             # FDA dataset (drug-ndc-0001-of-0001.json)
├── chroma_store/     # Pre-built vector database
└── [config files]
```