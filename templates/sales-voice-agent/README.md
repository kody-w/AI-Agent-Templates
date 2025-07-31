# Sales Voice Agent - Azure Deployment Package

This folder contains all resources needed to deploy the Sales Voice Copilot to Azure using the centralized agent architecture.

## 🚀 Quick Deploy

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FYOUR-USERNAME%2FAI-AGENT-TEMPLATES%2Fmain%2Ftemplates%2Fsales-voice-agent%2Fazuredeploy.json)

Replace `YOUR-USERNAME` with your GitHub username in the URL above.

## 📋 Overview

The Sales Voice Agent is a comprehensive AI-powered solution that enables sales teams to:

- Update CRM records using voice commands
- Access customer information hands-free
- Get real-time market insights
- Maintain conversation context across sessions

### Key Features

- 🎤 **Voice Interface**: Natural language voice commands with Azure Speech Services
- 🤖 **Multi-Agent System**: Orchestrates multiple specialized agents
- 💾 **Persistent Memory**: GUID-based user tracking with conversation history
- 🔗 **CRM Integration**: Native Dynamics 365 support
- 📊 **Market Intelligence**: Real-time tech news and insights
- 🔒 **Enterprise Security**: Azure AD, Key Vault, and RBAC

## 🏗️ Architecture

This template uses the **centralized agent architecture**:

```
├── Central Agent Library (GitHub)
│   ├── core/BasicAgent
│   ├── memory/ManageMemory
│   ├── memory/ContextMemory
│   ├── integrations/Dynamics365CRUD
│   └── intelligence/HackerNewsAgent
│
└── Azure Deployment
    ├── Function App (Downloads agents)
    ├── Storage Account (Stores agents)
    └── Key Vault (Manages secrets)
```

## 📦 What Gets Deployed

- **Azure Function App** (Python 3.9)
- **Storage Account** with File Shares
- **Application Insights** for monitoring
- **Key Vault** for secure secrets
- **Speech Services** (optional)
- **Container Instance** (temporary, for agent deployment)

## 🛠️ Prerequisites

1. **Azure Subscription** with appropriate permissions
2. **Azure OpenAI Service** with GPT-4 deployment
3. **Azure CLI** installed locally
4. **GitHub Repository** forked/cloned with agent library

### Optional Prerequisites

- **Dynamics 365** instance and app registration (for CRM features)
- **SharePoint** access (for document processing)

## 📖 Deployment Options

### Option 1: One-Click Deploy (Recommended)

1. Click the "Deploy to Azure" button above
2. Fill in the required parameters:
   - Project Name (3-11 characters)
   - Azure OpenAI endpoint and key
   - Optional: CRM credentials
3. Review and create
4. Wait ~10 minutes for deployment

### Option 2: PowerShell Script

```powershell
# Clone the repository
git clone https://github.com/YOUR-USERNAME/AI-AGENT-TEMPLATES.git
cd AI-AGENT-TEMPLATES/templates/sales-voice-agent

# Run deployment
./deploy-sales-voice.ps1 `
    -ResourceGroupName "rg-salesvoice-prod" `
    -Location "East US" `
    -AzureOpenAIEndpoint "https://your-openai.openai.azure.com/" `
    -AzureOpenAIApiKey "your-key"
```

### Option 3: Manual Deployment

1. Deploy the ARM template:

```bash
az deployment group create \
    --resource-group rg-salesvoice \
    --template-file azuredeploy.json \
    --parameters @parameters.json
```

2. Deploy agents from central library:

```powershell
../../scripts/deploy-agents.ps1 `
    -ManifestPath ./agent-manifest.json `
    -ResourceGroup rg-salesvoice
```

## 📝 Configuration

### Agent Manifest

The `agent-manifest.json` file declares which agents this template uses:

```json
{
  "name": "sales-voice-agent",
  "version": "1.0.0",
  "agents": {
    "required": [
      "core/BasicAgent",
      "memory/ManageMemory",
      "memory/ContextMemory",
      "integrations/Dynamics365CRUD",
      "intelligence/HackerNewsAgent"
    ],
    "optional": ["integrations/SharePointExtractor"]
  }
}
```

### Environment Variables

Key environment variables set by the deployment:

- `AZURE_OPENAI_ENDPOINT` - Your OpenAI endpoint
- `AZURE_OPENAI_API_KEY` - API key (from Key Vault)
- `AGENT_MANIFEST_URL` - Points to agent manifest
- `MEMORY_PATH` - Agent memory storage path
- `DYNAMICS_365_*` - CRM configuration (if enabled)
- `SPEECH_SERVICES_*` - Voice configuration (if enabled)

## 🧪 Testing

### Test the Function Endpoint

```bash
curl -X POST https://<function-app>.azurewebsites.net/api/businessinsightbot_function \
  -H "Content-Type: application/json" \
  -H "x-functions-key: <function-key>" \
  -d '{
    "user_input": "Hello, can you help me update my CRM?",
    "conversation_history": [],
    "user_guid": "test-user-123"
  }'
```

### Test Voice Commands

1. Open the voice interface (index_voice.html)
2. Allow microphone access
3. Try commands like:
   - "Show me the latest tech news"
   - "Update the Contoso account in CRM"
   - "What did we discuss last time?"

## 📊 Monitoring

### Application Insights

View logs and metrics:

1. Go to Azure Portal
2. Navigate to your Application Insights resource
3. Check:
   - Live Metrics Stream
   - Failures
   - Performance
   - Custom events

### Storage Explorer

View agent files and memories:

1. Open Azure Storage Explorer
2. Navigate to your storage account
3. Browse file shares:
   - `/agents/` - Deployed agent files
   - `/memory/{guid}/` - User memories
   - `/shared_memories/` - Shared context

## 🔧 Customization

### Adding New Agents

1. Add agent to central library: `/agents/category/NewAgent.py`
2. Update manifest to include new agent
3. Redeploy agents:

```powershell
../../scripts/deploy-agents.ps1 -ManifestPath ./agent-manifest.json -ResourceGroup rg-salesvoice
```

### Modifying Voice Settings

Edit the function app settings:

- `SPEECH_SERVICES_REGION` - Change region
- `ASSISTANT_NAME` - Customize assistant name
- `CHARACTERISTIC_DESCRIPTION` - Modify behavior

## 🚨 Troubleshooting

### Common Issues

1. **Agents not loading**

   - Check Application Insights logs
   - Verify agent files in storage
   - Ensure manifest URL is accessible

2. **Voice not working**

   - Verify Speech Services is deployed
   - Check browser microphone permissions
   - Confirm HTTPS is enabled

3. **CRM integration failing**
   - Verify app registration permissions
   - Check Dynamics 365 URL format
   - Confirm credentials in Key Vault

### Debug Mode

Enable debug logging:

```bash
az functionapp config appsettings set \
    --name <function-app> \
    --resource-group <rg> \
    --settings "AGENT_DEBUG=true"
```

## 💰 Cost Estimation

Typical monthly costs (2,500 conversations/week):

- Function App (Consumption): $50-100
- Storage Account: $20-40
- Application Insights: $30-50
- Speech Services: $0-20
- **Total: $100-210/month**

_Note: Azure OpenAI costs are separate and usage-based_

## 📚 Additional Resources

- [Main Repository](https://github.com/YOUR-USERNAME/AI-AGENT-TEMPLATES)
- [Agent Library Documentation](https://github.com/YOUR-USERNAME/AI-AGENT-TEMPLATES/tree/main/agents)
- [Azure Functions Python Guide](https://docs.microsoft.com/azure/azure-functions/functions-reference-python)
- [Dynamics 365 Web API](https://docs.microsoft.com/dynamics365/customer-engagement/web-api/)

## 🤝 Contributing

To contribute improvements:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📄 License

MIT License - see [LICENSE](../../LICENSE) for details.

---

**Need help?** Open an issue in the [GitHub repository](https://github.com/YOUR-USERNAME/AI-AGENT-TEMPLATES/issues)
