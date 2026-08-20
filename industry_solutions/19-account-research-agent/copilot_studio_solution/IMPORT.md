# Import — Account Research Agent (Copilot Studio)

Two solutions, in order. Publisher: **Microsoft AI Business Applications Specialist Team (AIBAST)**.

1. **AccountResearchAgentMcpConnectors_1_0_0_1.zip** — the inline MCP data connector (synthetic Account Research Agent data; every tool answers from embedded data, no external server). Import FIRST.
2. **AccountResearchAgentMcpAgents_1_0_0_1.zip** — the new-generation connected agents. Import SECOND.
3. Publish the parent agent.
4. On the agent: **Tools → Add a tool → Model Context Protocol** → pick the `Account Research Agent` connector → create the **no-auth** connection → **Add** → **Publish**.

Synthetic data — no PII.
