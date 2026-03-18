import os
import sys
import shutil

sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from ingest import ingest_pdf
from retriever import search_chunks
from generator import generate_answer

application = FastAPI(title="RAG Chatbot with Endee")

class QueryRequest(BaseModel):
    question: str

@application.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    num_chunks = ingest_pdf(temp_path)
    os.remove(temp_path)
    return {"message": f"Ingested {num_chunks} chunks from {file.filename}"}

@application.post("/chat")
async def chat(request: QueryRequest):
    chunks = search_chunks(request.question)
    if not chunks:
        return {"answer": "No relevant content found. Please upload a PDF first."}
    answer = generate_answer(request.question, chunks)
    return {"answer": answer, "sources": chunks[:2]}

@application.get("/health")
async def health():
    return {"status": "ok"}