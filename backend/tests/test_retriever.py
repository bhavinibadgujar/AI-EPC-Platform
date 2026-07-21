from backend.app.rag.store import SimpleVectorStore


def test_retriever_returns_empty_without_matches():
    store = SimpleVectorStore()
    store.index_pages("spec.pdf", [{"page": 1, "text": "Switchgear energization"}])

    assert store.retrieve("chilled water") == []
