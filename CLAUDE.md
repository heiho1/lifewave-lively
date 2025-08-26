# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based project that creates and manages a Pinecone assistant for LifeWave-related document analysis. The project focuses on uploading and processing PDF documents containing research papers, studies, and patents related to acupressure, phototherapy, and LifeWave X39 patches.

## Virtual Environment Setup

**CRITICAL: This project uses a local virtual environment named `lifewave-env`. All scripts are configured to use this environment's Python interpreter.**

### Initial Setup
```bash
# Create virtual environment (already done)
python3 -m venv lifewave-env

# Install dependencies
source lifewave-env/bin/activate
pip install pinecone pinecone-plugin-assistant PyMuPDF
```

### Activate Environment
```bash
source lifewave-env/bin/activate
```

## Dependencies

All dependencies are installed in the `lifewave-env` virtual environment:
- **Python 3.12+** 
- **pinecone** (7.3.0) - Core Pinecone client
- **pinecone-plugin-assistant** (1.7.0) - Assistant functionality  
- **PyMuPDF** (1.26.3) - PDF processing via `fitz` module

## Key Scripts

**IMPORTANT: All scripts use `#!/lifewave-env/bin/python3` shebang and can be run directly as executables.**

### `create_agent.py`
Creates a new Pinecone assistant named "lifewave-assistant" with specific instructions for polite, concise responses in American English.

**Usage:**
```bash
./create_agent.py
# OR with virtual environment activated:
python create_agent.py
```

### `upload.py`
Bulk uploads text files from the `vectors/` directory to the Pinecone assistant. Includes error handling for failed uploads.

**Usage:**
```bash
./upload.py
# OR with virtual environment activated:
python upload.py
```

### `agent.py`
Retrieves and lists files associated with the existing "lifewave-assistant".

**Usage:**
```bash
./agent.py
# OR with virtual environment activated:
python agent.py
```

### `pdf_to_text.py`
Converts all PDF files from `documents/` directory to text files in `vectors/` directory using PyMuPDF.

**Usage:**
```bash
./pdf_to_text.py
# OR with virtual environment activated:
python pdf_to_text.py
```

### `text_to_embeddings.py`
Converts text files from `vectors/` directory to embeddings using Pinecone's llama-text-embed-v2 model. Saves embeddings as JSON files in `embeddings/` directory.

**Features:**
- Uses llama-text-embed-v2 (1024-dimensional embeddings)
- Intelligent text chunking with sentence boundary detection
- Handles large documents by splitting into manageable chunks
- Rate limiting to respect API quotas

**Usage:**
```bash
./text_to_embeddings.py
# OR with virtual environment activated:
python text_to_embeddings.py
```

### `upload_embeddings.py`
Uploads vector embeddings from `embeddings/` directory to Pinecone index "lifewave-x39". Creates the index if it doesn't exist.

**Features:**
- Automatically creates Pinecone index with optimal settings
- Batch uploading with rate limiting
- Comprehensive metadata including source file and chunk information
- Progress tracking and error handling

**Usage:**
```bash
./upload_embeddings.py
# OR with virtual environment activated:
python upload_embeddings.py
```

## Architecture

The project follows a six-script workflow:

1. **Conversion Layer** (`pdf_to_text.py`) - PDF to text conversion
2. **Embedding Layer** (`text_to_embeddings.py`) - Text to vector embeddings using llama-text-embed-v2
3. **Index Upload** (`upload_embeddings.py`) - Vector embeddings to Pinecone index "lifewave-x39"
4. **Creation Layer** (`create_agent.py`) - Assistant initialization
5. **Data Layer** (`upload.py`) - Text file ingestion to Pinecone Assistant
6. **Query Layer** (`agent.py`) - Assistant interaction and file management

All scripts use a shared Pinecone API key. Vector scripts target the "lifewave-x39" index, while assistant scripts use "lifewave-assistant".

## Directory Structure

- `documents/` - Contains 28 research PDFs organized by topic:
  - Acupressure studies and abstracts
  - LifeWave X39 patch research and clinical trials
  - Phototherapy and nanotechnology papers
  - Patent documents and regulatory information
- `vectors/` - Contains converted text files from PDFs (28 .txt files)
- `embeddings/` - Contains vector embeddings as JSON files (28 .json files)
  - Generated using llama-text-embed-v2 model
  - 1024-dimensional embeddings with metadata
  - Includes chunking information and source text
- `lifewave-env/` - Python virtual environment (excluded from git)

## Development Notes

- **Virtual Environment**: Always use `lifewave-env` - scripts are configured with local shebang paths
- Scripts use hardcoded API keys (consider environment variables for production)
- No formal testing framework - verify functionality by running scripts directly
- Error handling is basic (try/catch with print statements)
- PDF processing relies on PyMuPDF's `fitz` module for document parsing
- **Embeddings**: Generated using llama-text-embed-v2 through Pinecone inference API
  - Free tier available until March 1, then $0.16/1M tokens
  - 1024-dimensional vectors optimized for retrieval tasks
  - Intelligent chunking preserves document context
  - 103 total vectors uploaded to "lifewave-x39" index