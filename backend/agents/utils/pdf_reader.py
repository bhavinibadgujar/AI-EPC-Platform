import fitz
import os

def extract_text(pdf_path):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"File not found: {pdf_path}")

    if os.path.getsize(pdf_path) == 0:
        raise ValueError(f"PDF file is empty (0 bytes): {pdf_path}")

    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        raise ValueError(f"Failed to open PDF file: {pdf_path}. Error: {str(e)}")

    if doc.page_count == 0:
        raise ValueError(f"PDF has no pages: {pdf_path}")

    text = ""
    for page in doc:
        text += page.get_text()

    doc.close()
    return text