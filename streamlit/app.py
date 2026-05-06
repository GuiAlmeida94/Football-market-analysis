import streamlit as st
import pandas as pd
import numpy as np
import pickle
import xgboost as xgb
from PIL import Image
import os

# 1. Page Configuration
st.set_page_config(page_title="Football Arbitrage Engine", layout="wide", page_icon="⚽")

# Custom CSS for professional branding
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    h1, h2, h3 { color: #1e3a8a; }
    </style>
    """, unsafe_allow_html=True)

# 2. Loading Resources
@st.cache_resource
def load_model():
    # Model is in the root directory as per your GitHub screenshot
    model_path = 'final_model.pkl'
    if os.path.exists(model_path):
        with open(model_path, 'rb') as f:
            return pickle.load(f)
    return None

model = load_model()

# 3. Sidebar - Profile and Market Selection
st.sidebar.header("👤 Player Technical Profile")
age = st.sidebar.slider("Age", 16, 40, 24)
minutes = st.sidebar.number_input("Total Minutes", 0, 3500, 1500)
goals = st.sidebar.number_input("Goals", 0, 50, 5)
assists = st.sidebar.number_input("Assists", 0, 30, 3)

st.sidebar.divider()
st.sidebar.header("🌍 Market Selection")
current_weight = st.sidebar.selectbox("Current League Level", [1, 2, 3, 4, 5], index=1)
target_weight = st.sidebar.selectbox("Target League Level", [1, 2, 3, 4, 5], index=4)

# 4. Main Layout with Tabs
tab1, tab2, tab3 = st.tabs(["🎮 Valuation Simulator", "📊 Market Analysis", "🔍 Model Explainability"])

# --- TAB 1: SIMULATOR ---
with tab1:
    st.header("Transfer Arbitrage Simulator")
    st.markdown("Simulate the financial impact of transferring players across global league tiers.")
    
    if model:
        # Prediction Logic
        def get_val(w, a, m, g, ast):
            # Feature order must match exactly your X_train columns
            features = pd.DataFrame([[a, m, g, ast, w]], 
                                    columns=['age_at_valuation', 'total_minutes', 'total_goals', 'total_assists', 'league_weight'])
            log_pred = model.predict(features)[0]
            return np.expm1(log_pred)

        val_cur = get_val(current_weight, age, minutes, goals, assists)
        val_tar = get_val(target_weight, age, minutes, goals, assists)
        diff = val_tar - val_cur
        roi = (diff / val_cur) * 100

        c1, c2, c3 = st.columns(3)
        c1.metric("Current Value", f"€ {val_cur:,.2f}")
        c2.metric("Target Value", f"€ {val_tar:,.2f}")
        c3.metric("Arbitrage Potential", f"€ {diff:,.2f}", delta=f"{roi:.1f}%")
        
        st.success(f"**Insight:** This transfer strategy projects a market value increase of **€ {diff:,.2f}**.")
    else:
        st.error("Model 'final_model.pkl' not found in root directory. Please check your GitHub upload.")

# --- TAB 2: MARKET ANALYSIS ---
with tab2:
    st.header("Market Segmentation & Data Distribution")
    st.markdown("Visual evidence of how the global market distributes value across clusters.")
    
    col_img1, col_img2 = st.columns(2)
    
    with col_img1:
        st.subheader("Value Dispersion by Cluster")
        # Referencing the images folder
        st.image("images/cluster_dispersion.png", caption="Statistical dispersion of market values.")

    with col_img2:
        st.subheader("Geographic Concentration")
        st.image("images/league_distribution.png", caption="Player volume by cluster across Top Leagues.")

# --- TAB 3: MODEL EXPLAINABILITY ---
with tab3:
    st.header("Explainable AI (SHAP Analysis)")
    st.markdown("Transparency report: Understanding the drivers behind the algorithm.")
    
    st.subheader("Global Feature Impact")
    st.image("images/shap_summary.png", use_container_width=True, caption="SHAP Summary Plot: Feature importance and direction.")
    
    st.markdown("---")
    
    st.subheader("Individual Valuation Breakdown")
    st.image("images/shap_waterfall.png", use_container_width=True, caption="SHAP Waterfall: Itemized receipt for a specific valuation.")
    
    st.write("""
    **Analytical Findings:**
    * **League Weight:** Primary driver of high valuations in the modern market.
    * **Age Decay:** Significant negative pressure as players exceed peak physical years.
    * **Engagement:** Minutes and games act as a reliability multiplier for technical stats.
    """)

# 5. Footer
st.divider()
st.caption("Developed by Guilherme Oyakawa de Almeida | Football Data Analytics Portfolio")
