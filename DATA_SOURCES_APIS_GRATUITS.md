# 📊 SOURCES DE DONNÉES FOOTBALL - GUIDE COMPLET

## 🎯 Vue d'Ensemble

**Pour ce projet tu besoin:**
1. ✅ **API Football-Data.org** (Recommandé - facile)
2. ✅ **Kaggle Datasets** (Alternative - download direct)
3. ✅ **Jeff Sackmann GitHub** (Bonus - stats avancées)
4. ✅ **Understat (Optional)** - Si tu veux xG (expected goals)

---

## 1️⃣ FOOTBALL-DATA.ORG API (RECOMMANDÉ - FACILE)

### Qu'est-ce que c'est?
- Plateforme gratuite d'API football
- Couverture: **2015-2024** (9 ans complètes)
- Ligues: **PL, La Liga, Bundesliga, Ligue 1, Serie A, Champions League**
- **~15,000 matchs** disponibles
- Cotes: Bet365, Pinnacle, William Hill, etc.
- **100% GRATUIT** pour usage personnel

### 📝 Étape 1: Créer un Compte

1. **Va sur:** https://www.football-data.org/client/register

2. **Remplir le formulaire:**
   ```
   Email:         jimmy@example.com
   Mot de passe:  (choisir un)
   Prénom:        Jimmy
   Nom:           (ton nom)
   Accord:        ✓ J'accepte les conditions
   ```

3. **Clique: "Register"**

4. **Vérifie ton email**
   - Tu recevras un email de confirmation
   - Clique le lien pour activer

### 🔑 Étape 2: Obtenir l'API Key

1. **Login:** https://www.football-data.org/client/login
   ```
   Email:    jimmy@example.com
   Password: (ton mot de passe)
   ```

2. **Va à:** https://www.football-data.org/client/register
   (ou Profile → API Token)

3. **Tu verras ta clé:**
   ```
   X-Auth-Token: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
   ```

4. **Copie cette clé!**

### 💾 Étape 3: Configurer dans le Projet

**Fichier:** `src/utils/config.py`

```python
# Replace this line:
FOOTBALL_DATA_API_KEY = 'YOUR_API_KEY_HERE'

# With your actual key:
FOOTBALL_DATA_API_KEY = 'a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6'
```

### 🔗 Étape 4: Tester l'API

**Option A: Via Python (dans le projet)**
```bash
python src/data/download_data.py
# → Télécharge tous les matchs 2015-2024
# → Crée: data/raw/matches_2015_2024.csv
```

**Option B: Via cURL (pour tester)**
```bash
curl -X GET \
  "https://api.football-data.org/v4/competitions/2021/matches" \
  -H "X-Auth-Token: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"

# Doit retourner: JSON avec liste de matchs
```

**Option C: Via Postman (GUI)**
1. Télécharge Postman: https://www.postman.com/downloads/
2. Create new request
3. Method: GET
4. URL: `https://api.football-data.org/v4/competitions/2021/matches`
5. Headers:
   ```
   Key: X-Auth-Token
   Value: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
   ```
6. Send → Doit voir JSON

### 📥 Exemple Réponse

```json
{
  "matches": [
    {
      "id": 401428,
      "utcDate": "2023-08-12T12:30:00Z",
      "status": "FINISHED",
      "venue": "Stamford Bridge",
      "homeTeam": {
        "id": 51,
        "name": "Chelsea",
        "shortName": "CHE",
        "crest": "https://..."
      },
      "awayTeam": {
        "id": 563,
        "name": "Fulham",
        "shortName": "FUL",
        "crest": "https://..."
      },
      "score": {
        "fullTime": {
          "home": 1,
          "away": 0
        }
      },
      "odds": {
        "homeWin": 1.85,
        "draw": 3.50,
        "awayWin": 4.50
      }
    },
    ...
  ]
}
```

### 🎯 Ligues Disponibles (IDs)

```python
COMPETITIONS = {
    2021: "Premier League",           # England
    2014: "La Liga",                  # Spain
    2002: "Bundesliga",               # Germany
    2015: "Ligue 1",                  # France
    2019: "Serie A",                  # Italy
    2001: "UEFA Champions League",    # Europe
}
```

### ⚡ Limits

- **Rate limit:** 10 requests/minute (gratuit)
- **Historique:** 2000+ matchs disponibles
- **Free tier:** Limité mais suffisant pour ce projet
- **Premium:** https://www.football-data.org/pricing (si tu veux plus tard)

### ❌ Troubleshooting

**Problème: "401 Unauthorized"**
```
Solution: Vérifie l'API key dans config.py
- Copy-paste exact
- Pas d'espaces avant/après
- Vérifie sur football-data.org/client/login
```

**Problème: "429 Too Many Requests"**
```
Solution: Rate limit dépassé
- Attends 60 secondes
- Réduis frequency des calls
- Implémenter retry avec délai
```

**Problème: "404 Not Found"**
```
Solution: Competition ID incorrect
- Vérifie l'ID dans COMPETITIONS dict
- Utilise les IDs listés ci-dessus
```

---

## 2️⃣ KAGGLE DATASETS (ALTERNATIVE - DOWNLOAD DIRECT)

### Qu'est-ce que c'est?
- Plateforme gratuite avec datasets publics
- Football data précurated et nettoyé
- **Download direct** (pas d'API limit)
- Plusieurs ligues disponibles
- Alternative si Football-Data fails

### 📝 Étape 1: Créer un Compte Kaggle

1. **Va sur:** https://www.kaggle.com/settings/account

2. **Create Account** (si pas déjà)
   ```
   Email:         jimmy@example.com
   Mot de passe:  (choisir un)
   Prénom:        Jimmy
   ```

3. **Vérifie l'email**

### 🔑 Étape 2: Obtenir Kaggle API

1. **Va sur:** https://www.kaggle.com/settings/account

2. **Scroll jusqu'à:** "API"

3. **Clique:** "Create New API Token"
   ```
   Cela télécharge: kaggle.json
   ```

4. **Contenu du fichier:**
   ```json
   {
     "username": "jimmy",
     "key": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
   }
   ```

### 💾 Étape 3: Setup Kaggle CLI

**Windows:**
```bash
# 1. Installe Kaggle CLI
pip install kaggle

# 2. Place kaggle.json dans:
# C:\Users\YourUsername\.kaggle\kaggle.json

# 3. Test
kaggle datasets list
```

**Linux/Mac:**
```bash
# 1. Installe Kaggle CLI
pip install kaggle

# 2. Place kaggle.json dans:
# ~/.kaggle/kaggle.json

# 3. Set permissions
chmod 600 ~/.kaggle/kaggle.json

# 4. Test
kaggle datasets list
```

### 📥 Télécharger les Données

**Meilleur Dataset: Premier League (1968-2023)**

```bash
# 1. Télécharge
kaggle datasets download -d hugomathien/soccer -p data/raw/

# 2. Unzip
unzip data/raw/soccer.zip -d data/raw/

# 3. Tu auras:
# - database.sqlite (SQLite database)
# - CSV files (si disponibles)
```

**Alternative: Direct Download**

1. Va sur: https://www.kaggle.com/hugomathien/soccer
2. Clique: "Download"
3. Extrais le ZIP
4. Place les fichiers dans `data/raw/`

### 📊 Datasets Populaires

| Dataset | Ligue | Années | URL |
|---------|-------|--------|-----|
| **Soccer Database** | Multiple | 1968-2023 | https://www.kaggle.com/hugomathien/soccer |
| **Premier League** | PL | 2017-2023 | https://www.kaggle.com/asonkosim/english-football-league-dataset |
| **La Liga** | La Liga | 2015-2023 | https://www.kaggle.com/asonkosim/spanish-football-league-dataset |
| **Serie A** | Serie A | 2017-2023 | https://www.kaggle.com/asonkosim/italian-football-league-dataset |
| **Bundesliga** | Bundesliga | 2015-2023 | https://www.kaggle.com/asonkosim/german-football-league-dataset |

### 🔍 Chercher d'autres Datasets

```bash
# Recherche Kaggle
kaggle datasets search soccer -s rating --sort rating

# Ou via le web:
https://www.kaggle.com/search?q=football
```

### ❌ Troubleshooting

**Problème: "Credentials not found"**
```
Solution: kaggle.json pas au bon endroit
- Windows: C:\Users\YourUsername\.kaggle\kaggle.json
- Linux/Mac: ~/.kaggle/kaggle.json
```

**Problème: "403 Forbidden"**
```
Solution: 
1. Accepte les conditions sur Kaggle.com
2. Va sur https://www.kaggle.com/settings/account
3. Scroll jusqu'à "API" et crée nouveau token
```

---

## 3️⃣ JEFF SACKMANN GITHUB (BONUS - TENNIS + STATS)

### Qu'est-ce que c'est?
- Repository GitHub avec tennis + football data
- **CSV files précurated**
- Football: Historique plus anciens, stats détaillées
- Tennis: Complete ATP/WTA data (1968+)
- **100% gratuit, open source**

### 📝 Lien Direct

**Tennis Data:**
https://github.com/JeffSackmann/tennis_atp

```bash
# Clone (tout le repo)
git clone https://github.com/JeffSackmann/tennis_atp.git

# Ou download des CSV spécifiques
# https://github.com/JeffSackmann/tennis_atp/tree/master/atp_matches_*.csv
```

**Football Data (optionnel):**
https://github.com/JeffSackmann/soccer

```bash
git clone https://github.com/JeffSackmann/soccer.git
```

### 📊 Fichiers Disponibles

**Tennis:**
```
atp_matches_1968.csv
atp_matches_1969.csv
...
atp_matches_2024.csv
wta_matches_2000.csv
...
```

**Colonnes:**
```
tourney_id
tourney_name
surface
draw_size
tourney_level
tourney_date
match_num
winner_id
winner_seed
winner_entry
winner_name
winner_hand
winner_ht
winner_age
winner_rank
winner_rank_points
loser_id
...
score
best_of
minutes
w_ace
w_df
w_svpt
w_1stIn
w_1stWon
w_2ndWon
w_SvGms
w_bpSaved
w_bpFaced
l_ace
...
```

### 🔗 Utilisation pour Football

```bash
# Si tu veux data alternative à Football-Data.org:

# 1. Clone
git clone https://github.com/JeffSackmann/soccer.git

# 2. Les fichiers sont dans: data/
# - matchResults.csv (PL, La Liga, etc)
# - playerAttributes.csv
- playerValuesOverTime.csv

# 3. Import dans le projet:
import pandas as pd
df_jeff = pd.read_csv('soccer/data/matchResults.csv')
```

---

## 4️⃣ UNDERSTAT (OPTIONAL - EXPECTED GOALS xG)

### Qu'est-ce que c'est?
- Statistiques avancées (xG = expected goals)
- Plus précis que buts bruts
- **Payant** mais data disponible en scraping
- Optionnel pour ce projet (peut être ajouté plus tard)

### 🌐 Lien

https://understat.com/

### 📥 Comment Obtenir

**Option 1: Via leur website (Gratuit - limité)**
```
1. Va sur: https://understat.com/league/EPL
2. Chaque match affiche xG
3. Scrape avec BeautifulSoup (un peu compliqué)
```

**Option 2: Paid API**
```
$ ~ 500-1000/an (trop cher pour nous)
```

**Option 3: Pour plus tard (Week 11+)**
```
Si tu veux xG:
- Scrape Understat
- Ou utilise StatsBomb (gratuit pour certaines équipes)
- Ajoute dans feature engineering (optionnel)
```

---

## 🚀 RÉSUMÉ RAPIDE - CE QUE FAIRE MAINTENANT

### Semaine 1: Commandes à Exécuter

```bash
# 1. FOOTBALL-DATA.ORG Setup
# (a) Va sur: https://www.football-data.org/client/register
# (b) Crée compte
# (c) Obtiens API key
# (d) Ajoute dans src/utils/config.py

# 2. Télécharge données
python src/data/download_data.py
# ← Utilise Football-Data.org API
# ← Crée: data/raw/matches_2015_2024.csv
# ← Temps: 2-3 min

# 3. (OPTIONNEL) Kaggle backup
pip install kaggle
kaggle datasets download -d hugomathien/soccer -p data/raw/
unzip data/raw/soccer.zip -d data/raw/
```

### Total Temps Setup: **5-10 minutes**

---

## 📋 CHECKLIST SOURCES

Avant de démarrer le projet, valide:

- [ ] **Football-Data.org**
  - [ ] Compte créé
  - [ ] API key obtenue
  - [ ] Ajoutée dans config.py
  - [ ] Teste via cURL/Python
  
- [ ] **Kaggle (optionnel)**
  - [ ] Compte créé
  - [ ] kaggle.json téléchargé
  - [ ] Placé dans ~/.kaggle/
  
- [ ] **Dossiers Créés**
  - [ ] `data/raw/` existe
  - [ ] `data/processed/` existe
  - [ ] `models/` existe

---

## 🎯 PROCHAINE ÉTAPE

**Une fois sources setup:**

```bash
# 1. Valide API key
curl -X GET \
  "https://api.football-data.org/v4/competitions/2021/matches?season=2023" \
  -H "X-Auth-Token: YOUR_KEY"

# 2. Télécharge données
python src/data/download_data.py

# 3. Vérifie le fichier
head -5 data/raw/matches_2015_2024.csv
# Doit montrer: date, home_team, away_team, home_goals, away_goals, etc
```

---

## 💡 TIPS BONUS

### Limiter Données (pour tester rapide)

```python
# Dans download_data.py:
# Télécharge juste 2023 au lieu de 2015-2024

for season in range(2023, 2024):  # Juste 2023
    # Download...
```

### Cacher API Key (Sécurité)

```python
# .env file
FOOTBALL_DATA_API_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6

# Code
from dotenv import load_dotenv
import os
load_dotenv()
API_KEY = os.getenv('FOOTBALL_DATA_API_KEY')
```

### Backup & Sync

```bash
# Si tu changes machine, sauvegarder:
cp data/raw/matches_2015_2024.csv ~/backup/
# ou sync via Google Drive/Dropbox
```

---

## ✅ TU ES PRÊT!

Toutes les sources sont gratuites et accessibles.

**Prochaine action:**
1. Crée compte Football-Data.org
2. Obtiens API key
3. Ajoute dans config.py
4. Teste avec `python src/data/download_data.py`

**Des questions?** Demande dans le projet!

---

**BONNE CHANCE! 🚀**
