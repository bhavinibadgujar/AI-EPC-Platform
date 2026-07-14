import os
import time
from google import genai
from google.genai.errors import ClientError
from backend.core.config import GEMINI_API_KEY

# Create client only if API key is present
client = None
if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)


def _mock_response(contents):
    """Return a lightweight mock response used when the API is unavailable."""
    return {
        "mock": True,
        "text": "AI unavailable: quota exceeded or key not configured. This is a fallback response.",
        "input_preview": contents if isinstance(contents, str) else str(contents),
    }


def generate_content_with_retry(model=None, contents=None, max_retries=3, allow_fallback=True):
    """
    Generate content with retry logic for quota errors. On quota exhaustion this
    function will return a sensible fallback (instead of raising) when
    `allow_fallback` is True. This keeps unit tests and local runs stable.

    Args:
        model: Model name (optional)
        contents: Content to send to the model
        max_retries: Maximum number of retry attempts
        allow_fallback: If True, return a mock response when quota is exhausted

    Returns:
        Model response object (from the SDK) or a fallback dict when the API
        cannot be reached due to quota or missing API key.
    """

    # If client isn't configured, return fallback immediately
    if client is None:
        if allow_fallback:
            print("Gemini client not configured. Returning fallback response.")
            return _mock_response(contents)
        raise ClientError(
            401,
            {"error": {"message": "GEMINI_API_KEY not configured."}},
            None,
        )

    retry_count = 0
    while retry_count < max_retries:
        try:
            response = client.models.generate_content(
                model=model,
                contents=contents,
            )
            return response
        except ClientError as e:
            error_str = str(e)

            # If it's clearly a quota issue, try retries with backoff
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str or "quota" in error_str.lower():
                retry_count += 1
                if retry_count < max_retries:
                    wait_time = 2 ** retry_count
                    print(f"Quota exceeded. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                # final retry failed — return fallback when allowed
                if allow_fallback:
                    print("Free tier quota exhausted after retries. Returning fallback response.")
                    return _mock_response(contents)
                raise

            # Model not found or other client errors — return fallback when allowed
            if allow_fallback:
                print(f"Gemini client error ({error_str}). Returning fallback response.")
                return _mock_response(contents)

            # Otherwise, re-raise the exception
            raise

    # Shouldn't reach here, but return fallback for safety
    if allow_fallback:
        return _mock_response(contents)
    return None


