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
- `agent_stacks/` - Complete solutions organized by industry:
  - `general_stacks/` - Cross-industry solutions (voice_to_crm, email_drafting, simulation_sales)
  - `[industry]_stacks/` - Industry-specific stacks (financial_services, healthcare, retail_cpg, etc.)
- `agents_lab/` - Legacy industry-specific agent stacks (being migrated to agent_stacks/)

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

# Stack-specific agents (general)
python agent_stacks/general_stacks/[stack_name]/agents/[agent_name].py

# Industry vertical agents
python agent_stacks/[industry]_stacks/[stack_name]/agents/[agent_name].py

# Update manifest for web interface
python update_manifest.py
```

### Testing Agents
No formal test framework is configured. Test agents by:
1. Creating test scripts that import and instantiate agents
2. Calling `perform(**kwargs)` with test parameters
3. Validating JSON response structure

## Demo HTML Structure

### M365 Copilot Pattern
All demo files follow the Microsoft 365 Copilot design system (`m365_copilot_demo_template.html`):
- Segoe UI font family
- Sidebar navigation with Copilot branding
- Chat-based interface with typing indicators
- Demo controls (Play/Pause/Skip/Reset)
- Agent result cards with structured data display

### Demo Script Format
Demo conversations use this structure:
```javascript
const demoScript = [
    {
        "type": "user",
        "content": "User message",
        "typingTime": 1500,
        "delay": 1000
    },
    {
        "type": "agent", 
        "content": "Agent response",
        "typingTime": 2000,
        "delay": 1500,
        "agentData": {
            "Category": {
                "Field": "Value"
            }
        }
    }
];
```

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

### Trading Card Export
Generate standalone HTML agent cards: `generate_trading_card.js`

### Manifest Generation
The `update_manifest.py` script scans the repository and generates `manifest.json` with:
- All agents from `agents/` directory
- All stacks from `agent_stacks/` with industry categorization
- Deduplication of agents that exist in both locations
- File sizes, URLs, and metadata for web interface

## Python Code Conventions

- **Classes**: PascalCase (e.g., `CalendarAgent`)
- **Methods**: snake_case (e.g., `perform()`, `validate_parameters()`)
- **Private methods**: Leading underscore (e.g., `_internal_method()`)
- **Agent inheritance**: All agents extend `BasicAgent`
- **Error handling**: Try-except blocks with structured error responses
- **Parameter validation**: Validate before processing

## AI Decision System Pattern

For agents requiring probabilistic decision-making:
```python
def make_decision(self, context):
    decision = {
        "recommendation": "action",
        "confidence": 0.85,
        "reasoning": "Detailed explanation",
        "factors": {
            "factor1": {"weight": 0.4, "value": 0.9},
            "factor2": {"weight": 0.6, "value": 0.7}
        },
        "alternatives": [
            {"action": "alternative", "confidence": 0.65}
        ]
    }
    return decision
```

## Common Issues and Solutions

### Demo Not Playing
If demo doesn't show content when Play is clicked:
1. Check JavaScript console for errors
2. Verify `demoScript` array structure matches expected format (type: "user"/"agent")
3. Ensure HTML strings in content are properly escaped with `<br>` tags for line breaks
4. Check that `playNextMessage()` function correctly reads message type

### Agent Not Found
If agents aren't loading:
1. Run `python update_manifest.py` to regenerate manifest
2. Check file paths match expected pattern
3. Verify metadata.json exists in stack directories