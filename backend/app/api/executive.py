from fastapi import APIRouter

from app.schemas.executive import ExecutiveSummary
from app.services.executive_service import get_executive_summary

router = APIRouter(
    prefix="/executive-summary",
    tags=["Executive Summary"],
)


@router.get("/", response_model=ExecutiveSummary)
def get_summary():
    return get_executive_summary()