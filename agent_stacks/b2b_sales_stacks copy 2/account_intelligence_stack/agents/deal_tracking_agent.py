"""
Deal Tracking Agent
Provides real-time deal dashboard and milestone tracking

Data Sources:
- Dynamics 365 (opportunity data, activities)
- Microsoft Graph (email/meeting activity)
- Historical deal data (for benchmarking)
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from agents.basic_agent import BasicAgent
from connectors.crm_connector import CRMConnector
from connectors.azure_openai_connector import AzureOpenAIConnector
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List

class DealTrackingAgent(BasicAgent):
    def __init__(self, connector_token: str = None):
        self.name = "DealTrackingAgent"
        self.metadata = {
            "name": self.name,
            "description": "Real-time deal dashboard with milestones, leading indicators, and stakeholder engagement tracking"
        }
        super().__init__(name=self.name, metadata=self.metadata)

        # Initialize connectors
        self.crm_connector = CRMConnector(connector_token)
        self.openai_connector = AzureOpenAIConnector(connector_token)

    def perform(self, **kwargs) -> Dict[str, Any]:
        opportunity_id = kwargs.get('opportunity_id')
        account_id = kwargs.get('account_id')

        return self._generate_deal_dashboard(account_id, opportunity_id)

    def _generate_deal_dashboard(self, account_id: str, opportunity_id: str = None) -> Dict[str, Any]:
        """Generate comprehensive deal tracking dashboard"""

        # Get opportunity data from Dynamics 365
        opportunity = self._get_opportunity_data(opportunity_id or "OPP001")

        # Get stakeholder engagement metrics from Graph API
        engagement = self._get_stakeholder_engagement(account_id)

        # Get milestone progress
        milestones = self._get_milestone_progress(opportunity_id)

        # Get leading indicators
        indicators = self._get_leading_indicators(account_id, opportunity_id)

        dashboard = {
            "📊 Deal Dashboard - Live Metrics": {
                "Deal Name": "Contoso Corporation - Renewal + Expansion",
                "Current Stage": "Qualification (Stage 2 of 7)",
                "Target Close Date": "January 20, 2025 (41 days)",
                "Deal Value": "$2.1M ARR (6.2x expansion)",
                "Close Probability": "47% (Below target - needs action)",
                "Last Updated": datetime.now().isoformat(),
                "Health Status": "🟡 YELLOW - At Risk"
            },
            "🎯 Critical Success Milestones": milestones,
            "📈 Leading Indicators (Early Warning System)": indicators,
            "🎯 Stakeholder Engagement Scorecard": engagement,
            "💰 Revenue Milestones & Quota Impact": self._get_revenue_metrics(opportunity),
            "📅 Weekly Checkpoint Framework": self._get_checkpoint_framework(),
            "🚨 Deal Risk Alerts (Auto-Monitored)": self._get_risk_alerts(),
            "✅ Success Criteria Checklist": self._get_success_criteria()
        }

        return {
            "status": "success",
            "operation": "deal_dashboard",
            "opportunity_id": opportunity_id,
            "timestamp": datetime.now().isoformat(),
            "data": dashboard
        }

    def _get_opportunity_data(self, opportunity_id: str) -> Dict[str, Any]:
        """Get opportunity data from Dynamics 365"""
        # Mock - in production, query Dynamics API
        return {
            "id": opportunity_id,
            "name": "Contoso - Digital Transformation",
            "value": 2100000,
            "stage": "Qualification",
            "probability": 47,
            "close_date": "2025-01-20",
            "account_id": "CONTOSO001"
        }

    def _get_stakeholder_engagement(self, account_id: str) -> Dict[str, Dict[str, Any]]:
        """Track engagement with each stakeholder"""
        return {
            "CTO Sarah Chen": {
                "Engagement Level": "0/10 - ❌ NO CONTACT",
                "Last Touch": "Never (she just started 6 weeks ago)",
                "Next Touch": "Within 24 hours (Alex intro)",
                "Target Score": "8/10 by Dec 20",
                "Activities Needed": "1 meeting + 3 email exchanges + 1 demo"
            },
            "CFO Robert Martinez": {
                "Engagement Level": "2/10 - 🔴 VERY WEAK",
                "Last Touch": "Trade show 18 months ago",
                "Next Touch": "ROI email after CTO meeting",
                "Target Score": "7/10 by Dec 20",
                "Activities Needed": "1 ROI presentation + business case review"
            },
            "Champion James Liu": {
                "Engagement Level": "6/10 - 🟡 FADING",
                "Last Touch": "3 weeks ago (support ticket)",
                "Next Touch": "Coffee this week",
                "Target Score": "9/10 by Dec 20",
                "Activities Needed": "Reactivate + involve in CTO meetings"
            }
        }

    def _get_milestone_progress(self, opportunity_id: str) -> Dict[str, Dict[str, Any]]:
        """Track critical milestones"""
        return {
            "✅ Week 1 (Dec 10-14)": {
                "Milestone": "CTO relationship established",
                "Target": "Meeting completed + pilot proposal submitted",
                "Status": "🔴 NOT STARTED - Meeting not scheduled yet",
                "Risk": "HIGH - Must complete by Friday or timeline slips",
                "Action": "Alex Zhang intro call TODAY"
            },
            "⏳ Week 2 (Dec 16-20)": {
                "Milestone": "Technical validation + stakeholder alignment",
                "Target": "Pilot scoping call + CFO meeting + Procurement engaged",
                "Status": "⚪ PENDING - Depends on Week 1 completion",
                "Risk": "MODERATE - Holiday calendar compression",
                "Success Criteria": "All 5 stakeholders engaged + pilot agreement"
            },
            "⏳ Week 3 (Dec 23-27)": {
                "Milestone": "Verbal commitment",
                "Target": "Executive alignment + contract negotiation started",
                "Status": "⚪ PENDING",
                "Risk": "HIGH - Holiday week (low availability)",
                "Backup Plan": "Extend to Jan 6 if holidays cause delay"
            },
            "⏳ Week 4-5 (Jan 6-17)": {
                "Milestone": "Contract finalization",
                "Target": "Legal review + pricing finalized + signatures",
                "Status": "⚪ PENDING",
                "Success Criteria": "Contracts signed by Jan 17"
            },
            "⏳ Week 6 (Jan 20)": {
                "Milestone": "DEAL CLOSED 🎉",
                "Target": "Signature + payment + kickoff scheduled",
                "Success Metric": "$2.1M ARR booked + Q1 quota credit"
            }
        }

    def _get_leading_indicators(self, account_id: str, opportunity_id: str) -> Dict[str, List[str]]:
        """Early warning indicators"""
        return {
            "🟢 GREEN Signals (Keep Doing This)": [
                "CTO responds to emails within 24 hours",
                "James Liu actively participating in technical discussions",
                "CFO asks detailed ROI questions (shows real interest)",
                "Sarah introduces you to other executives",
                "Usage metrics trending upward"
            ],
            "🟡 YELLOW Signals (Watch Closely)": [
                "⚠️ Email response time >48 hours (losing priority)",
                "⚠️ Meeting rescheduled more than once (lack of urgency)",
                "⚠️ CFO not engaged yet (economic buyer missing)",
                "⚠️ Champion going silent (political pressure)"
            ],
            "🔴 RED Signals (URGENT - Fix Immediately)": [
                "❌ CTO stops responding to outreach (ghosting)",
                "❌ James Liu says 'now's not good time' (politically blocked)",
                "❌ Competitor mentioned favorably >3 times (losing mindshare)",
                "❌ Budget freeze or 'let's wait til next quarter' (deal death)"
            ]
        }

    def _get_revenue_metrics(self, opportunity: Dict[str, Any]) -> Dict[str, Any]:
        """Revenue and quota impact"""
        return {
            "Current ARR": "$340K (base renewal)",
            "Target ARR": "$2.1M (expansion)",
            "Upside ARR": "$3.5M (if strategic enterprise tier)",
            "Your Quota": "$8M annual",
            "Deal % of Quota": "26% (make or break deal for your year)",
            "Commission Impact": "$63K at target ($2.1M x 3% commission)",
            "Bonus Impact": "This deal puts you at 112% of quota = President's Club"
        }

    def _get_checkpoint_framework(self) -> Dict[str, str]:
        """Weekly checkpoint cadence"""
        return {
            "Every Monday 9am": "Review deal dashboard + update close probability",
            "Every Wednesday": "Stakeholder touch (email, call, or meeting)",
            "Every Friday": "Week-in-review with manager + next week plan",
            "Daily During Close": "Update CRM notes + track all interactions",
            "Red Flag Check": "If no contact in 4 days = immediate outreach"
        }

    def _get_risk_alerts(self) -> Dict[str, List[str]]:
        """Automated risk alerts"""
        return {
            "Time-Based Alerts": [
                "Day 7: No CTO meeting yet = CRITICAL",
                "Day 14: No pilot proposal submitted = HIGH RISK",
                "Day 21: No verbal commitment = AT RISK",
                "Day 30: No contract draft = LIKELY LOST"
            ],
            "Activity-Based Alerts": [
                "Email response time >72 hours = YELLOW",
                "Meeting cancelled 2x = RED",
                "Competitor mentioned 3x = RED",
                "Champion score drops below 6/10 = YELLOW"
            ]
        }

    def _get_success_criteria(self) -> Dict[str, List[str]]:
        """Success criteria by milestone"""
        return {
            "By Dec 14": [
                "☐ CTO meeting completed",
                "☐ Pilot proposal submitted",
                "☐ Champion James re-engaged",
                "☐ CFO outreach initiated"
            ],
            "By Dec 20": [
                "☐ All 5 stakeholders contacted",
                "☐ Technical validation started",
                "☐ Procurement process mapped",
                "☐ Competitive positioning established",
                "☐ Close probability >65%"
            ],
            "By Dec 27": [
                "☐ Verbal commitment secured",
                "☐ Contract negotiation started",
                "☐ Legal review initiated"
            ],
            "By Jan 20": [
                "☐ Contracts signed",
                "☐ Payment received",
                "☐ $2.1M ARR booked",
                "☐ Champagne celebration 🍾"
            ]
        }


if __name__ == "__main__":
    agent = DealTrackingAgent()
    result = agent.perform(
        account_id="CONTOSO001",
        opportunity_id="OPP001"
    )
    print(json.dumps(result, indent=2))
