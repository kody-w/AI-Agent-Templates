---
name: building-permit-review-agent
description: Automate building permit review processes to enable faster service, lower operational costs, and higher citizen satisfaction. Use for State and Local Government permit lookups — list all or fetch one by name or PRM- reference.
---

# Building Permit Review Agent

Automate building permit review processes to enable faster service, lower operational costs, and higher citizen satisfaction.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python building-permit-review-agent.py "list"` (all permit records) or `python building-permit-review-agent.py "<name or PRM- id>"`.
- Import: `from building_permit_review_agent import query; query("list")`.

Returns permit records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
