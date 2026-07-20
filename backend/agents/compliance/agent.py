from backend.agents.utils.pdf_reader import extract_text
from backend.agents.compliance.prompt import COMPLIANCE_PROMPT
from backend.core.gemini import client, generate_content_with_retry
from google.genai.errors import ClientError



class ComplianceAgent:

    def analyze(self, spec_pdf, vendor_pdf):

        # Read PDFs
        spec_text = extract_text(spec_pdf)
        vendor_text = extract_text(vendor_pdf)
        prompt = f"""
{COMPLIANCE_PROMPT}

Client Specification:
{spec_text}

Vendor Submittal:
{vendor_text}
"""
        try:
            response = generate_content_with_retry(
                model="gemini-2.0-flash",
                contents=prompt,
                max_retries=3
            )

            return {
                "status": "success",
                "result": response.text
            }

        except ClientError as e:
            error_str = str(e)
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str or "quota" in error_str.lower():
                print("Gemini API quota exceeded. Free tier limit reached.")
                return {
                    "status": "quota_exceeded",
                    "error": "Gemini API quota exceeded. Please upgrade your API key with billing or wait for daily quota to reset."
                }
            else:
                print("Gemini Error:", e)
                return {
                    "status": "error",
                "error": str(e)
            }