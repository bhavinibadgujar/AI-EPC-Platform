import os
import json
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate(prompt: str, model: str = "gemini-2.0-flash", temperature: float = 0.2) -> str:
    """Plain text generation."""
    instance = genai.GenerativeModel(model)
    response = instance.generate_content(prompt, generation_config={"temperature": temperature})
    return response.text

def generate_json(prompt: str, model: str = "gemini-2.0-flash", temperature: float = 0.1) -> dict:
    """Generation with strict JSON output. Use for compliance/risk/executive endpoints."""
    instance = genai.GenerativeModel(
        model,
        generation_config={"temperature": temperature, "response_mime_type": "application/json"}
    )
    response = instance.generate_content(prompt)
    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        cleaned = response.text.strip().removeprefix("```json").removesuffix("```").strip()
        return json.loads(cleaned)

def embed(text: str) -> list[float]:
    result = genai.embed_content(model="models/text-embedding-004", content=text)
    return result["embedding"]