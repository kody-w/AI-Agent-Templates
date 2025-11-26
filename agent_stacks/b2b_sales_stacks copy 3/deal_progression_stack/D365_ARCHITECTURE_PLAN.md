# Deal Progression Stack - Dynamics 365 Architecture Plan

## Overview
This document outlines the 10 core features for the Deal Progression Stack, each powered by direct Dynamics 365 Sales API queries using trial instance data.

## Dynamics 365 Sales Entities Used

### Core Entities
- **opportunity** - Sales opportunities/deals
- **account** - Customer organizations
- **contact** - Individual stakeholders
- **task** - To-do items and follow-ups
- **appointment** - Scheduled meetings
- **phonecall** - Phone call activities
- **email** - Email communications
- **opportunityclose** - Closed opportunity records
- **competitorproduct** - Competitor associations
- **quote** - Price quotes

## 10 Core Features with D365 Queries

### 1. Stalled Deal Detection Agent
**Purpose**: Identify opportunities with no recent activity

**D365 Query**:
```
GET /api/data/v9.2/opportunities?
$filter=statecode eq 0 and
        Microsoft.Dynamics.CRM.OlderThanXDays(PropertyName='modifiedon',PropertyValue=14)
$expand=customerid_account($select=name),
        ownerid($select=fullname),
        Opportunity_Tasks($select=subject,scheduledend),
        Opportunity_Appointments($select=subject,scheduledstart),
        Opportunity_PhoneCalls($select=subject,actualend)
$select=name,estimatedvalue,closeprobability,stepname,modifiedon,estimatedclosedate
$orderby=modifiedon asc
$top=50
```

**Data Points**:
- Days since last activity
- Current stage/step
- Opportunity value
- Last activity type
- Owner information

**Output**:
```json
{
  "stalled_deals": [
    {
      "opportunity_id": "guid",
      "name": "Contoso Enterprise Deal",
      "value": 250000,
      "days_stalled": 21,
      "current_stage": "Proposal",
      "last_activity": "2025-10-04",
      "last_activity_type": "Email",
      "owner": "John Smith",
      "risk_level": "High"
    }
  ],
  "summary": {
    "total_stalled": 12,
    "total_value_at_risk": 1450000,
    "avg_days_stalled": 18
  }
}
```

---

### 2. Next Best Action Recommender Agent
**Purpose**: Suggest optimal next actions based on opportunity stage and history

**D365 Query**:
```
GET /api/data/v9.2/opportunities/{id}?
$expand=customerid_account($select=name,revenue),
        Opportunity_Tasks($select=subject,scheduledend,actualend,statecode),
        Opportunity_Appointments($select=subject,scheduledstart,actualstart),
        Opportunity_PhoneCalls($select=subject,actualstart,actualend),
        opportunity_quotes($select=name,totalamount,statecode),
        opportunitycompetitors_association($select=name)
$select=name,stepname,salesstagecode,estimatedvalue,closeprobability,
        estimatedclosedate,actualclosedate,budgetstatus,purchasetimeframe
```

**Logic**:
- Analyze completed vs pending activities
- Check stage-specific requirements (e.g., "Proposal" needs quote)
- Identify missing critical activities
- Consider deal value and close date urgency

**Output**:
```json
{
  "opportunity_id": "guid",
  "opportunity_name": "Fabrikam Cloud Migration",
  "current_stage": "Proposal",
  "recommended_actions": [
    {
      "action": "Schedule executive briefing",
      "priority": "High",
      "reasoning": "No C-level meetings in 30 days, deal value >$500K",
      "confidence": 0.89,
      "expected_impact": "Increase win probability by 15-20%"
    },
    {
      "action": "Send technical comparison document",
      "priority": "Medium",
      "reasoning": "Competitor identified, no competitive analysis shared",
      "confidence": 0.82,
      "expected_impact": "Address competitive concerns"
    }
  ],
  "stage_requirements": {
    "completed": ["Initial meeting", "Needs assessment", "Demo"],
    "missing": ["Executive briefing", "Technical deep dive", "Quote"]
  }
}
```

---

### 3. Deal Health Score Agent
**Purpose**: Calculate comprehensive health score (0-100) for each opportunity

**D365 Queries**:
```
# Main opportunity data
GET /api/data/v9.2/opportunities/{id}?
$expand=customerid_account,ownerid,
        Opportunity_Tasks($select=statecode,actualend,scheduledend),
        Opportunity_Appointments($select=actualstart,scheduledstart),
        Opportunity_Emails($select=directioncode,createdon)
$select=name,stepname,salesstagecode,estimatedvalue,closeprobability,
        estimatedclosedate,createdon,modifiedon,budgetstatus,purchasetimeframe

# Activity frequency (last 30 days)
GET /api/data/v9.2/tasks?
$filter=regardingobjectid_opportunity_task/opportunityid eq {id} and
        createdon gt {30_days_ago}
$select=subject,createdon

# Stage history
GET /api/data/v9.2/opportunitychangehistory?
$filter=opportunityid eq {id}
$orderby=createdon desc
```

**Health Factors**:
1. **Engagement Score (30%)**: Activity frequency, stakeholder interactions
2. **Momentum Score (25%)**: Stage progression rate, modification frequency
3. **Alignment Score (20%)**: Budget confirmed, timeline fit, decision process
4. **Completeness Score (15%)**: Required activities completed, documentation
5. **Risk Score (10%)**: Competitor presence, stalled indicators

**Output**:
```json
{
  "opportunity_id": "guid",
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
        "timeline_fit": "Q4 2025",
        "decision_process_mapped": true
      }
    },
    "completeness": {
      "score": 65,
      "weight": 0.15,
      "indicators": {
        "activities_complete": "13/20",
        "documents_shared": 8,
        "quote_sent": true
      }
    },
    "risk": {
      "score": 85,
      "weight": 0.10,
      "indicators": {
        "competitors_present": 1,
        "stalled_days": 0,
        "past_due_activities": 2
      }
    }
  }
}
```

---

### 4. Pipeline Velocity Tracker Agent
**Purpose**: Measure deal progression speed through sales stages

**D365 Query**:
```
GET /api/data/v9.2/opportunities?
$filter=statecode eq 0 and createdon gt {90_days_ago}
$select=name,estimatedvalue,salesstagecode,stepname,createdon,estimatedclosedate
$orderby=createdon desc

# For detailed stage history
GET /api/data/v9.2/audits?
$filter=objectid/Id eq {opportunity_id} and
        action eq 'Update' and
        contains(changedata,'salesstagecode')
$orderby=createdon desc
```

**Calculations**:
- Average days per stage
- Stage conversion rates
- Deal velocity (stages/week)
- Bottleneck identification

**Output**:
```json
{
  "pipeline_metrics": {
    "average_deal_cycle": 45,
    "current_velocity": "2.3 stages/month",
    "trend": "15% faster than last quarter"
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
  ],
  "deals_analyzed": 127,
  "time_period": "Last 90 days"
}
```

---

### 5. Stakeholder Engagement Analysis Agent
**Purpose**: Track and analyze contact engagement across deal stakeholders

**D365 Query**:
```
# Get opportunity with all contacts
GET /api/data/v9.2/opportunities/{id}?
$expand=opportunity_customer_contacts($select=fullname,jobtitle,emailaddress1)

# Get activities for each contact
GET /api/data/v9.2/appointments?
$filter=regardingobjectid_opportunity_appointment/opportunityid eq {id}
$expand=appointment_activity_parties($select=partyid,participationtypemask)
$select=subject,scheduledstart,actualstart,statecode

GET /api/data/v9.2/emails?
$filter=regardingobjectid_opportunity_email/opportunityid eq {id}
$expand=email_activity_parties($select=partyid,participationtypemask)
$select=subject,createdon,directioncode

GET /api/data/v9.2/phonecalls?
$filter=regardingobjectid_opportunity_phonecall/opportunityid eq {id}
$expand=phonecall_activity_parties($select=partyid,participationtypemask)
$select=subject,actualstart,actualend,directioncode
```

**Analysis**:
- Engagement frequency per stakeholder
- Influence level (based on title and activity)
- Last contact date
- Sentiment indicators

**Output**:
```json
{
  "opportunity_id": "guid",
  "opportunity_name": "Adventure Works Platform Deal",
  "stakeholders": [
    {
      "contact_id": "guid",
      "name": "Sarah Johnson",
      "title": "VP of Operations",
      "role": "Economic Buyer",
      "engagement_level": "High",
      "total_interactions": 12,
      "last_contact": "2025-10-23",
      "activities": {
        "meetings": 4,
        "emails": 6,
        "calls": 2
      },
      "sentiment": "Positive",
      "influence_score": 95
    },
    {
      "contact_id": "guid",
      "name": "Mike Chen",
      "title": "IT Director",
      "role": "Technical Buyer",
      "engagement_level": "Medium",
      "total_interactions": 8,
      "last_contact": "2025-10-20",
      "activities": {
        "meetings": 2,
        "emails": 5,
        "calls": 1
      },
      "sentiment": "Neutral",
      "influence_score": 78
    },
    {
      "contact_id": "guid",
      "name": "Robert Martinez",
      "title": "CFO",
      "role": "Financial Buyer",
      "engagement_level": "Low",
      "total_interactions": 2,
      "last_contact": "2025-09-15",
      "activities": {
        "meetings": 1,
        "emails": 1,
        "calls": 0
      },
      "sentiment": "Unknown",
      "influence_score": 92,
      "alert": "Key decision maker with low engagement"
    }
  ],
  "engagement_summary": {
    "total_stakeholders": 3,
    "highly_engaged": 1,
    "at_risk": 1,
    "key_contact_gaps": ["CFO needs engagement"]
  }
}
```

---

### 6. Competitor Intelligence Agent
**Purpose**: Identify and analyze competitor presence in deals

**D365 Query**:
```
GET /api/data/v9.2/opportunities?
$filter=statecode eq 0
$expand=opportunitycompetitors_association($select=name,strengths,weaknesses)
$select=name,estimatedvalue,closeprobability,stepname,estimatedclosedate
$orderby=estimatedvalue desc

# Detailed competitor analysis for opportunity
GET /api/data/v9.2/competitors?
$filter=competitorproduct_association/any(c:c/opportunityid eq {id})
$select=name,strengths,weaknesses,threats,opportunities
```

**Output**:
```json
{
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
      "common_strengths": ["Brand recognition", "Ecosystem", "Features"],
      "common_weaknesses": ["Price", "Complexity", "Implementation time"],
      "our_positioning": "Better TCO, faster implementation, superior support"
    },
    {
      "competitor_name": "HubSpot",
      "deals_present": 8,
      "total_value": 1800000,
      "win_rate_against": 0.62,
      "avg_deal_size": 225000,
      "common_strengths": ["Ease of use", "Marketing tools", "Price"],
      "common_weaknesses": ["Enterprise features", "Scalability", "Advanced reporting"],
      "our_positioning": "Enterprise capabilities, better analytics, advanced automation"
    }
  ],
  "active_competitive_deals": [
    {
      "opportunity_id": "guid",
      "opportunity_name": "Contoso Cloud Suite",
      "value": 450000,
      "stage": "Proposal",
      "competitors": ["Salesforce", "Microsoft"],
      "competitive_strategy": "Emphasize integration capabilities and total cost of ownership",
      "battle_card": "vs_salesforce_enterprise.pdf",
      "recommended_actions": [
        "Share TCO calculator",
        "Schedule technical comparison demo",
        "Provide customer references in similar industry"
      ]
    }
  ]
}
```

---

### 7. Deal Risk Assessment Agent
**Purpose**: Identify and quantify risks threatening deal closure

**D365 Query**:
```
GET /api/data/v9.2/opportunities/{id}?
$expand=customerid_account($select=name,revenue,industrycode),
        ownerid($select=fullname),
        Opportunity_Tasks($select=subject,scheduledend,actualend,statecode),
        Opportunity_Appointments($select=scheduledstart,actualstart),
        opportunitycompetitors_association($select=name),
        opportunity_quotes($select=statecode,totalamount,createdon)
$select=name,estimatedvalue,closeprobability,stepname,salesstagecode,
        estimatedclosedate,createdon,modifiedon,budgetstatus,purchasetimeframe,
        decisionmaker,completeinternalreview,completefinalproposal
```

**Risk Factors**:
1. Timeline risks (close date approaching, slow stage progression)
2. Engagement risks (low activity, missed meetings)
3. Competitive risks (multiple competitors, strong competition)
4. Budget risks (unconfirmed budget, value misalignment)
5. Stakeholder risks (missing decision makers, low engagement)
6. Process risks (missing required activities, incomplete documentation)

**Output**:
```json
{
  "opportunity_id": "guid",
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
        },
        {
          "risk": "In current stage for 28 days (avg is 14)",
          "impact": "Medium",
          "probability": 0.8,
          "mitigation": "Identify and address blocker, escalate internally"
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
        },
        {
          "risk": "CFO not engaged in 45 days",
          "impact": "High",
          "probability": 0.85,
          "mitigation": "Request executive briefing with finance team"
        }
      ]
    },
    "competitive_risks": {
      "severity": "Medium",
      "score": 60,
      "risks": [
        {
          "risk": "2 competitors identified",
          "impact": "Medium",
          "probability": 0.6,
          "mitigation": "Share competitive differentiators, provide battle cards"
        }
      ]
    },
    "budget_risks": {
      "severity": "Low",
      "score": 30,
      "risks": [
        {
          "risk": "Budget status unconfirmed",
          "impact": "High",
          "probability": 0.4,
          "mitigation": "Qualify budget in next call"
        }
      ]
    },
    "stakeholder_risks": {
      "severity": "High",
      "score": 80,
      "risks": [
        {
          "risk": "Decision maker not mapped",
          "impact": "High",
          "probability": 0.9,
          "mitigation": "Ask champion to facilitate introduction"
        }
      ]
    },
    "process_risks": {
      "severity": "Medium",
      "score": 55,
      "risks": [
        {
          "risk": "Quote not sent",
          "impact": "Medium",
          "probability": 0.7,
          "mitigation": "Complete and send quote within 48 hours"
        }
      ]
    }
  },
  "recommended_immediate_actions": [
    "Schedule call with decision maker within 48 hours",
    "Send formal quote with value justification",
    "Engage executive sponsor for escalation"
  ]
}
```

---

### 8. Revenue Forecast Accuracy Agent
**Purpose**: Analyze forecast reliability and predict deal closure timing

**D365 Query**:
```
# Current open opportunities
GET /api/data/v9.2/opportunities?
$filter=statecode eq 0
$select=name,estimatedvalue,closeprobability,estimatedclosedate,createdon,salesstagecode,stepname
$orderby=estimatedclosedate asc

# Historical closed opportunities for pattern analysis
GET /api/data/v9.2/opportunities?
$filter=statecode eq 1 and actualclosedate gt {180_days_ago}
$select=name,estimatedvalue,actualrevenue,estimatedclosedate,actualclosedate,
        closeprobability,salesstagecode
$orderby=actualclosedate desc

# Stage history for velocity calculation
GET /api/data/v9.2/audits?
$filter=objectid/Id eq {opportunity_id} and
        action eq 'Update' and
        contains(changedata,'salesstagecode')
$orderby=createdon asc
```

**Analysis**:
- Compare estimated vs actual close dates (historical)
- Calculate stage-specific slip rates
- Predict adjusted close dates based on patterns
- Identify forecast reliability by rep/stage/deal size

**Output**:
```json
{
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
      "opportunity_id": "guid",
      "opportunity_name": "Contoso Enterprise Suite",
      "estimated_value": 350000,
      "current_close_probability": 75,
      "estimated_close_date": "2025-11-15",
      "predicted_close_date": "2025-12-03",
      "prediction_confidence": 0.84,
      "slip_risk": "Medium",
      "factors": {
        "current_stage": "Proposal",
        "days_in_stage": 14,
        "avg_days_for_stage": 18,
        "velocity": "Normal",
        "historical_pattern": "Deals in Proposal typically slip 2-3 weeks"
      },
      "adjusted_probability": 68,
      "adjusted_value": 238000
    }
  ],
  "accuracy_insights": [
    {
      "insight": "Deals >$500K slip 3 weeks on average",
      "sample_size": 23,
      "confidence": 0.89
    },
    {
      "insight": "Proposal stage has 45% slip rate",
      "sample_size": 67,
      "confidence": 0.92
    },
    {
      "insight": "Deals with 2+ competitors close 25% slower",
      "sample_size": 34,
      "confidence": 0.81
    }
  ],
  "recommendations": [
    "Adjust Q4 forecast down by 10% based on historical patterns",
    "Focus on accelerating Proposal stage (highest slip rate)",
    "Increase oversight on deals >$500K"
  ]
}
```

---

### 9. Activity Gap Identifier Agent
**Purpose**: Detect missing critical activities required for each sales stage

**D365 Query**:
```
GET /api/data/v9.2/opportunities/{id}?
$expand=Opportunity_Tasks($select=subject,category,statecode,actualend),
        Opportunity_Appointments($select=subject,subject,actualstart,statecode),
        Opportunity_PhoneCalls($select=subject,directioncode,actualend),
        opportunity_quotes($select=name,statecode,createdon),
        Opportunity_Emails($select=subject,directioncode,createdon)
$select=name,stepname,salesstagecode,estimatedvalue,closeprobability
```

**Stage Requirements** (configurable):
- **Qualify**: Discovery call, needs assessment, budget discussion
- **Develop**: Product demo, technical deep dive, stakeholder meeting
- **Propose**: Quote sent, proposal presented, ROI analysis shared
- **Close**: Contract review, legal approval, final negotiation

**Output**:
```json
{
  "opportunity_id": "guid",
  "opportunity_name": "Wide World Importers CRM",
  "current_stage": "Develop",
  "completeness_score": 65,
  "required_activities": {
    "qualify_stage": {
      "status": "Complete",
      "completion_rate": 1.0,
      "activities": [
        {"activity": "Discovery call", "completed": true, "date": "2025-09-15"},
        {"activity": "Needs assessment", "completed": true, "date": "2025-09-20"},
        {"activity": "Budget discussion", "completed": true, "date": "2025-09-22"}
      ]
    },
    "develop_stage": {
      "status": "In Progress",
      "completion_rate": 0.67,
      "activities": [
        {"activity": "Product demo", "completed": true, "date": "2025-10-01"},
        {"activity": "Technical deep dive", "completed": true, "date": "2025-10-08"},
        {"activity": "Stakeholder meeting", "completed": false, "required_by": "2025-10-28"},
        {"activity": "Security review", "completed": false, "required_by": "2025-10-30"}
      ],
      "missing_critical": ["Stakeholder meeting", "Security review"]
    },
    "propose_stage": {
      "status": "Not Started",
      "completion_rate": 0.0,
      "activities": [
        {"activity": "Quote sent", "completed": false, "required_by": "Stage entry"},
        {"activity": "Proposal presented", "completed": false, "required_by": "Stage entry"},
        {"activity": "ROI analysis shared", "completed": false, "required_by": "Stage entry"}
      ]
    }
  },
  "gaps_identified": [
    {
      "gap": "No stakeholder alignment meeting scheduled",
      "stage": "Develop",
      "priority": "High",
      "impact": "Cannot advance to Propose without stakeholder buy-in",
      "recommendation": "Schedule meeting with VP and Director-level stakeholders"
    },
    {
      "gap": "Security review not initiated",
      "stage": "Develop",
      "priority": "High",
      "impact": "May delay deal closure if security concerns arise later",
      "recommendation": "Engage security team immediately, typical review takes 2 weeks"
    },
    {
      "gap": "No documented ROI analysis",
      "stage": "Propose (prep)",
      "priority": "Medium",
      "impact": "Proposal will lack financial justification",
      "recommendation": "Complete ROI calculator with customer data before quote"
    }
  ],
  "recommended_timeline": [
    {"date": "2025-10-26", "action": "Schedule stakeholder meeting"},
    {"date": "2025-10-27", "action": "Initiate security review"},
    {"date": "2025-10-29", "action": "Complete ROI analysis"},
    {"date": "2025-11-05", "action": "Ready to advance to Propose stage"}
  ]
}
```

---

### 10. Win Probability Calculator Agent
**Purpose**: Calculate data-driven win probability based on deal characteristics and historical patterns

**D365 Query**:
```
# Current opportunity details
GET /api/data/v9.2/opportunities/{id}?
$expand=customerid_account($select=revenue,industrycode),
        opportunitycompetitors_association($select=name),
        Opportunity_Tasks($select=statecode),
        Opportunity_Appointments($select=statecode),
        opportunity_quotes($select=statecode)
$select=name,estimatedvalue,closeprobability,stepname,salesstagecode,
        createdon,estimatedclosedate,budgetstatus,purchasetimeframe,
        decisionmaker,completeinternalreview

# Historical won/lost deals for ML pattern matching
GET /api/data/v9.2/opportunities?
$filter=statecode eq 1 and actualclosedate gt {365_days_ago}
$expand=customerid_account($select=revenue,industrycode),
        opportunitycompetitors_association($select=name)
$select=estimatedvalue,actualrevenue,salesstagecode,createdon,actualclosedate,
        opportunityid,budgetstatus,statuscode
$orderby=actualclosedate desc
```

**Probability Factors**:
1. Deal characteristics (size, industry, account revenue)
2. Sales process completion (activities, stage progression)
3. Engagement metrics (stakeholder involvement, activity frequency)
4. Competitive situation (number, strength of competitors)
5. Timeline alignment (days in stage, close date proximity)
6. Historical win rates (by stage, deal size, industry)

**Output**:
```json
{
  "opportunity_id": "guid",
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
        },
        "industry": {
          "value": "Retail",
          "historical_win_rate": 0.71,
          "impact": "Positive"
        },
        "account_size": {
          "value": "50M-100M revenue",
          "fit_score": 85,
          "impact": "Positive"
        }
      }
    },
    "sales_process": {
      "contribution": 0.30,
      "score": 55,
      "factors": {
        "stage_progression": {
          "current_stage": "Develop",
          "historical_win_rate_from_stage": 0.62,
          "days_in_stage": 18,
          "typical_days": 14,
          "impact": "Neutral/Negative"
        },
        "activity_completion": {
          "completed": 8,
          "required": 12,
          "completion_rate": 0.67,
          "impact": "Negative"
        }
      }
    },
    "engagement_metrics": {
      "contribution": 0.25,
      "score": 48,
      "factors": {
        "stakeholder_engagement": {
          "engaged_stakeholders": 3,
          "decision_makers_engaged": 1,
          "champion_identified": false,
          "impact": "Negative"
        },
        "activity_frequency": {
          "activities_last_30_days": 6,
          "expected": 12,
          "trend": "Declining",
          "impact": "Negative"
        }
      }
    },
    "competitive_situation": {
      "contribution": 0.15,
      "score": 52,
      "factors": {
        "competitors_present": 2,
        "competitor_names": ["Salesforce", "HubSpot"],
        "historical_win_rate_vs_competition": 0.52,
        "impact": "Negative"
      }
    },
    "timeline_alignment": {
      "contribution": 0.15,
      "score": 75,
      "factors": {
        "days_to_close": 35,
        "alignment_with_buyer_timeline": "Good",
        "urgency_indicators": true,
        "impact": "Positive"
      }
    }
  },
  "risk_adjustments": [
    {
      "risk": "Below-average stakeholder engagement",
      "probability_impact": -8,
      "reasoning": "Only 1 of 3 key decision makers engaged"
    },
    {
      "risk": "Multiple competitors",
      "probability_impact": -6,
      "reasoning": "Historical win rate drops 15% with 2+ competitors"
    },
    {
      "risk": "Slow stage progression",
      "probability_impact": -4,
      "reasoning": "28% longer than typical deal in this stage"
    }
  ],
  "recommendations_to_improve": [
    {
      "action": "Engage remaining decision makers",
      "potential_impact": "+10-15% probability",
      "priority": "High"
    },
    {
      "action": "Complete pending activities",
      "potential_impact": "+5-8% probability",
      "priority": "High"
    },
    {
      "action": "Share competitive differentiators",
      "potential_impact": "+5-7% probability",
      "priority": "Medium"
    },
    {
      "action": "Increase engagement frequency",
      "potential_impact": "+4-6% probability",
      "priority": "Medium"
    }
  ],
  "similar_historical_deals": {
    "sample_size": 23,
    "won": 13,
    "lost": 10,
    "win_rate": 0.57,
    "avg_deal_size": 445000,
    "similarity_score": 0.84
  }
}
```

---

## Technical Implementation

### Authentication & Connection
```python
# connectors/d365_connector.py
import os
import requests
from datetime import datetime, timedelta
import msal

class D365Connector:
    def __init__(self):
        self.client_id = os.environ.get('DYNAMICS_365_CLIENT_ID')
        self.client_secret = os.environ.get('DYNAMICS_365_CLIENT_SECRET')
        self.tenant_id = os.environ.get('DYNAMICS_365_TENANT_ID')
        self.resource_url = os.environ.get('DYNAMICS_365_RESOURCE')
        self.api_base = f"{self.resource_url}/api/data/v9.2"
        self.token = None
        self.token_expiry = None

    def get_token(self):
        if self.token and self.token_expiry > datetime.now():
            return self.token

        authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        app = msal.ConfidentialClientApplication(
            self.client_id,
            authority=authority,
            client_credential=self.client_secret
        )

        result = app.acquire_token_for_client(scopes=[f"{self.resource_url}/.default"])

        if "access_token" in result:
            self.token = result['access_token']
            self.token_expiry = datetime.now() + timedelta(seconds=result['expires_in'] - 60)
            return self.token
        else:
            raise Exception(f"Failed to acquire token: {result.get('error_description')}")

    def query(self, endpoint, params=None):
        headers = {
            'Authorization': f'Bearer {self.get_token()}',
            'OData-MaxVersion': '4.0',
            'OData-Version': '4.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        url = f"{self.api_base}/{endpoint}"
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Query failed: {response.status_code} - {response.text}")
```

### Agent Base Class Extension
```python
# agents/d365_base_agent.py
from agents.basic_agent import BasicAgent
from connectors.d365_connector import D365Connector

class D365BaseAgent(BasicAgent):
    def __init__(self, name, metadata):
        super().__init__(name, metadata)
        self.d365 = D365Connector()

    def query_opportunities(self, filter_str=None, expand=None, select=None, orderby=None, top=None):
        params = {}
        if filter_str:
            params['$filter'] = filter_str
        if expand:
            params['$expand'] = expand
        if select:
            params['$select'] = select
        if orderby:
            params['$orderby'] = orderby
        if top:
            params['$top'] = top

        return self.d365.query('opportunities', params)
```

---

## Demo Flow Structure

The interactive demo will showcase all 10 agents in a realistic sales scenario:

1. **Opening**: Sales rep asks for deal health overview
2. **Stalled Deal Detection**: System flags 3 stalled deals
3. **Deal Health Score**: Deep dive into specific deal health
4. **Next Best Action**: Get recommendations for flagged deal
5. **Stakeholder Engagement**: Analyze contact engagement gaps
6. **Activity Gap Identifier**: Identify missing critical activities
7. **Pipeline Velocity**: Show overall pipeline performance
8. **Competitor Intelligence**: Review competitive landscape
9. **Risk Assessment**: Comprehensive risk analysis
10. **Win Probability**: Calculate data-driven win probability
11. **Revenue Forecast**: Adjust forecast based on insights

---

## Environment Variables Required

```bash
# Dynamics 365 Authentication
DYNAMICS_365_CLIENT_ID=your_app_client_id
DYNAMICS_365_CLIENT_SECRET=your_app_client_secret
DYNAMICS_365_TENANT_ID=your_tenant_id
DYNAMICS_365_RESOURCE=https://yourorg.crm.dynamics.com

# Azure OpenAI (for AI-powered recommendations)
AZURE_OPENAI_API_KEY=your_openai_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4o
```

---

## Testing with D365 Trial

1. Create D365 Sales trial: https://dynamics.microsoft.com/sales/free-trial/
2. Enable sample data in Settings > Data Management
3. Create Azure AD app registration for API access
4. Grant permissions: Dynamics CRM API (user_impersonation)
5. Create client secret
6. Test queries using Postman or Python script
7. Verify sample opportunities, contacts, and activities exist

---

## Next Steps

1. ✅ Create D365 connector module
2. ✅ Implement 10 agent classes with real queries
3. ✅ Build comprehensive M365 Copilot demo HTML
4. ✅ Update metadata.json with all agents
5. ✅ Create testing guide with sample queries
6. ✅ Document environment setup
