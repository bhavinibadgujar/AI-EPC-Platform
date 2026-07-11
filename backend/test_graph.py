from agents.schedule.graph_builder import ScheduleGraphBuilder
from agents.schedule.model import Activity, Relationship

activities = [
    Activity(
        activity_id="A1",
        activity_name="Foundation",
        duration_days=5,
    ),
    Activity(
        activity_id="A2",
        activity_name="Columns",
        duration_days=4,
    ),
    Activity(
        activity_id="A3",
        activity_name="Roof",
        duration_days=3,
    ),
]

relationships = [
    Relationship(
        predecessor="A1",
        successor="A2",
    ),
    Relationship(
        predecessor="A2",
        successor="A3",
    ),
]

builder = ScheduleGraphBuilder()

builder.build_graph(
    activities,
    relationships,
)

print("Start Activities:", builder.get_start_nodes())
print("End Activities:", builder.get_end_nodes())
print("Execution Order:", builder.topological_sort())
print("Contains Cycle:", builder.has_cycle())