"""Compatibility entry point for the consolidated FastAPI app.

Preferred command:
    uvicorn backend.app.main:app --reload

Legacy command still works:
    uvicorn backend.main:app --reload
"""

from backend.app.main import app
