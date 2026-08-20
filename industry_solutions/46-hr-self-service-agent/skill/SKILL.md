---
name: hr-self-service-agent
description: Provide self-service HR inquiry handling that transforms the process from a manual ticket-based system to intelligent, automated resolutions. Use for Cross-Industry case lookups — list all or fetch one by name or CS- reference.
---

# HR Self-Service Agent

Provide self-service HR inquiry handling that transforms the process from a manual ticket-based system to intelligent, automated resolutions.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python hr-self-service-agent.py "list"` (all case records) or `python hr-self-service-agent.py "<name or CS- id>"`.
- Import: `from hr_self_service_agent import query; query("list")`.

Returns case records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
