from .agent import ScheduleAgent


class ScheduleService:

    def __init__(self):
        self.agent = ScheduleAgent()

    def analyze_schedule(self, file_path: str):
        return self.agent.run(file_path)