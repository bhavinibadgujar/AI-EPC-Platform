"""
Prompt templates for the Schedule Risk Engine.
These prompts are used by Gemini to generate
risk explanations and executive summaries.
"""


# ==========================================================
# Executive Summary Prompt
# ==========================================================

EXECUTIVE_SUMMARY_PROMPT = """
You are a Senior EPC Project Planning Engineer.

Analyze the schedule data below.

Generate:

1. Executive Summary
2. Overall Project Health
3. Top 5 Risks
4. Estimated Delay Probability
5. Recommendations

Return ONLY valid JSON.

Example:

{
    "summary": "...",
    "project_health": "...",
    "top_risks": [
        "...",
        "..."
    ],
    "delay_probability": 35,
    "recommendations": [
        "...",
        "..."
    ]
}

Schedule Data:

{schedule_data}
"""


# ==========================================================
# Risk Explanation Prompt
# ==========================================================

RISK_EXPLANATION_PROMPT = """
You are an EPC Construction Risk Expert.

Explain the following schedule risk.

Activity:

{activity}

Risk:

{risk}

Return ONLY JSON.

Example:

{
    "cause": "...",
    "impact": "...",
    "recommendation": "...",
    "severity": "HIGH"
}
"""


# ==========================================================
# Activity Analysis Prompt
# ==========================================================

ACTIVITY_ANALYSIS_PROMPT = """
Analyze this project activity.

Activity:

{activity}

Return ONLY JSON.

Example:

{
    "risk_level":"MEDIUM",
    "possible_delay":"Equipment delivery",
    "recommendation":"Monitor vendor progress"
}
"""


# ==========================================================
# Project Health Prompt
# ==========================================================

PROJECT_HEALTH_PROMPT = """
You are a Data Center EPC Planning Specialist.

Evaluate the schedule.

Project Summary:

{summary}

Return ONLY JSON.

{
    "health_score":90,
    "status":"GOOD",
    "major_issue":"Electrical work",
    "recommendation":"Increase workforce"
}
"""


# ==========================================================
# User Question Prompt
# ==========================================================

USER_QUERY_PROMPT = """
You are an AI EPC Copilot.

Answer the user's question using the project schedule.

Schedule:

{schedule}

Question:

{question}

Give a short professional answer.
"""


# ==========================================================
# Delay Prediction Prompt
# ==========================================================

DELAY_PREDICTION_PROMPT = """
You are a Project Controls Expert.

Predict the probability of schedule delay.

Schedule Information:

{schedule}

Return ONLY JSON.

{
    "delay_probability":45,
    "expected_delay_days":8,
    "reason":"Critical procurement delay",
    "recommendation":"Expedite vendor delivery"
}
"""