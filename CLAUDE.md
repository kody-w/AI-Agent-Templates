# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

AI-Agent-Templates is the **original single-file agent template library** for the Microsoft AI stack: standalone Python agents plus 86 industry agent stacks across 14 verticals, a web gallery (`index.html`), interactive demos, and one-click Azure deployment. Its evolution is the [RAR registry](https://github.com/kody-w/RAR) (live-data agents, community store); this repo stays the readable, copyable origin.

GitHub Pages serves the repo root at https://kody-w.github.io/AI-Agent-Templates/ (legacy build, branch `main`, path `/`).

## Stable Contracts — Do Not Break

External agents in the RAR ecosystem consume this repo raw. Never rename or remove:

1. **`manifest.json`** — schema `{version, generated, repository, branch, agents, stacks}` and the entry shapes inside (fetched by `@kody-w/transcript2prototype_agent`). Regenerating values is fine; keys and referenced paths must stay resolvable.
2. **`agents/*.py` filenames and `agents/index.json`** (`{"agents": [filenames]}`) — enumerated by `@discreetRappers/scripted_demo_agent` and `@kody-w/github_agent_library_agent`. Content edits are fine if each file still parses and runs standalone.
3. **`agent_stacks/<vertical>_stacks/<stack>/` paths** referenced by manifest.json, and the `agent_stacks/demos_needing_videos/*.html` filenames.
4. **`index.html` at repo root** — it is the Pages landing page.

## Build Commands

```bash
# Regenerate manifest.json + agents/index.json (the only build step; CI runs it too)
python3 scripts/generate_manifest.py     # update_manifest.py is a back-compat shim

# Regenerate all 31 demo pages from the single template
python3 scripts/generate_demos.py
```

CI: `.github/workflows/generate-manifest.yml` runs `scripts/generate_manifest.py` on pushes touching `agents/**` or `agent_stacks/**` and commits the result.

## Architecture

### Core Agent Pattern

All agents inherit from `BasicAgent` (`agents/basic_agent.py`), define `self.metadata` (name, description, JSON-schema parameters), and implement `perform(**kwargs)`. One file per agent, `*_agent.py`, snake_case. Every agent must run standalone: `python3 agents/<name>.py` exits cleanly.

### Directory Structure

- `agents/` — standalone single-file agents
- `agent_stacks/<vertical>_stacks/<stack>/` — industry stacks: `agents/` + `metadata.json` + optional `demos/`, `files/`
- `agent_stacks/demos_needing_videos/` — the 31 generated demo pages (edit `scripts/generate_demos.py`, never the HTML directly)
- `agents_lab/` — legacy stacks kept for reference
- `scripts/` — generators (manifest, demos)

### Demo Pages

All demos in `demos_needing_videos/` come from **one template** inside `scripts/generate_demos.py`: dark-first responsive UI, scripted 3-turn conversation, and a live-data panel fetching the matching simulated-estate API in-browser (graceful offline fallback). To change a demo, edit its spec in the `DEMOS` dict and rerun the generator. The generator refuses to create files not already present (filenames are a contract).

### The Simulated Enterprise Estate

Demos and the `index.html` sandbox section fetch from 14 public schema-true simulators (`kody-w.github.io/static-*`) sharing the Aster Lane Office Systems fictional world. Full map: RAR `skill.md`, section "The Simulated Enterprise Estate". When adding demo integrations, verify an endpoint with `curl` before wiring it in.

### index.html

Single-file gallery, no dependencies, no emojis (inline SVG glyphs only). Stacks/agents render from `manifest.json` fetched at runtime with an embedded fallback snapshot (`FALLBACK` const) so `file://` works. If the manifest changes shape-visibly (new stacks/verticals), refresh the embedded fallback: build a compact `{agents, stacks}` snapshot from manifest.json and replace the JSON after the `/*__FALLBACK_JSON__*/` marker comment (see git history for the injection snippet).

## Deployment Tiers (README has the user-facing version)

1. **Brainstem (local)** — RAPP installer, GitHub Copilot as engine, agents drop-in.
2. **Azure** — `azuredeploy.json` ARM template (Function App Python 3.11, Azure OpenAI, storage, App Insights).
3. **Copilot Studio** — import `MSFTAIBASMultiAgentCopilot_1_0_0_5.zip`, point it at the Azure Function, publish to Teams/M365 Copilot. The zip rides the rapp-installer release train — update it by copying the new binary from `kody-w/rapp-installer` (never push to that repo) and bumping every filename reference.

## Conventions

- Python 3.11+; classes PascalCase, methods snake_case, agents end `_agent.py`.
- Secrets via `os.environ.get()`, never hardcoded; agents degrade gracefully when env vars are missing.
- `manifest.json` and `agents/index.json` are generated — never hand-edit.
- No emojis in any UI surface; use inline SVG glyphs.
- Verify pages by serving locally (`python3 -m http.server`) and driving with a real browser before pushing.
