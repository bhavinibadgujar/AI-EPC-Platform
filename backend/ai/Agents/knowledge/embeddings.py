"""
embeddings.py

Responsible for:
1. Creating Google Embedding Model
2. Creating ChromaDB Vector Store
3. Saving document chunks
4. Loading existing vector store
"""

from pathlib import Path
import shutil

from backend.config import GEMINI_API_KEY
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma


# Folder where ChromaDB will be stored
CHROMA_PATH = Path("backend/data/chroma_db")


class EmbeddingManager:
    """
    Handles embedding creation and vector database.
    """

    def __init__(self):
        # Google Embedding Model
        self.embedding_model = GoogleGenerativeAIEmbeddings(
            model="gemini-embedding-2",
            google_api_key=GEMINI_API_KEY,
        )

    def create_vector_store(self, chunks):
        """
        Create a fresh ChromaDB database.
        """

        # Delete old database if it exists
        if CHROMA_PATH.exists():
            shutil.rmtree(CHROMA_PATH)

        # Create a new empty folder
        CHROMA_PATH.mkdir(parents=True, exist_ok=True)

        # Create vector database
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=self.embedding_model,
            persist_directory=str(CHROMA_PATH),
        )

        return vector_store

    def load_vector_store(self):
        """
        Load existing ChromaDB database.
        """

        vector_store = Chroma(
            persist_directory=str(CHROMA_PATH),
            embedding_function=self.embedding_model,
        )

        return vector_store

    def add_documents(self, chunks):
        """
        Add new chunks into an existing database.
        """

        db = self.load_vector_store()

        db.add_documents(chunks)

        return db