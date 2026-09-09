import pandas as pd
import numpy as np


def _safe_float(value, default=0.0):
    try:
        return float(value)
    except Exception:
        return float(default)


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add realistic football context features from a match-level row.

    The idea is to extend the sample data toward the feature set described in
    the project guide: home/away form, xG deltas, goals deltas and a stability/risk index.
    """
    out = df.copy()

    # Ensure columns are present safely.
    for col in ["home_form", "away_form", "home_xg", "away_xg", "home_goals", "away_goals"]:
        if col not in out.columns:
            out[col] = 0.0

    # Home and away base strengths.
    out["home_team_strength"] = out["home_form"] + out["home_xg"] * 2
    out["away_team_strength"] = out["away_form"] + out["away_xg"] * 2

    # Feature derivatives used by the model.
    out["home_form_delta"] = out["home_form"] - out["away_form"]
    out["away_form_delta"] = out["away_form"] - out["home_form"]
    out["xg_delta"] = out["home_xg"] - out["away_xg"]
    out["goals_delta"] = out["home_goals"] - out["away_goals"]
    out["strength_delta"] = out["home_team_strength"] - out["away_team_strength"]

    # Goal expectation and football-style pressure signal.
    out["goal_expectation_home"] = 1.2 + (out["strength_delta"] / 8)
    out["goal_expectation_away"] = 1.0 - (out["strength_delta"] / 10)

    # Team match-up risk: lower risk if xG and forms are close.
    form_gap = out["home_form"] - out["away_form"]
    xg_gap = out["home_xg"] - out["away_xg"]
    score_gap = out["home_goals"] - out["away_goals"]
    out["risk_index"] = np.clip(
        (abs(form_gap) * 0.12 + abs(xg_gap) * 0.22 + abs(score_gap) * 0.10),
        0.0,
        1.0,
    )

    # Derby indicator: the dataset may include rivalry names later.
    derby_teams = {"Arsenal", "Chelsea", "Liverpool", "Manchester City", "Real Madrid", "Barcelona"}
    out["is_derby"] = out.apply(
        lambda row: row["home_team"] in derby_teams and row["away_team"] in derby_teams,
        axis=1,
    ).astype(bool)

    # Round fragile columns and ensure input is numeric.
    for numeric_col in [
        "home_form_delta",
        "away_form_delta",
        "xg_delta",
        "goals_delta",
        "strength_delta",
        "goal_expectation_home",
        "goal_expectation_away",
        "risk_index",
    ]:
        out[numeric_col] = pd.to_numeric(out[numeric_col], errors="coerce").fillna(0.0)

    return out
