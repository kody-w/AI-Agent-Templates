"""
Stakeholder Intelligence Agent
Analyzes buying committee, relationship health, and stakeholder profiles

Data Sources:
- Dynamics 365 (CRM contacts and relationships)
- Microsoft Graph API (emails, meetings, org chart)
- LinkedIn Sales Navigator (professional background, connections)
- Azure OpenAI (synthesis and insights)
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

from agents.basic_agent import BasicAgent
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List

class StakeholderIntelligenceAgent(BasicAgent):
    """
    Provides deep intelligence on stakeholders and buying committees
    """

    def __init__(self):
        self.name = "StakeholderIntelligenceAgent"
        self.metadata = {
            "name": self.name,
            "description": "Analyzes stakeholders, buying committees, and relationship dynamics using Dynamics 365, Microsoft Graph, and LinkedIn Sales Navigator",
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": [
                            "analyze_buying_committee",
                            "stakeholder_profile",
                            "relationship_health",
                            "influence_mapping"
                        ]
                    },
                    "account_id": {
                        "type": "string"
                    },
                    "contact_id": {
                        "type": "string"
                    }
                },
                "required": ["operation", "account_id"]
            }
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs) -> Dict[str, Any]:
        operation = kwargs.get('operation', 'analyze_buying_committee')
        account_id = kwargs.get('account_id')

        if operation == "analyze_buying_committee":
            return self._analyze_buying_committee(account_id)
        elif operation == "stakeholder_profile":
            return self._stakeholder_profile(kwargs.get('contact_id'))
        elif operation == "relationship_health":
            return self._relationship_health(account_id)
        elif operation == "influence_mapping":
            return self._influence_mapping(account_id)

    def _analyze_buying_committee(self, account_id: str) -> Dict[str, Any]:
        """
        Analyze entire buying committee with influence scores
        Connects to Dynamics 365 and Microsoft Graph
        """

        # Get contacts from Dynamics 365
        contacts = self._get_dynamics_contacts(account_id)

        # Enrich with Graph API data (emails, meetings)
        enriched_contacts = [self._enrich_contact_with_graph(c) for c in contacts]

        # Get LinkedIn data
        linkedin_data = [self._get_linkedin_data(c['email']) for c in enriched_contacts]

        # Calculate influence scores
        buying_committee = [
            self._calculate_influence_score(contact, linkedin, account_id)
            for contact, linkedin in zip(enriched_contacts, linkedin_data)
        ]

        # Sort by influence
        buying_committee.sort(key=lambda x: x['influence_score'], reverse=True)

        return {
            "status": "success",
            "operation": "analyze_buying_committee",
            "account_id": account_id,
            "timestamp": datetime.now().isoformat(),
            "data": {
                "stakeholder_count": len(buying_committee),
                "buying_committee": buying_committee[:5],  # Top 5 stakeholders
                "decision_dynamics": self._analyze_decision_dynamics(buying_committee),
                "engagement_gaps": self._identify_engagement_gaps(buying_committee)
            },
            "sources": ["Dynamics 365", "Microsoft Graph", "LinkedIn Sales Navigator"]
        }

    def _stakeholder_profile(self, contact_id: str) -> Dict[str, Any]:
        """
        Deep dive on single stakeholder
        """

        contact = self._get_contact_details(contact_id)
        graph_data = self._enrich_contact_with_graph(contact)
        linkedin_data = self._get_linkedin_data(contact['email'])
        recent_activity = self._get_recent_activity(contact_id)

        return {
            "status": "success",
            "operation": "stakeholder_profile",
            "contact_id": contact_id,
            "data": {
                "Executive Profile": {
                    "Full Name": contact['full_name'],
                    "Title": contact['job_title'],
                    "Tenure": contact['tenure'],
                    "Background": linkedin_data['career_summary'],
                    "Education": linkedin_data['education']
                },
                "Professional Interests": linkedin_data['interests'],
                "Current Initiatives": contact['current_projects'],
                "Communication Style": self._analyze_communication_style(graph_data),
                "Engagement Strategy": self._recommend_engagement_strategy(contact, linkedin_data),
                "Recent Activity": recent_activity,
                "Relationship Strength": self._calculate_relationship_strength(contact_id)
            }
        }

    def _get_dynamics_contacts(self, account_id: str) -> List[Dict[str, Any]]:
        """
        Get contacts from Dynamics 365
        In production: Uses Microsoft Dataverse API
        """
        # Mock data - in production, call Dataverse API
        return [
            {
                "contact_id": "CONT001",
                "full_name": "Dr. Sarah Chen",
                "job_title": "Chief Technology Officer",
                "email": "sarah.chen@contoso.com",
                "phone": "+1-206-555-0100",
                "decision_role": "Economic Buyer",
                "tenure": "6 weeks",
                "department": "Technology",
                "reports_to": "CEO"
            },
            {
                "contact_id": "CONT002",
                "full_name": "Robert Martinez",
                "job_title": "Chief Financial Officer",
                "email": "robert.martinez@contoso.com",
                "decision_role": "Budget Approver",
                "tenure": "2 years",
                "department": "Finance"
            },
            {
                "contact_id": "CONT003",
                "full_name": "James Liu",
                "job_title": "VP Engineering",
                "email": "james.liu@contoso.com",
                "decision_role": "Technical Evaluator",
                "tenure": "5 years",
                "department": "Engineering"
            },
            {
                "contact_id": "CONT004",
                "full_name": "Michelle Park",
                "job_title": "Director of Procurement",
                "email": "michelle.park@contoso.com",
                "decision_role": "Gatekeeper",
                "tenure": "8 years",
                "department": "Procurement"
            },
            {
                "contact_id": "CONT005",
                "full_name": "David Kumar",
                "job_title": "VP Operations",
                "email": "david.kumar@contoso.com",
                "decision_role": "End User",
                "tenure": "12 years",
                "department": "Operations"
            }
        ]

    def _enrich_contact_with_graph(self, contact: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enrich contact with Microsoft Graph data (emails, meetings)
        In production: Uses Microsoft Graph API
        """
        # Mock Graph API data
        contact['graph_data'] = {
            "email_interactions": 12,
            "meetings_attended": 3,
            "last_contact": "2024-10-18",
            "response_time_avg": "4 hours",
            "email_sentiment": "neutral"
        }
        return contact

    def _get_linkedin_data(self, email: str) -> Dict[str, Any]:
        """
        Get LinkedIn profile data via Sales Navigator
        In production: Uses LinkedIn Sales Navigator API via Dynamics 365
        """
        # Mock LinkedIn data
        linkedin_profiles = {
            "sarah.chen@contoso.com": {
                "linkedin_url": "linkedin.com/in/sarahchen",
                "connections": 4800,
                "career_summary": "Microsoft Azure (8yr) → Amazon AWS (4yr) → Startup Founder",
                "education": "PhD Computer Science MIT | MS Stanford | BS Berkeley",
                "posts_last_30_days": 6,
                "engagement_rate": "high",
                "interests": ["AI/ML", "Cloud Infrastructure", "Manufacturing AI"],
                "speaking": "Keynote at ManufacturingTech Summit 2025",
                "mutual_connections": 2
            },
            "james.liu@contoso.com": {
                "linkedin_url": "linkedin.com/in/jamesliu",
                "connections": 1200,
                "career_summary": "5 years at Contoso, previously at tech startups",
                "education": "MS Computer Science Stanford",
                "interests": ["DevOps", "Cloud Native", "Platform Engineering"],
                "mutual_connections": 1
            }
        }

        return linkedin_profiles.get(email, {
            "linkedin_url": "Unknown",
            "connections": 500,
            "career_summary": "Unknown",
            "education": "Unknown",
            "interests": []
        })

    def _calculate_influence_score(self, contact: Dict, linkedin: Dict, account_id: str) -> Dict[str, Any]:
        """
        Calculate influence score based on multiple factors
        """
        # Scoring algorithm
        base_score = 50

        # Role-based score
        role_scores = {
            "Economic Buyer": 45,
            "Budget Approver": 35,
            "Technical Evaluator": 20,
            "Gatekeeper": 10,
            "End User": 5
        }
        base_score += role_scores.get(contact.get('decision_role', ''), 0)

        # Tenure bonus (longer tenure = more influence)
        if 'tenure' in contact:
            if 'years' in contact['tenure']:
                years = int(contact['tenure'].split()[0])
                base_score += min(years * 2, 10)

        # LinkedIn influence
        if linkedin.get('connections', 0) > 2000:
            base_score += 5

        influence_score = min(base_score, 100)

        # Determine relationship status
        if contact.get('graph_data', {}).get('email_interactions', 0) == 0:
            relationship = "❌ NONE"
            relationship_color = "red"
        elif contact.get('graph_data', {}).get('email_interactions', 0) < 5:
            relationship = "🟡 WEAK"
            relationship_color = "yellow"
        else:
            relationship = "✅ STRONG"
            relationship_color = "green"

        return {
            "name": contact['full_name'],
            "title": contact['job_title'],
            "influence_score": influence_score,
            "influence_label": f"{influence_score}/100 - {contact.get('decision_role', 'Unknown')}",
            "tenure": contact.get('tenure', 'Unknown'),
            "relationship": relationship,
            "relationship_color": relationship_color,
            "background": linkedin.get('career_summary', 'Unknown'),
            "email_interactions": contact.get('graph_data', {}).get('email_interactions', 0),
            "last_contact": contact.get('graph_data', {}).get('last_contact', 'Never'),
            "action_needed": self._recommend_action(contact, relationship)
        }

    def _recommend_action(self, contact: Dict, relationship: str) -> str:
        """Recommend next action for this stakeholder"""
        if "NONE" in relationship:
            return f"URGENT: Establish contact with {contact['full_name']}"
        elif "WEAK" in relationship:
            return f"Re-engage {contact['full_name']} - schedule meeting"
        else:
            return f"Maintain relationship with {contact['full_name']}"

    def _analyze_decision_dynamics(self, buying_committee: List[Dict]) -> Dict[str, Any]:
        """Analyze how the buying committee makes decisions"""
        return {
            "Decision Timeline": "45-60 days (before renewal deadline)",
            "Evaluation Process": "Technical POC + Business case + Procurement",
            "Consensus Required": f"All {len(buying_committee)} stakeholders must approve",
            "Key Influencer": buying_committee[0]['name'] if buying_committee else "Unknown",
            "Current Sentiment": "🟡 Mixed - Champion supportive, CTO unknown"
        }

    def _identify_engagement_gaps(self, buying_committee: List[Dict]) -> List[str]:
        """Identify stakeholders with no/weak engagement"""
        gaps = []
        for stakeholder in buying_committee:
            if "NONE" in stakeholder['relationship'] or "WEAK" in stakeholder['relationship']:
                gaps.append(f"{stakeholder['name']} ({stakeholder['title']}) - {stakeholder['relationship']}")
        return gaps if gaps else ["No major gaps - all stakeholders engaged"]

    def _get_contact_details(self, contact_id: str) -> Dict[str, Any]:
        """Get detailed contact information"""
        # Mock - in production, call Dynamics API
        return {
            "contact_id": contact_id,
            "full_name": "Dr. Sarah Chen",
            "job_title": "Chief Technology Officer",
            "email": "sarah.chen@contoso.com",
            "tenure": "6 weeks (started Nov 1, 2024)",
            "current_projects": ["Project Phoenix - $200M cloud migration", "AI Integration initiative"]
        }

    def _get_recent_activity(self, contact_id: str) -> Dict[str, Any]:
        """Get recent activity from Graph API and Dynamics"""
        return {
            "Last Email": "Oct 18, 2024 - Support ticket escalation",
            "Last Meeting": "Never - No meetings scheduled",
            "LinkedIn Activity": "Posted 6 times in last 30 days about manufacturing AI",
            "Recent News": "Keynote speaker at ManufacturingTech Summit (Feb 2025)"
        }

    def _analyze_communication_style(self, graph_data: Dict) -> str:
        """Analyze communication patterns from email data"""
        avg_response = graph_data.get('graph_data', {}).get('response_time_avg', 'Unknown')
        return f"Data-driven, responds in {avg_response}, prefers morning meetings"

    def _recommend_engagement_strategy(self, contact: Dict, linkedin: Dict) -> Dict[str, Any]:
        """Recommend how to engage with this stakeholder"""
        return {
            "First Touch": "LinkedIn connection + thoughtful note (NOT sales pitch)",
            "Message Angle": "Mutual connection introduction",
            "Meeting Ask": "30min Tuesday 7:30am coffee | Her office",
            "Meeting Format": "15min demo + 15min Q&A | Zero slides",
            "Credibility Builder": "Reference mutual connections or shared interests"
        }

    def _calculate_relationship_strength(self, contact_id: str) -> str:
        """Calculate overall relationship strength"""
        # Mock calculation - in production, analyze all interactions
        return "3/10 - WEAK (needs immediate attention)"

    def _relationship_health(self, account_id: str) -> Dict[str, Any]:
        """Overall relationship health across all stakeholders"""
        contacts = self._get_dynamics_contacts(account_id)
        enriched = [self._enrich_contact_with_graph(c) for c in contacts]

        total_interactions = sum(c.get('graph_data', {}).get('email_interactions', 0) for c in enriched)
        avg_interactions = total_interactions / len(enriched) if enriched else 0

        return {
            "status": "success",
            "data": {
                "Overall Health": "🟡 MODERATE" if avg_interactions > 5 else "🔴 POOR",
                "Total Stakeholders": len(enriched),
                "Strong Relationships": sum(1 for c in enriched if c.get('graph_data', {}).get('email_interactions', 0) > 10),
                "Weak Relationships": sum(1 for c in enriched if c.get('graph_data', {}).get('email_interactions', 0) < 5),
                "No Contact": sum(1 for c in enriched if c.get('graph_data', {}).get('email_interactions', 0) == 0),
                "Recommendation": "Immediate action required to strengthen relationships"
            }
        }

    def _influence_mapping(self, account_id: str) -> Dict[str, Any]:
        """Create influence map showing who influences whom"""
        return {
            "status": "success",
            "data": {
                "Power Structure": {
                    "CEO Patricia Miller": "Ultimate decision authority",
                    "CTO Sarah Chen": "Reports to CEO | Primary economic buyer",
                    "CFO Robert Martinez": "Reports to CEO | Budget approver",
                    "VP Engineering James Liu": "Reports to CTO | Your champion",
                    "VP Operations David Kumar": "Reports to VP Engineering | End user"
                },
                "Coalition Dynamics": "CTO + CFO must both approve for deal to proceed",
                "Your Champions": ["James Liu (VP Engineering)"],
                "Blockers": ["None identified yet"],
                "Influencers": ["CTO has strong influence over all technology decisions"]
            }
        }


if __name__ == "__main__":
    # Test the agent
    agent = StakeholderIntelligenceAgent()

    result = agent.perform(
        operation="analyze_buying_committee",
        account_id="CONTOSO001"
    )

    print(json.dumps(result, indent=2))
