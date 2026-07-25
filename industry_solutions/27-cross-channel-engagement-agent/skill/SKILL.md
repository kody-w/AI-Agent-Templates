---
name: cross-channel-engagement-agent
description: Deliver a single, unified view of cross-channel interactions for more strategic, streamlined support and stronger engagement. Use for Cross-Industry, Retail record lookups — list all or fetch one by name or CX- reference.
---

# Cross-Channel Engagement Agent

Deliver a single, unified view of cross-channel interactions for more strategic, streamlined support and stronger engagement.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python cross-channel-engagement-agent.py "list"` (all record records) or `python cross-channel-engagement-agent.py "<name or CX- id>"`.
- Import: `from cross_channel_engagement_agent import query; query("list")`.

Returns record records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
