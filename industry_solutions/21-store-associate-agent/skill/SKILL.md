---
name: store-associate-agent
description: Deliver real-time product intelligence and transaction support to deliver faster service and boost sales performance. Use for Retail record lookups — list all or fetch one by name or REC- reference.
---

# Store Associate Agent

Deliver real-time product intelligence and transaction support to deliver faster service and boost sales performance.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python store-associate-agent.py "list"` (all record records) or `python store-associate-agent.py "<name or REC- id>"`.
- Import: `from store_associate_agent import query; query("list")`.

Returns record records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
