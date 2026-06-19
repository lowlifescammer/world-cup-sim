import streamlit as st
import pandas as pd
import numpy as np
from collections import Counter
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
    background-color: #0e0e10;
    color: #e6e6e6;
}

/* main app background */
.stApp {
    background-color: #0e0e10;
}

/* sidebar */
[data-testid="stSidebar"] {
    background-color: #111114;
}

/* headings */
h1, h2, h3 {
    letter-spacing: -0.5px;
}

/* cards */
div[data-testid="stMarkdownContainer"] {
    line-height: 1.6;
}

</style>
""", unsafe_allow_html=True)
st.markdown(f"""
<div style="
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #2a2a2a;
    background: #151518;
    margin-bottom: 10px;
">
    <div style="font-size:16px; font-weight:600;">
        {row['team']}
    </div>
    <div style="opacity:0.7;">
        win share: {row['probability']:.2%}
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown("""
<style>
:root {
    --accent: #7c5cff;
}

/* buttons */
.stButton > button {
    background-color: var(--accent);
    color: white;
    border-radius: 8px;
    border: none;
}

.stButton > button:hover {
    background-color: #6a4df0;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<div style="padding: 20px 0 10px 0;">
    <h1 style="margin-bottom:0;">world cup simulator</h1>
    <p style="opacity:0.6; margin-top:4px;">
        monte carlo simulation • team strength model • probabilistic outcomes
    </p>
</div>
""", unsafe_allow_html=True)
