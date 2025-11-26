# Testing Guide - Deal Progression Agent Stack

## Overview
This guide provides comprehensive testing instructions for all 10 agents in the Deal Progression Stack using a Dynamics 365 trial instance with sample data.

## Prerequisites

### 1. Dynamics 365 Sales Trial Setup
1. Sign up for D365 Sales trial: https://dynamics.microsoft.com/sales/free-trial/
2. Complete the trial signup process (requires business email)
3. Enable sample data: **Settings > Data Management > Sample Data > Install Sample Data**
4. Wait 5-10 minutes for sample data to populate

### 2. Azure AD App Registration
1. Go to Azure Portal: https://portal.azure.com
2. Navigate to **Azure Active Directory > App registrations > New registration**
3. Configure app:
   - Name: `D365 Deal Progression Agents`
   - Supported account types: `Accounts in this organizational directory only`
   - Redirect URI: Leave blank
4. Click **Register**
5. Note the **Application (client) ID** and **Directory (tenant) ID**
6. Create client secret:
   - Go to **Certificates & secrets > New client secret**
   - Description: `Agent Access`
   - Expires: 12 months
   - Click **Add** and copy the **Value** immediately (shown only once)

### 3. Grant API Permissions
1. In your app registration, go to **API permissions**
2. Click **Add a permission > Dynamics CRM**
3. Select **Delegated permissions**
4. Check **user_impersonation**
5. Click **Add permissions**
6. Click **Grant admin consent for [your organization]**

### 4. Environment Variables Setup

Create a `.env` file in the `deal_progression_stack` directory:

```bash
# Dynamics 365 Configuration
DYNAMICS_365_CLIENT_ID=your_application_client_id
DYNAMICS_365_CLIENT_SECRET=your_client_secret_value
DYNAMICS_365_TENANT_ID=your_tenant_id
DYNAMICS_365_RESOURCE=https://yourorg.crm.dynamics.com

# Example:
# DYNAMICS_365_CLIENT_ID=12345678-1234-1234-1234-123456789012
# DYNAMICS_365_CLIENT_SECRET=abcdef~ABCdefG123456789_x.y-z
# DYNAMICS_365_TENANT_ID=87654321-4321-4321-4321-210987654321
# DYNAMICS_365_RESOURCE=https://org123456.crm.dynamics.com
```

To find your D365 instance URL:
1. Log into your D365 trial
2. Look at the browser URL bar: `https://[yourorg].crm.dynamics.com/...`
3. Use `https://[yourorg].crm.dynamics.com` (without the trailing path)

### 5. Install Python Dependencies

```bash
cd agent_stacks/b2b_sales_stacks/deal_progression_stack
pip install -r requirements.txt
```

Create `requirements.txt` if it doesn't exist:
```
requests>=2.28.0
msal>=1.20.0
python-dotenv>=0.19.0
```

## Testing Each Agent

### Agent 1: Stalled Deal Detection Agent

**Purpose**: Identify deals with no activity in the last 14+ days

**Test Command**:
```bash
python agents/stalled_deal_detection_agent.py
```

**Expected Output**:
```json
{
  "status": "success",
  "message": "Found 12 stalled deals (no activity in 14+ days)",
  "data": {
    "stalled_deals": [
      {
        "opportunity_id": "guid-here",
        "name": "Contoso Electronics Deal",
        "value": 250000,
        "value_formatted": "$250,000",
        "days_stalled": 21,
        "current_stage": "Proposal",
        "last_activity": "2025-10-04",
        "owner": "John Smith",
        "account": "Contoso Electronics",
        "close_probability": 60,
        "risk_level": "High"
      }
    ],
    "summary": {
      "total_stalled": 12,
      "total_value_at_risk": 1450000,
      "avg_days_stalled": 18.5,
      "risk_breakdown": {
        "Critical": 2,
        "High": 4,
        "Medium": 5,
        "Low": 1
      }
    }
  }
}
```

**Verification Checklist**:
- [ ] Returns list of stalled deals from D365
- [ ] Calculates days since last activity correctly
- [ ] Assigns appropriate risk levels
- [ ] Provides summary metrics
- [ ] Handles empty result set gracefully

**D365 Query Used**:
```
GET /api/data/v9.2/opportunities?
$filter=statecode eq 0 and modifiedon lt 2025-10-11T00:00:00Z
$expand=customerid_account($select=name),ownerid($select=fullname)
$select=name,estimatedvalue,closeprobability,stepname,modifiedon
$orderby=modifiedon asc
$top=50
```

---

### Agent 2: Next Best Action Agent

**Purpose**: Recommend optimal next actions for a specific opportunity

**Test Command**:
```bash
python agents/next_best_action_agent.py
```

**Test with Parameters** (requires modification of `__main__` block):
```python
if __name__ == "__main__":
    agent = NextBestActionAgent()
    result = agent.perform(
        opportunity_name="Fabrikam Cloud Migration",
        current_stage="Develop"
    )
    print(json.dumps(result, indent=2))
```

**Expected Output**:
```json
{
  "status": "success",
  "message": "Generated 5 action recommendations for Fabrikam Cloud Migration",
  "data": {
    "opportunity_name": "Fabrikam Cloud Migration",
    "current_stage": "Develop",
    "estimated_value": "$425,000",
    "close_probability": 65,
    "recommended_actions": [
      {
        "action": "Complete Technical deep dive",
        "priority": "High",
        "reasoning": "Required activity for Develop stage not yet completed",
        "confidence": 0.92,
        "expected_impact": "Enables stage progression",
        "category": "Stage Requirement"
      },
      {
        "action": "Schedule executive briefing with C-level stakeholders",
        "priority": "High",
        "reasoning": "Deal value $425,000 requires executive sponsorship",
        "confidence": 0.89,
        "expected_impact": "Increase win probability by 15-20%",
        "category": "Stakeholder Engagement"
      }
    ],
    "stage_requirements": {
      "completed": ["Product demo"],
      "missing": ["Technical deep dive", "Stakeholder meeting", "Security review"]
    }
  }
}
```

**Verification Checklist**:
- [ ] Generates relevant recommendations based on stage
- [ ] Identifies missing stage activities
- [ ] Prioritizes actions appropriately
- [ ] Provides clear reasoning and expected impact
- [ ] Handles different stages (Qualify, Develop, Propose, Close)

---

### Agent 3: Deal Health Score Agent

**Purpose**: Calculate comprehensive health score (0-100)

**Test Command**:
```bash
python agents/deal_health_score_agent.py
```

**Expected Output**:
```json
{
  "status": "success",
  "message": "Health score calculated: 76/100 (Good)",
  "data": {
    "opportunity_name": "Northwind SaaS Implementation",
    "health_score": 76,
    "health_rating": "Good",
    "trend": "Improving",
    "factors": {
      "engagement": {
        "score": 82,
        "weight": 0.30,
        "indicators": {
          "activities_last_30_days": 15,
          "stakeholder_meetings": 4,
          "response_rate": "85%"
        }
      },
      "momentum": {
        "score": 71,
        "weight": 0.25,
        "indicators": {
          "days_in_current_stage": 12,
          "stage_progression_rate": "Normal",
          "last_activity": "2 days ago"
        }
      },
      "alignment": {
        "score": 80,
        "weight": 0.20,
        "indicators": {
          "budget_confirmed": true,
          "timeline_fit": "Q4 2025"
        }
      },
      "completeness": {
        "score": 65,
        "weight": 0.15,
        "indicators": {
          "activities_complete": "13/20"
        }
      },
      "risk": {
        "score": 85,
        "weight": 0.10,
        "indicators": {
          "competitors_present": 1,
          "stalled_days": 0
        }
      }
    }
  }
}
```

**Verification Checklist**:
- [ ] Calculates score from 0-100
- [ ] Provides breakdown across 5 factors
- [ ] Weights factors appropriately
- [ ] Assigns health rating (Excellent/Good/Fair/Poor/Critical)
- [ ] Determines trend (Improving/Stable/Declining)

---

### Agent 4: Pipeline Velocity Agent

**Purpose**: Measure deal progression speed

**Test Command**:
```bash
python agents/pipeline_velocity_agent.py
```

**Expected Output**:
```json
{
  "status": "success",
  "message": "Pipeline velocity analysis complete for last 90 days",
  "data": {
    "time_period": "Last 90 days",
    "deals_analyzed": 127,
    "pipeline_metrics": {
      "average_deal_cycle": 45,
      "current_velocity": "2.3 stages/month",
      "trend": "15% faster than previous period"
    },
    "stage_performance": [
      {
        "stage": "Qualify",
        "avg_duration_days": 7,
        "conversion_rate": 0.85,
        "status": "Healthy"
      },
      {
        "stage": "Develop",
        "avg_duration_days": 18,
        "conversion_rate": 0.72,
        "status": "Bottleneck",
        "recommendation": "Increase demo resources"
      },
      {
        "stage": "Propose",
        "avg_duration_days": 12,
        "conversion_rate": 0.68,
        "status": "Healthy"
      },
      {
        "stage": "Close",
        "avg_duration_days": 8,
        "conversion_rate": 0.91,
        "status": "Excellent"
      }
    ]
  }
}
```

**Verification Checklist**:
- [ ] Calculates average deal cycle time
- [ ] Identifies stage bottlenecks
- [ ] Calculates conversion rates per stage
- [ ] Provides actionable recommendations
- [ ] Compares to previous period

---

### Agent 5: Stakeholder Engagement Agent

**Purpose**: Analyze contact engagement patterns

**Test Command**:
```bash
python agents/stakeholder_engagement_agent.py
```

**Expected Output**:
```json
{
  "status": "success",
  "message": "Analyzed engagement for 4 stakeholders",
  "data": {
    "opportunity_name": "Adventure Works Platform Deal",
    "stakeholders": [
      {
        "name": "Sarah Johnson",
        "title": "VP of Operations",
        "role": "Economic Buyer",
        "engagement_level": "High",
        "total_interactions": 12,
        "last_contact": "2025-10-23",
        "days_since_contact": 2,
        "activities": {
          "meetings": 4,
          "emails": 6,
          "calls": 2
        },
        "sentiment": "Positive",
        "influence_score": 95
      },
      {
        "name": "Robert Martinez",
        "title": "CFO",
        "role": "Financial Buyer",
        "engagement_level": "Low",
        "total_interactions": 2,
        "last_contact": "2025-09-15",
        "days_since_contact": 40,
        "activities": {
          "meetings": 1,
          "emails": 1,
          "calls": 0
        },
        "sentiment": "Unknown",
        "influence_score": 92,
        "alert": "Key decision maker with low engagement - 40 days since contact"
      }
    ],
    "engagement_summary": {
      "total_stakeholders": 4,
      "highly_engaged": 2,
      "at_risk": 1,
      "key_contact_gaps": ["CFO needs engagement"]
    }
  }
}
```

**Verification Checklist**:
- [ ] Identifies all stakeholders for opportunity
- [ ] Calculates engagement levels
- [ ] Tracks interaction history
- [ ] Flags at-risk stakeholders
- [ ] Provides influence scores

---

### Agent 6: Competitor Intelligence Agent

**Purpose**: Analyze competitive landscape

**Test Command**:
```bash
python agents/competitor_intelligence_agent.py
```

**Expected Output**:
```json
{
  "status": "success",
  "message": "Competitive intelligence analysis complete",
  "data": {
    "competitive_landscape": {
      "total_deals_with_competition": 34,
      "total_competitive_value": 8500000
    },
    "competitor_analysis": [
      {
        "competitor_name": "Salesforce",
        "deals_present": 12,
        "total_value": 3200000,
        "win_rate_against": 0.45,
        "avg_deal_size": 266667,
        "common_strengths": ["Brand recognition", "Ecosystem"],
        "common_weaknesses": ["Price", "Complexity"],
        "our_positioning": "Better TCO, faster implementation"
      }
    ],
    "active_competitive_deals": [
      {
        "opportunity_name": "Contoso Cloud Suite",
        "value": 450000,
        "stage": "Proposal",
        "competitors": ["Salesforce", "Microsoft"],
        "competitive_strategy": "Emphasize integration capabilities and TCO",
        "recommended_actions": [
          "Share TCO calculator",
          "Schedule technical comparison demo"
        ]
      }
    ]
  }
}
```

**Verification Checklist**:
- [ ] Identifies competitors across pipeline
- [ ] Calculates win rates
- [ ] Provides battle strategies
- [ ] Recommends specific actions
- [ ] Shows competitor strengths/weaknesses

---

### Agent 7: Deal Risk Assessment Agent

**Purpose**: Comprehensive risk analysis

**Test Command**:
```bash
python agents/deal_risk_assessment_agent.py
```

**Expected Output**:
```json
{
  "status": "success",
  "message": "Risk assessment complete: High risk level with 6 risks",
  "data": {
    "opportunity_name": "Fabrikam Digital Transformation",
    "overall_risk_level": "High",
    "risk_score": 72,
    "total_identified_risks": 6,
    "risk_categories": {
      "timeline_risks": {
        "severity": "High",
        "score": 85,
        "risks": [
          {
            "risk": "Close date in 15 days",
            "impact": "High",
            "probability": 0.9,
            "mitigation": "Expedite proposal review, schedule urgency call"
          }
        ]
      },
      "engagement_risks": {
        "severity": "Medium",
        "score": 65,
        "risks": [
          {
            "risk": "No activities in 12 days",
            "impact": "High",
            "probability": 0.7,
            "mitigation": "Immediate outreach to primary contact"
          }
        ]
      }
    },
    "recommended_immediate_actions": [
      "Schedule call with decision maker within 48 hours",
      "Send formal quote with value justification"
    ]
  }
}
```

**Verification Checklist**:
- [ ] Analyzes 6 risk categories
- [ ] Assigns severity levels
- [ ] Calculates probability and impact
- [ ] Provides specific mitigation strategies
- [ ] Prioritizes immediate actions

---

### Agent 8: Revenue Forecast Agent

**Purpose**: Analyze forecast accuracy

**Test Command**:
```bash
python agents/revenue_forecast_agent.py
```

**Expected Output**:
```json
{
  "status": "success",
  "message": "Forecast analysis complete for Q4 2025",
  "data": {
    "forecast_period": "Q4 2025",
    "forecast_summary": {
      "total_pipeline_value": 4850000,
      "weighted_forecast": 2425000,
      "adjusted_forecast": 2180000,
      "confidence_level": 0.78,
      "forecast_accuracy": {
        "last_quarter": 0.82,
        "trend": "Improving"
      }
    },
    "deal_predictions": [
      {
        "opportunity_name": "Contoso Enterprise Suite",
        "estimated_value": 350000,
        "current_close_probability": 75,
        "estimated_close_date": "2025-11-15",
        "predicted_close_date": "2025-12-03",
        "prediction_confidence": 0.84,
        "slip_risk": "Medium",
        "adjusted_probability": 68
      }
    ],
    "accuracy_insights": [
      {
        "insight": "Deals >$500K slip 3 weeks on average",
        "sample_size": 23,
        "confidence": 0.89
      }
    ],
    "recommendations": [
      "Adjust Q4 forecast down by 10% based on historical patterns"
    ]
  }
}
```

**Verification Checklist**:
- [ ] Calculates weighted forecast
- [ ] Predicts slip rates
- [ ] Provides adjusted close dates
- [ ] Generates insights from historical patterns
- [ ] Recommends forecast adjustments

---

### Agent 9: Activity Gap Agent

**Purpose**: Identify missing critical activities

**Test Command**:
```bash
python agents/activity_gap_agent.py
```

**Expected Output**:
```json
{
  "status": "success",
  "message": "Activity gap analysis complete: 3 gaps identified",
  "data": {
    "opportunity_name": "Wide World Importers CRM",
    "current_stage": "Develop",
    "completeness_score": 65,
    "required_activities": {
      "qualify_stage": {
        "status": "Complete",
        "completion_rate": 1.0,
        "activities": [
          {"activity": "Discovery call", "completed": true, "date": "2025-09-15"}
        ]
      },
      "develop_stage": {
        "status": "In Progress",
        "completion_rate": 0.67,
        "activities": [
          {"activity": "Product demo", "completed": true, "date": "2025-10-01"},
          {"activity": "Stakeholder meeting", "completed": false, "required_by": "2025-10-28"}
        ],
        "missing_critical": ["Stakeholder meeting", "Security review"]
      }
    },
    "gaps_identified": [
      {
        "gap": "No stakeholder alignment meeting scheduled",
        "stage": "Develop",
        "priority": "High",
        "impact": "Cannot advance to Propose without stakeholder buy-in",
        "recommendation": "Schedule meeting with VP and Director-level stakeholders"
      }
    ],
    "recommended_timeline": [
      {"date": "2025-10-26", "action": "Schedule stakeholder meeting"},
      {"date": "2025-11-05", "action": "Ready to advance to Propose stage"}
    ]
  }
}
```

**Verification Checklist**:
- [ ] Identifies missing activities by stage
- [ ] Calculates completeness score
- [ ] Provides completion timeline
- [ ] Prioritizes gaps by impact
- [ ] Gives actionable recommendations

---

### Agent 10: Win Probability Agent

**Purpose**: Calculate AI-driven win probability

**Test Command**:
```bash
python agents/win_probability_agent.py
```

**Expected Output**:
```json
{
  "status": "success",
  "message": "Win probability calculated: 58% (adjusted from 70%)",
  "data": {
    "opportunity_name": "Tailspin Toys Digital Platform",
    "sales_rep_probability": 70,
    "calculated_win_probability": 58,
    "confidence_interval": {
      "low": 51,
      "high": 65
    },
    "probability_factors": {
      "deal_characteristics": {
        "contribution": 0.15,
        "score": 72,
        "factors": {
          "deal_size": {
            "value": 425000,
            "category": "Medium Enterprise",
            "historical_win_rate": 0.68,
            "impact": "Positive"
          }
        }
      },
      "sales_process": {
        "contribution": 0.30,
        "score": 55
      },
      "engagement_metrics": {
        "contribution": 0.25,
        "score": 48
      }
    },
    "risk_adjustments": [
      {
        "risk": "Below-average stakeholder engagement",
        "probability_impact": -8,
        "reasoning": "Only 1 of 3 key decision makers engaged"
      }
    ],
    "recommendations_to_improve": [
      {
        "action": "Engage remaining decision makers",
        "potential_impact": "+10-15% probability",
        "priority": "High"
      }
    ],
    "similar_historical_deals": {
      "sample_size": 23,
      "won": 13,
      "lost": 10,
      "win_rate": 0.57
    }
  }
}
```

**Verification Checklist**:
- [ ] Calculates data-driven probability
- [ ] Shows variance from sales rep estimate
- [ ] Provides confidence interval
- [ ] Breaks down factors with weights
- [ ] Gives recommendations to improve probability
- [ ] Shows similar historical deals

---

## Common Issues and Troubleshooting

### Issue 1: Authentication Error

**Error**: `Failed to acquire token: AADSTS7000215`

**Solution**:
- Verify client ID, client secret, and tenant ID are correct
- Ensure client secret hasn't expired
- Check that app registration has Dynamics CRM permissions
- Confirm admin consent was granted

### Issue 2: D365 Connection Timeout

**Error**: `Request timed out after 30 seconds`

**Solution**:
- Check internet connection
- Verify D365 instance URL is correct (should end with `.crm.dynamics.com`)
- Ensure D365 trial hasn't expired
- Try with a smaller query (use `$top=5` parameter)

### Issue 3: No Sample Data

**Error**: `Query returns empty results`

**Solution**:
- Log into D365 portal
- Go to Settings > Data Management > Sample Data
- Click "Install Sample Data" and wait 5-10 minutes
- Refresh and verify opportunities exist in Sales > Opportunities

### Issue 4: Permission Denied

**Error**: `403 Forbidden` or `Insufficient privileges`

**Solution**:
- Ensure user account has Sales Manager or System Administrator role
- Verify API permissions include `user_impersonation`
- Check that admin consent was granted
- Try logging into D365 web interface to verify access

### Issue 5: Module Import Error

**Error**: `ModuleNotFoundError: No module named 'msal'`

**Solution**:
```bash
pip install -r requirements.txt
# or individually:
pip install msal requests python-dotenv
```

---

## Performance Testing

### Load Testing
Test with increasing data volumes:

1. **Small dataset** (10 opportunities):
   ```python
   result = agent.perform(max_results=10)
   ```

2. **Medium dataset** (50 opportunities):
   ```python
   result = agent.perform(max_results=50)
   ```

3. **Large dataset** (200 opportunities):
   ```python
   result = agent.perform(max_results=200)
   ```

**Expected Performance**:
- Small: < 2 seconds
- Medium: < 5 seconds
- Large: < 15 seconds

### Concurrent Testing
Test multiple agents simultaneously:

```python
import concurrent.futures

agents = [
    StalledDealDetectionAgent(),
    PipelineVelocityAgent(),
    CompetitorIntelligenceAgent()
]

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(agent.perform) for agent in agents]
    results = [f.result() for f in futures]
```

---

## Integration Testing

### Test with Real D365 Workflow

1. Create a new opportunity in D365
2. Add activities (meetings, tasks)
3. Add stakeholders (contacts)
4. Add competitors
5. Run agents and verify they detect the new data

### Test Data Modification

1. Update an opportunity's stage in D365
2. Run agents to verify they reflect the change
3. Add new activity to stalled deal
4. Verify stalled deal agent no longer flags it

---

## Automated Test Suite

Create `test_all_agents.py`:

```python
import json
from agents.stalled_deal_detection_agent import StalledDealDetectionAgent
from agents.next_best_action_agent import NextBestActionAgent
from agents.deal_health_score_agent import DealHealthScoreAgent
from agents.pipeline_velocity_agent import PipelineVelocityAgent
from agents.stakeholder_engagement_agent import StakeholderEngagementAgent
from agents.competitor_intelligence_agent import CompetitorIntelligenceAgent
from agents.deal_risk_assessment_agent import DealRiskAssessmentAgent
from agents.revenue_forecast_agent import RevenueForecastAgent
from agents.activity_gap_agent import ActivityGapAgent
from agents.win_probability_agent import WinProbabilityAgent

def test_agent(agent_class, agent_name, **kwargs):
    """Test a single agent"""
    print(f"\n{'='*60}")
    print(f"Testing: {agent_name}")
    print(f"{'='*60}")

    try:
        agent = agent_class()
        result = agent.perform(**kwargs)

        assert result['status'] == 'success', f"Agent failed: {result.get('message')}"
        assert 'data' in result, "Missing data in result"

        print(f"✓ {agent_name} passed")
        print(f"  Message: {result['message']}")
        return True

    except Exception as e:
        print(f"✗ {agent_name} failed: {str(e)}")
        return False

def main():
    """Run all agent tests"""
    print("="*60)
    print("Deal Progression Agent Stack - Test Suite")
    print("="*60)

    tests = [
        (StalledDealDetectionAgent, "Stalled Deal Detection", {}),
        (NextBestActionAgent, "Next Best Action", {"opportunity_name": "Test Deal", "current_stage": "Develop"}),
        (DealHealthScoreAgent, "Deal Health Score", {"opportunity_name": "Test Deal"}),
        (PipelineVelocityAgent, "Pipeline Velocity", {}),
        (StakeholderEngagementAgent, "Stakeholder Engagement", {"opportunity_name": "Test Deal"}),
        (CompetitorIntelligenceAgent, "Competitor Intelligence", {}),
        (DealRiskAssessmentAgent, "Deal Risk Assessment", {"opportunity_name": "Test Deal"}),
        (RevenueForecastAgent, "Revenue Forecast", {}),
        (ActivityGapAgent, "Activity Gap Identifier", {"opportunity_name": "Test Deal", "current_stage": "Develop"}),
        (WinProbabilityAgent, "Win Probability Calculator", {"opportunity_name": "Test Deal"})
    ]

    results = []
    for agent_class, agent_name, kwargs in tests:
        passed = test_agent(agent_class, agent_name, **kwargs)
        results.append((agent_name, passed))

    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)

    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)

    for agent_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {agent_name}")

    print(f"\nTotal: {passed_count}/{total_count} passed ({passed_count/total_count*100:.0f}%)")

    return passed_count == total_count

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
```

Run the test suite:
```bash
python test_all_agents.py
```

---

## Demo Mode Testing

All agents support **Demo Mode** when D365 credentials are not configured. This generates realistic sample data for testing agent logic without requiring D365 access.

**To test in Demo Mode**:
1. Don't set environment variables
2. Run any agent
3. Agent will automatically use demo mode
4. Verify demo data is realistic and properly formatted

**Example**:
```bash
# Test without D365 connection
unset DYNAMICS_365_CLIENT_ID
python agents/stalled_deal_detection_agent.py
```

Expected: Agent runs successfully with generated demo data.

---

## Continuous Integration

### GitHub Actions Workflow

Create `.github/workflows/test-agents.yml`:

```yaml
name: Test Deal Progression Agents

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        cd agent_stacks/b2b_sales_stacks/deal_progression_stack
        pip install -r requirements.txt

    - name: Run agent tests (demo mode)
      run: |
        cd agent_stacks/b2b_sales_stacks/deal_progression_stack
        python test_all_agents.py
```

---

## Next Steps

1. **Production Deployment**: Deploy agents to Azure Functions for serverless execution
2. **M365 Copilot Integration**: Connect agents to Microsoft 365 Copilot via Power Platform
3. **Custom Demo**: Use `demo-generator-m365` agent to create interactive HTML demo
4. **Monitoring**: Add Application Insights for production monitoring
5. **Optimization**: Fine-tune queries based on production usage patterns

---

## Support and Resources

- **D365 Web API Documentation**: https://docs.microsoft.com/dynamics365/customer-engagement/web-api/
- **MSAL Python Documentation**: https://msal-python.readthedocs.io/
- **Azure AD App Registration**: https://docs.microsoft.com/azure/active-directory/develop/quickstart-register-app
- **Architecture Plan**: See `D365_ARCHITECTURE_PLAN.md` in this directory
- **Metadata**: See `metadata.json` for complete component listing
