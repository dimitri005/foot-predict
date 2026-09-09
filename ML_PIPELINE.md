# ML Pipeline

The production training path uses only information available before each
match. It builds chronological Elo, form, goals and rest-day features, then
compares logistic regression, histogram gradient boosting and a calibrated
gradient boosting classifier with a temporal 80/20 split.

## Train

Place a sufficiently large historical dataset in
`data/raw/training_dataset.csv`. It must contain `date`, `home_team`,
`away_team`, `home_goals` and `away_goals`.

Run:

```bash
python -m src.models.train
```

The selected candidate is promoted only when its test `log_loss` is not worse
than the currently saved model. Use `--force` only when intentionally changing
the model policy.

This writes:

- `data/processed/pre_match_features.csv`
- `models/football_predictor.joblib`
- `models/football_predictor.json`

The Streamlit application loads the saved model automatically. Until a model
has been trained, it uses the existing baseline predictor and labels the
result with `model=baseline`.

Live inference rebuilds Elo, form, goals and rest-day state from
`data/raw/football_data_matches.csv` before scoring upcoming matches. This
keeps training and inference feature definitions aligned.

The monitoring helpers in `src/monitoring/model_monitor.py` measure normalized
feature drift and write alerts to `models/monitoring_report.json`.

The current repository dataset is intentionally too small to train a useful
model. The training command refuses datasets with fewer than 30 completed
matches rather than producing misleading metrics.

## SofaScore

SofaScore collection is isolated in `src/data/sofascore_client.py` and can be
run with:

```bash
python -m src.data.collect_sofascore --date 2026-09-08
```

It writes `data/raw/sofascore_events.csv`. Detailed statistics are retained as
post-match data and must be lagged or aggregated over previous matches before
being used as prediction features. They must never be joined directly to the
same match target.

The optional PowerShell update is:

```powershell
.\scripts\update_pipeline.ps1 -IncludeSofaScore
```

The connector uses a public web endpoint, not a guaranteed developer API. A
403 response is handled as a source outage; the primary Football-Data.org
pipeline remains usable.
