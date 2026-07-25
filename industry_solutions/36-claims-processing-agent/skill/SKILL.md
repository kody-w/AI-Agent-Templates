---
name: claims-processing-agent
description: Automate claims processing workflows to deliver faster, consistent, and more compliant claim outcomes. Use for Financial Services claim lookups — list all or fetch one by name or CLM- reference.
---

# Claims Processing Agent

Automate claims processing workflows to deliver faster, consistent, and more compliant claim outcomes.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python claims-processing-agent.py "list"` (all claim records) or `python claims-processing-agent.py "<name or CLM- id>"`.
- Import: `from claims_processing_agent import query; query("list")`.

Returns claim records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
