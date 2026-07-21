from pydantic import BaseModel
from typing import List, Optional

class ComplianceRequest(BaseModel):
    project_id: str
    document_id: str
    project_context: Optional[str] = ""

class ComplianceFinding(BaseModel):
    issue: str
    standard_ref: str
    severity: str
    recommendation: str

class ComplianceResponse(BaseModel):
    findings: List[ComplianceFinding]
    overall_compliance_score: int