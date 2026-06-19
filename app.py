import streamlit as st
import numpy as np
import pandas as pd
from collections import Counter

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(layout="wide")

# =========================
# SESSION STATE (MENU SYSTEM)
# =========================
if "menu" not in st.session_state:
    st.session_state.menu = "dashboard"

# =========================
# SIMULATION MODEL (SAFE DUMMY)
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
# CSS (FIFA CAREER MODE UI)
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

html, body, .stApp {
    background-color: #000 !important;
    color: #fff !important;
    font-family: 'Press Start 2P', monospace !important;
}

/* HEADINGS */
h1, h2, h3 {
    font-size: 20px !important;
    text-transform: lowercase;
    text-shadow: 0 0 8px #00ffcc;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: #050505 !important;
    border-right: 1px solid #222;
}

/* BUTTONS */
.stButton > button {
    background: #111;
    color: #00ffcc;
    border: 1px solid #00ffcc;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: #00ffcc;
    color: #000;
    box-shadow: 0 0 12px #00ffcc;
}

/* MENU CARDS */
.menu-card {
    padding: 12px;
    margin-bottom: 10px;
    border-radius: 10px;
    border: 1px solid #222;
    background: #0a0a0a;
    transition: all 0.2s ease;
    cursor: pointer;
}

/* hover glow */
.menu-card:hover {
    border: 1px solid #00ffcc;
    box-shadow: 0 0 12px #00ffcc;
    transform: scale(1.02);
}

/* ACTIVE STATE */
.menu-active {
    border: 1px solid #00ffcc !important;
    box-shadow: 0 0 18px #00ffcc !important;
}

/* CARD OUTPUT */
.card {
    background: #0a0a0a;
    border: 1px solid #222;
    padding: 10px;
    margin-bottom: 8px;
    border-radius: 8px;
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
# SIDEBAR (CAREER MODE MENU)
# =========================
with st.sidebar:

    st.markdown("## world cup simulator")
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    sims = st.slider("simulations", 500, 20000, 5000)
    run = st.button("run simulation")

    st.markdown("---")
    st.markdown("## career mode")

    def menu_item(label, key):
        is_active = st.session_state.menu == key
        cls = "menu-card menu-active" if is_active else "menu-card"

        if st.button(label, key=key):
            st.session_state.menu = key

        st.markdown(f"""
        <div class="{cls}">
            {label}
        </div>
        """, unsafe_allow_html=True)

    menu_item("dashboard", "dashboard")
    menu_item("initial model", "phase1")
    menu_item("sportsbook comparison", "phase2")
    menu_item("brier calibration", "phase3")
    menu_item("monte carlo engine", "phase4")
    menu_item("final system", "phase5")

# =========================
# HEADER
# =========================
st.markdown("# world cup simulator")
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# =========================
# SIMULATION ENGINE
# =========================
def simulate(n):
    counter = Counter()
    for _ in range(n):
        winner = np.random.choice(teams, p=probs)
        counter[winner] += 1
    return counter

# =========================
# MAIN LAYOUT
# =========================
col1, col2 = st.columns([2.5, 1])

with col1:

    st.markdown(f"## {st.session_state.menu}")

    if run:

        results = simulate(int(sims))

        df = pd.DataFrame(results.items(), columns=["team", "wins"])
        df["prob"] = df["wins"] / df["wins"].sum()
        df = df.sort_values("prob", ascending=False)

        for _, row in df.iterrows():
            st.markdown(f"""
            <div class="card">
                <b>{row['team'].lower()}</b><br>
                win probability: {row['prob']:.2%}
            </div>
            """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="card">
        select a career mode stage and run simulation
        </div>
        """, unsafe_allow_html=True)

with col2:

    st.markdown("## insights")

    if run:
        st.markdown("""
        <div class="card">
        <b>model notes</b><br><br>
        • monte carlo stabilises randomness<br>
        • stronger teams dominate<br>
        • upsets still occur
        </div>
        """, unsafe_allow_html=True)
