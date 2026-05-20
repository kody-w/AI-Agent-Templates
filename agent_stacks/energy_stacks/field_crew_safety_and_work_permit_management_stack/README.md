# Field Crew Safety and Work Permit Management — Agent Stack

Eight focused agents that, together, digitises the end-to-end permit-to-work process to reduce unsafe working conditions, ensure regulatory compliance, and provide real-time crew safety visibility across the field estate.. Built for the **Energy Utilities** domain. Portable to the `rapp_ai` BasicAgent runtime and to Copilot Studio via the parallel solution bundle.

> No PII. Synthetic, domain-shaped outputs. Deterministic where it matters — per-key seeds make demos and code reviews reproducible.

---

## The 8 agents (no orchestrator)

| # | Agent | What it does |
|---|-------|--------------|
| 1 | `permit_request_capture_agent.py` | Captures permit-to-work request from a mobile form. |
| 2 | `risk_assessment_agent.py` | Drafts a Risk Assessment + Method Statement (RAMS) tailored to asset class and work. |
| 3 | `isolation_plan_validator_agent.py` | Validates the RAMS against the published asset isolation plan. |
| 4 | `permit_authorisation_workflow_agent.py` | Routes the permit through PIC -> AP -> Manager digital sign-off. |
| 5 | `live_isolation_confirmation_agent.py` | Confirms live breaker / disconnector state from the DMS. |
| 6 | `crew_acceptance_agent.py` | Captures on-site safety brief and per-crew acceptance signatures. |
| 7 | `permit_clearance_agent.py` | Closes permit: personnel count + tools accounted + area safe. |
| 8 | `safety_analytics_agent.py` | Aggregates permit-cycle KPIs (cycle time, on-time closure, near-miss). |

---

## Data flow

```
request_capture -> risk_assessment -> isolation_plan_validator -> auth_workflow
                          -> live_isolation_confirmation -> crew_acceptance
                          -> work execution (out of stack) -> permit_clearance
                          -> safety_analytics (rollup)
```

Each agent is independent. The LLM (or your code) composes them.

---

## Run locally

```bash
# Each agent has a self-test
python agents/permit_request_capture_agent.py
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
  -d '{"user_input": "Raise a permit-to-work request for substation SUB-12 transformer overhaul", "conversation_history": []}'
```
