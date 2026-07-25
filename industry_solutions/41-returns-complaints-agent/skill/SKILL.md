---
name: returns-complaints-agent
description: Automate return decisions and complaint handling to speed resolution, reduce fraud, and protect customer loyalty. Use for Retail, Consumable Products Industry case lookups — list all or fetch one by name or CS- reference.
---

# Returns & Complaints Agent

Automate return decisions and complaint handling to speed resolution, reduce fraud, and protect customer loyalty.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python returns-complaints-agent.py "list"` (all case records) or `python returns-complaints-agent.py "<name or CS- id>"`.
- Import: `from returns_complaints_agent import query; query("list")`.

Returns case records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
