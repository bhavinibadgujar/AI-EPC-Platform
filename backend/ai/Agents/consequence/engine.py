IMPACT_MAP = {
    "UPS": {"trades": ["Electrical", "Commissioning"], "milestones": ["IST"]},
    "Switchgear": {"trades": ["Electrical"], "milestones": ["Energization"]},
    "Cooling Tower": {"trades": ["Mechanical", "Commissioning"], "milestones": ["IST"]},
    "Generator": {"trades": ["Electrical", "Mechanical"], "milestones": ["Load Bank Test"]},
    "Fire Suppression": {"trades": ["Mechanical", "Safety"], "milestones": ["Life Safety Sign-off"]},
}

SEVERITY_WEIGHTS = {"low": 0.2, "medium": 0.4, "high": 0.7, "critical": 1.0}

class ConsequenceEngine:
    def calculate(self, flag: dict) -> dict:
        category = self._match_category(flag.get("clause_reference", ""))
        impact = IMPACT_MAP.get(category, {"trades": ["Unknown"], "milestones": ["Unknown"]})

        severity_weight = SEVERITY_WEIGHTS.get(flag.get("severity", "medium"), 0.4)
        confidence = flag.get("confidence_score", 0.5)
        severity_score = round(severity_weight * confidence, 2)

        return {
            "affected_trades": impact["trades"],
            "affected_milestones": impact["milestones"],
            "severity_score": severity_score,
            "suggested_action": self._suggest_action(category, flag.get("severity", "medium"))
        }

    def _match_category(self, clause_reference: str) -> str:
        for category in IMPACT_MAP:
            if category.lower() in clause_reference.lower():
                return category
        return "Unknown"

    def _suggest_action(self, category: str, severity: str) -> str:
        if severity in ("high", "critical"):
            return f"Escalate to {category} lead immediately and hold related milestone pending review."
        return f"Flag to {category} lead for review during next coordination meeting."