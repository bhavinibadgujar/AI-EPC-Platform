from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone


SEED_STATE = {
    "compliance_results": [
        {
            "id": "CMP-001",
            "parameter": "UPS battery autonomy",
            "requirement": "15 minutes at full IT load",
            "required_value": "15 minutes",
            "submitted_value": "10 minutes",
            "status": "Deviation",
            "severity": "Critical",
            "source": "EPC Specification",
            "page": 42,
            "snippet": "UPS shall support full IT load for 15 minutes.",
        },
        {
            "id": "CMP-002",
            "parameter": "Generator load bank test",
            "requirement": "4 hour load bank test at 100% nameplate rating",
            "required_value": "4 hours at 100%",
            "submitted_value": "2 hours at 75%",
            "status": "Deviation",
            "severity": "Major",
            "source": "EPC Specification",
            "page": 67,
            "snippet": "Emergency generators require a 4 hour full-load acceptance test.",
        },
    ],
    "documents": [
        {
            "id": "spec-demo",
            "name": "Sample EPC Specification",
            "pages": [
                {"page": 42, "text": "UPS shall support full IT load for 15 minutes. Vendor submittals must include battery calculations."},
                {"page": 67, "text": "Emergency generators require a 4 hour full-load acceptance test with load bank evidence."},
            ],
        }
    ],
    "schedule_risks": [
        {"id": "SCH-001", "activity": "Temporary power energization", "reason": "Successor commissioning activity starts before predecessor float recovers.", "severity": "Critical", "eta": "9 days", "owner": "Construction"},
        {"id": "SCH-002", "activity": "BMS point-to-point testing", "reason": "Controls integration has low float and unresolved interface dependency.", "severity": "Major", "eta": "4 days", "owner": "Controls"},
    ],
    "supply_chain": [
        {"vendor": "Schneider Electric", "package": "Switchgear", "status": "On Track", "eta": "2026-08-12"},
        {"vendor": "Vertiv", "package": "UPS Systems", "status": "At Risk", "eta": "2026-08-29"},
        {"vendor": "Carrier", "package": "Chillers", "status": "Delayed", "eta": "2026-09-04"},
    ],
    "commissioning": [
        {"item": "UPS integrated systems test", "owner": "Cx Lead", "progress": 86, "status": "In Progress"},
        {"item": "Generator black start sequence", "owner": "Electrical", "progress": 72, "status": "Ready"},
        {"item": "BMS point-to-point validation", "owner": "Controls", "progress": 58, "status": "Blocked"},
        {"item": "Chilled water balancing", "owner": "Mechanical", "progress": 91, "status": "Passed"},
    ],
    "chat_history": [
        {"question": "What are the top compliance gaps?", "answer": "UPS autonomy and generator load-bank evidence are the top gaps."}
    ],
}


def fresh_state() -> dict:
    state = deepcopy(SEED_STATE)
    state["seeded_at"] = datetime.now(timezone.utc).isoformat()
    return state
