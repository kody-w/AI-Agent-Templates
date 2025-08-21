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
- Each stack contains its own agents that may extend or compose base agents

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

# Execute agent stacks
python agent_stacks/[stack_name]/[script_name].py
```

### Testing Agents
Since no test framework is configured, test agents by:
1. Creating test scripts that import and instantiate agents
2. Calling `perform()` with appropriate test parameters
3. Validating JSON response structure and content

## Agent Development Guidelines

### Creating New Agents
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

## Integration Points

### CRM Integrations
- **Dynamics 365**: Full CRUD operations via Web API
- **Salesforce**: Query operations via REST API
- **ServiceNow**: Ticket and workflow management

### Agent Composition
- Agents can instantiate and call other agents (e.g., `BulkCRMDataGeneratorAgent` uses `OneClickCRMIntakeAgent`)
- Stack solutions combine multiple agents for end-to-end workflows

### Web Interface
- `index.html` provides browser-based agent interaction
- Stack-specific HTML files demonstrate specialized workflows

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