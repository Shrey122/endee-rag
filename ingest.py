import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

import fitz
from endee import Endee, Precision
from sentence_transformers import SentenceTransformer

INDEX_NAME = "pdf_chunks"
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_client():
    return Endee()

def create_index():
    client = get_client()
    try:
        client.create_index(
            name=INDEX_NAME,
            dimension=384,
            space_type="cosine",
            precision=Precision.INT8
        )
    except Exception:
        pass

def extract_chunks(pdf_path, chunk_size=300):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    words = full_text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    return chunks

def ingest_pdf(pdf_path):
    create_index()
    chunks = extract_chunks(pdf_path)
    embeddings = model.encode(chunks).tolist()
    client = get_client()
    index = client.get_index(name=INDEX_NAME)
    vectors = []
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        vectors.append({
            "id": str(i),
            "vector": embedding,
            "meta": {"text": chunk}
        })
    for i in range(0, len(vectors), 50):
        index.upsert(vectors[i:i + 50])
    return len(chunks)