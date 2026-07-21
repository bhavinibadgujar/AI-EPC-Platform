from app.ai.gemini import generate_json
from app.ai.prompts.executive_prompts import EXECUTIVE_BRIEF_PROMPT

class ExecutiveAgent:
    def generate_brief(self, flags: list[dict], rfis: list[dict]) -> str:
        flags_summary = "\n".join(
            f"- [{f['severity'].upper()}] {f['clause_reference']}: {f['explanation']}"
            for f in flags[:5]
        ) or "None"

        rfis_summary = "\n".join(
            f"- {r['title']} (open since {r['created_at']})"
            for r in rfis[:5]
        ) or "None"

        prompt = EXECUTIVE_BRIEF_PROMPT.format(flags_summary=flags_summary, rfis_summary=rfis_summary)
        result = generate_json(prompt)
        return result.get("brief", "")