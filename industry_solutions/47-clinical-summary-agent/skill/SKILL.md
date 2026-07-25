---
name: clinical-summary-agent
description: Transform complex clinical histories into clear, actionable summaries for faster decision-making, better coordination, and safer care. Use for Healthcare record lookups — list all or fetch one by name or PT- reference.
---

# Clinical Summary Agent

Transform complex clinical histories into clear, actionable summaries for faster decision-making, better coordination, and safer care.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python clinical-summary-agent.py "list"` (all record records) or `python clinical-summary-agent.py "<name or PT- id>"`.
- Import: `from clinical_summary_agent import query; query("list")`.

Returns record records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
