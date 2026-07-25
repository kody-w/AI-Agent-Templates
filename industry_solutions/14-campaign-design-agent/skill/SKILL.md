---
name: campaign-design-agent
description: Automate personalized campaign design and execution to boost engagement, accelerate revenue, and strengthen customer loyalty. Use for Retail record lookups — list all or fetch one by name or CX- reference.
---

# Campaign Design Agent

Automate personalized campaign design and execution to boost engagement, accelerate revenue, and strengthen customer loyalty.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python campaign-design-agent.py "list"` (all record records) or `python campaign-design-agent.py "<name or CX- id>"`.
- Import: `from campaign_design_agent import query; query("list")`.

Returns record records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
