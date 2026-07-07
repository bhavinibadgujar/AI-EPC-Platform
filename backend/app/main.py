from fastapi import FastAPI

from app.db.database import Base, engine
import app.db.models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI EPC Platform API",
    description="Backend API for the AI EPC Platform",
    version="1.0.0"
)


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