from backend.app.core.gemini_client import mock_json


def test_gemini_mock_is_deterministic():
    result = mock_json("hello")

    assert result["mock"] is True
    assert "answer" in result
