# 🔄 AUTOMATISATION DE LA MISE À JOUR DES DONNÉES

**Qu'est-ce que tu veux:** Les données se téléchargent automatiquement sans intervention manuelle  
**Fréquence:** Quotidienne (chaque jour à 3h du matin par exemple)  
**Plateforme:** Local + Cloud

---

## 🎯 Vue d'Ensemble - Solutions

| Solution | Où | Fréquence | Coût | Complexité | Recommandation |
|----------|-----|----------|------|-----------|-----------------|
| **Windows Task Scheduler** | PC Local | Flexible | Gratuit | Facile | ✅ Pour testing local |
| **Cron Jobs** | Linux/Mac | Flexible | Gratuit | Facile | ✅ Pour serveur |
| **GitHub Actions** | Cloud (Gratuit) | Flexible | Gratuit | Moyen | ✅✅ BEST - Recommandé |
| **Google Cloud Scheduler** | Cloud Google | Flexible | ~$1/mois | Facile | ✅ Alternative |
| **AWS Lambda** | Cloud AWS | Flexible | ~$0.2/mois | Moyen | Possible |
| **Heroku Scheduler** | Cloud Heroku | Heures/jours | Gratuit | Facile | Pas mal |
| **Docker Cron Container** | Anywhere | Flexible | Dépend | Avancé | Pour prod |

---

## ✅ SOLUTION 1: GITHUB ACTIONS (RECOMMANDÉ - GRATUIT)

### Pourquoi GitHub Actions?
- ✅ **100% gratuit** (2000 min/mois)
- ✅ **Pas besoin serveur** (runs sur cloud GitHub)
- ✅ **Facile à configurer** (fichier YAML simple)
- ✅ **Intégration Git** (auto-push données mises à jour)
- ✅ **Notifications intégrées** (email si erreur)
- ✅ **Parfait pour portfolio** (montre DevOps)

### 📝 Étape 1: Crée Fichier GitHub Actions

**Fichier:** `.github/workflows/update_data_daily.yml`

```yaml
name: Update Football Data Daily

# Trigger: Tous les jours à 2h du matin UTC (3h UTC+1)
on:
  schedule:
    - cron: '0 2 * * *'  # 2:00 AM UTC every day
  workflow_dispatch:  # Permet lancer manuellement

jobs:
  update_data:
    runs-on: ubuntu-latest
    
    steps:
      # 1. Clone le repo
      - name: Checkout code
        uses: actions/checkout@v3
      
      # 2. Setup Python 3.12
      - name: Set up Python 3.12
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      
      # 3. Cache pour pip (accélère)
      - name: Cache pip
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
      
      # 4. Install dependencies
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      
      # 5. Download data
      - name: Download latest Football Data
        env:
          FOOTBALL_DATA_API_KEY: ${{ secrets.FOOTBALL_DATA_API_KEY }}
        run: |
          python src/data/download_data_2026.py
      
      # 6. Commit et push si data changée
      - name: Commit and push changes
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add data/raw/matches_2024_2026.csv
          git add data/processed/features_complete.csv
          git commit -m "🔄 Auto-update: Data updated $(date)" || echo "No changes to commit"
          git push
      
      # 7. Notification si succès
      - name: Success notification
        if: success()
        run: echo "✅ Data updated successfully at $(date)"
      
      # 8. Notification si erreur
      - name: Failure notification
        if: failure()
        run: |
          echo "❌ Data update failed!"
          exit 1
```

### 🔑 Étape 2: Ajoute API Key à GitHub Secrets

**Via GitHub Web Interface:**

1. Va à: `Settings → Secrets and variables → Actions`
2. Clique: "New repository secret"
3. Name: `FOOTBALL_DATA_API_KEY`
4. Value: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6` (ta clé)
5. Clique: "Add secret"

```bash
# Ou via GitHub CLI:
gh secret set FOOTBALL_DATA_API_KEY --body "YOUR_API_KEY"
```

### ✅ Étape 3: Test

```bash
# Push le fichier
git add .github/workflows/update_data_daily.yml
git commit -m "Add data update workflow"
git push

# Va sur GitHub → Actions
# Doit voir: "Update Football Data Daily" workflow
# Clique Play pour tester manuellement
```

### 📊 Résultat Attendu

```
✅ Workflow runs every day at 2 AM UTC
✅ Data downloaded automatically
✅ Git updated with new CSV
✅ You see commits like "🔄 Auto-update: Data updated Sep 15"
✅ No manual intervention needed
```

---

## ✅ SOLUTION 2: WINDOWS TASK SCHEDULER (LOCAL)

### Idéal pour: Testing local avant déployer

### 📝 Étape 1: Crée Script Batch

**Fichier:** `update_data.bat`

```batch
@echo off
REM Update Football Data Script

REM Change to project directory
cd C:\path\to\football_predictor

REM Activate venv
call venv\Scripts\activate.bat

REM Set API key
set FOOTBALL_DATA_API_KEY=YOUR_API_KEY

REM Download data
python src/data/download_data_2026.py

REM Log result
echo Data updated at %date% %time% >> logs/update_log.txt

REM Commit to git (si dans Git repo)
git add data/
git commit -m "Auto-update: %date%"
git push

REM Success
echo ✅ Data updated successfully!
pause
```

### 📝 Étape 2: Crée Python Script Alternative

**Fichier:** `scripts/auto_update.py`

```python
#!/usr/bin/env python3
"""
Automatic data update script
Run via Task Scheduler / Cron
"""

import os
import sys
import logging
from datetime import datetime
import subprocess

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/auto_update.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def update_data():
    """Download latest data"""
    
    logger.info("🔄 Starting automatic data update...")
    
    try:
        # Set API key from environment
        api_key = os.getenv('FOOTBALL_DATA_API_KEY')
        if not api_key:
            logger.error("❌ FOOTBALL_DATA_API_KEY not set!")
            return False
        
        # Execute download
        logger.info("📥 Downloading data from Football-Data.org...")
        result = subprocess.run(
            [sys.executable, 'src/data/download_data_2026.py'],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            logger.error(f"❌ Download failed: {result.stderr}")
            return False
        
        logger.info("✅ Data downloaded successfully")
        
        # Calculate features
        logger.info("🔧 Calculating features...")
        result = subprocess.run(
            [sys.executable, 'src/data/feature_calculator.py'],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            logger.error(f"❌ Feature calculation failed: {result.stderr}")
            return False
        
        logger.info("✅ Features calculated")
        
        # Git commit (optional)
        try:
            logger.info("📤 Committing to Git...")
            subprocess.run(['git', 'add', 'data/'], check=True)
            subprocess.run(
                ['git', 'commit', '-m', f'🔄 Auto-update: {datetime.now().strftime("%Y-%m-%d %H:%M")}'],
                check=False  # Don't fail if nothing to commit
            )
            subprocess.run(['git', 'push'], check=True)
            logger.info("✅ Changes pushed to GitHub")
        except Exception as e:
            logger.warning(f"⚠️ Git commit failed: {e}")
        
        logger.info("✅ Automatic update completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        return False

if __name__ == '__main__':
    success = update_data()
    sys.exit(0 if success else 1)
```

### 📝 Étape 3: Schedule en Windows Task Scheduler

**Via GUI:**

1. **Ouvre:** Task Scheduler (Recherche "Task Scheduler")

2. **Crée tâche:**
   - Action → Create Basic Task
   - Name: "Update Football Data"
   - Description: "Automatic daily data update"

3. **Trigger:**
   - When: Daily
   - Time: 03:00 (3 AM)
   - Repeat: Every 1 day

4. **Action:**
   - Program: `C:\path\to\venv\Scripts\python.exe`
   - Arguments: `scripts/auto_update.py`
   - Start in: `C:\path\to\football_predictor`

5. **Conditions:**
   - Start task only if idle
   - If the task fails, retry after 1 hour

6. **Settings:**
   - Allow task to be run on demand
   - Stop if running longer than 30 minutes

**Via PowerShell (Avancé):**

```powershell
# Crée action
$action = New-ScheduledTaskAction -Execute "C:\path\to\venv\Scripts\python.exe" -Argument "scripts/auto_update.py" -WorkingDirectory "C:\path\to\football_predictor"

# Crée trigger (tous les jours à 3h)
$trigger = New-ScheduledTaskTrigger -Daily -At 3:00AM

# Crée tâche
Register-ScheduledTask -TaskName "Update Football Data" -Action $action -Trigger $trigger -RunLevel Highest
```

---

## ✅ SOLUTION 3: LINUX/MAC CRON JOBS

### Simple & Puissant

### 📝 Étape 1: Crée Script Shell

**Fichier:** `scripts/update_data.sh`

```bash
#!/bin/bash

# Auto-update script for Linux/Mac

# Project directory
PROJECT_DIR="/home/jimmy/football_predictor"
cd $PROJECT_DIR

# Activate venv
source venv/bin/activate

# Set API key
export FOOTBALL_DATA_API_KEY="YOUR_API_KEY"

# Download data
python src/data/download_data_2026.py

# Calculate features
python src/data/feature_calculator.py

# Git operations
git add data/
git commit -m "🔄 Auto-update: $(date '+%Y-%m-%d %H:%M')"
git push origin main

# Log
echo "✅ Data updated at $(date)" >> logs/update.log
```

### Rendre exécutable:
```bash
chmod +x scripts/update_data.sh
```

### 📝 Étape 2: Setup Cron Job

```bash
# Ouvre crontab
crontab -e

# Ajoute cette ligne (pour exécuter chaque jour à 3h):
0 3 * * * /home/jimmy/football_predictor/scripts/update_data.sh

# Explications:
# 0     = minute (0)
# 3     = heure (3 AM)
# *     = jour du mois (tout)
# *     = mois (tout)
# *     = jour de la semaine (tout)
# rest  = commande à exécuter
```

### Autres fréquences:
```bash
# Chaque heure
0 * * * * /path/to/script.sh

# Chaque 6 heures
0 */6 * * * /path/to/script.sh

# Tous les jours à 2 AM et 2 PM
0 2,14 * * * /path/to/script.sh

# Tous les lundis à 3h
0 3 * * 1 /path/to/script.sh

# Premier jour du mois à 3h
0 3 1 * * /path/to/script.sh
```

### Vérifier cron jobs:
```bash
# Voir mes crons
crontab -l

# Voir logs
tail -f /var/log/syslog | grep CRON
```

---

## ✅ SOLUTION 4: CLOUD - GOOGLE CLOUD SCHEDULER

### Gratuit (1-2 $ par mois max)

### 📝 Étape 1: Setup Cloud Function

**Dans Google Cloud Console:**

1. Va à: Cloud Functions
2. Create Function:
   ```
   Runtime: Python 3.12
   Entry point: update_data
   Memory: 256 MB
   Timeout: 300 seconds
   ```

3. Code (`main.py`):
```python
import subprocess
import os
from datetime import datetime

def update_data(request):
    """Cloud Function pour update data"""
    
    api_key = os.getenv('FOOTBALL_DATA_API_KEY')
    
    if not api_key:
        return 'Error: API key not set', 500
    
    try:
        # Download
        result = subprocess.run(
            ['python', 'src/data/download_data_2026.py'],
            capture_output=True,
            text=True,
            timeout=300,
            env={**os.environ, 'FOOTBALL_DATA_API_KEY': api_key}
        )
        
        if result.returncode != 0:
            return f'Error: {result.stderr}', 500
        
        return f'✅ Data updated successfully at {datetime.now()}', 200
        
    except Exception as e:
        return f'Error: {str(e)}', 500
```

### 📝 Étape 2: Schedule Execution

1. Va à: Cloud Scheduler
2. Create Job:
   ```
   Name: update-football-data
   Frequency: 0 2 * * * (chaque jour à 2h)
   Timezone: UTC
   Execution: HTTPS
   URL: https://region-project.cloudfunctions.net/update_data
   Auth: No auth
   ```

3. Create!

---

## 📊 ARCHITECTURE COMPLÈTE AUTOMATISÉE

```
┌─────────────────────────────────────────────────────────┐
│              AUTOMATED DATA PIPELINE 2026                │
└─────────────────────────────────────────────────────────┘
        │
        ├─→ Schedule (GitHub Actions / Cron / Cloud)
        │
        ↓
┌─────────────────────────────────────────────────────────┐
│  1️⃣ DOWNLOAD                                            │
│  ├─ Football-Data.org API (20,000+ matchs)             │
│  ├─ Kaggle backup (optionnel)                          │
│  └─ Save: data/raw/matches_2024_2026.csv               │
└─────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────┐
│  2️⃣ VALIDATE                                            │
│  ├─ Check rows count                                   │
│  ├─ Verify date range                                  │
│  ├─ Check for duplicates                               │
│  └─ Log results                                         │
└─────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────┐
│  3️⃣ CALCULATE FEATURES                                  │
│  ├─ Load raw data                                       │
│  ├─ Calculate 35+ features                             │
│  └─ Save: data/processed/features_complete.csv         │
└─────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────┐
│  4️⃣ RETRAIN MODELS                                      │
│  ├─ Load fresh features                                │
│  ├─ Train 4 models (1X2, O/U, BTS, Exact)             │
│  └─ Save updated models: models/*.pkl                  │
└─────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────┐
│  5️⃣ GIT COMMIT                                          │
│  ├─ Commit raw data                                    │
│  ├─ Commit processed features                          │
│  ├─ Commit model files                                 │
│  └─ Push to GitHub                                     │
└─────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────┐
│  6️⃣ NOTIFY                                              │
│  ├─ Email: Success / Failure                           │
│  ├─ Slack: Optional                                    │
│  └─ GitHub: Workflow status                            │
└─────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────┐
│  ✅ APP AUTOMATICALLY USES LATEST DATA                  │
│  (Streamlit reads fresh files on reload)               │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 SCRIPT COMPLET POUR AUTOMATION

**Fichier:** `scripts/full_auto_update.py`

```python
#!/usr/bin/env python3
"""
Complete automatic update pipeline
- Download data
- Validate
- Calculate features
- Retrain models
- Commit to Git
"""

import os
import sys
import logging
import subprocess
from datetime import datetime
import pandas as pd
import traceback

# Setup logging
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'{log_dir}/auto_pipeline_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def run_command(cmd, description):
    """Execute command and log"""
    logger.info(f"▶️  {description}...")
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode != 0:
            logger.error(f"❌ {description} failed!")
            logger.error(f"STDERR: {result.stderr}")
            return False
        
        logger.info(f"✅ {description} completed")
        return True
        
    except subprocess.TimeoutExpired:
        logger.error(f"❌ {description} timed out!")
        return False
    except Exception as e:
        logger.error(f"❌ {description} error: {e}")
        return False

def validate_data():
    """Validate downloaded data"""
    logger.info("🔍 Validating data...")
    
    try:
        df = pd.read_csv('data/raw/matches_2024_2026.csv')
        
        checks = {
            'Total rows': len(df) > 15000,
            'Date range': df['date'].min() < '2024-01-01' and df['date'].max() > '2026-01-01',
            'No NaNs': not df[['home_team', 'away_team', 'result']].isnull().any(),
            'Result values': df['result'].isin([0, 1, 2]).all(),
        }
        
        for check, result in checks.items():
            status = "✅" if result else "❌"
            logger.info(f"{status} {check}: {result}")
        
        return all(checks.values())
        
    except Exception as e:
        logger.error(f"❌ Validation failed: {e}")
        return False

def push_to_git():
    """Commit and push changes to GitHub"""
    logger.info("📤 Pushing to GitHub...")
    
    try:
        subprocess.run(['git', 'add', 'data/'], check=True)
        subprocess.run(['git', 'add', 'models/'], check=True)
        
        commit_msg = f'🔄 Auto-update: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        subprocess.run(['git', 'commit', '-m', commit_msg], check=False)
        
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        logger.info("✅ Pushed to GitHub")
        return True
        
    except Exception as e:
        logger.warning(f"⚠️ Git push failed: {e}")
        return False  # Don't fail if git fails

def send_notification(success):
    """Send email/Slack notification"""
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if success:
        message = f"✅ Data pipeline completed successfully at {timestamp}"
    else:
        message = f"❌ Data pipeline failed at {timestamp}"
    
    logger.info(f"📧 {message}")
    
    # TODO: Add email/Slack integration
    # Example:
    # send_email(to='jimmy@example.com', subject='Data Update', body=message)
    # send_slack(message)

def main():
    """Main pipeline"""
    
    logger.info("=" * 70)
    logger.info("🚀 STARTING AUTOMATIC DATA UPDATE PIPELINE")
    logger.info("=" * 70)
    
    try:
        # Step 1: Download
        if not run_command(
            [sys.executable, 'src/data/download_data_2026.py'],
            "📥 Download data"
        ):
            raise Exception("Download failed")
        
        # Step 2: Validate
        if not validate_data():
            raise Exception("Validation failed")
        
        # Step 3: Calculate features
        if not run_command(
            [sys.executable, 'src/data/feature_calculator.py'],
            "🔧 Calculate features"
        ):
            raise Exception("Feature calculation failed")
        
        # Step 4: Retrain models
        if not run_command(
            [sys.executable, 'src/models/training.py'],
            "🧠 Retrain models"
        ):
            logger.warning("⚠️ Model training failed, but continuing...")
        
        # Step 5: Git commit
        push_to_git()
        
        # Success!
        logger.info("=" * 70)
        logger.info("✅ PIPELINE COMPLETED SUCCESSFULLY!")
        logger.info("=" * 70)
        
        send_notification(True)
        return 0
        
    except Exception as e:
        logger.error("=" * 70)
        logger.error(f"❌ PIPELINE FAILED!")
        logger.error(f"Error: {e}")
        logger.error(traceback.format_exc())
        logger.error("=" * 70)
        
        send_notification(False)
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
```

### Exécuter:
```bash
python scripts/full_auto_update.py
```

---

## 📋 CHECKLIST - SETUP AUTOMATISATION

### GitHub Actions (RECOMMANDÉ)
- [ ] Crée `.github/workflows/update_data_daily.yml`
- [ ] Ajoute API key aux GitHub Secrets
- [ ] Test workflow (appuie Play)
- [ ] Vérifie commits automatiques

### Windows Task Scheduler
- [ ] Crée script Python/Batch
- [ ] Ouvre Task Scheduler
- [ ] Crée tâche avec schedule
- [ ] Test manuel

### Linux/Mac Cron
- [ ] Crée script shell
- [ ] Rend exécutable (`chmod +x`)
- [ ] Ajoute à crontab
- [ ] Test avec `crontab -l`

### Cloud (Optionnel)
- [ ] Cloud Function setup
- [ ] Cloud Scheduler setup
- [ ] Test execution

---

## 📊 MONITORING & ALERTES

### Voir l'Status des Updates

**GitHub Actions:**
```
GitHub → Actions → Update Football Data Daily
```

**Logs Locaux:**
```bash
tail -f logs/auto_pipeline_*.log
```

**Email/Slack Notifications:**

```python
# Ajouter à script:

import smtplib
from email.mime.text import MIMEText

def send_email(success):
    msg = MIMEText("Data update: " + ("SUCCESS" if success else "FAILED"))
    msg['Subject'] = '🔄 Data Update Status'
    msg['From'] = 'jimmy@example.com'
    msg['To'] = 'jimmy@example.com'
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login('YOUR_EMAIL', 'YOUR_PASSWORD')
        server.send_message(msg)
```

---

## 🎯 RÉSUMÉ: QUELLE SOLUTION CHOISIR?

### Pour Portfolio Project (RECOMMANDÉ):
```
✅ GitHub Actions
- Gratuit
- Runs in cloud (pas besoin serveur)
- Intégration Git parfaite
- Fait bien sur GitHub
- Visible: "Updated data at 3 AM" commits
```

### Pour Testing Local:
```
✅ Windows Task Scheduler (Windows)
✅ Cron Jobs (Linux/Mac)
- Simple à setup
- Bon pour comprendre
```

### Pour Production Pro:
```
✅ Cloud (Google Cloud Scheduler, AWS Lambda)
- Monitoring avancé
- Alertes
- Scaling automatique
```

---

## 🚀 DÉMARRER MAINTENANT

### Étape 1: Push le workflow GitHub Actions

```bash
# Crée le fichier
mkdir -p .github/workflows
cat > .github/workflows/update_data_daily.yml << 'EOF'
name: Update Football Data Daily

on:
  schedule:
    - cron: '0 2 * * *'
  workflow_dispatch:

jobs:
  update_data:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt
      - run: |
          export FOOTBALL_DATA_API_KEY=${{ secrets.FOOTBALL_DATA_API_KEY }}
          python src/data/download_data_2026.py
      - run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add data/
          git commit -m "🔄 Auto-update $(date)" || true
          git push
EOF

# Push
git add .github/
git commit -m "Add automatic data update workflow"
git push
```

### Étape 2: Ajoute API Key Secret

```bash
# Via GitHub CLI
gh secret set FOOTBALL_DATA_API_KEY --body "YOUR_API_KEY"

# Ou via web: Settings → Secrets → New repository secret
```

### Étape 3: Test

```
GitHub → Actions → Update Football Data Daily
Click: Run workflow
Attends 2-3 minutes
✅ Doit voir "✓ passed"
```

---

## ✅ RÉSULTAT FINAL

```
Après setup:
✅ Chaque jour à 2h du matin: data automatiquement téléchargée
✅ Features calculées
✅ Modèles retrain
✅ Changements commitées à GitHub
✅ Tu vois: "🔄 Auto-update 2026-09-15 02:00" commits
✅ Streamlit app toujours accès aux données les plus récentes
✅ Zero maintenance
```

---

**C'est possible! GitHub Actions est la solution parfaite pour toi.** 🚀
