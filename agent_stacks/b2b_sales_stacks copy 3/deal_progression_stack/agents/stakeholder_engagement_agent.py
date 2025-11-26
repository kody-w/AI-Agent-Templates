import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from agents.d365_base_agent import D365BaseAgent
import json
import random
from datetime import datetime, timedelta


class StakeholderEngagementAgent(D365BaseAgent):
    """
    Tracks and analyzes contact engagement across deal stakeholders
    Identifies engagement gaps and recommends stakeholder strategy
    """

    def __init__(self):
        self.name = "StakeholderEngagementAgent"
        self.metadata = {
            "name": self.name,
            "description": "Analyzes stakeholder engagement patterns, identifies gaps, and recommends engagement strategies",
            "parameters": {
                "type": "object",
                "properties": {
                    "opportunity_id": {
                        "type": "string",
                        "description": "D365 opportunity ID to analyze"
                    },
                    "opportunity_name": {
                        "type": "string",
                        "description": "Opportunity name (for demo mode)"
                    }
                },
                "required": []
            }
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        """Analyze stakeholder engagement"""
        opportunity_id = kwargs.get('opportunity_id')
        opportunity_name = kwargs.get('opportunity_name', 'Unknown Opportunity')

        try:
            if self.d365 and not self.d365.demo_mode and opportunity_id:
                # Real D365 query
                engagement_data = self._analyze_d365_stakeholders(opportunity_id)
            else:
                # Demo mode
                engagement_data = self._generate_demo_engagement_data(opportunity_name)

            return {
                "status": "success",
                "message": f"Analyzed engagement for {len(engagement_data['stakeholders'])} stakeholders",
                "data": engagement_data
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to analyze stakeholder engagement: {str(e)}",
                "data": {}
            }

    def _analyze_d365_stakeholders(self, opportunity_id):
        """Analyze stakeholders from D365 data"""
        # Would query D365 for contacts, activities, etc.
        return {}

    def _generate_demo_engagement_data(self, opportunity_name):
        """Generate realistic demo stakeholder engagement data"""
        demo_stakeholders = [
            {"name": "Sarah Johnson", "title": "VP of Operations", "role": "Economic Buyer", "influence": 95},
            {"name": "Mike Chen", "title": "IT Director", "role": "Technical Buyer", "influence": 78},
            {"name": "Robert Martinez", "title": "CFO", "role": "Financial Buyer", "influence": 92},
            {"name": "Emily Davis", "title": "Project Manager", "role": "Champion", "influence": 70},
            {"name": "David Kim", "title": "CIO", "role": "Final Approver", "influence": 98}
        ]

        stakeholders = []
        alerts = []

        for i, person in enumerate(demo_stakeholders[:random.randint(3, 5)]):
            meetings = random.randint(0, 6)
            emails = random.randint(0, 10)
            calls = random.randint(0, 4)
            total_interactions = meetings + emails + calls

            days_since_contact = random.randint(0, 60)
            last_contact = (datetime.now() - timedelta(days=days_since_contact)).strftime('%Y-%m-%d')

            # Determine engagement level
            if total_interactions >= 10:
                engagement_level = "High"
            elif total_interactions >= 5:
                engagement_level = "Medium"
            else:
                engagement_level = "Low"

            # Determine sentiment
            if total_interactions >= 8:
                sentiment = "Positive"
            elif total_interactions >= 4:
                sentiment = "Neutral"
            else:
                sentiment = "Unknown"

            stakeholder = {
                "contact_id": f"contact-{random.randint(1000, 9999)}",
                "name": person["name"],
                "title": person["title"],
                "role": person["role"],
                "engagement_level": engagement_level,
                "total_interactions": total_interactions,
                "last_contact": last_contact,
                "days_since_contact": days_since_contact,
                "activities": {
                    "meetings": meetings,
                    "emails": emails,
                    "calls": calls
                },
                "sentiment": sentiment,
                "influence_score": person["influence"]
            }

            # Generate alerts for key stakeholders with low engagement
            if person["influence"] >= 90 and engagement_level == "Low":
                stakeholder["alert"] = f"Key decision maker with low engagement - {days_since_contact} days since contact"
                alerts.append(stakeholder["alert"])

            stakeholders.append(stakeholder)

        # Calculate summary
        highly_engaged = sum(1 for s in stakeholders if s["engagement_level"] == "High")
        at_risk = sum(1 for s in stakeholders if s["engagement_level"] == "Low" and s["influence_score"] >= 80)

        summary = {
            "total_stakeholders": len(stakeholders),
            "highly_engaged": highly_engaged,
            "at_risk": at_risk,
            "key_contact_gaps": alerts if alerts else ["All key stakeholders appropriately engaged"]
        }

        return {
            "opportunity_id": f"opp-{random.randint(1000, 9999)}",
            "opportunity_name": opportunity_name,
            "stakeholders": stakeholders,
            "engagement_summary": summary
        }


if __name__ == "__main__":
    agent = StakeholderEngagementAgent()
    result = agent.perform(opportunity_name="Adventure Works Platform Deal")
    print(json.dumps(result, indent=2))
