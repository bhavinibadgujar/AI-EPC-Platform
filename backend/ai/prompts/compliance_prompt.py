COMPLIANCE_CHECK_PROMPT = """
You are a compliance analyst for an EPC (Engineering, Procurement, Construction) project.

SPEC DOCUMENT (source of truth):
{spec_text}

SUBMITTAL DOCUMENT (to be checked against the spec):
{submittal_text}

Compare the submittal against the spec clause by clause. For every deviation you find,
output a finding. Do not invent clauses that are not present in the spec text.

Respond ONLY as JSON matching this exact schema:
{{
  "flags": [
    {{
      "clause_reference": "string, e.g. 'Section 4.2 - UPS Output Voltage'",
      "expected_value": "string, what the spec requires",
      "submitted_value": "string, what the submittal actually states",
      "severity": "one of: low, medium, high, critical",
      "confidence_score": "float between 0 and 1",
      "explanation": "one sentence on why this is a deviation"
    }}
  ]
}}

If there are no deviations, return {{"flags": []}}.
"""