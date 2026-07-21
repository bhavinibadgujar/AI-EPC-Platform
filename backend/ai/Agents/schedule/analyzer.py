from .model import Activity


class ScheduleAnalyzer:
    """
    Analyze schedule after CPM calculation.
    """

    def __init__(self, activities: list[Activity]):
        self.activities = activities

    def get_critical_activities(self):
        """
        Activities with zero or negative float.
        """
        return [
            activity
            for activity in self.activities
            if activity.is_critical
        ]

    def get_near_critical_activities(self, threshold: int = 3):
        """
        Activities with small positive float.
        """
        return [
            activity
            for activity in self.activities
            if 0 < activity.total_float <= threshold
        ]

    def calculate_schedule_health(self):
        """
        Calculate schedule health score.
        """

        total = len(self.activities)

        if total == 0:
            return 100

        critical = len(self.get_critical_activities())

        health = 100 - ((critical / total) * 100)

        return round(max(0, health), 2)

    def generate_summary(self):
        """
        Return schedule summary.
        """

        return {
            "total_activities": len(self.activities),
            "critical_activities": len(
                self.get_critical_activities()
            ),
            "near_critical_activities": len(
                self.get_near_critical_activities()
            ),
            "schedule_health": self.calculate_schedule_health(),
        }

    def analyze(self):
        """
        Complete schedule analysis.
        """

        return {
            "summary": self.generate_summary(),
            "critical_path": [
                activity.activity_id
                for activity in self.get_critical_activities()
            ],
            "near_critical": [
                activity.activity_id
                for activity in self.get_near_critical_activities()
            ]
        }