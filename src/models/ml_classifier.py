import pickle
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


class FootballMLClassifier:
    """A supervised logistic-regression baseline for the 1X2 football classification task."""

    def __init__(self, model=None, feature_columns=None):
        self.model = model or LogisticRegression(max_iter=1000, solver="lbfgs")
        self.feature_columns = feature_columns or [
            "home_form_delta",
            "away_form_delta",
            "xg_delta",
            "goals_delta",
            "strength_delta",
            "goal_expectation_home",
            "goal_expectation_away",
            "risk_index",
        ]

    def fit(self, df: pd.DataFrame):
        X = df[self.feature_columns]
        y = df["target"]
        self.model.fit(X, y)
        return self

    def predict_proba(self, df_or_row):
        if isinstance(df_or_row, pd.DataFrame):
            X = df_or_row[self.feature_columns]
        else:
            X = pd.DataFrame([df_or_row])[self.feature_columns]

        proba = self.model.predict_proba(X)
        classes = self.model.classes_
        proba_map = {}
        for cls, val in zip(classes, proba[0]):
            proba_map[str(cls)] = float(val)

        # Align the 3 x-class probabilities with the domain labels home/draw/away.
        return {
            "home": proba_map.get("0", 0.0),
            "draw": proba_map.get("1", 0.0),
            "away": proba_map.get("2", 0.0),
        }

    def save(self, path: str | Path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("wb") as fp:
            pickle.dump(self, fp)

    @staticmethod
    def load(path: str | Path):
        path = Path(path)
        with path.open("rb") as fp:
            return pickle.load(fp)


def train_classifier(data: pd.DataFrame, output_path: str | Path = "models/football_model.pkl") -> tuple[FootballMLClassifier, float]:
    """Train a logistic regression model from a match DataFrame with a label column target.

    target is encoded as:
    0 = away win
    1 = draw
    2 = home win
    """
    data = data.copy()
    required = {"home_goals", "away_goals", "home_form", "away_form", "home_xg", "away_xg"}
    if not required.issubset(data.columns):
        raise ValueError("Dataset must include football base columns for training.")

    # Label generation
    data["target"] = np.where(data["home_goals"] > data["away_goals"], 2,
                               np.where(data["home_goals"] < data["away_goals"], 0, 1))

    # Build feature set
    feature_df = data.copy()
    feature_df = add_features_from_training_df(feature_df)

    # Keep only rows with target and enough signal
    feature_df = feature_df.dropna(subset=["target"])
    feature_df = feature_df.replace([np.inf, -np.inf], np.nan).dropna()

    X = feature_df[[
        "home_form_delta",
        "away_form_delta",
        "xg_delta",
        "goals_delta",
        "strength_delta",
        "goal_expectation_home",
        "goal_expectation_away",
        "risk_index",
    ]]
    y = feature_df["target"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    model = FootballMLClassifier()
    model.fit(pd.concat([X_train, y_train], axis=1))

    # Compute model accuracy quickly.
    predictions = model.model.predict(X_test)
    accuracy = float(accuracy_score(y_test, predictions))

    model.save(output_path)
    return model, accuracy


def add_features_from_training_df(df: pd.DataFrame) -> pd.DataFrame:
    """Compatibility layer that delegates to the feature engineering function."""
    from src.features.feature_engineering import add_features
    return add_features(df)
