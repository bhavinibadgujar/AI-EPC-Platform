import streamlit as st
import os
from utils.pdf_reader import extract_text

st.set_page_config(
    page_title="EPC AI Copilot",
    page_icon="🏗️",
    layout="wide"
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

st.title("🏗️ EPC AI Copilot")
st.subheader("AI Intelligence Platform for Data Centre EPC Projects")

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

if uploaded_file is not None:

    filepath = os.path.join(
        UPLOAD_FOLDER,
        uploaded_file.name
    )

    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("PDF Uploaded Successfully!")

    # Read PDF
    text = extract_text(filepath)

    st.subheader("Extracted Text")

    st.text_area(
        "PDF Content",
        text,
        height=400
    )