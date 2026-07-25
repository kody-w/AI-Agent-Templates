---
name: account-research-agent
description: Automate account research and strategy planning to help sellers prepare faster, win more, and elevate deal quality. Use for Cross-Industry opportunity lookups — list all or fetch one by name or OPP- reference.
---

# Account Research Agent

Automate account research and strategy planning to help sellers prepare faster, win more, and elevate deal quality.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python account-research-agent.py "list"` (all opportunity records) or `python account-research-agent.py "<name or OPP- id>"`.
- Import: `from account_research_agent import query; query("list")`.

Returns opportunity records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
