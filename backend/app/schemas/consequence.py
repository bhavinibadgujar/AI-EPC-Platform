from pydantic import BaseModel
from typing import List

class ConsequenceResponse(BaseModel):
    affected_trades: List[str]
    affected_milestones: List[str]
    severity_score: float
    suggested_action: str