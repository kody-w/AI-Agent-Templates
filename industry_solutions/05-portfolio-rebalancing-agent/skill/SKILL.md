---
name: portfolio-rebalancing-agent
description: Provide intelligent, automated portfolio rebalancing that streamlines manual reviews and improves wealth management outcomes. Use for Capital Markets case lookups — list all or fetch one by name or CS- reference.
---

# Portfolio Rebalancing Agent

Provide intelligent, automated portfolio rebalancing that streamlines manual reviews and improves wealth management outcomes.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python portfolio-rebalancing-agent.py "list"` (all case records) or `python portfolio-rebalancing-agent.py "<name or CS- id>"`.
- Import: `from portfolio_rebalancing_agent import query; query("list")`.

Returns case records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
