from agents.schedule.model import Activity
from agents.schedule.analyzer import ScheduleAnalyzer

activities = [

    Activity(
        activity_id="A1",
        activity_name="Foundation",
        duration_days=5,
        total_float=0,
        is_critical=True
    ),

    Activity(
        activity_id="A2",
        activity_name="Columns",
        duration_days=3,
        total_float=2,
        is_critical=False
    ),

    Activity(
        activity_id="A3",
        activity_name="Roof",
        duration_days=4,
        total_float=8,
        is_critical=False
    )
]

analyzer = ScheduleAnalyzer(activities)

print(analyzer.analyze())