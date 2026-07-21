from fastapi import APIRouter, HTTPException
from app.db.session import get_db
from app.db.models import ConsequenceRecord

router = APIRouter(prefix="/api/consequence", tags=["Consequence"])

@router.get("/{compliance_flag_id}")
async def get_consequence(compliance_flag_id: str):
    db = next(get_db())
    record = db.query(ConsequenceRecord).filter_by(compliance_flag_id=compliance_flag_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="No consequence record for this flag")
    return {
        "affected_trades": record.affected_trades,
        "affected_milestones": record.affected_milestones,
        "severity_score": record.severity_score,
        "suggested_action": record.suggested_action
    }