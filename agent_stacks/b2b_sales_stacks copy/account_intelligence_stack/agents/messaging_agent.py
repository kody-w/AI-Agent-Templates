"""
Messaging Agent
Generates personalized messages using Azure OpenAI

Capabilities:
- LinkedIn connection requests
- Follow-up emails
- Champion activation messages
- CFO/executive outreach
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

from agents.basic_agent import BasicAgent
import json
from datetime import datetime
from typing import Dict, Any

class MessagingAgent(BasicAgent):
    def __init__(self):
        self.name = "MessagingAgent"
        self.metadata = {
            "name": self.name,
            "description": "Generates personalized sales messages using Azure OpenAI based on stakeholder profiles and context"
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs) -> Dict[str, Any]:
        message_type = kwargs.get('context', {}).get('message_type', 'linkedin_connection')
        contact_id = kwargs.get('contact_id')
        account_id = kwargs.get('account_id')

        # Get stakeholder context
        stakeholder = self._get_stakeholder_context(contact_id)

        # Generate message using Azure OpenAI
        message = self._generate_message(message_type, stakeholder, account_id)

        return {
            "status": "success",
            "operation": "generate_messaging",
            "message_type": message_type,
            "timestamp": datetime.now().isoformat(),
            "data": message
        }

    def _get_stakeholder_context(self, contact_id: str) -> Dict[str, Any]:
        """Get stakeholder context for personalization"""
        return {
            "name": "Sarah Chen",
            "title": "CTO",
            "company": "Contoso",
            "interests": ["Manufacturing AI", "Cloud Migration"],
            "communication_style": "Direct, data-driven",
            "mutual_connections": ["Alex Zhang"],
            "recent_activity": "Posted about manufacturing AI adoption"
        }

    def _generate_message(self, message_type: str, stakeholder: Dict, account_id: str) -> Dict[str, Any]:
        """Generate personalized message using Azure OpenAI"""

        templates = {
            "linkedin_connection": self._linkedin_connection_template(stakeholder),
            "post_meeting_email": self._post_meeting_email_template(stakeholder),
            "champion_activation": self._champion_activation_template(stakeholder),
            "cfo_outreach": self._cfo_outreach_template(stakeholder)
        }

        return templates.get(message_type, {})

    def _linkedin_connection_template(self, stakeholder: Dict) -> Dict[str, Any]:
        return {
            "Message": f"Hi {stakeholder['name']} - {stakeholder['mutual_connections'][0]} (my VP Eng, your former Amazon colleague) mentioned you're leading an impressive AI transformation at {stakeholder['company']}. I work with manufacturers implementing AI-powered operations and would love to exchange ideas. Looking forward to our coffee chat tomorrow morning.",
            "Character Count": "287 / 300 (optimized for LinkedIn limit)",
            "Why This Works": "Personal connection, mutual respect, value-first (not sales-y)",
            "Send Timing": "Tonight at 6pm (she checks LinkedIn evenings)",
            "Acceptance Probability": "85%"
        }

    def _post_meeting_email_template(self, stakeholder: Dict) -> Dict[str, Any]:
        return {
            "Subject": "30-Day Pilot Proposal - Predictive Maintenance AI for Contoso",
            "Body": f"{stakeholder['name']},<br><br>Thank you for the candid conversation this morning. Three things stuck with me:<br><br>1️⃣ Your vision to eliminate manual bottlenecks in quality control<br>2️⃣ The pressure to show measurable AI ROI by your board meeting in January<br>3️⃣ Your concern about vendor solutions that overpromise and underdeliver<br><br>I've put together a risk-free 30-day pilot that addresses all three:<br><br>📅 TIMELINE:<br>• Dec 16-20: Data integration (we do the heavy lifting)<br>• Dec 23-Jan 3: AI model training on your historical data<br>• Jan 6-10: Production pilot with your ops team<br>• Jan 13: Results presentation (ready for your board)<br><br>🎯 GUARANTEED OUTCOMES (or you pay $0):<br>✅ 20% reduction in quality control time<br>✅ 90%+ prediction accuracy for equipment failures<br>✅ Live dashboard deployed in <30 days<br><br>Let me know what questions you have.<br><br>Best,<br>[Your Name]",
            "Attachments": ["Pilot proposal PDF", "Case study PDF", "Custom video link"],
            "Why This Works": [
                "Summarizes her pain points (proves you listened)",
                "Addresses objections preemptively",
                "Specific timeline with dates",
                "Risk-reversal guarantee",
                "Clear next step"
            ]
        }

    def _champion_activation_template(self, stakeholder: Dict) -> Dict[str, Any]:
        return {
            "Subject": "Coffee next week? + Quick favor to ask",
            "Body": f"Hey James,<br><br>Hope you're doing well! I know things have been busy with the new CTO onboarding.<br><br>I met with {stakeholder['name']} yesterday and showed her the AI capabilities you've been using. She seemed really interested in the predictive maintenance use case.<br><br>Quick favor: Would you be open to joining a 30-min technical scoping call with {stakeholder['name']} and me this Thursday? Your perspective on how the platform works in production would be invaluable.<br><br>Also - I owe you coffee. Available next Tuesday or Wednesday?<br><br>Thanks,<br>[Your Name]",
            "Why This Works": "Acknowledges political situation, gives him credit, low-commitment ask"
        }

    def _cfo_outreach_template(self, stakeholder: Dict) -> Dict[str, Any]:
        return {
            "Subject": "ROI Analysis - Contoso Manufacturing AI Initiative",
            "Body": "Robert,<br><br>I'm working with Sarah Chen on a pilot for AI-powered manufacturing operations at Contoso.<br><br>Given your focus on measurable ROI, I put together a financial analysis specific to your business:<br><br>• 30% operational cost reduction = $4.2M annual savings<br>• Payback period: 4.2 months<br>• 3-year NPV: $11.7M (at your 12% discount rate)<br><br>I've attached the full model with assumptions - happy to walk through it if useful.<br><br>Would 15 minutes next week work to discuss the financial case?<br><br>Best regards,<br>[Your Name]<br><br>P.S. - I know you're reviewing all SaaS contracts >$100K. This analysis shows how we compare on total cost of ownership.",
            "Why This Works": "Speaks CFO language (numbers, ROI, NPV), acknowledges his initiative"
        }


if __name__ == "__main__":
    agent = MessagingAgent()
    result = agent.perform(
        contact_id="CONT001",
        account_id="CONTOSO001",
        context={"message_type": "linkedin_connection"}
    )
    print(json.dumps(result, indent=2))
