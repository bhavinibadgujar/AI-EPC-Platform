from .parser import ScheduleParser
from .graph_builder import ScheduleGraphBuilder
from .cpm import CriticalPathMethod
from .analyzer import ScheduleAnalyzer
from .comparator import ScheduleComparator


class ScheduleAgent:

    def __init__(self):

        self.parser = ScheduleParser()
        self.graph_builder = ScheduleGraphBuilder()

    def run(self, file_path: str):

        # -----------------------------
        # Step 1 : Parse Schedule File
        # -----------------------------
        activities, relationships = self.parser.parse(file_path)

        # -----------------------------
        # Step 2 : Build Graph
        # -----------------------------
        graph = self.graph_builder.build_graph(
            activities,
            relationships
        )

        # -----------------------------
        # Step 3 : Run Critical Path
        # -----------------------------
        cpm = CriticalPathMethod(self.graph_builder)

        cpm_result = cpm.calculate()

        # -----------------------------
        # Step 4 : Analyze Schedule
        # -----------------------------
        analyzer = ScheduleAnalyzer(activities)

        analysis = analyzer.analyze()

        # -----------------------------
        # Step 5 : Detect Risks
        # -----------------------------
        comparator = ScheduleComparator(activities)

        risks = comparator.compare()

        # -----------------------------
        # Step 6 : Final Result
        # -----------------------------
        result = {
            "project_duration": cpm_result["project_duration"],
            "critical_path": cpm_result["critical_path"],
            "analysis": analysis,
            "risks": [
                risk.model_dump()
                for risk in risks
            ]
        }

        return result