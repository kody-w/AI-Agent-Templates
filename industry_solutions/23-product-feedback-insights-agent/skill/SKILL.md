---
name: product-feedback-insights-agent
description: Turn fragmented feedback into actionable insights that accelerate product improvements, prevent churn, and optimize engineering priorities. Use for Cross-Industry record lookups — list all or fetch one by name or CX- reference.
---

# Product Feedback Insights Agent

Turn fragmented feedback into actionable insights that accelerate product improvements, prevent churn, and optimize engineering priorities.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python product-feedback-insights-agent.py "list"` (all record records) or `python product-feedback-insights-agent.py "<name or CX- id>"`.
- Import: `from product_feedback_insights_agent import query; query("list")`.

Returns record records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
