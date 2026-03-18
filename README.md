# PDF RAG Chatbot using Endee Vector Database

A RAG (Retrieval Augmented Generation) chatbot that lets you
upload any PDF and ask questions about it — powered by the
Endee vector database.

## Project Overview
This project demonstrates a real-world AI application using:
- **Endee** as the vector database for semantic search
- **FastAPI** as the backend REST API
- **PyMuPDF** for PDF text extraction
- **sentence-transformers** for generating embeddings
- **Groq LLM** for generating answers
- **Streamlit** for the chat UI

## System Design
User uploads PDF → PyMuPDF extracts text → sentence-transformers 
creates embeddings → Endee stores vectors → User asks question → 
Endee semantic search finds relevant chunks → Groq LLM generates answer

## How Endee is Used
- Creates a cosine similarity index with 384 dimensions
- Stores embedded text chunks with metadata
- Performs fast semantic vector search at query time
- Returns most relevant chunks to feed into the LLM

## Setup Instructions

### Prerequisites
- Python 3.9+
- Docker Desktop

### Step 1 - Clone the repo
git clone https://github.com/Shrey122/endee-rag
cd endee-rag

### Step 2 - Install dependencies
pip install -r requirements.txt

### Step 3 - Start Endee vector database
docker compose up -d

### Step 4 - Add your Groq API key
Get free Groq API key from https://console.groq.com
Open app/generator.py and add your key

### Step 5 - Start the backend
uvicorn app.main:application --reload --port 8000

### Step 6 - Start the UI
streamlit run ui/streamlit_app.py

### Step 7 - Open browser
http://localhost:8501

## Usage
1. Upload any PDF file
2. Wait for ingestion into Endee vector database
3. Ask any question about the PDF content
4. Get AI-powered answers based on the document

## Tech Stack
- Vector Database: Endee
- Backend API: FastAPI
- PDF Processing: PyMuPDF
- Embeddings: sentence-transformers (all-MiniLM-L6-v2)
- LLM: Groq (llama-3.3-70b-versatile)
- UI: Streamlit
