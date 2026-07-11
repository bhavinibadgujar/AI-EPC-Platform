from agents.schedule.validator import ScheduleValidator

response = """
{
    "summary":"Project is healthy",
    "top_risks":["Electrical","Procurement"],
    "recommendations":["Increase manpower"],
    "confidence":0.92
}
"""

result = ScheduleValidator.validate(response)

print(result)