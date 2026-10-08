# Data Dictionary

> **The dataset is SYNTHETIC (simulated)** — produced by `src/data/generate_data.py` (seed 42). It is not real canteen data. File: `data/raw/synthetic_meals_raw.csv` (raw, with injected quality issues) → `data/processed/meals_clean.csv` (cleaned). One row per `date × meal_type`.

| Column | Type | Description / simulation rule |
|---|---|---|
| `date` | date | Service date (2022-01-08 → 2024-12-31; first week dropped because lags need history) |
| `day_of_week` | category | Monday … Sunday (derived from `date`) |
| `meal_type` | category | Breakfast, Lunch, Dinner |
| `temperature` | float (°C) | Seasonal sinusoid + noise; lower on rainy/cloudy days |
| `weather` | category | Sunny, Cloudy, Rainy (rain more likely in one season) |
| `is_holiday` | 0/1 | Public holiday, random holiday, or semester break (Dec 24–Jan 2, Jun 1–14) |
| `is_event` | 0/1 | Campus event (~5 % of non-holiday days); raises lunch/dinner demand most |
| `student_count` | int | Students on campus that day (aggregate headcount); lower on weekends, holidays, breaks |
| `previous_day_demand` | int | `meals_sold` of the same meal type the day before |
| `previous_week_demand` | int | `meals_sold` of the same meal type 7 days before |
| `meals_prepared` | int | Planner output: `(0.6·prev_week + 0.4·prev_day) × margin(≈N(1.12, 0.10))`, rounded to 5; only sometimes adjusted for holiday/event |
| `meals_sold` | int | **Target 1.** `min(true demand, meals_prepared)` — note censoring on stock-outs |
| `food_waste_kg` | float | `surplus_meals × kg/meal` (≈0.38 kg, noise) |
| `surplus_meals` | int | `meals_prepared − meals_sold` |
| `waste_percentage` | float | `surplus_meals / meals_prepared × 100` |
| `waste_risk` | category | **Target 2.** LOW `< 8 %`, MEDIUM `8–18 %`, HIGH `≥ 18 %` (thresholds in `src/config.py`) |

**True demand** = `student_count × participation rate (Breakfast .42, Lunch .68, Dinner .62) × modifiers (weekend, rain +4 %, lunch heat, cold breakfast/dinner, holiday −15 %, event +3/15/20 %) × lognormal noise (σ 0.05)`.

**Injected raw-data issues** (to exercise the pipeline): 12 missing `temperature`, 5 missing `weather`, 6 exact duplicate rows.

**Derived model features:** see `src/features/engineering.py` (`is_weekend`, `month_sin/cos`, `avg_prev_demand`, `demand_ratio`, `prepared_per_student`, `prep_vs_prev_week`, `prep_vs_prev_day`, `prep_vs_avg_prev`).

**Database tables** (`database/foodwise.db`): `historical_meals` (flag `is_synthetic=1`), `predictions` (test-period model outputs), `prediction_logs` (UI prediction inputs/outputs).
