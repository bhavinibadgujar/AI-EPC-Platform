from fastapi import FastAPI

from backend.api.routes.schedule import router as schedule_router
from backend.api.routes.compliance import router as compliance_router

app = FastAPI(
    title="AI EPC Platform"
)

@app.get("/")
def home():
    return {
        "message": "AI EPC Backend is running"
    }

app.include_router(
    schedule_router,
    prefix="/ai",
    tags=["Schedule"]
)

app.include_router(
    compliance_router,
    prefix="/ai",
    tags=["Compliance"]
)