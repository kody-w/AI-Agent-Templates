# Import — Contact Center Escalation Agent (Copilot Studio)

Two solutions, in order. Publisher: **Microsoft AI Business Applications Specialist Team (AIBAST)**.

1. **ContactCenterEscalationAgentMcpConnectors_1_0_0_1.zip** — the inline MCP data connector (synthetic Contact Center Escalation Agent data; every tool answers from embedded data, no external server). Import FIRST.
2. **ContactCenterEscalationAgentMcpAgents_1_0_0_1.zip** — the new-generation connected agents. Import SECOND.
3. Publish the parent agent.
4. On the agent: **Tools → Add a tool → Model Context Protocol** → pick the `Contact Center Escalation Agent` connector → create the **no-auth** connection → **Add** → **Publish**.

Synthetic data — no PII.
