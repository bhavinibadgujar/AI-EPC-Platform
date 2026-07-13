from pydantic import BaseModel
from typing import Optional, Dict, Any


# -------- Chat --------
class AIChatRequest(BaseModel):
    project_id: int
    query: str


class AIChatResponse(BaseModel):
    response: str


# -------- Compliance --------
class AIComplianceRequest(BaseModel):
    project_id: int


# -------- Risk --------
class AIRiskRequest(BaseModel):
    project_id: int


# -------- Executive Brief --------
class AIExecutiveBriefRequest(BaseModel):
    project_id: int


# -------- Simulation --------
class AISimulationRequest(BaseModel):
    project_id: int
    scenario: str


# -------- Consequence Engine --------
class AIConsequenceRequest(BaseModel):
    project_id: int
    event: str