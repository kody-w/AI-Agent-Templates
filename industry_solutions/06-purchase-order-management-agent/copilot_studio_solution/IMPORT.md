# Import — Purchase Order Management Agent (Copilot Studio)

Two solutions, in order. Publisher: **Microsoft AI Business Applications Specialist Team (AIBAST)**.

1. **PurchaseOrderManagementAgentMcpConnectors_1_0_0_1.zip** — the inline MCP data connector (synthetic Purchase Order Management Agent data; every tool answers from embedded data, no external server). Import FIRST.
2. **PurchaseOrderManagementAgentMcpAgents_1_0_0_1.zip** — the new-generation connected agents. Import SECOND.
3. Publish the parent agent.
4. On the agent: **Tools → Add a tool → Model Context Protocol** → pick the `Purchase Order Management Agent` connector → create the **no-auth** connection → **Add** → **Publish**.

Synthetic data — no PII.
