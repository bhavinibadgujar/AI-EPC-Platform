from __future__ import annotations

import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

logger = logging.getLogger("epc.db")
ROOT_DIR = Path(__file__).resolve().parents[2]
SQLITE_URL = f"sqlite:///{ROOT_DIR / 'ai_epc_platform.db'}"
REQUESTED_DATABASE_URL = os.getenv("DATABASE_URL")

Base = declarative_base()


def _connect_args(url: str) -> dict:
    return {"check_same_thread": False} if url.startswith("sqlite") else {}


def _create_engine_with_fallback():
    if REQUESTED_DATABASE_URL:
        candidate = create_engine(REQUESTED_DATABASE_URL, pool_pre_ping=True)
        try:
            with candidate.connect():
                logger.info("Connected to configured database.")
            return candidate, REQUESTED_DATABASE_URL
        except SQLAlchemyError as exc:
            logger.warning("Configured database unavailable, falling back to SQLite: %s", exc)

    sqlite_engine = create_engine(SQLITE_URL, connect_args=_connect_args(SQLITE_URL))
    return sqlite_engine, SQLITE_URL


engine, DATABASE_URL = _create_engine_with_fallback()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    from backend.app.db import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
