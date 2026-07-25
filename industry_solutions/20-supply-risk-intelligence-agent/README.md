# Supply Risk Intelligence Agent

Deliver real-time risk intelligence and planning to protect production continuity and reduce disruption exposure.

**Industry:** Manufacturing · **Personas:** Procurement Manager; Supply Chain Director · **Featured tools:** Dynamics 365 ERP, Microsoft Teams
**Publisher:** Microsoft AI Business Applications Specialist Team (AIBAST). Synthetic demo data — no PII.

Install this solution **three ways**:

## 1. One-click Copilot Studio (manual import)
No code, no hosting — new-generation connected agents with embedded data.
1. **Copilot Studio → Solutions → Import solution** → `copilot_studio_solution/SupplyRiskIntelligenceAgentMcpConnectors_1_0_0_1.zip` → Import.
2. Repeat for `copilot_studio_solution/SupplyRiskIntelligenceAgentMcpAgents_1_0_0_1.zip`.
3. Open **SupplyRiskIntelligenceAgent** and **Publish**.
4. **Tools → Add a tool → Model Context Protocol** → the `Supply Risk Intelligence Agent` connector → no-auth connection → Add → Publish.
See `copilot_studio_solution/IMPORT.md`.

## 2. RAPP brainstem (agent.py)
Drop [`agent.py`](agent.py) into your local RAPP brainstem's `agents/` folder
(`~/.brainstem/agents/` or the repo's `agents/`). It answers immediately via the
brainstem `/chat` — ask it to *"list today's work order records"*.

## 3. Portable skill — any AI tool (no RAPP)
[`skill/SKILL.md`](skill/SKILL.md) + [`skill/supply-risk-intelligence-agent.py`](skill/supply-risk-intelligence-agent.py) are a
framework-free skill: run `python skill/supply-risk-intelligence-agent.py "list"`, import `query()`, or
hand the SKILL.md to Claude / any agent that reads skills. Same data + contract
as the agent.py, zero RAPP dependency.
