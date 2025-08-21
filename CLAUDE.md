# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a Python-based AI agent template repository that provides modular, reusable agent components for building intelligent automation solutions. The project focuses on business integration scenarios including CRM systems (Dynamics 365, Salesforce, ServiceNow), email management, calendar scheduling, and document processing.

## Architecture

### Core Pattern: Agent Inheritance
All agents inherit from `BasicAgent` class (`agents/basic_agent.py`):
- Base class with `__init__(name, metadata)` and abstract `perform()` method
- Metadata structure defines agent capabilities, parameters, and descriptions
- Each agent implements `perform(**kwargs)` to execute its specific functionality

### Directory Structure
- `agents/` - Individual agent implementations (single-purpose components)
- `agent_stacks/` - Complete solutions combining multiple agents for complex workflows
  - Each stack follows a standardized structure:
    - `agents/` - Stack-specific agent implementations
    - `demos/` - Interactive HTML demonstrations
    - `files/` - Additional resources (zip files, templates, etc.)
    - `metadata.json` - Complete stack configuration and documentation
- `index.html` - Web interface gallery for browsing agents and stacks
- `generate_trading_card.js` - Utility for exporting standalone HTML agent cards

### Key Design Patterns
1. **Metadata-Driven**: Agents self-describe their capabilities through structured metadata
2. **Parameter Validation**: Agents validate required parameters before execution
3. **JSON Communication**: All agents return JSON-formatted results
4. **Environment Configuration**: External service credentials via environment variables
5. **Error Handling**: Consistent error reporting through JSON responses

## Common Development Tasks

### Running Python Scripts
```bash
# Execute individual agents
python agents/[agent_name].py

# Execute stack-specific agents
python agent_stacks/[stack_name]/agents/[agent_name].py

# Run interactive demos
# Open in browser: agent_stacks/[stack_name]/demos/[demo_name].html
```

### Testing Agents
Since no test framework is configured, test agents by:
1. Creating test scripts that import and instantiate agents
2. Calling `perform()` with appropriate test parameters
3. Validating JSON response structure and content

## Agent Stack Development

### Stack Metadata Structure
Each agent stack must include a `metadata.json` file with:
```json
{
  "id": "stack_identifier",
  "name": "Human-readable name",
  "version": "1.0.0",
  "description": "Brief description",
  "category": "communication|data-management|training|etc",
  "complexity": "starter|intermediate|advanced",
  "features": ["array", "of", "features"],
  "benefits": ["key", "benefits"],
  "technicalRequirements": {
    "platforms": ["Windows", "macOS", "Linux"],
    "dependencies": ["Python 3.8+", "etc"],
    "apiKeys": ["REQUIRED_API_KEY_NAMES"]
  },
  "components": [
    {
      "name": "agent_file.py",
      "description": "What this agent does",
      "role": "Agent's role in the stack"
    }
  ],
  "demo": {
    "available": true,
    "url": "agent_stacks/stack_name/demos/demo.html",
    "title": "Demo title",
    "description": "What the demo shows"
  }
}
```

### Creating New Agent Stacks
1. Create directory: `agent_stacks/your_stack_name/`
2. Add subdirectories:
   - `agents/` - All Python agent files
   - `demos/` - Interactive HTML demonstrations
   - `files/` - Supporting resources (optional)
3. Create `metadata.json` with complete configuration
4. Ensure all agents follow the BasicAgent pattern
5. Add demo HTML to showcase functionality

## Agent Development Guidelines

### Creating New Individual Agents
1. Extend `BasicAgent` class
2. Define metadata with name, description, and parameters schema
3. Implement `perform(**kwargs)` method
4. Return JSON-formatted results
5. Handle errors gracefully with informative messages

### Required Environment Variables
Agents requiring external services expect these environment variables:
- **Dynamics 365**: `DYNAMICS_365_CLIENT_ID`, `DYNAMICS_365_CLIENT_SECRET`, `DYNAMICS_365_TENANT_ID`, `DYNAMICS_365_RESOURCE`
- **Azure OpenAI**: `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`
- **Azure Storage**: `AZURE_STORAGE_CONNECTION_STRING`

### Parameter Structure
All agents follow consistent parameter patterns:
- Required parameters defined in metadata `required` array
- Optional parameters with defaults or conditional logic
- Nested objects for complex configurations
- Validation before execution

## Available Agent Stacks

### voice_to_crm_stack
- **Purpose**: Voice-enabled CRM data entry with real-time processing
- **Key Agents**: dynamics_365_agent, servicenow-agent, email_drafting_agent, extract_sharepoint_document_url_agent
- **Demo**: Interactive voice recording with live API integration mode
- **Use Cases**: Field sales updates, customer service call logging, executive meeting notes

### crm_bulk_data_creator_stack
- **Purpose**: Generate and import large volumes of test data into CRM systems
- **Key Agents**: bulk_crm_data_generator, dynamics_365_agent, OneClickCRMIntakeAgent
- **Use Cases**: Testing environment setup, sales training data, demo preparation

### email_drafting_stack
- **Purpose**: AI-powered email composition and automation
- **Key Agents**: email_drafting_agent
- **Use Cases**: Customer support responses, sales outreach, internal communications

### simulation_sales_stack
- **Purpose**: Advanced sales training and simulation platform
- **Key Agents**: sales_simulation_agent
- **Demo**: Interactive sales scenario simulations
- **Use Cases**: New hire onboarding, objection handling practice, negotiation training

## Integration Points

### CRM Integrations
- **Dynamics 365**: Full CRUD operations via Web API
- **Salesforce**: Query operations via REST API
- **ServiceNow**: Ticket and workflow management

### Agent Composition
- Agents can instantiate and call other agents (e.g., `BulkCRMDataGeneratorAgent` uses `OneClickCRMIntakeAgent`)
- Stack solutions combine multiple agents for end-to-end workflows
- Stack agents are located in `agent_stacks/[stack_name]/agents/` directory

### Web Interface
- `index.html` provides comprehensive gallery and agent browser
  - Dynamic loading from GitHub repository
  - Interactive stack templates with metadata
  - Trading card export functionality
  - Live API integration capabilities
- Stack demos located in `agent_stacks/[stack_name]/demos/`
  - `voice_to_crm_showcase.html` - Voice recording and CRM integration
  - `ai-simulation-sales-demo.html` - Sales simulation interface
  - Additional demos for each stack's specific workflow

## Code Conventions

### Python Style
- Class names: PascalCase (e.g., `CalendarAgent`)
- Method names: snake_case (e.g., `perform()`, `validate_parameters()`)
- Private methods: Leading underscore (e.g., `_perform_operation()`)

### Response Format
All agents return JSON with consistent structure:
```json
{
  "status": "success|error",
  "message": "Human-readable message",
  "data": {},
  "errors": []
}
```

### Error Handling
- Validate parameters before processing
- Return structured error responses
- Include helpful error details for debugging
- Use try-except blocks for external service calls

## Web Interface Features

### index.html Capabilities
- **Agent Gallery**: Browse all individual agents with GitHub integration
- **Stack Templates**: Explore complete agent stacks with metadata
- **Trading Card Export**: Generate standalone HTML files for sharing stacks
- **Live Demo Mode**: Test stacks with simulated data
- **Live API Mode**: Connect to real Azure Functions endpoints
- **Dynamic Loading**: Automatically fetches latest agents from GitHub

### Stack Demo Pages
Each stack can include demo HTML files in `demos/` directory:
- Interactive UI for testing agent functionality
- Live mode for production API integration
- Simulated mode for testing without credentials
- Visual feedback and real-time processing