import os

import httpx
from dotenv import load_dotenv
from fastapi import HTTPException, UploadFile

load_dotenv()

AI_BASE_URL = os.getenv("AI_BASE_URL")


async def post_request(endpoint: str, **kwargs):
    if not AI_BASE_URL:
        raise HTTPException(
            status_code=500,
            detail="AI_BASE_URL is not configured."
        )

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                f"{AI_BASE_URL}{endpoint}",
                **kwargs
            )

        response.raise_for_status()

        return response.json()

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=e.response.text
        )

    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="AI service is unavailable."
        )


# ----------------------------
# Compliance AI
# ----------------------------
async def compliance_with_ai(
    specification: UploadFile,
    vendor: UploadFile
):
    specification_content = await specification.read()
    vendor_content = await vendor.read()

    files = {
        "specification": (
            specification.filename,
            specification_content,
            specification.content_type,
        ),
        "vendor": (
            vendor.filename,
            vendor_content,
            vendor.content_type,
        ),
    }

    return await post_request(
        "/ai/compliance",
        files=files
    )


# ----------------------------
# Schedule Risk AI
# ----------------------------
async def schedule_risk_with_ai(
    file: UploadFile
):
    file_content = await file.read()

    files = {
        "file": (
            file.filename,
            file_content,
            file.content_type,
        )
    }

    return await post_request(
        "/ai/schedule-risk",
        files=files
    )