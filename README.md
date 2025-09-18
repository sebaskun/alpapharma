# AlpaPharma - Pharmaceutical CV Entity Extractor

AI-powered ATS system that extracts pharmaceutical entities (drugs, ingredients, compounds) from specialist CVs using multi-stage validation with LLMs and vector similarity search.

## 🏗️ Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed system design and API documentation.

## 📋 Prerequisites

- **Python 3.8+**
- **Node.js 16+** and npm
- **OpenAI API key** or **Google Gemini API key**
- Internet connection for model downloads

## 🚀 Installation

### Backend Setup

1. **Clone and navigate to backend:**
   ```bash
   cd backend
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download spaCy model:**
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. **Set up data directories:**
   ```bash
   # Create data directory in project root (one level up from backend)
   mkdir ../data
   ```

5. **Download and setup FDA dataset:**
   ```bash
   # Download FDA drug dataset
   curl -o ../data/drug-ndc-0001-of-0001.json.zip https://download.open.fda.gov/drug/ndc/drug-ndc-0001-of-0001.json.zip

   # Extract the JSON file
   cd ../data
   Folder should be at same level as /backend and /frontend
   unzip drug-ndc-0001-of-0001.json.zip
   cd ../backend
   ```

6. **Download pre-built vector store:**

   **Option A (Recommended): Use Pre-built Vector Store**
   ```bash
   # Download from Google Drive
   # https://drive.google.com/file/d/1KREf_1bcRjjbG9UdzbZKt9OrJBgHaQk2/view?usp=sharing

   # Extract to project root (one level up from backend)
   # The extracted folder should be: ../chroma_store/
   Folder should be at same level as /backend and /frontend
   ```

   **Option B: Build Your Own Vector Store**
   - Use this Google Colab notebook: https://colab.research.google.com/drive/1QkKClTrf1Rp8m6yEuJ7ZVuYF0VnnXKhs#scrollTo=kye_W_IGLLtb
   - Follow the notebook instructions to generate the vector store
   - Download and place the generated `chroma_store` folder in the project root

7. **Configure environment variables:**
   ```bash
   # Copy environment template
   cp .env.example .env

   # Edit .env and add your API keys
   # Choose ONE of the following:

   # For OpenAI (alternative option):
   OPENAI_API_KEY=your_openai_api_key_here

   # For Google Gemini (preferred - faster response):
   GOOGLE_API_KEY=your_google_gemini_api_key_here
   ```

8. **Verify folder structure:**
   ```
   pharma_challenge/
   ├── backend/
   │   ├── main.py
   │   ├── requirements.txt
   │   └── .env
   ├── data/
   │   └── drug-ndc-0001-of-0001.json
   ├── chroma_store/          # Vector store (used by backend)
   │   └── [chroma files]
   └── frontend/
   ```

9. **Start backend server:**
   ```bash
   python main.py
   ```
   Server will run on `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```
   Frontend will run on `http://localhost:5173`

## ⚙️ Configuration Options

### SpaCy Models (Optional)

For better accuracy, you can install larger spaCy models:

```bash
# Medium model (better accuracy)
python -m spacy download en_core_web_md

# Large model (best accuracy, slower)
python -m spacy download en_core_web_lg
```

Then update your code to use the larger model in `backend/services/pdf_parser.py`:
```python
nlp = spacy.load("en_core_web_md")  # or "en_core_web_lg"
```

### LLM Provider Configuration

**Google Gemini (Recommended)** - Faster response time:
```bash
# In .env file
GOOGLE_API_KEY=your_google_gemini_api_key
```

**OpenAI (Alternative)**:
```bash
# In .env file
OPENAI_API_KEY=your_openai_api_key
```

The system automatically uses Gemini if available, otherwise falls back to OpenAI.

## 🔧 API Endpoints

### POST /extract
Extract pharmaceutical entities from PDF CV:
```bash
curl -X POST "http://localhost:8000/extract" \
  -F "file=@path/to/cv.pdf"
```

### GET /entity/{id}
Get detailed information about a specific entity:
```bash
curl "http://localhost:8000/entity/65162-630"
```

### GET /query
Query vectorstore directly:
```bash
curl "http://localhost:8000/query?term=itraconazole&n_results=5"
```

## 📁 Project Structure

```
pharma_challenge/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   ├── services/           # Business logic
│   │   ├── pdf_parser.py   # PDF processing & entity extraction
│   │   └── entity_service.py
│   └── utils/              # Utilities
│       ├── vectorstore_handler.py  # ChromaDB interface
│       ├── drug_lookup_dict.py     # FDA dictionary
│       ├── llm_handler.py          # LLM integration
│       └── term_blacklist.py       # Filtering logic
├── frontend/
│   ├── src/
│   │   └── App.vue         # Main Vue application
│   ├── package.json        # Node dependencies
│   └── vite.config.ts      # Vite configuration
├── data/
│   └── drug-ndc-0001-of-0001.json  # FDA dataset
├── chroma_store/           # Vector database (ChromaDB)
└── ARCHITECTURE.md         # System documentation
```

## 🚨 Troubleshooting

### Common Issues

1. **"Chroma persist directory does not exist"**
   - Ensure the `chroma_store` folder is in the project root
   - Verify you downloaded and extracted the vector store correctly

2. **"drug-ndc-0001-of-0001.json not found"**
   - Check that the FDA dataset is in `../data/` relative to the backend folder
   - Verify the file was extracted correctly from the zip

3. **CORS errors**
   - Ensure frontend is running on `http://localhost:5173`
   - Backend CORS is configured for this specific URL

4. **LLM API errors**
   - Verify your API keys are correctly set in `.env`
   - Check that you have credits/quota available

5. **spaCy model not found**
   - Run `python -m spacy download en_core_web_sm`
   - Ensure you're in the correct Python environment

### Performance Tips

1. **Use Gemini over OpenAI** for faster response times
2. **Large spaCy models** improve accuracy but are slower
3. **Vector store location** should be on SSD for better performance

## 📊 Usage

1. Start both backend and frontend servers
2. Navigate to `http://localhost:5173`
3. Upload a pharmaceutical specialist's CV (PDF format)
4. Wait for analysis to complete
5. View extracted entities categorized as:
   - **Drugs**: Brand names and generic drugs
   - **Ingredients**: Active pharmaceutical ingredients
6. Click on any entity to see detailed FDA information
