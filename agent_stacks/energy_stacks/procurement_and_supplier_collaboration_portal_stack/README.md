# Procurement and Supplier Collaboration Portal — Agent Stack

Eight focused agents that, together, accelerates procurement cycles and improves supplier performance via AI-assisted bid evaluation, automated approval workflows, and a digital supplier collaboration portal -- covering demand signal through three-way invoice match.. Built for the **Energy Utilities** domain. Portable to the `rapp_ai` BasicAgent runtime and to Copilot Studio via the parallel solution bundle.

> No PII. Synthetic, domain-shaped outputs. Deterministic where it matters — per-key seeds make demos and code reviews reproducible.

---

## The 8 agents (no orchestrator)

| # | Agent | What it does |
|---|-------|--------------|
| 1 | `demand_signal_requisition_agent.py` | Pulls demand from maintenance + capital plans. |
| 2 | `procurement_strategy_agent.py` | Direct award / mini-comp / open tender decision. |
| 3 | `rfq_builder_agent.py` | Builds RFQ + shortlists eligible suppliers. |
| 4 | `supplier_bid_intake_agent.py` | Receives bids + clarification Q&A. |
| 5 | `bid_evaluation_agent.py` | Scores bids across weighted criteria. |
| 6 | `po_approval_issuance_agent.py` | Drafts PO + routes for approval (pending_review). |
| 7 | `delivery_tracking_agent.py` | Tracks ASN + flags deviation vs commitment. |
| 8 | `three_way_match_agent.py` | PO <-> GR <-> Invoice reconciliation. |

---

## Data flow

```
demand_signal -> procurement_strategy -> rfq_builder -> supplier_bid_intake
                                              -> bid_evaluation -> po_approval_issuance
                                              -> delivery_tracking -> three_way_match
```

Each agent is independent. The LLM (or your code) composes them.

---

## Run locally

```bash
# Each agent has a self-test
python agents/demand_signal_requisition_agent.py
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
  -d '{"user_input": "Recommend a procurement route for this 2 MUSD framework order", "conversation_history": []}'
```
