# AI Agent Templates

A comprehensive collection of AI agent templates and stacks for building intelligent automation solutions. This repository provides ready-to-use agent templates for various business scenarios including CRM integration, email management, calendar scheduling, and more.

## 🚀 Features

- **Modular Agent Architecture**: Built on a flexible `BasicAgent` base class for easy extension
- **Pre-built Agent Templates**: Ready-to-use agents for common business scenarios
- **Agent Stacks**: Complete solutions combining multiple agents for complex workflows
- **Integration Ready**: Templates for popular platforms (Dynamics 365, Salesforce, ServiceNow, etc.)
- **Azure Integration**: Built-in support for Azure services (OpenAI, File Storage)

## 📁 Project Structure

```
AI-Agent-Templates/
├── agents/                    # Individual agent templates
│   ├── basic_agent.py         # Base agent class
│   ├── calendar_agent.py      # Calendar scheduling
│   ├── dynamics_365_agent.py  # Dynamics 365 CRM integration
│   ├── email_drafting_agent.py # Email composition
│   ├── image_generation_agent.py # DALL-E image generation
│   └── ...                    # More agent templates
├── agent_stacks/              # Complete agent solutions
│   ├── crm_bulk_data_creator_stack/
│   │   ├── agents/            # Stack-specific agents
│   │   ├── demos/             # Interactive demonstrations
│   │   └── metadata.json      # Stack configuration
│   ├── email_drafting_stack/
│   │   ├── agents/            # Email processing agents
│   │   ├── demos/             # Demo interfaces
│   │   ├── files/             # Additional resources
│   │   └── metadata.json      # Stack configuration
│   ├── simulation_sales_stack/
│   │   ├── agents/            # Sales simulation agents
│   │   ├── demos/             # Interactive demos
│   │   └── metadata.json      # Stack configuration
│   └── voice_to_crm_stack/
│       ├── agents/            # Voice processing agents
│       ├── demos/             # Voice-to-CRM demo
│       ├── files/             # Supporting files
│       └── metadata.json      # Stack configuration
└── index.html                 # Web interface gallery

```

## 🤖 Available Agents

### Core Agents
- **BasicAgent**: Base class for all agents
- **ContextMemoryAgent**: Agent with persistent memory capabilities
- **ManageMemoryAgent**: Memory management and optimization

### Business Integration Agents
- **Dynamics365Agent**: Microsoft Dynamics 365 CRM operations
- **SalesforceQueryAgent**: Salesforce data queries and operations
- **ServiceNowAgent**: ServiceNow ticket and workflow management
- **CalendarAgent**: Meeting scheduling with conflict resolution
- **EmailDraftingAgent**: Intelligent email composition

### Utility Agents
- **ImageGenerationAgent**: Azure OpenAI DALL-E integration
- **CodeReviewAgent**: Automated code review and analysis
- **AdaptiveCardAgent**: Microsoft Adaptive Cards generation
- **DuckDuckGoSearchAgent**: Web search capabilities
- **HackerNewsAgent**: Hacker News content fetching

### Demo & Skill Agents
- **PowerPointAgent**: Presentation generation
- **MeetingPrepAgent**: Meeting preparation assistance
- **MotivationalQuoteSkill**: Random motivational quotes
- **FetchRandomWikipediaArticle**: Wikipedia content retrieval

## 🛠️ Agent Stacks

Agent Stacks are complete, production-ready solutions that combine multiple agents to solve complex business problems. Each stack follows a standardized structure:

- **`agents/`** - Contains all Python agent files for the stack
- **`demos/`** - Interactive HTML demonstrations
- **`files/`** - Additional resources and dependencies
- **`metadata.json`** - Complete stack configuration and documentation

### Voice to CRM Stack
Voice-enabled CRM data entry with real-time processing:
- Speech-to-text conversion with Azure Cognitive Services
- Natural language processing for entity extraction
- Automatic CRM record creation in Dynamics 365/ServiceNow
- Email drafting from voice commands
- SharePoint document linking
- Live API integration mode for production use

### CRM Bulk Data Creator Stack
Complete solution for generating test data in CRM systems:
- Generate thousands of realistic customer records
- Create complex relationship hierarchies
- Bulk import to Dynamics 365
- Industry-specific data templates
- GDPR-compliant test data generation
- Performance testing datasets

### Email Drafting Stack
AI-powered email composition and automation:
- Context-aware email generation
- Multi-language support
- Microsoft 365 integration
- Sentiment analysis and tone adjustment
- Template library management
- Automated follow-up scheduling

### Simulation Sales Stack
Advanced sales training and simulation platform:
- Realistic customer persona simulations
- Real-time AI coaching and feedback
- Objection handling practice
- Negotiation scenario training
- Performance analytics dashboard
- Gamification and leaderboards

## 🚦 Getting Started

### Prerequisites
```python
# Required Python packages (install as needed)
import json
import random
import requests
import logging
from datetime import datetime
```

### Basic Usage

1. **Using a Basic Agent:**
```python
from agents.basic_agent import BasicAgent

# Create an agent instance
agent = BasicAgent(name="MyAgent", metadata={})

# Execute agent task
result = agent.perform()
```

2. **Using Specialized Agents:**
```python
from agents.calendar_agent import CalendarAgent

# Initialize calendar agent
calendar = CalendarAgent()

# Schedule a meeting
meeting_result = calendar.perform()
```

3. **Using Agent Stacks:**
```python
# Import agents from the standardized structure
from agent_stacks.crm_bulk_data_creator_stack.agents.bulk_crm_data_generator import BulkCRMDataGeneratorAgent
from agent_stacks.voice_to_crm_stack.agents.dynamics_365_agent import Dynamics365Agent

# Initialize bulk data generator
generator = BulkCRMDataGeneratorAgent()

# Generate CRM data
data = generator.perform(
    iterations=10,
    company_name_components={...},
    contact_name_pools={...}
)

# Or use voice-to-CRM agents
dynamics = Dynamics365Agent()
result = dynamics.create_account(account_data)
```

## 🔧 Configuration

Most agents require environment variables or configuration:

```python
# Example for Azure OpenAI integration
AZURE_OPENAI_API_KEY = "your-api-key"
AZURE_OPENAI_ENDPOINT = "your-endpoint"
AZURE_STORAGE_CONNECTION_STRING = "your-connection-string"
```

## 📚 Agent Development

### Creating a Custom Agent

```python
from agents.basic_agent import BasicAgent

class CustomAgent(BasicAgent):
    def __init__(self):
        self.name = "CustomAgent"
        self.metadata = {
            "name": self.name,
            "description": "Your agent description",
            "parameters": {
                "type": "object",
                "properties": {
                    # Define your parameters
                },
                "required": []
            }
        }
        super().__init__(name=self.name, metadata=self.metadata)
    
    def perform(self, **kwargs):
        # Implement your agent logic
        return "Agent result"
```

## 🌐 Web Interface

The project includes a comprehensive web interface (`index.html`) that provides:
- **Agent Gallery**: Browse and explore all available agents
- **Stack Templates**: Interactive demos for each agent stack
- **Trading Card Export**: Generate standalone HTML "trading cards" for sharing agent stacks
- **Live API Integration**: Connect to your own Azure Functions for real-time processing
- **GitHub Integration**: Automatically loads agents and stacks from the repository

Open `index.html` in a browser to explore the full gallery and interactive demonstrations.

## 🤝 Contributing

Contributions are welcome! 

### To add a new individual agent:
1. Create a new Python file in the `agents/` directory
2. Extend the `BasicAgent` class
3. Implement the `perform()` method
4. Add appropriate metadata and parameters
5. Document your agent's functionality

### To add a new agent stack:
1. Create a new directory under `agent_stacks/your_stack_name/`
2. Follow the standard structure:
   - `agents/` - Place all Python agent files here
   - `demos/` - Add interactive HTML demonstrations
   - `files/` - Include any additional resources
   - `metadata.json` - Define stack configuration
3. Ensure your metadata.json includes all required fields
4. Add demo files to showcase stack capabilities

## 📝 License

This project is provided as-is for educational and development purposes.

## 🔗 Integration Examples

### Dynamics 365 Integration
The Dynamics 365 agents provide comprehensive CRM functionality including account management, contact creation, and opportunity tracking.

### Azure Services Integration
Multiple agents leverage Azure services:
- Azure OpenAI for image generation
- Azure File Storage for document management
- Azure Cognitive Services for various AI capabilities

## 📧 Support

For questions or issues, please create an issue in the repository.

---

**Note**: Remember to configure your API keys and endpoints before using agents that require external service integration.