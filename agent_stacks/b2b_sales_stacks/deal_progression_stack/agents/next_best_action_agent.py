import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from agents.d365_base_agent import D365BaseAgent
import json
from datetime import datetime


class NextBestActionAgent(D365BaseAgent):
    """
    Recommends optimal next actions based on opportunity stage and activity history
    Analyzes D365 data to suggest stage-specific actions
    """

    def __init__(self):
        self.name = "NextBestActionAgent"
        self.metadata = {
            "name": self.name,
            "description": "Recommends next best actions based on deal stage, activity history, and best practices",
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
                    },
                    "current_stage": {
                        "type": "string",
                        "description": "Current sales stage (for demo mode)"
                    }
                },
                "required": []
            }
        }
        super().__init__(name=self.name, metadata=self.metadata)

        # Stage-specific action templates
        self.stage_requirements = {
            "Qualify": [
                {"activity": "Discovery call", "category": "meeting"},
                {"activity": "Needs assessment", "category": "task"},
                {"activity": "Budget discussion", "category": "meeting"}
            ],
            "Develop": [
                {"activity": "Product demo", "category": "meeting"},
                {"activity": "Technical deep dive", "category": "meeting"},
                {"activity": "Stakeholder meeting", "category": "meeting"},
                {"activity": "Security review", "category": "task"}
            ],
            "Propose": [
                {"activity": "Quote sent", "category": "task"},
                {"activity": "Proposal presented", "category": "meeting"},
                {"activity": "ROI analysis shared", "category": "task"},
                {"activity": "Executive briefing", "category": "meeting"}
            ],
            "Close": [
                {"activity": "Contract review", "category": "meeting"},
                {"activity": "Legal approval", "category": "task"},
                {"activity": "Final negotiation", "category": "meeting"}
            ]
        }

    def perform(self, **kwargs):
        """Generate next best action recommendations"""
        opportunity_id = kwargs.get('opportunity_id')
        opportunity_name = kwargs.get('opportunity_name', 'Unknown Opportunity')
        current_stage = kwargs.get('current_stage', 'Develop')

        try:
            if self.d365 and not self.d365.demo_mode and opportunity_id:
                # Real D365 query
                result = self.d365.get_opportunity_by_id(
                    opportunity_id,
                    expand="Opportunity_Tasks($select=subject,statecode),Opportunity_Appointments($select=subject,statecode)",
                    select="name,stepname,estimatedvalue,closeprobability,estimatedclosedate"
                )

                opportunity_data = self._process_opportunity_data(result)
            else:
                # Demo mode
                opportunity_data = self._generate_demo_opportunity_data(opportunity_name, current_stage)

            # Generate recommendations
            recommendations = self._generate_recommendations(opportunity_data)

            return {
                "status": "success",
                "message": f"Generated {len(recommendations)} action recommendations for {opportunity_data['name']}",
                "data": {
                    "opportunity_id": opportunity_data.get('opportunity_id'),
                    "opportunity_name": opportunity_data['name'],
                    "current_stage": opportunity_data['current_stage'],
                    "estimated_value": self.format_currency(opportunity_data.get('estimated_value', 0)),
                    "close_probability": opportunity_data.get('close_probability', 0),
                    "recommended_actions": recommendations,
                    "stage_requirements": {
                        "completed": opportunity_data.get('completed_activities', []),
                        "missing": opportunity_data.get('missing_activities', [])
                    }
                }
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to generate recommendations: {str(e)}",
                "data": {}
            }

    def _process_opportunity_data(self, opp_data):
        """Process D365 opportunity data"""
        current_stage = opp_data.get('stepname', 'Develop')
        completed_activities = []
        missing_activities = []

        # Analyze completed vs required activities
        required = self.stage_requirements.get(current_stage, [])
        tasks = opp_data.get('Opportunity_Tasks', [])
        appointments = opp_data.get('Opportunity_Appointments', [])

        # Simplification: Check which activities exist
        for req in required:
            found = False
            for task in tasks + appointments:
                if req['activity'].lower() in task.get('subject', '').lower():
                    completed_activities.append(req['activity'])
                    found = True
                    break
            if not found:
                missing_activities.append(req['activity'])

        return {
            "opportunity_id": opp_data.get('opportunityid'),
            "name": opp_data.get('name'),
            "current_stage": current_stage,
            "estimated_value": opp_data.get('estimatedvalue', 0),
            "close_probability": opp_data.get('closeprobability', 0),
            "completed_activities": completed_activities,
            "missing_activities": missing_activities
        }

    def _generate_demo_opportunity_data(self, opportunity_name, current_stage):
        """Generate demo opportunity data"""
        import random

        all_requirements = self.stage_requirements.get(current_stage, [])
        num_completed = random.randint(1, max(1, len(all_requirements) - 2))

        completed = [req['activity'] for req in all_requirements[:num_completed]]
        missing = [req['activity'] for req in all_requirements[num_completed:]]

        return {
            "opportunity_id": f"opp-demo-{random.randint(1000, 9999)}",
            "name": opportunity_name,
            "current_stage": current_stage,
            "estimated_value": random.randint(200000, 800000),
            "close_probability": random.randint(50, 85),
            "completed_activities": completed,
            "missing_activities": missing,
            "days_in_stage": random.randint(5, 25),
            "has_competitors": random.choice([True, False]),
            "executive_engaged": random.choice([True, False])
        }

    def _generate_recommendations(self, opp_data):
        """Generate AI-powered action recommendations"""
        recommendations = []
        current_stage = opp_data['current_stage']
        value = opp_data.get('estimated_value', 0)
        missing = opp_data.get('missing_activities', [])
        days_in_stage = opp_data.get('days_in_stage', 10)

        # Priority 1: Missing critical stage activities
        if missing:
            for activity in missing[:2]:  # Top 2 missing activities
                recommendations.append({
                    "action": f"Complete {activity}",
                    "priority": "High",
                    "reasoning": f"Required activity for {current_stage} stage not yet completed",
                    "confidence": 0.92,
                    "expected_impact": "Enables stage progression",
                    "category": "Stage Requirement"
                })

        # Priority 2: High-value deal specific actions
        if value >= 500000 and not opp_data.get('executive_engaged', True):
            recommendations.append({
                "action": "Schedule executive briefing with C-level stakeholders",
                "priority": "High",
                "reasoning": f"Deal value ${value:,} requires executive sponsorship and alignment",
                "confidence": 0.89,
                "expected_impact": "Increase win probability by 15-20%",
                "category": "Stakeholder Engagement"
            })

        # Priority 3: Competitor response
        if opp_data.get('has_competitors', False):
            recommendations.append({
                "action": "Send competitive differentiation document and ROI comparison",
                "priority": "Medium",
                "reasoning": "Competitors identified, need to establish clear value proposition",
                "confidence": 0.82,
                "expected_impact": "Address competitive concerns proactively",
                "category": "Competitive Strategy"
            })

        # Priority 4: Stage velocity
        if days_in_stage > 20:
            recommendations.append({
                "action": "Identify and address blockers causing stage delay",
                "priority": "High",
                "reasoning": f"Deal in {current_stage} for {days_in_stage} days (typical: 14 days)",
                "confidence": 0.87,
                "expected_impact": "Accelerate deal progression",
                "category": "Deal Velocity"
            })

        # Priority 5: Stage-specific best practices
        stage_specific = self._get_stage_specific_actions(current_stage, opp_data)
        recommendations.extend(stage_specific)

        # Limit to top 5 recommendations
        return recommendations[:5]

    def _get_stage_specific_actions(self, stage, opp_data):
        """Get stage-specific recommended actions"""
        actions = []

        if stage == "Qualify":
            actions.append({
                "action": "Document BANT (Budget, Authority, Need, Timeline)",
                "priority": "Medium",
                "reasoning": "Ensure qualification criteria are met before investing resources",
                "confidence": 0.85,
                "expected_impact": "Improve forecast accuracy",
                "category": "Qualification"
            })

        elif stage == "Develop":
            actions.append({
                "action": "Create customized demo highlighting top 3 pain points",
                "priority": "Medium",
                "reasoning": "Personalized demos increase engagement and show value alignment",
                "confidence": 0.78,
                "expected_impact": "Strengthen solution fit perception",
                "category": "Solution Development"
            })

        elif stage == "Propose":
            actions.append({
                "action": "Provide customer references in similar industry and use case",
                "priority": "Medium",
                "reasoning": "Social proof reduces perceived risk during evaluation",
                "confidence": 0.81,
                "expected_impact": "Build confidence in solution and vendor",
                "category": "Trust Building"
            })

        elif stage == "Close":
            actions.append({
                "action": "Schedule final decision call with all stakeholders",
                "priority": "High",
                "reasoning": "Align all parties and address final concerns before signature",
                "confidence": 0.88,
                "expected_impact": "Accelerate close and prevent last-minute blockers",
                "category": "Deal Closure"
            })

        return actions


if __name__ == "__main__":
    agent = NextBestActionAgent()

    # Test execution
    result = agent.perform(
        opportunity_name="Contoso Enterprise CRM",
        current_stage="Develop"
    )
    print(json.dumps(result, indent=2))
