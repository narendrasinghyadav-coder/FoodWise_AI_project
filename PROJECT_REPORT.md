# Project Report — FoodWise AI

## 1. Abstract
FoodWise AI is a prototype decision-support system that forecasts canteen meal demand, classifies food-waste risk (LOW/MEDIUM/HIGH), estimates surplus and recommends preparation quantities, supporting SDG 12 (primary) and SDG 2 (secondary). It is built with Python, scikit-learn, Plotly, Streamlit and SQLite and evaluated on a **synthetic** dataset.

## 2. Problem statement
Over-preparation of meals causes food waste and financial loss; surplus is rarely identified early enough to be considered for safe redistribution.

## 3. Objectives
Predict demand, predict waste risk, estimate surplus, recommend preparation, raise advisory redistribution alerts, provide analytics, and expose honest model metrics.

## 4. Methodology
1. **Data** — simulator (`generate_data.py`) with documented relationships; injected missing values/duplicates in the raw file. 3,273 raw → 3,267 clean rows.
2. **Validation & cleaning** — schema/type/range/category/consistency checks; duplicate removal; imputation; recomputation of derived columns; strict re-validation.
3. **EDA** — `docs/EDA_SUMMARY.md`: holidays ≈ −55 % demand and far higher waste %; events ≈ +12 % demand; LOW 57 / MEDIUM 24 / HIGH 19 %.
4. **Features** — calendar, cyclical month, lag aggregates, preparation ratios; `meals_prepared` kept out of the demand model.
5. **Modelling** — 3 regressors and 3 classifiers; time-series CV for selection; time-based hold-out for reporting; naive baselines for context.
6. **Serving** — `PredictionService` (validation → feature engineering → models → business rules) used by all UI pages; predictions logged in SQLite.

## 5. Results (actual, from the pipeline run)
| Task | Selected | Key test metrics |
|---|---|---|
| Demand | Gradient Boosting | MAE 53.83, RMSE 73.13, R² 0.953 (baseline prev-week: RMSE 228.90, R² 0.542) |
| Waste risk | Gradient Boosting | Acc 0.791, macro-P 0.755, macro-R 0.740, macro-F1 0.747 (majority baseline F1 0.234) |

All candidate comparisons are in `models/metadata.json`, the Model Performance page and the README. Selection used CV; on the test set Random Forest had marginally lower demand RMSE (71.67) and Logistic Regression higher risk F1 (0.768) — differences are small.

## 6. Business logic
`surplus = prepared − predicted demand` (never negative for waste %), `waste % = surplus / prepared × 100`, recommended preparation = ⌈demand × 1.05⌉, estimated waste kg = surplus × 0.38. Recommendation levels: shortage (< −5 %), appropriate (< 8 %), reduce (8–18 %), potential surplus (≥ 18 %) with a redistribution *consideration* message. No automated action.

## 7. System design
`src/` (data, features, models, evaluation, prediction) is independent of the UI; `app/` holds Streamlit pages/components; `database/db.py` manages SQLite (`historical_meals`, `predictions`, `prediction_logs`). Single command: `python run.py`.

## 8. Testing
76 pytest tests incl. edge cases and page-render smoke tests — see [TESTING.md](TESTING.md).

## 9. Ethics
Synthetic-data caveats, uncertainty, food safety, human oversight, no automatic redistribution, no personal data, bias/generalisation — see README §19.

## 10. Conclusion
The project demonstrates a complete, reproducible ML workflow and a usable decision-support UI. Its numbers say nothing about real kitchens until it is validated with real data (see [LIMITATIONS.md](LIMITATIONS.md), [FUTURE_SCOPE.md](FUTURE_SCOPE.md)).
