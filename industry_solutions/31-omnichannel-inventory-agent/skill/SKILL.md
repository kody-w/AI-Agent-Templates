---
name: omnichannel-inventory-agent
description: Deliver real-time cross-channel inventory intelligence to prevent stockouts, reduce overstock, and maximize omnichannel retail performance. Use for Retail SKU lookups — list all or fetch one by name or SKU- reference.
---

# Omnichannel Inventory Agent

Deliver real-time cross-channel inventory intelligence to prevent stockouts, reduce overstock, and maximize omnichannel retail performance.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python omnichannel-inventory-agent.py "list"` (all SKU records) or `python omnichannel-inventory-agent.py "<name or SKU- id>"`.
- Import: `from omnichannel_inventory_agent import query; query("list")`.

Returns SKU records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
