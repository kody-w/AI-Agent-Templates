"""
Competitive Intelligence Agent
Detects competitive threats and generates battle cards

Data Sources:
- Azure AI Search (competitive intelligence index)
- Web scraping (G2, TrustRadius, competitor websites)
- Dynamics 365 (past competitive wins/losses)
- Azure OpenAI (synthesis)
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

from agents.basic_agent import BasicAgent
import json
from datetime import datetime
from typing import Dict, Any, List

class CompetitiveIntelligenceAgent(BasicAgent):
    def __init__(self):
        self.name = "CompetitiveIntelligenceAgent"
        self.metadata = {
            "name": self.name,
            "description": "Detects competitive threats and generates battle cards using Azure AI Search and market intelligence"
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs) -> Dict[str, Any]:
        operation = kwargs.get('operation', 'detect_active_threats')
        account_id = kwargs.get('account_id')

        if operation == "detect_active_threats":
            return self._detect_active_threats(account_id)
        elif operation == "generate_battle_card":
            return self._generate_battle_card(account_id, kwargs.get('competitor'))

    def _detect_active_threats(self, account_id: str) -> Dict[str, Any]:
        """Detect active competitive threats using Azure AI Search and CRM data"""

        # Query Azure AI Search for competitive mentions
        competitors = self._search_competitive_activity(account_id)

        # Analyze CRM for competitor mentions in notes/emails
        crm_mentions = self._analyze_crm_competitive_mentions(account_id)

        # Get market intelligence
        market_intel = self._get_market_intelligence()

        return {
            "status": "success",
            "operation": "detect_active_threats",
            "account_id": account_id,
            "timestamp": datetime.now().isoformat(),
            "data": {
                "active_threats": competitors,
                "threat_level": "🔴 SEVERE - 2 competitors in active evaluation",
                "primary_competitor": "DataBricks (CTO's former colleague)",
                "secondary_competitor": "Snowflake (aggressive pricing)",
                "intelligence_sources": ["LinkedIn activity", "G2 reviews", "CRM notes", "Champion intel"]
            }
        }

    def _generate_battle_card(self, account_id: str, competitor: str) -> Dict[str, Any]:
        """Generate detailed competitive battle card"""

        battle_card = {
            "Competitor": competitor,
            "Threat Level": "🔴 CRITICAL" if competitor == "DataBricks" else "🟡 MODERATE",
            "Recent Activity": self._get_competitor_activity(competitor, account_id),
            "Their Strategy": self._analyze_competitor_strategy(competitor),
            "Their Strengths": self._get_competitor_strengths(competitor),
            "Their Weaknesses": self._get_competitor_weaknesses(competitor),
            "Your Counter-Strategy": self._generate_counter_strategy(competitor),
            "Competitive Positioning": self._get_positioning(competitor)
        }

        return {
            "status": "success",
            "data": {"battle_card": battle_card}
        }

    def _search_competitive_activity(self, account_id: str) -> List[Dict[str, Any]]:
        """Search Azure AI Search for competitive intelligence"""
        # Mock - in production, query Azure AI Search index
        return [
            {
                "competitor": "DataBricks",
                "threat_level": "CRITICAL",
                "relationship": "CTO's ex-Microsoft colleague is their AE",
                "proposal_status": "Submitted 2 weeks ago ($1.8M, 3-year)"
            },
            {
                "competitor": "Snowflake",
                "threat_level": "MODERATE",
                "activity": "Running free POC in finance dept (60 days)",
                "pricing": "$1.2M vs your $1.9M"
            }
        ]

    def _analyze_crm_competitive_mentions(self, account_id: str) -> Dict[str, Any]:
        """Analyze CRM notes and emails for competitor mentions"""
        return {
            "total_mentions": 12,
            "DataBricks_mentions": 7,
            "Snowflake_mentions": 5,
            "last_mention": "2024-12-05"
        }

    def _get_market_intelligence(self) -> Dict[str, Any]:
        """Get broader market intelligence"""
        return {
            "market_trends": ["AI/ML adoption accelerating", "Vendor consolidation trend"],
            "buying_patterns": "Customers prefer unified platforms over point solutions"
        }

    def _get_competitor_activity(self, competitor: str, account_id: str) -> str:
        activities = {
            "DataBricks": "CTO's ex-Microsoft colleague is their AE | Proposal submitted 2 weeks ago",
            "Snowflake": "Running free POC in finance department (Day 60 of 90)"
        }
        return activities.get(competitor, "Unknown")

    def _analyze_competitor_strategy(self, competitor: str) -> str:
        strategies = {
            "DataBricks": "Personal relationship + AI/ML capabilities + modern stack",
            "Snowflake": "Aggressive 40% discount + data warehousing + cloud-native story"
        }
        return strategies.get(competitor, "Unknown")

    def _get_competitor_strengths(self, competitor: str) -> List[str]:
        strengths = {
            "DataBricks": [
                "Strong AI/ML capabilities",
                "CTO familiarity and trust",
                "Modern, cloud-native architecture",
                "Strong brand in data space"
            ],
            "Snowflake": [
                "Lower price point (40% cheaper)",
                "Strong data warehouse reputation",
                "Proven scalability",
                "Large customer base"
            ]
        }
        return strengths.get(competitor, [])

    def _get_competitor_weaknesses(self, competitor: str) -> List[str]:
        weaknesses = {
            "DataBricks": [
                "No manufacturing vertical experience",
                "Weak integration with legacy Oracle systems",
                "No local support team (12hr time zone gap)",
                "Recent customer churn in industrial sector (23%)"
            ],
            "Snowflake": [
                "Limited analytics capabilities vs your platform",
                "POC struggling to prove ROI (insider intel)",
                "No AI/ML features that CTO requires",
                "Consultant-dependent (weak services team)"
            ]
        }
        return weaknesses.get(competitor, [])

    def _generate_counter_strategy(self, competitor: str) -> str:
        strategies = {
            "DataBricks": "Emphasize manufacturing expertise + Oracle integration toolkit + 24/7 US support + lower industrial churn",
            "Snowflake": "Prove total cost of ownership + faster time-to-value + AI/ML roadmap alignment"
        }
        return strategies.get(competitor, "Position on value, not price")

    def _get_positioning(self, competitor: str) -> str:
        return "Trusted manufacturing transformation partner (not just a vendor)"


if __name__ == "__main__":
    agent = CompetitiveIntelligenceAgent()
    result = agent.perform(operation="detect_active_threats", account_id="CONTOSO001")
    print(json.dumps(result, indent=2))
