---
name: predictive-maintenance-agent
description: Perform predictive maintenance analysis and scheduling orchestration to prevent unplanned downtime and protect production capacity. Use for Manufacturing work order lookups — list all or fetch one by name or WO- reference.
---

# Predictive Maintenance Agent

Perform predictive maintenance analysis and scheduling orchestration to prevent unplanned downtime and protect production capacity.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python predictive-maintenance-agent.py "list"` (all work order records) or `python predictive-maintenance-agent.py "<name or WO- id>"`.
- Import: `from predictive_maintenance_agent import query; query("list")`.

Returns work order records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
