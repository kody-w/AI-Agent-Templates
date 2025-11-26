# Local Testing Guide - Account Intelligence Stack

## Quick Start (30 seconds)

### Step 1: Start the Server
```bash
cd agent_stacks/b2b_sales_stacks/account_intelligence_stack
python3 local_server.py
```

You should see:
```
================================================================================
🚀 ACCOUNT INTELLIGENCE STACK - LOCAL TEST SERVER
================================================================================

Mode: MOCK (no API credentials required)
Version: 2.0.0

✅ Server is ready!
   Open http://localhost:5001 in your browser to start testing
```

### Step 2: Open the Test Interface

**Option A - Web Browser:**
1. Open your browser
2. Navigate to: http://localhost:5001
3. Click any operation button to test

**Option B - Command Line Testing:**
```bash
# Test health endpoint
curl http://localhost:5001/health

# Test account briefing
curl -X POST http://localhost:5001/intelligence \
  -H "Content-Type: application/json" \
  -d '{"operation": "account_briefing", "account_id": "CONTOSO001"}'
```

---

## What You Can Test

The test interface provides **8 operations** with realistic mock data:

### 1. **Account Briefing**
Get comprehensive overview of Contoso Corporation
- Company details (12,400 employees, $2.3B revenue)
- Health score (72/100 - Yellow)
- 5 key stakeholders
- 2 competitive threats
- $2.1M opportunity

### 2. **Stakeholder Analysis**
Analyze buying committee with influence scores
- Dr. Sarah Chen (CTO) - Influence: 100/100 - **ZERO CONTACT YET**
- Robert Martinez (CFO) - Influence: 94/100 - Weak relationship
- James Liu (VP Eng) - Influence: 85/100 - Your champion
- Michelle Park (Procurement) - Influence: 75/100
- David Kumar (VP Ops) - Influence: 70/100

### 3. **Competitive Intelligence**
Detect active competitive threats
- **DataBricks** - CRITICAL threat (CTO's ex-colleague is their AE)
- **Snowflake** - MODERATE threat (running free POC)
- Battle cards with strengths/weaknesses
- Win/loss analysis (61% win rate vs. DataBricks)

### 4. **Meeting Preparation**
Generate executive meeting brief for Sarah Chen
- Opening script
- 4 discovery questions
- Objection handling
- Next steps

### 5. **Message Generation**
Create personalized LinkedIn connection request
- 287 characters (optimized length)
- 85% acceptance rate prediction
- References her recent post about AI + manufacturing

### 6. **Risk Assessment**
Assess deal risks and win probability
- Deal health: 62/100
- Win probability: 47% → 75% (with mitigation)
- 3 CRITICAL risks identified
- Mitigation strategies for each

### 7. **Action Plan**
Prioritized 48-hour action plan
- Next 30 minutes: Call Alex Zhang for warm CTO intro
- Hour 1: Send LinkedIn connection to Sarah
- Hour 2: Reactivate champion James Liu
- Hour 3-4: Customer success audit
- 10 total actions with priority scores

### 8. **Deal Dashboard**
Real-time deal tracking metrics
- Milestone progress (Week 1-6)
- Stakeholder engagement scorecard
- Leading indicators (green/yellow/red signals)
- Revenue impact on quota (26% of annual target)

---

## Test Interface Features

The web interface (`http://localhost:5001`) provides:

✅ **Visual Operation Buttons** - Click any operation to run
✅ **Real-Time Server Status** - Auto-checks every 5 seconds
✅ **JSON Syntax Highlighting** - Color-coded results
✅ **Loading States** - Spinners during operations
✅ **Error Display** - Clear error messages
✅ **Metadata Display** - Operation, status, confidence scores
✅ **Account Info Box** - Shows Contoso Corporation details
✅ **Quick Start Guide** - Embedded instructions

---

## Mock Data Story

All 8 operations use **interconnected mock data** telling a coherent story:

**Company:** Contoso Corporation
**Industry:** Manufacturing & Industrial Technology
**Size:** 12,400 employees, $2.3B revenue
**Current ARR:** $340K
**Deal Value:** $2.1M (renewal + expansion)
**Close Date:** January 20, 2025 (41 days)
**Win Probability:** 47%
**Health Score:** 72/100 (YELLOW)

**Critical Situation:**
- New CTO (Dr. Sarah Chen) started 6 weeks ago - **ZERO CONTACT**
- She will re-evaluate ALL vendors
- DataBricks already submitted proposal ($1.8M)
- Their AE is Sarah's ex-Microsoft colleague
- Usage declining 12%
- Champion (James Liu) going silent

**Action Required:**
- Get warm intro to CTO THIS WEEK
- Reactivate champion
- Re-engage CFO (18 months since last contact)
- Counter DataBricks with manufacturing expertise

---

## API Endpoints

### Health Check
```bash
GET http://localhost:5001/health
```

**Response:**
```json
{
  "status": "healthy",
  "mode": "mock",
  "server": "Account Intelligence Stack - Local Test Server",
  "version": "2.0.0"
}
```

### Intelligence Operations
```bash
POST http://localhost:5001/intelligence
Content-Type: application/json

{
  "operation": "account_briefing",
  "account_id": "CONTOSO001",
  "contact_id": "CONT001",     // optional
  "opportunity_id": "OPP001",  // optional
  "context": {}                // optional
}
```

**Response:**
```json
{
  "status": "success",
  "operation": "account_briefing",
  "account_id": "CONTOSO001",
  "timestamp": "2025-10-25T10:48:49.654640",
  "data": { ... },
  "sources": ["Dynamics 365", "LinkedIn Sales Navigator", ...],
  "confidence": 0.92
}
```

### List Operations
```bash
GET http://localhost:5001/operations
```

### Get Metadata
```bash
GET http://localhost:5001/metadata
```

---

## Command Line Examples

### Run All 8 Operations
```bash
# 1. Account Briefing
curl -X POST http://localhost:5001/intelligence \
  -H "Content-Type: application/json" \
  -d '{"operation": "account_briefing", "account_id": "CONTOSO001"}'

# 2. Stakeholder Analysis
curl -X POST http://localhost:5001/intelligence \
  -H "Content-Type: application/json" \
  -d '{"operation": "stakeholder_analysis", "account_id": "CONTOSO001"}'

# 3. Competitive Intelligence
curl -X POST http://localhost:5001/intelligence \
  -H "Content-Type: application/json" \
  -d '{"operation": "competitive_intelligence", "account_id": "CONTOSO001"}'

# 4. Meeting Preparation
curl -X POST http://localhost:5001/intelligence \
  -H "Content-Type: application/json" \
  -d '{"operation": "meeting_prep", "account_id": "CONTOSO001", "contact_id": "CONT001", "context": {"meeting_type": "executive_briefing"}}'

# 5. Message Generation
curl -X POST http://localhost:5001/intelligence \
  -H "Content-Type: application/json" \
  -d '{"operation": "generate_messaging", "account_id": "CONTOSO001", "contact_id": "CONT001", "context": {"message_type": "linkedin_connection"}}'

# 6. Risk Assessment
curl -X POST http://localhost:5001/intelligence \
  -H "Content-Type: application/json" \
  -d '{"operation": "risk_assessment", "account_id": "CONTOSO001", "opportunity_id": "OPP001"}'

# 7. Action Plan
curl -X POST http://localhost:5001/intelligence \
  -H "Content-Type: application/json" \
  -d '{"operation": "action_plan", "account_id": "CONTOSO001", "context": {"timeframe": "48_hours"}}'

# 8. Deal Dashboard
curl -X POST http://localhost:5001/intelligence \
  -H "Content-Type: application/json" \
  -d '{"operation": "deal_dashboard", "account_id": "CONTOSO001", "opportunity_id": "OPP001"}'
```

---

## Python Testing Script

```python
import requests
import json

SERVER_URL = "http://localhost:5001"

# Test account briefing
response = requests.post(
    f"{SERVER_URL}/intelligence",
    json={
        "operation": "account_briefing",
        "account_id": "CONTOSO001"
    }
)

result = response.json()
print(json.dumps(result, indent=2))
```

---

## Troubleshooting

### Port Already in Use
If you see `Address already in use` error:

**On macOS:**
- Disable AirPlay Receiver: System Preferences → Sharing → Uncheck "AirPlay Receiver"

**Or use different port:**
1. Edit `local_server.py`: Change `port=5001` to `port=8000`
2. Edit `test_interface.html`: Change `SERVER_URL = 'http://localhost:5001'` to `8000`

### Server Not Starting
```bash
# Check if Python 3 is installed
python3 --version

# Check if Flask is installed
pip3 install flask flask-cors

# Make sure you're in the correct directory
pwd
# Should show: .../account_intelligence_stack
```

### Browser Shows "Server Offline"
1. Make sure `python3 local_server.py` is running
2. Check terminal for errors
3. Try refreshing browser (Cmd+R / Ctrl+R)
4. Check that port 5001 is not blocked by firewall

---

## What's Happening Behind the Scenes

### Request Flow
```
Browser/CLI → Flask Server → Orchestrator → Agent → Connectors → Mock Data
```

### In Mock Mode:
1. **No API credentials needed** - All connectors return mock data
2. **Instant responses** - No network calls
3. **Realistic data** - Comprehensive, interconnected scenarios
4. **100% functional** - All 7 agents working

### Code Path Example (Account Briefing):
```
local_server.py (Flask endpoint)
  → AccountIntelligenceOrchestrator.perform(operation="account_briefing")
    → StakeholderIntelligenceAgent.perform()
      → CRMConnector.get_contacts() → Returns mock Contoso contacts
      → GraphConnector.get_email_interactions() → Returns mock email data
      → LinkedInConnector.get_profile() → Returns mock LinkedIn data
    → CompetitiveIntelligenceAgent.perform()
      → AzureSearchConnector.search_competitor() → Returns mock DataBricks data
    → RiskAssessmentAgent.perform()
      → CRMConnector.get_opportunities() → Returns mock deal data
    → AzureOpenAIConnector.synthesize_briefing()
      → Returns comprehensive synthesis
  → Returns JSON response to browser
```

---

## Next Steps

### Already Working ✅
- [x] 7 AI agents fully functional
- [x] 5 data source connectors
- [x] Mock mode for local testing
- [x] Comprehensive test suite (15/15 tests passing)
- [x] Web test interface
- [x] Local Flask server

### To Deploy to Production
1. **Set environment variables:**
   ```bash
   export MODE=production
   export CRM_SYSTEM=salesforce  # or dynamics_365, monday, hubspot
   export SALESFORCE_INSTANCE_URL=...
   export AZURE_OPENAI_ENDPOINT=...
   # etc.
   ```

2. **Implement production API calls** in connector stubs:
   - `connectors/crm_connector.py` (lines 346-448)
   - `connectors/graph_connector.py` (lines 297-332)
   - `connectors/linkedin_connector.py` (lines 285-311)
   - `connectors/azure_openai_connector.py` (lines 256-295)
   - `connectors/azure_search_connector.py` (lines 298-325)

3. **Deploy to Azure:**
   ```bash
   ./deploy.sh
   ```

4. **Integrate with Copilot Studio:**
   - See `COPILOT_STUDIO_SETUP_GUIDE.md`

---

## Resources

- **Architecture:** `CONNECTOR_ARCHITECTURE.md`
- **Integration Status:** `CONNECTOR_INTEGRATION_STATUS.md`
- **Implementation Summary:** `IMPLEMENTATION_COMPLETE.md`
- **Copilot Studio Setup:** `COPILOT_STUDIO_SETUP_GUIDE.md`
- **Quick Start:** `QUICKSTART.md`

---

## Support

**Test Results:**
- Comprehensive test suite: `python tests/test_all_agents.py`
- 15/15 tests passing (100%)
- All 8 operations validated

**Documentation:**
All documentation is in the `account_intelligence_stack/` directory.

**Happy Testing!** 🚀
