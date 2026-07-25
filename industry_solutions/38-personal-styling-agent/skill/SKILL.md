---
name: personal-styling-agent
description: Deliver intelligent personal styling to strengthen customer experience, increase revenue, and elevate associate efficiency at scale. Use for Retail record lookups — list all or fetch one by name or CX- reference.
---

# Personal Styling Agent

Deliver intelligent personal styling to strengthen customer experience, increase revenue, and elevate associate efficiency at scale.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python personal-styling-agent.py "list"` (all record records) or `python personal-styling-agent.py "<name or CX- id>"`.
- Import: `from personal_styling_agent import query; query("list")`.

Returns record records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
