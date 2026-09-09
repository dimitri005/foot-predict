from src.data.sofascore_client import normalize_event


def test_normalize_sofascore_event():
    row = normalize_event(
        {
            "id": 123,
            "startTimestamp": 1760000000,
            "tournament": {"name": "Premier League", "uniqueTournament": {"slug": "premier-league"}},
            "homeTeam": {"name": "Home FC"},
            "awayTeam": {"name": "Away FC"},
            "homeScore": {"current": 2},
            "awayScore": {"current": 1},
            "status": {"type": "finished", "description": "Finished"},
        }
    )
    assert row["source"] == "sofascore"
    assert row["source_match_id"] == 123
    assert row["home_team"] == "Home FC"
    assert row["home_goals"] == 2
    assert row["away_goals"] == 1
