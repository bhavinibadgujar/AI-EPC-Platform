"""Report download and history endpoints."""

import os
import logging
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.report import Report
from app.schemas.report import ReportOut

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.get("/{report_id}/download")
async def download_report(report_id: int, db: Session = Depends(get_db)) -> FileResponse:
    """Stream the generated PDF report back to the client."""
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found.")

    if not os.path.exists(report.filepath):
        logger.error("Report file missing on disk: %s", report.filepath)
        raise HTTPException(status_code=404, detail="Report file missing on disk.")

    return FileResponse(
        path=report.filepath,
        media_type="application/pdf",
        filename=report.filename,
        headers={"Content-Disposition": f'attachment; filename="{report.filename}"'},
    )


@router.get("/project/{project_id}", response_model=list[ReportOut])
async def list_project_reports(project_id: int, db: Session = Depends(get_db)):
    """Return report history for a given project, most recent first."""
    return (
        db.query(Report)
        .filter(Report.project_id == project_id)
        .order_by(Report.created_at.desc())
        .all()
    )