from google import genai
from google.genai.errors import ClientError
from backend.core.config import GEMINI_API_KEY
import time

client = genai.Client(api_key=GEMINI_API_KEY)

def generate_content_with_retry(model, contents, max_retries=3):
    """
    Generate content with retry logic for quota exceeded errors.
    
    Args:
        model: Model name (e.g., "gemini-2.0-flash")
        contents: Content to send to the model
        max_retries: Maximum number of retry attempts
        
    Returns:
        Response object or None if all retries fail
        
    Raises:
        ClientError: If error is not a quota issue
    """
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            response = client.models.generate_content(
                model=model,
                contents=contents
            )
            return response
        except ClientError as e:
            # Check if it's a quota exceeded error (429)
            error_str = str(e)
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str or "quota" in error_str.lower():
                retry_count += 1
                if retry_count < max_retries:
                    wait_time = 2 ** retry_count  # Exponential backoff: 2s, 4s, 8s
                    print(f"Quota exceeded. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    raise ClientError(
                        429,
                        {
                            "error": {
                                "message": "Free tier quota exhausted after retries. "
                                          "Please wait a few hours for daily quota to reset or upgrade your API key with billing."
                            }
                        },
                        None
                    )
            else:
                raise
    
    return None


