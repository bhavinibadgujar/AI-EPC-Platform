from fastapi import APIRouter

from app.schemas.timeline import TimelineItem
from app.services.timeline_service import get_timeline_data

router = APIRouter(
    prefix="/timeline",
    tags=["Timeline"],
)


@router.get("/", response_model=list[TimelineItem])
def get_timeline():
    return get_timeline_data()