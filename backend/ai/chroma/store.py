import chromadb
from app.ai.gemini import embed

_client = chromadb.PersistentClient(path="app/ai/chroma/db")

def get_collection(name: str):
    return _client.get_or_create_collection(name)

def add_chunk(collection_name: str, chunk_id: str, text: str, metadata: dict):
    collection = get_collection(collection_name)
    collection.add(
        ids=[chunk_id],
        embeddings=[embed(text)],
        documents=[text],
        metadatas=[metadata]
    )

def query(collection_name: str, query_text: str, top_k: int = 5):
    collection = get_collection(collection_name)
    query_embedding = embed(query_text)
    return collection.query(query_embeddings=[query_embedding], n_results=top_k)