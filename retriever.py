import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from endee import Endee
from sentence_transformers import SentenceTransformer

INDEX_NAME = "pdf_chunks"
model = SentenceTransformer("all-MiniLM-L6-v2")

def search_chunks(query, top_k=5):
    query_vector = model.encode([query])[0].tolist()
    client = Endee()
    index = client.get_index(name=INDEX_NAME)
    results = index.query(vector=query_vector, top_k=top_k, ef=128)
    chunks = []
    for item in results:
        if item.get("meta") and item["meta"].get("text"):
            chunks.append(item["meta"]["text"])
    return chunks