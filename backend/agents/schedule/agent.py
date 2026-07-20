from backend.agents.schedule.parser import ScheduleParser
from backend.agents.schedule.graph_builder import ScheduleGraphBuilder
from backend.agents.schedule.cpm import CriticalPathMethod
from backend.agents.schedule.analyzer import ScheduleAnalyzer
from backend.agents.schedule.comparator import ScheduleComparator
from backend.agents.schedule.prompt import SCHEDULE_PROMPT
from backend.core.gemini import generate_content_with_retry
from backend.agents.schedule.prompt import SCHEDULE_PROMPT
import json

from backend.core.gemini import generate_content_with_retry


class ScheduleAgent:

    def __init__(self):
        self.parser = ScheduleParser()
        self.graph_builder = ScheduleGraphBuilder()

    def run(self, file_path: str):
        return self.analyze(file_path)

    def analyze(self, file_path: str):

        # -----------------------------
        # Step 1: Parse Schedule
        # -----------------------------
        activities, relationships = self.parser.parse(file_path)

        # -----------------------------
        # Step 2: Build Dependency Graph
        # -----------------------------
        self.graph_builder.build_graph(
            activities,
            relationships
        )

        # -----------------------------
        # Step 3: Critical Path
        # -----------------------------
        cpm = CriticalPathMethod(self.graph_builder)

        cpm_result = cpm.calculate()

        # -----------------------------
        # Step 4: Analyze Schedule
        # -----------------------------
        analyzer = ScheduleAnalyzer(activities)

        analysis = analyzer.analyze()

        # -----------------------------
        # Step 5: Generate Risks
        # -----------------------------
        comparator = ScheduleComparator(activities)

        risks = comparator.compare()

        risk_list = [risk.model_dump() for risk in risks]

        schedule_data = {
        "project_duration": cpm_result["project_duration"],
        "critical_path": cpm_result["critical_path"],
        "analysis": analysis,
        "risks": risk_list,
}

        risk_list = [risk.model_dump() for risk in risks]

        # -----------------------------
        # Step 6: Prepare data for AI
        # -----------------------------
        schedule_data = {
            "project_duration": cpm_result["project_duration"],
            "critical_path": cpm_result["critical_path"],
            "analysis": analysis,
            "risks": risk_list,
        }

        # -----------------------------
        # Step 7: Build Prompt
        # -----------------------------
        prompt = SCHEDULE_PROMPT.format(
        schedule_data=json.dumps(schedule_data, indent=2)
)

        response = generate_content_with_retry(
        model="gemini-2.0-flash",
        contents=prompt
)
        # -----------------------------
        # Step 8: Gemini Analysis
        # -----------------------------
        ai_summary = generate_content_with_retry(
            contents=prompt,
            model="gemini-2.5-flash"
        )

        # -----------------------------
        # Step 9: Return Final Response
        # -----------------------------
        return {
            "project_duration": cpm_result["project_duration"],
            "critical_path": cpm_result["critical_path"],
            "analysis": analysis,
            "risks": risk_list,
            "ai_summary": ai_summary,
        }