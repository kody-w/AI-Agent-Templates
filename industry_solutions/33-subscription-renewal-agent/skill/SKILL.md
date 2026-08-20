---
name: subscription-renewal-agent
description: Streamline subscription renewal management and expansion planning, turning risk into growth opportunities while increasing win probability. Use for Software Tech opportunity lookups — list all or fetch one by name or OPP- reference.
---

# Subscription Renewal Agent

Streamline subscription renewal management and expansion planning, turning risk into growth opportunities while increasing win probability.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python subscription-renewal-agent.py "list"` (all opportunity records) or `python subscription-renewal-agent.py "<name or OPP- id>"`.
- Import: `from subscription_renewal_agent import query; query("list")`.

Returns opportunity records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
