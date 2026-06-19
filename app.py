import streamlit as st
import numpy as np
import pandas as pd
from collections import Counter

import pandas as pdeau
import os

print(os.listdir())

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

    elo_diff = max(min(home_elo - away_elo, 400), -400)

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
        return team1 if np.random.rand() < 0.5 else team2

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
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background: #0e0e10;
    color: #e6e6e6;
}

.stApp {
    background: #0e0e10;
}

/* sidebar */
[data-testid="stSidebar"] {
    background: #111114;
    border-right: 1px solid #222;
}

/* remove default padding clutter */
.block-container {
    padding-top: 2rem;
}

/* card style */
.card {
    background: #151518;
    border: 1px solid #2a2a2a;
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 10px;
}

.small {
    opacity: 0.6;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# SIDEBAR (INTERLOPER NAV)
# -------------------------
with st.sidebar:
    st.markdown("## world cup sim")
    st.markdown("---")

    sims = st.slider("simulations", 500, 20000, 5000)
    run = st.button("run simulation")

    st.markdown("---")
    st.markdown("model: elo + form + mc")

# -------------------------
# HEADER (INTERLOPER STYLE)
# -------------------------
st.markdown("# world cup simulator")
st.markdown("<div class='small'>probabilistic tournament engine</div>", unsafe_allow_html=True)

st.markdown("---")

# -------------------------
# SIMULATION (placeholder hook)
# -------------------------
def simulate(n):
    return monte_carlo(n)
# -------------------------
# LAYOUT: FEED + SIDE INSIGHTS
# -------------------------
col1, col2 = st.columns([2.5, 1])

with col1:

    if run:
        results = simulate(int(sims))

        df = pd.DataFrame(results.items(), columns=["team", "wins"])
        df["prob"] = df["wins"] / df["wins"].sum()

        st.markdown("## feed")

        # INTERLOPER STYLE POSTS
        for _, row in df.sort_values("wins", ascending=False).iterrows():
            st.markdown(f"""
            <div class="card">
                <b>{row['team']}</b><br>
                <span class="small">win probability: {row['prob']:.2%}</span>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.markdown("## feed")
        st.markdown("<div class='card'>run simulation to generate tournament outcomes</div>", unsafe_allow_html=True)

with col2:

    st.markdown("## notes")

    if run:
        st.markdown("""
        <div class="card">
        <b>model behavior</b><br>
        <span class="small">
        • strong teams dominate<br>
        • knockout variance increases noise<br>
        • MC smooths randomness
        </span>
        </div>
        """, unsafe_allow_html=True)
