# 🎯 Football Predictor - Guide Complet du Projet

**Auteur:** Jimmy (Data Analyst / BI Developer)  
**Statut:** En cours de développement (Week 1)  
**Dernière mise à jour:** Septembre 2026  
**Timeline:** 13 semaines (3+ mois)

---

## 📋 Table des Matières

1. [Résumé du Projet](#résumé-du-projet)
2. [Contexte et Objectifs](#contexte-et-objectifs)
3. [Architecture Complète](#architecture-complète)
4. [Spécifications Techniques](#spécifications-techniques)
5. [Données Sources](#données-sources)
6. [Modèles ML (4 Marchés)](#modèles-ml-4-marchés)
7. [App Streamlit (5 Pages)](#app-streamlit-5-pages)
8. [Roadmap Détaillée (13 Semaines)](#roadmap-détaillée-13-semaines)
9. [Instructions d'Installation](#instructions-dinstallation)
10. [Pipeline d'Exécution](#pipeline-dexécution)
11. [Fichiers de Code](#fichiers-de-code)
12. [Validation et Testing](#validation-et-testing)
13. [FAQ & Troubleshooting](#faq--troubleshooting)

---

## Résumé du Projet

### Qu'est-ce que c'est?
Un **système complet de prédiction de résultats sportifs (football)** avec:
- **4 modèles ML** pour prédire différents marchés de paris
- **App Streamlit** interactive pour tester avec argent virtuel
- **Walk-forward validation** rigoureuse (2020-2024)
- **Portfolio piece** professionnel et deployable

### Objectifs Principaux
✅ Développer modèles ML performants pour prédire résultats football  
✅ Valider stratégie sur argent virtuel AVANT de parier réel  
✅ Créer app Streamlit complète et utilisable  
✅ Portfolio project montrant compétences ML/BI/Data Engineering  
✅ Après football: répliquer architecture pour tennis  

### Caractéristiques Clés
- **Types de paris implémentés:** 1X2 (Match Result), Over/Under (Buts), Both Teams Score, Score Exact
- **Ligues couvertes:** Premier League, La Liga, Bundesliga, Ligue 1, Serie A, Champions League
- **Données:** Football-Data.org + Kaggle (gratuit)
- **Validation:** Walk-Forward (2020-2024)
- **Argent virtuel:** 1000$ pour simuler stratégies
- **Deployment:** Local + Streamlit Cloud

---

## Contexte et Objectifs

### Profil de Jimmy
- **Titre:** Data Analyst / BI Developer
- **Base:** Dschang, Cameroon
- **Formation:** 
  - Licence Professionnelle SIAD (Université de Dschang) - Mention Bien
  - BTS Génie Logiciel (ISSTN) - Mention Assez Bien
  - Google Data Analytics Certificate
- **Expérience:** Projets data/BI (portfolio en développement)
- **Skills actuels:** Excel, SQL, Pandas, Power BI, quelques ML basics
- **Cible carrière:** Junior Data Analyst / BI Developer roles (3-6 mois)

### Spécification du Projet (Décisions Prises)
| Aspect | Choix | Raison |
|--------|-------|--------|
| **Sport prioritaire** | Football | Données massives, alpha meilleur que tennis |
| **Types de paris** | TOUS 4 (1X2, O/U, BTS, Exact) | Portfolio plus complet |
| **Validation** | Argent virtuel dans app | Pas de risque réel d'abord |
| **Python version** | 3.12.4 | Moderne, compatible |
| **Données** | Football-Data.org + Kaggle | Gratuit, suffisant |
| **Premium data** | Non (xG, StatssBomb, etc) | Pas nécessaire |
| **Deployment** | Local + Streamlit Cloud | Flexible, accessible |

### What Success Looks Like
✅ **Portfolio:** Repo GitHub public avec 500+ stars, Streamlit app live  
✅ **Performance:** ROI +5% simulé sur 2024 (50+ paris)  
✅ **Documentation:** Code professionnel, README complet, Jupyter notebooks  
✅ **Transportabilité:** Même pipeline pour tennis (généralizable)  

---

## Architecture Complète

### Vue d'Ensemble (Diagramme Conceptuel)

```
┌─────────────────────────────────────────────────────────────────┐
│                     FOOTBALL PREDICTOR                          │
│                   (13-Week Development)                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┼─────────────┐
                ↓             ↓             ↓
        ┌──────────────┐  ┌──────────┐  ┌──────────────┐
        │ DATA LAYER   │  │ ML LAYER │  │ APP LAYER    │
        │ (Week 1)     │  │ (Week 2-3)  (Week 4-7)
        └──────────────┘  └──────────┘  └──────────────┘
                │             │             │
        ┌───────┴─────────────┴─────────────┴────────┐
        │                                             │
        ↓                                             ↓
    DATA SOURCES                          STREAMLIT APP (5 Pages)
    ├─ Football-Data.org                  ├─ Dashboard
    ├─ Kaggle                             ├─ Simulator
    └─ Processed Features                 ├─ Backtest
                                          ├─ Monitoring
    MODELS (4)                            └─ Analysis
    ├─ Model 1X2 (3-class)
    ├─ Model O/U (Regression)
    ├─ Model BTS (Dual)                  BETTING ENGINE
    └─ Model Exact (Poisson)             ├─ EV Calculator
                                         ├─ Kelly Criterion
                                         └─ Virtual Bankroll
```

### Composants Clés

#### 1. Data Pipeline
```
Raw Data (Football-Data) 
  ↓
Data Processor (Clean, normalize)
  ↓
Feature Calculator (35+ features)
  ↓
Processed Features (10k+ rows × 35+ cols)
  ↓
Train/Test Splits (Walk-Forward 2020-2024)
```

#### 2. ML Models
```
Features → LightGBM/XGBoost →
├─ Model 1X2: P(Home), P(Draw), P(Away)
├─ Model O/U: P(Over 2.5), P(Under 2.5)
├─ Model BTS: P(Both Score), P(No Both)
└─ Model Exact: Top 5 most probable scores
```

#### 3. Betting Engine
```
Prediction + Odds →
├─ EV Calculator
├─ Kelly Criterion
├─ Bet Size Calculator
├─ Virtual Settlement
└─ Performance Tracking
```

#### 4. Streamlit App
```
Web Interface →
├─ Page 1: Dashboard (upcoming matches + predictions)
├─ Page 2: Simulator (place virtual bets)
├─ Page 3: Backtest (walk-forward results)
├─ Page 4: Monitoring (model performance)
└─ Page 5: Analysis (detailed stats)
```

---

## Spécifications Techniques

### Stack Technologique

**Core Libraries**
```
Python 3.12.4
├─ Data Processing: Pandas 2.1.4, NumPy 1.24.3
├─ ML Models: LightGBM 4.1.1, XGBoost 2.0.3, Scikit-learn 1.3.2
├─ Statistics: SciPy 1.11.4 (Poisson distribution)
├─ Web App: Streamlit 1.31.0
├─ Visualization: Plotly 5.18.0, Matplotlib 3.8.2
├─ APIs: Requests 2.31.0, BeautifulSoup4 4.12.2
├─ Utilities: Joblib, Optuna (hyperparameter tuning)
└─ Testing: Pytest 7.4.3
```

**Installation**
```bash
# Virtual Environment
python3.12 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install Dependencies
pip install -r requirements.txt
```

### Environment Setup

**API Keys Required**
```bash
# 1. Football-Data.org API Key
FOOTBALL_DATA_API_KEY='YOUR_KEY_HERE'
# → Get from: https://www.football-data.org/client/register

# 2. Kaggle API (Optional)
# → Download from: https://www.kaggle.com/settings/account
# → Place in: ~/.kaggle/kaggle.json
```

**Configuration**
```python
# src/utils/config.py
FOOTBALL_DATA_API_KEY = 'YOUR_KEY'
DATA_START_YEAR = 2015
DATA_END_YEAR = 2024
COMPETITIONS = {
    'PL': 2021,
    'LA_LIGA': 2014,
    'BUNDESLIGA': 2002,
    'LIGUE_1': 2015,
    'SERIE_A': 2019,
    'CL': 2001,
}
```

### Requirements.txt
```
pandas==2.1.4
numpy==1.24.3
scipy==1.11.4
scikit-learn==1.3.2
lightgbm==4.1.1
xgboost==2.0.3
optuna==3.14.0
requests==2.31.0
beautifulsoup4==4.12.2
streamlit==1.31.0
plotly==5.18.0
matplotlib==3.8.2
seaborn==0.13.0
pytest==7.4.3
jupyter==1.0.0
```

---

## Données Sources

### Football-Data.org API

**Qu'est-ce que c'est?**
- Plateforme gratuite d'API football
- Données: 2015-2024 (complètes)
- Couverture: ~15k matchs (PL, La Liga, Bundesliga, Ligue 1, Serie A, CL)
- Cotes: Bet365, Pinnacle, William Hill, etc.

**Setup**
```bash
# 1. Crée compte sur https://www.football-data.org
# 2. Obtiens API key (gratuit)
# 3. Ajoute à config.py
# 4. Appel API:

GET https://api.football-data.org/v4/competitions/{id}/matches?season=2023
Headers: X-Auth-Token: YOUR_KEY

# Retourne:
{
  "matches": [
    {
      "utcDate": "2023-08-12T12:30:00Z",
      "homeTeam": {"name": "Chelsea"},
      "awayTeam": {"name": "Fulham"},
      "score": {
        "fullTime": {"home": 1, "away": 0}
      }
    }
  ]
}
```

### Kaggle Datasets

**Datasets Disponibles**
```
1. Premier League Matches (1968-2023)
   → kaggle datasets download -d hugomathien/soccer
   
2. Kaggle Football Match Data
   → Plus de stats et contexte
   
3. Understat Data (Optional)
   → xG, xA (expected goals/assists)
   → Besoin scraping + API
```

**Utilisation**
```python
# Automatique si disponible, sinon skip
# data/download_data.py détecte et combine automatiquement
```

### Schéma des Données Brutes

**Tableau: Matches**
```
date (datetime)
home_team (string)
away_team (string)
home_goals (int)
away_goals (int)
result (int: 2=home win, 1=draw, 0=away win)
league_id (int)
season (int)
odds_1 (float)
odds_x (float)
odds_2 (float)
```

**Données Calculées (Features)**
```
35+ colonnes incluant:
- home/away win_pct (10, 20 match windows)
- home/away goals_for/against
- ELO ratings
- Jours de repos
- Streaks (W/L current)
- H2H records
- Cotes implicites
- Indicateurs contexte
```

---

## Modèles ML (4 Marchés)

### Vue d'Ensemble

| Marché | Modèle | Type | Input | Output | Probabilités |
|--------|--------|------|-------|--------|--------------|
| **1X2** | LightGBM | Classification 3-class | 35 features | Home/Draw/Away | P(H), P(D), P(A) |
| **O/U** | LightGBM Regr | Regression + Poisson | 25 features | Over/Under 2.5 | P(>2.5), P(<2.5) |
| **BTS** | LightGBM Dual | Dual Classification | 25 features | Both Teams Score | P(Yes), P(No) |
| **Exact** | LightGBM Regr × 2 | Poisson bivariée | 20 features | Score exact | Matrix 4×4 |

### Détail Modèle 1: Match Result (1X2)

**Objectif**
Prédire résultat du match: Home Win, Draw, Away Win

**Type**
Multiclass Classification (3 classes: 0=Away, 1=Draw, 2=Home)

**Features (35 colonnes)**
```
HOME TEAM:
- home_win_pct_10/20 (% victoires derniers 10/20 matchs)
- home_goals_for_10/20 (buts marqués par match)
- home_goals_against_10/20 (buts encaissés par match)
- home_elo (rating Elo)
- home_days_rest (jours depuis dernier match)
- home_streak (W/L streak courant)

AWAY TEAM:
- away_win_pct_10/20
- away_goals_for_10/20
- away_goals_against_10/20
- away_elo
- away_days_rest
- away_streak

CONTEXT:
- elo_diff (home_elo - away_elo)
- h2h_home_wins, h2h_draws, h2h_total
- h2h_home_pct (% victoires vs opponent)
- prob_home_implicit (de cotes: 1/odds_1)
- prob_draw_implicit
- prob_away_implicit
- bookmaker_margin
- league_strength_factor
- month_of_year
- is_weekend
- day_of_week
```

**Algorithme**
```python
model = LGBMClassifier(
    num_class=3,
    learning_rate=0.05,
    num_leaves=15,
    max_depth=7,
    lambda_l1=5,
    lambda_l2=5,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
)

# Output: P(class 0), P(class 1), P(class 2)
```

**Output**
```python
{
    'away': array([0.25, 0.30, ...]),  # P(Away wins)
    'draw': array([0.35, 0.40, ...]),  # P(Draw)
    'home': array([0.40, 0.30, ...]),  # P(Home wins)
}
```

**Performance Expected**
- Accuracy: 52-55% (vs 33% random)
- Log Loss: 0.90-1.00
- AUC-ROC: 0.60-0.65

---

### Détail Modèle 2: Over/Under (Buts)

**Objectif**
Prédire nombre total de buts → P(Total > 2.5)

**Approche**
1. Régression: Prédis buts totaux (λ via Poisson)
2. Proportions: Ratio buts home vs away
3. Poisson CDF: Calcule P(Over/Under 2.5)

**Formule Poisson**
```
Λ (lambda) = expected_total_goals
P(k) = (e^-λ × λ^k) / k!

P(Total > 2.5) = 1 - P(Total ≤ 2)
                = 1 - [P(0) + P(1) + P(2)]
```

**Features (25 colonnes)**
```
Attaque/Défense:
- home_goals_for_10/20
- home_goals_against_10/20
- away_goals_for_10/20
- away_goals_against_10/20

Rating:
- home_elo
- away_elo
- elo_diff

Context:
- league_strength
- is_weekend
- month_of_year
```

**Output**
```python
{
    'expected_total': array([2.3, 2.8, ...]),  # Buts attendus
    'expected_home': array([1.2, 1.5, ...]),   # Buts domicile
    'expected_away': array([1.1, 1.3, ...]),   # Buts extérieur
    'prob_over_2_5': array([0.45, 0.62, ...]), # P(>2.5)
    'prob_under_2_5': array([0.55, 0.38, ...]),# P(<2.5)
}
```

---

### Détail Modèle 3: Both Teams Score (BTS)

**Objectif**
Prédire si les deux équipes marquent au moins 1 but

**Approche**
Dual classification:
1. Model A: P(Home scores)? (1/0)
2. Model B: P(Away scores)? (1/0)
3. Combine: P(BTS) = P(Home) × P(Away) [simplifié, ignore corrélation]

**Features (25 colonnes)**
Similaires à 1X2 et O/U, focus sur attaque/défense

**Output**
```python
{
    'prob_home_scores': array([0.65, 0.70, ...]),
    'prob_away_scores': array([0.45, 0.55, ...]),
    'prob_bts': array([0.29, 0.39, ...]),        # P(Both)
    'prob_no_bts': array([0.71, 0.61, ...]),     # P(Not Both)
}
```

---

### Détail Modèle 4: Score Exact

**Objectif**
Prédire score exact du match (ex: 2-1, 1-1, 3-0)

**Approche**
Poisson bivariée:
1. Model A: Régresse buts domicile (λ₁)
2. Model B: Régresse buts extérieur (λ₂)
3. Matrice: P(H-A) = Poisson(H, λ₁) × Poisson(A, λ₂)

**Features (20 colonnes)**
Attaque/défense focus

**Output**
```python
[
    {
        'lambda_home': 1.8,
        'lambda_away': 1.1,
        'score_matrix': {
            '0-0': 0.082,
            '1-0': 0.148,
            '2-0': 0.133,
            ...
        },
        'top_5_scores': [
            ('1-0', 0.148),
            ('1-1', 0.128),
            ('2-0', 0.133),
            ('2-1', 0.122),
            ('0-1', 0.090),
        ]
    },
    ...
]
```

---

### Training Pipeline

**Pseudo-Code Complet**

```python
# 1. Load features
features_df = pd.read_csv('data/processed/features_complete.csv')

# 2. Prepare data
X = features_df[feature_columns]
y_1x2 = features_df['result']
y_ou = features_df['total_goals']
y_bts_home = (features_df['home_goals'] > 0).astype(int)
y_bts_away = (features_df['away_goals'] > 0).astype(int)

# 3. Walk-Forward Validation
models = {}
for year in [2020, 2021, 2022, 2023, 2024]:
    # Split
    train = features_df[features_df['year'] < year]
    test = features_df[features_df['year'] == year]
    
    # Train Model 1X2
    model_1x2 = LGBMClassifier(...)
    model_1x2.fit(train[features], train['result'])
    
    # Evaluate
    y_pred = model_1x2.predict_proba(test[features])
    auc = roc_auc_score(test['result'], y_pred[:, 2])
    
    # Save
    models[year] = {
        '1x2': model_1x2,
        'auc': auc,
        ...
    }

# 4. Final training on all data
for model_name in ['1x2', 'ou', 'bts', 'exact']:
    model = Model[model_name](...)
    model.fit(X, y)
    model.save(f'models/{model_name}.pkl')
```

---

## App Streamlit (5 Pages)

### Architecture App

```
Streamlit Cloud URL: https://your-username-football-predictor.streamlit.app/
                            │
        ┌───────────────────┼───────────────────┐
        ↓                   ↓                   ↓
    Sidebar          Main Content          Session State
    (Navigation)     (Page Content)        (Bankroll, Cache)
    
    Pages:
    ├─ 01_Dashboard.py
    ├─ 02_Simulator.py
    ├─ 03_Backtest.py
    ├─ 04_Monitoring.py
    └─ 05_Analysis.py
```

### Page 1: Dashboard

**Objectif**
Afficher matches de la semaine prochaine + prédictions live

**Composants**
```
Left Column (60%):
├─ Match 1
│  ├─ Chelsea vs Man City
│  ├─ Premier League | 15 Sep 2026, 15:00
│  └─ Prediction: Home 45% | Draw 27% | Away 28%
│       Over 60% | BTS 55%
│
├─ Match 2
│  └─ ... (similar)
│
└─ Match N

Right Column (40%):
├─ Virtual Bankroll
│  ├─ Balance: $1,000.00
│  ├─ Week ROI: +2.5%
│  └─ Total Bets: 12
│
└─ Quick Stats
   ├─ Win Rate: 54%
   ├─ Avg EV: +2.1%
   └─ Sharpe Ratio: 0.45
```

**Fonctionnalité**
```python
# Load upcoming matches from API
upcoming = get_upcoming_matches_week()

# For each match:
for match in upcoming:
    features = calculate_features(match)
    
    pred_1x2 = model_1x2.predict([features])
    pred_ou = model_ou.predict([features])
    pred_bts = model_bts.predict([features])
    
    # Display
    st.metric(f"{match.home} Win %", f"{pred_1x2['home'][0]:.0%}")
    st.metric(f"Over 2.5 %", f"{pred_ou['over_2_5'][0]:.0%}")
    st.metric(f"BTS %", f"{pred_bts['prob_bts'][0]:.0%}")
```

---

### Page 2: Simulator

**Objectif**
Tester stratégie de paris sur matchs passés avec argent virtuel

**Workflow**
```
1. Select Date
   ↓
2. Select Match
   ↓
3. View Predictions (1X2, O/U, BTS, Exact)
   ↓
4. Choose Bet Type & Amount
   ↓
5. See EV & Kelly Calculation
   ↓
6. Place Bet
   ↓
7. See Result & Updated Balance
```

**Détail Étapes**

**Étape 1-2: Selection Match**
```python
sim_date = st.date_input("Select match date")
matches = load_matches_by_date(sim_date)
selected = st.selectbox("Select match", 
                        [f"{m['home']} vs {m['away']}" for m in matches])
```

**Étape 3: View Predictions**
```python
match = get_match_data(selected)
features = calculate_features(match)

# Get predictions from all 4 models
pred_1x2 = model_1x2.predict([features])
pred_ou = model_ou.predict([features])
pred_bts = model_bts.predict([features])
pred_exact = model_exact.predict([features])

# Display
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("P(Home Win)", f"{pred_1x2['home'][0]:.0%}")
    st.metric("P(Draw)", f"{pred_1x2['draw'][0]:.0%}")
    st.metric("P(Away Win)", f"{pred_1x2['away'][0]:.0%}")

with col2:
    st.metric("P(Over 2.5)", f"{pred_ou['over'][0]:.0%}")
    st.metric("P(Under 2.5)", f"{pred_ou['under'][0]:.0%}")

with col3:
    st.metric("P(BTS)", f"{pred_bts['bts'][0]:.0%}")
    st.metric("P(No BTS)", f"{pred_bts['no_bts'][0]:.0%}")

with col4:
    st.metric("Top Score", pred_exact['top_1_score'])
    st.metric("Prob", f"{pred_exact['top_1_prob']:.1%}")
```

**Étape 4: Choose Bet**
```python
bet_type = st.selectbox("Bet Type", ["1X2", "Over/Under", "BTS", "Exact"])

if bet_type == "1X2":
    outcome = st.selectbox("Outcome", ["Home Win", "Draw", "Away Win"])
    odds = match.get_odds(outcome)
    proba = pred_1x2[outcome]
elif bet_type == "Over/Under":
    outcome = st.selectbox("Outcome", ["Over 2.5", "Under 2.5"])
    odds = 1.90  # Default
    proba = pred_ou[outcome]
...

bet_amount = st.number_input("Bet Amount ($)", min_value=1, max_value=100, value=10)
```

**Étape 5-6: EV & Kelly**
```python
ev = betting_engine.calculate_ev(proba, odds)
kelly = betting_engine.calculate_kelly_fraction(proba, odds)
suggested_size = betting_engine.calculate_bet_size(proba, odds)

st.info(f"""
**Expected Value:** {ev:+.2%}
**Implied Prob:** {1/odds:.0%}
**Predicted Prob:** {proba:.0%}
**Kelly Fraction:** {kelly:.1%}
**Suggested Bet:** ${suggested_size:.2f}
""")

if st.button("Place Bet"):
    # Simulate result based on actual match
    actual_result = match.get_actual_result()
    won = betting_engine.check_win(outcome, actual_result)
    
    if won:
        profit = bet_amount * (odds - 1)
        st.success(f"✅ BET WON! +${profit:.2f}")
    else:
        st.error(f"❌ BET LOST! -${bet_amount:.2f}")
    
    st.session_state.bankroll += profit if won else -bet_amount
```

**Étape 7: Tracking**
```python
st.session_state.total_bets += 1
st.session_state.bets_history.append({
    'date': sim_date,
    'match': selected,
    'bet_type': bet_type,
    'outcome': outcome,
    'odds': odds,
    'amount': bet_amount,
    'result': 'WIN' if won else 'LOSS',
    'pnl': profit if won else -bet_amount,
})
```

---

### Page 3: Backtest

**Objectif**
Run walk-forward validation complète sur 2020-2024

**Workflow**
```
1. Configure Parameters
   ├─ Initial Capital: $1000
   ├─ Kelly Fraction: 25%
   └─ Min EV Threshold: 5%
   
2. Run Backtest
   ├─ Boucle 2020-2024
   ├─ Entraîne modèle avant année
   ├─ Teste sur année
   └─ Simule paris réels
   
3. Display Results
   ├─ Equity Curve
   ├─ Statistics
   ├─ Performance par marché
   └─ Detailed Bets Table
```

**Configuration**
```python
col1, col2, col3 = st.columns(3)

with col1:
    initial_capital = st.number_input(
        "Initial Capital",
        value=1000,
        min_value=100,
        max_value=10000,
        step=100
    )

with col2:
    kelly_fraction = st.slider(
        "Kelly Fraction",
        min_value=0.1,
        max_value=1.0,
        value=0.25,
        step=0.05
    )

with col3:
    min_ev = st.slider(
        "Min EV Threshold (%)",
        min_value=1,
        max_value=10,
        value=5,
        step=1
    )

if st.button("Run Backtest", type="primary"):
    with st.spinner("Running backtest..."):
        results = run_walk_forward_backtest(
            initial_capital=initial_capital,
            kelly_fraction=kelly_fraction,
            min_ev_threshold=min_ev / 100
        )
```

**Résultats Affichés**
```python
# High-level metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    roi = (results['final_capital'] - initial_capital) / initial_capital
    st.metric("Final Capital", f"${results['final_capital']:.0f}")
    st.metric("ROI", f"{roi:+.1%}")

with col2:
    st.metric("Total Bets", results['n_bets'])
    st.metric("Win Rate", f"{results['win_rate']:.1%}")

with col3:
    st.metric("Sharpe Ratio", f"{results['sharpe']:.2f}")
    st.metric("Avg EV", f"{results['avg_ev']:+.2%}")

with col4:
    st.metric("Max Drawdown", f"{results['max_drawdown']:.1%}")
    st.metric("Consecutive Losses", results['max_consecutive_losses'])

# Equity Curve
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=results['equity_df']['date'],
    y=results['equity_df']['balance'],
    mode='lines+markers',
    name='Balance',
    line=dict(color='#00CC88', width=2)
))
fig.update_layout(
    title="Equity Curve (2020-2024)",
    xaxis_title="Date",
    yaxis_title="Capital ($)",
    hovermode='x unified',
    height=500,
)
st.plotly_chart(fig, use_container_width=True)

# Performance par type de pari
col1, col2, col3, col4 = st.columns(4)

for bet_type, col in zip(['1X2', 'Over/Under', 'BTS', 'Exact'], [col1, col2, col3, col4]):
    bets_type = results['bets_df'][results['bets_df']['bet_type'] == bet_type]
    if len(bets_type) > 0:
        roi_type = bets_type['pnl'].sum() / bets_type['bet_size'].sum()
        with col:
            st.metric(
                f"{bet_type} ROI",
                f"{roi_type:+.1%}",
                f"{len(bets_type)} bets"
            )

# Detailed Bets Table
st.subheader("Detailed Bets")
st.dataframe(
    results['bets_df'][[
        'date', 'home', 'away', 'bet_type', 'outcome',
        'odds', 'bet_size', 'ev', 'pnl', 'balance'
    ]].head(100),
    use_container_width=True,
    height=400
)
```

---

### Page 4: Monitoring

**Objectif**
Monitor performance des modèles (calibration, feature importance, drift)

**Sections**

**1. Calibration Curves**
```python
# Pour chaque modèle, affiche:
# - Predicted Probability vs Actual Frequency
# - Ideal = 45° line

for model_name in ['1x2', 'ou', 'bts']:
    model = models[model_name]
    plot_calibration_curve(model)
```

**2. Feature Importance**
```python
# Top 15 features
fig = px.bar(
    feature_importance_df.head(15),
    x='importance',
    y='feature',
    orientation='h',
    title='Feature Importance (1X2 Model)'
)
st.plotly_chart(fig)
```

**3. Performance par Année**
```
Year  | ROI   | Win Rate | Sharpe | Avg EV | N Bets
------|-------|----------|--------|--------|-------
2020  | +3.2% | 54%      | 0.32   | +2.1%  | 180
2021  | +1.8% | 52%      | 0.18   | +1.9%  | 176
2022  | +2.5% | 53%      | 0.28   | +2.0%  | 182
2023  | +1.1% | 51%      | 0.12   | +1.5%  | 174
2024  | +4.2% | 56%      | 0.42   | +2.8%  | 168
```

---

### Page 5: Analysis

**Objectif**
Analyse détaillée des prédictions et patterns

**Sections**

**1. Model Comparison**
```
Model      | Accuracy | AUC   | LogLoss | Precision | Recall
-----------|----------|-------|---------|-----------|--------
1X2        | 54.3%    | 0.615 | 0.948   | 58%       | 52%
Over/Under | 56.1%    | 0.628 | 0.912   | 61%       | 54%
BTS        | 63.2%    | 0.687 | 0.854   | 68%       | 59%
Exact      | 12.4%    | 0.542 | 1.245   | 14%       | 10%
```

**2. Prediction Distribution**
```python
# Histogram of predicted probabilities
fig = px.histogram(
    predictions_df,
    x='predicted_prob',
    nbins=20,
    title='Distribution of Predicted Probabilities',
    labels={'predicted_prob': 'Predicted Probability'}
)
st.plotly_chart(fig)
```

**3. Winning vs Losing Patterns**
```python
# Features most common in winning bets vs losing bets
comparison_df = analyze_feature_patterns(bets_df)
st.dataframe(comparison_df)
```

---

## Roadmap Détaillée (13 Semaines)

### WEEK 1: Data & Setup (Semaine Actuelle)

**Objectifs**
- ✅ Setup Python environment
- ✅ Get Football-Data API key
- ✅ Download historical data
- ✅ Initial data exploration

**Tâches**

```bash
# 1. Create project structure
mkdir football_predictor
cd football_predictor
git init

# 2. Setup Python
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Get API key
# → Visit https://www.football-data.org/client/register
# → Copy API key
# → Add to src/utils/config.py

# 4. Download data
python src/data/download_data.py
# Expected output: data/raw/matches_2015_2024.csv (~15k rows)

# 5. Initial exploration
jupyter notebook notebooks/01_data_exploration.ipynb
# Plots, stats, distributions, outliers
```

**Deliverables**
```
✓ requirements.txt
✓ src/utils/config.py (with API key)
✓ data/raw/matches_2015_2024.csv
✓ notebooks/01_data_exploration.ipynb
```

**Success Criteria**
- Data downloaded successfully (no API errors)
- 10k+ matches in CSV
- All columns present (date, home, away, score, odds)
- Data quality checked (nulls, duplicates, date ranges)

---

### WEEK 2: Feature Engineering

**Objectifs**
- Calculer 35+ features
- Handle edge cases
- Prepare pour training

**Tâches**

```bash
# 1. Calculate features
python src/data/feature_calculator.py
# Expected output: data/processed/features_complete.csv (~9k rows)

# 2. Feature exploration
jupyter notebook notebooks/02_feature_engineering.ipynb
# Feature distributions, correlations, univariate analysis

# 3. Validate features
# Check: no NaNs, correct data types, reasonable ranges
```

**Deliverables**
```
✓ data/processed/features_complete.csv
✓ notebooks/02_feature_engineering.ipynb
```

**Success Criteria**
- All 35+ features calculated
- No missing values in features
- Features have reasonable ranges (e.g., win_pct 0-1, elo 1300-1700)
- Correlations computed

---

### WEEK 3: Model Training (1X2 + O/U)

**Objectifs**
- Train Model 1X2 (classification)
- Train Model Over/Under (regression)
- Walk-forward validation setup

**Tâches**

```bash
# 1. Build & train models
python src/models/training.py
# Trains: Model1X2, ModelOverUnder

# 2. Walk-forward validation (2020-2024)
# For each year:
#   - Train on all previous years
#   - Test on that year
#   - Record: AUC, accuracy, Sharpe

# 3. Hyperparameter tuning (optional)
# python src/models/optuna_tuning.py

# 4. Save models
# models/1x2.pkl
# models/ou.pkl
```

**Expected Results**
```
Year | Model | Accuracy | AUC   | Sharpe
-----|-------|----------|-------|-------
2020 | 1X2   | 54.1%    | 0.612 | 0.15
2021 | 1X2   | 52.8%    | 0.608 | 0.08
2022 | 1X2   | 55.3%    | 0.615 | 0.12
2023 | 1X2   | 53.1%    | 0.605 | 0.05
2024 | 1X2   | 54.9%    | 0.620 | 0.18
-----|-------|----------|-------|-------
2020 | O/U   | 56.2%    | 0.628 | 0.22
2021 | O/U   | 55.4%    | 0.620 | 0.18
...
```

**Deliverables**
```
✓ src/models/models_complete.py
✓ src/models/training.py
✓ models/1x2.pkl
✓ models/ou.pkl
✓ notebooks/03_model_training.ipynb
```

**Success Criteria**
- Both models train without errors
- Accuracy > 50% (better than random 33%)
- AUC > 0.55 (better than random 0.5)
- Walk-forward stable (similar year-to-year)

---

### WEEK 4: Models BTS + Exact

**Objectifs**
- Train Model BTS (dual classification)
- Train Model Exact Score (Poisson)
- Combine all 4 models

**Tâches**

```bash
# 1. Build BTS model
python src/models/training.py --model bts

# 2. Build Exact Score model
python src/models/training.py --model exact

# 3. Validate all 4 models
# Check prediction correlations (shouldn't be perfectly correlated)

# 4. Save all models
# models/bts.pkl
# models/exact.pkl

# 5. Create model loader utility
# src/models/loader.py: load_all_models()
```

**Deliverables**
```
✓ models/bts.pkl
✓ models/exact.pkl
✓ src/models/loader.py
```

**Success Criteria**
- All 4 models train and save
- Predictions sum to 100% (for 1X2)
- Reasonable probabilities (0-1 range)

---

### WEEK 5: Betting Engine + Simulator

**Objectifs**
- Implement EV calculator
- Implement Kelly Criterion
- Create bet simulator

**Tâches**

```bash
# 1. Build betting engine
# src/betting/betting_engine.py
python tests/test_betting_engine.py

# 2. Create simulator
# src/betting/bet_simulator.py

# 3. Test on sample data
# Example: 10 virtual bets with known outcomes

# 4. Integration tests
# Verify: EV calc, Kelly calc, settlement logic
```

**Test Cases**
```python
# Test 1: EV Calculation
assert calculate_ev(0.60, 2.0) == 0.20  # +20%
assert calculate_ev(0.40, 2.0) == -0.20  # -20%

# Test 2: Kelly Criterion
kelly = calculate_kelly(0.60, 2.0)
assert 0 < kelly < 1

# Test 3: Bet Settlement
bet_size = 100
odds = 2.0
pnl_win = bet_size * (odds - 1)  # 100
assert pnl_win == 100

# Test 4: Bankroll Management
initial = 1000
place_bet(initial, 100)
assert remaining_balance == 900
```

**Deliverables**
```
✓ src/betting/betting_engine.py
✓ src/betting/bet_simulator.py
✓ tests/test_betting_engine.py (passing)
```

**Success Criteria**
- All betting tests pass
- EV, Kelly, settlement calculations correct
- Virtual bankroll tracked accurately

---

### WEEK 6: Backtest Engine

**Objectifs**
- Implement walk-forward backtest
- Simulate real betting with Kelly
- Generate performance metrics

**Tâches**

```bash
# 1. Build backtest engine
# src/betting/backtest.py

# 2. Run complete backtest on 2020-2024
# For each year:
#   - Load model trained on previous years
#   - Place virtual bets on all matches
#   - Track equity, ROI, Sharpe

# 3. Output results
# - Equity curve (CSV)
# - Statistics (dict)
# - Detailed bets (CSV)

# 4. Visualize results
# notebooks/04_walk_forward_validation.ipynb
```

**Backtest Pseudocode**
```python
def walk_forward_backtest(initial_capital=1000, kelly_fraction=0.25, min_ev=0.05):
    results = []
    balance = initial_capital
    
    for year in [2020, 2021, 2022, 2023, 2024]:
        # Train on all data before year
        train_data = features_df[features_df['year'] < year]
        models = train_all_models(train_data)
        
        # Test on year
        test_data = features_df[features_df['year'] == year]
        
        for _, match in test_data.iterrows():
            features = match[feature_columns]
            
            # Get predictions
            pred_1x2 = models['1x2'].predict([features])
            odds = match['odds_1']  # For example
            
            # Check EV
            ev = calculate_ev(pred_1x2['home'], odds)
            
            if ev > min_ev:
                # Place bet
                bet_size = calculate_bet_size(balance, kelly_fraction, ev, odds)
                
                # Simulate outcome
                won = match['result'] == 2  # Home team won
                
                if won:
                    pnl = bet_size * (odds - 1)
                else:
                    pnl = -bet_size
                
                balance += pnl
                
                results.append({
                    'date': match['date'],
                    'match': f"{match['home']} vs {match['away']}",
                    'bet_type': '1X2',
                    'outcome': 'Home',
                    'odds': odds,
                    'bet_size': bet_size,
                    'ev': ev,
                    'pnl': pnl,
                    'balance': balance,
                    'won': won
                })
    
    return results
```

**Expected Output**
```
Year | ROI    | Win Rate | Sharpe | Avg EV  | N Bets
-----|--------|----------|--------|---------|-------
2020 | +3.2%  | 54%      | 0.32   | +2.1%   | 180
2021 | +1.8%  | 52%      | 0.18   | +1.9%   | 176
2022 | +2.5%  | 53%      | 0.28   | +2.0%   | 182
2023 | +1.1%  | 51%      | 0.12   | +1.5%   | 174
2024 | +4.2%  | 56%      | 0.42   | +2.8%   | 168
-----|--------|----------|--------|---------|-------
TOTAL| +2.6%  | 53%      | 0.26   | +2.1%   | 880
```

**Deliverables**
```
✓ src/betting/backtest.py
✓ notebooks/04_walk_forward_validation.ipynb
✓ Backtest results (CSV/JSON)
```

**Success Criteria**
- Backtest completes without errors
- ROI > 0% (positive)
- Sharpe > 0.2 (reasonably stable)
- Win rate > 50% (better than random)

---

### WEEK 7-9: Streamlit App Development

**Objectifs**
- Create Streamlit app
- Implement 5 pages
- Deploy locally + cloud

**Tâches**

**Week 7: Setup + Pages 1-2**
```bash
# 1. Create app structure
app/
├── streamlit_app.py (main entry point)
└── pages/
    ├── 01_Dashboard.py
    └── 02_Simulator.py

# 2. Implement Dashboard
# - Upcoming matches
# - Predictions
# - Virtual bankroll

# 3. Implement Simulator
# - Date/match selection
# - Bet placement
# - Result simulation
# - Balance update

# 4. Test locally
streamlit run app/streamlit_app.py
# → http://localhost:8501
```

**Week 8: Pages 3-5**
```bash
# 1. Implement Backtest
# - Configuration UI
# - Run button
# - Equity curve
# - Statistics

# 2. Implement Monitoring
# - Calibration plots
# - Feature importance
# - Performance by year

# 3. Implement Analysis
# - Model comparison
# - Prediction distribution
# - Winning vs losing patterns

# 4. Fix UI/UX bugs
```

**Week 9: Deployment**
```bash
# 1. Push to GitHub
git add .
git commit -m "Add Streamlit app"
git push origin main

# 2. Deploy to Streamlit Cloud
# - Go to https://share.streamlit.io
# - Connect GitHub
# - Select repo & branch
# - Deploy!

# 3. Test on cloud
# - All pages functional
# - Models load correctly
# - No timeout errors

# 4. Add to README
# Link: https://your-username-football-predictor.streamlit.app
```

**Deliverables**
```
✓ app/streamlit_app.py
✓ app/pages/*.py (5 pages)
✓ GitHub repo (public)
✓ Streamlit Cloud deployment (live URL)
✓ README.md with instructions
```

**Success Criteria**
- App runs locally without errors
- All 5 pages functional
- Simulator works with virtual bets
- Backtest completes and visualizes
- Deployed on Streamlit Cloud

---

### WEEK 10-12: Optimization + Tennis

**Objectifs**
- Optimize ML models (hyperparameter tuning)
- Add advanced features
- Setup tennis data pipeline

**Tâches**

**Week 10: Model Optimization**
```bash
# 1. Hyperparameter tuning (Optuna)
python src/models/optuna_tuning.py

# 2. Feature engineering advanced
# - Add xG (if available)
# - Add injury data (scrape)
# - Add recent form weighted metrics

# 3. Ensemble methods
# - Combine 1X2 + O/U predictions
# - Weighted voting

# 4. Retrain all models
# Save improved versions
```

**Week 11-12: Tennis Setup**
```bash
# 1. Download tennis data
# - ATP/WTA matches 2015-2024
# - Source: Jeff Sackmann GitHub

# 2. Calculate tennis features
# - Player rankings
# - H2H records
# - Surface-specific stats
# - Age/form metrics

# 3. Train tennis models
# - Same 4 models (1X2, O/U, BTS, Exact)
# - Walk-forward validation

# 4. Update app for sports selection
# - Dropdown: Football / Tennis
# - Load respective models
# - Reuse 5 pages logic
```

**Deliverables**
```
✓ Optimized models (better hyperparameters)
✓ Tennis data pipeline
✓ Tennis feature engineering
✓ Tennis models (1x2, ou, bts, exact)
✓ Updated app (sports selector)
```

---

### WEEK 13: Documentation + Portfolio

**Objectifs**
- Final polish
- Complete documentation
- Portfolio presentation

**Tâches**

```bash
# 1. Write comprehensive README
# - Project overview
# - Installation instructions
# - Usage guide
# - Results summary

# 2. Create portfolio summary
# - Blog post / Medium article
# - Performance metrics
# - Learnings & insights

# 3. GitHub cleanup
# - Remove unnecessary files
# - Clean commit history
# - Add badges (Python version, license)

# 4. Final testing
# - Run all tests
# - Check app on cloud
# - Verify notebooks

# 5. Project showcase
# - LinkedIn post
# - GitHub stars
# - Portfolio website update
```

**Deliverables**
```
✓ Complete README.md
✓ Blog post / article
✓ Portfolio summary
✓ Clean GitHub repo
✓ Live Streamlit app
✓ Jupyter notebooks (all 5)
```

---

## Instructions d'Installation

### Prerequisites
- Python 3.12.4
- Git
- pip (comes with Python)
- Football-Data.org API key (gratuit)

### Step-by-Step Setup

**1. Clone ou créer le projet**
```bash
mkdir football_predictor
cd football_predictor
git init
```

**2. Python Virtual Environment**
```bash
python3.12 -m venv venv

# Activate
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure API Key**
```bash
# 1. Get API key from https://www.football-data.org/client/register
# 2. Open src/utils/config.py
# 3. Replace:
FOOTBALL_DATA_API_KEY = 'YOUR_API_KEY_HERE'
```

**5. Download Data**
```bash
python src/data/download_data.py
# Creates: data/raw/matches_2015_2024.csv
```

**6. Calculate Features**
```bash
python src/data/feature_calculator.py
# Creates: data/processed/features_complete.csv
```

**7. Train Models**
```bash
python src/models/training.py
# Creates: models/1x2.pkl, models/ou.pkl, models/bts.pkl, models/exact.pkl
```

**8. Run Streamlit App**
```bash
streamlit run app/streamlit_app.py
# Opens: http://localhost:8501
```

---

## Pipeline d'Exécution

### Ordre Correct d'Exécution

```
1. download_data.py
   INPUT:  Football-Data.org API
   OUTPUT: data/raw/matches_2015_2024.csv
   
2. feature_calculator.py
   INPUT:  data/raw/matches_2015_2024.csv
   OUTPUT: data/processed/features_complete.csv
   
3. training.py
   INPUT:  data/processed/features_complete.csv
   OUTPUT: models/{1x2,ou,bts,exact}.pkl
   
4. backtest.py (optional, for validation)
   INPUT:  data/processed/features_complete.csv + models/
   OUTPUT: backtest_results.csv
   
5. streamlit_app.py
   INPUT:  models/ + data/processed/
   OUTPUT: Web interface (localhost:8501)
```

### Commandes Complètes

```bash
# Full pipeline from scratch
bash run_pipeline.sh

# Ou manuellement:
python src/data/download_data.py && \
python src/data/feature_calculator.py && \
python src/models/training.py && \
streamlit run app/streamlit_app.py
```

---

## Fichiers de Code

### Fichiers Fournis

**1. Configuration**
```
✓ requirements.txt              # Dependencies
✓ src/utils/config.py           # Global config + API keys
```

**2. Data**
```
✓ src/data/download_data.py     # Download Football-Data + Kaggle
✓ src/data/feature_calculator.py # Calculate 35+ features
```

**3. Models**
```
✓ src/models/models_complete.py # All 4 models (1X2, O/U, BTS, Exact)
✓ src/models/training.py        # Training pipeline (you need to create)
```

**4. Betting**
```
✓ src/betting/betting_engine.py # EV, Kelly, virtual bankroll
✓ src/betting/bet_simulator.py  # Simulate bets (you need to create)
✓ src/betting/backtest.py       # Walk-forward backtest (you need to create)
```

**5. App**
```
(You need to create):
✓ app/streamlit_app.py
✓ app/pages/01_Dashboard.py
✓ app/pages/02_Simulator.py
✓ app/pages/03_Backtest.py
✓ app/pages/04_Monitoring.py
✓ app/pages/05_Analysis.py
```

---

## Validation et Testing

### Unit Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_betting_engine.py -v

# Test with coverage
pytest --cov=src tests/
```

### Test Cases à Implémenter

```python
# tests/test_betting_engine.py
def test_ev_calculation():
    assert calculate_ev(0.60, 2.0) == 0.20
    
def test_kelly_fraction():
    kelly = calculate_kelly(0.60, 2.0)
    assert 0 < kelly < 1
    
def test_bet_settlement():
    engine = BettingEngine()
    engine.place_bet(...)
    engine.settle_bet(..., won=True)
    assert engine.current_balance == 1100
    
# tests/test_models.py
def test_model_1x2_output():
    pred = model_1x2.predict(X_test)
    assert 'home' in pred and 'draw' in pred and 'away' in pred
    
def test_model_ou_poisson():
    pred = model_ou.predict(X_test)
    assert 0 <= pred['prob_over_2_5'] <= 1
```

### Validation Checklist

- [ ] Data downloaded (10k+ matches)
- [ ] Features calculated (no NaNs)
- [ ] All 4 models train
- [ ] Walk-forward validation stable
- [ ] Backtest ROI > 0%
- [ ] Streamlit app runs locally
- [ ] All 5 pages functional
- [ ] Tests passing (pytest)
- [ ] GitHub repo created
- [ ] Deployed on Streamlit Cloud

---

## FAQ & Troubleshooting

### Problèmes Courants

**Q: "Football-Data API returns 403 error"**
```
A: Check your API key
   - Verify in src/utils/config.py
   - Check at https://www.football-data.org/client/register
   - Sometimes API needs warm-up (wait 5 min)
```

**Q: "Feature calculator takes too long"**
```
A: Normal for 10k+ matches (5-10 min)
   - Run with --verbose flag for progress
   - Can reduce DATA_START_YEAR in config.py for testing
```

**Q: "Streamlit app runs locally but not on cloud"**
```
A: Common issues:
   1. secrets.toml not in .streamlit/
      → Add: .streamlit/secrets.toml (gitignore)
      → Add secrets via Streamlit Cloud UI
   
   2. Models not loading
      → Ensure models/*.pkl in repo root
      → Check path: BASE_DIR / 'models'
   
   3. Timeout on backtest
      → Add st.cache_resource decorator
      → Limit to 2024 data for cloud
```

**Q: "My ROI is negative. Is this broken?"**
```
A: Not necessarily! Possible causes:
   1. Not enough data (need 50+ bets for confidence)
   2. Min EV threshold too low
   3. Kelly fraction too aggressive
   
   Try:
   - Increase min_ev_threshold to 10%
   - Decrease kelly_fraction to 0.1
   - Ensure walk-forward uses fresh models
```

### Performance Tips

**Optimize Feature Calculation**
```python
# Use vectorized operations (not loops)
# In feature_calculator.py:
team_matches['win'] = (team_matches['result'] == winner).astype(int)
win_pct = team_matches['win'].rolling(10).mean()  # Much faster
```

**Cache Models in Streamlit**
```python
@st.cache_resource
def load_models():
    return load_all_models(MODELS_PATH)

models = load_models()
```

**Reduce Backtest Time**
```python
# Instead of iterating all matches:
matches_with_ev = matches[matches['ev'] > MIN_EV_THRESHOLD]
# Process only bettable matches
```

---

## Contact & Support

**Issues?** Check:
1. README errors
2. API key validity
3. Data download status
4. Python version (3.12.4)

**Want to contribute?**
- Fork GitHub repo
- Create feature branch
- Submit PR

---

**Good luck with your project, Jimmy! 🚀**

---

## Checklist Final (À Cocher au Fur et à Mesure)

### Week 1
- [ ] Venv créé et activé
- [ ] requirements.txt installé
- [ ] API key obtenue et ajoutée
- [ ] Data téléchargée (15k+ matches)
- [ ] Notebook exploration terminé

### Week 2
- [ ] Features calculées (9k rows)
- [ ] Pas de NaNs dans features
- [ ] Correlations analysées
- [ ] Feature distributions visualisées

### Week 3
- [ ] Model 1X2 entraîné
- [ ] Model O/U entraîné
- [ ] Walk-forward validation fait
- [ ] Models sauvegardés

### Week 4
- [ ] Model BTS entraîné
- [ ] Model Exact entraîné
- [ ] Tous 4 models testés
- [ ] Model loader créé

### Week 5-6
- [ ] Betting engine implémenté
- [ ] Tests passing
- [ ] Backtest complet
- [ ] ROI > 0% (simulé)

### Week 7-9
- [ ] App runs locally
- [ ] 5 pages créées
- [ ] Deployed on cloud
- [ ] URL live

### Week 10-12
- [ ] Models optimisés
- [ ] Tennis data téléchargée
- [ ] Tennis models entraînés
- [ ] Multi-sport app

### Week 13
- [ ] README complète
- [ ] Blog post écrit
- [ ] Tests tous passing
- [ ] GitHub public
- [ ] Streamlit live
- [ ] Portfolio présenté

---

**END OF DOCUMENTATION**

**Next Step:** Start with Week 1 checklist!
