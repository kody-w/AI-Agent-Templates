---
name: mortgage-origination-agent
description: Streamline mortgage origination with intelligent automation, enabling faster, more accurate loan decisions. Use for Financial Services application lookups — list all or fetch one by name or APP- reference.
---

# Mortgage Origination Agent

Streamline mortgage origination with intelligent automation, enabling faster, more accurate loan decisions.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python mortgage-origination-agent.py "list"` (all application records) or `python mortgage-origination-agent.py "<name or APP- id>"`.
- Import: `from mortgage_origination_agent import query; query("list")`.

Returns application records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
