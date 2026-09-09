"""Leakage-safe training and inference utilities for football 1X2 models."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import joblib
import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import accuracy_score, balanced_accuracy_score, log_loss
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

LOGGER = logging.getLogger(__name__)

MODEL_VERSION = "1.1.0"
TARGET = "target"
FEATURE_COLUMNS = [
    "home_elo",
    "away_elo",
    "elo_delta",
    "home_form_5",
    "away_form_5",
    "home_goals_for_5",
    "away_goals_for_5",
    "home_goals_against_5",
    "away_goals_against_5",
    "home_home_points_5",
    "away_away_points_5",
    "rest_days_home",
    "rest_days_away",
]
LABELS = {0: "away", 1: "draw", 2: "home"}


@dataclass
class TeamState:
    elo: float = 1500.0
    results: list[int] | None = None
    goals_for: list[int] | None = None
    goals_against: list[int] | None = None
    home_points: list[int] | None = None
    away_points: list[int] | None = None
    last_date: pd.Timestamp | None = None

    def __post_init__(self) -> None:
        self.results = [] if self.results is None else self.results
        self.goals_for = [] if self.goals_for is None else self.goals_for
        self.goals_against = [] if self.goals_against is None else self.goals_against
        self.home_points = [] if self.home_points is None else self.home_points
        self.away_points = [] if self.away_points is None else self.away_points


def _state(states: dict[str, TeamState], team: str) -> TeamState:
    if team not in states:
        states[team] = TeamState()
    return states[team]


def _mean(values: Iterable[float], default: float = 0.0) -> float:
    values = list(values)
    return float(np.mean(values)) if values else default


def build_pre_match_dataset(matches: pd.DataFrame) -> pd.DataFrame:
    """Create features using only information available before each match.

    The function sorts chronologically and updates team state only after the
    current row has been emitted, preventing target leakage.
    """
    required = {"date", "home_team", "away_team", "home_goals", "away_goals"}
    missing = required - set(matches.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    frame = matches.copy()
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce", utc=True)
    frame = frame.dropna(subset=["date", "home_team", "away_team", "home_goals", "away_goals"])
    frame = frame.sort_values("date", kind="stable").reset_index(drop=True)
    states: dict[str, TeamState] = {}
    rows: list[dict[str, object]] = []

    for _, match in frame.iterrows():
        home_name = str(match["home_team"])
        away_name = str(match["away_team"])
        home = _state(states, home_name)
        away = _state(states, away_name)
        date = match["date"]

        def rest_days(team: TeamState) -> float:
            if team.last_date is None:
                return 14.0
            return max(0.0, min(60.0, float((date - team.last_date).days)))

        rows.append(
            {
                "date": date,
                "league": match.get("league", "unknown"),
                "home_team": home_name,
                "away_team": away_name,
                "home_elo": home.elo,
                "away_elo": away.elo,
                "elo_delta": home.elo + 55.0 - away.elo,
                "home_form_5": _mean(home.results[-5:], 0.0),
                "away_form_5": _mean(away.results[-5:], 0.0),
                "home_goals_for_5": _mean(home.goals_for[-5:], 1.2),
                "away_goals_for_5": _mean(away.goals_for[-5:], 1.0),
                "home_goals_against_5": _mean(home.goals_against[-5:], 1.2),
                "away_goals_against_5": _mean(away.goals_against[-5:], 1.2),
                "home_home_points_5": _mean(home.home_points[-5:], 1.0),
                "away_away_points_5": _mean(away.away_points[-5:], 1.0),
                "rest_days_home": rest_days(home),
                "rest_days_away": rest_days(away),
                TARGET: int(
                    2
                    if float(match["home_goals"]) > float(match["away_goals"])
                    else 0
                    if float(match["home_goals"]) < float(match["away_goals"])
                    else 1
                ),
            }
        )

        home_goals = int(match["home_goals"])
        away_goals = int(match["away_goals"])
        if home_goals > away_goals:
            home_points, away_points, home_result, away_result = 3, 0, 3, 0
        elif home_goals < away_goals:
            home_points, away_points, home_result, away_result = 0, 3, 0, 3
        else:
            home_points, away_points, home_result, away_result = 1, 1, 1, 1

        expected_home = 1 / (1 + 10 ** ((away.elo - (home.elo + 55)) / 400))
        change = 20.0 * ((home_result / 3.0) - expected_home)
        home.elo += change
        away.elo -= change
        for team, scored, conceded, result, points, venue in (
            (home, home_goals, away_goals, home_result, home_points, "home"),
            (away, away_goals, home_goals, away_result, away_points, "away"),
        ):
            team.results.append(result)
            team.goals_for.append(scored)
            team.goals_against.append(conceded)
            (team.home_points if venue == "home" else team.away_points).append(points)
            team.last_date = date

    return pd.DataFrame(rows)


def build_inference_features(history: pd.DataFrame, upcoming: pd.DataFrame) -> pd.DataFrame:
    """Build pre-match features for upcoming rows from completed history only."""
    required_history = {"date", "home_team", "away_team", "home_goals", "away_goals"}
    missing = required_history - set(history.columns)
    if missing:
        raise ValueError(f"Missing history columns: {sorted(missing)}")
    required_upcoming = {"date", "home_team", "away_team"}
    missing = required_upcoming - set(upcoming.columns)
    if missing:
        raise ValueError(f"Missing upcoming columns: {sorted(missing)}")

    history = history.copy()
    history["date"] = pd.to_datetime(history["date"], errors="coerce", utc=True)
    upcoming_teams = set(upcoming["home_team"].dropna().astype(str)) | set(upcoming["away_team"].dropna().astype(str))
    history = history[
        history["home_team"].astype(str).isin(upcoming_teams)
        | history["away_team"].astype(str).isin(upcoming_teams)
    ]
    history = history.dropna(subset=list(required_history)).sort_values("date")
    states: dict[str, TeamState] = {}

    def emit(home_name: str, away_name: str, match_date: pd.Timestamp, league: str) -> dict[str, object]:
        home = _state(states, home_name)
        away = _state(states, away_name)
        home_rest = 14.0 if home.last_date is None else max(0.0, min(60.0, float((match_date - home.last_date).days)))
        away_rest = 14.0 if away.last_date is None else max(0.0, min(60.0, float((match_date - away.last_date).days)))
        return {
            "date": match_date,
            "league": league,
            "home_team": home_name,
            "away_team": away_name,
            "home_elo": home.elo,
            "away_elo": away.elo,
            "elo_delta": home.elo + 55.0 - away.elo,
            "home_form_5": _mean(home.results[-5:], 0.0),
            "away_form_5": _mean(away.results[-5:], 0.0),
            "home_goals_for_5": _mean(home.goals_for[-5:], 1.2),
            "away_goals_for_5": _mean(away.goals_for[-5:], 1.0),
            "home_goals_against_5": _mean(home.goals_against[-5:], 1.2),
            "away_goals_against_5": _mean(away.goals_against[-5:], 1.2),
            "home_home_points_5": _mean(home.home_points[-5:], 1.0),
            "away_away_points_5": _mean(away.away_points[-5:], 1.0),
            "rest_days_home": home_rest,
            "rest_days_away": away_rest,
        }

    def update(home_name: str, away_name: str, match_date: pd.Timestamp, home_goals: int, away_goals: int) -> None:
        home = _state(states, home_name)
        away = _state(states, away_name)
        if home_goals > away_goals:
            home_result, away_result, home_points, away_points = 3, 0, 3, 0
        elif home_goals < away_goals:
            home_result, away_result, home_points, away_points = 0, 3, 0, 3
        else:
            home_result, away_result, home_points, away_points = 1, 1, 1, 1
        expected_home = 1 / (1 + 10 ** ((away.elo - (home.elo + 55.0)) / 400))
        change = 20.0 * ((home_result / 3.0) - expected_home)
        home.elo += change
        away.elo -= change
        for team, scored, conceded, result, points, venue in (
            (home, home_goals, away_goals, home_result, home_points, "home"),
            (away, away_goals, home_goals, away_result, away_points, "away"),
        ):
            team.results.append(result)
            team.goals_for.append(scored)
            team.goals_against.append(conceded)
            (team.home_points if venue == "home" else team.away_points).append(points)
            team.last_date = match_date

    for _, match in history.iterrows():
        update(
            str(match["home_team"]),
            str(match["away_team"]),
            match["date"],
            int(match["home_goals"]),
            int(match["away_goals"]),
        )

    rows = []
    upcoming = upcoming.copy()
    upcoming["date"] = pd.to_datetime(upcoming["date"], errors="coerce", utc=True)
    for _, match in upcoming.dropna(subset=["date", "home_team", "away_team"]).sort_values("date").iterrows():
        rows.append(emit(str(match["home_team"]), str(match["away_team"]), match["date"], str(match.get("league", "unknown"))))
    return pd.DataFrame(rows)


def _model() -> Pipeline:
    return Pipeline(
        [
            ("scale", StandardScaler()),
            ("classifier", LogisticRegression(max_iter=2000, class_weight="balanced")),
        ]
    )


def _gradient_model() -> Pipeline:
    return Pipeline(
        [
            (
                "classifier",
                HistGradientBoostingClassifier(
                    max_iter=250,
                    learning_rate=0.05,
                    max_leaf_nodes=15,
                    l2_regularization=1.0,
                    random_state=42,
                ),
            )
        ]
    )


def _multiclass_brier(y_true: pd.Series, probabilities: np.ndarray) -> float:
    expected = np.zeros_like(probabilities)
    for index, label in enumerate(y_true.astype(int)):
        expected[index, label] = 1.0
    return float(np.mean(np.sum((probabilities - expected) ** 2, axis=1)))


def validate_training_data(dataset: pd.DataFrame) -> None:
    required = {"date", "home_team", "away_team", TARGET}
    missing = required - set(dataset.columns)
    if missing:
        raise ValueError(f"Training schema is missing: {sorted(missing)}")
    if dataset.empty:
        raise ValueError("Training dataset is empty")
    if dataset[TARGET].isna().any():
        raise ValueError("Training target contains null values")
    if not set(dataset[TARGET].astype(int).unique()).issubset({0, 1, 2}):
        raise ValueError("Training target must contain only 0, 1 or 2")


def train_model(dataset: pd.DataFrame) -> tuple[Pipeline, dict[str, object]]:
    """Train on a chronologically ordered dataset and return metrics."""
    validate_training_data(dataset)
    frame = dataset.dropna(subset=FEATURE_COLUMNS + [TARGET]).sort_values("date")
    if len(frame) < 30:
        raise ValueError("At least 30 historical matches are required for training")
    split = max(1, int(len(frame) * 0.8))
    train, test = frame.iloc[:split], frame.iloc[split:]
    if train[TARGET].nunique() < 2 or test[TARGET].nunique() < 2:
        raise ValueError("Temporal split must contain at least two outcome classes")

    candidates = {
        "logistic_regression": _model(),
        "hist_gradient_boosting": _gradient_model(),
        "calibrated_gradient_boosting": CalibratedClassifierCV(
            _gradient_model(), method="sigmoid", cv=3
        ),
    }
    candidate_metrics: dict[str, dict[str, float]] = {}
    best_name = ""
    best_model: Pipeline | None = None
    best_loss = float("inf")
    for name, candidate in candidates.items():
        candidate.fit(train[FEATURE_COLUMNS], train[TARGET].astype(int))
        probabilities = candidate.predict_proba(test[FEATURE_COLUMNS])
        predictions = candidate.predict(test[FEATURE_COLUMNS])
        loss = float(log_loss(test[TARGET], probabilities, labels=[0, 1, 2]))
        candidate_metrics[name] = {
            "accuracy": float(accuracy_score(test[TARGET], predictions)),
            "balanced_accuracy": float(balanced_accuracy_score(test[TARGET], predictions)),
            "log_loss": loss,
            "brier_score": _multiclass_brier(test[TARGET], probabilities),
        }
        if loss < best_loss:
            best_loss, best_name, best_model = loss, name, candidate

    if best_model is None:
        raise RuntimeError("No candidate model was trained")
    metrics: dict[str, object] = {
        "selected_model": best_name,
        "accuracy": candidate_metrics[best_name]["accuracy"],
        "balanced_accuracy": candidate_metrics[best_name]["balanced_accuracy"],
        "log_loss": candidate_metrics[best_name]["log_loss"],
        "brier_score": candidate_metrics[best_name]["brier_score"],
        "train_rows": len(train),
        "test_rows": len(test),
        "candidate_metrics": candidate_metrics,
    }
    return best_model, metrics


def save_model(model: Pipeline, metrics: dict[str, object], path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)
    metadata = {
        "model_version": MODEL_VERSION,
        "feature_columns": FEATURE_COLUMNS,
        "labels": LABELS,
        "metrics": metrics,
    }
    path.with_suffix(".json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")


def load_model(path: str | Path) -> Pipeline | None:
    path = Path(path)
    if not path.exists():
        return None
    return joblib.load(path)


def predict_model(model: Pipeline, features: pd.DataFrame) -> pd.DataFrame:
    missing = set(FEATURE_COLUMNS) - set(features.columns)
    if missing:
        raise ValueError(f"Missing inference features: {sorted(missing)}")
    probabilities = model.predict_proba(features[FEATURE_COLUMNS])
    return pd.DataFrame(
        {
            "home_probability": probabilities[:, 2],
            "draw_probability": probabilities[:, 1],
            "away_probability": probabilities[:, 0],
            "prediction": [LABELS[int(value)] for value in model.predict(features[FEATURE_COLUMNS])],
        },
        index=features.index,
    )
