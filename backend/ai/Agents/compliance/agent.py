from app.ai.gemini import generate_json
from app.ai.prompts.compliance_prompts import COMPLIANCE_CHECK_PROMPT

class ComplianceAgent:
    def check(self, spec_text: str, submittal_text: str) -> dict:
        prompt = COMPLIANCE_CHECK_PROMPT.format(
            spec_text=spec_text,
            submittal_text=submittal_text
        )
        result = generate_json(prompt)
        return self._validate(result)

    def _validate(self, result: dict) -> dict:
        flags = result.get("flags", [])
        cleaned = []
        for f in flags:
            cleaned.append({
                "clause_reference": f.get("clause_reference", "Unspecified"),
                "expected_value": f.get("expected_value", ""),
                "submitted_value": f.get("submitted_value", ""),
                "severity": f.get("severity", "medium"),
                "confidence_score": float(f.get("confidence_score", 0.5)),
                "explanation": f.get("explanation", "")
            })
        return {"flags": cleaned}