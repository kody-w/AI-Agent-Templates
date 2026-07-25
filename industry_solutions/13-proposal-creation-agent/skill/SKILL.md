---
name: proposal-creation-agent
description: Automate proposal creation to accelerate deal cycles, improve win rates, and deliver consistent, high-quality responses. Use for Cross-Industry opportunity lookups — list all or fetch one by name or OPP- reference.
---

# Proposal Creation Agent

Automate proposal creation to accelerate deal cycles, improve win rates, and deliver consistent, high-quality responses.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python proposal-creation-agent.py "list"` (all opportunity records) or `python proposal-creation-agent.py "<name or OPP- id>"`.
- Import: `from proposal_creation_agent import query; query("list")`.

Returns opportunity records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
