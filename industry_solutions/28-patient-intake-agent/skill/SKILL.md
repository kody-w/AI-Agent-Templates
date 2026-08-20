---
name: patient-intake-agent
description: Automate patient intake workflows to streamline operations, protect revenue from avoidable losses, and deliver a smoother patient experience. Use for Healthcare record lookups — list all or fetch one by name or PT- reference.
---

# Patient Intake Agent

Automate patient intake workflows to streamline operations, protect revenue from avoidable losses, and deliver a smoother patient experience.

Portable — no RAPP/framework dependency; synthetic demo data (no PII).

## Use it
- CLI: `python patient-intake-agent.py "list"` (all record records) or `python patient-intake-agent.py "<name or PT- id>"`.
- Import: `from patient_intake_agent import query; query("list")`.

Returns record records (reference · subject · status · owner · metric). The
matching Copilot Studio solution and RAPP `agent.py` carry the identical data
and contract — see this folder's parent `README.md` for all three install paths.
