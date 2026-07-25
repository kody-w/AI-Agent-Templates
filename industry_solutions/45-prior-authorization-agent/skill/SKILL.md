---
name: prior-authorization-agent
description: Automate insurance approval workflows to accelerate authorization processes, improve documentation accuracy, and reduce care delays. Use for Healthcare, Financial Services record lookups — list all or fetch one by name or PT- reference.
---

# Prior Authorization Agent

Automate insurance approval workflows to accelerate authorization processes, improve documentation accuracy, and reduce care delays.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python prior-authorization-agent.py "list"` (all record records) or `python prior-authorization-agent.py "<name or PT- id>"`.
- Import: `from prior_authorization_agent import query; query("list")`.

Returns record records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
