---
name: branch-banking-advisory-agent
description: Automate branch banking and advisory workflows to streamline customer interactions, strengthen compliance, and improve financial guidance. Use for Financial Services case lookups — list all or fetch one by name or CS- reference.
---

# Branch Banking Advisory Agent

Automate branch banking and advisory workflows to streamline customer interactions, strengthen compliance, and improve financial guidance.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python branch-banking-advisory-agent.py "list"` (all case records) or `python branch-banking-advisory-agent.py "<name or CS- id>"`.
- Import: `from branch_banking_advisory_agent import query; query("list")`.

Returns case records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
