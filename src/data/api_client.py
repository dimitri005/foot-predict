import os
import logging
from pathlib import Path

import requests
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
try:
    from dotenv import load_dotenv
except ModuleNotFoundError:  # Keep local startup usable before pip install.
    def load_dotenv() -> None:
        env_file = Path(__file__).resolve().parents[2] / ".env"
        if not env_file.exists():
            return
        for line in env_file.read_text(encoding="utf-8").splitlines():
            name, separator, value = line.partition("=")
            if separator and name.strip() and not name.strip().startswith("#"):
                os.environ.setdefault(name.strip(), value.strip().strip('"').strip("'"))


load_dotenv()

LOGGER = logging.getLogger(__name__)

_RETRY = Retry(
    total=3,
    backoff_factor=1.5,
    status_forcelist=(429, 500, 502, 503, 504),
    allowed_methods=("GET",),
    respect_retry_after_header=True,
)
_SESSION = requests.Session()
_SESSION.mount("https://", HTTPAdapter(max_retries=_RETRY))


WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
GITIGNORE_FILE = WORKSPACE_ROOT / ".gitignore"
RAW_DATA_DIR = WORKSPACE_ROOT / "data" / "raw"
MATCHES_RAW_FILE = RAW_DATA_DIR / "matches_2026.csv"

COMPETITION_IDS = {
    "WC": "FIFA World Cup",
    "CL": "UEFA Champions League",
    "BL1": "Bundesliga",
    "DED": "Eredivisie",
    "BSA": "Campeonato Brasileiro Serie A",
    "PD": "Primera Division",
    "FL1": "Ligue 1",
    "ELC": "Championship",
    "PPL": "Primeira Liga",
    "EC": "European Championship",
    "SA": "Serie A",
    "PL": "Premier League",
}


def read_api_key_from_gitignore() -> str | None:
    """Read FOOTBALL_DATA_API_KEY from a .gitignore-style assignment."""
    if not GITIGNORE_FILE.exists():
        return None

    text = GITIGNORE_FILE.read_text(encoding="utf-8", errors="ignore")
    key_line = next((line for line in text.splitlines() if line.strip().startswith("FOOTBALL_DATA_API_KEY") and "=" in line), None)
    if key_line:
        _, value = key_line.split("=", 1)
        return value.strip()

    return None


def get_api_key() -> str | None:
    """Return the API key from environment variables or a local .env file."""
    return os.getenv("FOOTBALL_DATA_API_KEY")


def fetch_football_data_matches(
    competition_id: str = "PL",
    limit: int = 100,
    season: int | None = None,
    status: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
) -> list[dict]:
    """Fetch matches from Football-Data.org for a competition.

    Falls back safely to an empty list if the key is absent or the request fails.
    """
    api_key = get_api_key()
    if not api_key:
        return []

    url = f"https://api.football-data.org/v4/competitions/{competition_id}/matches"
    headers = {
        "X-Auth-Token": api_key,
        "Accept": "application/json",
    }

    try:
        params = {"limit": limit}
        if season is not None:
            params["season"] = season
        if status:
            params["status"] = status
        if date_from:
            params["dateFrom"] = date_from
        if date_to:
            params["dateTo"] = date_to
        response = _SESSION.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        payload = response.json()
        matches = payload.get("matches", [])[:limit]

        output = []
        for match in matches:
            home_team = match.get("homeTeam", {}).get("name")
            away_team = match.get("awayTeam", {}).get("name")
            home_goals = match.get("score", {}).get("fullTime", {}).get("home")
            away_goals = match.get("score", {}).get("fullTime", {}).get("away")

            output.append({
                "match_id": match.get("id"),
                "competition": payload.get("competition", {}).get("name"),
                "league": payload.get("competition", {}).get("name"),
                "season": match.get("season", {}).get("startDate", "")[:4],
                "date": match.get("utcDate", ""),
                "status": match.get("status"),
                "home_team": home_team,
                "away_team": away_team,
                "home_goals": home_goals,
                "away_goals": away_goals,
            })

        return output

    except requests.RequestException as exc:
        LOGGER.warning("Football-Data request failed for %s: %s", competition_id, exc)
        return []
    except (KeyError, TypeError, ValueError) as exc:
        LOGGER.warning("Invalid Football-Data response for %s: %s", competition_id, exc)
        return []


def load_real_matches(competition_ids: list[str] | None = None, limit: int = 10) -> pd.DataFrame:
    """Return a DataFrame built from Football-Data.org for the selected competition IDs."""
    if competition_ids is None:
        competition_ids = list(COMPETITION_IDS)

    rows = []
    for competition_id in competition_ids:
        for row in fetch_football_data_matches(competition_id=competition_id, limit=limit):
            rows.append(row)

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df


def save_raw_matches(df: pd.DataFrame) -> Path:
    """Persist the real API snapshot to a local file for reproducible use."""
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(MATCHES_RAW_FILE, index=False)
    return MATCHES_RAW_FILE
