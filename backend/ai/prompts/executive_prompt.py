EXECUTIVE_BRIEF_PROMPT = """
You are writing a plain-English executive brief for a project stakeholder who has no time
to read raw data. Summarize the state of the project in 4-6 sentences based only on the
data below. Be direct about risk, don't pad with filler.

TOP COMPLIANCE FLAGS (by severity):
{flags_summary}

OPEN RFIs:
{rfis_summary}

Respond as JSON:
{{"brief": "the 4-6 sentence summary"}}
"""