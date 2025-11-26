# Copilot Studio Setup Guide
## Integrate Account Intelligence with Microsoft 365 Copilot

This guide walks you through integrating the Account Intelligence Stack with Microsoft Copilot Studio.

---

## Prerequisites

✅ **Azure Resources** (deployed via `deploy.sh`):
- Azure Function App running
- Function endpoint URL
- Function key/authentication

✅ **Microsoft 365**:
- Microsoft 365 E3/E5 license (or Copilot license)
- Dynamics 365 Sales license
- LinkedIn Sales Navigator license (optional but recommended)

✅ **Permissions**:
- Global Administrator or Copilot Studio Administrator
- Azure subscription Owner/Contributor

---

## Step 1: Deploy Azure Function

```bash
# Make deploy script executable
chmod +x deploy.sh

# Run deployment
./deploy.sh

# Save the output:
# - Function Endpoint: https://your-function.azurewebsites.net/api/intelligence
# - Function Key: your-function-key
```

---

## Step 2: Configure Azure Key Vault Secrets

Navigate to Azure Portal → Key Vault → Secrets:

### Required Secrets:

1. **DYNAMICS-365-URL**
   ```
   Value: https://yourorg.crm.dynamics.com
   ```

2. **AZURE-OPENAI-ENDPOINT**
   ```
   Value: https://your-openai.openai.azure.com
   ```

3. **AZURE-OPENAI-KEY**
   ```
   Value: your-openai-api-key
   ```

4. **GRAPH-API-CLIENT-ID**
   ```
   Value: your-app-registration-client-id
   ```

5. **GRAPH-API-CLIENT-SECRET**
   ```
   Value: your-app-registration-client-secret
   ```

6. **AZURE-AI-SEARCH-ENDPOINT**
   ```
   Value: https://your-search.search.windows.net
   ```

7. **AZURE-AI-SEARCH-KEY**
   ```
   Value: your-search-api-key
   ```

### Update Function App to Use Key Vault:

```bash
# Get Key Vault URI
KEY_VAULT_URI="https://your-keyvault.vault.azure.net"

# Update Function App settings
az functionapp config appsettings set \
  --name your-function-app \
  --resource-group your-resource-group \
  --settings \
    DYNAMICS_365_URL="@Microsoft.KeyVault(SecretUri=${KEY_VAULT_URI}/secrets/DYNAMICS-365-URL)" \
    AZURE_OPENAI_ENDPOINT="@Microsoft.KeyVault(SecretUri=${KEY_VAULT_URI}/secrets/AZURE-OPENAI-ENDPOINT)" \
    AZURE_OPENAI_KEY="@Microsoft.KeyVault(SecretUri=${KEY_VAULT_URI}/secrets/AZURE-OPENAI-KEY)" \
    GRAPH_API_CLIENT_ID="@Microsoft.KeyVault(SecretUri=${KEY_VAULT_URI}/secrets/GRAPH-API-CLIENT-ID)" \
    GRAPH_API_CLIENT_SECRET="@Microsoft.KeyVault(SecretUri=${KEY_VAULT_URI}/secrets/GRAPH-API-CLIENT-SECRET)" \
    AZURE_AI_SEARCH_ENDPOINT="@Microsoft.KeyVault(SecretUri=${KEY_VAULT_URI}/secrets/AZURE-AI-SEARCH-ENDPOINT)" \
    AZURE_AI_SEARCH_KEY="@Microsoft.KeyVault(SecretUri=${KEY_VAULT_URI}/secrets/AZURE-AI-SEARCH-KEY)"

# Enable Managed Identity
az functionapp identity assign \
  --name your-function-app \
  --resource-group your-resource-group

# Grant Key Vault access to Function App
FUNCTION_IDENTITY=$(az functionapp identity show --name your-function-app --resource-group your-resource-group --query principalId -o tsv)

az keyvault set-policy \
  --name your-keyvault \
  --object-id $FUNCTION_IDENTITY \
  --secret-permissions get list
```

---

## Step 3: Test Azure Function

```bash
# Test with curl
curl -X POST "https://your-function.azurewebsites.net/api/intelligence?code=your-function-key" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "account_briefing",
    "account_id": "CONTOSO001"
  }'

# Expected response:
# {
#   "status": "success",
#   "operation": "account_briefing",
#   "account_id": "CONTOSO001",
#   "data": { ... },
#   "sources": ["Dynamics 365", "Microsoft Graph", ...],
#   "confidence": 0.92
# }
```

---

## Step 4: Create Azure AD App Registration (for Graph API)

### 4.1 Create App Registration:

1. Navigate to **Azure Portal** → **Azure Active Directory** → **App Registrations**
2. Click **New Registration**
3. Name: `Account Intelligence Graph API`
4. Supported account types: **Single tenant**
5. Click **Register**

### 4.2 Configure API Permissions:

1. Go to **API Permissions**
2. Add permissions:
   - **Microsoft Graph** → **Application permissions**:
     - `User.Read.All`
     - `Contacts.Read`
     - `Mail.Read`
     - `Calendars.Read`
3. Click **Grant admin consent**

### 4.3 Create Client Secret:

1. Go to **Certificates & secrets**
2. Click **New client secret**
3. Description: `Account Intelligence Secret`
4. Expiry: 24 months
5. Copy the **Client Secret** value
6. Save to Key Vault as `GRAPH-API-CLIENT-SECRET`

---

## Step 5: Register Plugin in Copilot Studio

### 5.1 Access Copilot Studio:

1. Navigate to **https://copilotstudio.microsoft.com**
2. Sign in with your Microsoft 365 account

### 5.2 Create New Copilot Agent:

1. Click **Create** → **New copilot**
2. Name: `Account Intelligence Assistant`
3. Description: `B2B sales account intelligence with stakeholder analysis, competitive intel, and deal tracking`
4. Language: English
5. Click **Create**

### 5.3 Add Plugin/Action:

1. In your Copilot, go to **Actions** → **Add an action**
2. Select **Create from blank**
3. Choose **HTTP action**

### 5.4 Configure HTTP Action:

**Action 1: Account Briefing**
```yaml
Name: Get Account Briefing
Description: Get comprehensive intelligence on an account including CRM data, stakeholders, and competitive threats

HTTP Request:
  Method: POST
  URL: https://your-function.azurewebsites.net/api/intelligence

Headers:
  Content-Type: application/json
  x-functions-key: your-function-key

Body (JSON):
  {
    "operation": "account_briefing",
    "account_id": "{account_id}"
  }

Input Parameters:
  - account_id (string, required): Account name or ID

Output Schema:
  - status (string)
  - operation (string)
  - data (object)
  - sources (array)
  - confidence (number)

Conversational Triggers:
  - "Give me a briefing on {account_id}"
  - "What do you know about {account_id}"
  - "Account intelligence for {account_id}"
```

**Action 2: Stakeholder Analysis**
```yaml
Name: Analyze Stakeholders
Description: Deep dive on buying committee with influence scores

HTTP Request:
  Method: POST
  URL: https://your-function.azurewebsites.net/api/intelligence

Body (JSON):
  {
    "operation": "stakeholder_analysis",
    "account_id": "{account_id}"
  }

Conversational Triggers:
  - "Who are the stakeholders at {account_id}"
  - "Show me the buying committee for {account_id}"
  - "Analyze decision makers at {account_id}"
```

**Action 3: Meeting Preparation**
```yaml
Name: Prepare for Meeting
Description: Generate executive meeting brief with scripts and strategies

HTTP Request:
  Method: POST
  URL: https://your-function.azurewebsites.net/api/intelligence

Body (JSON):
  {
    "operation": "meeting_prep",
    "account_id": "{account_id}",
    "contact_id": "{contact_id}"
  }

Conversational Triggers:
  - "Prepare me for my meeting with {contact_id}"
  - "Meeting prep for {contact_id} at {account_id}"
```

Repeat for remaining operations: `competitive_intelligence`, `generate_messaging`, `risk_assessment`, `action_plan`, `deal_dashboard`

---

## Step 6: Configure Response Formatting

In Copilot Studio, configure the response format:

### 6.1 Add Response Templates:

**Account Briefing Template:**
```
I've analyzed {{account_id}} across multiple data sources. Here's your briefing:

**Company Overview:**
- Industry: {{data.Company_Overview.Industry}}
- Size: {{data.Company_Overview.Size}}
- Health Score: {{data.CRM_Status.Health_Score}}

**Key Findings:**
- {{data.Key_Stakeholders}} stakeholders identified
- Win Probability: {{data.Win_Probability}}
- Priority: {{data.Priority}}

**Competitive Threats:**
{{#each data.Competitive_Threats}}
- {{competitor}}: {{threat_level}}
{{/each}}

**Data Sources:** {{sources}}
**Confidence:** {{confidence}}
```

---

## Step 7: Test in Microsoft Teams

### 7.1 Deploy to Teams:

1. In Copilot Studio, click **Publish**
2. Select **Microsoft Teams**
3. Click **Deploy**
4. App will appear in Teams app store

### 7.2 Test Conversational Flow:

**In Microsoft Teams:**
```
User: "Give me a briefing on Contoso Corporation"

Copilot: [Calls Account Intelligence Function]

Response: "I've analyzed Contoso Corporation across Dynamics 365, Microsoft Graph, and LinkedIn Sales Navigator. Here's your briefing:

**Company Overview:**
- Industry: Manufacturing & Industrial Technology
- Size: 12,400 employees | $2.3B revenue
- Health Score: 72/100 - Yellow

**Key Findings:**
- 5 stakeholders identified in buying committee
- Win Probability: 47%
- Priority: HIGH - At-risk renewal + expansion opportunity

**Competitive Threats:**
- DataBricks: CRITICAL - CTO's ex-Microsoft colleague is their AE
- Snowflake: MODERATE - Running free POC in finance dept

**Next Steps:**
Type 'stakeholders' to see buying committee details
Type 'risks' for deal risk assessment
Type 'meeting prep' to prepare for executive meetings"
```

---

## Step 8: Advanced Features

### 8.1 Enable Proactive Notifications:

Create Power Automate flow:
```
Trigger: When opportunity stage changes in Dynamics 365
Action: Call Account Intelligence risk_assessment
Condition: If win_probability < 50%
Action: Send Teams notification to account owner
```

### 8.2 Dashboard Integration:

Embed Power BI dashboard:
```
1. Create Power BI report with deal tracking data
2. Embed in Teams channel
3. Link Copilot actions to refresh dashboard
```

### 8.3 Multi-Language Support:

Configure in Copilot Studio:
```
Languages: English, Spanish, French, German
Translation: Azure Translator
Localization: Currency, date formats
```

---

## Troubleshooting

### Function Returns 500 Error:
```bash
# Check Function logs
az functionapp log tail --name your-function-app --resource-group your-resource-group

# Check Application Insights
# Azure Portal → Application Insights → Failures
```

### Authentication Issues:
```bash
# Verify Key Vault access
az keyvault secret show --name AZURE-OPENAI-KEY --vault-name your-keyvault

# Check Managed Identity
az functionapp identity show --name your-function-app --resource-group your-resource-group
```

### Copilot Not Responding:
1. Check Copilot Studio → Analytics → Errors
2. Verify HTTP action configuration
3. Test function endpoint directly with curl
4. Check function key hasn't expired

---

## Security Best Practices

✅ **Use Managed Identity** for Azure resources
✅ **Store secrets in Key Vault** (never hardcode)
✅ **Enable RBAC** on all resources
✅ **Enable audit logging** in Application Insights
✅ **Rotate keys** every 90 days
✅ **Restrict CORS** to Copilot Studio domains only
✅ **Enable TLS 1.2+** for all connections

---

## Cost Optimization

| Resource | Pricing Tier | Est. Monthly Cost |
|----------|-------------|-------------------|
| Azure Functions | Consumption | $0-20 |
| Azure OpenAI | Pay-per-token | $50-200 |
| Azure AI Search | Standard | $250 |
| Application Insights | Pay-per-GB | $10-50 |
| Key Vault | Standard | $3 |
| Storage Account | Standard LRS | $2 |
| **Total** | | **$315-525/month** |

**Cost Savings:**
- Cache account data (15min TTL)
- Batch Graph API requests
- Use cheaper GPT-3.5 for simple queries
- Enable consumption plan auto-scale

---

## Support

- **Documentation**: README_COPILOT_STUDIO_INTEGRATION.md
- **Issues**: GitHub Issues
- **Microsoft Learn**: https://learn.microsoft.com/copilot-studio
- **Azure Support**: https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade

---

## Next Steps

1. ✅ Deploy Azure Function
2. ✅ Configure secrets in Key Vault
3. ✅ Register plugin in Copilot Studio
4. ✅ Test in Microsoft Teams
5. 🎯 Train sales team on usage
6. 📊 Monitor analytics and improve
7. 🚀 Add more operations as needed

**Ready to supercharge your B2B sales with AI-powered account intelligence!** 🚀
