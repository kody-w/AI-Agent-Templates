# Product Line Optimization Agent

Provide intelligent production capacity analysis and optimization planning to boost throughput and efficiency while maintaining quality.

**Industry:** Manufacturing · **Personas:** Plant Manager; Production Engineer; Operations Director · **Featured tools:** Dynamics 365 ERP, PowerBI, Azure IoT Hub
**Publisher:** Microsoft AI Business Applications Specialist Team (AIBAST). Synthetic demo data — no PII.

Install this solution **three ways**:

## 1. One-click Copilot Studio (manual import)
No code, no hosting — new-generation connected agents with embedded data.
1. **Copilot Studio → Solutions → Import solution** → `copilot_studio_solution/ProductLineOptimizationAgentMcpConnectors_1_0_0_1.zip` → Import.
2. Repeat for `copilot_studio_solution/ProductLineOptimizationAgentMcpAgents_1_0_0_1.zip`.
3. Open **ProductLineOptimizationAgent** and **Publish**.
4. **Tools → Add a tool → Model Context Protocol** → the `Product Line Optimization Agent` connector → no-auth connection → Add → Publish.
See `copilot_studio_solution/IMPORT.md`.

## 2. RAPP brainstem (agent.py)
Drop [`agent.py`](agent.py) into your local RAPP brainstem's `agents/` folder
(`~/.brainstem/agents/` or the repo's `agents/`). It answers immediately via the
brainstem `/chat` — ask it to *"list today's record records"*.

## 3. Portable skill — any AI tool (no RAPP)
[`skill/SKILL.md`](skill/SKILL.md) + [`skill/product-line-optimization-agent.py`](skill/product-line-optimization-agent.py) are a
framework-free skill: run `python skill/product-line-optimization-agent.py "list"`, import `query()`, or
hand the SKILL.md to Claude / any agent that reads skills. Same data + contract
as the agent.py, zero RAPP dependency.
