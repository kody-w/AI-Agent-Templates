---
name: regulatory-compliance-agent
description: Automate compliance monitoring and regulatory reporting to achieve proactive risk management with real-time surveillance. Use for Financial Services item lookups — list all or fetch one by name or REG- reference.
---

# Regulatory Compliance Agent

Automate compliance monitoring and regulatory reporting to achieve proactive risk management with real-time surveillance.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python regulatory-compliance-agent.py "list"` (all item records) or `python regulatory-compliance-agent.py "<name or REG- id>"`.
- Import: `from regulatory_compliance_agent import query; query("list")`.

Returns item records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
