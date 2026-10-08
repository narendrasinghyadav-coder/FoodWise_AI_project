# Testing

Run: `python -m pytest -q` (76 tests, ~16 s; last run: **76 passed**). Test models are trained quickly on a small simulated dataset in a temp directory; the UI smoke tests use the real trained artefacts (run `python -m src.pipeline` first, otherwise they are skipped).

| File | Covers |
|---|---|
| `tests/test_data.py` | generator reproducibility & realistic relationships, validation (missing columns, empty data, negatives, bad categories, injected issues), cleaning (duplicates, imputation, invalid rows, standardisation) |
| `tests/test_features.py` | engineered feature values, `meals_prepared` exclusion from demand model, weekend flag, zero denominators, unknown categories, leakage-free temporal split |
| `tests/test_business_logic.py` | surplus / waste %, shortage, **zero meals prepared**, zero demand, recommendation levels & wording, negative/missing values |
| `tests/test_prediction.py` | model loading, **missing / corrupted model file**, real predictions responding to inputs, over-preparation raises HIGH risk, batch prediction, **extremely high student count**, **missing input**, **negative values**, **unexpected categories**, input normalisation, metadata sanity, SQLite round-trip |
| `tests/test_app_smoke.py` | all 7 pages render without exceptions (Streamlit `AppTest`); the 3 prediction forms return real model output |

A test run also found and fixed a real bug during development (undefined helper on the Analytics page).

**Manual checks performed:** `python run.py` starts the server, `/_stcore/health` returns `ok` and the root page returns HTTP 200.
Visual review of the rendered UI in a browser is still recommended (screenshots are placeholders in the README).
