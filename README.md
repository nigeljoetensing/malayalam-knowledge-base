# A Malayalam AI Knowledge Base

<p align="center">
  <img src="https://img.shields.io/badge/Language-Malayalam-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/LLM-Ollama%20Local-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Vector%20DB-ChromaDB-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Embeddings-LaBSE-purple?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge" />
</p>

---

> An AI-powered Retrieval-Augmented Generation (RAG) system built specifically for Malayalam-language documents. Index 50+ Malayalam PDFs — digital or scanned — and get instant, citation-backed answers in Malayalam or English. Runs 100% on-premise using Ollama. No API keys. No internet required. No data leaves your machine.

---

## Table of Contents

- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [License](#license)

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   INGESTION PIPELINE                    │
│  (run once)                                             │
│                                                         │
│  50 PDFs  →  Extract  →  Chunk  →  Embed  →  ChromaDB  │
│           pdfplumber    512 chars  LaBSE    vector store│
│           + Tesseract   mal-aware  768-dim              │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                    QUERY PIPELINE                       │
│  (per request)                                          │
│                                                         │
│  Question  →  Embed  →  Search  →  Context  →  Answer  │
│  Mal/Eng     LaBSE    ChromaDB    Top-5       Ollama    │
│                        top-k      chunks      (local)   │
└─────────────────────────────────────────────────────────┘
```

---

## Prerequisites

### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| OS | Windows 10 / Ubuntu 20.04 / macOS 12 | Windows 11 / Ubuntu 24.04 |
| Python | 3.10 | 3.11+ |
| RAM | 8 GB | 16 GB |
| Disk | 5 GB free | 15 GB |
| CPU | 4 cores | 8 cores |

### Required Software

1. **Python 3.11+** — https://www.python.org/downloads/
2. **Ollama** — https://ollama.com/download
3. **Tesseract OCR** (with Malayalam language pack)
   - Windows: https://github.com/UB-Mannheim/tesseract/wiki
   - During install: check ✅ **Add to PATH** and ✅ **Malayalam** under additional languages
4. **Poppler**
   - Windows: https://github.com/oschwartz10612/poppler-windows/releases
   - Extract to `C:\poppler\` and add `C:\poppler\Library\bin` to system PATH

### Verify Installations

```bash
python --version          # Python 3.11+
tesseract --version       # Tesseract 5.x
tesseract --list-langs    # must include: mal
pdfinfo --version         # confirms Poppler is in PATH
ollama --version          # Ollama installed
```

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/nigeljoetensing/malayalam-knowledge-base.git
cd malayalam-knowledge-base
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3.11 -m venv venv
source venv/bin/activate
```

### 3. Install Python Dependencies

```bash
python -m pip install --upgrade pip

python -m pip install chromadb==0.4.24 \
    pdfplumber==0.11.0 \
    sentence-transformers==2.7.0 \
    pytesseract==0.3.10 \
    pdf2image==1.17.0 \
    ollama==0.2.1 \
    python-dotenv==1.0.1 \
    tqdm==4.66.2 \
    Pillow==10.3.0
```

### 4. Pull Ollama Model

```bash
# Start Ollama (if not already running)
ollama serve

# In a new terminal — pull a model
ollama pull llama3       # recommended
# or
ollama pull mistral      # faster, lighter
```

### 5. Configure Environment

Create a `.env` file in the project root:

```bash
# .env
OLLAMA_MODEL=llama3
OLLAMA_HOST=http://localhost:11434
PDF_DIR=./pdfs
CHROMA_DIR=./chroma_db
```

### 6. Add Your PDFs

Place all Malayalam PDF files in the `pdfs/` folder:

```
vaaksetu/
└── pdfs/
    ├── kerala_history.pdf
    ├── malayalam_literature.pdf
    └── ...
```

---

## Usage

### Step 1 — Index Your Documents (Run Once)

```bash
python ingest.py
```

Expected output:
```
Found 14 PDFs to ingest
   [OCR] No text layer — running Tesseract (mal+eng)
   ✓ Indexed 8 chunks
   ...
Done! Total docs in ChromaDB: 94
```

> Ingestion takes 15–25 minutes for 50 PDFs. It is safe to re-run — existing chunks are updated, not duplicated.

### Step 2 — Ask Questions

```bash
python query.py
```

```
Malayalam Knowledge Base (Ollama Local Mode)
════════════════════════════════════════════════════════
Ollama connected  |  Model: llama3
   All inference is local — no data leaves this machine.

Knowledge base loaded: 94 chunks indexed

ചോദ്യം (Question): കേരളത്തിലെ പ്രധാന നദികൾ ഏവ?

Retrieved sources:
   • kerala_geography.pdf, p.1  (score: 0.923)
   • rivers_of_india.pdf, p.3   (score: 0.887)

Answer [llama3 — local]:
കേരളത്തിലെ പ്രധാന നദികൾ... [Source: kerala_geography.pdf, Page 1]
```

---

## Project Structure

```
vaaksetu/
│
├── pdfs/                    # Place your Malayalam PDFs here
├── chroma_db/               # ChromaDB vector store (auto-created)
│
├── src/
│   ├── extractor.py         # PDF text extraction + OCR
│   ├── chunker.py           # Malayalam-aware text chunking
│   ├── embedder.py          # LaBSE multilingual embeddings
│   ├── indexer.py           # ChromaDB indexing
│   ├── retriever.py         # Similarity search
│   └── qa_engine.py         # Ollama LLM answer generation
│
├── ingest.py                # Run once to index all PDFs
├── query.py                 # Interactive Q&A interface
├── test_ocr.py              # OCR diagnostic tool
├── debug_check.py           # PDF extraction diagnostic
├── .env                     # Configuration (not committed to git)
├── .gitignore               # Excludes venv, chroma_db, .env
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

---

## Configuration

All configuration is in `.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_MODEL` | `llama3` | LLM model name (`llama3`, `mistral`, `gemma3`) |
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama server address |
| `PDF_DIR` | `./pdfs` | Folder containing Malayalam PDFs |
| `CHROMA_DIR` | `./chroma_db` | ChromaDB persistent storage path |

### Choosing an Ollama Model

| Model | Size | Speed | Malayalam Quality |
|-------|------|-------|-------------------|
| `llama3` | 4.7 GB | Medium | Best overall |
| `mistral` | 4.1 GB | Fast | Good |
| `gemma3` | 3.3 GB | Fast | Fair |
| `llama3:70b` | 40 GB | Slow | Excellent |

---

## Built With

- [ChromaDB](https://www.trychroma.com/) — On-premise vector database
- [LaBSE](https://huggingface.co/sentence-transformers/LaBSE) — Multilingual sentence embeddings
- [Ollama](https://ollama.com/) — Local LLM inference
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) — Malayalam OCR engine
- [pdfplumber](https://github.com/jsvine/pdfplumber) — PDF text extraction
- [sentence-transformers](https://www.sbert.net/) — Embedding model wrapper

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---
