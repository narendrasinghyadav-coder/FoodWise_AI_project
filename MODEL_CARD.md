# Model Card — FoodWise AI

> Trained and evaluated on **synthetic (simulated)** data only. Metrics reflect the simulator, not real kitchens.

## Model 1 — Demand forecasting
- **Task:** regression, target `meals_sold`
- **Candidates:** Linear Regression, Random Forest (300 trees, min leaf 3), Gradient Boosting (300 trees, lr 0.05, depth 3, subsample 0.8)
- **Selected:** Gradient Boosting (lowest mean 5-fold TimeSeriesSplit CV RMSE: 77.52 vs RF 78.85 vs LR 102.06)
- **Features:** weekday, meal type, weather, temperature, holiday, event, weekend, student count, previous-day/week demand, cyclical month, `demand_ratio`, `avg_prev_demand`. `meals_prepared` excluded on purpose.
- **Test results (654 rows, 2024-05-28 → 2024-12-31):** MAE 53.83 · RMSE 73.13 · R² 0.953 · WMAPE 5.6 %
- **Baselines:** previous-week demand → RMSE 228.90, R² 0.542; mean(prev day, prev week) → RMSE 159.44, R² 0.778
- **Uncertainty:** 80 % range = prediction + [p10, p90] of test residuals (−98.1, +73.3 meals); indicative, slightly asymmetric (model tends to under-predict).
- **Most important features (permutation):** `avg_prev_demand`, `student_count`, `previous_week_demand`, `meal_type`.

## Model 2 — Waste-risk classification
- **Task:** 3-class classification (LOW / MEDIUM / HIGH), derived from `waste_percentage` thresholds 8 % / 18 %
- **Candidates:** Logistic Regression (balanced), Random Forest (balanced), Gradient Boosting
- **Selected:** Gradient Boosting (highest CV macro-F1 0.747 vs LR 0.737 vs RF 0.727)
- **Features:** demand features + `meals_prepared`, `prepared_per_student`, `prep_vs_prev_week`, `prep_vs_prev_day`, `prep_vs_avg_prev`
- **Test results:** accuracy 0.791 · macro precision 0.755 · macro recall 0.740 · macro F1 0.747
- **Per-class F1:** LOW 0.892 · MEDIUM 0.579 · HIGH 0.770
- **Confusion matrix** (rows actual LOW/MED/HIGH): `[[322,32,0],[44,93,24],[2,35,102]]`
- **Baseline:** majority class → accuracy 0.541, macro-F1 0.234
- **Most important feature:** `prepared_per_student`.

## Evaluation protocol
Time-based split (no leakage), `TimeSeriesSplit` CV on the training period for selection, test set used once for reporting. Seed 42. Logistic/Linear models use standard scaling; tree models do not.

## Intended use
Educational / portfolio decision-support demonstration; advisory recommendations for a human planner.

## Out-of-scope / not intended
Automatic food-redistribution decisions, contacting organisations, food-safety judgements, deployment on real data without retraining and validation.

## Caveats
- Synthetic data; sold meals are capped by prepared meals (censored demand).
- Top candidates differ little; on the test set Random Forest had slightly lower demand RMSE (71.67) and Logistic Regression a higher risk macro-F1 (0.768) than the CV-selected models — selection is deliberately CV-based.
- MEDIUM risk is the hardest class.
- Inputs far outside the training range trigger a warning; extrapolation is unreliable for tree models.
- Possible bias: one simulated site, three meal types, fixed weather/holiday patterns.

## Reproduce
`python -m src.pipeline` (metrics are written to `models/metadata.json`).
