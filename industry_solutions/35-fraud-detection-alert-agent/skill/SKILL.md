---
name: fraud-detection-alert-agent
description: Deploy AI-driven fraud monitoring and identification to accelerate investigations, enhance detection rates, and improve prevention. Use for Financial Services case lookups — list all or fetch one by name or FRD- reference.
---

# Fraud Detection & Alert Agent

Deploy AI-driven fraud monitoring and identification to accelerate investigations, enhance detection rates, and improve prevention.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python fraud-detection-alert-agent.py "list"` (all case records) or `python fraud-detection-alert-agent.py "<name or FRD- id>"`.
- Import: `from fraud_detection_alert_agent import query; query("list")`.

Returns case records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
