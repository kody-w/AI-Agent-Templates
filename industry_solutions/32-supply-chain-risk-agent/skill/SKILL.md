---
name: supply-chain-risk-agent
description: Detect and manage supply chain risks to defend against disruptions, protect revenue, and maintain operational continuity. Use for Retail, Manufacturing work order lookups — list all or fetch one by name or WO- reference.
---

# Supply Chain Risk Agent

Detect and manage supply chain risks to defend against disruptions, protect revenue, and maintain operational continuity.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python supply-chain-risk-agent.py "list"` (all work order records) or `python supply-chain-risk-agent.py "<name or WO- id>"`.
- Import: `from supply_chain_risk_agent import query; query("list")`.

Returns work order records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
