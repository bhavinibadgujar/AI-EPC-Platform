from backend.app.agents.consequence.engine import ConsequenceEngine


def test_consequence_engine_maps_ups_flag():
    result = ConsequenceEngine().calculate({"parameter": "UPS battery autonomy", "severity": "Critical", "confidence": 0.9})

    assert "Electrical" in result["affected_trades"]
    assert result["severity_score"] == 0.9
