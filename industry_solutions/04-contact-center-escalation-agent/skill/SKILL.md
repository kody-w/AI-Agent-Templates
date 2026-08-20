---
name: contact-center-escalation-agent
description: Automate back-office contact center escalation workflows to deliver better service outcomes and retention rates. Use for Cross-Industry, Contact Center case lookups — list all or fetch one by name or CS- reference.
---

# Contact Center Escalation Agent

Automate back-office contact center escalation workflows to deliver better service outcomes and retention rates.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python contact-center-escalation-agent.py "list"` (all case records) or `python contact-center-escalation-agent.py "<name or CS- id>"`.
- Import: `from contact_center_escalation_agent import query; query("list")`.

Returns case records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
