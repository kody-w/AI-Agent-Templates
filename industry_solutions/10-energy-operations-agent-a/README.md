# Energy Operations Agent (a)

Deliver real-time insights, automate critical workflows, and enable guided decision making—boosting efficiency while reducing operational and compliance risk for energy organizations.

**Industry:** Energy and Utilities · **Personas:** Plant Manager / Reliability Engineer; Compliance Manager; Sustainability Lead; Data Analyst · **Featured tools:** Dynamics 365 ERP, SharePoint, Microsoft Teams
**Publisher:** Microsoft AI Business Applications Specialist Team (AIBAST). Synthetic demo data — no PII.

Install this solution **three ways**:

## 1. One-click Copilot Studio (manual import)
No code, no hosting — new-generation connected agents with embedded data.
1. **Copilot Studio → Solutions → Import solution** → `copilot_studio_solution/EnergyOperationsAgentAMcpConnectors_1_0_0_1.zip` → Import.
2. Repeat for `copilot_studio_solution/EnergyOperationsAgentAMcpAgents_1_0_0_1.zip`.
3. Open **EnergyOperationsAgentA** and **Publish**.
4. **Tools → Add a tool → Model Context Protocol** → the `Energy Operations Agent (a)` connector → no-auth connection → Add → Publish.
See `copilot_studio_solution/IMPORT.md`.

## 2. RAPP brainstem (agent.py)
Drop [`agent.py`](agent.py) into your local RAPP brainstem's `agents/` folder
(`~/.brainstem/agents/` or the repo's `agents/`). It answers immediately via the
brainstem `/chat` — ask it to *"list today's site records"*.

## 3. Portable skill — any AI tool (no RAPP)
[`skill/SKILL.md`](skill/SKILL.md) + [`skill/energy-operations-agent-a.py`](skill/energy-operations-agent-a.py) are a
framework-free skill: run `python skill/energy-operations-agent-a.py "list"`, import `query()`, or
hand the SKILL.md to Claude / any agent that reads skills. Same data + contract
as the agent.py, zero RAPP dependency.
