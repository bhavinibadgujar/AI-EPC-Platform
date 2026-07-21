IMPACT_MAP = {
    "UPS": {"trades": ["Electrical", "Commissioning"], "milestones": ["IST"]},
    "Switchgear": {"trades": ["Electrical"], "milestones": ["Energization"]},
    "Cooling Tower": {"trades": ["Mechanical", "Commissioning"], "milestones": ["IST"]},
    "Generator": {"trades": ["Electrical", "Mechanical"], "milestones": ["Load Bank Test"]},
    "Fire Suppression": {"trades": ["Mechanical", "Safety"], "milestones": ["Life Safety Sign-off"]},
}

SEVERITY_WEIGHTS = {"low": 0.2, "medium": 0.4, "major": 0.7, "high": 0.7, "critical": 1.0}


class ConsequenceEngine:
    def calculate(self, flag: dict) -> dict:
        category = self._match_category(" ".join(str(flag.get(key, "")) for key in ("parameter", "clause_reference", "requirement")))
        impact = IMPACT_MAP.get(category, {"trades": ["Project Controls"], "milestones": ["Next Gate Review"]})
        severity = str(flag.get("severity", "medium")).lower()
        confidence = float(flag.get("confidence", flag.get("confidence_score", 0.5)) or 0.5)
        return {
            "affected_trades": impact["trades"],
            "affected_milestones": impact["milestones"],
            "severity_score": round(SEVERITY_WEIGHTS.get(severity, 0.4) * confidence, 2),
            "suggested_action": self._suggest_action(category, severity),
        }

    def _match_category(self, text: str) -> str:
        for category in IMPACT_MAP:
            if category.lower() in text.lower():
                return category
        return "Unknown"

    def _suggest_action(self, category: str, severity: str) -> str:
        if severity in ("high", "critical", "major"):
            return f"Escalate to {category} lead immediately and hold related milestone pending review."
        return f"Flag to {category} lead for review during next coordination meeting."
