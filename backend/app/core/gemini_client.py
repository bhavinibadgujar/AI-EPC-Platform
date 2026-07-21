from __future__ import annotations

import hashlib
import json
import re
import time
from typing import Any

from backend.app.core.config import settings

_CACHE: dict[str, dict[str, Any]] = {}
_MODELS = ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-flash-8b"]


def mock_json(prompt: str, reason: str = "Gemini disabled or unavailable") -> dict[str, Any]:
    return {
        "mock": True,
        "summary": reason,
        "answer": "AI unavailable: using deterministic project analysis.",
        "citations": [],
        "brief": "AI unavailable: using deterministic executive summary.",
        "input_preview": prompt[:500],
    }


def generate_json(prompt: str, system: str = "", temperature: float = 0.1) -> dict[str, Any] | None:
    if not settings.ai_epc_use_gemini or not settings.gemini_api_key:
        return None

    cache_key = hashlib.sha256(f"{system}\n{prompt[:4000]}".encode("utf-8")).hexdigest()
    if cache_key in _CACHE:
        return _CACHE[cache_key]

    try:
        from google import genai as google_genai
        from google.genai import types as genai_types
    except Exception:
        return None

    client = google_genai.Client(api_key=settings.gemini_api_key)
    full_prompt = f"{system}\n\n{prompt}" if system else prompt

    for model_name in _MODELS:
        for attempt in range(3):
            try:
                resp = client.models.generate_content(
                    model=model_name,
                    contents=full_prompt,
                    config=genai_types.GenerateContentConfig(
                        temperature=temperature,
                        response_mime_type="application/json",
                    ),
                )
                raw = (getattr(resp, "text", "") or "").strip()
                if raw.startswith("```"):
                    raw = re.sub(r"^```[a-zA-Z]*\n?", "", raw)
                    raw = re.sub(r"\n?```$", "", raw)
                data = json.loads(raw)
                _CACHE[cache_key] = data
                return data
            except Exception as exc:
                text = str(exc)
                if "429" in text or "quota" in text.lower() or "RESOURCE_EXHAUSTED" in text:
                    time.sleep(2**attempt)
                    continue
                break
    return None
