from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from backend.app.core.gemini_client import generate_json

from .analyzer import ScheduleAnalyzer
from .comparator import ScheduleComparator
from .cpm import CriticalPathMethod
from .graph_builder import ScheduleGraphBuilder
from .parser import ScheduleParser

SCHEDULE_SYSTEM = """You are an EPC schedule risk analyst. Return JSON with keys summary, top_risks, and executive_recommendation."""


class ScheduleAgent:
    def __init__(self) -> None:
        self.parser = ScheduleParser()

    def analyze(self, file_path: str | Path) -> dict[str, Any]:
        activities, relationships = self.parser.parse(str(file_path))
        graph_builder = ScheduleGraphBuilder()
        graph_builder.build_graph(activities, relationships)
        if graph_builder.has_cycle():
            raise ValueError("Schedule contains circular dependencies.")

        cpm = CriticalPathMethod(graph_builder)
        cpm_result = cpm.calculate()
        analysis = ScheduleAnalyzer(activities).analyze()
        risks = ScheduleComparator(activities).compare()
        risk_list = [risk.model_dump(mode="json") for risk in risks]
        schedule_data = {
            "project_duration": cpm_result["project_duration"],
            "critical_path": cpm_result["critical_path"],
            "analysis": analysis,
            "risks": risk_list,
        }
        narrative = generate_json(json.dumps(schedule_data, indent=2), system=SCHEDULE_SYSTEM) or {
            "summary": f"{len(cpm_result['critical_path'])} activities are on the critical path.",
            "top_risks": [risk.get("description", "") for risk in risk_list[:3]],
            "executive_recommendation": "Focus daily controls review on critical and near-critical activities.",
        }
        return {**schedule_data, "ai_summary": narrative}

    def run(self, file_path: str | Path) -> dict[str, Any]:
        return self.analyze(file_path)
