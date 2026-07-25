---
name: purchase-order-management-agent
description: Automate purchase order management and vendor selection to enable faster and more cost-effective purchasing. Use for Cross-Industry order lookups — list all or fetch one by name or PO- reference.
---

# Purchase Order Management Agent

Automate purchase order management and vendor selection to enable faster and more cost-effective purchasing.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python purchase-order-management-agent.py "list"` (all order records) or `python purchase-order-management-agent.py "<name or PO- id>"`.
- Import: `from purchase_order_management_agent import query; query("list")`.

Returns order records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
