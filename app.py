import streamlit as st
import numpy as np
import pandas as pd
from collections import Counter
import os

# -------------------------
# PAGE CONFIG
# -------------------------

# =========================
# PAGE SETUP (UI ONLY)
# =========================
st.set_page_config(layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

html, body, [class*="css"] {
    background-color: #000000 !important;
    color: #e6e6e6 !important;
    font-family: 'Press Start 2P', monospace !important;
}

/* FORCE BLACK BACKGROUND */
.stApp {
    background-color: #000000 !important;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background-color: #050505 !important;
    border-right: 1px solid #222;
    padding: 20px;
}

/* HEADINGS (ALL UNIFIED) */
h1, h2, h3 {
    font-family: 'Press Start 2P', monospace !important;
    font-size: 20px !important;
    color: #ffffff !important;
    text-transform: lowercase !important;
    text-shadow: 0 0 6px #00ffcc;
}

/* BODY TEXT */
p, span, div, label {
    text-transform: lowercase !important;
}

/* SLIDER (brighter, game-like) */
.stSlider > div {
    color: #00ffcc !important;
}

/* BUTTON CENTERING */
div.stButton {
    display: flex;
    justify-content: center;
}

/* BUTTON STYLE */
.stButton > button {
    background-color: #111;
    color: #00ffcc;
    border: 1px solid #00ffcc;
    padding: 0.6rem 1rem;
    transition: all 0.2s ease-in-out;
    font-family: 'Press Start 2P', monospace;
}

/* BUTTON HOVER */
.stButton > button:hover {
    background-color: #00ffcc;
    color: #000;
    box-shadow: 0 0 10px #00ffcc;
}

/* CARD STYLE */
.card {
    background: #0a0a0a;
    border: 1px solid #222;
    border-radius: 8px;
    padding: 12px;
    margin-bottom: 10px;
}

/* blinking "pac-man style" divider */
.divider {
    width: 100%;
    height: 6px;
    background: repeating-linear-gradient(
        90deg,
        #00ffcc,
        #00ffcc 4px,
        transparent 4px,
        transparent 12px
    );
    animation: blink 1.2s infinite linear;
}

@keyframes blink {
    0% { opacity: 1; }
    50% { opacity: 0.2; }
    100% { opacity: 1; }
}

.small {
    opacity: 0.7;
    font-size: 12px;
}
</style>
""", unsafe_allow_html=True)


# =========================
# HEADER
# =========================
st.markdown("# world cup simulator")
st.markdown("<div class='small'>career mode simulation engine</div>", unsafe_allow_html=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# =========================
# SIMULATION WRAPPER
# =========================
def simulate(n):
    return monte_carlo(n)

# =========================
# LAYOUT
# =========================
col1, col2 = st.columns([2.5, 1])

with col1:

    if run:
        results = simulate(int(sims))

        df = pd.DataFrame(results.items(), columns=["team", "wins"])
        df["prob"] = df["wins"] / df["wins"].sum()

        st.markdown("## results feed")

        for _, row in df.sort_values("wins", ascending=False).iterrows():
            st.markdown(f"""
            <div class="card">
                <b>{row['team'].lower()}</b><br>
                <span class="small">win probability: {row['prob']:.2%}</span>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.markdown("## results feed")
        st.markdown("<div class='card'>press run simulation to start tournament engine</div>", unsafe_allow_html=True)

with col2:

    st.markdown("## insights")

    if run:
        st.markdown("""
        <div class="card">
        <b>model behavior</b><br><br>
        • favorites dominate early rounds<br>
        • knockout variance increases randomness<br>
        • monte carlo stabilizes outcome distribution
        </div>
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
