from __future__ import annotations

from backend.app.core.gemini_client import generate_json


class CommissioningAgent:
    def analyze(self, checklist: list[dict]) -> dict:
        blockers = []
        for item in checklist:
            status = str(item.get("status", ""))
            text = " ".join(str(item.get(key, "")) for key in ("item", "owner", "status")).lower()
            if status.lower() == "blocked" or ("electrical" in text and "blocked" in text):
                blockers.append(
                    {
                        "item": item.get("item", "Commissioning item"),
                        "owner": item.get("owner", "Commissioning"),
                        "reason": "Blocked dependency requires trade coordination.",
                        "recommendation": "Run a same-day dependency review and assign a recovery owner.",
                    }
                )

        ai = generate_json(
            f"Checklist: {checklist}\nBlockers: {blockers}",
            system="Return JSON with mitigation_options and recovery_recommendations for EPC commissioning.",
        ) or {}
        return {
            "checklist": checklist,
            "blockers": blockers,
            "mitigation_options": ai.get("mitigation_options", ["Prioritize blocked systems before IST readiness review."]),
            "recovery_recommendations": ai.get("recovery_recommendations", ["Escalate cross-trade blockers within 24 hours."]),
        }
