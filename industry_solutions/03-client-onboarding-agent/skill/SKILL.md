---
name: client-onboarding-agent
description: Orchestrate client onboarding journeys with unified workflows to accelerate revenue and mitigate compliance risk. Use for Cross-Industry, Financial Services case lookups — list all or fetch one by name or CS- reference.
---

# Client Onboarding Agent

Orchestrate client onboarding journeys with unified workflows to accelerate revenue and mitigate compliance risk.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python client-onboarding-agent.py "list"` (all case records) or `python client-onboarding-agent.py "<name or CS- id>"`.
- Import: `from client_onboarding_agent import query; query("list")`.

Returns case records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
