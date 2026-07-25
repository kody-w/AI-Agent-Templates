---
name: product-line-optimization-agent
description: Provide intelligent production capacity analysis and optimization planning to boost throughput and efficiency while maintaining quality. Use for Manufacturing record lookups — list all or fetch one by name or REC- reference.
---

# Product Line Optimization Agent

Provide intelligent production capacity analysis and optimization planning to boost throughput and efficiency while maintaining quality.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python product-line-optimization-agent.py "list"` (all record records) or `python product-line-optimization-agent.py "<name or REC- id>"`.
- Import: `from product_line_optimization_agent import query; query("list")`.

Returns record records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
