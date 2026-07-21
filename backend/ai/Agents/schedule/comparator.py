from .model import (
    Activity,
    RiskFinding,
    RiskType,
    Severity,
)


class ScheduleComparator:
    """
    Applies deterministic business rules
    to identify schedule risks.
    """

    def __init__(self, activities: list[Activity]):
        self.activities = activities

    def compare(self):
        risks = []

        for activity in self.activities:

            # --------------------------------
            # Critical Activity
            # --------------------------------
            if activity.is_critical:

                risks.append(
                    RiskFinding(
                        risk_id=f"RISK-{activity.activity_id}",
                        risk_type=RiskType.CRITICAL_PATH,
                        severity=Severity.HIGH,
                        activity_id=activity.activity_id,
                        activity_name=activity.activity_name,
                        description="Activity is on the Critical Path.",
                        recommendation="Monitor daily and avoid delays.",
                        deterministic=True,
                        source="Rule Engine"
                    )
                )

            # --------------------------------
            # Near Critical Activity
            # --------------------------------
            elif activity.total_float <= 3:

                risks.append(
                    RiskFinding(
                        risk_id=f"RISK-{activity.activity_id}",
                        risk_type=RiskType.FLOAT_RISK,
                        severity=Severity.MEDIUM,
                        activity_id=activity.activity_id,
                        activity_name=activity.activity_name,
                        description="Activity has very little float.",
                        recommendation="Closely monitor progress.",
                        deterministic=True,
                        source="Rule Engine"
                    )
                )

            # --------------------------------
            # Long Duration Activity
            # --------------------------------
            if activity.duration_days > 30:

                risks.append(
                    RiskFinding(
                        risk_id=f"LONG-{activity.activity_id}",
                        risk_type=RiskType.GENERAL,
                        severity=Severity.LOW,
                        activity_id=activity.activity_id,
                        activity_name=activity.activity_name,
                        description="Long duration activity.",
                        recommendation="Consider splitting into smaller tasks.",
                        deterministic=True,
                        source="Rule Engine"
                    )
                )

            # --------------------------------
            # Low Progress Warning
            # --------------------------------
            if (
                activity.percent_complete < 20
                and activity.duration_days > 10
            ):

                risks.append(
                    RiskFinding(
                        risk_id=f"PROGRESS-{activity.activity_id}",
                        risk_type=RiskType.DEADLINE_RISK,
                        severity=Severity.HIGH,
                        activity_id=activity.activity_id,
                        activity_name=activity.activity_name,
                        description="Progress is significantly behind.",
                        recommendation="Increase manpower or extend working hours.",
                        deterministic=True,
                        source="Rule Engine"
                    )
                )

        return risks