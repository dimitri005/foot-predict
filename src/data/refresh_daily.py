"""Refresh the local fixture snapshot for the current and next few days."""

from __future__ import annotations

import argparse
import logging
import time
from datetime import date, timedelta

import pandas as pd

from src.data.api_client import COMPETITION_IDS, MATCHES_RAW_FILE, fetch_football_data_matches, get_api_key

LOGGER = logging.getLogger(__name__)


def refresh_daily(window_days: int = 3, delay_seconds: float = 1.0) -> pd.DataFrame:
    """Fetch fixtures in a rolling date window and merge them into the snapshot."""
    if not get_api_key():
        raise RuntimeError("FOOTBALL_DATA_API_KEY is missing from .env")
    if window_days < 0:
        raise ValueError("window_days must be positive")

    start = date.today()
    end = start + timedelta(days=window_days)
    rows: list[dict] = []
    for code, name in COMPETITION_IDS.items():
        LOGGER.info("Refreshing %s: %s to %s", name, start, end)
        rows.extend(
            fetch_football_data_matches(
                competition_id=code,
                date_from=start.isoformat(),
                date_to=end.isoformat(),
                limit=100,
            )
        )
        time.sleep(max(0.0, delay_seconds))

    fresh = pd.DataFrame(rows)
    if fresh.empty:
        LOGGER.warning("No fixtures returned; preserving the existing snapshot")
        return pd.read_csv(MATCHES_RAW_FILE) if MATCHES_RAW_FILE.exists() else fresh

    if MATCHES_RAW_FILE.exists():
        existing = pd.read_csv(MATCHES_RAW_FILE)
        combined = pd.concat([existing, fresh], ignore_index=True)
    else:
        combined = fresh
    combined["date"] = pd.to_datetime(combined["date"], errors="coerce", utc=True)
    combined = combined.dropna(subset=["match_id", "date"])
    combined = combined.drop_duplicates(subset=["match_id"], keep="last").sort_values("date")
    MATCHES_RAW_FILE.parent.mkdir(parents=True, exist_ok=True)
    combined.to_csv(MATCHES_RAW_FILE, index=False)
    LOGGER.info("Snapshot updated: %s matches", len(combined))
    return combined.reset_index(drop=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Refresh daily football fixtures")
    parser.add_argument("--window-days", type=int, default=3)
    parser.add_argument("--delay", type=float, default=1.0)
    args = parser.parse_args()
    refresh_daily(args.window_days, args.delay)
    return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    raise SystemExit(main())
