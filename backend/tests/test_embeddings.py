from backend.app.rag.store import SimpleVectorStore


def test_simple_vector_store_retrieves_matching_chunk():
    store = SimpleVectorStore()
    store.index_pages("spec.pdf", [{"page": 42, "text": "UPS battery autonomy shall be 15 minutes."}])

    results = store.retrieve("UPS autonomy", k=1)

    assert results[0]["document"] == "spec.pdf"
    assert results[0]["page"] == 42
