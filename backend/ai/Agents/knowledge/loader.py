"""
loader.py

Responsible for:

1. Loading PDF files
2. Extracting text
3. Splitting into LangChain Documents

No embeddings.
No Gemini.
No ChromaDB.
"""

from pathlib import Path

import fitz  # PyMuPDF

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class PDFLoader:
    """
    Reads a PDF and converts it into LangChain Documents.
    """

    def __init__(
        self,
        chunk_size: int = 800,
        chunk_overlap: int = 150,
    ):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def extract_text(self, pdf_path: str) -> str:
        """
        Extract raw text from PDF.
        """

        pdf_path = Path(pdf_path)

        if not pdf_path.exists():
            raise FileNotFoundError(f"{pdf_path} not found.")

        doc = fitz.open(pdf_path)

        text = ""

        for page in doc:
            text += page.get_text("text") + "\n"

        doc.close()

        return text.strip()

    def split_text(self, text: str):
        """
        Convert raw text into LangChain Documents.
        """

        documents = [Document(page_content=text)]

        chunks = self.splitter.split_documents(documents)

        return chunks

    def load(self, pdf_path: str):
        """
        Complete pipeline.

        PDF
            ↓
        Extract
            ↓
        Split
            ↓
        Return Chunks
        """

        text = self.extract_text(pdf_path)

        chunks = self.split_text(text)

        return chunks