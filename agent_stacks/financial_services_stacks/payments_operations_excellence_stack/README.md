# Payments Operations Excellence — Agent Stack

Eight focused agents that, together, optimises end-to-end payments processing: reduces exceptions, improves STP rates, and ensures real-time compliance with scheme rules across CHAPS, Faster Payments, SEPA, and SWIFT rails.. Built for the **Financial Services** domain. Portable to the `rapp_ai` BasicAgent runtime and to Copilot Studio via the parallel solution bundle.

> No PII. Synthetic, domain-shaped outputs. Deterministic where it matters — per-key seeds make demos and code reviews reproducible.

---

## The 8 agents (no orchestrator)

| # | Agent | What it does |
|---|-------|--------------|
| 1 | `payment_ingestion_validator_agent.py` | Validates payment against scheme rules (CHAPS / FPS / SEPA / SWIFT). |
| 2 | `sanctions_screening_agent.py` | Screens parties against OFAC / HMT / EU lists. |
| 3 | `payment_exception_repair_agent.py` | Diagnoses payment-failure root cause + repair playbook. |
| 4 | `nostro_reconciliation_agent.py` | Reconciles internal payment-position to nostro statement. |
| 5 | `correspondent_banking_monitor_agent.py` | Monitors correspondent-bank limits + nostro funding. |
| 6 | `pre_release_fraud_scorer_agent.py` | Scores transaction-level fraud risk pre-release. |
| 7 | `payment_status_tracker_agent.py` | Returns lifecycle state of a payment by reference. |
| 8 | `payments_analytics_agent.py` | STP rate, volume, scheme-compliance KPIs by rail. |

---

## Data flow

```
ingestion_validator -> sanctions_screening -> pre_release_fraud_scorer -> release
                                ^                            
                                | (on fail) -> exception_repair
                                                              
settlement -> nostro_reconciliation -> correspondent_banking_monitor
                                                                    
payment_status_tracker (any time)  payments_analytics (rollup)
```

Each agent is independent. The LLM (or your code) composes them.

---

## Run locally

```bash
# Each agent has a self-test
python agents/payment_ingestion_validator_agent.py
```

```bash
# Pytest suite (no rapp_ai runtime needed — uses a BasicAgent stub)
pytest -xvs tests/test_agents.py
```

---

## Drop into rapp_ai

Copy any agent into `rapp_ai/agents/`. They each `from agents.basic_agent import BasicAgent`, so they register automatically when the Function App starts.

```bash
cp agents/*.py /path/to/rapp_ai/agents/
cd /path/to/rapp_ai && func start
```

Hit the endpoint and the model will compose the chain on its own:

```bash
curl -X POST http://localhost:7072/api/businessinsightbot_function \
  -H "Content-Type: application/json" \
  -d '{"user_input": "Show me today's STP rate by payment rail", "conversation_history": []}'
```

---

## 🚀 One-click Copilot Studio deploy

Want this in **Copilot Studio** instead of (or as well as) the local runtime?
[`copilot_studio_solution/`](copilot_studio_solution/) is a ready-to-import
Power Platform bundle — the **Payments Operations Excellence** solution as new-generation connected
agents, published by **Microsoft AI Business Applications Specialist Team
(AIBAST)**. Import `PaymentsOperationsMcpConnectors_1_0_0_1.zip` then `PaymentsOperationsMcpAgents_1_0_0_1.zip`, publish, attach the MCP connector, and
you have a working agent in your environment. Full steps in
[`copilot_studio_solution/README.md`](copilot_studio_solution/README.md).
