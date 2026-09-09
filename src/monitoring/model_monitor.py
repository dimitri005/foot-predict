"""Lightweight data and model monitoring without external services."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


def feature_drift(reference: pd.DataFrame, current: pd.DataFrame, columns: list[str]) -> dict[str, float]:
    """Return normalized mean shifts for numeric features."""
    drift: dict[str, float] = {}
    for column in columns:
        if column not in reference or column not in current:
            continue
        left = pd.to_numeric(reference[column], errors="coerce").dropna()
        right = pd.to_numeric(current[column], errors="coerce").dropna()
        if left.empty or right.empty:
            continue
        scale = max(float(left.std()), 1e-6)
        drift[column] = abs(float(right.mean()) - float(left.mean())) / scale
    return drift


def drift_alerts(drift: dict[str, float], threshold: float = 2.0) -> list[str]:
    return sorted(column for column, value in drift.items() if value >= threshold)


def save_monitoring_report(
    reference: pd.DataFrame,
    current: pd.DataFrame,
    columns: list[str],
    path: str | Path = "models/monitoring_report.json",
) -> dict[str, Any]:
    values = feature_drift(reference, current, columns)
    report: dict[str, Any] = {
        "drift": values,
        "alerts": drift_alerts(values),
        "reference_rows": len(reference),
        "current_rows": len(current),
    }
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report
