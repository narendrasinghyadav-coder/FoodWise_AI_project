# Limitations

1. **Synthetic data.** Every record is simulated with assumed parameters. Metrics (R² 0.953, macro-F1 0.747) demonstrate the pipeline, not real-world performance. No real-world impact is claimed.
2. **Simulator–model circularity.** The simulator's rules (e.g. participation rates) are what the model learns; real data has unknown, messier drivers (menu, exams, nearby events, price).
3. **Censored demand.** `meals_sold = min(demand, prepared)`; on stock-out days true demand is under-recorded, biasing forecasts low. Real deployments should log stock-outs.
4. **Assumed risk thresholds.** LOW/MEDIUM/HIGH cut-offs (8 % / 18 %) are assumptions in `src/config.py`.
5. **Weak MEDIUM class.** F1 0.58 — the middle band is inherently ambiguous.
6. **Approximate uncertainty.** The 80 % range comes from test residuals and is only indicative.
7. **Fixed `kg_per_meal`.** Waste/saved kg uses a single average (0.38 kg/meal); real portions vary by menu.
8. **Single site, three meals, no menu detail.** No item-level forecasts, no per-dish waste.
9. **User-supplied lags.** The forms need previous-day/week demand entered manually; there is no live data feed.
10. **No drift monitoring or retraining automation.**
11. **Not a food-safety tool.** The app says nothing about whether surplus food is safe to redistribute.
12. **Prototype security.** No authentication; SQLite is single-user.
