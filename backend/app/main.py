from fastapi import FastAPI

from app.db.database import Base, engine
import app.db.models

from app.api import (
    projects,
    document,
    dashboard,
    timeline,
    risk,
    executive,
    ai
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI EPC Platform API",
    description="Backend API for the AI EPC Platform",
    version="1.0.0"
)

app.include_router(projects.router)
app.include_router(document.router)
app.include_router(dashboard.router)
app.include_router(timeline.router)
app.include_router(risk.router)
app.include_router(executive.router)
app.include_router(ai.router)


@app.get("/")
def root():
    return {
        "status": "success",
        "message": "AI EPC Platform Backend is Running 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }