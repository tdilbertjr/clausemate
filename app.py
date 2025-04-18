import streamlit as st
import os
from dotenv import load_dotenv
import fitz  # PyMuPDF
from openai import OpenAI

load_dotenv()

# Load your OpenAI key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Clausemate", layout="centered")

st.title("📄 Clausemate")
st.subheader("Your Legal Document Copilot – Summarize and Interact with Contracts using AI")

uploaded_file = st.file_uploader("Upload a legal document (.txt or .pdf)", type=["txt", "pdf"])

def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

text = ""
if uploaded_file:
    if uploaded_file.name.endswith(".pdf"):
        text = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".txt"):
        text = uploaded_file.read().decode("utf-8")

    st.text_area("Extracted Text", text, height=200)

    if st.button("Summarize Document"):
        with st.spinner("Summarizing..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful legal assistant."},
                        {"role": "user", "content": f"Summarize this legal document:\n{text}"}
                    ]
                )
                summary = response.choices[0].message.content
                st.success("Summary:")
                st.write(summary)
            except Exception as e:
                st.error(f"Error: {e}")

    st.markdown("---")
    st.subheader("Ask a Question")

    question = st.text_input("Enter your question:")

    if question and st.button("Ask"):
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful legal assistant."},
                        {"role": "user", "content": f"Based on the following legal text:\n{text}\n\nAnswer the question: {question}"}
                    ]
                )
                answer = response.choices[0].message.content
                st.success("Answer:")
                st.write(answer)
            except Exception as e:
                st.error(f"Error: {e}")

st.markdown("---")
st.caption("🔹 Built by Terry Dilbert · Veteran Technologist & Future Legal Strategist")
