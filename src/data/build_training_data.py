import pandas as pd
import numpy as np

from src.data.api_client import COMPETITION_IDS, fetch_football_data_matches
from src.features.feature_engineering import add_features


TRAINING_DATA_FILE = "data/raw/training_dataset.csv"


def build_training_dataset(competition_ids=None, limit=50):
    """Create a truth-label dataset based on the Football-Data.org API payload.

    This function will attempt to call the Football-Data API and create local training data.
    It will also save an enriched dataset with labels for 1X2 target generation.
    """
    if competition_ids is None:
        competition_ids = list(COMPETITION_IDS)

    rows = []
    for competition_id in competition_ids:
        for row in fetch_football_data_matches(
            competition_id=competition_id,
            limit=limit,
            status="FINISHED",
        ):
            rows.append(row)

    df = pd.DataFrame(rows)
    if df.empty:
        return pd.DataFrame()

    # add label
    df["home_goals"] = pd.to_numeric(df.get("home_goals", 0), errors="coerce")
    df["away_goals"] = pd.to_numeric(df.get("away_goals", 0), errors="coerce")
    df["target"] = np.where(df["home_goals"] > df["away_goals"], 2,
                             np.where(df["home_goals"] < df["away_goals"], 0, 1))

    # create feature columns
    df = add_features(df)

    # Keep columns with useful signal
    df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=["target"])

    df.to_csv(TRAINING_DATA_FILE, index=False)
    return df
