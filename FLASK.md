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

On Windows, create a Task Scheduler task:

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
