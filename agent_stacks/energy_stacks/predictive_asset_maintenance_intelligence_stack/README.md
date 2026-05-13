# Predictive Asset Maintenance Intelligence — Agent Stack

Eight focused agents that, together, extend the operational life of critical grid infrastructure and reduce unplanned outages. Built for the **Energy Utilities** domain. Portable to the `rapp_ai` BasicAgent runtime and to Copilot Studio via the parallel solution bundle.

> No PII. Synthetic, domain-shaped outputs. Deterministic where it matters (per-asset telemetry is seeded so demos and code reviews are reproducible).

---

## The 8 agents (no orchestrator)

| # | Agent | What it does |
|---|-------|--------------|
| 1 | `asset_sensor_aggregator_agent.py` | Pulls + normalizes IoT/SCADA telemetry across transformers, switchgear, cables, overhead lines. |
| 2 | `asset_health_scorer_agent.py` | Anomaly score, health score, condition band, Remaining Useful Life (RUL). |
| 3 | `failure_probability_ranker_agent.py` | Ranks fleet by failure probability across 30 / 90 / 180-day horizons. Hazard-survival model — `p(180) >= p(90) >= p(30)` always. |
| 4 | `maintenance_work_order_agent.py` | Drafts D365 Field Service work orders for assets above threshold. `pending_review` by design — dispatcher confirms. |
| 5 | `parts_planner_agent.py` | Consolidates parts demand, flags long-lead items, emits SAP MM / D365 Supply Chain procurement triggers. |
| 6 | `field_execution_capture_agent.py` | Captures field-execution outcomes from the Power Apps mobile form. |
| 7 | `asset_register_writeback_agent.py` | Stages updates to the Asset Management System + ERP fixed-asset register. |
| 8 | `lifecycle_capex_planner_agent.py` | Multi-year capex replacement pipeline with benefit/cost ratio. |

---

## Data flow

```
sensors ──> [1 aggregator] ──> [2 scorer] ──> [3 ranker] ──┬──> [4 WO] ──> [5 parts]
                                                            │       │
                                                            │       └─> [6 capture] ──> [7 register write-back]
                                                            │
                                                            └─> [8 capex planner]
```

Each agent is independent. The LLM (or your code) composes them.

---

## Run locally

```bash
# Each agent has a self-test
python agents/asset_sensor_aggregator_agent.py
python agents/lifecycle_capex_planner_agent.py
```

```bash
# Full pytest suite (no rapp_ai runtime needed — uses a BasicAgent stub)
pytest -xvs tests/test_agents.py
```

Expected: **11 passed**.

---

## Drop into rapp_ai

Copy any agent into `rapp_ai/agents/`. They each `from agents.basic_agent import BasicAgent`, so they'll register automatically when the function app starts.

```bash
cp agents/*.py /path/to/rapp_ai/agents/
cd /path/to/rapp_ai && func start
```

Then hit the endpoint:

```bash
curl -X POST http://localhost:7072/api/businessinsightbot_function \
  -H "Content-Type: application/json" \
  -d '{"user_input": "Show me the highest-risk grid assets for the next 90 days", "conversation_history": []}'
```

The model will compose: aggregator → scorer → ranker → return.
