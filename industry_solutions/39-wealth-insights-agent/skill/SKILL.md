---
name: wealth-insights-agent
description: Deliver AI-powered portfolio intelligence to uncover hidden asset opportunities, strengthen client relationships, and drive advisory growth at scale. Use for Financial Services case lookups — list all or fetch one by name or CS- reference.
---

# Wealth Insights Agent

Deliver AI-powered portfolio intelligence to uncover hidden asset opportunities, strengthen client relationships, and drive advisory growth at scale.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python wealth-insights-agent.py "list"` (all case records) or `python wealth-insights-agent.py "<name or CS- id>"`.
- Import: `from wealth_insights_agent import query; query("list")`.

Returns case records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
