from sqlalchemy.orm import Session
from backend.app.db.models import Project, Document


def get_dashboard_data(db: Session):
    total_projects = db.query(Project).count()
    total_documents = db.query(Document).count()

    completed_projects = 0
    active_projects = total_projects
    high_risks = 0
    budget_used = 72

    return {
        "total_projects": total_projects,
        "completed_projects": completed_projects,
        "active_projects": active_projects,
        "total_documents": total_documents,
        "high_risks": high_risks,
        "budget_used": budget_used,
    }