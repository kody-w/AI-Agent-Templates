---
name: utility-leak-detection-billing-agent
description: Automate leak detection and billing processes to improve customer satisfaction, ensure policy compliance, and protect municipal revenue. Use for Energy and Utilities, State and Local Government invoice lookups — list all or fetch one by name or INV- reference.
---

# Utility Leak Detection & Billing Agent

Automate leak detection and billing processes to improve customer satisfaction, ensure policy compliance, and protect municipal revenue.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python utility-leak-detection-billing-agent.py "list"` (all invoice records) or `python utility-leak-detection-billing-agent.py "<name or INV- id>"`.
- Import: `from utility_leak_detection_billing_agent import query; query("list")`.

Returns invoice records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
