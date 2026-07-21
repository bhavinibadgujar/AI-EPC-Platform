"""
retriever.py

Responsible for:
1. Loading ChromaDB
2. Searching similar chunks
3. Returning relevant documents

No Gemini.
No Prompt.
"""

from backend.agents.knowledge.embeddings import EmbeddingManager


class KnowledgeRetriever:
    """
    Retrieves relevant chunks from ChromaDB.
    """

    def __init__(self):
        self.embedding_manager = EmbeddingManager()
        self.db = self.embedding_manager.load_vector_store()

    def retrieve(self, question: str, k: int = 5):
        """
        Search the vector database.

        Args:
            question (str): User question
            k (int): Number of chunks to return

        Returns:
            List[Document]
        """

        results = self.db.similarity_search(
            query=question,
            k=k
        )

        return results

    def print_results(self, question: str, k: int = 5):
        """
        Helper function for testing.
        """

        docs = self.retrieve(question, k)

        print("=" * 80)
        print("QUESTION:")
        print(question)
        print("=" * 80)

        for i, doc in enumerate(docs, start=1):
            print(f"\nResult {i}")
            print("-" * 80)
            print(doc.page_content[:400])