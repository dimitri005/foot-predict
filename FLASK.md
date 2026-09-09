# Flask Application

The project now runs as a Flask web application instead of Streamlit.

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the production WSGI server:

```bash
python app.py
```

Or explicitly:

```bash
waitress-serve --listen=0.0.0.0:5000 app:app
```

Open `http://127.0.0.1:5000`.

Available routes:

- `/` web dashboard with competition filters and predictions;
- `/api/predictions` JSON response for frontend/mobile clients;
- `/health` deployment health check.

The Flask layer calls the same trained model and historical feature builder as
the training pipeline. It does not train a model during an HTTP request.

Live API results are cached for 15 minutes by default to avoid exhausting the
Football-Data.org quota. Change this with `LIVE_CACHE_SECONDS` if needed.

## Daily Fixtures

The Flask page reads `data/raw/matches_2026.csv`. Refresh this file every day
with:

```powershell
.\scripts\daily_refresh.ps1
```

The script requests only today plus the next three days, merges by
`match_id`, and preserves the old snapshot when the API returns no data.

GitHub Actions is the primary refresh system. If you previously created the
local Windows task, disable it from an **Administrator PowerShell**:

```powershell
schtasks /Change /TN "FOOT-PREDICT Daily Refresh" /DISABLE
```

The Windows script remains available as a manual fallback. To create that
fallback task again, use:

1. Open **Task Scheduler** and choose **Create Basic Task**.
2. Choose **Daily**, for example at `06:00`.
3. Choose **Start a program**.
4. Program: `powershell.exe`
5. Arguments:

```text
-NoProfile -ExecutionPolicy Bypass -File "C:\Users\kenmo\Downloads\FOOT-PREDICT\scripts\daily_refresh.ps1"
```

6. In **Start in**, use:

```text
C:\Users\kenmo\Downloads\FOOT-PREDICT
```

The scheduled task needs access to the project `.env` file. Retrain the model
separately, for example once per week, with `scripts/update_pipeline.ps1`.

## GitHub Actions Refresh

The repository also contains `.github/workflows/daily-refresh.yml`. It runs at
05:00 UTC every day, which is 06:00 in `Africa/Lagos`, and commits updated
fixtures to `data/raw/matches_2026.csv`.

In GitHub, add this repository secret:

```text
Settings -> Secrets and variables -> Actions -> New repository secret
Name: FOOTBALL_DATA_API_KEY
Value: your API token
```

You can run it immediately from **Actions -> Daily Match Refresh -> Run
workflow**. Scheduled GitHub Actions can start a few minutes late, but it is
the primary refresh system for this project.
