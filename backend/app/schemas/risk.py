from pydantic import BaseModel


class RiskResponse(BaseModel):
    title: str
    severity: str
    status: str