import streamlit as st
import numpy as np
import pandas as pd
from collections import Counter
import os

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(layout="wide")

# =========================
# UI STYLE (FIFA / GAME MENU)
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
    text-transform: lowercase !important;
    text-shadow: 0 0 6px #00ffcc;
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
# SAFE SIDEBAR
# =========================
with st.sidebar:
    st.markdown("## world cup simulator")

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    sims = st.slider("simulations", 500, 20000, 5000)
    run = st.button("run simulation")

    st.markdown("---")
    st.markdown("elo + monte carlo model")

# =========================
# HEADER
# =========================
st.markdown("# world cup simulator")
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# =========================
# CORE SIMULATION
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
        • monte carlo reduces noise<br>
        • upsets still possible
        </div>
        """, unsafe_allow_html=True)
