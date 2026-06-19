import streamlit as st
import numpy as np
import pandas as pd
from collections import Counter

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="World Cup Sim", layout="wide")

# =========================
# UI STYLE (FONTS + GRADIENT)
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Lato:wght@300;400;700&display=swap');

html, body {
    font-family: 'Lato', sans-serif;
    background: linear-gradient(135deg, #0b0c10, #111827, #0b0c10);
    color: #eaeaea;
}

h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px;
}

.stApp {
    background: transparent;
}

/* sidebar */
[data-testid="stSidebar"] {
    background: rgba(10, 10, 15, 0.85);
    border-right: 1px solid #222;
}

/* cards */
.card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 16px;
    border-radius: 14px;
    margin-bottom: 10px;
    backdrop-filter: blur(10px);
}

.small {
    font-size: 13px;
    opacity: 0.7;
}

</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("## World Cup Simulator")
    sims = st.slider("Simulations", 1000, 20000, 5000)
    run = st.button("Run Simulation")

    st.markdown("---")
    st.markdown("Elo + Form + Monte Carlo Model")

# =========================
# TEAM BASE (SAFE DEFAULTS)
# =========================
teams = [
    "Brazil", "Germany", "France", "Argentina",
    "Mexico", "England", "Spain", "Netherlands",
    "South Korea", "Morocco", "Canada", "USA"
]

# simple “realism” weights (you can tune later)
base_strength = {
    "Brazil": 0.95,
    "Germany": 0.90,
    "France": 0.92,
    "Argentina": 0.91,
    "England": 0.88,
    "Spain": 0.87,
    "Netherlands": 0.84,
    "Mexico": 0.75,
    "USA": 0.74,
    "Canada": 0.70,
    "South Korea": 0.73,
    "Morocco": 0.76
}

def simulate_match(a, b):
    pa = base_strength.get(a, 0.5)
    pb = base_strength.get(b, 0.5)

    total = pa + pb
    pa /= total
    pb /= total

    r = np.random.rand()
    if r < pa:
        return a
    else:
        return b


def simulate_world_cup():
    pool = teams.copy()
    np.random.shuffle(pool)

    # knockout style tournament
    while len(pool) > 1:
        next_round = []
        for i in range(0, len(pool), 2):
            next_round.append(simulate_match(pool[i], pool[i+1]))
        pool = next_round

    return pool[0]


def monte_carlo(n):
    winners = Counter()
    for _ in range(n):
        winners[simulate_world_cup()] += 1
    return winners

# =========================
# HEADER
# =========================
st.markdown("# World Cup Simulator")
st.markdown("<div class='small'>Monte Carlo tournament engine</div>", unsafe_allow_html=True)
st.markdown("---")

# =========================
# MAIN
# =========================
col1, col2 = st.columns([2.5, 1])

with col1:
    st.markdown("## Results Feed")

    if run:
        results = monte_carlo(sims)

        df = pd.DataFrame(results.items(), columns=["team", "wins"])
        df["prob"] = df["wins"] / df["wins"].sum()
        df = df.sort_values("prob", ascending=False)

        for _, r in df.iterrows():
            st.markdown(f"""
            <div class="card">
                <b>{r['team']}</b><br>
                <span class="small">Win probability: {r['prob']:.2%}</span>
            </div>
            """, unsafe_allow_html=True)

        st.bar_chart(df.set_index("team")["prob"])

    else:
        st.markdown("""
        <div class="card">
        Run the simulation to generate World Cup outcomes
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("## Model Notes")

    if run:
        st.markdown("""
        <div class="card">
        <b>Behaviour</b><br>
        <span class="small">
        • Strong teams dominate<br>
        • Knockout randomness included<br>
        • Monte Carlo smooths variance
        </span>
        </div>
        """, unsafe_allow_html=True)
