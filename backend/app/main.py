from fastapi import FastAPI

from app.db.database import Base, engine
import app.db.models

# Import the router
from app.api.projects import router as project_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI EPC Platform API",
    description="Backend API for the AI EPC Platform",
    version="1.0.0"
)

# Register the Projects router
app.include_router(project_router)


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