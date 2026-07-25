---
name: order-status-delay-agent
description: Automate proactive order updates, delay management, and customer communications to protect relationships and revenue. Use for Manufacturing order lookups — list all or fetch one by name or PO- reference.
---

# Order Status & Delay Agent

Automate proactive order updates, delay management, and customer communications to protect relationships and revenue.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python order-status-delay-agent.py "list"` (all order records) or `python order-status-delay-agent.py "<name or PO- id>"`.
- Import: `from order_status_delay_agent import query; query("list")`.

Returns order records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
