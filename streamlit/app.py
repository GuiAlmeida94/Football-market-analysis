import streamlit as st
import os
import pandas as pd
import numpy as np
import pickle
import xgboost as xgb
from PIL import Image

# 1. Page Configuration
st.set_page_config(page_title="Capstone Project: Football Valuation", layout="wide", page_icon="📈")

# Custom CSS for a professional, academic/executive look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    h1 { color: #1e3a8a; font-weight: 700; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px;}
    h2 { color: #2d3748; font-weight: 600; margin-top: 30px;}
    h3 { color: #4a5568; font-weight: 600; }
    .highlight-box { background-color: #ffffff; padding: 20px; border-left: 5px solid #1e3a8a; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 20px;}
    .metric-card { background-color: #ffffff; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center; border-top: 4px solid #3182ce;}
    .metric-value { font-size: 24px; font-weight: bold; color: #1e3a8a; }
    .metric-label { font-size: 14px; color: #718096; text-transform: uppercase; letter-spacing: 0.5px;}
    </style>
    """, unsafe_allow_html=True)

# 2. Path Handling & Resource Loading
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_image(filename):
    img_path = os.path.join(BASE_DIR, 'images', filename)
    if os.path.exists(img_path):
        return Image.open(img_path)
    return None

@st.cache_resource
def load_model():
    model_path = os.path.join(BASE_DIR, 'final_model.pkl')
    if os.path.exists(model_path):
        with open(model_path, 'rb') as f:
            return pickle.load(f)
    return None

model = load_model()

# 3. Header Section
st.title("⚽ Capstone Project: Football Market Valuation Engine")
st.markdown("**A Data-Driven Approach to Player Pricing and Market Arbitrage**")
st.markdown("Developed by **Guilherme Oyakawa de Almeida**")

# 4. Executive Summary (The "Elevator Pitch")
st.markdown("<div class='highlight-box'>", unsafe_allow_html=True)
st.markdown("""
**Business Problem:** The football transfer market is highly subjective, often driven by emotion rather than data. This leads to inefficient capital allocation when buying or selling players.

**Solution:** An end-to-end Machine Learning pipeline that objectively calculates a player's "Fair Market Value" based on technical performance, physical attributes, and geographic league strength. 

**Why it matters:** By establishing a baseline value, sporting directors can identify **Market Arbitrage** opportunities (undervalued players) and simulate the financial ROI of moving a prospect to an Elite league.
""")
st.markdown("</div>", unsafe_allow_html=True)

# 5. Main Navigation (Tabs for logical flow)
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "1️⃣ Data Engineering", 
    "2️⃣ Market Segmentation", 
    "3️⃣ Predictive Modeling", 
    "4️⃣ Explainable AI (SHAP)",
    "5️⃣ Arbitrage Simulator"
])

# --- TAB 1: DATA ENGINEERING ---
with tab1:
    st.header("1. Data Engineering & Architecture")
    st.markdown("""
    A reliable Machine Learning model requires a bulletproof data foundation. The raw data consisted of multiple relational tables (players, clubs, appearances, valuations) spanning from 2008 to 2026.
    """)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='metric-card'><div class='metric-value'>300,000+</div><div class='metric-label'>Raw Records Processed</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='metric-card'><div class='metric-value'>PostgreSQL</div><div class='metric-label'>Database Engine</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='metric-card'><div class='metric-value'>2022-2025</div><div class='metric-label'>ML Training Window</div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    st.subheader("Key Methodologies Applied:")
    st.markdown("""
    * **Temporal Anchoring:** Created a `season_year` logic via SQL to correctly join a player's technical stats (goals, minutes) with their *exact* market valuation at that specific point in time.
    * **Feature Aggregation:** Engineered complex CTEs to calculate metrics like `starter_ratio` and `clean_sheets` per season.
    * **Noise Reduction:** Filtered out players with less than 90 minutes played to ensure the model only learned from active professionals.
    * **League Weighting:** Assigned a strategic numerical weight to leagues (e.g., Premier League = 5, Major League Soccer = 2) to capture the financial disparity between geographic markets.
    """)

# --- TAB 2: MARKET SEGMENTATION (CLUSTERING) ---
with tab2:
    st.header("2. Market Segmentation (K-Means Clustering)")
    st.markdown("""
    **The Strategic "Why":** A £100M global superstar is not priced using the same logic as a £1M rotation player. Training a single "one-size-fits-all" model would create massive errors. Therefore, K-Means clustering was applied to segment the market into distinct financial and technical tiers.
    """)
    
    col_img1, col_img2 = st.columns(2)
    
    with col_img1:
        st.subheader("Value Dispersion by Tier")
        img1 = load_image('market_dispersion_clusters.png')
        if img1: st.image(img1, caption="Statistical dispersion highlights the extreme volatility of Cluster 3 (Superstars).")
        else: st.warning("Image 'market_dispersion_clusters.png' not found.")
        
    with col_img2:
        st.subheader("Geographic Concentration")
        img2 = load_image('Market_dispersion_leagues.png')
        if img2: st.image(img2, caption="Elite leagues heavily monopolize high-value clusters.")
        else: st.warning("Image 'Market_dispersion_leagues.png' not found.")

    st.markdown("""
    **The Clusters:**
    * **Cluster 1 (Mass Market):** High volume, low volatility. The backbone of global football.
    * **Cluster 2 (Veterans):** Players transitioning out of peak age. Value is heavily tied to age decay.
    * **Cluster 0 & 3 (Elite & Superstars):** Low volume, extremely high value. Heavily concentrated in the 'Big Five' European leagues.
    """)

# --- TAB 3: PREDICTIVE MODELING ---
with tab3:
    st.header("3. Machine Learning Evaluation")
    st.markdown("""
    **The Strategic "Why":** With the market segmented, specialized regression models (XGBoost, Random Forest, Ridge, KNN) were trained for *each* cluster. 
    
    *Crucial Transformation:* The target variable (Market Value) was transformed using a **Logarithmic Scale (np.log1p)**. This was mathematically necessary to handle the severe right-skewness of football transfer fees, preventing hyper-expensive outliers from distorting the algorithm's learning process.
    """)
    
    st.subheader("Model Performance Comparison")
    img3 = load_image('model_R2_comparison_cluster.png')
    if img3: st.image(img3, use_container_width=True)
    else: st.info("Placeholder: Insert R2/MAE comparison chart here.")

    st.markdown("""
    **Results & Optimization:**
    * **GridSearchCV:** Applied to fine-tune hyperparameters (learning rate, tree depth) to prevent overfitting.
    * **Ridge Regression** proved highly effective for linear-heavy clusters (like Veterans), while **XGBoost** captured the non-linear nuances of the Mass Market.
    * **Final R²:** Achieved strong variance explanation, particularly in the Veteran segment (R² > 0.70), proving that age and minutes are highly predictive in that specific tier.
    """)

# --- TAB 4: EXPLAINABLE AI (SHAP) ---
with tab4:
    st.header("4. Explainable AI (Opening the Black Box)")
    st.markdown("""
    **The Strategic "Why":** In a corporate sports environment, an algorithm that says "Player X is worth €20M" is useless if it cannot explain *why*. Directors of Football need transparency. SHAP (Shapley Additive exPlanations) values were integrated to provide an itemized receipt for every valuation.
    """)
    
    st.subheader("Global Drivers (What matters most?)")
    img4 = load_image('SHAP_Summary.png')
    if img4: st.image(img4, use_container_width=True, caption="League Weight and Age are universally the strongest predictors of value.")
    else: st.warning("Image 'SHAP_Summary.png' not found.")
    
    st.markdown("---")
    
    st.subheader("Individual Valuation Breakdown (The 'Receipt')")
    img5 = load_image('SHAP_Waterfall_plot.png')
    if img5: st.image(img5, use_container_width=True, caption="How the model adds or subtracts value based on a player's specific metrics.")
    else: st.warning("Image 'SHAP_Waterfall_plot.png' not found.")
    
    st.markdown("""
    **Executive Insights Derived:**
    1. **The 'Premier League Tax':** Geographic location (`league_weight`) often outweighs raw technical output (goals/assists).
    2. **The Age Cliff:** The model strictly penalizes market value as players cross the 28-30 age threshold, regardless of current performance.
    3. **Minutes as a Gatekeeper:** High goal-scoring rates are heavily discounted if the player lacks sustained minutes on the pitch.
    """)

# --- TAB 5: ARBITRAGE SIMULATOR ---
with tab5:
    st.header("5. Transfer Arbitrage Simulator")
    st.markdown("""
    **Practical Application:** This tool deploys the trained XGBoost model to simulate **Market Arbitrage**. 
    It calculates the financial impact of transferring a player from a lower-tier league to an Elite environment, assuming their technical output translates proportionally.
    """)
    
    if model:
        col_in1, col_in2 = st.columns(2)
        with col_in1:
            st.subheader("📊 Technical Profile")
            s_age = st.slider("Age", 16, 40, 24)
            s_mins = st.number_input("Total Minutes", 0, 3500, 1500)
            s_goals = st.number_input("Goals", 0, 50, 5)
            s_asts = st.number_input("Assists", 0, 30, 3)
        
        with col_in2:
            st.subheader("🌍 Market Strategy")
            cur_w = st.selectbox("Current League Level (1=Minor, 5=Elite)", [1, 2, 3, 4, 5], index=1)
            tar_w = st.selectbox("Target League Level (1=Minor, 5=Elite)", [1, 2, 3, 4, 5], index=4)

        # Bruce's Note: Predictive execution using expected features
        def predict_val(w, a, m, g, ast):
            features = model.get_booster().feature_names
            input_df = pd.DataFrame(0, index=[0], columns=features)
            
            if 'age_at_valuation' in input_df.columns: input_df['age_at_valuation'] = a
            if 'total_minutes' in input_df.columns: input_df['total_minutes'] = m
            if 'total_goals' in input_df.columns: input_df['total_goals'] = g
            if 'total_assists' in input_df.columns: input_df['total_assists'] = ast
            if 'league_weight' in input_df.columns: input_df['league_weight'] = w
            
            return np.expm1(model.predict(input_df)[0])

        val_cur = predict_val(cur_w, s_age, s_mins, s_goals, s_asts)
        val_tar = predict_val(tar_w, s_age, s_mins, s_goals, s_asts)
        diff = val_tar - val_cur
        roi = (diff / val_cur * 100) if val_cur > 0 else 0

        st.divider()
        m1, m2, m3 = st.columns(3)
        m1.metric("Current Estimated Value", f"€ {val_cur:,.2f}")
        m2.metric("Target League Value", f"€ {val_tar:,.2f}")
        m3.metric("Arbitrage Potential", f"€ {diff:,.2f}", delta=f"{roi:.1f}%")
    else:
        st.error("⚠️ Model 'final_model.pkl' not found. Please upload it to enable predictions.")

# 6. Footer
st.divider()
st.caption("Capstone Project Portfolio | Built with Streamlit, Pandas, XGBoost & SHAP")
