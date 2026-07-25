---
name: inventory-optimization-agent
description: Intelligently optimize inventory portfolios to improve cash flow and warehouse efficiency while reducing waste. Use for Manufacturing SKU lookups — list all or fetch one by name or SKU- reference.
---

# Inventory Optimization Agent

Intelligently optimize inventory portfolios to improve cash flow and warehouse efficiency while reducing waste.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python inventory-optimization-agent.py "list"` (all SKU records) or `python inventory-optimization-agent.py "<name or SKU- id>"`.
- Import: `from inventory_optimization_agent import query; query("list")`.

Returns SKU records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
