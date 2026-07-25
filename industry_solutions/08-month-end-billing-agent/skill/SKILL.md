---
name: month-end-billing-agent
description: Automate month-end billing cycles to accelerate invoicing, reduce risk, and ensure audit-ready compliance. Use for Professional Services, Consulting invoice lookups — list all or fetch one by name or INV- reference.
---

# Month-End Billing Agent

Automate month-end billing cycles to accelerate invoicing, reduce risk, and ensure audit-ready compliance.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python month-end-billing-agent.py "list"` (all invoice records) or `python month-end-billing-agent.py "<name or INV- id>"`.
- Import: `from month_end_billing_agent import query; query("list")`.

Returns invoice records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
