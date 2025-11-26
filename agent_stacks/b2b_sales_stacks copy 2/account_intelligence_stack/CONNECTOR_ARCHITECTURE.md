# Connector Architecture Guide
## Multi-CRM Support with Mock & Production Modes

This guide explains how the Account Intelligence Stack connects to multiple data sources with support for **testing (MOCK mode)** and **production (LIVE mode)**.

---

## 🏗️ **Architecture Overview**

```
┌────────────────────────────────────────────────────────────┐
│                  Azure Function Entry Point                 │
│                      (__init__.py)                         │
└──────────────────────┬─────────────────────────────────────┘
                       │
                       ▼
┌────────────────────────────────────────────────────────────┐
│           Account Intelligence Orchestrator                 │
│         (account_intelligence_orchestrator.py)             │
└──────────────────────┬─────────────────────────────────────┘
                       │
          ┌────────────┼────────────┐
          │            │            │
          ▼            ▼            ▼
    ┌─────────┐  ┌──────────┐  ┌──────────┐
    │Stakeholder│ │Competitive│ │Meeting   │
    │  Agent   │  │  Agent    │  │Prep Agent│
    └─────────┘  └──────────┘  └──────────┘
          │            │            │
          └────────────┴────────────┘
                       │
                       ▼
┌────────────────────────────────────────────────────────────┐
│                   CONNECTORS LAYER                         │
│                                                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │CRM Connector │  │Graph         │  │LinkedIn      │   │
│  │- Dynamics365 │  │Connector     │  │Connector     │   │
│  │- Salesforce  │  │(M365 data)   │  │(Sales Nav)   │   │
│  │- Monday.com  │  │              │  │              │   │
│  │- HubSpot     │  │              │  │              │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
│                                                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │Azure OpenAI  │  │Azure AI      │  │Power Platform│   │
│  │Connector     │  │Search        │  │Connector     │   │
│  │(GPT-4o)      │  │Connector     │  │(Pass-through)│   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
└────────────────────────────────────────────────────────────┘
                       │
          ┌────────────┴────────────┐
          │                         │
          ▼                         ▼
    ┌──────────┐             ┌──────────┐
    │MOCK DATA │             │REAL APIs │
    │(Testing) │             │(Production)│
    └──────────┘             └──────────┘
```

---

## 🔄 **MOCK vs PRODUCTION Mode**

### **MOCK Mode** (Default - for testing)
- ✅ No API credentials required
- ✅ Returns realistic fake data
- ✅ Test locally without Azure/CRM setup
- ✅ Instant responses (no network calls)
- ✅ Perfect for development & demos

### **PRODUCTION Mode** (for live deployment)
- ✅ Connects to real CRM systems
- ✅ Real Microsoft Graph API data
- ✅ Live LinkedIn Sales Navigator
- ✅ Actual Azure OpenAI responses
- ✅ Real competitive intelligence

---

## ⚙️ **Configuration**

### **Switching Modes**

Edit `config.py` or set environment variable:

```bash
# MOCK mode (default - no setup required)
export MODE=mock

# PRODUCTION mode (requires credentials)
export MODE=production
```

### **Selecting CRM System**

```bash
# Choose your CRM system
export CRM_SYSTEM=dynamics_365  # or salesforce, monday, hubspot
```

### **Full Configuration Example**

```bash
# Mode selection
export MODE=production
export CRM_SYSTEM=salesforce

# Salesforce credentials
export SALESFORCE_INSTANCE_URL=https://yourinstance.salesforce.com
export SALESFORCE_USERNAME=your.email@company.com
export SALESFORCE_PASSWORD=yourpassword
export SALESFORCE_SECURITY_TOKEN=yoursecuritytoken

# Azure OpenAI
export AZURE_OPENAI_ENDPOINT=https://your-openai.openai.azure.com
export AZURE_OPENAI_KEY=your-api-key
export AZURE_OPENAI_DEPLOYMENT=gpt-4o

# Microsoft Graph API
export GRAPH_API_CLIENT_ID=your-app-registration-id
export GRAPH_API_CLIENT_SECRET=your-client-secret
export GRAPH_API_TENANT_ID=your-tenant-id

# Azure AI Search
export AZURE_AI_SEARCH_ENDPOINT=https://your-search.search.windows.net
export AZURE_AI_SEARCH_KEY=your-search-key
```

---

## 📦 **Connector Details**

### **1. CRM Connector** (`connectors/crm_connector.py`)

**Supports:**
- ✅ Microsoft Dynamics 365
- ✅ Salesforce
- ✅ Monday.com
- ✅ HubSpot

**Methods:**
```python
crm = CRMConnector()

# Get account data
account = crm.get_account("CONTOSO001")

# Get contacts (buying committee)
contacts = crm.get_contacts("CONTOSO001")

# Get opportunities (deals)
opportunities = crm.get_opportunities("CONTOSO001")

# Get activities (emails, meetings, calls)
activities = crm.get_activities("CONTOSO001")
```

**Mock Data Includes:**
- Account: Company info, revenue, employees, health score
- Contacts: 5 stakeholders with titles, emails, relationship strength
- Opportunities: $2.1M deal with stage, probability, risks
- Activities: Recent emails, meetings, phone calls

**Production Setup:**

**Dynamics 365:**
```bash
export DYNAMICS_365_URL=https://org.crm.dynamics.com
export DYNAMICS_365_CLIENT_ID=your-app-id
export DYNAMICS_365_CLIENT_SECRET=your-secret
export DYNAMICS_365_TENANT_ID=your-tenant
```

**Salesforce:**
```bash
export SALESFORCE_INSTANCE_URL=https://yourinstance.salesforce.com
export SALESFORCE_USERNAME=user@company.com
export SALESFORCE_PASSWORD=password
export SALESFORCE_SECURITY_TOKEN=token
```

**Monday.com:**
```bash
export MONDAY_API_URL=https://api.monday.com/v2
export MONDAY_API_KEY=your-api-key
```

**HubSpot:**
```bash
export HUBSPOT_API_URL=https://api.hubapi.com
export HUBSPOT_API_KEY=your-api-key
```

---

### **2. Microsoft Graph Connector** (To be created)

**Data Sources:**
- Emails (stakeholder communication)
- Meetings (calendar interactions)
- Org charts (company structure)
- User profiles

**Mock Data:**
- 12 email interactions with CTO
- 3 meetings attended
- Response time: 4 hours average
- Last contact: dates and sentiment

---

### **3. LinkedIn Connector** (Via Power Platform)

**Integration Method:**
Copilot Studio → Power Platform LinkedIn Connector → Azure Function

**Data:**
- Professional backgrounds
- Connections & mutual connections
- Recent posts & engagement
- Career history

---

### **4. Azure OpenAI Connector**

**Use Cases:**
- Intelligence synthesis
- Message generation
- Meeting brief creation
- Risk analysis summaries

**Mock Mode:**
- Returns pre-written templates
- Simulates AI responses

**Production Mode:**
- Calls real GPT-4o API
- Generates custom responses

---

### **5. Azure AI Search Connector**

**Purpose:**
Competitive intelligence indexing

**Data Sources:**
- Web scraping (competitor sites)
- G2/TrustRadius reviews
- News articles
- Market research

---

## 🔌 **Power Platform Connector Integration**

### **How Copilot Studio Passes Credentials**

When Copilot Studio calls your Azure Function, it can pass connector tokens:

```javascript
// Copilot Studio HTTP Action configuration
{
  "method": "POST",
  "url": "https://your-function.azurewebsites.net/api/intelligence",
  "headers": {
    "Content-Type": "application/json",
    "x-functions-key": "your-function-key",
    "x-connector-token": "{{PowerPlatformConnectorToken}}"  // <-- Passed from Copilot Studio
  },
  "body": {
    "operation": "account_briefing",
    "account_id": "{{account_id}}"
  }
}
```

**Azure Function receives it:**

```python
# __init__.py
def main(req: func.HttpRequest) -> func.HttpResponse:
    # Get connector token from header
    connector_token = req.headers.get('x-connector-token')

    # Pass to orchestrator
    orchestrator = AccountIntelligenceOrchestrator(connector_token=connector_token)
    result = orchestrator.perform(**req_body)
```

**Connector uses it:**

```python
# connectors/crm_connector.py
class CRMConnector(BaseConnector):
    def __init__(self, connector_token: str = None):
        super().__init__(connector_token)
        # Use connector_token for Power Platform authenticated API calls
```

---

## 🧪 **Testing Locally**

### **Test CRM Connector (Mock Mode)**

```bash
cd connectors
python crm_connector.py

# Output:
# Testing CRM Connector in MOCK mode...
# Connection Test: {
#   "status": "success",
#   "mode": "mock",
#   "crm_system": "dynamics_365"
# }
# Account Data: { ... }
# Contacts Count: 5
# Opportunities Count: 1
# ✅ CRM Connector test complete!
```

### **Test Full Stack**

```bash
cd agents
python account_intelligence_orchestrator.py

# Output:
# {
#   "status": "success",
#   "operation": "account_briefing",
#   "data": { ... },
#   "mode": "mock"
# }
```

---

## 🚀 **Deploying to Production**

### **Step 1: Configure Environment Variables**

In Azure Function App → Configuration → Application Settings:

```
MODE=production
CRM_SYSTEM=salesforce

# Salesforce (example)
SALESFORCE_INSTANCE_URL=https://yourinstance.salesforce.com
SALESFORCE_USERNAME=@Microsoft.KeyVault(SecretUri=https://your-kv.vault.azure.net/secrets/SF-USERNAME)
SALESFORCE_PASSWORD=@Microsoft.KeyVault(SecretUri=https://your-kv.vault.azure.net/secrets/SF-PASSWORD)
SALESFORCE_SECURITY_TOKEN=@Microsoft.KeyVault(SecretUri=https://your-kv.vault.azure.net/secrets/SF-TOKEN)

# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://your-openai.openai.azure.com
AZURE_OPENAI_KEY=@Microsoft.KeyVault(SecretUri=https://your-kv.vault.azure.net/secrets/OPENAI-KEY)

# Microsoft Graph
GRAPH_API_CLIENT_ID=your-app-id
GRAPH_API_CLIENT_SECRET=@Microsoft.KeyVault(SecretUri=https://your-kv.vault.azure.net/secrets/GRAPH-SECRET)
GRAPH_API_TENANT_ID=your-tenant-id

# Azure AI Search
AZURE_AI_SEARCH_ENDPOINT=https://your-search.search.windows.net
AZURE_AI_SEARCH_KEY=@Microsoft.KeyVault(SecretUri=https://your-kv.vault.azure.net/secrets/SEARCH-KEY)
```

### **Step 2: Test Production Connection**

```bash
# Call Azure Function with production mode
curl -X POST "https://your-function.azurewebsites.net/api/intelligence?code=your-key" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "account_briefing",
    "account_id": "REAL_ACCOUNT_ID"
  }'

# Response will include:
# "mode": "production"
# "source": "salesforce"  (or dynamics_365, etc.)
```

### **Step 3: Monitor & Validate**

Check Application Insights for:
- API call success rates
- Response times
- Error logs
- Data source availability

---

## 🔐 **Security Best Practices**

✅ **Always use Key Vault** for secrets (never environment variables directly)
✅ **Enable Managed Identity** for Azure resources
✅ **Use Power Platform connectors** for pre-authenticated APIs
✅ **Rotate credentials** every 90 days
✅ **Limit API scopes** to minimum required permissions
✅ **Enable audit logging** for all data access

---

## 📊 **Data Flow Example**

**User Query in Teams:**
> "Give me a briefing on Contoso Corporation"

**Flow:**
```
1. Copilot Studio recognizes intent
2. Calls Azure Function HTTP endpoint
3. Azure Function → Orchestrator
4. Orchestrator → CRM Connector (get_account, get_contacts, get_opportunities)
5. CRM Connector checks Config.MODE
   - If MOCK: Returns fake data instantly
   - If PRODUCTION: Calls Salesforce API with credentials
6. Orchestrator → Graph Connector (get stakeholder emails)
7. Orchestrator → Azure OpenAI (synthesize intelligence)
8. Response flows back to Copilot Studio
9. User sees formatted briefing in Teams
```

---

## 🛠️ **Troubleshooting**

### **"Connection failed" in Production**

```bash
# Check credentials
az keyvault secret show --name SF-USERNAME --vault-name your-kv

# Test CRM connection manually
python connectors/crm_connector.py
```

### **"Mock data returned" when expecting production**

```bash
# Verify MODE is set to production
az functionapp config appsettings list --name your-function --resource-group your-rg | grep MODE

# Should show: MODE=production
```

### **Salesforce authentication errors**

- Verify security token is correct (check email for reset token)
- Ensure IP is whitelisted in Salesforce
- Check API version compatibility

---

## 📚 **Next Steps**

1. ✅ Test locally with MOCK mode
2. ✅ Deploy to Azure Function
3. ⚙️ Configure production credentials in Key Vault
4. 🔄 Set MODE=production
5. 🧪 Test with real CRM data
6. 🚀 Integrate with Copilot Studio
7. 📊 Monitor in Application Insights

---

**Ready to connect to real systems!** Follow COPILOT_STUDIO_SETUP_GUIDE.md for complete deployment. 🚀
