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
pip install Flask pinecone pinecone-plugin-assistant PyMuPDF pymupdf4llm
```

### Activate Environment
```bash
source lifewave-env/bin/activate
```

## Dependencies

All dependencies are installed in the `lifewave-env` virtual environment:
- **Python 3.12+** 
- **Flask** (3.1.2) - Web server for serving HTML interface
- **pinecone** (7.3.0) - Core Pinecone client
- **pinecone-plugin-assistant** (1.7.0) - Assistant functionality  
- **PyMuPDF** (1.26.4) - PDF processing via `fitz` module
- **pymupdf4llm** (0.0.27) - Enhanced PDF to markdown conversion

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

### `bin/pdf_to_markdown.py`
Converts all PDF files from `pdfs/` directory to markdown files in `markdown/` directory using pymupdf4llm for enhanced formatting and structure preservation.

**Usage:**
```bash
./bin/pdf_to_markdown.py
# OR with virtual environment activated:
python bin/pdf_to_markdown.py
```

### `bin/clean_html_tags.py`
Removes HTML tags from markdown files that contain them, cleaning up formatting artifacts from PDF conversion.

**Usage:**
```bash
./bin/clean_html_tags.py
```

### `bin/remove_javascript.py`
Removes `(javascript:.*)` blocks from markdown files to clean up any JavaScript artifacts.

**Usage:**
```bash
./bin/remove_javascript.py
```

### `bin/clean_invisible_chars.py`
Detects and removes null bytes, control characters, and other invisible characters that can cause parsing issues.

**Usage:**
```bash
./bin/clean_invisible_chars.py
```

### `bin/escape_statistical_notation.py`
Escapes statistical notation patterns like `p<0.001` using backticks to prevent MDX JSX parsing errors.

**Usage:**
```bash
./bin/escape_statistical_notation.py
```

### `server.py`
Flask web server that serves the chat interface (`index.html`) and static files.

**Usage:**
```bash
python server.py
# Access at http://localhost:5000
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

The project follows a multi-layer architecture:

### Data Processing Pipeline:
1. **PDF Conversion** (`pdf_to_text.py`) - PDF to text conversion for embeddings
2. **Markdown Conversion** (`bin/pdf_to_markdown.py`) - PDF to markdown for enhanced readability
3. **Document Cleaning** - Multiple scripts to clean and prepare markdown:
   - `bin/clean_html_tags.py` - Remove HTML artifacts
   - `bin/remove_javascript.py` - Remove JavaScript blocks
   - `bin/clean_invisible_chars.py` - Remove problematic invisible characters
   - `bin/escape_statistical_notation.py` - Escape statistical notation for MDX compatibility
4. **Embedding Layer** (`text_to_embeddings.py`) - Text to vector embeddings using llama-text-embed-v2
5. **Index Upload** (`upload_embeddings.py`) - Vector embeddings to Pinecone index "lifewave-x39"

### Assistant Layer:
6. **Creation Layer** (`create_agent.py`) - Assistant initialization
7. **Data Layer** (`upload.py`) - Text file ingestion to Pinecone Assistant
8. **Query Layer** (`agent.py`) - Assistant interaction and file management

### Web Interface:
9. **Presentation Layer** (`server.py`) - Flask web server serving chat interface

All scripts use a shared Pinecone API key. Vector scripts target the "lifewave-x39" index, while assistant scripts use "lifewave-assistant".

## Directory Structure

- `pdfs/` - Contains 28 research PDFs organized by topic:
  - Acupressure studies and abstracts
  - LifeWave X39 patch research and clinical trials
  - Phototherapy and nanotechnology papers
  - Patent documents and regulatory information
- `vectors/` - Contains converted text files from PDFs (28 .txt files)
- `markdown/` - Contains converted markdown files from PDFs (using pymupdf4llm)
- `embeddings/` - Contains vector embeddings as JSON files (28 .json files)
  - Generated using llama-text-embed-v2 model
  - 1024-dimensional embeddings with metadata
  - Includes chunking information and source text
- `bin/` - Utility scripts for data processing:
  - `pdf_to_markdown.py` - PDF to markdown conversion
  - `clean_html_tags.py` - HTML tag removal
  - `remove_javascript.py` - JavaScript block removal
  - `clean_invisible_chars.py` - Invisible character cleaning
  - `escape_statistical_notation.py` - Statistical notation escaping for MDX
- `lifewave-env/` - Python virtual environment (excluded from git)
- `index.html` - Chat interface powered by n8n webhook
- `server.py` - Flask web server for serving the interface
- `README.md` - Project overview and setup instructions

## Development Notes

- **Virtual Environment**: Always use `lifewave-env` - scripts are configured with local shebang paths
- Scripts use hardcoded API keys (consider environment variables for production)
- No formal testing framework - verify functionality by running scripts directly
- Error handling is basic (try/catch with print statements)
- PDF processing relies on PyMuPDF's `fitz` module for document parsing
- **Document Cleaning**: Multiple cleaning scripts ensure markdown compatibility with various parsers
- **MDX Compatibility**: Statistical notation is escaped to prevent JSX parsing errors
- **Embeddings**: Generated using llama-text-embed-v2 through Pinecone inference API
  - Free tier available until March 1, then $0.16/1M tokens
  - 1024-dimensional vectors optimized for retrieval tasks
  - Intelligent chunking preserves document context
  - 103 total vectors uploaded to "lifewave-x39" index