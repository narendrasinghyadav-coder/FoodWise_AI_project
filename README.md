# FoodWise AI — Smart Food Waste Prediction and Redistribution System

> **Primary SDG:** 12 – Responsible Consumption and Production · **Secondary SDG:** 2 – Zero Hunger
>
> ⚠️ **All data in this project is synthetic (simulated).** No real canteen data was collected and no real-world impact is claimed. Reported metrics describe how well the models learn the *simulator*, not real-world accuracy.

## 1. Project overview
FoodWise AI is an end-to-end, ML-powered **decision-support** web application for canteens, hostels, hotels and institutional kitchens. It forecasts meal demand, classifies food-waste risk, estimates surplus, recommends a preparation quantity and raises *advisory* alerts about potential surplus.

## 2. Real-world problem
Kitchens often cook more than needed because demand is hard to predict → unnecessary preparation, food waste, financial loss and wasted resources, while edible surplus may be identified too late to be redistributed.

## 3. SDG alignment
- **SDG 12** – reduce over-production and food waste through better planning.
- **SDG 2** – earlier visibility of edible surplus supports *safe, human-approved* redistribution.

## 4. Proposed solution
Two scikit-learn models behind a prediction service:
1. **Demand forecasting** (regression, target `meals_sold`).
2. **Waste-risk classification** (LOW / MEDIUM / HIGH).

Business rules then compute `surplus = prepared − predicted demand`, `waste % = surplus / prepared × 100`, a recommended quantity (predicted demand + 5 % buffer) and a plain-language recommendation. The system **never** contacts NGOs or moves food.

## 5. Features
- 7-page Streamlit app: Dashboard · Demand Prediction · Waste Risk · Surplus Analysis · Analytics · Model Performance · About
- Real model predictions (nothing hard-coded), with an indicative 80 % prediction range
- Interactive Plotly charts, KPI cards, tooltips, what-if curve
- SQLite storage of history, stored predictions and prediction logs (no personal data)
- Input validation and graceful error handling; 76 automated tests

## 6. Architecture
```
 generate (synthetic) → validate → clean → EDA → features → train/compare/select → serialize
                                                                                     │
 SQLite (history, predictions, logs) ◄───────────────────────── PredictionService ◄──┘
                                                                         ▲
                                                           Streamlit UI (app/)
```
FastAPI was intentionally not used: the UI calls the in-process `PredictionService` directly, so an API layer would add no value for this prototype.

## 7. Dataset (synthetic)
~3,300 daily meal-service records (Breakfast/Lunch/Dinner, 2022-01-08 → 2024-12-31) produced by `src/data/generate_data.py`. Relationships encoded: holidays/breaks lower demand, events raise it, rain/heat/cold shift it, weekends differ, headcount scales demand, and over-preparation drives waste. A few missing values and duplicate rows are **deliberately injected** into the raw file so validation/cleaning are exercised. See [DATA_DICTIONARY.md](DATA_DICTIONARY.md).

## 8. Data preprocessing
Validation (schema, types, ranges, categories, `sold ≤ prepared`, duplicates, weekday/date consistency) → cleaning (standardise text, drop exact & key duplicates, drop invalid rows, impute temperature by monthly median and weather by mode, recompute derived columns) → strict re-validation. On the last run: 3,273 raw rows → 3,267 clean (6 duplicates removed, 12 temperatures + 5 weather values imputed).

## 9. EDA
Auto-generated with real statistics in [docs/EDA_SUMMARY.md](docs/EDA_SUMMARY.md) and visualised on the **Analytics** page. Class balance: LOW 57 %, MEDIUM 24 %, HIGH 19 %.

## 10. Feature engineering
Weekday, `is_weekend`, cyclical month (sin/cos), `avg_prev_demand`, `demand_ratio`, and — for the risk model — `prepared_per_student`, `prep_vs_prev_week`, `prep_vs_prev_day`, `prep_vs_avg_prev`. One-hot encoding for categoricals (unknown values ignored); standard scaling only for linear models.
**`meals_prepared` is intentionally excluded from the demand model** (demand must not depend on the supply decision); it is used for surplus and risk.

## 11. ML models
| Task | Candidates | Selection rule |
|---|---|---|
| Demand regression | Linear Regression, Random Forest, Gradient Boosting | lowest mean RMSE, 5-fold `TimeSeriesSplit` CV on the training period |
| Waste-risk classification | Logistic Regression, Random Forest, Gradient Boosting | highest mean macro-F1, same CV |

Time-based split: the last 20 % of dates (from 2024-05-28) form the held-out test set. Seed 42.

## 12. Model evaluation (actual results of `python -m src.pipeline`)
**Demand (test set, 654 rows)** — selected: **Gradient Boosting**

| Model | CV RMSE | Test MAE | Test RMSE | Test R² |
|---|---|---|---|---|
| Linear Regression | 102.06 | 74.04 | 100.88 | 0.911 |
| Random Forest | 78.85 | 52.54 | 71.67 | 0.955 |
| **Gradient Boosting** | **77.52** | 53.83 | 73.13 | 0.953 |
| *Baseline: previous-week demand* | – | 133.25 | 228.90 | 0.542 |

**Waste risk (test set)** — selected: **Gradient Boosting**

| Model | CV macro-F1 | Test Accuracy | Test Precision (macro) | Test Recall (macro) | Test F1 (macro) |
|---|---|---|---|---|---|
| Logistic Regression | 0.737 | 0.801 | 0.759 | 0.780 | 0.768 |
| Random Forest | 0.727 | 0.787 | 0.752 | 0.759 | 0.755 |
| **Gradient Boosting** | **0.747** | 0.791 | 0.755 | 0.740 | 0.747 |
| *Baseline: majority class* | – | 0.541 | 0.180 | 0.333 | 0.234 |

Confusion matrix (rows = actual, cols = LOW/MEDIUM/HIGH): `[[322, 32, 0], [44, 93, 24], [2, 35, 102]]`.

> Models are chosen on **cross-validation**, not on the test set. Differences between the top candidates are small, and some test scores (e.g. Random Forest RMSE, Logistic Regression F1) are slightly better than the selected model's — this is expected noise and is reported transparently. MEDIUM is the hardest class (F1 0.58) because it is the narrow middle band.

## 13. Installation
```bash
python -m venv .venv
.venv\Scripts\activate        # Windows  (source .venv/bin/activate on macOS/Linux)
pip install -r requirements.txt
```
Tested with Python 3.10, pandas 2.1, scikit-learn 1.3, Streamlit 1.47.

## 14. How to run
```bash
python run.py                  # trains if needed, then launches the app (http://localhost:8501)
```
Or step by step:
```bash
python -m src.pipeline         # generate → validate → clean → EDA → train → evaluate → save → DB (~1.5 min)
streamlit run app/dashboard.py
python -m pytest -q            # 76 tests
```
Pipeline options: `--seed N`, `--keep-raw`, `--quick` (smaller models).

## 15. Project structure
```
foodwise-ai/
├── app/
│   ├── dashboard.py            # Streamlit entry point (navigation)
│   ├── pages/                  # 7 page modules (render())
│   └── components/             # theme, charts, forms, data access, runner
├── data/{raw,processed}/       # generated CSVs (git-ignored)
├── database/db.py              # SQLite schema + helpers (foodwise.db is generated)
├── models/                     # *.joblib + metadata.json (generated)
├── notebooks/
├── src/
│   ├── config.py
│   ├── data/                   # generate_data, validation, cleaning, loader, labels, eda
│   ├── features/engineering.py
│   ├── models/train.py
│   ├── evaluation/metrics.py
│   ├── prediction/             # service.py, business_logic.py
│   └── pipeline.py
├── tests/
├── docs/EDA_SUMMARY.md
├── run.py · requirements.txt · .streamlit/config.toml
└── README.md, PROJECT_PLAN.md, PROJECT_REPORT.md, MODEL_CARD.md, DATA_DICTIONARY.md,
    TESTING.md, LIMITATIONS.md, FUTURE_SCOPE.md
```

## 16. Limitations
See [LIMITATIONS.md](LIMITATIONS.md). Key points: synthetic data; censored demand (sold ≤ prepared); thresholds are assumptions; interval is approximate; single simulated site.

## 17. Future scope
See [FUTURE_SCOPE.md](FUTURE_SCOPE.md): real data & retraining, probabilistic forecasts, drift monitoring, weather API, menu-level forecasting, human-approved donation workflow.

## 18. Ethical considerations
- **Synthetic data:** results do not transfer automatically to real kitchens.
- **Uncertainty:** every prediction can be wrong; ranges are indicative.
- **Food safety:** surplus must pass safety checks before any redistribution.
- **Human oversight:** recommendations only — no automatic redistribution, no automatic contact with NGOs.
- **Privacy:** only aggregate counts are used; no personal data is stored.
- **Bias/generalisation:** models learn one simulated site's patterns; re-validate before use elsewhere (festivals, menu changes, new campuses).
- **No unsupported impact claims:** "Estimated Food Saved" is a *potential* figure, not a measured outcome.

