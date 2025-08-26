# LifeWave X39 Research Assistant

This is a Python-based project that creates an AI assistant for LifeWave X39 patch research analysis. This project processes PDF research documents and provides an interactive chat interface powered by Pinecone vector search and n8n webhook integration.

## Overview

This project combines document processing, vector embeddings, and AI assistance to make LifeWave X39 research more accessible. It includes 28 research papers covering acupressure studies, phototherapy research, clinical trials, and patent documentation.

## Features

- **PDF Processing**: Convert PDFs to text and markdown formats
- **Vector Search**: Generate embeddings and upload to Pinecone for semantic search
- **AI Assistant**: Pinecone assistant trained on research documents
- **Web Interface**: Flask-served chat interface with n8n integration
- **Data Cleaning**: Scripts to remove HTML tags and JavaScript from processed documents

## Quick Start

1. **Setup Environment**:
   ```bash
   python3 -m venv lifewave-env
   source lifewave-env/bin/activate
   pip install Flask pinecone pinecone-plugin-assistant PyMuPDF pymupdf4llm
   ```

2. **Process Documents**:
   ```bash
   ./pdf_to_text.py              # Convert PDFs to text
   ./bin/pdf_to_markdown.py      # Convert PDFs to markdown
   ./text_to_embeddings.py       # Generate vector embeddings
   ./upload_embeddings.py        # Upload to Pinecone index
   ```

3. **Setup Assistant**:
   ```bash
   ./create_agent.py             # Create Pinecone assistant
   ./upload.py                   # Upload documents to assistant
   ```

4. **Start Web Interface**:
   ```bash
   python server.py              # Start Flask server
   # Access at http://localhost:5000
   ```

## Project Structure

```
├── pdfs/              # 28 research PDFs
├── vectors/           # Text files converted from PDFs
├── markdown/          # Markdown files converted from PDFs
├── embeddings/        # Vector embeddings (JSON)
├── bin/               # Utility scripts
│   ├── pdf_to_markdown.py
│   ├── clean_html_tags.py
│   └── remove_javascript.py
├── lifewave-env/      # Python virtual environment
├── index.html         # Chat interface
├── server.py          # Flask web server
└── README.md          # This file
```

## Research Focus

The included research documents cover:
- **Acupressure Studies**: Pain reduction, weight management, sleep improvement
- **LifeWave X39 Research**: Clinical trials and pilot studies
- **Phototherapy**: Low-level light therapy mechanisms
- **Regulatory**: Anti-doping agency approvals and patent documentation

## Technologies

- **Python 3.12+** with virtual environment
- **Pinecone** for vector search and AI assistant
- **PyMuPDF & pymupdf4llm** for PDF processing
- **Flask** for web server
- **n8n** webhook for chat functionality

## Usage

The chat interface allows users to ask questions about LifeWave X39 patches and receive responses based on the processed research documents. The AI assistant has access to clinical trial data, study results, and scientific literature related to phototherapy and acupressure.

## Note

This is a research and educational tool. All information is derived from publicly available research papers and studies. Users should consult healthcare professionals for medical advice.