import streamlit as st
import pandas as pd
import numpy as np
import pickle
import xgboost as xgb
import os

# 1. Page Configuration
st.set_page_config(page_title="Football Arbitrage Engine", layout="wide", page_icon="⚽")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    h1, h2, h3 { color: #1e3a8a; }
    </style>
    """, unsafe_allow_html=True)

# 2. Loading Resources with Error Handling
@st.cache_resource
def load_model():
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
        # THE FIX: Robust Prediction Logic
        def get_val(w, a, m, g, ast):
            # 1. Extract exact feature names expected by the trained XGBoost model
            expected_features = model.get_booster().feature_names
            
            # 2. Create a blank DataFrame with zeros for ALL expected features
            input_df = pd.DataFrame(0, index=[0], columns=expected_features)
            
            # 3. Update only the core numerical features we are simulating
            if 'age_at_valuation' in input_df.columns:
                input_df['age_at_valuation'] = a
            if 'total_minutes' in input_df.columns:
                input_df['total_minutes'] = m
            if 'total_goals' in input_df.columns:
                input_df['total_goals'] = g
            if 'total_assists' in input_df.columns:
                input_df['total_assists'] = ast
            if 'league_weight' in input_df.columns:
                input_df['league_weight'] = w
                
            # 4. Predict using the fully constructed row
            log_pred = model.predict(input_df)[0]
            return np.expm1(log_pred)

        # Calculating values
        val_cur = get_val(current_weight, age, minutes, goals, assists)
        val_tar = get_val(target_weight, age, minutes, goals, assists)
        diff = val_tar - val_cur
        
        # Protecting against division by zero just in case
        roi = ((diff / val_cur) * 100) if val_cur > 0 else 0

        c1, c2, c3 = st.columns(3)
        c1.metric("Current Value", f"€ {val_cur:,.2f}")
        c2.metric("Target Value", f"€ {val_tar:,.2f}")
        c3.metric("Arbitrage Potential", f"€ {diff:,.2f}", delta=f"{roi:.1f}%")
        
        st.success(f"**Insight:** This transfer strategy projects a market value variance of **€ {diff:,.2f}**.")
    else:
        st.error("⚠️ Model file 'final_model.pkl' not found. Please ensure it is uploaded to the repository.")

# --- TAB 2: MARKET ANALYSIS ---
with tab2:
    st.header("Market Segmentation & Data Distribution")
    col_img1, col_img2 = st.columns(2)
    
    with col_img1:
        st.subheader("Value Dispersion by Cluster")
        # Displaying image with robust error handling
        try:
            st.image("images/cluster_dispersion.png")
        except FileNotFoundError:
            st.warning("Image 'images/cluster_dispersion.png' not found.")

    with col_img2:
        st.subheader("Geographic Concentration")
        try:
            st.image("images/league_distribution.png")
        except FileNotFoundError:
            st.warning("Image 'images/league_distribution.png' not found.")

# --- TAB 3: MODEL EXPLAINABILITY ---
with tab3:
    st.header("Explainable AI (SHAP Analysis)")
    
    st.subheader("Global Feature Impact")
    try:
        st.image("images/shap_summary.png", use_container_width=True)
    except FileNotFoundError:
        st.warning("Image 'images/shap_summary.png' not found.")
    
    st.markdown("---")
    
    st.subheader("Individual Valuation Breakdown")
    try:
        st.image("images/shap_waterfall.png", use_container_width=True)
    except FileNotFoundError:
        st.warning("Image 'images/shap_waterfall.png' not found.")
