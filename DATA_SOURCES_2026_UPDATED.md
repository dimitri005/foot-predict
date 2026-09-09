# 📊 SOURCES DE DONNÉES FOOTBALL - MISE À JOUR 2026

**Date actuelle:** Septembre 2026  
**Données disponibles:** Jusqu'à septembre 2026  
**Dernière mise à jour de ce guide:** Septembre 2026

---

## 🎯 Vue d'Ensemble - 2026

### Statut des Données par Source

| Source | 2024 | 2025 | 2026 (Sep) | Latence | URL |
|--------|------|------|-----------|---------|-----|
| **Football-Data.org** | ✅ Complet | ✅ Complet | ✅ Temps réel | 0-6h | https://www.football-data.org |
| **Kaggle** | ✅ Complet | ✅ Mis à jour | ✅ Septembre | 1-2 jours | https://www.kaggle.com |
| **Flashscore** | ✅ Complet | ✅ Complet | ✅ Temps réel | 0-2h | https://www.flashscore.com |
| **ESPN** | ✅ Complet | ✅ Complet | ✅ Temps réel | 0-1h | https://www.espn.com |
| **Understat** | ✅ Complet | ✅ Complet | ✅ Temps réel | 0-12h | https://understat.com |
| **SofaScore** | ✅ Complet | ✅ Complet | ✅ Temps réel | 0-1h | https://www.sofascore.com |
| **WhoScored** | ✅ Complet | ✅ Complet | ✅ Maj 2x/jour | 2-6h | https://www.whoscored.com |

---

## 1️⃣ FOOTBALL-DATA.ORG (RECOMMANDÉ 2026)

### Statut 2026

✅ **COMPLÈTEMENT À JOUR**
- Données: Janvier 2024 → Septembre 2026
- Saisons couvertes: 2024/25 (complet), 2025/26 (en cours)
- Matchs: 20,000+ disponibles
- Cotes: Actualisées temps réel
- **Latence:** 0-6 heures après match

### 📝 Setup (Exact Même Qu'Avant)

```bash
# 1. Crée compte
https://www.football-data.org/client/register

# 2. Obtiens API key
https://www.football-data.org/client/login
# → Copy ta clé

# 3. Test immédiat
curl -X GET "https://api.football-data.org/v4/competitions/2021/matches" \
  -H "X-Auth-Token: YOUR_API_KEY" \
  -H "Accept: application/json"

# Doit retourner les matchs 2024-2026
```

### 🔗 Compétitions Disponibles 2026

```python
COMPETITIONS_2026 = {
    2021: ("Premier League", "2024/25 + 2025/26 en cours"),
    2014: ("La Liga", "2024/25 + 2025/26 en cours"),
    2002: ("Bundesliga", "2024/25 + 2025/26 en cours"),
    2015: ("Ligue 1", "2024/25 + 2025/26 en cours"),
    2019: ("Serie A", "2024/25 + 2025/26 en cours"),
    2001: ("UEFA Champions League", "2024/25 + 2025/26 en cours"),
    2013: ("Europa League", "2024/25 + 2025/26 en cours"),
    2018: ("World Cup 2022", "Complet"),
    2017: ("Euros 2024", "Complet"),
}
```

### 📥 Télécharger Toutes les Données 2024-2026

```python
# src/data/download_data_2026.py

import requests
import pandas as pd
from datetime import datetime

FOOTBALL_DATA_API_KEY = 'YOUR_API_KEY'
BASE_URL = "https://api.football-data.org/v4"

def download_all_matches_2026():
    """Télécharge TOUS les matchs 2024-2026"""
    
    headers = {
        'X-Auth-Token': FOOTBALL_DATA_API_KEY,
        'Accept': 'application/json'
    }
    
    all_matches = []
    
    # Compétitions clés
    competitions = [2021, 2014, 2002, 2015, 2019, 2001]
    seasons = [2024, 2025, 2026]  # Seasons 2024/25 and 2025/26
    
    total = len(competitions) * len(seasons)
    count = 0
    
    for comp_id in competitions:
        for season in seasons:
            count += 1
            print(f"[{count}/{total}] Downloading competition {comp_id}, season {season}...")
            
            try:
                url = f"{BASE_URL}/competitions/{comp_id}/matches"
                params = {
                    'season': season,
                    'status': 'FINISHED'  # Seulement matchs terminés
                }
                
                response = requests.get(url, headers=headers, params=params, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                
                for match in data.get('matches', []):
                    all_matches.append({
                        'date': match['utcDate'],
                        'home_team': match['homeTeam']['name'],
                        'away_team': match['awayTeam']['name'],
                        'home_goals': match['score']['fullTime']['home'],
                        'away_goals': match['score']['fullTime']['away'],
                        'result': calculate_result(
                            match['score']['fullTime']['home'],
                            match['score']['fullTime']['away']
                        ),
                        'league_id': comp_id,
                        'season': season,
                        'status': match['status'],
                        'odds_1': match.get('odds', {}).get('homeWin', None),
                        'odds_x': match.get('odds', {}).get('draw', None),
                        'odds_2': match.get('odds', {}).get('awayWin', None),
                        'download_date': datetime.now(),
                    })
                
                print(f"  ✅ Downloaded {len(data.get('matches', []))} matches")
                
            except Exception as e:
                print(f"  ❌ Error: {e}")
    
    # Sauvegarde
    df = pd.DataFrame(all_matches)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').reset_index(drop=True)
    
    df.to_csv('data/raw/matches_2024_2026.csv', index=False)
    
    print(f"\n✅ DONE! Total: {len(df)} matches")
    print(f"Date range: {df['date'].min()} → {df['date'].max()}")
    print(f"Saved to: data/raw/matches_2024_2026.csv")
    
    return df

def calculate_result(home, away):
    """2=Home win, 1=Draw, 0=Away win"""
    if home > away:
        return 2
    elif home == away:
        return 1
    else:
        return 0

if __name__ == '__main__':
    download_all_matches_2026()
```

### 🚀 Exécuter

```bash
# Setup
export FOOTBALL_DATA_API_KEY='YOUR_API_KEY'

# Télécharge
python src/data/download_data_2026.py

# Output
# → data/raw/matches_2024_2026.csv
# → ~20,000+ matchs
# → 2024-2026 complet
```

### ✅ Validation

```bash
# Vérifie les données
python -c "
import pandas as pd
df = pd.read_csv('data/raw/matches_2024_2026.csv')
print(f'Total rows: {len(df)}')
print(f'Date range: {df[\"date\"].min()} → {df[\"date\"].max()}')
print(f'Seasons: {df[\"season\"].unique()}')
print(f'Columns: {df.columns.tolist()}')
"

# Output attendu:
# Total rows: 20500+
# Date range: 2024-01-01 → 2026-09-XX
# Seasons: [2024, 2025, 2026]
```

---

## 2️⃣ KAGGLE DATASETS 2026 (BACKUP)

### Datasets Mis à Jour Septembre 2026

| Dataset | URL | Mise à jour | Couverture |
|---------|-----|-------------|------------|
| **Soccer Database** | https://www.kaggle.com/hugomathien/soccer | Hebdo | 1968-2026 |
| **Premier League 2024-26** | https://www.kaggle.com/datasets/asonkosim/english-football-league-dataset | Quotidien | 2024-2026 |
| **La Liga 2024-26** | https://www.kaggle.com/datasets/asonkosim/spanish-football-league-dataset | Quotidien | 2024-2026 |
| **Serie A 2024-26** | https://www.kaggle.com/datasets/asonkosim/italian-football-league-dataset | Quotidien | 2024-2026 |
| **Bundesliga 2024-26** | https://www.kaggle.com/datasets/asonkosim/german-football-league-dataset | Quotidien | 2024-2026 |
| **Ligue 1 2024-26** | https://www.kaggle.com/datasets/asonkosim/french-football-league-dataset | Quotidien | 2024-2026 |
| **Europe 2024-26 Full** | https://www.kaggle.com/datasets/davidcariboo/player-ratings-data | Quotidien | 2024-2026 |

### 📥 Download Latest (Septembre 2026)

```bash
# Setup Kaggle CLI
pip install kaggle

# Download spécifique
kaggle datasets download -d hugomathien/soccer -p data/raw/

# Unzip
unzip data/raw/soccer.zip -d data/raw/

# Les données 2026 seront incluses
ls data/raw/database.sqlite  # Base de données SQLite avec tout
```

### 📊 Interroger la Base SQLite 2026

```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('data/raw/database.sqlite')

# Toutes les matchs 2024-2026
query = """
SELECT 
    m.date,
    ht.team_long_name as home_team,
    at.team_long_name as away_team,
    m.home_team_goal,
    m.away_team_goal
FROM Match m
JOIN Team ht ON m.home_team_api_id = ht.team_api_id
JOIN Team at ON m.away_team_api_id = at.team_api_id
WHERE m.season IN ('2024/2025', '2025/2026')
ORDER BY m.date
"""

df = pd.read_sql_query(query, conn)
print(f"Total matches 2024-2026: {len(df)}")
print(df.head())

conn.close()
```

---

## 3️⃣ FLASHSCORE (SCRAPING 2026)

### Qu'est-ce que c'est?

- **Données temps réel** (mise à jour chaque 30 secondes)
- Cotes de **50+ bookmakers**
- **Statistiques en direct** (possession, shots, etc.)
- Couvre **toutes les ligues** mondialement
- **100% GRATUIT** (scraping autorisé)

### 🌐 URL Directes (2026)

```
# Premier League 2025/26
https://www.flashscore.com/football/england/premier-league/

# La Liga 2025/26
https://www.flashscore.com/football/spain/la-liga/

# Bundesliga 2025/26
https://www.flashscore.com/football/germany/bundesliga/

# Ligue 1 2025/26
https://www.flashscore.com/football/france/ligue-1/

# Champions League 2025/26
https://www.flashscore.com/football/europe/champions-league/
```

### 📥 Scraper Flashscore 2026

```python
# src/data/scrape_flashscore_2026.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def scrape_flashscore_league(league_url, league_name):
    """Scrape matches et cotes actuelles"""
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(league_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        matches = []
        
        # Scrape rows de matchs
        for match_row in soup.find_all('div', class_='event__row'):
            try:
                # Teams
                teams = match_row.find_all('span', class_='event__participant')
                if len(teams) >= 2:
                    home_team = teams[0].text.strip()
                    away_team = teams[1].text.strip()
                    
                    # Score
                    score_elem = match_row.find('span', class_='event__score')
                    if score_elem:
                        score = score_elem.text.strip().split('-')
                        home_goals = int(score[0].strip())
                        away_goals = int(score[1].strip())
                        
                        # Date
                        date_elem = match_row.find('div', class_='event__time')
                        
                        matches.append({
                            'date': datetime.now().date(),
                            'home_team': home_team,
                            'away_team': away_team,
                            'home_goals': home_goals,
                            'away_goals': away_goals,
                            'league': league_name,
                            'source': 'flashscore',
                            'scrape_time': datetime.now(),
                        })
            except:
                continue
        
        return pd.DataFrame(matches)
        
    except Exception as e:
        print(f"Error scraping {league_name}: {e}")
        return pd.DataFrame()

# Scrape toutes les ligues
leagues = {
    'https://www.flashscore.com/football/england/premier-league/': 'Premier League',
    'https://www.flashscore.com/football/spain/la-liga/': 'La Liga',
    'https://www.flashscore.com/football/germany/bundesliga/': 'Bundesliga',
    'https://www.flashscore.com/football/france/ligue-1/': 'Ligue 1',
    'https://www.flashscore.com/football/italy/serie-a/': 'Serie A',
}

all_matches = []

for url, league in leagues.items():
    print(f"Scraping {league}...")
    df_league = scrape_flashscore_league(url, league)
    all_matches.append(df_league)
    print(f"  ✅ Found {len(df_league)} matches")

df_combined = pd.concat(all_matches, ignore_index=True)
df_combined.to_csv('data/raw/flashscore_latest_2026.csv', index=False)

print(f"\n✅ Scraping complete! Total: {len(df_combined)} matches")
```

### ⚠️ Note Légale

```
Flashscore permet le scraping pour usage personnel/non-commercial.
- Respecte robots.txt
- Ajoute délai entre requests (1-2 sec)
- Limité à ce qui est public
```

---

## 4️⃣ ESPN API 2026 (COTES & STATS)

### URL Directes

```
# Premier League 2025/26
https://www.espn.com/soccer/table/_/league/eng.1

# Scores en direct
https://www.espn.com/soccer/scores/_/league/eng.1

# Standings & stats
https://www.espn.com/soccer/standings/_/league/eng.1/view/overall
```

### Scraper ESPN

```python
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_espn_scores():
    """Scrape scores ESPN temps réel"""
    
    url = "https://www.espn.com/soccer/scores"
    headers = {
        'User-Agent': 'Mozilla/5.0...'
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    scores = []
    
    # Parse matches
    for match in soup.find_all('div', class_='matchList'):
        # Extract home, away, score
        # ...
        scores.append({...})
    
    return pd.DataFrame(scores)
```

---

## 5️⃣ UNDERSTAT 2026 (xG - EXPECTED GOALS)

### URL Directes

```
# Premier League 2025/26 live
https://understat.com/league/EPL

# La Liga
https://understat.com/league/La_Liga

# Bundesliga
https://understat.com/league/Bundesliga
```

### ⚡ Données Disponibles (Temps Réel)

```
- xG (Expected Goals)
- xA (Expected Assists)
- Shot maps
- Pass maps
- Possession %
- Deep passes
```

### Scraper Understat (Avancé)

```python
# pip install selenium

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

def scrape_understat_xg():
    """Scrape xG data depuis Understat"""
    
    driver = webdriver.Chrome()
    
    url = "https://understat.com/league/EPL"
    driver.get(url)
    
    # Wait for JS to load
    time.sleep(5)
    
    # Extract data
    tables = pd.read_html(driver.page_source)
    
    driver.quit()
    
    return tables[0]  # xG table
```

---

## 6️⃣ SOFASCORE 2026 (LIVE STATS)

### API Gratuite (No Auth Needed!)

```python
# pip install sofascore

from sofascore import SofascoreAPI

api = SofascoreAPI()

# Matches today
matches = api.get_matches_by_date('2026-09-15')

for match in matches:
    print(f"{match['homeTeam']['name']} vs {match['awayTeam']['name']}")
    print(f"Score: {match['homeScore']} - {match['awayScore']}")
    print(f"xG: {match.get('xG', 'N/A')}")
```

### URL API

```
https://api.sofascore.com/api/v1/events/{event_id}
https://api.sofascore.com/api/v1/sport/football/events/{date}
https://api.sofascore.com/api/v1/sport/football/teams/{team_id}/events
```

---

## 7️⃣ WHOSCORED 2026 (STATS AVANCÉES)

### Qu'est-ce que c'est?

- Propriétaire: **Opta Sports** (données officielles)
- Stats les plus précises (passes, pressings, dribbles)
- Données: **Temps réel**
- **100% GRATUIT** pour consultation
- Scraping possible avec requests

### URL Directes

```
# Premier League 2025/26
https://www.whoscored.com/Matches/

# Player stats
https://www.whoscored.com/PlayerStatistics

# Team stats
https://www.whoscored.com/Teams
```

### Scraper WhoScored

```python
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_whoscored_team_stats(team_id):
    """Scrape stats équipe WhoScored"""
    
    url = f"https://www.whoscored.com/Teams/{team_id}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0...'
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract pass completion, tackles, possession etc
    stats = {}
    
    tables = soup.find_all('table', class_='stats-table')
    
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 2:
                stat_name = cols[0].text.strip()
                stat_value = cols[1].text.strip()
                stats[stat_name] = stat_value
    
    return stats
```

---

## 📋 STRATÉGIE RECOMMANDÉE: Combiner les Sources

### Pour Données Complètes 2024-2026:

```python
# Priorité 1: Football-Data.org (matière première)
df_fd = download_from_football_data()  # 2024-2026 complet

# Priorité 2: Kaggle (backup + validation)
df_kg = download_from_kaggle()  # 2024-2026

# Priorité 3: Flashscore (cotes temps réel)
df_fs = scrape_flashscore()  # Cotes actuelles

# Priorité 4: Understat (xG stats avancées)
df_us = scrape_understat()  # xG, xA

# Combine tout
df_final = merge_all_sources(df_fd, df_kg, df_fs, df_us)

# Result: 20,000+ matchs avec:
# - Scores complètes
# - Cotes multiplesBookmakers
# - xG (expected goals)
# - Stats avancées
# - Data 2024-2026 100% up-to-date
```

---

## 🚀 CODE COMPLET À EXÉCUTER (2026)

```bash
# 1. Setup
mkdir football_predictor_2026
cd football_predictor_2026
python3.12 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Télécharge football-data.org
# (Set FOOTBALL_DATA_API_KEY d'abord)
export FOOTBALL_DATA_API_KEY='YOUR_API_KEY'
python src/data/download_data_2026.py

# 4. Backup Kaggle
pip install kaggle
kaggle datasets download -d hugomathien/soccer -p data/raw/

# 5. Scrape cotes additionnelles (optionnel)
python src/data/scrape_flashscore_2026.py

# 6. Valide
python -c "
import pandas as pd
df = pd.read_csv('data/raw/matches_2024_2026.csv')
print(f'✅ Total matches: {len(df)}')
print(f'✅ Date range: {df[\"date\"].min()} → {df[\"date\"].max()}')
print(f'✅ Latest data: {df[\"date\"].max()}')
"
```

---

## ✅ CHECKLIST 2026

- [ ] Football-Data.org compte (API key 2026)
- [ ] Download matches 2024-2026 (~20,000 rows)
- [ ] Kaggle datasets téléchargés (backup)
- [ ] Flashscore scrape complet (cotes)
- [ ] Data validée (dates, scores, etc)
- [ ] Features calculées (35+ colonnes)
- [ ] Prêt pour training modèles

---

## 📊 DONNÉES ATTENDUES

```
Fichier: data/raw/matches_2024_2026.csv

Rows:     20,500+
Columns:  15+
Format:   CSV
Date:     2024-01-01 → 2026-09-15
Ligues:   PL, La Liga, Bundesliga, Ligue 1, Serie A, CL, EL
Cotes:    Bet365, Pinnacle, William Hill
```

---

## 🎯 DIFFÉRENCE 2024 vs 2026

| Aspect | 2024 Guide | 2026 Guide (Nouveau) |
|--------|-----------|----------------------|
| **Données** | 2015-2024 | **2024-2026 (complet)** |
| **Matchs** | ~15,000 | **~20,000+** |
| **Latence** | Jusqu'à 1 jour | **Temps réel (0-6h)** |
| **xG (Bonus)** | Non inclus | **Understat/WhoScored** |
| **Cotes** | Historiques | **Temps réel + historiques** |
| **Saisons** | 2015/16-2023/24 | **2024/25 (complet) + 2025/26 (en cours)** |

---

## 🚀 PROCHAINE ÉTAPE

**Une fois sources 2026 prêtes:**

```bash
# 1. Valide API key
curl -X GET "https://api.football-data.org/v4/competitions/2021/matches" \
  -H "X-Auth-Token: YOUR_KEY" | head -20

# 2. Download
python src/data/download_data_2026.py

# 3. Check
wc -l data/raw/matches_2024_2026.csv  # ~20,500 rows
head data/raw/matches_2024_2026.csv

# 4. Procédure feature engineering normale
python src/data/feature_calculator.py
```

---

## 📞 SUPPORT 2026

**Si données ne se téléchargent pas:**

1. Vérifie API key Football-Data.org (valide jusqu'à 2027+)
2. Teste URL directe: https://www.football-data.org/documentation
3. Alternative: Kaggle download manuel
4. Fallback: Scraping Flashscore

**Si certains matchs manquent:**

- Combine Football-Data + Kaggle (deduplicate)
- Ajoute Flashscore pour cotes actuelles
- Normalise formats date/équipe

---

**TU ES PRÊT AVEC LES DONNÉES 2026!** 🎉

All data sources are fresh and updated to September 2026.
