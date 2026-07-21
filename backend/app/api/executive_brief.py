from fastapi import APIRouter
from app.ai.agents.executive.agent import ExecutiveAgent
from app.db.session import get_db
from app.db.models import ComplianceFlagRecord, RFIRecord  # adjust to your models

router = APIRouter(prefix="/api/executive-brief", tags=["Executive Brief"])
agent = ExecutiveAgent()

_cache = {}  # simple in-memory cache: {project_id: brief_text} — swap for Redis later if needed

@router.get("/{project_id}")
async def get_brief(project_id: str, regenerate: bool = False):
    if not regenerate and project_id in _cache:
        return {"brief": _cache[project_id], "cached": True}

    db = next(get_db())
    flags = (
        db.query(ComplianceFlagRecord)
        .filter_by(project_id=project_id)
        .order_by(ComplianceFlagRecord.confidence_score.desc())
        .limit(5)
        .all()
    )
    rfis = db.query(RFIRecord).filter_by(project_id=project_id, status="open").limit(5).all()

    brief_text = agent.generate_brief(
        flags=[f.__dict__ for f in flags],
        rfis=[r.__dict__ for r in rfis]
    )
    _cache[project_id] = brief_text
    return {"brief": brief_text, "cached": False}