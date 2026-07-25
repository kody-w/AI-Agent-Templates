---
name: contract-review-agent
description: Automate contract review processes to enable faster, lower-risk, and more successful negotiations. Use for Professional Services, Consulting item lookups — list all or fetch one by name or REG- reference.
---

# Contract Review Agent

Automate contract review processes to enable faster, lower-risk, and more successful negotiations.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python contract-review-agent.py "list"` (all item records) or `python contract-review-agent.py "<name or REG- id>"`.
- Import: `from contract_review_agent import query; query("list")`.

Returns item records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
