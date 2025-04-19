import streamlit as st
import os
import fitz  # PyMuPDF
from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()

# Load OpenAI key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Streamlit page config
st.set_page_config(page_title="Clausemate", layout="wide")

# Unified background styling (color + image)
st.markdown(
    """
    <style>
    .stApp {
        background-color: #766759;
        background-image: url("Clausemate_BG.png");
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: bottom right;
        background-size: 50%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Fixed Header Logo (Fallback Method) ---
from PIL import Image
logo = Image.open("Logo.png")

st.markdown(
    """
    <style>
        .logo-container {
            display: flex;
            align-items: center;
            position: fixed;
            top: 1.2rem;
            left: 1.5rem;
            z-index: 999;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Render the logo using st.image() inside custom div
st.markdown('<div class="logo-container">', unsafe_allow_html=True)
st.image(logo, width=600)
st.markdown('</div>', unsafe_allow_html=True)

# Spacer to avoid overlap
st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)


# --- Title & Description ---
st.title("Your Legal Copilot, Reinvented")
st.markdown(
    "Upload a contract or agreement, and Clausemate will break it down for you in plain English."
)

# --- File Uploader ---
st.markdown("📎 Upload a legal document (.pdf or .txt)")
uploaded_file = st.file_uploader(" ", type=["pdf", "txt"])

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

# --- Footer ---
st.markdown("---")
st.caption("✨ Built by Terry Dilbert · Veteran Technologist & Future Legal Strategist")
