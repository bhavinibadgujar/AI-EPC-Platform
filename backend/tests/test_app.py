from fastapi.testclient import TestClient

from backend.app.main import app


def test_health_endpoint_reports_service():
    with TestClient(app) as client:
        response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_chat_requires_question():
    with TestClient(app) as client:
        response = client.post("/chat", json={})

    assert response.status_code == 400
