---
name: client-health-score-agent
description: Automate client portfolio health monitoring and planning to improve client relationships, protect revenue, and optimize financial performance. Use for Professional Services, Consulting case lookups — list all or fetch one by name or CS- reference.
---

# Client Health Score Agent

Automate client portfolio health monitoring and planning to improve client relationships, protect revenue, and optimize financial performance.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python client-health-score-agent.py "list"` (all case records) or `python client-health-score-agent.py "<name or CS- id>"`.
- Import: `from client_health_score_agent import query; query("list")`.

Returns case records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
