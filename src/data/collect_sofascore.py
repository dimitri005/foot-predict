"""Collect SofaScore events without mixing post-match stats into features."""

from __future__ import annotations

import argparse
import logging
from datetime import date

from src.data.sofascore_client import fetch_scheduled_events, save_snapshot


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect SofaScore football events")
    parser.add_argument("--date", default=date.today().isoformat(), help="ISO date, for example 2026-09-08")
    args = parser.parse_args()
    frame = fetch_scheduled_events(args.date)
    if frame.empty:
        logging.warning("SofaScore returned no football events for %s", args.date)
    else:
        path = save_snapshot(frame)
        logging.info("Saved %s SofaScore events to %s", len(frame), path)
    return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    raise SystemExit(main())
