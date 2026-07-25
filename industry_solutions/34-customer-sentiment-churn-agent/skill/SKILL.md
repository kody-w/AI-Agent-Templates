---
name: customer-sentiment-churn-agent
description: Deliver AI-powered sentiment intelligence that detects churn risk early and enables proactive retention strategies. Use for Financial Services case lookups — list all or fetch one by name or CS- reference.
---

# Customer Sentiment & Churn Agent

Deliver AI-powered sentiment intelligence that detects churn risk early and enables proactive retention strategies.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python customer-sentiment-churn-agent.py "list"` (all case records) or `python customer-sentiment-churn-agent.py "<name or CS- id>"`.
- Import: `from customer_sentiment_churn_agent import query; query("list")`.

Returns case records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
