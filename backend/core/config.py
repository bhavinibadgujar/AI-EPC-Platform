from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Read the Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Optional: Check if the key exists
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")