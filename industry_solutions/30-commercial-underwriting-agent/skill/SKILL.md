---
name: commercial-underwriting-agent
description: Automate commercial underwriting analysis to accelerate evaluations, improve pricing accuracy, and maintain full compliance. Use for Financial Services application lookups — list all or fetch one by name or APP- reference.
---

# Commercial Underwriting Agent

Automate commercial underwriting analysis to accelerate evaluations, improve pricing accuracy, and maintain full compliance.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python commercial-underwriting-agent.py "list"` (all application records) or `python commercial-underwriting-agent.py "<name or APP- id>"`.
- Import: `from commercial_underwriting_agent import query; query("list")`.

Returns application records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
