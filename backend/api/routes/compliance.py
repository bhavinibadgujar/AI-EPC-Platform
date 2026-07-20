import os
import shutil

from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.agents.compliance.agent import ComplianceAgent

router = APIRouter()

agent = ComplianceAgent()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/compliance")
async def analyze_compliance(
    specification: UploadFile = File(...),
    vendor: UploadFile = File(...)
):
    try:
        # Save uploaded files
        spec_path = os.path.join(UPLOAD_DIR, specification.filename)
        vendor_path = os.path.join(UPLOAD_DIR, vendor.filename)

        with open(spec_path, "wb") as buffer:
            shutil.copyfileobj(specification.file, buffer)

        with open(vendor_path, "wb") as buffer:
            shutil.copyfileobj(vendor.file, buffer)

        # Analyze PDFs
        result = agent.analyze(spec_path, vendor_path)

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )