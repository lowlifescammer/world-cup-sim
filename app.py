import os
import pandas as pd

if not os.path.exists("fixtures.csv"):
    st.error("fixtures.csv missing from repo")
    st.stop()

if not os.path.exists("elo.csv"):
    st.error("elo.csv missing from repo")
    st.stop()

if not os.path.exists("odds.csv"):
    st.error("odds.csv missing from repo")
    st.stop()

if not os.path.exists("results.csv"):
    st.error("results.csv missing from repo")
    st.stop()

fixtures = pd.read_csv("fixtures.csv")
elo = pd.read_csv("elo.csv")
odds = pd.read_csv("odds.csv")
results = pd.read_csv("results.csv")

# =========================
# GLOBAL STORAGE (must exist)
# =========================
match_cache = {}

# =========================
# FIXTURE PROB LOOKUP
# =========================
# -------------------------
# SAFE DATA LOAD
# -------------------------
import pandas as pd

try:
    fixtures = pd.read_csv("fixtures.csv")
    odds = pd.read_csv("odds.csv")
except Exception as e:
    st.error(f"Missing data files: {e}")
    st.stop()

# -------------------------
# CLEAN KEYS
# -------------------------
fixtures["key"] = (
    fixtures["home_team"].str.strip().str.lower()
    + " vs "
    + fixtures["away_team"].str.strip().str.lower()
)

odds["key"] = (
    odds["home_team"].str.strip().str.lower()
    + " vs "
    + odds["away_team"].str.strip().str.lower()
)

# -------------------------
# MERGE (THIS CREATES comparison)
# -------------------------
comparison = fixtures.merge(odds, on="key", how="inner")

st.write("Matched rows:", len(comparison))
# =========================
# MATCH PROBABILITY ENGINE
# =========================
def get_match_probs(team1, team2):

    key = tuple(sorted([team1.strip().lower(), team2.strip().lower()]))

    if key in match_cache:
        return match_cache[key]

    home, away = key

    home_elo = elo_lookup.get(home, 1500)
    away_elo = elo_lookup.get(away, 1500)

    home_elo = float(home_elo)
    away_elo = float(away_elo)

    elo_diff = (home_elo - away_elo) / 25
    elo_diff = max(min(elo_diff, 20), -20)

    row = pd.DataFrame([{
        'elo_diff': elo_diff,
        'neutral': 1,
        'is_world_cup': 1,
        'is_friendly': 0,
        'form_diff': 0
    }])

    features = ['elo_diff', 'neutral', 'is_world_cup', 'is_friendly', 'form_diff']

    X = row[features]

    probs = model.predict_proba(X)[0]

    result = {
        'home': probs[2],
        'draw': probs[1],
        'away': probs[0]
    }

    match_cache[key] = result
    return result

# =========================
# MATCH SIMULATION
# =========================
def simulate_match(home, away):

    probs = get_match_probs(home, away)

    outcome = np.random.choice(
        ['home', 'draw', 'away'],
        p=[probs['home'], probs['draw'], probs['away']]
    )

    return outcome

# =========================
# KNOCKOUT RESOLUTION
# =========================
def knockout_winner(team1, team2):

    probs = get_match_probs(team1, team2)

    outcome = np.random.choice(
        ['home', 'draw', 'away'],
        p=[probs['home'], probs['draw'], probs['away']]
    )

    if outcome == 'home':
        return team1
    elif outcome == 'away':
        return team2
    else:
        return team1 if np.random.rand() < 0.52 else team2

# =========================
# GROUP STAGE SIMULATION
# =========================
def simulate_group(teams):

    points = {t: 0 for t in teams}

    for i in range(len(teams)):
        for j in range(i+1, len(teams)):

            t1, t2 = teams[i], teams[j]

            result = simulate_match(t1, t2)

            if result == "home":
                points[t1] += 3
            elif result == "away":
                points[t2] += 3
            else:
                points[t1] += 1
                points[t2] += 1

    standings = sorted(points.items(), key=lambda x: x[1], reverse=True)
    return standings

# =========================
# FULL TOURNAMENT SIM
# =========================
def simulate_world_cup():

    group_results = {}

    # GROUP STAGE
    for group, teams in groups.items():
        group_results[group] = simulate_group(teams)

    # QUALIFICATION
    top2 = []
    third = []

    for group, standings in group_results.items():
        top2.extend([standings[0][0], standings[1][0]])
        third.append(standings[2][0])

    qualified = top2 + third[:8]

    # R16
    r16 = []
    for i in range(0, 32, 2):
        r16.append(knockout_winner(qualified[i], qualified[i+1]))

    # QF
    qf = []
    for i in range(0, len(r16), 2):
        qf.append(knockout_winner(r16[i], r16[i+1]))

    # SF
    sf = []
    for i in range(0, len(qf), 2):
        sf.append(knockout_winner(qf[i], qf[i+1]))

    # FINALISTS
    finalists = []
    for i in range(0, len(sf), 2):
        finalists.append(knockout_winner(sf[i], sf[i+1]))

    return knockout_winner(finalists[0], finalists[1])

# =========================
# MONTE CARLO WRAPPER
# =========================
def monte_carlo(n):

    winners = Counter()

    for _ in range(n):
        champ = simulate_world_cup()
        winners[champ] += 1

    return winners
# -------------------------
# PAGE SETUP
# -------------------------
st.set_page_config(layout="wide")

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Lato:wght@300;400;700&display=swap" rel="stylesheet">

<style>

/* =========================
   GLOBAL BACKGROUND (GRADIENT)
========================= */
.stApp {
    background: linear-gradient(135deg, #0b0c10 0%, #11131a 40%, #0a0f1f 100%);
    color: #eaeaea;
}

/* =========================
   GLOBAL FONT RULES
========================= */
html, body, [class*="css"] {
    font-family: 'Lato', sans-serif;
    color: #eaeaea;
}

/* HEADINGS = PLAYFAIR */
h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px;
    color: #ffffff !important;
}

/* remove Streamlit ugly blue links */
a {
    color: inherit !important;
    text-decoration: none !important;
}

/* =========================
   SIDEBAR
========================= */
[data-testid="stSidebar"] {
    background: rgba(10, 12, 18, 0.85);
    backdrop-filter: blur(10px);
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* =========================
   CARDS (YOUR FEED UI)
========================= */
.card {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 14px 16px;
    margin-bottom: 12px;
    backdrop-filter: blur(8px);
}

/* small muted text */
.small {
    opacity: 0.65;
    font-size: 13px;
}

/* remove top padding clutter */
.block-container {
    padding-top: 2rem;
}

/* buttons */
.stButton > button {
    background: linear-gradient(90deg, #3b82f6, #8b5cf6);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.5rem 1rem;
}

.stButton > button:hover {
    transform: scale(1.02);
    transition: 0.2s;
}

</style>
""", unsafe_allow_html=True)
