---
name: expansion-opportunity-agent
description: Identify and prioritize expansion opportunities to drive revenue growth and strengthen customer relationships. Use for Cross-Industry opportunity lookups — list all or fetch one by name or OPP- reference.
---

# Expansion Opportunity Agent

Identify and prioritize expansion opportunities to drive revenue growth and strengthen customer relationships.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python expansion-opportunity-agent.py "list"` (all opportunity records) or `python expansion-opportunity-agent.py "<name or OPP- id>"`.
- Import: `from expansion_opportunity_agent import query; query("list")`.

Returns opportunity records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
