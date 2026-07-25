---
name: care-gap-closure-agent
description: Automate quality gap analysis and targeted outreach to improve HEDIS performance, campaign ROI, and care gap closure efficiency. Use for Healthcare record lookups — list all or fetch one by name or PT- reference.
---

# Care Gap Closure Agent

Automate quality gap analysis and targeted outreach to improve HEDIS performance, campaign ROI, and care gap closure efficiency.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python care-gap-closure-agent.py "list"` (all record records) or `python care-gap-closure-agent.py "<name or PT- id>"`.
- Import: `from care_gap_closure_agent import query; query("list")`.

Returns record records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
