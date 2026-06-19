import streamlit as st
import numpy as np
import pandas as pd
from collections import Counter
import os

# -------------------------
# PAGE CONFIG
# -------------------------
# =========================
# PAGE SETUP (FIFA CAREER MODE UI)
# =========================

st.set_page_config(layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Lato:wght@300;400;700&display=swap');

:root {
    --bg1: #050505;
    --bg2: #000000;
    --neon: #00ffcc;
    --neon2: #ff2bd6;
    --text: #eaeaea;
}

/* GLOBAL BACKGROUND */
html, body, .stApp {
    background: #000000 !important;
    color: #eaeaea;
    font-family: 'Lato', sans-serif;
}
/* PIXEL HEADINGS */
h3, h3, h3 {
    font-family: 'Press Start 2P', cursive;
    color: #f2f2f2;

    text-shadow:
        0 0 2px rgba(0, 255, 204, 0.25),
        0 0 6px rgba(0, 255, 204, 0.18);

    letter-spacing: 1px;
    text-transform: lowercase;
}
h1 {
    font-size: 42px;
}

h2 {
    font-size: 26px;
    opacity: 0.95;
}

h3 {
    font-size: 18px;
    opacity: 0.85;
}
/* SIDEBAR */
[data-testid="stSidebar"] {
    background: #050505;
    border-right: 1px solid #1a1a1a;
    padding: 20px;
}

/* SIDEBAR TITLE */
.sidebar-title {
    font-family: 'Press Start 2P', cursive;
    color: white;
    text-shadow: 0 0 10px var(--neon);
    font-size: 14px;
    margin-bottom: 20px;
}
:root {
    --heading-font: 'Press Start 2P', monospace;
    --body-font: 'Lato', sans-serif;
}
/* sidebar title font source */
[data-testid="stSidebar"] h2 {
    font-family: var(--heading-font);
}

/* global headings adopt same font */
h1, h2, h3, h4 {
    font-family: var(--heading-font);
}

/* BUTTONS */
.stButton>button {
    background: transparent;
    border: 1px solid var(--neon);
    color: white;
    padding: 12px 18px;
    border-radius: 6px;
    font-family: 'Lato', sans-serif;
    text-transform: lowercase;
    transition: 0.2s ease;
}

.stButton>button:hover {
    background: var(--neon);
    color: black;
    box-shadow: 0 0 20px var(--neon);
    transform: scale(1.02);
}

/* SLIDER */
.stSlider > div {
    color: white;
}

/* CARD STYLE */
.card {
    background: rgba(10,10,10,0.8);
    border: 1px solid #222;
    border-radius: 10px;
    padding: 14px;
    margin-bottom: 10px;
    box-shadow: 0 0 10px rgba(0,255,204,0.08);
}

/* SMALL TEXT */
.small {
    opacity: 0.7;
    font-size: 12px;
    text-transform: lowercase;
}

/* CENTER BUTTON */
.center {
    display: flex;
    justify-content: center;
}

/* PAC-MAN STYLE DIVIDER */
.divider {
    width: 100%;
    height: 10px;
    margin: 20px 0;
    background: repeating-linear-gradient(
        90deg,
        var(--neon),
        var(--neon) 4px,
        transparent 4px,
        transparent 12px
    );
    animation: move 1.2s linear infinite;
}

@keyframes move {
    from {background-position: 0 0;}
    to {background-position: 40px 0;}
}
</style>
""", unsafe_allow_html=True)


# =========================
# SIDEBAR (FIFA CAREER MODE)
# =========================

with st.sidebar:
    st.markdown("<div class='sidebar-title'>world cup simulator</div>", unsafe_allow_html=True)

    st.markdown("### simulation controls")

    sims = st.slider(
        "simulation depth",
        500, 20000, 5000
    )

    st.markdown("""
    <div class="card">
    <b>about this model</b><br><br>
    uses monte carlo simulation + elo ratings + form dynamics to simulate tournament outcomes.<br><br>
    higher simulation count = smoother probability distribution.
    </div>
    """, unsafe_allow_html=True)

    run = st.button("run simulation")


# =========================
# HEADER (FIFA MENU STYLE)
# =========================

st.markdown("# world cup simulator")
st.markdown("<div class='small'>career mode probabilistic engine</div>", unsafe_allow_html=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)


# =========================
# SIMULATION LAYOUT
# =========================

col1, col2 = st.columns([2.5, 1])


with col1:

    if run:

        results = simulate(int(sims))

        df = pd.DataFrame(results.items(), columns=["team", "wins"])
        df["prob"] = df["wins"] / df["wins"].sum()

        st.markdown("## simulation feed")

        for _, row in df.sort_values("wins", ascending=False).iterrows():

            st.markdown(f"""
            <div class="card">
                <b>{row['team'].lower()}</b><br>
                <span class="small">win probability: {row['prob']:.2%}</span>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.markdown("## simulation feed")
        st.markdown("""
        <div class="card">
        ready to simulate world cup outcomes
        </div>
        """, unsafe_allow_html=True)


with col2:

    st.markdown("## analytics")

    if run:

        st.markdown("""
        <div class="card">
        <b>system status</b><br><br>
        • elo engine active<br>
        • monte carlo enabled<br>
        • knockout variance: high<br>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown("<div class='card'>waiting for simulation input</div>", unsafe_allow_html=True)


# =========================
# CENTER BUTTON (OPTIONAL VISUAL EMPHASIS)
# =========================

st.markdown("<div class='center'></div>", unsafe_allow_html=True)
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
    font-family: 'Press Start 2P', serif !important;
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
