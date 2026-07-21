from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


def _truthy(value: str | None) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    app_name: str = "EPC Orbit AI Control Tower"
    ai_epc_use_gemini: bool = False
    gemini_api_key: str | None = None
    database_url: str | None = None
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:5174,http://127.0.0.1:5174"

    @property
    def parsed_cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    def validate_ai(self) -> None:
        if self.ai_epc_use_gemini and not self.gemini_api_key:
            raise RuntimeError("GEMINI_API_KEY is required when AI_EPC_USE_GEMINI=1")


@lru_cache
def get_settings() -> Settings:
    settings = Settings(
        ai_epc_use_gemini=_truthy(os.getenv("AI_EPC_USE_GEMINI")),
        gemini_api_key=os.getenv("GEMINI_API_KEY"),
        database_url=os.getenv("DATABASE_URL"),
        cors_origins=os.getenv("CORS_ORIGINS") or Settings.cors_origins,
    )
    settings.validate_ai()
    return settings


settings = get_settings()
GEMINI_API_KEY = settings.gemini_api_key
DATABASE_URL = settings.database_url
