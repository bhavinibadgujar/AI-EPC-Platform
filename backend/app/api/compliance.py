"""Compliance analysis endpoint."""

import logging
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.report import Report
from app.services.report_generator import ReportGenerator
from app.services.ai_analysis import run_ai_compliance_analysis  # your existing Gemini logic
from app.schemas.report import AnalyzeResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/compliance", tags=["compliance"])

report_generator = ReportGenerator()


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_compliance(
    project_id: int,
    project_name: str,
    specification_file: UploadFile = File(...),
    vendor_file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> AnalyzeResponse:
    """
    Run AI compliance analysis on the uploaded PDFs, generate a report,
    persist it, and return the result to the client.
    """
    try:
        # 1. Run existing AI comparison logic (your current implementation)
        analysis_result = await run_ai_compliance_analysis(specification_file, vendor_file)

        compliance_score = analysis_result["compliance_score"]
        deviations = analysis_result["deviations"]
        recommendations = analysis_result.get("recommendations", [])
        summary = analysis_result.get("summary", {})

    except Exception as exc:
        logger.exception("AI analysis failed: %s", exc)
        raise HTTPException(status_code=500, detail="AI analysis failed.")

    # 2. Generate report — failure here must not break the analysis response
    report_id = None
    report_url = None
    try:
        timestamp = datetime.now()
        filepath = report_generator.generate(
            project_id=project_id,
            project_name=project_name,
            compliance_score=compliance_score,
            deviations=deviations,
            recommendations=recommendations,
            specification_filename=specification_file.filename,
            vendor_filename=vendor_file.filename,
            analysis_summary=summary,
            timestamp=timestamp,
        )

        report = Report(
            project_id=project_id,
            filename=filepath.split("/")[-1],
            filepath=filepath,
            compliance_score=compliance_score,
            created_at=timestamp,
        )
        db.add(report)
        db.commit()
        db.refresh(report)

        report_id = report.id
        report_url = f"/api/reports/{report.id}/download"

    except Exception as exc:
        logger.exception("Report generation/storage failed: %s", exc)
        return AnalyzeResponse(
            success=False,
            message="Failed to generate report.",
            score=compliance_score,
            deviations=deviations,
            recommendations=recommendations,
        )

    return AnalyzeResponse(
        success=True,
        score=compliance_score,
        deviations=deviations,
        recommendations=recommendations,
        report_id=report_id,
        report_url=report_url,
    )