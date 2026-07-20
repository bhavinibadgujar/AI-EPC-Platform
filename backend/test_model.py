from agents.schedule.model import Activity

activity = Activity(
    activity_id="A101",
    activity_name="Foundation Work",
    duration_days=10,
    percent_complete=30
)

print(activity.model_dump())