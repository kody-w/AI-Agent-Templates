# Omnichannel Inventory Agent

Deliver real-time cross-channel inventory intelligence to prevent stockouts, reduce overstock, and maximize omnichannel retail performance.

**Industry:** Retail · **Personas:** Inventory Planners; Store Managers; Category Managers · **Featured tools:** Dynamics 365 Commerce, Microsoft Teams
**Publisher:** Microsoft AI Business Applications Specialist Team (AIBAST). Synthetic demo data — no PII.

Install this solution **three ways**:

## 1. One-click Copilot Studio (manual import)
No code, no hosting — new-generation connected agents with embedded data.
1. **Copilot Studio → Solutions → Import solution** → `copilot_studio_solution/OmnichannelInventoryAgentMcpConnectors_1_0_0_1.zip` → Import.
2. Repeat for `copilot_studio_solution/OmnichannelInventoryAgentMcpAgents_1_0_0_1.zip`.
3. Open **OmnichannelInventoryAgent** and **Publish**.
4. **Tools → Add a tool → Model Context Protocol** → the `Omnichannel Inventory Agent` connector → no-auth connection → Add → Publish.
See `copilot_studio_solution/IMPORT.md`.

## 2. RAPP brainstem (agent.py)
Drop [`agent.py`](agent.py) into your local RAPP brainstem's `agents/` folder
(`~/.brainstem/agents/` or the repo's `agents/`). It answers immediately via the
brainstem `/chat` — ask it to *"list today's SKU records"*.

## 3. Portable skill — any AI tool (no RAPP)
[`skill/SKILL.md`](skill/SKILL.md) + [`skill/omnichannel-inventory-agent.py`](skill/omnichannel-inventory-agent.py) are a
framework-free skill: run `python skill/omnichannel-inventory-agent.py "list"`, import `query()`, or
hand the SKILL.md to Claude / any agent that reads skills. Same data + contract
as the agent.py, zero RAPP dependency.
