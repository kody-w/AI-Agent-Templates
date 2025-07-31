# Universal Agent Library

This directory contains reusable agents that can be deployed across different AI templates.

## Structure

- **core/** - Base agent classes and common functionality
- **memory/** - Agents for managing conversation memory and context
- **integrations/** - Agents for integrating with external systems (CRM, SharePoint, etc.)
- **intelligence/** - Agents for data analysis and market intelligence
- **utils/** - Utility agents for common tasks

## Usage

Each template declares its agent dependencies in an agent-manifest.json file. The deployment scripts automatically pull the required agents from this central library.

## Version Management

Each agent includes version information in its docstring and a VERSION constant. Update these when making changes.

## Adding New Agents

1. Create the agent in the appropriate directory
2. Inherit from BasicAgent in the core module
3. Add proper documentation and version info
4. Update any template manifests that should use the new agent
