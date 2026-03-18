import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY", "your-groq-api-key-here"))

def generate_answer(query: str, chunks: list[str]) -> str:
    context = "\n\n---\n\n".join(chunks[:3])
    prompt = f"""You are a helpful assistant. Answer the question using ONLY the context below.
If the answer is not in the context, say "I couldn't find that in the document."

Context:
{context}

Question: {query}

Answer:"""
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    return response.choices[0].message.content

