# AI Agent Templates

**Live library: https://kody-w.github.io/AI-Agent-Templates/**

An open library of **single-file AI agent templates** and **industry agent stacks** for the Microsoft AI stack. Each stack is a folder of plain Python agents plus an interactive demo — browse it, copy it, point it at your own tenant. No framework, no build step, no lock-in.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fkody-w%2FAI-Agent-Templates%2Fmain%2Fazuredeploy.json)

## This library and RAR

This repository is the **original template library** — the place the industry agents were first written and where the patterns are easiest to read. Its evolution lives at the **[RAPP Agent Registry (RAR)](https://kody-w.github.io/RAR/)**: upgraded live-data versions of these same industry agents, a community store with ratings, quality tiers, and one-command install. Start here to learn; graduate to RAR to run.

## What's inside

| Path | What it is |
|------|------------|
| `agents/` | Standalone single-file agents (calendar, CRM, search, memory, …). Drop any into an `agents/` folder and it self-registers. |
| `agent_stacks/<vertical>_stacks/` | Industry agent stacks — 86 stacks across 14 verticals (B2B/B2C sales, financial services, healthcare, energy, government, manufacturing, retail, IT, HR, professional services, software). |
| `agent_stacks/demos_needing_videos/` | 31 interactive demos, one per use case: a scripted conversation plus a **live-data panel** that fetches real records from the simulated enterprise sandbox. |
| `manifest.json` | Machine-readable index of every agent and stack (auto-generated — see below). |
| `index.html` | The web gallery — search, filter by vertical, live sandbox status. Works from `file://` too. |
| `azuredeploy.json` | One-click ARM template: Function App, Azure OpenAI, storage, App Insights. |
| `MSFTAIBASMultiAgentCopilot_1_0_0_5.zip` | Power Platform solution for Copilot Studio / Teams / M365 Copilot. |

### The agent pattern

Every agent is one Python file extending `BasicAgent`:

```python
from agents.basic_agent import BasicAgent

class WeatherAgent(BasicAgent):
    def __init__(self):
        self.name = "Weather"
        self.metadata = {
            "name": self.name,
            "description": "Gets the weather for a city.",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string", "description": "City name"}},
                "required": ["city"]
            }
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, city="", **kwargs):
        return f"It's sunny in {city}!"
```

Any `*_agent.py` file with this shape is auto-discovered by the RAPP brainstem, the Azure Function host, and Copilot Studio alike.

## The live enterprise sandbox

The demos (and your own experiments) run against a **globally public, simulated enterprise estate**: fourteen schema-true static APIs that mirror the real systems these agents integrate with — same shapes, field names, and id formats, no auth, no rate limits. All fourteen share one fictional world (**Aster Lane Office Systems**, 22 customer accounts, cross-linked stories), so records join *across* systems: CRM case `CAS-2601xx` → ITSM `INC00100xx` → ERP `PO-470xx` → HRIS `TOR-10xx`.

| System | Sample endpoint |
|--------|-----------------|
| CRM (Dynamics 365 style) | `https://kody-w.github.io/static-dynamics-365/api/data/v9.2/accounts.json` |
| Finance & Ops (F&O style) | `https://kody-w.github.io/static-dynamics-fno/data/CustomersV3.json` |
| ITSM (ServiceNow style) | `https://kody-w.github.io/static-itsm/api/now/table/incident.json` |
| Healthcare (FHIR R4) | `https://kody-w.github.io/static-fhir/fhir/Patient.json` |
| ERP / supply chain | `https://kody-w.github.io/static-erp/api/v1/purchase_orders.json` |
| HRIS | `https://kody-w.github.io/static-hris/api/v1/workers.json` |
| Sensor telemetry | `https://kody-w.github.io/static-telemetry/api/v1/sensors.json` |
| Second CRM (Salesforce style) | `https://kody-w.github.io/static-salesforce/services/data/v59.0/query/Account.json` |
| Documents (SharePoint style) | `https://kody-w.github.io/static-sharepoint/_api/web/lists/Policies/items.json` |
| Chat (Teams/Graph style) | `https://kody-w.github.io/static-teams/v1.0/teams.json` |
| Mail + Calendar (Graph style) | `https://kody-w.github.io/static-outlook/v1.0/users/jordan.lee/messages.json` |
| Issue tracking (Jira style) | `https://kody-w.github.io/static-issue-tracker/rest/api/2/search.json` |
| Core banking | `https://kody-w.github.io/static-core-banking/api/v1/members.json` |
| Firmographic enrichment | `https://kody-w.github.io/static-enrichment/api/v1/companies/summittrail.example.json` |

Templates coded against these run unchanged against a real tenant — swap the base URL. The full estate map (all shapes, join keys, and Issues-based write APIs) is documented in [RAR's skill.md](https://github.com/kody-w/RAR/blob/main/skill.md).

## Quickstart

**Just browse:** open https://kody-w.github.io/AI-Agent-Templates/ — search the stacks, play the demos, watch the sandbox status pings.

**Run an agent locally** (any Python 3.11+):

```bash
git clone https://github.com/kody-w/AI-Agent-Templates.git
cd AI-Agent-Templates
python3 agents/calendar_agent.py
```

**Run the full ladder** — the same three tiers the [RAPP installer](https://kody-w.github.io/rapp-installer/) teaches:

1. **Tier 1 — The Brainstem (local).** `curl -fsSL https://kody-w.github.io/rapp-installer/install.sh | bash` gives you a local agent server powered by GitHub Copilot (no API keys). Drop any agent file from this library into its `agents/` folder.
2. **Tier 2 — The Spinal Cord (Azure).** Click **Deploy to Azure** above: Function App (Python 3.11), Azure OpenAI, storage, App Insights — Entra ID auth, no keys.
3. **Tier 3 — The Nervous System (Copilot Studio).** Import the included Power Platform solution (`MSFTAIBASMultiAgentCopilot_1_0_0_5.zip`) into Copilot Studio, point it at your Azure Function, and publish. The same agent logic you tested locally now answers in Microsoft Teams and M365 Copilot across your organization.

## Regenerating the manifest

`manifest.json` and `agents/index.json` are generated — never hand-edit them:

```bash
python3 scripts/generate_manifest.py   # CI runs this on every push to agents/ or agent_stacks/
```

The manifest schema (`{version, generated, repository, branch, agents, stacks}`) and the `agents/index.json` shape (`{"agents": [filenames]}`) are **stable contracts** consumed by external agents in the RAR ecosystem — keep keys and paths resolvable.

The demo pages are also generated from one template:

```bash
python3 scripts/generate_demos.py      # rewrites agent_stacks/demos_needing_videos/*.html in place
```

## Contributing

1. Fork, then add your agent as **one Python file** following the `BasicAgent` pattern (`*_agent.py`, snake_case).
2. Standalone agents go in `agents/`; industry solutions get a stack folder: `agent_stacks/<vertical>_stacks/<your_stack>/` with `agents/`, `metadata.json`, and optionally `demos/`.
3. Run `python3 scripts/generate_manifest.py` and include the regenerated `manifest.json` in your PR.
4. Want ratings, versioning, and one-command install for your agent? Submit it to [RAR](https://github.com/kody-w/RAR) — that's where the community registry lives.

## License

MIT
