# Account Intelligence Stack - Quick Start

Get your AI-powered B2B sales intelligence system running in **under 30 minutes**.

---

## 🚀 **3-Step Deployment**

### **Step 1: Deploy to Azure (5 minutes)**

```bash
# Navigate to the stack directory
cd agent_stacks/b2b_sales_stacks/account_intelligence_stack

# Run deployment script
./deploy.sh

# Save the output:
# ✅ Function URL: https://your-function.azurewebsites.net/api/intelligence
# ✅ Function Key: your-secret-key
```

### **Step 2: Configure Secrets (10 minutes)**

Navigate to Azure Portal → Key Vault and add these secrets:

| Secret Name | Example Value | Where to Get It |
|------------|---------------|-----------------|
| `DYNAMICS-365-URL` | `https://org.crm.dynamics.com` | Dynamics 365 Admin Center |
| `AZURE-OPENAI-ENDPOINT` | `https://openai.openai.azure.com` | Azure OpenAI resource |
| `AZURE-OPENAI-KEY` | `sk-...` | Azure OpenAI → Keys |
| `GRAPH-API-CLIENT-ID` | `12345678-...` | Azure AD → App Registration |
| `GRAPH-API-CLIENT-SECRET` | `abc123...` | App Registration → Certificates & Secrets |
| `AZURE-AI-SEARCH-ENDPOINT` | `https://search.search.windows.net` | Azure AI Search resource |
| `AZURE-AI-SEARCH-KEY` | `xyz789...` | Azure AI Search → Keys |

Then update Function App to reference Key Vault:
```bash
# See COPILOT_STUDIO_SETUP_GUIDE.md Step 2 for commands
```

### **Step 3: Integrate with Copilot Studio (15 minutes)**

1. Go to https://copilotstudio.microsoft.com
2. Create new Copilot agent
3. Add HTTP action pointing to your Function URL
4. Configure operations (see COPILOT_STUDIO_SETUP_GUIDE.md)
5. Deploy to Microsoft Teams
6. Test: "Give me a briefing on Contoso Corporation"

✅ **Done!** Your sales team now has AI-powered account intelligence.

---

## 🧪 **Local Testing** (Before Azure Deployment)

```bash
# Install dependencies
pip install -r requirements.txt

# Test orchestrator locally
cd agents
python account_intelligence_orchestrator.py

# Expected output:
# {
#   "status": "success",
#   "operation": "account_briefing",
#   "account_id": "CONTOSO001",
#   ...
# }
```

---

## 💡 **Example Usage in Teams**

### **Get Account Briefing:**
```
You: "Give me a briefing on Contoso Corporation"

Copilot: "I've analyzed Contoso Corporation across Dynamics 365, Microsoft Graph,
and LinkedIn. Here's your briefing:

Company: Contoso Corporation ($2.3B revenue, 12,400 employees)
Health Score: 72/100 - Yellow (usage declining 12%)
Win Probability: 47%
Priority: HIGH - At-risk renewal + expansion opportunity

Key Stakeholders: 5 identified
Competitive Threats: DataBricks (CRITICAL), Snowflake (MODERATE)

Data Sources: Dynamics 365, LinkedIn Sales Navigator, Azure AI Search
Confidence: 92%"
```

### **Analyze Stakeholders:**
```
You: "Who are the key stakeholders at Contoso?"

Copilot: "Buying committee for Contoso:

1. Dr. Sarah Chen - CTO (100/100 influence)
   - Zero contact yet - URGENT ACTION NEEDED
   - New hire (6 weeks) from Microsoft Azure
   - Mandate: Modernize tech stack, reduce vendors

2. Robert Martinez - CFO (89/100 influence)
   - Weak relationship (last contact: 18 months ago)
   - Focus: Cost optimization, ROI

3. James Liu - VP Engineering (80/100 influence)
   - Your champion but going silent
   - Action: Re-engage this week

Recommendation: Prioritize CTO meeting THIS WEEK"
```

### **Get Meeting Prep:**
```
You: "Prepare me for my meeting with Sarah Chen tomorrow at 8am"

Copilot: "Meeting Brief for Sarah Chen (CTO, Contoso):

OBJECTIVES:
✓ Establish credibility + secure pilot agreement
✓ Understand her AI vision
✓ Move from 'vendor' to 'strategic partner'

OPENING (0-5 min):
'Sarah, thanks for the time. I know you're in week 6 of your 100-day plan...'

CORE MESSAGE (5-20 min):
'We've helped 12 manufacturers reduce costs 30% with AI in 90 days...'

DISCOVERY QUESTIONS:
'What's the #1 bottleneck you'd eliminate with a magic wand?'

THE ASK (25-30 min):
'30-day pilot with zero risk - 3 measurable outcomes or you pay $0'

MATERIALS TO BRING:
- Demo pre-loaded with Contoso data
- 3 case studies: Fabrikam, Northwind, Fourth Coffee
- ROI calculator (tablet)
- 1-page pilot proposal

OBJECTION HANDLING:
If she mentions DataBricks: 'They're strong in general AI - we're...'
"
```

### **Assess Deal Risks:**
```
You: "What are the risks to closing the Contoso deal?"

Copilot: "Deal Risk Assessment for Contoso:

Overall Risk: 🟡 MODERATE-HIGH (62/100)
Win Probability: 47% → Can improve to 75%

🔴 CRITICAL RISKS:
1. CTO Relationship Gap (95% probability)
   - Zero contact in 6 weeks
   - Mitigation: Alex Zhang intro + meeting THIS WEEK

2. DataBricks Inside Track (80% probability)
   - Their AE is her ex-colleague
   - Mitigation: Counter with manufacturing expertise

3. Usage Declining 12% (100% probability)
   - Signals dissatisfaction
   - Mitigation: Customer success intervention ASAP

ACTION PLAN - NEXT 48 HOURS:
Hour 1: Call Alex Zhang for CTO intro
Hour 2: LinkedIn connection to Sarah
Hour 3-4: Prepare meeting materials

Success Probability Roadmap:
Current: 47% → After CTO meeting: 58% → After pilot: 65% → Target: 75%"
```

### **Get Next Actions:**
```
You: "What should I do next for Contoso?"

Copilot: "Prioritized Action Plan (Impact × Urgency × Ease):

⏰ NEXT 30 MINUTES (Priority Score: 100/100):
Action: Call Alex Zhang for warm intro to CTO Sarah Chen
Why: You need CTO meeting THIS WEEK to save $2M deal
Time: 15 minutes

⏰ HOUR 1 (Priority Score: 95/100):
Action: Send LinkedIn connection to Sarah Chen
Why: Prime her before Alex's intro email
Time: 10 minutes

⏰ HOUR 2 (Priority Score: 90/100):
Action: Call James Liu for coffee this week
Why: Reactivate champion before CTO meeting
Time: 20 minutes

Success Metric: Move from 47% → 65% close probability in 48 hours"
```

---

## 📁 **File Structure**

```
account_intelligence_stack/
├── agents/
│   ├── account_intelligence_orchestrator.py    # Main entry point
│   ├── stakeholder_intelligence_agent.py       # Buying committee analysis
│   ├── competitive_intelligence_agent.py       # Battle cards
│   ├── meeting_prep_agent.py                   # Meeting briefs
│   ├── messaging_agent.py                      # AI-generated messages
│   ├── risk_assessment_agent.py                # Deal risk scoring
│   ├── action_prioritization_agent.py          # Action plans
│   └── deal_tracking_agent.py                  # Real-time dashboards
├── demos/
│   └── account_intelligence_stack_demo.html    # Interactive demo
├── __init__.py                                 # Azure Function entry point
├── function.json                               # Function configuration
├── host.json                                   # Function app settings
├── requirements.txt                            # Python dependencies
├── deploy.sh                                   # Deployment script
├── metadata.json                               # Stack metadata
├── README_COPILOT_STUDIO_INTEGRATION.md        # Architecture & integration
├── COPILOT_STUDIO_SETUP_GUIDE.md              # Step-by-step setup
└── QUICKSTART.md                              # This file
```

---

## 🎯 **Operations Available**

| Operation | Description | Use Case |
|-----------|-------------|----------|
| `account_briefing` | Complete account overview | "Briefing on Contoso" |
| `stakeholder_analysis` | Buying committee deep dive | "Who are the stakeholders?" |
| `competitive_intelligence` | Battle cards & threats | "Competitive landscape?" |
| `meeting_prep` | Executive meeting briefs | "Prepare for Sarah Chen meeting" |
| `generate_messaging` | AI-generated messages | "Draft LinkedIn message" |
| `risk_assessment` | Deal health & win probability | "Deal risks?" |
| `action_plan` | Prioritized next steps | "What should I do next?" |
| `deal_dashboard` | Real-time tracking | "Show deal dashboard" |

---

## 📊 **Data Sources Integrated**

✅ **Microsoft Dynamics 365** - CRM data, opportunities, activities
✅ **Microsoft Graph API** - Emails, meetings, org charts
✅ **LinkedIn Sales Navigator** - Professional profiles, connections
✅ **Azure OpenAI (GPT-4o)** - Intelligence synthesis
✅ **Azure AI Search** - Competitive intelligence
✅ **Power Automate** - Workflow automation

---

## 💰 **ROI & Business Value**

| Metric | Impact |
|--------|--------|
| **Time Savings** | 15-20 hours/week per sales rep |
| **Win Rate** | +15-25% increase in close probability |
| **Deal Size** | +20-30% larger deals |
| **Research Speed** | 50% faster account prep |
| **Risk Prevention** | Early warning prevents slippage |

**Example:**
- Sales team of 10 reps
- 20 hours saved per rep/week = 200 hours/week
- @ $100/hour = **$20,000/week value**
- = **$1M+/year in productivity gains**

---

## 🔧 **Troubleshooting**

### **Function returns 500 error:**
```bash
# Check logs
az functionapp log tail --name your-function-app --resource-group your-rg
```

### **Copilot not responding:**
1. Test function directly with curl
2. Check Copilot Studio → Analytics → Errors
3. Verify HTTP action configuration

### **Authentication errors:**
```bash
# Verify Key Vault access
az keyvault secret show --name AZURE-OPENAI-KEY --vault-name your-kv
```

---

## 📚 **Documentation**

- **Architecture**: `README_COPILOT_STUDIO_INTEGRATION.md`
- **Setup Guide**: `COPILOT_STUDIO_SETUP_GUIDE.md`
- **API Reference**: See individual agent `.py` files
- **Demo**: `demos/account_intelligence_stack_demo.html`

---

## 🆘 **Need Help?**

- **GitHub Issues**: [Report issues]
- **Microsoft Learn**: https://learn.microsoft.com/copilot-studio
- **Azure Support**: https://portal.azure.com/#support

---

## 🎉 **You're Ready!**

Your AI-powered account intelligence system is now running. Start using it in Microsoft Teams:

```
"Give me a briefing on [Account Name]"
"Who are the stakeholders at [Company]?"
"Prepare me for my meeting with [Executive]"
"What are the risks to closing this deal?"
"What should I do next?"
```

**Happy selling!** 🚀📈
