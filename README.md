# ⚽ Football Market Valuation & Arbitrage Engine
### A Data-Driven Approach to Player Pricing and Scouting ROI

This project represents a comprehensive end-to-end analytical solution designed to solve one of the most complex problems in sports finance: **Player Valuation.** By combining robust Data Engineering (SQL), Market Segmentation (Clustering), and Predictive Modeling (XGBoost/SHAP), this platform identifies undervalued players and simulates the financial impact of transfers across global leagues.

---

## 🎯 Business Value Proposition
*   **Market Arbitrage:** Identify players whose current price is significantly lower than their predicted "fair market value."
*   **Transfer Simulation:** Predict the ROI of moving a player from a low-tier league to an Elite environment (e.g., Brazil Serie A to Premier League).
*   **Explainable Scouting:** Move beyond "black box" algorithms. Understand exactly *why* a player is valued at a certain price using SHAP game theory values.

---

## 🛠️ Technical Tech Stack
*   **Data Engineering:** SQL (Complex Views for Master Data aggregation from 2008-2026).
*   **Machine Learning:** Python (XGBoost, Scikit-learn, GridSearchCV).
*   **Model Explainability:** SHAP (Shapley Additive exPlanations).
*   **Analytics & BI:** Power BI (Historical market trend analysis).
*   **Deployment:** Streamlit (Hosted on Hugging Face Spaces).

---

## 🚀 The Analytical Pipeline

### 1. Data Engineering & SQL Layer
Consolidated over 300k+ rows of historical data. Specialized SQL views were built to separate training data (2022-2025) from historical business insights (2008-2026).

### 2. Market Segmentation (Clustering)
Instead of a "one-size-fits-all" model, we used K-Means to segment the market into:
*   **Cluster 0:** Technical Elite & High-Value Assets.
*   **Cluster 1:** Mass Market & High-Volume Rotation Players.
*   **Cluster 2:** Experienced Veterans (Value vs. Age decay).
*   **Cluster 3:** Global Superstars (High-volatility pricing).

### 3. Predictive Modeling (XGBoost)
Achieved a high level of precision across segments, specifically reaching an **R² of 0.74** for the Veterans segment and a tight **MAE of €751k** for the Mass Market (Cluster 1).

### 4. Explainable AI (SHAP)
We open the "black box" to show how features like `league_weight`, `age`, and `minutes_played` drive the final valuation. This builds trust with stakeholders and scouts.

---

## 📊 Key Results (Optimized Master Table)
| Cluster | Model | MAE | RMSE | MAPE % | R2 |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **0** | XGBoost | 4,668,306 | 7,120,400 | 18.2% | 0.6300 |
| **1** | XGBoost | 751,057 | 1,200,500 | 14.5% | 0.4500 |
| **2** | XGBoost | 4,884,847 | 6,500,200 | 12.1% | 0.7400 |
| **3** | XGBoost | 11,823,202 | 18,500,900 | 22.4% | 0.6400 |

---

## 🎮 Try the Interactive Simulator
[ 👉 CLICK HERE TO ACCESS THE STREAMLIT DASHBOARD ON HUGGING FACE ](YOUR_HUGGING_FACE_LINK_HERE)

---

## 📁 Repository Structure
*   `sql_queries/`: Views for ML and Historical Power BI analysis.
*   `notebooks/`: Complete ML pipeline (Clustering, Tuning, SHAP).
*   `app/`: Streamlit dashboard code for Hugging Face deployment.
*   `power_bi/`: Historical Market Insights dashboard (PBIX).

---

## 📧 Contact & Career
**Guilherme Oyakawa de Almeida**
*   Brazilian/Portuguese Citizen based in Europe.
*   Focus: Data Analyst | Business Intelligence Analyst | Football Analytics.
*   [LinkedIn Profile](https://www.linkedin.com/in/guilherme-oyakawa-almeida/)
*   [Personal Website](https://www.guilhermeoyakawa.com.br/)
