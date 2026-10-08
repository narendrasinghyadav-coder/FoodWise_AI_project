# Future Scope

**Data & validation**
- Pilot with real canteen logs (prepared, sold, leftover, stock-outs); retrain and re-validate; compare against the planner's actual baseline.
- Record stock-outs to model uncensored demand.

**Modelling**
- Quantile / probabilistic forecasting (e.g. quantile gradient boosting) for proper prediction intervals.
- Hyper-parameter search, calibration of risk probabilities, cost-sensitive thresholds (cost of shortage vs waste).
- Menu-item level forecasting; exam-calendar and local-event features; weather-forecast API.
- Drift monitoring and scheduled retraining; model registry.

**Product**
- Live ingestion of previous-day/week demand, role-based access, multi-site support, PostgreSQL.
- FastAPI service if other systems need to consume predictions.
- **Human-approved** donation workflow: notification drafts, food-safety checklists, audit trail — still no automatic redistribution without an accountable person.
- Impact tracking (measured waste before/after) so any sustainability claim is evidence-based.
