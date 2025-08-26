# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

AI Agent Templates is a comprehensive collection of modular AI agents and stacks for building intelligent automation solutions with Azure and Microsoft 365 integration. The repository contains both individual agents and complete agent stacks organized by industry verticals.

## Architecture

### Core Agent Pattern
All agents inherit from `BasicAgent` class (`agents/basic_agent.py`):
```python
class BasicAgent:
    def __init__(self, name, metadata):
        self.name = name
        self.metadata = metadata
    
    def perform(self):
        pass
```

### Directory Structure
- `agents/` - Individual agent implementations (single-purpose components)
- `agent_stacks/` - Legacy complete solutions (voice_to_crm, email_drafting, etc.)
- `agents_lab/` - Industry-specific agent stacks organized by vertical:
  - `b2b_sales_stack/` - B2B sales automation agents
  - `b2c_sales_stack/` - B2C retail and e-commerce agents
  - `healthcare_stack/` - Healthcare and clinical agents
  - `financial_services_stack/` - Banking and insurance agents
  - `energy_stack/` - Energy and utilities agents
  - `manufacturing_stack/` - Manufacturing and supply chain agents
  - `federal_government_stack/` - Federal government agents
  - `slg_government_stack/` - State and local government agents
  - `professional_services_stack/` - Professional services agents
  - `retail_cpg_stack/` - Retail and CPG agents
  - `software_dp_stack/` - Software and digital products agents

### Stack Structure Pattern
Each agent stack follows standardized organization:
```
stack_name/
├── agents/
│   └── stack_agent.py         # Python agent implementation
├── demos/
│   └── stack_demo.html        # Interactive HTML demonstration
├── metadata.json              # Stack configuration and documentation
└── files/ (optional)          # Supporting resources
```

## Common Development Tasks

### Running Agent Scripts
```bash
# Individual agents
python agents/[agent_name].py

# Stack-specific agents (legacy)
python agent_stacks/[stack_name]/agents/[agent_name].py

# Industry vertical agents
python agents_lab/[vertical]_stack/[stack_name]/agents/[agent_name].py

# Batch generate all industry stacks
python agents_lab/generate_all_stacks.py

# Update all demo files
python agents_lab/update_all_demos.py

# Update manifest for web interface
python update_manifest.py
```

### Testing Agents
No formal test framework is configured. Test agents by:
1. Creating test scripts that import and instantiate agents
2. Calling `perform(**kwargs)` with test parameters
3. Validating JSON response structure

## Azure Deployment

### One-Click Deployment
Deploy complete infrastructure using ARM template:
- Azure OpenAI Service (GPT-4o)
- Azure Function App for agent execution
- Storage Account for data persistence
- Application Insights for monitoring

Deploy via: `azuredeploy.json`

### Microsoft 365 Integration
1. Import Power Platform solution: `MSFTAIBASMultiAgentCopilot_1_0_0_2.zip`
2. Configure Power Automate flow with Azure Function endpoint
3. Deploy to Teams/M365 Copilot via Copilot Studio

## Agent Development Guidelines

### Metadata Structure
All agents must define metadata with:
- `name`: Agent identifier
- `description`: Clear purpose statement
- `parameters`: Input schema with types and requirements
- `required`: Array of mandatory parameters

### Response Format
Consistent JSON structure:
```json
{
  "status": "success|error",
  "message": "Human-readable message",
  "data": {},
  "errors": []
}
```

### Environment Variables
External service credentials:
- **Dynamics 365**: `DYNAMICS_365_CLIENT_ID`, `DYNAMICS_365_CLIENT_SECRET`, `DYNAMICS_365_TENANT_ID`, `DYNAMICS_365_RESOURCE`
- **Azure OpenAI**: `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`
- **Azure Storage**: `AZURE_STORAGE_CONNECTION_STRING`

## Web Interface

### Main Gallery (`index.html`)
- Dynamic agent/stack browsing from GitHub
- Trading card export functionality
- Live API integration mode
- Simulated demo mode

### Demo Pages
Each stack includes interactive HTML demo in `demos/` directory showcasing:
- Agent capabilities and workflow
- Input/output examples
- Integration points
- Business value proposition

### Trading Card Export
Generate standalone HTML agent cards: `generate_trading_card.js`

## Python Code Conventions

- **Classes**: PascalCase (e.g., `CalendarAgent`)
- **Methods**: snake_case (e.g., `perform()`, `validate_parameters()`)
- **Private methods**: Leading underscore (e.g., `_internal_method()`)
- **Agent inheritance**: All agents extend `BasicAgent`
- **Error handling**: Try-except blocks with structured error responses
- **Parameter validation**: Validate before processing