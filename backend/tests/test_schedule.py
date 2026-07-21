from pathlib import Path

from fastapi.testclient import TestClient

from backend.app.agents.schedule.agent import ScheduleAgent
from backend.app.main import app


SAMPLE = Path("dataset/schedules/schedule_1.csv")


def test_schedule_agent_computes_critical_path():
    report = ScheduleAgent().analyze(SAMPLE)

    assert report["project_duration"] == 13
    assert report["critical_path"] == ["A001", "A002", "A003"]
    assert report["analysis"]["summary"]["total_activities"] == 3
    assert report["risks"]


def test_schedule_risk_endpoint_accepts_csv_upload():
    with TestClient(app) as client:
        with SAMPLE.open("rb") as handle:
            response = client.post("/schedule-risk", files={"file": ("schedule.csv", handle, "text/csv")})

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "success"
    assert payload["project_duration"] == 13
    assert payload["critical_path"] == ["A001", "A002", "A003"]
    assert payload["summary"]["open_risks"] >= 1
