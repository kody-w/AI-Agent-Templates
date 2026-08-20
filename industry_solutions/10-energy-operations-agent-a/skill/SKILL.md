---
name: energy-operations-agent-a
description: Deliver real-time insights, automate critical workflows, and enable guided decision making—boosting efficiency while reducing operational and compliance risk for energy organizations. Use for Energy and Utilities site lookups — list all or fetch one by name or SITE- reference.
---

# Energy Operations Agent (a)

Deliver real-time insights, automate critical workflows, and enable guided decision making—boosting efficiency while reducing operational and compliance risk for energy organizations.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python energy-operations-agent-a.py "list"` (all site records) or `python energy-operations-agent-a.py "<name or SITE- id>"`.
- Import: `from energy_operations_agent_a import query; query("list")`.

Returns site records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
