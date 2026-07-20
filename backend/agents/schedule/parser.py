import os
import pandas as pd
from xml.etree import ElementTree as ET

from .model import Activity, Relationship


class ScheduleParser:

    def parse(self, file_path: str):

        extension = os.path.splitext(file_path)[1].lower()

        if extension == ".csv":
            return self._parse_csv(file_path)

        elif extension in [".xlsx", ".xls"]:
            return self._parse_excel(file_path)

        elif extension == ".xml":
            return self._parse_xml(file_path)

        elif extension == ".xer":
            raise NotImplementedError(
                "Primavera XER parsing is not implemented yet."
            )

        else:
            raise ValueError("Unsupported file format.")

    # -------------------------------------

    def _parse_csv(self, file_path):

        df = pd.read_csv(file_path)

        return self._convert_dataframe(df)

    # -------------------------------------

    def _parse_excel(self, file_path):

        df = pd.read_excel(file_path)

        return self._convert_dataframe(df)

    # -------------------------------------

    def _parse_xml(self, file_path):

        tree = ET.parse(file_path)

        root = tree.getroot()

        activities = []
        relationships = []

        for activity in root.findall(".//Activity"):

            activities.append(
                Activity(
                    activity_id=activity.findtext("ID"),
                    activity_name=activity.findtext("Name"),
                    duration_days=int(activity.findtext("Duration")),
                )
            )

        return activities, relationships

    # -------------------------------------

    def _convert_dataframe(self, df):

        activities = []
        relationships = []

        for _, row in df.iterrows():

            activity = Activity(
                activity_id=str(row["Activity ID"]),
                activity_name=row["Activity Name"],
                duration_days=int(row["Duration"]),
            )

            activities.append(activity)

            predecessor = row.get("Predecessor")

            if pd.notna(predecessor):

                relationships.append(
                    Relationship(
                        predecessor=str(predecessor),
                        successor=str(row["Activity ID"]),
                    )
                )

        return activities, relationships