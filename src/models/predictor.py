"""Prediction service with a trained-model path and a safe baseline fallback."""

from __future__ import annotations

from pathlib import Path
from math import exp, factorial
from typing import Any

import numpy as np
import pandas as pd

from src.models.ml_pipeline import FEATURE_COLUMNS, load_model, predict_model


class FootballPredictor:
    """Expose a stable prediction API for Streamlit and automated clients."""

    def __init__(self, model_path: str | Path = "models/football_predictor.joblib") -> None:
        self.model_path = Path(model_path)
        self.model = load_model(self.model_path)

    @staticmethod
    def _legacy_probabilities(row: pd.Series | dict[str, Any]) -> dict[str, float]:
        get = row.get
        home_form = float(get("home_form", 0.0) or 0.0)
        away_form = float(get("away_form", 0.0) or 0.0)
        home_xg = float(get("home_xg", 1.2) or 1.2)
        away_xg = float(get("away_xg", 1.0) or 1.0)
        signal = 0.45 * (home_form - away_form) + 0.35 * (home_xg - away_xg)
        home = float(np.clip(0.38 + signal * 0.08, 0.05, 0.85))
        away = float(np.clip(0.28 - signal * 0.08, 0.05, 0.75))
        draw = max(0.05, 1.0 - home - away)
        values = np.array([home, draw, away], dtype=float)
        values /= values.sum()
        return {"home": float(values[0]), "draw": float(values[1]), "away": float(values[2])}

    def predict_proba(self, row: pd.Series | dict[str, Any]) -> dict[str, float]:
        if self.model is not None:
            adapted = dict(row)
            adapted.setdefault("home_elo", 1500.0)
            adapted.setdefault("away_elo", 1500.0)
            adapted.setdefault("elo_delta", 55.0)
            adapted.setdefault("home_form_5", adapted.get("home_form", 0.0))
            adapted.setdefault("away_form_5", adapted.get("away_form", 0.0))
            adapted.setdefault("home_goals_for_5", adapted.get("home_xg", 1.2))
            adapted.setdefault("away_goals_for_5", adapted.get("away_xg", 1.0))
            adapted.setdefault("home_goals_against_5", 1.2)
            adapted.setdefault("away_goals_against_5", 1.2)
            adapted.setdefault("home_home_points_5", 1.0)
            adapted.setdefault("away_away_points_5", 1.0)
            adapted.setdefault("rest_days_home", 14.0)
            adapted.setdefault("rest_days_away", 14.0)
            result = predict_model(self.model, pd.DataFrame([adapted])).iloc[0]
            return {
                "home": float(result["home_probability"]),
                "draw": float(result["draw_probability"]),
                "away": float(result["away_probability"]),
            }
        return self._legacy_probabilities(row)

    def predict(self, row: pd.Series | dict[str, Any]) -> dict[str, Any]:
        probabilities = self.predict_proba(row)
        markets = self._goal_markets(row)
        winner = max(probabilities, key=probabilities.get)
        confidence = probabilities[winner]
        confidence_label = "High" if confidence >= 0.65 else "Medium" if confidence >= 0.50 else "Low"
        return {
            "home_team": row.get("home_team", ""),
            "away_team": row.get("away_team", ""),
            "date": row.get("date"),
            "home_probability": probabilities["home"],
            "draw_probability": probabilities["draw"],
            "away_probability": probabilities["away"],
            "home_prob": probabilities["home"],
            "draw_prob": probabilities["draw"],
            "away_prob": probabilities["away"],
            "winner": winner,
            "confidence": confidence,
            "confidence_label": confidence_label,
            "model": "trained" if self.model is not None else "baseline",
            "markets": markets,
        }

    @staticmethod
    def _poisson_distribution(rate: float, maximum: int = 6) -> dict[int, float]:
        rate = float(np.clip(rate, 0.1, 5.0))
        probabilities = {goals: exp(-rate) * rate**goals / factorial(goals) for goals in range(maximum + 1)}
        tail = max(0.0, 1.0 - sum(probabilities.values()))
        probabilities[maximum] += tail
        return probabilities

    @staticmethod
    def _goal_rates(row: pd.Series | dict[str, Any]) -> tuple[float, float]:
        get = row.get
        home_attack = float(get("home_goals_for_5", get("home_xg", 1.2)) or 1.2)
        away_attack = float(get("away_goals_for_5", get("away_xg", 1.0)) or 1.0)
        home_defence = float(get("home_goals_against_5", 1.2) or 1.2)
        away_defence = float(get("away_goals_against_5", 1.2) or 1.2)
        home_rate = np.clip((home_attack + away_defence) / 2.0 + 0.15, 0.2, 4.0)
        away_rate = np.clip((away_attack + home_defence) / 2.0, 0.2, 4.0)
        return float(home_rate), float(away_rate)

    @classmethod
    def _goal_markets(cls, row: pd.Series | dict[str, Any]) -> dict[str, Any]:
        home_rate, away_rate = cls._goal_rates(row)
        home_distribution = cls._poisson_distribution(home_rate)
        away_distribution = cls._poisson_distribution(away_rate)
        score_probabilities = {
            (home_goals, away_goals): home_probability * away_probability
            for home_goals, home_probability in home_distribution.items()
            for away_goals, away_probability in away_distribution.items()
        }
        over_25 = sum(probability for (home, away), probability in score_probabilities.items() if home + away >= 3)
        btts_yes = sum(probability for (home, away), probability in score_probabilities.items() if home >= 1 and away >= 1)
        exact_scores = [
            {"score": f"{home}-{away}", "probability": probability}
            for (home, away), probability in sorted(score_probabilities.items(), key=lambda item: item[1], reverse=True)[:3]
        ]
        return {
            "expected_goals": {"home": home_rate, "away": away_rate, "total": home_rate + away_rate},
            "over_under_2_5": {
                "over": over_25,
                "under": 1.0 - over_25,
                "pick": "over" if over_25 >= 0.5 else "under",
            },
            "btts": {
                "yes": btts_yes,
                "no": 1.0 - btts_yes,
                "pick": "yes" if btts_yes >= 0.5 else "no",
            },
            "exact_score": exact_scores,
        }
