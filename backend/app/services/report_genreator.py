"""
Report Generator Service
Generates professional PDF compliance reports using ReportLab.
"""

import os
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    Frame,
    PageTemplate,
    BaseDocTemplate,
)
from reportlab.platypus.flowables import HRFlowable

logger = logging.getLogger(__name__)

REPORTS_DIR = os.path.join("backend", "storage", "reports")


class ReportGenerator:
    """Generates a PDF compliance report from AI analysis results."""

    def __init__(self, output_dir: str = REPORTS_DIR):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.styles = getSampleStyleSheet()
        self._register_custom_styles()

    def _register_custom_styles(self) -> None:
        """Add custom paragraph styles used throughout the report."""
        self.styles.add(ParagraphStyle(
            name="CoverTitle", fontSize=26, leading=32, alignment=TA_CENTER,
            textColor=colors.HexColor("#1F2937"), spaceAfter=12, fontName="Helvetica-Bold",
        ))
        self.styles.add(ParagraphStyle(
            name="CoverSubtitle", fontSize=16, leading=20, alignment=TA_CENTER,
            textColor=colors.HexColor("#4B5563"), spaceAfter=6,
        ))
        self.styles.add(ParagraphStyle(
            name="SectionHeader", fontSize=15, leading=18, spaceBefore=18, spaceAfter=8,
            textColor=colors.HexColor("#111827"), fontName="Helvetica-Bold",
        ))
        self.styles.add(ParagraphStyle(
            name="GaugeScore", fontSize=42, alignment=TA_CENTER, fontName="Helvetica-Bold",
        ))
        self.styles.add(ParagraphStyle(
            name="GaugeLabel", fontSize=12, alignment=TA_CENTER,
            textColor=colors.HexColor("#6B7280"),
        ))
        self.styles.add(ParagraphStyle(
            name="BulletItem", fontSize=10.5, leading=15, leftIndent=14,
        ))
        self.styles.add(ParagraphStyle(
            name="FooterText", fontSize=8, alignment=TA_CENTER,
            textColor=colors.HexColor("#9CA3AF"),
        ))

    # ------------------------------------------------------------------ #
    # Public entry point
    # ------------------------------------------------------------------ #
    def generate(
        self,
        project_id: int,
        project_name: str,
        compliance_score: float,
        deviations: List[Dict[str, Any]],
        recommendations: List[str],
        specification_filename: str,
        vendor_filename: str,
        analysis_summary: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None,
    ) -> str:
        """
        Build the PDF report and save it to disk.

        Returns:
            The absolute filepath of the generated PDF.
        """
        timestamp = timestamp or datetime.now()
        analysis_summary = analysis_summary or {}

        filename = self._build_filename(project_id, timestamp)
        filepath = os.path.join(self.output_dir, filename)

        try:
            doc = SimpleDocTemplate(
                filepath, pagesize=A4,
                topMargin=2 * cm, bottomMargin=2 * cm,
                leftMargin=2 * cm, rightMargin=2 * cm,
            )

            story = []
            story += self._build_cover(project_name, timestamp)
            story.append(PageBreak())
            story += self._build_executive_summary(compliance_score, deviations, analysis_summary)
            story += self._build_gauge(compliance_score)
            story.append(PageBreak())
            story += self._build_deviation_register(deviations)
            story += self._build_recommendations(recommendations)
            story += self._build_risk_summary(deviations)
            story += self._build_footer()

            doc.build(story)
            logger.info("Report generated successfully: %s", filepath)
            return filepath

        except Exception as exc:
            logger.exception("Failed to generate report for project %s: %s", project_id, exc)
            raise

    # ------------------------------------------------------------------ #
    # Section builders
    # ------------------------------------------------------------------ #
    def _build_filename(self, project_id: int, timestamp: datetime) -> str:
        ts = timestamp.strftime("%Y_%m_%d_%H%M%S")
        return f"report_{project_id}_{ts}.pdf"

    def _build_cover(self, project_name: str, timestamp: datetime) -> list:
        return [
            Spacer(1, 5 * cm),
            Paragraph("AI EPC Orbit", self.styles["CoverTitle"]),
            Paragraph("Compliance Analysis Report", self.styles["CoverSubtitle"]),
            Spacer(1, 2 * cm),
            Paragraph(f"Project: {project_name}", self.styles["Normal"]),
            Paragraph(f"Date: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}", self.styles["Normal"]),
            Paragraph("Generated by: AI EPC Orbit Compliance Engine", self.styles["Normal"]),
        ]

    def _build_executive_summary(self, score: float, deviations: list, summary: dict) -> list:
        severities = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        for d in deviations:
            sev = str(d.get("severity", "")).lower()
            if sev in severities:
                severities[sev] += 1

        rows = [
            ["Metric", "Value"],
            ["Compliance Score", f"{score}%"],
            ["Total Clauses", str(summary.get("total_clauses", "-"))],
            ["Matched Clauses", str(summary.get("matched_clauses", "-"))],
            ["Deviations", str(len(deviations))],
            ["Critical Issues", str(severities["critical"])],
            ["High Issues", str(severities["high"])],
            ["Medium Issues", str(severities["medium"])],
            ["Low Issues", str(severities["low"])],
        ]

        table = Table(rows, colWidths=[8 * cm, 6 * cm])
        table.setStyle(self._default_table_style(header_bg="#111827"))

        return [
            Paragraph("Executive Summary", self.styles["SectionHeader"]),
            table,
            Spacer(1, 0.5 * cm),
        ]

    def _build_gauge(self, score: float) -> list:
        color = self._score_color(score)
        return [
            Spacer(1, 0.5 * cm),
            Paragraph("Compliance Score", self.styles["GaugeLabel"]),
            Paragraph(f'<font color="{color}">{score}%</font>', self.styles["GaugeScore"]),
            Spacer(1, 0.5 * cm),
        ]

    def _build_deviation_register(self, deviations: list) -> list:
        header = ["Clause", "Specification", "Vendor Submitted", "Status",
                  "Severity", "Impact", "Recommendation", "Source"]
        rows = [header]

        for d in deviations:
            rows.append([
                Paragraph(str(d.get("clause", "-")), self.styles["BulletItem"]),
                Paragraph(str(d.get("specification", "-")), self.styles["BulletItem"]),
                Paragraph(str(d.get("vendor_submitted", "-")), self.styles["BulletItem"]),
                Paragraph(str(d.get("status", "-")), self.styles["BulletItem"]),
                Paragraph(str(d.get("severity", "-")), self.styles["BulletItem"]),
                Paragraph(str(d.get("impact", "-")), self.styles["BulletItem"]),
                Paragraph(str(d.get("recommendation", "-")), self.styles["BulletItem"]),
                Paragraph(str(d.get("source", "-")), self.styles["BulletItem"]),
            ])

        col_widths = [2.2 * cm, 2.6 * cm, 2.6 * cm, 1.8 * cm, 2 * cm, 2.6 * cm, 3 * cm, 2 * cm]
        table = Table(rows, colWidths=col_widths, repeatRows=1)
        table.setStyle(self._default_table_style(header_bg="#374151", font_size=8))

        return [
            Paragraph("Deviation Register", self.styles["SectionHeader"]),
            table,
            Spacer(1, 0.5 * cm),
        ]

    def _build_recommendations(self, recommendations: list) -> list:
        items = [Paragraph("AI Recommendations", self.styles["SectionHeader"])]
        if not recommendations:
            items.append(Paragraph("No recommendations generated.", self.styles["BulletItem"]))
        for rec in recommendations:
            items.append(Paragraph(f"• {rec}", self.styles["BulletItem"]))
        items.append(Spacer(1, 0.5 * cm))
        return items

    def _build_risk_summary(self, deviations: list) -> list:
        critical = [d for d in deviations if str(d.get("severity", "")).lower() == "critical"]

        rows = [["Critical Risks", "Business Impact", "Recommended Action"]]
        if critical:
            for d in critical:
                rows.append([
                    Paragraph(str(d.get("clause", "-")), self.styles["BulletItem"]),
                    Paragraph(str(d.get("impact", "-")), self.styles["BulletItem"]),
                    Paragraph(str(d.get("recommendation", "-")), self.styles["BulletItem"]),
                ])
        else:
            rows.append(["None identified", "-", "-"])

        table = Table(rows, colWidths=[5 * cm, 5.5 * cm, 5.5 * cm])
        table.setStyle(self._default_table_style(header_bg="#7F1D1D", font_size=9))

        return [
            Paragraph("Risk Summary", self.styles["SectionHeader"]),
            table,
            Spacer(1, 1 * cm),
        ]

    def _build_footer(self) -> list:
        return [
            HRFlowable(width="100%", color=colors.HexColor("#E5E7EB")),
            Spacer(1, 0.2 * cm),
            Paragraph("Generated by EPC Orbit AI", self.styles["FooterText"]),
        ]

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #
    @staticmethod
    def _score_color(score: float) -> str:
        if score >= 80:
            return "#15803D"
        if score >= 50:
            return "#B45309"
        return "#B91C1C"

    @staticmethod
    def _default_table_style(header_bg: str, font_size: int = 9) -> TableStyle:
        return TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(header_bg)),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), font_size),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F9FAFB")]),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ])