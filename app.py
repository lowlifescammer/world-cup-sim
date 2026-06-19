import streamlit as st
import numpy as np
import pandas as pd
from collections import Counter

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
teams = ["Brazil","Germany","France","Mexico","England","Argentina"]

def simulate(n):
    r = Counter()
    for _ in range(n):
        r[np.random.choice(teams)] += 1
    return r

# -------------------------
# LAYOUT: FEED + SIDE INSIGHTS
# -------------------------
col1, col2 = st.columns([2.5, 1])

with col1:

    if run:
        results = simulate(sims)

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
