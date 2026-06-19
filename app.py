import streamlit as st
import numpy as np
import pandas as pd
from collections import Counter
import os

# =========================
# PAGE SETUP (ARCADE UI)
# =========================

st.set_page_config(page_title="world cup simulator", layout="wide")

st.markdown("""
<style>

/* =========================
   GLOBAL THEME
========================= */

@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

html, body, [class*="css"] {
    background-color: #000000 !important;
    color: #ffffff !important;
    font-family: 'Press Start 2P', monospace !important;
}

/* main app */
.stApp {
    background-color: #000000;
}

/* =========================
   HEADINGS (PIXEL + NEON)
========================= */

h1, h2, h3 {
    font-family: 'Press Start 2P', monospace !important;
    color: #ffffff !important;
    text-shadow:
        0 0 5px #00fff7,
        0 0 10px #00fff7,
        0 0 20px #ff00ff;
    letter-spacing: 1px;
}

/* =========================
   LOWERCASE EVERYTHING ELSE
========================= */

p, div, span, label, button {
    text-transform: lowercase !important;
    font-family: Arial, sans-serif !important;
}

/* =========================
   SIDEBAR
========================= */

[data-testid="stSidebar"] {
    background-color: #050505;
    border-right: 1px solid #111;
}

/* sidebar title */
.sidebar-title {
    font-family: 'Press Start 2P', monospace;
    color: #fff;
    text-shadow: 0 0 10px #00fff7;
    font-size: 14px;
    margin-bottom: 10px;
}

/* slider glow */
.stSlider > div > div > div > div {
    background: #00fff7 !important;
}

/* =========================
   BUTTON (NEON + HOVER)
========================= */

.stButton > button {
    background-color: #111;
    color: #fff;
    border: 1px solid #00fff7;
    padding: 12px 18px;
    border-radius: 10px;
    font-family: 'Press Start 2P', monospace;
    transition: all 0.2s ease-in-out;
}

.stButton > button:hover {
    background-color: #00fff7;
    color: #000;
    box-shadow: 0 0 15px #00fff7;
    transform: scale(1.05);
}

/* center button */
.center-button {
    display: flex;
    justify-content: center;
}

/* =========================
   PAC-MAN STYLE BLINKING LINE
========================= */

.pac-line {
    display: flex;
    justify-content: center;
    margin: 20px 0;
}

.dot {
    width: 6px;
    height: 6px;
    margin: 0 4px;
    background-color: #00fff7;
    border-radius: 50%;
    animation: blink 1s infinite alternate;
}

@keyframes blink {
    0% { opacity: 0.2; transform: scale(0.8); }
    100% { opacity: 1; transform: scale(1.2); }
}

/* stagger dots */
.dot:nth-child(1) { animation-delay: 0s; }
.dot:nth-child(2) { animation-delay: 0.1s; }
.dot:nth-child(3) { animation-delay: 0.2s; }
.dot:nth-child(4) { animation-delay: 0.3s; }
.dot:nth-child(5) { animation-delay: 0.4s; }
.dot:nth-child(6) { animation-delay: 0.5s; }

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================

st.markdown("# world cup simulator")

st.markdown("<div style='text-align:center; opacity:0.7;'>simulate alternate tournament realities using monte carlo chaos</div>", unsafe_allow_html=True)

# pac-man blinking separator
st.markdown("""
<div class="pac-line">
    <div class="dot"></div>
    <div class="dot"></div>
    <div class="dot"></div>
    <div class="dot"></div>
    <div class="dot"></div>
    <div class="dot"></div>
</div>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.markdown("<div class='sidebar-title'>world cup simulator</div>", unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    <div style='font-size:11px; line-height:1.6; opacity:0.8;'>
    this slider controls the number of monte carlo simulations.<br><br>
    each simulation runs a full tournament path using probabilistic match outcomes derived from team strength assumptions.<br><br>
    higher values = more stable probabilities but slower computation.
    </div>
    """, unsafe_allow_html=True)

    sims = st.slider("simulations", 1000, 20000, 5000)

    st.markdown("---")

# =========================
# CENTER RUN BUTTON
# =========================

colA, colB, colC = st.columns([1,2,1])

with colB:
    run = st.button("run simulation")

# =========================
# OPTIONAL GRAPHIC SLOT
# =========================

st.markdown("")

col1, col2 = st.columns([2,1])

with col1:

    st.markdown("## results feed")

    if run:

        results = simulate(int(sims))  # assumes your backend exists

        df = pd.DataFrame(results.items(), columns=["team", "wins"])
        df["prob"] = df["wins"] / df["wins"].sum()
        df = df.sort_values("prob", ascending=False)

        for _, r in df.iterrows():
            st.markdown(f"""
            <div style="
                border:1px solid #111;
                padding:14px;
                margin-bottom:10px;
                border-radius:10px;
                box-shadow: 0 0 10px rgba(0,255,247,0.1);
            ">
                <b style="color:#fff; text-shadow:0 0 5px #00fff7;">
                    {r['team']}
                </b><br>
                <span style="opacity:0.7;">win probability: {r['prob']:.2%}</span>
            </div>
            """, unsafe_allow_html=True)

        st.bar_chart(df.set_index("team")["prob"])

    else:
        st.markdown("""
        <div style="opacity:0.7; padding:20px;">
        run simulation to generate tournament outcomes
        </div>
        """)

with col2:

    st.markdown("## visual")

    st.markdown("""
    <div style="
        border:1px solid #111;
        padding:10px;
        border-radius:10px;
        opacity:0.8;
    ">
    image slot (insert pinterest graphics here)
    </div>
    """, unsafe_allow_html=True)

    # example image hook
    # st.image("your_image.png")
