from fastapi import APIRouter

from app.schemas.risk import RiskResponse
from app.services.risk_service import get_risk_data

router = APIRouter(
    prefix="/risks",
    tags=["Risk"],
)


@router.get("/", response_model=list[RiskResponse])
def get_risks():
    return get_risk_data()