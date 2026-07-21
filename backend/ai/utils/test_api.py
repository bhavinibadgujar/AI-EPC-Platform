from google import genai
from backend.config import GEMINI_API_KEY

print("API Key Loaded:", GEMINI_API_KEY[:10] + "...")

client = genai.Client(api_key=GEMINI_API_KEY)

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents="Say hello in one sentence."
    )

    print("\nSUCCESS!")
    print(response.text)

except Exception as e:
    print("\nERROR!")
    print(e)
    