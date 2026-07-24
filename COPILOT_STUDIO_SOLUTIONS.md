# Copilot Studio Solutions — One-Click Industry Deploys

Ready-to-import **Power Platform solutions** that stand up each industry agent
stack as **new-generation connected agents** in Copilot Studio — the **Tier 3**
of the [3-tier model](README.md) (local runtime → Azure Function → Copilot Studio).
No code, no hosting: import two solutions, publish, attach one connector.

**Publisher:** Microsoft AI Business Applications Specialist Team (AIBAST) · prefix `aibast`

| Industry solution | Domain | One-pager | One-click bundle |
|-------------------|--------|-----------|------------------|
| **Loan Origination & Credit Decisioning** | retail lending | [view](agent_stacks/financial_services_stacks/loan_origination_assistant_stack/ONE_PAGER.html) | [`agent_stacks/financial_services_stacks/loan_origination_assistant_stack/copilot_studio_solution/`](agent_stacks/financial_services_stacks/loan_origination_assistant_stack/copilot_studio_solution/) |
| **Payments Operations Excellence** | payments | [view](agent_stacks/financial_services_stacks/payments_operations_excellence_stack/ONE_PAGER.html) | [`agent_stacks/financial_services_stacks/payments_operations_excellence_stack/copilot_studio_solution/`](agent_stacks/financial_services_stacks/payments_operations_excellence_stack/copilot_studio_solution/) |
| **Intelligent Patient Intake & Triage** | patient access | [view](agent_stacks/healthcare_stacks/patient_intake_stack/ONE_PAGER.html) | [`agent_stacks/healthcare_stacks/patient_intake_stack/copilot_studio_solution/`](agent_stacks/healthcare_stacks/patient_intake_stack/copilot_studio_solution/) |
| **Clinical Documentation & Coding** | clinical documentation | [view](agent_stacks/healthcare_stacks/clinical_notes_summarizer_stack/ONE_PAGER.html) | [`agent_stacks/healthcare_stacks/clinical_notes_summarizer_stack/copilot_studio_solution/`](agent_stacks/healthcare_stacks/clinical_notes_summarizer_stack/copilot_studio_solution/) |
| **Prior Authorization & Utilization Management** | utilization management | [view](agent_stacks/healthcare_stacks/prior_authorization_stack/ONE_PAGER.html) | [`agent_stacks/healthcare_stacks/prior_authorization_stack/copilot_studio_solution/`](agent_stacks/healthcare_stacks/prior_authorization_stack/copilot_studio_solution/) |

## The shape (BlastBox two-solution)
Each bundle is **two** solutions: an inline **MCP data connector** (synthetic
domain data, every tool answers from embedded data — no external server) and a
**new-generation agents** solution (a `cliagent` parent + a connected specialist
child, each agent riding as a Python skill). Import the connector first, then the
agents; publish; and attach the MCP connector to each agent (the one step with no
API — walked through in each bundle's `MANUAL_STEPS.html`).

Each `copilot_studio_solution/` folder also ships an `EVALUATION.csv` (demo script
+ Copilot Studio Evaluate import) and the RAPP quality-contract `source_agents/`
the solution was generated from. Synthetic data only — **no PII**.
