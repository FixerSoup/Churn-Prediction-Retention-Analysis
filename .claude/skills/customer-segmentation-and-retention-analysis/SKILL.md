---
name: customer-segmentation-retention   
description: >
  End-to-end production skill for Customer Segmentation and Retention Analysis projects.
  Trigger this skill whenever the user mentions customer segmentation, churn prediction,
  retention analysis, RFM analysis, cohort analysis, CLV/LTV modeling, ARIMA forecasting,
  TabFM, customer clustering, or any related ML workflow. This skill governs how Claude
  explains concepts, structures code, selects models, and produces outputs throughout the
  full project lifecycle — from raw data to production deployment. Always use this skill
  when the user is working on this project, even if they only ask a small question about
  one module, because context continuity and conceptual depth matter across every stage.
---

# Customer Segmentation & Retention Analysis — Production Project Skill

## 🎯 Skill Purpose

This skill ensures Claude produces:
- **Production-grade code** that is modular, documented, and deployable
- **Deep conceptual explanations** so the user genuinely understands what each model/technique does and *why*
- **Consistent project structure** across all stages from EDA to deployment
- **Smart model selection** using the right tool for each problem (ARIMA, TabFM, sklearn, etc.)
- **Real-world thinking** — handling missing data, class imbalance, drift, and scalability

---

## 🗂️ Project Structure

Always scaffold and refer to this directory structure:

```
customer_segmentation_retention/
│
├── data/
│   ├── raw/                  # Original CSVs, never modified
│   ├── processed/            # Cleaned, feature-engineered data
│   └── external/             # Any third-party or lookup data
│
├── notebooks/
│   ├── 01_EDA.ipynb
│   ├── 02_Feature_Engineering.ipynb
│   ├── 03_Segmentation.ipynb
│   ├── 04_Churn_Prediction.ipynb
│   ├── 05_Retention_Forecasting.ipynb
│   └── 06_Model_Evaluation.ipynb
│
├── scripts/
│   ├── preprocess.py
│   ├── features.py
│   ├── segmentation.py
│   ├── churn_model.py
│   ├── retention_forecast.py
│   └── evaluate.py
│
├── models/
│   ├── saved/                # Serialized models (.pkl, .joblib, .pt)
│   └── reports/              # Metrics, confusion matrices, SHAP plots
│
├── api/
│   ├── app.py                # FastAPI serving layer
│   └── schemas.py
│
├── tests/
│   └── test_pipeline.py
│
├── .env
├── requirements.txt
└── README.md
```

---

## 📚 Concept Explanation Standard

**Every time Claude introduces a model, algorithm, or technique, it MUST:**

1. **What it is** — plain English definition (1-2 sentences)
2. **Why we use it here** — specific justification for this project
3. **How it works** — intuitive explanation + key formula/diagram if needed
4. **Hyperparameters that matter** — what to tune and why
5. **Limitations** — what can go wrong, and how to handle it
6. **Code** — clean, commented, production-ready implementation

---

## 🔬 Stage-by-Stage Project Roadmap

### STAGE 1 — Data Understanding & EDA

**Goal:** Understand the dataset shape, distributions, quality, and business context.

**Key concepts to explain when covering EDA:**
- Difference between transactional, behavioral, and demographic data
- Why data quality matters more than model complexity
- How to identify target leakage early

**Standard EDA outputs Claude should produce:**
- Missing value heatmaps
- Distribution plots per feature
- Correlation matrix
- Purchase frequency and monetary distributions
- Temporal patterns (seasonality, trends)

**Code pattern:**
```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def run_eda(df: pd.DataFrame, target_col: str = "churn_flag"):
    """
    Produces a full EDA report for customer data.
    Always explain what each plot tells us about the business.
    """
    print(f"Shape: {df.shape}")
    print(f"\nMissing values:\n{df.isnull().sum()}")
    print(f"\nClass balance:\n{df[target_col].value_counts(normalize=True)}")
    
    # Distribution of key metrics
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    for ax, col in zip(axes.flat, df.select_dtypes('number').columns[:4]):
        sns.histplot(df[col], ax=ax, kde=True)
        ax.set_title(f"Distribution of {col}")
    plt.tight_layout()
    plt.savefig("models/reports/eda_distributions.png", dpi=150)
```

---

### STAGE 2 — Feature Engineering

**Goal:** Build meaningful features that capture customer behavior signals.

**Key techniques Claude uses here:**

#### RFM Features (Recency, Frequency, Monetary)
```
📖 CONCEPT: RFM Analysis
- WHAT: A behavioral segmentation framework measuring 3 dimensions of customer value
- WHY: Proven, interpretable, and directly maps to business action
- HOW:
  • Recency    = Days since last purchase (lower = better)
  • Frequency  = Number of purchases in time window
  • Monetary   = Total spend in time window
- LIMITATION: Ignores product diversity, doesn't capture trend direction
```

```python
def compute_rfm(df: pd.DataFrame, snapshot_date: str) -> pd.DataFrame:
    """
    Computes RFM scores per customer.
    snapshot_date: reference date for recency calculation (e.g., '2024-12-31')
    """
    snapshot = pd.Timestamp(snapshot_date)
    rfm = df.groupby("customer_id").agg(
        recency   = ("purchase_date", lambda x: (snapshot - x.max()).days),
        frequency = ("purchase_date", "count"),
        monetary  = ("total_spend", "sum")
    ).reset_index()
    return rfm
```

**Other features to engineer:**
- `avg_order_value` = monetary / frequency
- `purchase_gap_std` = standard deviation of days between purchases (loyalty signal)
- `category_diversity` = count of unique product categories purchased
- `trend_spend` = slope of spend over time (growing vs. declining customer)
- `days_since_first_purchase` = customer tenure

---

### STAGE 3 — Customer Segmentation

**Models to use (in order of complexity):**

#### 3a. K-Means Clustering
```
📖 CONCEPT: K-Means Clustering
- WHAT: Partitions customers into K groups by minimizing within-cluster variance
- WHY: Fast, interpretable, works well on scaled RFM data
- HOW: Iteratively assigns points to nearest centroid, recomputes centroids
- KEY HYPERPARAMETERS:
  • n_clusters (K): Use Elbow Method + Silhouette Score to choose
  • init='k-means++': Smarter initialization, avoids bad local minima
- LIMITATION: Assumes spherical clusters, sensitive to outliers, needs scaling
```

```python
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import numpy as np

def find_optimal_k(X_scaled, k_range=range(2, 11)):
    """
    Uses Elbow Method and Silhouette Score to find best K.
    Always visualize both — elbow tells you diminishing returns,
    silhouette tells you how well-separated clusters actually are.
    """
    inertias, silhouettes = [], []
    for k in k_range:
        km = KMeans(n_clusters=k, init='k-means++', random_state=42, n_init=10)
        labels = km.fit_predict(X_scaled)
        inertias.append(km.inertia_)
        silhouettes.append(silhouette_score(X_scaled, labels))
    return inertias, silhouettes

def segment_customers(rfm: pd.DataFrame, n_clusters: int = 4) -> pd.DataFrame:
    features = ["recency", "frequency", "monetary"]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(rfm[features])
    
    km = KMeans(n_clusters=n_clusters, init='k-means++', random_state=42, n_init=10)
    rfm["segment"] = km.fit_predict(X_scaled)
    
    # Label segments by business meaning
    segment_summary = rfm.groupby("segment")[features].mean()
    print(segment_summary)  # Inspect to assign labels like "Champions", "At Risk"
    return rfm, km, scaler
```

#### 3b. Hierarchical Clustering (for smaller datasets)
```
📖 CONCEPT: Agglomerative Hierarchical Clustering
- WHAT: Builds a tree of clusters (dendrogram) by merging closest pairs bottom-up
- WHY: Doesn't require pre-specifying K; dendrogram visually reveals natural groupings
- HOW: Each customer starts as its own cluster; merge by linkage criterion
  • Ward linkage: minimizes total within-cluster variance (best for RFM)
- LIMITATION: O(n²) memory — use only on <50k customers
```

#### 3c. DBSCAN (for noise-robust clustering)
```
📖 CONCEPT: DBSCAN
- WHAT: Density-based clustering that auto-detects outliers as noise (-1 label)
- WHY: Finds non-spherical clusters; flags truly anomalous customers automatically
- KEY PARAMS: eps (neighborhood radius), min_samples (minimum cluster density)
- LIMITATION: Sensitive to eps — must tune carefully; struggles in high dimensions
```

---

### STAGE 4 — Churn Prediction

**This is a binary classification problem: will a customer churn in the next N days?**

#### 4a. Baseline — Logistic Regression
```
📖 CONCEPT: Logistic Regression for Churn
- WHAT: Models probability of churn as sigmoid(wX + b)
- WHY: Interpretable coefficients, fast to train, great baseline
- OUTPUT: Probability score [0,1] — threshold at 0.3-0.4 for imbalanced churn data
- LIMITATION: Assumes linear decision boundary; misses feature interactions
```

#### 4b. Primary Model — XGBoost / LightGBM
```
📖 CONCEPT: Gradient Boosted Trees
- WHAT: Ensemble of decision trees built sequentially, each correcting prior errors
- WHY: Best-in-class for tabular churn data; handles missing values natively
- KEY PARAMS:
  • n_estimators: number of trees (100-1000, use early stopping)
  • max_depth: tree depth (3-7 for tabular data)
  • learning_rate: step size (0.01-0.1, lower = more robust)
  • scale_pos_weight: handles class imbalance (set to neg/pos ratio)
- LIMITATION: Less interpretable — use SHAP values to explain predictions
```

```python
import lightgbm as lgb
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score, classification_report
import shap

def train_churn_model(X_train, y_train, X_val, y_val):
    """
    Trains LightGBM churn model with early stopping.
    scale_pos_weight handles the class imbalance problem
    (churners are always the minority class).
    """
    neg, pos = (y_train == 0).sum(), (y_train == 1).sum()
    
    model = lgb.LGBMClassifier(
        n_estimators=1000,
        learning_rate=0.05,
        max_depth=6,
        num_leaves=31,
        scale_pos_weight=neg/pos,  # Corrects for class imbalance
        random_state=42,
        n_jobs=-1
    )
    model.fit(
        X_train, y_train,
        eval_set=[(X_val, y_val)],
        callbacks=[lgb.early_stopping(50), lgb.log_evaluation(100)]
    )
    
    preds = model.predict_proba(X_val)[:, 1]
    print(f"ROC-AUC: {roc_auc_score(y_val, preds):.4f}")
    return model

def explain_churn_model(model, X_val):
    """
    SHAP values explain WHY the model predicts churn for each customer.
    This is critical for business trust and actionability.
    """
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_val)
    shap.summary_plot(shap_values, X_val, plot_type="bar")
```

#### 4c. Advanced — TabFM (Tabular Foundation Model)
```
📖 CONCEPT: TabFM — Tabular Foundation Models
- WHAT: Large pretrained models specifically designed for tabular data
  (e.g., TabPFN, SAINT, TabNet, or newer foundation models)
- WHY: Zero-shot or few-shot performance on small datasets where XGBoost
  overfits; captures complex feature interactions automatically
- HOW: Pretrained on thousands of tabular datasets; fine-tuned on your data
- WHEN TO USE:
  • Dataset < 10k rows (TabFM shines on small data)
  • When XGBoost overfits despite regularization
  • When you need uncertainty estimates per prediction
- LIMITATION: Slower inference; less customizable than gradient boosting
```

```python
# TabPFN example (pip install tabpfn)
from tabpfn import TabPFNClassifier

def train_tabfm_churn(X_train, y_train, X_val, y_val):
    """
    TabPFN: A transformer trained on synthetic tabular datasets.
    Works extremely well out-of-the-box on small datasets (<10k rows).
    No hyperparameter tuning needed — it's a foundation model.
    """
    model = TabPFNClassifier(device='cpu', N_ensemble_configurations=32)
    model.fit(X_train, y_train)
    
    preds = model.predict_proba(X_val)[:, 1]
    print(f"TabFM ROC-AUC: {roc_auc_score(y_val, preds):.4f}")
    return model
```

**Model Selection Guide:**
| Dataset Size | Recommended Model |
|---|---|
| < 5k rows | TabPFN (TabFM) |
| 5k – 100k rows | LightGBM / XGBoost |
| > 100k rows | LightGBM + neural features |
| Real-time scoring needed | LightGBM (fastest inference) |

---

### STAGE 5 — Retention Forecasting with ARIMA

```
📖 CONCEPT: ARIMA (AutoRegressive Integrated Moving Average)
- WHAT: Classical time series model for forecasting future values
- WHY: Forecasts aggregate retention rate, churn rate, or revenue over time
- HOW:
  • AR(p): Uses past p values to predict next value (autoregression)
  • I(d):  Differencing d times to make series stationary (removes trend)
  • MA(q): Uses past q forecast errors to correct predictions
  • Full model: ARIMA(p, d, q)
- STATIONARITY: ARIMA requires stationary data (constant mean/variance)
  → Test with ADF (Augmented Dickey-Fuller) test
  → If non-stationary: difference once (d=1) or log-transform
- KEY PARAMS: Use auto_arima (pmdarima) to find best p,d,q automatically
- SEASONAL VARIANT: SARIMA(p,d,q)(P,D,Q,m) — use when monthly/weekly patterns exist
- LIMITATION: Linear model only; can't capture sudden behavioral shifts
```

```python
import pmdarima as pm
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt

def test_stationarity(series, name="Series"):
    """
    ADF Test: If p-value < 0.05, series is stationary (good for ARIMA).
    If not, we need to difference the data.
    """
    result = adfuller(series.dropna())
    print(f"ADF Statistic: {result[0]:.4f}")
    print(f"p-value: {result[1]:.4f}")
    print("✅ Stationary" if result[1] < 0.05 else "❌ Not stationary — apply differencing")

def forecast_retention(monthly_retention: pd.Series, periods: int = 6):
    """
    Forecasts retention rate for next N months using auto ARIMA.
    
    monthly_retention: Series indexed by month with retention rate [0,1]
    periods: how many months ahead to forecast
    """
    # Auto-selects best ARIMA order using AIC criterion
    model = pm.auto_arima(
        monthly_retention,
        seasonal=True,
        m=12,               # 12 = monthly seasonality
        stepwise=True,      # Faster search
        suppress_warnings=True,
        error_action='ignore'
    )
    print(model.summary())
    
    forecast, conf_int = model.predict(n_periods=periods, return_conf_int=True)
    
    # Visualize forecast with confidence intervals
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(monthly_retention.index, monthly_retention, label="Historical")
    future_idx = pd.date_range(monthly_retention.index[-1], periods=periods+1, freq='M')[1:]
    ax.plot(future_idx, forecast, label="Forecast", color='orange')
    ax.fill_between(future_idx, conf_int[:,0], conf_int[:,1], alpha=0.3, color='orange')
    ax.set_title("Retention Rate Forecast (ARIMA)")
    ax.legend()
    plt.savefig("models/reports/retention_forecast.png", dpi=150)
    return forecast, model
```

---

### STAGE 6 — Cohort Analysis

```
📖 CONCEPT: Cohort Analysis
- WHAT: Groups customers by acquisition month and tracks their retention over time
- WHY: Reveals whether retention is improving across newer cohorts (product health signal)
- OUTPUT: Heatmap where rows = acquisition cohort, columns = months since acquisition
```

```python
def cohort_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Builds cohort retention matrix.
    Each cell = % of cohort still active at month N.
    """
    df['acquisition_month'] = df.groupby('customer_id')['purchase_date'].transform('min').dt.to_period('M')
    df['purchase_month'] = df['purchase_date'].dt.to_period('M')
    df['cohort_index'] = (df['purchase_month'] - df['acquisition_month']).apply(lambda x: x.n)
    
    cohort_data = df.groupby(['acquisition_month', 'cohort_index'])['customer_id'].nunique().reset_index()
    cohort_pivot = cohort_data.pivot(index='acquisition_month', columns='cohort_index', values='customer_id')
    retention_matrix = cohort_pivot.divide(cohort_pivot.iloc[:, 0], axis=0)
    
    plt.figure(figsize=(16, 8))
    sns.heatmap(retention_matrix, annot=True, fmt='.0%', cmap='RdYlGn', vmin=0, vmax=1)
    plt.title("Cohort Retention Matrix")
    plt.savefig("models/reports/cohort_heatmap.png", dpi=150)
    return retention_matrix
```

---

### STAGE 7 — Customer Lifetime Value (CLV)

```
📖 CONCEPT: Customer Lifetime Value
- WHAT: Expected total revenue a customer generates over their relationship with the business
- WHY: Drives resource allocation — spend more retaining high-CLV customers
- MODELS:
  • Simple: CLV = avg_order_value × purchase_frequency × avg_customer_lifespan
  • BG/NBD model: Probabilistic model (use lifetimes library) — gold standard
  • ML approach: Predict CLV as a regression target using customer features
```

```python
# BG/NBD + Gamma-Gamma model (probabilistic CLV)
from lifetimes import BetaGeoFitter, GammaGammaFitter

def compute_probabilistic_clv(rfm: pd.DataFrame, time_horizon: int = 12):
    """
    BG/NBD models purchase frequency.
    Gamma-Gamma models monetary value.
    Combined → Expected CLV over time_horizon months.
    """
    bgf = BetaGeoFitter(penalizer_coef=0.01)
    bgf.fit(rfm['frequency'], rfm['recency'], rfm['T'])  # T = customer age in days
    
    ggf = GammaGammaFitter(penalizer_coef=0.01)
    ggf.fit(rfm['frequency'], rfm['monetary'])
    
    rfm['predicted_clv'] = ggf.customer_lifetime_value(
        bgf, rfm['frequency'], rfm['recency'],
        rfm['T'], rfm['monetary'], time=time_horizon, freq='D'
    )
    return rfm
```

---

### STAGE 8 — Model Evaluation Standards

**Claude always reports these metrics for churn models:**

```python
from sklearn.metrics import (
    roc_auc_score, average_precision_score,
    confusion_matrix, classification_report, ConfusionMatrixDisplay
)

def full_evaluation_report(y_true, y_pred_proba, threshold=0.35):
    """
    Comprehensive evaluation for imbalanced churn classification.
    
    WHY THESE METRICS:
    - ROC-AUC: Overall discrimination ability (threshold-independent)
    - PR-AUC: Better for imbalanced classes than ROC-AUC
    - Precision@threshold: Of predicted churners, how many actually churn?
    - Recall@threshold: Of actual churners, how many did we catch?
    - F1: Harmonic mean — balances precision and recall
    """
    y_pred = (y_pred_proba >= threshold).astype(int)
    
    print(f"ROC-AUC:  {roc_auc_score(y_true, y_pred_proba):.4f}")
    print(f"PR-AUC:   {average_precision_score(y_true, y_pred_proba):.4f}")
    print(f"\nAt threshold {threshold}:")
    print(classification_report(y_true, y_pred))
    
    ConfusionMatrixDisplay.from_predictions(y_true, y_pred)
    plt.savefig("models/reports/confusion_matrix.png", dpi=150)
```

---

### STAGE 9 — Production API (FastAPI)

```python
# api/app.py
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI(title="Customer Churn Prediction API")

model = joblib.load("models/saved/churn_model.joblib")
scaler = joblib.load("models/saved/scaler.joblib")

class CustomerFeatures(BaseModel):
    recency: float
    frequency: float
    monetary: float
    avg_order_value: float
    category_diversity: int
    days_since_first_purchase: int

@app.post("/predict/churn")
def predict_churn(customer: CustomerFeatures):
    """
    Returns churn probability and risk segment for a single customer.
    """
    X = pd.DataFrame([customer.dict()])
    prob = model.predict_proba(X)[0][1]
    risk = "HIGH" if prob > 0.6 else "MEDIUM" if prob > 0.3 else "LOW"
    return {"churn_probability": round(prob, 4), "risk_segment": risk}
```

---

## 🧠 Conceptual Learning Checklist

Claude tracks whether the user has been taught each concept. If not yet covered, introduce it at the relevant stage:

- [ ] What is class imbalance and why it matters for churn
- [ ] Difference between correlation and causation in feature selection
- [ ] Why train/val/test split must respect time (no data leakage)
- [ ] What stationarity means and why ARIMA needs it
- [ ] What SHAP values are and how to interpret them
- [ ] Difference between precision and recall — which matters more for churn?
- [ ] What overfitting looks like and 3 ways to prevent it
- [ ] Why CLV matters more than churn rate alone

---

## ⚙️ Dependencies

```
# requirements.txt
pandas>=2.0
numpy>=1.24
scikit-learn>=1.3
lightgbm>=4.0
xgboost>=2.0
pmdarima>=2.0
statsmodels>=0.14
lifetimes>=0.11
shap>=0.44
tabpfn>=0.1.9
fastapi>=0.100
uvicorn>=0.23
python-dotenv>=1.0
matplotlib>=3.7
seaborn>=0.12
jupyter>=1.0
```

---

## 🚦 Output Quality Rules

Claude must always:
1. **Explain before coding** — never drop code without a concept explanation
2. **Comment every non-obvious line** — especially model parameters
3. **Flag data leakage risks** whenever time-based features are engineered
4. **Suggest next step** at the end of every stage response
5. **Use consistent variable names** matching the project structure above
6. **Save all plots** to `models/reports/` with descriptive filenames
7. **Print shape and dtypes** after every data transformation
8. **Validate outputs** — assert no nulls, check value ranges after each step
