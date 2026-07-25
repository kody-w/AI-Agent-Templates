---
name: loyalty-insights-agent
description: Deliver AI-driven loyalty insights and planning to reduce points liability, improve engagement results, and boost member retention. Use for Cross-Industry record lookups — list all or fetch one by name or CX- reference.
---

# Loyalty Insights Agent

Deliver AI-driven loyalty insights and planning to reduce points liability, improve engagement results, and boost member retention.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python loyalty-insights-agent.py "list"` (all record records) or `python loyalty-insights-agent.py "<name or CX- id>"`.
- Import: `from loyalty_insights_agent import query; query("list")`.

Returns record records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
