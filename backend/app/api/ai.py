from fastapi import APIRouter, UploadFile, File
from backend.app.services.ai_service import (
    compliance_with_ai,
    schedule_risk_with_ai
)

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


# ----------------------------
# Compliance
# ----------------------------
@router.post("/compliance")
async def compliance_analysis(
    specification: UploadFile = File(...),
    vendor: UploadFile = File(...)
):
    return await compliance_with_ai(
        specification,
        vendor
    )


# ----------------------------
# Schedule Risk
# ----------------------------
@router.post("/schedule-risk")
async def schedule_risk_analysis(
    file: UploadFile = File(...)
):
    return await schedule_risk_with_ai(file)


# ----------------------------
# Chat (Placeholder)
# ----------------------------
@router.post("/chat")
async def ai_chat():
    return {
        "status": "success",
        "message": "Chat AI endpoint is not integrated yet."
    }


# ----------------------------
# Risk (Placeholder)
# ----------------------------
@router.post("/risk")
async def risk_analysis():
    return {
        "status": "success",
        "message": "Risk AI endpoint is not integrated yet."
    }


# ----------------------------
# Executive Brief (Placeholder)
# ----------------------------
@router.post("/executive-brief")
async def executive_brief():
    return {
        "status": "success",
        "message": "Executive Brief endpoint is not integrated yet."
    }


# ----------------------------
# Simulation (Placeholder)
# ----------------------------
@router.post("/simulation")
async def simulation():
    return {
        "status": "success",
        "message": "Simulation endpoint is not integrated yet."
    }


# ----------------------------
# Consequence Engine (Placeholder)
# ----------------------------
@router.post("/consequence-engine")
async def consequence_engine():
    return {
        "status": "success",
        "message": "Consequence Engine endpoint is not integrated yet."
    }