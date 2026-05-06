import streamlit as st
import pandas as pd
import numpy as np
import pickle
import xgboost as xgb
import os
from PIL import Image

# 1. Page Configuration
st.set_page_config(page_title="Football Arbitrage Engine", layout="wide", page_icon="⚽")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    h1, h2, h3 { color: #1e3a8a; }
    </style>
    """, unsafe_allow_html=True)

# 2. Dynamic Path Resolution (Bulletproof for Streamlit Cloud)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@st.cache_resource
def load_model():
    model_path = os.path.join(BASE_DIR, 'final_model.pkl')
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

# 4. Main Layout with 4 Tabs now
tab1, tab2, tab3, tab4 = st.tabs(["📋 Executive Overview", "🎮 Valuation Simulator", "📊 Market Analysis", "🔍 Model Explainability"])

# --- TAB 1: EXECUTIVE OVERVIEW (NEW) ---
with tab1:
    st.header("Project Purpose & Methodology")
    st.markdown("""
    Welcome to the **Football Market Valuation & Arbitrage Engine**. 
    
    This platform was developed to solve a critical business problem in modern football: **Valuation Subjectivity**. By leveraging advanced Data Engineering and Machine Learning, this tool provides an objective, data-driven framework to price players and identify lucrative transfer arbitrage opportunities across global leagues.
    """)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("🛠️ The Analytical Pipeline")
        st.markdown("""
        * **Data Engineering (SQL):** Aggregated and cleaned over **300,000+ historical records** (2008-2026) using complex PostgreSQL views to ensure data integrity.
        * **Market Segmentation (Clustering):** Applied K-Means to divide the global market into distinct financial tiers (e.g., Mass Market, Veterans, Superstars), recognizing that a £100M player is priced differently than a £1M prospect.
        * **Predictive Engine (XGBoost/Ridge):** Trained specialized regression models for each cluster, utilizing Log-Scaling to handle extreme market volatility.
        * **Explainable AI (SHAP):** Integrated Game Theory algorithms to break down the "black box" of Machine Learning, ensuring every valuation can be explained to sporting directors.
        """)
        
    with col_b:
        st.subheader("💼 About the Author")
        st.markdown("""
        **Guilherme Oyakawa de Almeida**  
        *Data Analyst | Business Intelligence | Football Analytics*
        
        Holding dual citizenship (Brazilian/Portuguese) and actively focused on the European market, Guilherme bridges the gap between raw data and executive decision-making. His technical stack includes Python, SQL, Power BI, and Tableau, with a pragmatic approach to solving complex business problems.
        """)
    
    st.info("👉 **Navigate to the 'Valuation Simulator' tab above to test the predictive model in real-time.**")

# --- TAB 2: SIMULATOR ---
with tab2:
    st.header("Transfer Arbitrage Simulator")
    st.markdown("Simulate the financial impact of transferring players across global league tiers.")
    
    if model:
        def get_val(w, a, m, g, ast):
            expected_features = model.get_booster().feature_names
            input_df = pd.DataFrame(0, index=[0], columns=expected_features)
            
            if 'age_at_valuation' in input_df.columns: input_df['age_at_valuation'] = a
            if 'total_minutes' in input_df.columns: input_df['total_minutes'] = m
            if 'total_goals' in input_df.columns: input_df['total_goals'] = g
            if 'total_assists' in input_df.columns: input_df['total_assists'] = ast
            if 'league_weight' in input_df.columns: input_df['league_weight'] = w
                
            log_pred = model.predict(input_df)[0]
            return np.expm1(log_pred)

        val_cur = get_val(current_weight, age, minutes, goals, assists)
        val_tar = get_val(target_weight, age, minutes, goals, assists)
        diff = val_tar - val_cur
        roi = ((diff / val_cur) * 100) if val_cur > 0 else 0

        c1, c2, c3 = st.columns(3)
        c1.metric("Current Value", f"€ {val_cur:,.2f}")
        c2.metric("Target Value", f"€ {val_tar:,.2f}")
        c3.metric("Arbitrage Potential", f"€ {diff:,.2f}", delta=f"{roi:.1f}%")
        
        st.success(f"**Insight:** This transfer strategy projects a market value variance of **€ {diff:,.2f}**.")
    else:
        st.error("⚠️ Model file 'final_model.pkl' not found. Please ensure it is uploaded to the repository.")

# --- TAB 3: MARKET ANALYSIS ---
with tab3:
    st.header("Market Segmentation & Data Distribution")
    col_img1, col_img2 = st.columns(2)
    
    with col_img1:
        st.subheader("Value Dispersion by Cluster")
        img_path_1 = os.path.join(BASE_DIR, 'images', 'market_dispersion_clusters.png')
        if os.path.exists(img_path_1): st.image(Image.open(img_path_1))
        else: st.warning("Image 'market_dispersion_clusters.png' not found.")

    with col_img2:
        st.subheader("Geographic Concentration")
        img_path_2 = os.path.join(BASE_DIR, 'images', 'Market_dispersion_leagues.png')
        if os.path.exists(img_path_2): st.image(Image.open(img_path_2))
        else: st.warning("Image 'Market_dispersion_leagues.png' not found.")

# --- TAB 4: MODEL EXPLAINABILITY ---
with tab4:
    st.header("Explainable AI (SHAP Analysis)")
    
    st.subheader("Global Feature Impact")
    img_path_3 = os.path.join(BASE_DIR, 'images', 'SHAP_Summary.png')
    if os.path.exists(img_path_3): st.image(Image.open(img_path_3), use_container_width=True)
    else: st.warning("Image 'SHAP_Summary.png' not found.")
    
    st.markdown("---")
    
    st.subheader("Individual Valuation Breakdown")
    img_path_4 = os.path.join(BASE_DIR, 'images', 'SHAP_Waterfall_plot.png')
    if os.path.exists(img_path_4): st.image(Image.open(img_path_4), use_container_width=True)
    else: st.warning("Image 'SHAP_Waterfall_plot.png' not found.")

# 5. Footer
st.divider()
st.caption("Developed by Guilherme Oyakawa de Almeida | Football Data Analytics Portfolio")
