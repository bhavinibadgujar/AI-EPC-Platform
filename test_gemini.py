from google import genai
from google.genai.errors import ClientError
from dotenv import load_dotenv
import os
import time

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

max_retries = 2
retry_count = 0

while retry_count < max_retries:
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents="Reply with only the word: Hello"
        )
        print(response.text)
        break
    except ClientError as e:
        # Check if it's a quota exceeded error (429)
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e) or "quota" in str(e).lower():
            retry_count += 1
            if retry_count < max_retries:
                wait_time = 1  # Use 1 second for testing
                print(f"Quota exceeded. Retrying in {wait_time} second... (Attempt {retry_count}/{max_retries})")
                time.sleep(wait_time)
            else:
                print(f"✓ Error handled: Gemini API quota exceeded after {max_retries} attempts.")
                print("\nSolution: The free tier quota has been exhausted. You can:")
                print("1. ⏱️  Wait a few hours for the daily quota to reset")
                print("2. 💳 Upgrade your API key with billing at https://ai.google.dev")
                print("\nYour code will now handle this gracefully in production.")
        else:
            print(f"Error: {e}")
            break
    except Exception as e:
        print(f"Unexpected error: {e}")
        break

