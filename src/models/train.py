"""CLI entry point for rebuilding and evaluating the football model."""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

import pandas as pd

from src.models.ml_pipeline import build_pre_match_dataset, save_model, train_model

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
LOGGER = logging.getLogger(__name__)


def main() -> int:
    parser = argparse.ArgumentParser(description="Train the leakage-safe football predictor")
    parser.add_argument("--input", default="data/raw/football_data_matches.csv")
    parser.add_argument("--model", default="models/football_predictor.joblib")
    parser.add_argument("--features-output", default="data/processed/pre_match_features.csv")
    parser.add_argument("--force", action="store_true", help="Promote the new model even if its log loss is worse")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        raise FileNotFoundError(f"Historical dataset not found: {input_path}")

    raw = pd.read_csv(input_path)
    dataset = build_pre_match_dataset(raw)
    output = Path(args.features_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    dataset.to_csv(output, index=False)

    model, metrics = train_model(dataset)
    model_path = Path(args.model)
    metadata_path = model_path.with_suffix(".json")
    old_loss = None
    if metadata_path.exists() and not args.force:
        try:
            old_loss = float(json.loads(metadata_path.read_text(encoding="utf-8"))["metrics"]["log_loss"])
        except (KeyError, TypeError, ValueError, json.JSONDecodeError):
            old_loss = None
    new_loss = float(metrics["log_loss"])
    if old_loss is not None and new_loss > old_loss:
        LOGGER.warning("Candidate rejected: log_loss %.4f is worse than %.4f", new_loss, old_loss)
        return 2
    save_model(model, metrics, model_path)
    LOGGER.info("Model saved to %s", args.model)
    LOGGER.info("Metrics: %s", metrics)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
