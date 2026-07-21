import fitz

def extract_text(pdf_path):
    """Extract all text from a PDF."""
    doc = fitz.open(pdf_path)

    text = ""

    for page in doc:
        text += page.get_text()

    doc.close()

    return text