import pandas as pd
from datetime import datetime, timedelta


def load_sample_data() -> pd.DataFrame:
    """Return a small synthetic football dataset for the MVP demo."""

    rows = [
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
        },
        {
            "match_id": "M002",
            "league": "Premier League",
            "season": "2025/26",
            "date": "2026-09-09",
            "home_team": "Liverpool",
            "away_team": "Manchester City",
            "home_goals": 3,
            "away_goals": 2,
            "home_form": 8,
            "away_form": 6,
            "home_xg": 2.3,
            "away_xg": 1.8,
        },
        {
            "match_id": "M003",
            "league": "La Liga",
            "season": "2025/26",
            "date": "2026-09-10",
            "home_team": "Real Madrid",
            "away_team": "Barcelona",
            "home_goals": 1,
            "away_goals": 1,
            "home_form": 7,
            "away_form": 7,
            "home_xg": 1.8,
            "away_xg": 1.9,
        },
        {
            "match_id": "M004",
            "league": "La Liga",
            "season": "2025/26",
            "date": "2026-09-11",
            "home_team": "Atletico Madrid",
            "away_team": "Sevilla",
            "home_goals": 2,
            "away_goals": 0,
            "home_form": 6,
            "away_form": 4,
            "home_xg": 1.6,
            "away_xg": 0.9,
        },
        {
            "match_id": "M005",
            "league": "Bundesliga",
            "season": "2025/26",
            "date": "2026-09-12",
            "home_team": "Bayern Munich",
            "away_team": "Borussia Dortmund",
            "home_goals": 4,
            "away_goals": 2,
            "home_form": 8,
            "away_form": 5,
            "home_xg": 2.6,
            "away_xg": 1.5,
        },
    ]

    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])
    return df
