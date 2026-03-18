import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="PDF RAG Chatbot", page_icon="📄")
st.title(" PDF RAG Chatbot")
st.caption("Upload a PDF, then ask questions about it!")

st.subheader("Step 1 — Upload a PDF")
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file:
    with st.spinner("Ingesting PDF into Endee vector database..."):
        response = requests.post(
            f"{API_URL}/upload",
            files={"file": (uploaded_file.name, uploaded_file, "application/pdf")}
        )
    if response.status_code == 200:
        st.success(response.json()["message"])
    else:
        st.error("Upload failed. Is the backend running?")

st.subheader("Step 2 — Ask questions")
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask something about your PDF..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Searching Endee + generating answer..."):
            try:
                res = requests.post(f"{API_URL}/chat", json={"question": prompt})
                if res.status_code == 200:
                    answer = res.json().get("answer", "Error getting answer")
                else:
                    answer = f"Backend error: {res.status_code} - {res.text}"
            except Exception as e:
                answer = f"Error: {str(e)}"
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})