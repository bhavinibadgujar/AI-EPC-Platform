from datetime import date
from pydantic import BaseModel


class TimelineItem(BaseModel):
    phase: str
    start: date
    end: date
    progress: int