import json
from typing import Any, Dict


class ScheduleValidator:
    """
    Validates Gemini responses for the Schedule Risk Engine.
    """

    @staticmethod
    def validate_json(response: str) -> Dict[str, Any]:
        """
        Convert Gemini response into Python dictionary.
        """

        try:
            return json.loads(response)

        except json.JSONDecodeError:
            raise ValueError("Gemini returned invalid JSON.")

    @staticmethod
    def validate_required_fields(data: Dict[str, Any]) -> bool:
        """
        Ensure required fields exist.
        """

        required_fields = [
            "summary",
            "top_risks",
            "recommendations"
        ]

        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

        return True

    @staticmethod
    def validate_confidence(data: Dict[str, Any]) -> bool:
        """
        Validate confidence score.
        """

        confidence = data.get("confidence", 1.0)

        if confidence < 0 or confidence > 1:
            raise ValueError(
                "Confidence must be between 0 and 1."
            )

        return True

    @staticmethod
    def validate(response: str):
        """
        Complete validation pipeline.
        """

        data = ScheduleValidator.validate_json(response)

        ScheduleValidator.validate_required_fields(data)

        ScheduleValidator.validate_confidence(data)

        return data