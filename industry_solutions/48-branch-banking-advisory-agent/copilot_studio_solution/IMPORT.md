# Import — Branch Banking Advisory Agent (Copilot Studio)

Two solutions, in order. Publisher: **Microsoft AI Business Applications Specialist Team (AIBAST)**.

1. **BranchBankingAdvisoryAgentMcpConnectors_1_0_0_1.zip** — the inline MCP data connector (synthetic Branch Banking Advisory Agent data; every tool answers from embedded data, no external server). Import FIRST.
2. **BranchBankingAdvisoryAgentMcpAgents_1_0_0_1.zip** — the new-generation connected agents. Import SECOND.
3. Publish the parent agent.
4. On the agent: **Tools → Add a tool → Model Context Protocol** → pick the `Branch Banking Advisory Agent` connector → create the **no-auth** connection → **Add** → **Publish**.

Synthetic data — no PII.
