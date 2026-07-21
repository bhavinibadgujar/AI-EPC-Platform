from datetime import datetime
from pydantic import BaseModel


class ReportOut(BaseModel):
    id: int
    project_id: int
    filename: str
    compliance_score: float
    created_at: datetime

    class Config:
        orm_mode = True


class AnalyzeResponse(BaseModel):
    success: bool
    score: float | None = None
    deviations: list | None = None
    recommendations: list | None = None
    report_id: int | None = None
    report_url: str | None = None
    message: str | None = None