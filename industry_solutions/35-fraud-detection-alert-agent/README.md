# Fraud Detection & Alert Agent

Deploy AI-driven fraud monitoring and identification to accelerate investigations, enhance detection rates, and improve prevention.

**Industry:** Financial Services · **Personas:** Fraud Analysts; SIU Investigators; Risk Leaders · **Featured tools:** Dynamics 365 ERP, Microsoft Teams
**Publisher:** Microsoft AI Business Applications Specialist Team (AIBAST). Synthetic demo data — no PII.

Install this solution **three ways**:

## 1. One-click Copilot Studio (manual import)
No code, no hosting — new-generation connected agents with embedded data.
1. **Copilot Studio → Solutions → Import solution** → `copilot_studio_solution/FraudDetectionAlertAgentMcpConnectors_1_0_0_1.zip` → Import.
2. Repeat for `copilot_studio_solution/FraudDetectionAlertAgentMcpAgents_1_0_0_1.zip`.
3. Open **FraudDetectionAlertAgent** and **Publish**.
4. **Tools → Add a tool → Model Context Protocol** → the `Fraud Detection & Alert Agent` connector → no-auth connection → Add → Publish.
See `copilot_studio_solution/IMPORT.md`.

## 2. RAPP brainstem (agent.py)
Drop [`agent.py`](agent.py) into your local RAPP brainstem's `agents/` folder
(`~/.brainstem/agents/` or the repo's `agents/`). It answers immediately via the
brainstem `/chat` — ask it to *"list today's case records"*.

## 3. Portable skill — any AI tool (no RAPP)
[`skill/SKILL.md`](skill/SKILL.md) + [`skill/fraud-detection-alert-agent.py`](skill/fraud-detection-alert-agent.py) are a
framework-free skill: run `python skill/fraud-detection-alert-agent.py "list"`, import `query()`, or
hand the SKILL.md to Claude / any agent that reads skills. Same data + contract
as the agent.py, zero RAPP dependency.
