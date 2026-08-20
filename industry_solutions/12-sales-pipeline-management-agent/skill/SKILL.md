---
name: sales-pipeline-management-agent
description: Automate sales pipeline management to keep deals moving, increase forecast confidence, and improve team productivity. Use for Cross-Industry opportunity lookups — list all or fetch one by name or OPP- reference.
---

# Sales Pipeline Management Agent

Automate sales pipeline management to keep deals moving, increase forecast confidence, and improve team productivity.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python sales-pipeline-management-agent.py "list"` (all opportunity records) or `python sales-pipeline-management-agent.py "<name or OPP- id>"`.
- Import: `from sales_pipeline_management_agent import query; query("list")`.

Returns opportunity records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
