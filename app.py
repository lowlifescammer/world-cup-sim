import streamlit as st
import pandas as pd
import numpy as np
from collections import Counter

# -----------------------------
# PAGE CONFIG (THEME BASE)
# -----------------------------
st.set_page_config(
    page_title="World Cup Simulator",
    page_icon="⚽",
    layout="wide"
)

# -----------------------------
# SIDEBAR (INTERLOPER STYLE CONTROL PANEL)
# -----------------------------
with st.sidebar:
    st.markdown("## ⚙️ controls")
    st.markdown("---")

    sims = st.slider("simulation runs", 500, 20000, 5000, step=500)

    st.markdown("---")
    st.markdown("**world cup model**")
    st.caption("elo + form + monte carlo")

    run = st.button("run simulation →")

# -----------------------------
# FAKE/REAL SIM FUNCTION HOOK
# (replace with your monte_carlo)
# -----------------------------
teams = [
    "Brazil", "Germany", "Mexico",
    "South Africa", "France", "England",
    "Argentina", "Netherlands"
]

def simulate(n):
    results = Counter()
    for _ in range(n):
        winner = np.random.choice(teams)
        results[winner] += 1
    return results

# -----------------------------
# MAIN HEADER (INTERLOPER FEEL)
# -----------------------------
st.markdown("# world cup simulator")
st.caption("probabilistic tournament outcomes using monte carlo simulation")

st.markdown("---")

# -----------------------------
# MAIN FEED LAYOUT
# -----------------------------
col1, col2 = st.columns([2, 1])

# LEFT COLUMN (MAIN FEED)
with col1:

    if run:
        results = simulate(sims)

        df = pd.DataFrame(results.items(), columns=["team", "wins"])
        df["probability"] = df["wins"] / df["wins"].sum()

        # ---- CARD 1: TOP TEAMS ----
        st.markdown("### 🏆 dominant outcomes")

        top_df = df.sort_values("wins", ascending=False)

        for _, row in top_df.iterrows():
            st.markdown(f"""
            <div style="
                padding: 12px;
                border: 1px solid #333;
                border-radius: 10px;
                margin-bottom: 8px;
            ">
                <b>{row['team']}</b><br>
                win share: {row['probability']:.2%}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # ---- CARD 2: CHART ----
        st.markdown("### distribution")

        st.bar_chart(df.set_index("team")["probability"])

    else:
        st.markdown("### run simulation to generate outcomes")
        st.info("use sidebar → run simulation")

# RIGHT COLUMN (INSIGHTS PANEL)
with col2:

    st.markdown("### insights")

    if run:
        st.markdown("**model behaviour**")
        st.write("• elite teams dominate due to elo priors")
        st.write("• variance increases in knockout stage")
        st.write("• upsets still occur in ~low probability tails")

        st.markdown("---")

        st.markdown("**simulation size**")
        st.metric("runs", sims)

    else:
        st.markdown("no data yet")
