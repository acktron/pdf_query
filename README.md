# PDF Query System

A PDF query system that allows users to upload PDF files and ask questions about their content using Ollama.

## Quick Start

### Step 1: Install Ollama

**macOS (with Homebrew):**
```bash
brew install ollama
```

**Other platforms:**
Download from https://ollama.ai

### Step 2: Pull the llama2 Model

```bash
ollama pull llama2
```

### Step 3: Start Ollama Server

Open a terminal and run:
```bash
ollama serve
```

Keep this terminal open. Ollama will run on `http://127.0.0.1:11434`.

### Step 4: Start FastAPI Backend

Open a **new terminal** and run:

```bash
cd /path/to/pdf_query
source venv/bin/activate
python3 -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

*(Replace `/path/to/pdf_query` with your actual project directory path)*

### Step 5: Open Browser

Navigate to: `http://127.0.0.1:8000`

Upload a PDF and ask questions!

## Setup (First Time Only)

### Backend Dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Frontend Dependencies

```bash
npm install
npm run build
```

## Project Structure

- `main.py` - FastAPI application entry point
- `llm_client.py` - Ollama LLM client wrapper
- `pdf_utils.py` - PDF text extraction utilities
- `src/` - React frontend source code
- `dist/` - Built React app (generated after `npm run build`)
- `requirements.txt` - Python dependencies
- `package.json` - Node.js dependencies

## API Endpoint

**POST `/query-pdf`**

Accepts:
- `file`: PDF file (multipart/form-data)
- `question`: User's question (form field)

Returns:
```json
{
  "answer": "Answer from Ollama",
  "context_truncated": false,
  "context_length": 1234
}
```
