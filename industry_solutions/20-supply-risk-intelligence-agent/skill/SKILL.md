---
name: supply-risk-intelligence-agent
description: Deliver real-time risk intelligence and planning to protect production continuity and reduce disruption exposure. Use for Manufacturing work order lookups — list all or fetch one by name or WO- reference.
---

# Supply Risk Intelligence Agent

Deliver real-time risk intelligence and planning to protect production continuity and reduce disruption exposure.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python supply-risk-intelligence-agent.py "list"` (all work order records) or `python supply-risk-intelligence-agent.py "<name or WO- id>"`.
- Import: `from supply_risk_intelligence_agent import query; query("list")`.

Returns work order records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
