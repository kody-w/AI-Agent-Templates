---
name: resource-utilization-agent
description: Provide intelligent resource analysis and recommendations to maximize billable utilization and reduce costs. Use for Professional Services, Consulting case lookups — list all or fetch one by name or CS- reference.
---

# Resource Utilization Agent

Provide intelligent resource analysis and recommendations to maximize billable utilization and reduce costs.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python resource-utilization-agent.py "list"` (all case records) or `python resource-utilization-agent.py "<name or CS- id>"`.
- Import: `from resource_utilization_agent import query; query("list")`.

Returns case records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
