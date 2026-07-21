from fastapi.testclient import TestClient

from backend.app.main import app


def test_chat_uses_seeded_document_context():
    with TestClient(app) as client:
        response = client.post("/chat", json={"question": "What is the UPS autonomy?"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["answer"]
    assert payload["citations"]
