COMPLIANCE_PROMPT = """
You are an EPC Compliance Engineer.

Compare the Specification and Vendor documents.

Find:
- Missing items
- Mismatches
- Non-compliance
- Critical risks

Return the answer in JSON format.

Specification:
{spec}

Vendor:
{vendor}
"""