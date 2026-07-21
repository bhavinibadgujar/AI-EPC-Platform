from backend.app.core.gemini_client import generate_json, mock_json


def test_gemini_wrapper_returns_none_when_disabled():
    assert generate_json("Say Hello from Gemini!") is None


def test_gemini_mock_response_shape():
    result = mock_json("Say Hello from Gemini!")

    assert result["mock"] is True
    assert result["answer"]
