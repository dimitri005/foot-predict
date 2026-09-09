"""Download and normalize historical football data for model training.

Football-Data.org is the authoritative source used by this project. Other
providers can be added as adapters, but their records must be normalized and
validated before they are merged into the training table.
"""

from __future__ import annotations

import argparse
import json
import logging
import time
from datetime import date
from pathlib import Path

import pandas as pd

from src.data.api_client import COMPETITION_IDS, fetch_football_data_matches, get_api_key

LOGGER = logging.getLogger(__name__)
ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw"
OUTPUT = RAW_DIR / "football_data_matches.csv"
MANIFEST = RAW_DIR / "football_data_manifest.json"


def collect_football_data(seasons: list[int], limit: int = 1000, delay_seconds: float = 1.0) -> pd.DataFrame:
    if not get_api_key():
        raise RuntimeError("FOOTBALL_DATA_API_KEY is missing from .env")

    rows: list[dict] = []
    total = len(seasons) * len(COMPETITION_IDS)
    completed = 0
    for season in seasons:
        for code, name in COMPETITION_IDS.items():
            completed += 1
            LOGGER.info("[%s/%s] Downloading %s season %s", completed, total, name, season)
            rows.extend(
                fetch_football_data_matches(
                    competition_id=code,
                    season=season,
                    status="FINISHED",
                    limit=limit,
                )
            )
            time.sleep(max(0.0, delay_seconds))

    frame = pd.DataFrame(rows)
    if frame.empty:
        raise RuntimeError("No finished matches were returned by Football-Data.org")
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce", utc=True)
    frame["home_goals"] = pd.to_numeric(frame["home_goals"], errors="coerce")
    frame["away_goals"] = pd.to_numeric(frame["away_goals"], errors="coerce")
    frame = frame.dropna(subset=["date", "home_team", "away_team", "home_goals", "away_goals"])
    frame = frame.drop_duplicates(subset=["match_id"], keep="last").sort_values("date")
    return frame.reset_index(drop=True)


def save_snapshot(frame: pd.DataFrame) -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    frame.to_csv(OUTPUT, index=False)
    manifest = {
        "source": "Football-Data.org",
        "downloaded_at": date.today().isoformat(),
        "rows": int(len(frame)),
        "competitions": sorted(frame["competition"].dropna().unique().tolist()),
        "date_min": frame["date"].min().isoformat(),
        "date_max": frame["date"].max().isoformat(),
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect finished football matches")
    parser.add_argument("--seasons", nargs="+", type=int, default=list(range(2018, 2027)))
    parser.add_argument("--limit", type=int, default=1000)
    parser.add_argument("--delay", type=float, default=1.0, help="Seconds between API requests")
    args = parser.parse_args()
    frame = collect_football_data(args.seasons, args.limit, args.delay)
    save_snapshot(frame)
    LOGGER.info("Saved %s matches to %s", len(frame), OUTPUT)
    return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    raise SystemExit(main())
