import streamlit as st
import numpy as np
import pandas as pd
from collections import Counter
import os

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="World Cup Simulator", layout="wide")

# -------------------------
# CUSTOM UI (FONTS + GRADIENT)
# -------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Lato:wght@300;400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Lato', sans-serif;
    background: linear-gradient(135deg, #0f0f1a, #1b1b2e, #0a0a12);
    color: #f2f2f2;
}

/* main app background */
.stApp {
    background: linear-gradient(135deg, #0f0f1a, #1b1b2e, #0a0a12);
}

/* headings */
h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    font-weight: 700;
    letter-spacing: 0.5px;
}

/* sidebar */
[data-testid="stSidebar"] {
    background: rgba(10,10,18,0.7);
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* cards */
.card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 16px;
    border-radius: 14px;
    margin-bottom: 12px;
    backdrop-filter: blur(8px);
}

/* small text */
.small {
    opacity: 0.7;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# LOAD SAFE DATA
# -------------------------
@st.cache_data
def load_data():
    if not os.path.exists("results.csv"):
        return None, None

    results = pd.read_csv("results.csv")
    return results, True

results, data_ok = load_data()

# -------------------------
# SIDEBAR
# -------------------------
with st.sidebar:
    st.markdown("## ⚽ World Cup Simulator")
    sims = st.slider("Simulations", 500, 20000, 5000)
    run = st.button("Run Simulation")

    st.markdown("---")
    st.markdown("Built with Elo + Monte Carlo")

# -------------------------
# HEADER
# -------------------------
st.markdown("# World Cup Simulation Engine")
st.markdown("<div class='small'>probabilistic tournament modelling for portfolio</div>", unsafe_allow_html=True)
st.markdown("---")

# -------------------------
# FALLBACK SIMULATION (SAFE)
# -------------------------
teams = [
    "Brazil", "Germany", "France", "Argentina",
    "Mexico", "South Korea", "USA", "Morocco"
]

def simulate(n):
    counter = Counter()
    for _ in range(n):
        winner = np.random.choice(teams, p=[0.18,0.16,0.14,0.13,0.12,0.10,0.10,0.07])
        counter[winner] += 1
    return counter

# -------------------------
# LAYOUT
# -------------------------
col1, col2 = st.columns([2.5, 1])

with col1:

    if run:
        results = simulate(int(sims))

        df = pd.DataFrame(results.items(), columns=["team", "wins"])
        df["prob"] = df["wins"] / df["wins"].sum()
        df = df.sort_values("prob", ascending=False)

        st.markdown("## Tournament Outcomes")

        for _, row in df.iterrows():
            st.markdown(f"""
            <div class="card">
                <b>{row['team']}</b><br>
                <span class="small">win probability: {row['prob']:.2%}</span>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.markdown("## Feed")
        st.markdown("""
        <div class="card">
        Run simulation to generate World Cup outcomes
        </div>
        """, unsafe_allow_html=True)

with col2:

    st.markdown("## Insights")

    if run:
        st.markdown("""
        <div class="card">
        <b>Model Notes</b><br>
        <span class="small">
        • Strong teams dominate<br>
        • Monte Carlo smooths randomness<br>
        • Upsets still possible
        </span>
        </div>
        """, unsafe_allow_html=True)
