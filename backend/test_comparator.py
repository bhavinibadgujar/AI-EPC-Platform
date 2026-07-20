from agents.schedule.model import Activity
from agents.schedule.comparator import ScheduleComparator

activities = [

    Activity(
        activity_id="A101",
        activity_name="Foundation",
        duration_days=5,
        total_float=0,
        percent_complete=100,
        is_critical=True
    ),

    Activity(
        activity_id="A102",
        activity_name="Columns",
        duration_days=15,
        total_float=2,
        percent_complete=10,
        is_critical=False
    ),

    Activity(
        activity_id="A103",
        activity_name="Roof",
        duration_days=40,
        total_float=10,
        percent_complete=80,
        is_critical=False
    )

]

engine = ScheduleComparator(activities)

risks = engine.compare()

for risk in risks:
    print(risk.model_dump())