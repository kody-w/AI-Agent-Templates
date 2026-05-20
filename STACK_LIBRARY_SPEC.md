# Stack Library Spec

This repository, and any sibling repository that mirrors it (e.g. focused subsets
used for testing), follow the same on-disk layout, metadata schema, and runtime
contract. This file is the contract.

A "stack library repo" is a static-site catalogue of agent stacks plus the
agent source itself, browsable through a single `index.html` and an
auto-generated `manifest.json`.

## Repo top level

```
repo/
├── index.html                 # the catalogue UI
├── manifest.json              # auto-generated; produced by update_manifest.py
├── update_manifest.py         # scans agents/ and agent_stacks/, rewrites manifest.json
├── README.md                  # repo overview
├── STACK_LIBRARY_SPEC.md      # this file
├── azuredeploy.json           # optional — one-click Azure Function deploy
├── agents/                    # singleton agents (no stack context)
│   ├── basic_agent.py         # BasicAgent shim — every agent imports this
│   └── *.py                   # one file per singleton agent
└── agent_stacks/
    └── {industry}_stacks/
        └── {stack_id}/
            ├── README.md
            ├── metadata.json
            ├── .gitignore
            ├── agents/        # the focused sub-agents
            │   └── *_agent.py
            ├── tests/         # pytest suite
            │   └── test_agents.py
            └── demos/         # optional HTML demo
                └── *_demo.html
```

`{industry}_stacks/` directories the manifest recognises:

| Directory                        | Display label              |
|----------------------------------|----------------------------|
| `b2b_sales_stacks`               | B2B Sales                  |
| `b2c_sales_stacks`               | B2C Sales                  |
| `energy_stacks`                  | Energy & Utilities         |
| `federal_government_stacks`      | Federal Government         |
| `financial_services_stacks`      | Financial Services         |
| `general_stacks`                 | Cross-Industry             |
| `healthcare_stacks`              | Healthcare                 |
| `manufacturing_stacks`           | Manufacturing              |
| `professional_services_stacks`   | Professional Services      |
| `retail_cpg_stacks`              | Retail & CPG               |
| `slg_government_stacks`          | State & Local Government   |
| `software_dp_stacks`             | Software & Digital Products|

## Agent source contract

Every agent file is a single `*_agent.py` that:

1. Imports `BasicAgent`:
   ```python
   from agents.basic_agent import BasicAgent
   ```
   That import resolves to the `rapp_ai` runtime in production, and to the
   in-repo shim (`agents/basic_agent.py`) when run standalone.

2. Defines exactly one class ending in `Agent` that subclasses `BasicAgent`,
   with:
   - `self.name` (string, matches class name)
   - `self.metadata` dict with `name`, `description`, and JSON-schema
     `parameters` (object with `properties` + `required`)
   - `perform(**kwargs)` returning a dict shaped:
     ```jsonc
     {
       "status": "success" | "needs_input" | "error" | "blocked",
       "agent":  "<self.name>",
       "message": "...",
       "data": { ... }    // present on success / structured outputs
     }
     ```

3. **Never fabricates data when required input is missing.** Missing required
   parameters return `status: "needs_input"`. Synthetic data is only emitted
   when caller explicitly opts in (e.g. omitting `asset_ids` to get a
   synthetic fleet sample).

4. Is **deterministic per input** where reasonable — use seeded random
   based on hashed keys so demos and code reviews are reproducible.

5. Has a `if __name__ == "__main__":` smoke test that prints a `perform()`
   result. Running `python agents/<name>.py` should produce valid JSON.

6. **No PII.** No real names, emails, account numbers, phone numbers, or
   real customer references. Synthetic IDs (`AST-00042`, `SUB-12`, `PMT-1`)
   only.

7. **No orchestrator agents.** Each agent owns one job. Composition is the
   LLM's responsibility — or the caller's. No `*_orchestrator_agent.py`.

## metadata.json schema

```jsonc
{
  "id": "field_crew_safety_and_work_permit_management_stack",
  "name": "Field Crew Safety and Work Permit Management Agent Stack",
  "version": "1.0.0.0",
  "description": "...",
  "category": "energy_utilities",        // matches industry_key
  "industry_label": "Energy Utilities",
  "complexity": "starter | intermediate | advanced",
  "features":  [ "...", ... ],
  "benefits":  [ "...", ... ],
  "starters":  [ "...", ... ],           // example user prompts
  "technicalRequirements": {
    "platforms":    ["Windows", "macOS", "Linux"],
    "dependencies": ["Python 3.11+"],
    "integrations": [ "...", ... ]
  },
  "components": [
    {
      "name": "<filename>.py",
      "description": "...",
      "role": "Focused agent in the 8-agent stack"
    }
  ],
  "useCases": [ "...", ... ]             // mirrors starters; consumed by index.html
}
```

The `stack_id` (directory name) MUST equal `metadata.id`.

## Tests

Every stack ships a `tests/test_agents.py` that:

- discovers `agents/*_agent.py`
- ensures the `*Agent` class loads with a valid metadata schema
- calls `perform()` with no args and asserts the status is `needs_input`,
  `error`, `blocked`, or `success` — never an uncaught exception, never
  fabricated content

Tests run standalone (`pytest -xvs tests/test_agents.py`). A BasicAgent
shim is written into `tests/_stub_runtime/` on first run.

## Manifest pipeline

`update_manifest.py` scans the repo and writes `manifest.json`. It is
expected to be runnable on the developer's box and is also invoked by
`.github/workflows/generate-manifest.yml`. The CLI UI (`index.html`)
fetches `manifest.json` at runtime — never reads files directly — so
`update_manifest.py` is the source of truth for what the catalogue shows.

To add a new stack:

1. Create `agent_stacks/{industry}_stacks/{stack_id}/` with the layout above
2. Run `python update_manifest.py`
3. Commit and push

`index.html` searches across: `name`, `description`, `longDescription`,
`useCase`, `category`, `industry`, `agents[]`, `benefits[]`, `features[]`,
`tags[]`. Make sure your metadata is rich enough that a user searching for
the natural keyword finds the stack.

## Forking this layout

To stand up a focused subset library (e.g. for testing a small group of
stacks against the same infrastructure), copy:

- `index.html`
- `update_manifest.py`
- `azuredeploy.json` (if you want one-click Azure Function deploy)
- `agents/basic_agent.py`
- `.github/workflows/`
- `STACK_LIBRARY_SPEC.md` (this file)

Then drop in only the stacks you want under `agent_stacks/`, run
`update_manifest.py`, and the catalogue self-builds.
