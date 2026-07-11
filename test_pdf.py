from backend.agents.utils.pdf_reader import extract_text

# Use a valid PDF from scripts/output/pdfs directory
pdf_path = "scripts/output/pdfs/spec_1.pdf"
try:
    text = extract_text(pdf_path)
    # Print first 500 characters to check
    print(f"Successfully extracted text from {pdf_path}")
    print(f"Text length: {len(text)} characters")
    print("\nFirst 500 characters:")
    print(text[:500])
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")

