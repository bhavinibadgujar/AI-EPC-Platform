from pydantic import BaseModel

class DashboardResponse(BaseModel):
    total_projects: int
    completed_projects: int
    active_projects: int
    total_documents: int
    high_risks: int
    budget_used: int