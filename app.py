"""Flask web application for the football prediction service."""

from __future__ import annotations

import json
import os
import threading
import time
from pathlib import Path
from typing import Any

import pandas as pd
from flask import Flask, jsonify, render_template, request

from src.data.api_client import COMPETITION_IDS, get_api_key, load_real_matches, save_raw_matches
from src.data.sample_data import load_sample_data
from src.features.feature_engineering import add_features
from src.models.ml_pipeline import build_inference_features
from src.models.predictor import FootballPredictor

app = Flask(__name__)
HISTORY_PATH = Path("data/raw/football_data_matches.csv")
LOCAL_MATCHES_PATH = Path("data/raw/matches_2026.csv")
LIVE_CACHE_SECONDS = int(os.getenv("LIVE_CACHE_SECONDS", "900"))
LIVE_REFRESH_ON_STARTUP = os.getenv("LIVE_REFRESH_ON_STARTUP", "false").lower() in {"1", "true", "yes"}
_MATCH_CACHE: tuple[float, pd.DataFrame] | None = None
_CACHE_LOCK = threading.Lock()


def _load_matches(force_refresh: bool = False) -> pd.DataFrame:
    """Load upcoming API matches, with a local demo fallback."""
    global _MATCH_CACHE
    with _CACHE_LOCK:
        now = time.monotonic()
        if not force_refresh and _MATCH_CACHE is not None and now - _MATCH_CACHE[0] < LIVE_CACHE_SECONDS:
            return _MATCH_CACHE[1].copy()

        # Serve the last successful snapshot immediately. API refreshes are
        # explicit by default so a provider quota cannot block the dashboard.
        if not force_refresh and LOCAL_MATCHES_PATH.exists() and not LIVE_REFRESH_ON_STARTUP:
            local = pd.read_csv(LOCAL_MATCHES_PATH)
            local = _ensure_match_ids(local)
            _MATCH_CACHE = (now, local.copy())
            return local

        if get_api_key():
            matches = load_real_matches(list(COMPETITION_IDS), limit=5)
            if not matches.empty:
                scheduled = matches[matches["status"].isin(["SCHEDULED", "TIMED", "POSTPONED"])] if "status" in matches else matches
                matches = scheduled if not scheduled.empty else matches
                matches = _ensure_match_ids(matches)
                save_raw_matches(matches)
                _MATCH_CACHE = (now, matches.copy())
                return matches

        if LOCAL_MATCHES_PATH.exists():
            local = pd.read_csv(LOCAL_MATCHES_PATH)
            if not local.empty:
                local = _ensure_match_ids(local)
                _MATCH_CACHE = (now, local.copy())
                return local
        sample = load_sample_data()
        sample = _ensure_match_ids(sample)
        _MATCH_CACHE = (now, sample.copy())
        return sample


def _ensure_match_ids(matches: pd.DataFrame) -> pd.DataFrame:
    result = matches.copy()
    if "match_id" not in result.columns:
        result["match_id"] = [f"fixture-{index}" for index in range(len(result))]
    result["match_id"] = result["match_id"].astype(str)
    return result


def _prediction_frame(matches: pd.DataFrame) -> pd.DataFrame:
    if HISTORY_PATH.exists():
        history = pd.read_csv(HISTORY_PATH)
        try:
            return build_inference_features(history, matches)
        except (KeyError, TypeError, ValueError):
            pass
    return add_features(matches)


def _dashboard_payload(league: str | None = None, force_refresh: bool = False) -> dict[str, Any]:
    matches = _load_matches(force_refresh=force_refresh)
    all_leagues = sorted(COMPETITION_IDS.values())
    if matches.empty:
        selected = league if league in all_leagues else (all_leagues[0] if all_leagues else None)
        return {
            "matches": [],
            "predictions": [],
            "leagues": all_leagues,
            "selected_league": selected,
            "model": "unavailable",
            "kpis": {
                "matches": 0,
                "competitions": len(all_leagues),
                "average_confidence": 0.0,
                "average_goals": 0.0,
            },
        }

    matches = matches.copy()
    matches["date"] = pd.to_datetime(matches["date"], errors="coerce", utc=True)
    # The snapshot also contains historical rows for training and auditing.
    # The dashboard must only expose today's and upcoming fixtures.
    today_utc = pd.Timestamp.now(tz="UTC").normalize()
    matches = matches[matches["date"].notna() & (matches["date"] >= today_utc)]
    available_from_data = {str(value) for value in matches["league"].dropna().unique()}
    leagues = sorted(set(COMPETITION_IDS.values()) | available_from_data)
    selected = league if league in leagues else (sorted(available_from_data)[0] if available_from_data else (leagues[0] if leagues else None))
    if matches.empty:
        return {
            "matches": [],
            "predictions": [],
            "leagues": leagues,
            "selected_league": selected,
            "model": "unavailable",
            "kpis": {
                "matches": 0,
                "competitions": len(leagues),
                "average_confidence": 0.0,
                "average_goals": 0.0,
            },
        }
    # Prefer a competition with downloaded fixtures on first load. The full
    # subscription list remains available in the selector.
    filtered = matches[matches["league"] == selected] if selected else matches
    inference = _prediction_frame(filtered.head(20))
    predictor = FootballPredictor()
    predictions = [predictor.predict(row) for _, row in inference.head(10).iterrows()]
    average_confidence = sum(item["confidence"] for item in predictions) / len(predictions) if predictions else 0.0
    average_goals = (
        sum(item["markets"]["expected_goals"]["total"] for item in predictions) / len(predictions)
        if predictions
        else 0.0
    )
    match_records = json.loads(filtered.head(10).to_json(orient="records", date_format="iso"))
    prediction_records = json.loads(json.dumps(predictions, default=str))
    return {
        "matches": match_records,
        "predictions": prediction_records,
        "leagues": leagues,
        "selected_league": selected,
        "model": predictions[0].get("model", "baseline") if predictions else "unavailable",
        "kpis": {
            "matches": int(len(filtered)),
            "competitions": int(len(leagues)),
            "average_confidence": average_confidence,
            "average_goals": average_goals,
        },
    }


@app.get("/")
def index() -> str:
    league = request.args.get("league")
    return render_template("index.html", **_dashboard_payload(league))


@app.get("/api/predictions")
def predictions() -> Any:
    force_refresh = request.args.get("refresh", "false").lower() in {"1", "true", "yes"}
    return jsonify(_dashboard_payload(request.args.get("league"), force_refresh=force_refresh))


@app.get("/match/<match_id>")
def match_detail(match_id: str) -> Any:
    matches = _load_matches()
    matches = _ensure_match_ids(matches)
    selected = matches[matches["match_id"] == str(match_id)]
    if selected.empty:
        return render_template("not_found.html", message="Rencontre introuvable"), 404
    match = selected.iloc[0]
    inference = _prediction_frame(selected)
    if inference.empty:
        return render_template("not_found.html", message="Données de prédiction indisponibles"), 503
    prediction = FootballPredictor().predict(inference.iloc[0])
    return render_template("match_detail.html", match=match.to_dict(), prediction=prediction)


@app.get("/health")
def health() -> Any:
    return jsonify({"status": "ok", "model_exists": Path("models/football_predictor.joblib").exists()})


if __name__ == "__main__":
    try:
        from waitress import serve
    except ModuleNotFoundError:
        raise SystemExit("Install dependencies with 'pip install -r requirements.txt' before starting Flask")
    port = int(os.getenv("PORT", "5000"))
    print(f"Football Predictor running at http://0.0.0.0:{port}", flush=True)
    serve(app, host="0.0.0.0", port=port)
