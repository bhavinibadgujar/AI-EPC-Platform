import os
from dotenv import load_dotenv
from google import genai
from google.genai.errors import ClientError

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file")

try:
    # Create Gemini client
    client = genai.Client(api_key=GEMINI_API_KEY)

    # Send a simple prompt
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Reply with one short sentence saying hello."
    )

    print("✅ Gemini Connected Successfully!")
    print("Response:", response.text)

except ClientError as e:
    print("❌ Gemini API Error")
    print(e)

except Exception as e:
    print("❌ Unexpected Error")
    print(e)