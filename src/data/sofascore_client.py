"""SofaScore public web-data connector.

This connector is intentionally isolated from the training pipeline. SofaScore
does not provide a stable public developer API in this project, so callers must
respect its terms, rate limits and robots policy before enabling collection.
"""

from __future__ import annotations

import logging
import re
import time
from pathlib import Path
from typing import Any

import pandas as pd
import requests

LOGGER = logging.getLogger(__name__)
BASE_URL = "https://www.sofascore.com/api/v1"
FALLBACK_BASE_URL = "https://api.sofascore.com/api/v1"
HEADERS = {"User-Agent": "FOOT-PREDICT-data-collector/1.0"}


def _get(path: str, timeout: int = 30) -> dict[str, Any]:
    response = None
    for base_url in (BASE_URL, FALLBACK_BASE_URL):
        candidate = requests.get(f"{base_url}/{path.lstrip('/')}", headers=HEADERS, timeout=timeout)
        if candidate.ok:
            response = candidate
            break
        LOGGER.warning("SofaScore endpoint %s returned HTTP %s", base_url, candidate.status_code)
    if response is None:
        candidate.raise_for_status()
    payload = response.json()
    if not isinstance(payload, dict):
        raise ValueError("SofaScore response is not a JSON object")
    return payload


def _score(event: dict[str, Any], side: str) -> int | None:
    value = event.get("homeScore" if side == "home" else "awayScore", {}).get("current")
    return int(value) if isinstance(value, (int, float)) else None


def normalize_event(event: dict[str, Any]) -> dict[str, Any]:
    tournament = event.get("tournament", {})
    status = event.get("status", {})
    return {
        "source": "sofascore",
        "source_match_id": event.get("id"),
        "competition_code": tournament.get("uniqueTournament", {}).get("slug"),
        "competition": tournament.get("name"),
        "date": pd.to_datetime(event.get("startTimestamp"), unit="s", errors="coerce", utc=True),
        "home_team": event.get("homeTeam", {}).get("name"),
        "away_team": event.get("awayTeam", {}).get("name"),
        "home_goals": _score(event, "home"),
        "away_goals": _score(event, "away"),
        "status": status.get("type"),
        "status_description": status.get("description"),
    }


def fetch_scheduled_events(day: str) -> pd.DataFrame:
    """Fetch all football events scheduled for an ISO date (YYYY-MM-DD)."""
    payload = _get(f"sport/football/scheduled-events/{day}")
    events = [item for item in payload.get("events", []) if isinstance(item, dict)]
    return pd.DataFrame([normalize_event(event) for event in events])


def fetch_tournament_events(tournament_id: int, season_id: int, page: int = 0) -> pd.DataFrame:
    """Fetch one historical tournament page (usually 0 is the latest page)."""
    payload = _get(f"unique-tournament/{tournament_id}/season/{season_id}/events/last/{page}")
    events = [item for item in payload.get("events", []) if isinstance(item, dict)]
    return pd.DataFrame([normalize_event(event) for event in events])


def _numeric_value(value: Any) -> float | None:
    if value is None:
        return None
    match = re.search(r"-?\d+(?:[.,]\d+)?", str(value))
    return float(match.group(0).replace(",", ".")) if match else None


def fetch_event_statistics(event_id: int, pause_seconds: float = 0.25) -> dict[str, Any]:
    """Return normalized post-match statistics for one event.

    These values must be lagged/aggregated before being used as model inputs.
    Using current-match possession, shots or xG directly would leak the result.
    """
    time.sleep(max(0.0, pause_seconds))
    payload = _get(f"event/{event_id}/statistics")
    output: dict[str, Any] = {"source_match_id": event_id}
    for period in payload.get("statistics", []):
        if period.get("period") != "ALL":
            continue
        for group in period.get("groups", []):
            for item in group.get("statisticsItems", []):
                name = re.sub(r"[^a-z0-9]+", "_", str(item.get("name", "")).lower()).strip("_")
                if not name:
                    continue
                output[f"home_{name}"] = _numeric_value(item.get("home"))
                output[f"away_{name}"] = _numeric_value(item.get("away"))
    return output


def save_snapshot(frame: pd.DataFrame, path: str | Path = "data/raw/sofascore_events.csv") -> Path:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    frame.drop_duplicates(subset=["source_match_id"], keep="last").to_csv(destination, index=False)
    return destination
