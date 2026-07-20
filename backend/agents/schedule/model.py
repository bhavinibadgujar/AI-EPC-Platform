from datetime import date, datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


# -------------------------------------------------------
# Enums
# -------------------------------------------------------

class RelationshipType(str, Enum):
    FS = "FS"   # Finish to Start
    SS = "SS"   # Start to Start
    FF = "FF"   # Finish to Finish
    SF = "SF"   # Start to Finish


class Severity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class RiskType(str, Enum):
    CRITICAL_PATH = "Critical Path"
    RESOURCE_OVERLOAD = "Resource Overload"
    PROCUREMENT_DELAY = "Procurement Delay"
    DEADLINE_RISK = "Deadline Risk"
    FLOAT_RISK = "Float Risk"
    GENERAL = "General"


# -------------------------------------------------------
# Resource Model
# -------------------------------------------------------

class Resource(BaseModel):
    resource_id: str
    resource_name: str
    role: Optional[str] = None
    capacity: float = 0.0
    assigned_units: float = 0.0


# -------------------------------------------------------
# Activity Model
# -------------------------------------------------------

class Activity(BaseModel):
    activity_id: str
    activity_name: str

    duration_days: int

    planned_start: Optional[date] = None
    planned_finish: Optional[date] = None

    actual_start: Optional[date] = None
    actual_finish: Optional[date] = None

    remaining_duration: int = 0

    total_float: float = 0
    free_float: float = 0

    percent_complete: float = Field(default=0, ge=0, le=100)

    calendar: Optional[str] = None

    resources: List[Resource] = []

    is_critical: bool = False


# -------------------------------------------------------
# Relationship Model
# -------------------------------------------------------

class Relationship(BaseModel):
    predecessor: str
    successor: str

    relationship_type: RelationshipType = RelationshipType.FS

    lag: int = 0


# -------------------------------------------------------
# Critical Path Model
# -------------------------------------------------------

class CriticalPath(BaseModel):
    activities: List[str]
    total_duration: int
    project_finish_date: Optional[date] = None


# -------------------------------------------------------
# Resource Conflict
# -------------------------------------------------------

class ResourceConflict(BaseModel):
    resource_name: str
    activity_ids: List[str]

    overallocated_by: float

    severity: Severity


# -------------------------------------------------------
# Risk Finding
# -------------------------------------------------------

class RiskFinding(BaseModel):
    risk_id: str

    risk_type: RiskType

    severity: Severity

    activity_id: Optional[str] = None
    activity_name: Optional[str] = None

    description: str

    recommendation: str

    confidence: float = Field(default=1.0, ge=0, le=1)

    deterministic: bool = True

    source: str = "Rule Engine"


# -------------------------------------------------------
# AI Narrative
# -------------------------------------------------------

class RiskNarrative(BaseModel):
    summary: str

    top_risks: List[str]

    executive_recommendation: str

    confidence: float = Field(default=1.0, ge=0, le=1)


# -------------------------------------------------------
# Final Report
# -------------------------------------------------------

class ScheduleRiskReport(BaseModel):
    project_name: str

    analysis_date: datetime = Field(default_factory=datetime.utcnow)

    critical_path: CriticalPath

    near_critical_path: List[str] = []

    resource_conflicts: List[ResourceConflict] = []

    risk_findings: List[RiskFinding] = []

    overall_risk: Severity

    delay_probability: float = Field(default=0, ge=0, le=100)

    estimated_delay_days: int = 0

    narrative: Optional[RiskNarrative] = None