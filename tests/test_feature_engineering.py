import pandas as pd

from src.features.feature_engineering import add_features


sample_df = pd.DataFrame([
    {
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
])


def test_add_features_adds_expected_columns_and_stability_bounds():
    features = add_features(sample_df)

    expected_cols = {
        "home_form_delta",
        "away_form_delta",
        "xg_delta",
        "goals_delta",
        "strength_delta",
        "goal_expectation_home",
        "goal_expectation_away",
        "is_derby",
        "risk_index",
    }

    missing = expected_cols.difference(features.columns)
    assert not missing

    assert isinstance(features["risk_index"].iloc[0], float)
    assert features["risk_index"].iloc[0] >= 0
    assert features["risk_index"].iloc[0] <= 1
