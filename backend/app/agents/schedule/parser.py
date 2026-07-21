import os
import pandas as pd
from xml.etree import ElementTree as ET

from .model import Activity, Relationship


def _pick(row, *names, default=None):
    for name in names:
        if name in row and pd.notna(row[name]):
            return row[name]
    lowered = {str(key).strip().lower(): key for key in row.keys()}
    for name in names:
        key = lowered.get(name.strip().lower())
        if key is not None and pd.notna(row[key]):
            return row[key]
    return default


class ScheduleParser:
    def parse(self, file_path: str):
        extension = os.path.splitext(file_path)[1].lower()
        if extension == ".csv":
            return self._parse_csv(file_path)
        if extension in [".xlsx", ".xls"]:
            return self._parse_excel(file_path)
        if extension == ".xml":
            return self._parse_xml(file_path)
        if extension == ".xer":
            raise NotImplementedError("Primavera XER parsing is not implemented yet.")
        raise ValueError("Unsupported file format.")

    def _parse_csv(self, file_path):
        return self._convert_dataframe(pd.read_csv(file_path))

    def _parse_excel(self, file_path):
        return self._convert_dataframe(pd.read_excel(file_path))

    def _parse_xml(self, file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()
        activities = []
        for activity in root.findall(".//Activity"):
            activities.append(
                Activity(
                    activity_id=activity.findtext("ID"),
                    activity_name=activity.findtext("Name"),
                    duration_days=int(activity.findtext("Duration") or 1),
                )
            )
        return activities, []

    def _convert_dataframe(self, df):
        activities = []
        relationships = []

        for _, row in df.iterrows():
            activity_id = str(_pick(row, "Activity ID", "activity_id", "id", "activity", default=len(activities) + 1))
            activity_name = str(_pick(row, "Activity Name", "activity_name", "name", "activity", default=f"Activity {activity_id}"))
            duration = int(float(_pick(row, "Duration", "duration", "duration_days", default=1) or 1))
            total_float = float(_pick(row, "Total Float", "total_float", "float", default=0) or 0)
            percent_complete = float(_pick(row, "Percent Complete", "percent_complete", "% Complete", default=0) or 0)

            activities.append(
                Activity(
                    activity_id=activity_id,
                    activity_name=activity_name,
                    duration_days=duration,
                    total_float=total_float,
                    percent_complete=percent_complete,
                )
            )

            predecessor = _pick(row, "Predecessor", "predecessor", "predecessors")
            if pd.notna(predecessor):
                for pred in str(predecessor).replace(";", ",").split(","):
                    pred = pred.strip()
                    if pred:
                        relationships.append(Relationship(predecessor=pred, successor=activity_id))

        return activities, relationships
