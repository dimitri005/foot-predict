import pandas as pd

from src.models.ml_pipeline import FEATURE_COLUMNS, build_inference_features, build_pre_match_dataset


def test_pre_match_features_do_not_use_current_match_goals():
    base = pd.DataFrame(
        [
            {
                "date": "2026-01-01",
                "home_team": "A",
                "away_team": "B",
                "home_goals": 5,
                "away_goals": 0,
            },
            {
                "date": "2026-01-08",
                "home_team": "B",
                "away_team": "A",
                "home_goals": 1,
                "away_goals": 1,
            },
        ]
    )
    changed = base.copy()
    changed.loc[1, ["home_goals", "away_goals"]] = [8, 0]

    left = build_pre_match_dataset(base)
    right = build_pre_match_dataset(changed)

    assert left.loc[1, FEATURE_COLUMNS].equals(right.loc[1, FEATURE_COLUMNS])
    assert left.loc[1, "target"] != right.loc[1, "target"]


def test_pre_match_dataset_has_all_model_features():
    matches = pd.DataFrame(
        [
            {
                "date": f"2026-01-{day:02d}",
                "home_team": "A" if day % 2 else "B",
                "away_team": "B" if day % 2 else "A",
                "home_goals": day % 3,
                "away_goals": (day + 1) % 3,
            }
            for day in range(1, 9)
        ]
    )
    result = build_pre_match_dataset(matches)
    assert set(FEATURE_COLUMNS).issubset(result.columns)


def test_inference_features_use_completed_history():
    history = pd.DataFrame(
        [
            {"date": "2026-01-01", "home_team": "A", "away_team": "B", "home_goals": 3, "away_goals": 0},
            {"date": "2026-01-08", "home_team": "B", "away_team": "A", "home_goals": 0, "away_goals": 1},
        ]
    )
    upcoming = pd.DataFrame(
        [{"date": "2026-01-15", "home_team": "A", "away_team": "B", "league": "Test"}]
    )
    result = build_inference_features(history, upcoming)
    assert set(FEATURE_COLUMNS).issubset(result.columns)
    assert result.loc[0, "home_form_5"] > result.loc[0, "away_form_5"]
