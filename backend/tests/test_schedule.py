from backend.agents.schedule.agent import ScheduleAgent

agent = ScheduleAgent()

result = agent.analyze("dataset/schedules/schedule_1.csv")

print(result)