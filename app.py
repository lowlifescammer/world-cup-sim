import streamlit as st
import numpy as np
import pandas as pd
from collections import Counter

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(layout="wide")

# =========================
# SESSION STATE (TIMELINE)
# =========================
if "stage" not in st.session_state:
    st.session_state.stage = 0

# =========================
# UI STYLE (FIFA / GAME UI)
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

html, body, .stApp {
    background-color: #000000 !important;
    color: #e6e6e6 !important;
    font-family: 'Press Start 2P', monospace !important;
}

/* HEADINGS */
h1, h2, h3 {
    font-family: 'Press Start 2P', monospace !important;
    font-size: 20px !important;
    color: #ffffff !important;
    text-shadow: 0 0 6px #00ffcc;
    text-transform: lowercase;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background-color: #050505 !important;
    border-right: 1px solid #222;
    padding: 20px;
}

/* TEXT */
p, span, div, label {
    text-transform: lowercase !important;
}

/* BUTTON */
.stButton > button {
    background-color: #111;
    color: #00ffcc;
    border: 1px solid #00ffcc;
    padding: 0.6rem 1rem;
    font-family: 'Press Start 2P', monospace;
}

.stButton > button:hover {
    background-color: #00ffcc;
    color: #000;
    box-shadow: 0 0 10px #00ffcc;
}

/* CARD */
.card {
    background: #0a0a0a;
    border: 1px solid #222;
    border-radius: 8px;
    padding: 12px;
    margin-bottom: 10px;
}

/* DIVIDER */
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
}
</style>
""", unsafe_allow_html=True)

# =========================
# CORE SIMULATION MODEL
# =========================
teams = [
    "Brazil", "Germany", "France", "Argentina",
    "Mexico", "South Korea", "USA", "Morocco"
]

probs = [0.18, 0.16, 0.14, 0.13, 0.12, 0.10, 0.10, 0.07]

def simulate(n):
    counter = Counter()
    for _ in range(n):
        winner = np.random.choice(teams, p=probs)
        counter[winner] += 1
    return counter

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("## world cup simulator")

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    sims = st.slider("simulations", 500, 20000, 5000)

    run = st.button("run simulation")

    if run:
        st.session_state.stage = min(st.session_state.stage + 1, 5)

    st.markdown("---")
    st.markdown("## model evolution")

def stage_card(title, text, stage_id):
    active = st.session_state.stage >= stage_id

    base_color = "#00ffcc" if active else "#222"
    opacity = "1" if active else "0.35"

    st.markdown(f"""
    <style>
    .card-{stage_id} {{
        border: 1px solid {base_color};
        padding: 10px;
        margin-bottom: 8px;
        border-radius: 8px;
        opacity: {opacity};
        transition: all 0.25s ease;
        box-shadow: none;
    }}
    </style>

    <div class="card card-{stage_id}">
        <b>{title}</b><br>
        <span style="font-size:10px;">
        {text}
        </span>
    </div>
    """, unsafe_allow_html=True)

    /* 🔥 HOVER EFFECT (THIS IS THE KEY) */
    .card-{stage_id}:hover {{
        border: 1px solid #00ffcc;
        box-shadow: 0 0 12px #00ffcc;
        opacity: 1;
        transform: scale(1.02);
    }}
    </style>

    <div class="card card-{stage_id}">
        <b>{title}</b><br>
        <span style="font-size:10px;">
        {text}
        </span>
    </div>
    """, unsafe_allow_html=True)

    stage_card("phase 1 — initial model", "basic elo prototype", 1)
    stage_card("phase 2 — sportsbook comparison", "benchmark vs market odds", 2)
    stage_card("phase 3 — calibration fixes", "brier score optimisation", 3)
    stage_card("phase 4 — monte carlo system", "tournament simulation layer", 4)
    stage_card("phase 5 — final dashboard", "fifa-style portfolio ui", 5)

# =========================
# HEADER
# =========================
st.markdown("# world cup simulator")
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# =========================
# LAYOUT
# =========================
col1, col2 = st.columns([2.5, 1])

with col1:

    if run:
        results = simulate(int(sims))

        df = pd.DataFrame(results.items(), columns=["team", "wins"])
        df["prob"] = df["wins"] / df["wins"].sum()
        df = df.sort_values("prob", ascending=False)

        st.markdown("## results feed")

        for _, row in df.iterrows():
            st.markdown(f"""
            <div class="card">
                <b>{row['team'].lower()}</b><br>
                win probability: {row['prob']:.2%}
            </div>
            """, unsafe_allow_html=True)

    else:
        st.markdown("## feed")

        st.markdown("""
        <div class="card">
        run simulation to generate tournament outcomes
        </div>
        """, unsafe_allow_html=True)

with col2:

    st.markdown("## insights")

    if run:
        st.markdown("""
        <div class="card">
        <b>model behavior</b><br><br>
        • stronger teams dominate<br>
        • monte carlo reduces randomness<br>
        • upsets still possible
        </div>
        """, unsafe_allow_html=True)
