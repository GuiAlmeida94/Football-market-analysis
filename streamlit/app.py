import streamlit as st
import pandas as pd
import numpy as np
import pickle
import xgboost as xgb
import os
from PIL import Image

# 1. Page Configuration
st.set_page_config(page_title="Capstone: Football Valuation", layout="wide", page_icon="📈")

# Estilização Profissional
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    h1 { color: #1e3a8a; font-weight: 700; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px;}
    .highlight-box { background-color: #ffffff; padding: 20px; border-left: 5px solid #1e3a8a; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 20px;}
    .metric-card { background-color: #ffffff; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center; border-top: 4px solid #3182ce;}
    </style>
    """, unsafe_allow_html=True)

# 2. Path Handling e Carregamento de Recursos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@st.cache_resource
def load_model():
    model_path = os.path.join(BASE_DIR, 'final_model.pkl')
    if os.path.exists(model_path):
        with open(model_path, 'rb') as f:
            return pickle.load(f)
    return None

model = load_model()

def load_img(name):
    path = os.path.join(BASE_DIR, 'images', name)
    return Image.open(path) if os.path.exists(path) else None

# 3. Header
st.title("⚽ Capstone Project: Football Market Valuation Engine")
st.markdown("Developed by **Guilherme Oyakawa de Almeida** | Data-Driven Football Analytics")

# 4. Navegação Principal
tabs = st.tabs([
    "1️⃣ Data Engineering", 
    "2️⃣ Market Segmentation", 
    "3️⃣ Predictive Modeling", 
    "4️⃣ Explainable AI (SHAP)",
    "5️⃣ Arbitrage Simulator"
])

# --- TAB 1: DATA ENGINEERING ---
with tabs[0]:
    st.header("1. Data Engineering & Architecture")
    st.markdown("""
    O objetivo desta fase foi transformar dados brutos do Transfermarkt em um dataset analítico mestre.
    - **Processamento SQL:** Consolidação de 300k+ registros utilizando PostgreSQL.
    - **Temporal Anchoring:** Sincronização entre estatísticas de performance e data da avaliação de mercado.
    - **Limpeza:** Filtragem de ruídos (jogadores sem minutos mínimos) para garantir o aprendizado do modelo.
    """)
    st.info("As queries SQL completas e a estrutura da `vw_master_data` estão disponíveis no repositório GitHub.")

# --- TAB 2: MARKET SEGMENTATION ---
with tabs[1]:
    st.header("2. Market Segmentation (Clustering)")
    st.markdown("Utilizamos K-Means para segmentar o mercado, reconhecendo que 'Superstars' e 'Jogadores de Rotação' possuem dinâmicas de preços diferentes.")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Dispersão de Valor por Cluster")
        img1 = load_img('market_dispersion_clusters.png')
        if img1: st.image(img1)
    with c2:
        st.subheader("Concentração por Liga")
        img2 = load_img('Market_dispersion_leagues.png')
        if img2: st.image(img2)

# --- TAB 3: PREDICTIVE MODELING ---
with tabs[2]:
    st.header("3. Machine Learning & Model Evaluation")
    st.markdown("""
    Treinamos modelos específicos para cada cluster. A variável alvo passou por uma **transformação logarítmica** para mitigar o impacto de outliers extremos.
    """)
    # Adicione aqui o gráfico de comparação de R2 se disponível
    st.subheader("Performance do Modelo (XGBoost)")
    img3 = load_img('importance_cluster_0.png') # Exemplo de importância de features
    if img3: st.image(img3, use_container_width=True)

# --- TAB 4: EXPLAINABLE AI ---
with tabs[3]:
    st.header("4. Explainable AI (SHAP)")
    st.markdown("Abrindo a 'caixa-preta' do modelo para entender o que realmente dita o valor de um jogador.")
    img4 = load_img('SHAP_Summary.png')
    if img4: st.image(img4, use_container_width=True)
    st.write("**Insights:** O peso da liga e a idade são os maiores drivers de desvalorização ou prêmio no mercado europeu.")

# --- TAB 5: SIMULATOR (A CONCLUSÃO PRÁTICA) ---
with tabs[4]:
    st.header("5. Transfer Arbitrage Simulator")
    st.markdown("""
    Esta ferramenta aplica o modelo treinado para simular o potencial de **Arbitragem de Mercado**. 
    Ela calcula quanto o valor de um jogador saltaria ao ser transferido de uma liga menor para uma liga de elite, mantendo suas estatísticas técnicas.
    """)
    
    if model:
        # Colunas de Input
        col_in1, col_in2 = st.columns(2)
        with col_in1:
            st.subheader("📊 Perfil Técnico")
            s_age = st.slider("Idade", 16, 40, 24)
            s_mins = st.number_input("Minutos Totais", 0, 3500, 1500)
            s_goals = st.number_input("Gols", 0, 50, 5)
            s_asts = st.number_input("Assistências", 0, 30, 3)
        
        with col_in2:
            st.subheader("🌍 Estratégia de Mercado")
            cur_w = st.selectbox("Nível da Liga Atual", [1, 2, 3, 4, 5], index=1)
            tar_w = st.selectbox("Nível da Liga Alvo", [1, 2, 3, 4, 5], index=4)

        # Lógica de Predição
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
        m1.metric("Valor Atual Estimado", f"€ {val_cur:,.2f}")
        m2.metric("Valor na Liga Alvo", f"€ {val_tar:,.2f}")
        m3.metric("Potencial de Arbitragem", f"€ {diff:,.2f}", delta=f"{roi:.1f}%")
    else:
        st.error("Modelo final_model.pkl não encontrado.")

st.divider()
st.caption("Guilherme Oyakawa de Almeida | Data Analyst Portfolio")
