---
name: abandoned-cart-recovery-agent
description: Automate abandoned cart analysis and recovery campaigns to convert lost sales, protect margins, and improve customer engagement. Use for Cross-Industry, Software Tech record lookups — list all or fetch one by name or CX- reference.
---

# Abandoned Cart Recovery Agent

Automate abandoned cart analysis and recovery campaigns to convert lost sales, protect margins, and improve customer engagement.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python abandoned-cart-recovery-agent.py "list"` (all record records) or `python abandoned-cart-recovery-agent.py "<name or CX- id>"`.
- Import: `from abandoned_cart_recovery_agent import query; query("list")`.

Returns record records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
