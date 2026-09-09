import math

from src.models.predictor import FootballPredictor


sample_row = {
    "match_id": "M001",
    "league": "Premier League",
    "season": "2025/26",
    "date": "2026-09-08",
    "home_team": "Arsenal",
    "away_team": "Chelsea",
    "home_goals": 2,
    "away_goals": 1,
    "home_form": 7,
    "away_form": 5,
    "home_xg": 1.9,
    "away_xg": 1.2,
}


def test_predictor_predict_proba_returns_normalized_probabilities():
    predictor = FootballPredictor()
    probabilities = predictor.predict_proba(sample_row)

    assert set(probabilities.keys()) == {"home", "draw", "away"}
    assert math.isclose(sum(probabilities.values()), 1.0, abs_tol=1e-9)
    assert all(0 <= p <= 1 for p in probabilities.values())


def test_predictor_predict_returns_prediction_payload():
    predictor = FootballPredictor()
    payload = predictor.predict(sample_row)

    assert payload["home_prob"] >= 0
    assert payload["draw_prob"] >= 0
    assert payload["away_prob"] >= 0
    assert "markets" in payload
    assert "over_under_2_5" in payload["markets"]
    assert "btts" in payload["markets"]
    assert len(payload["markets"]["exact_score"]) == 3
    assert math.isclose(payload["home_prob"] + payload["draw_prob"] + payload["away_prob"], 1.0, abs_tol=1e-9)
