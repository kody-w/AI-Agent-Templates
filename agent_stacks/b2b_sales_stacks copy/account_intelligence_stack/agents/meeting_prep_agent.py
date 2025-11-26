"""
Meeting Prep Agent
Synthesizes all intelligence into executive meeting briefs

Data Sources:
- All other agents (stakeholder, competitive, etc.)
- Dynamics 365 (past interactions)
- Azure OpenAI (synthesis and script generation)
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

from agents.basic_agent import BasicAgent
import json
from datetime import datetime
from typing import Dict, Any

class MeetingPrepAgent(BasicAgent):
    def __init__(self):
        self.name = "MeetingPrepAgent"
        self.metadata = {
            "name": self.name,
            "description": "Generates comprehensive meeting preparation briefs with talking points, objection handling, and success metrics"
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs) -> Dict[str, Any]:
        account_id = kwargs.get('account_id')
        contact_id = kwargs.get('contact_id')
        meeting_type = kwargs.get('context', {}).get('meeting_type', 'executive_briefing')

        return self._generate_meeting_brief(account_id, contact_id, meeting_type)

    def _generate_meeting_brief(self, account_id: str, contact_id: str, meeting_type: str) -> Dict[str, Any]:
        """Generate complete meeting brief using Azure OpenAI"""

        # Get stakeholder profile
        stakeholder = self._get_stakeholder_profile(contact_id)

        # Get account context
        account_context = self._get_account_context(account_id)

        # Generate meeting script with Azure OpenAI
        meeting_brief = {
            "📅 Meeting Details": {
                "Who": stakeholder['name'],
                "When": "Tomorrow, 8:00 AM - 8:30 AM (30 minutes)",
                "Where": "Contoso HQ, Building 3, Executive Floor",
                "Format": "In-person (preferred for first meetings)",
                "Attendees": "1:1 with CTO",
                "Energy Level": "High - morning person, peak performance time"
            },
            "🎯 Your Meeting Objectives": {
                "Primary Goal": "Establish credibility + secure pilot agreement",
                "Secondary Goal": "Understand her AI vision + position your platform",
                "Success Metric": "Leave with next step scheduled (technical scoping call)",
                "Relationship Goal": "Move from 'vendor' to 'strategic partner' perception"
            },
            "🗣️ Opening (Minutes 0-5)": {
                "Icebreaker": f"'{stakeholder['name']}, thanks for the time. I know you're in week 6 of your 100-day plan - how's it going?'",
                "Credibility": "'I worked with our VP Eng who was your colleague at Amazon'",
                "Permission": "'I have a 12-minute demo that shows how we helped 3 manufacturers achieve 30% cost reduction. Sound relevant?'",
                "What NOT to say": "Avoid: 'Tell me about your business' (unprepared)"
            },
            "💡 Core Message (Minutes 5-20)": self._generate_core_message(),
            "❓ Discovery Questions (Minutes 20-25)": self._generate_discovery_questions(),
            "🎁 The Ask (Minutes 25-30)": self._generate_the_ask(),
            "🛡️ Objection Handling": self._generate_objection_handling(),
            "📊 Materials to Bring": self._list_materials(),
            "✅ Post-Meeting Actions": self._post_meeting_checklist()
        }

        return {
            "status": "success",
            "operation": "meeting_prep",
            "meeting_type": meeting_type,
            "timestamp": datetime.now().isoformat(),
            "data": meeting_brief
        }

    def _get_stakeholder_profile(self, contact_id: str) -> Dict[str, Any]:
        """Get stakeholder profile from Stakeholder Intelligence Agent"""
        return {
            "name": "Dr. Sarah Chen",
            "title": "Chief Technology Officer",
            "background": "Ex-Microsoft Azure, PhD MIT",
            "communication_style": "Direct, data-driven, morning person"
        }

    def _get_account_context(self, account_id: str) -> Dict[str, Any]:
        """Get account context from CRM"""
        return {
            "company": "Contoso Corporation",
            "current_arr": 340000,
            "opportunity_value": 2100000,
            "challenges": ["Legacy system integration", "Vendor sprawl"]
        }

    def _generate_core_message(self) -> Dict[str, str]:
        return {
            "Hook": "'We've helped 12 manufacturers reduce operational costs 30% with AI - in 90 days, not years'",
            "Proof Point #1": "'Fabrikam Manufacturing - $2.3B revenue like you - went from 47 systems to 1 platform'",
            "Proof Point #2": "'They achieved ROI in 4.2 months vs 18-month industry average'",
            "Live Demo Focus": "Real-time predictive maintenance AI (her #1 use case)",
            "Differentiation": "'Unlike DataBricks or Snowflake, we're built specifically for manufacturing'"
        }

    def _generate_discovery_questions(self) -> Dict[str, str]:
        return {
            "Question 1": "'What's the #1 operational bottleneck you'd eliminate with a magic wand?'",
            "Question 2": "'You're consolidating from 47 to 15 vendors - what's your criteria?'",
            "Question 3": "'Where is your team spending time on manual work that AI could eliminate?'",
            "Listen For": "Pain points, decision criteria, timeline pressure, budget"
        }

    def _generate_the_ask(self) -> Dict[str, str]:
        return {
            "Proposal": "'30-day pilot with zero risk - 3 measurable outcomes or you pay $0'",
            "Timeline": "'Week 1: Data integration | Week 2-3: AI training | Week 4: Production pilot'",
            "Success Metrics": "'20% efficiency gain, 90% prediction accuracy, <30 day deployment'",
            "Next Steps": "'Can we get your VP Engineering James on a call Thursday to scope details?'",
            "Urgency": "'If we start by Dec 20, you'll have results for your January board meeting'"
        }

    def _generate_objection_handling(self) -> Dict[str, str]:
        return {
            "Already evaluating DataBricks": "'They're strong in general AI - we're specialized in manufacturing. Let me show accuracy differences...'",
            "Snowflake is cheaper": "'Initial price yes, but 3-year TCO? Our customers save 40% when factoring in...'",
            "Too busy for evaluations": "'That's why our pilot is turn-key - we do 90% of the work, you validate results'",
            "Budget concerns": "'We can structure to fit Q1 budget vs year-end, whichever works better'"
        }

    def _list_materials(self) -> List[str]:
        return [
            "Demo pre-loaded with Contoso's industry data",
            "3 printed case studies: Fabrikam, Northwind, Fourth Coffee",
            "ROI calculator (tablet with interactive tool)",
            "1-page pilot proposal PDF",
            "Business card with handwritten note: 'Amazon connection: Alex Zhang'"
        ]

    def _post_meeting_checklist(self) -> Dict[str, str]:
        return {
            "Within 2 Hours": "Personalized video recap + custom pilot proposal",
            "Within 4 Hours": "LinkedIn connection with thoughtful note",
            "Within 24 Hours": "Case study matching her exact use case + reference intro",
            "Within 48 Hours": "Technical scoping call scheduled with James Liu"
        }


if __name__ == "__main__":
    agent = MeetingPrepAgent()
    result = agent.perform(
        account_id="CONTOSO001",
        contact_id="CONT001",
        context={"meeting_type": "executive_briefing"}
    )
    print(json.dumps(result, indent=2))
