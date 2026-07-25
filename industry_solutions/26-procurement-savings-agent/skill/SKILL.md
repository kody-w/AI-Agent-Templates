---
name: procurement-savings-agent
description: Identify and optimize savings opportunities across vendors, contracts, and purchasing cycles to reduce costs and increase procurement efficiency. Use for Cross-Industry order lookups — list all or fetch one by name or PO- reference.
---

# Procurement Savings Agent

Identify and optimize savings opportunities across vendors, contracts, and purchasing cycles to reduce costs and increase procurement efficiency.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python procurement-savings-agent.py "list"` (all order records) or `python procurement-savings-agent.py "<name or PO- id>"`.
- Import: `from procurement_savings_agent import query; query("list")`.

Returns order records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
