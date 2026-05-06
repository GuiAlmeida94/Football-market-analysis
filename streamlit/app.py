import streamlit as st
import pandas as pd
import numpy as np
import pickle
import xgboost as xgb
from PIL import Image

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
    # Ensure final_model.pkl is uploaded to your Space
    with open('final_model.pkl', 'rb') as f:
        return pickle.load(f)

# Using try-except to handle cases where the model isn't uploaded yet
try:
    model = load_model()
except FileNotFoundError:
    model = None

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
    st.markdown("Use this tool to simulate the ROI of moving a player between different league tiers.")
    
    if model:
        # Prediction Logic
        def get_val(w, a, m, g, ast):
            # Feature order must match X_train: [age, minutes, goals, assists, league_weight]
            features = pd.DataFrame([[a, m, g, ast, w]], 
                                    columns=['age_at_valuation', 'total_minutes', 'total_goals', 'total_assists', 'league_weight'])
            return np.expm1(model.predict(features)[0])

        val_cur = get_val(current_weight, age, minutes, goals, assists)
        val_tar = get_val(target_weight, age, minutes, goals, assists)
        diff = val_tar - val_cur
        roi = (diff / val_cur) * 100

        c1, c2, c3 = st.columns(3)
        c1.metric("Current Value", f"€ {val_cur:,.2f}")
        c2.metric("Target Value", f"€ {val_tar:,.2f}")
        c3.metric("Arbitrage Potential", f"€ {diff:,.2f}", delta=f"{roi:.1f}%")
        
        st.success(f"**Insight:** This transfer strategy projects a market value increase of **€ {diff:,.2f}** based on league tier escalation.")
    else:
        st.warning("Model file (final_model.pkl) not found. Please upload it to enable the simulator.")

# --- TAB 2: MARKET ANALYSIS ---
with tab2:
    st.header("Market Segmentation & Data Distribution")
    st.markdown("Understanding how the global market distributes value across different player clusters.")
    
    col_img1, col_img2 = st.columns(2)
    
    with col_img1:
        st.subheader("Value Dispersion by Cluster")
        # Ensure output_38_0.png is in the app folder
        st.image("output_38_0.png", caption="Statistical dispersion of market values across player segments.")
        st.info("Note how Cluster 3 (Superstars) presents extreme volatility compared to the Mass Market (Cluster 1).")

    with col_img2:
        st.subheader("Geographic Concentration")
        # Ensure output_37_0.png is in the app folder
        st.image("output_37_0.png", caption="Player volume by cluster across Top Leagues.")
        st.info("The Premier League shows a disproportionate concentration of high-value assets (Clusters 0 and 3).")

# --- TAB 3: MODEL EXPLAINABILITY ---
with tab3:
    st.header("Explainable AI (SHAP Analysis)")
    st.markdown("Opening the 'Black Box' to understand the variables driving player valuations.")
    
    st.subheader("Global Feature Impact")
    # Using the Summary Plot (e.g., output_57_0.png or output_58_0.png)
    st.image("output_58_0.png", use_container_width=True, caption="SHAP Summary Plot: Directional impact of features.")
    
    st.markdown("---")
    
    st.subheader("Individual Valuation Breakdown")
    # Using the Waterfall Plot (e.g., output_64_1.png)
    st.image("output_64_1.png", use_container_width=True, caption="SHAP Waterfall: How the model built the price for a specific player.")
    
    st.write("""
    **Key Takeaways:**
    * **League Weight:** The most dominant factor in player valuation.
    * **Age Decay:** Clearly visible negative impact on market value as players cross the 28-30 year threshold.
    * **Minutes Played:** Acts as a validation gate; high technical performance without minutes is heavily penalized.
    """)

# 5. Footer
st.divider()
st.caption("Developed by Guilherme Oyakawa de Almeida | Data-Driven Football Analytics")
