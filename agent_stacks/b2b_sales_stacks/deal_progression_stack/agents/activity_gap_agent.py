import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from agents.d365_base_agent import D365BaseAgent
import json
import random
from datetime import datetime, timedelta


class ActivityGapAgent(D365BaseAgent):
    """
    Detects missing critical activities required for each sales stage
    Identifies gaps between completed and required activities
    """

    def __init__(self):
        self.name = "ActivityGapAgent"
        self.metadata = {
            "name": self.name,
            "description": "Identifies missing critical activities for current sales stage and provides completion roadmap",
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
                        "description": "Current sales stage"
                    }
                },
                "required": []
            }
        }
        super().__init__(name=self.name, metadata=self.metadata)

        # Define stage requirements
        self.stage_requirements = {
            "Qualify": [
                "Discovery call",
                "Needs assessment",
                "Budget discussion",
                "Timeline alignment"
            ],
            "Develop": [
                "Product demo",
                "Technical deep dive",
                "Stakeholder meeting",
                "Security review",
                "Use case validation"
            ],
            "Propose": [
                "Quote sent",
                "Proposal presented",
                "ROI analysis shared",
                "Executive briefing",
                "Reference calls"
            ],
            "Close": [
                "Contract review",
                "Legal approval",
                "Final negotiation",
                "Implementation planning"
            ]
        }

    def perform(self, **kwargs):
        """Identify activity gaps"""
        opportunity_id = kwargs.get('opportunity_id')
        opportunity_name = kwargs.get('opportunity_name', 'Unknown Opportunity')
        current_stage = kwargs.get('current_stage', 'Develop')

        try:
            if self.d365 and not self.d365.demo_mode and opportunity_id:
                gap_data = self._analyze_d365_gaps(opportunity_id)
            else:
                gap_data = self._generate_demo_gap_analysis(opportunity_name, current_stage)

            return {
                "status": "success",
                "message": f"Activity gap analysis complete: {len(gap_data['gaps_identified'])} gaps identified",
                "data": gap_data
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to identify activity gaps: {str(e)}",
                "data": {}
            }

    def _analyze_d365_gaps(self, opportunity_id):
        """Analyze gaps from D365 data"""
        return {}

    def _generate_demo_gap_analysis(self, opportunity_name, current_stage):
        """Generate realistic demo gap analysis"""
        all_stages = ["Qualify", "Develop", "Propose", "Close"]
        current_stage_index = all_stages.index(current_stage) if current_stage in all_stages else 1

        required_activities = {}

        # Process each stage
        for idx, stage in enumerate(all_stages):
            requirements = self.stage_requirements.get(stage, [])
            activities = []

            for activity in requirements:
                if idx < current_stage_index:
                    # Past stage - all complete
                    completed = True
                    date = (datetime.now() - timedelta(days=random.randint(15, 45))).strftime('%Y-%m-%d')
                    activities.append({
                        "activity": activity,
                        "completed": completed,
                        "date": date
                    })
                elif idx == current_stage_index:
                    # Current stage - some complete, some missing
                    completed = random.choice([True, False])
                    if completed:
                        date = (datetime.now() - timedelta(days=random.randint(1, 15))).strftime('%Y-%m-%d')
                        activities.append({
                            "activity": activity,
                            "completed": completed,
                            "date": date
                        })
                    else:
                        required_by = (datetime.now() + timedelta(days=random.randint(3, 14))).strftime('%Y-%m-%d')
                        activities.append({
                            "activity": activity,
                            "completed": completed,
                            "required_by": required_by
                        })
                else:
                    # Future stage - not started
                    activities.append({
                        "activity": activity,
                        "completed": False,
                        "required_by": "Stage entry"
                    })

            # Calculate completion rate
            completed_count = sum(1 for a in activities if a['completed'])
            completion_rate = completed_count / len(activities) if activities else 0

            # Determine status
            if idx < current_stage_index:
                status = "Complete"
            elif idx == current_stage_index:
                status = "In Progress"
            else:
                status = "Not Started"

            # Identify missing critical activities for current stage
            missing_critical = []
            if status == "In Progress":
                missing_critical = [a['activity'] for a in activities if not a['completed']]

            required_activities[f"{stage.lower()}_stage"] = {
                "status": status,
                "completion_rate": round(completion_rate, 2),
                "activities": activities
            }

            if missing_critical:
                required_activities[f"{stage.lower()}_stage"]["missing_critical"] = missing_critical

        # Identify gaps
        gaps = self._identify_gaps(required_activities, current_stage)

        # Generate timeline
        timeline = self._generate_timeline(gaps)

        # Calculate completeness score
        all_activities = []
        for stage_data in required_activities.values():
            all_activities.extend(stage_data['activities'])

        completed = sum(1 for a in all_activities if a['completed'])
        total = len(all_activities)
        completeness_score = int((completed / total) * 100) if total > 0 else 0

        return {
            "opportunity_id": f"opp-{random.randint(1000, 9999)}",
            "opportunity_name": opportunity_name,
            "current_stage": current_stage,
            "completeness_score": completeness_score,
            "required_activities": required_activities,
            "gaps_identified": gaps,
            "recommended_timeline": timeline
        }

    def _identify_gaps(self, required_activities, current_stage):
        """Identify critical gaps"""
        gaps = []

        for stage_name, stage_data in required_activities.items():
            if stage_data["status"] == "In Progress":
                missing = stage_data.get("missing_critical", [])

                for activity in missing:
                    gap = {
                        "gap": f"No {activity.lower()} scheduled or completed",
                        "stage": current_stage,
                        "priority": "High",
                        "impact": self._get_gap_impact(activity, current_stage),
                        "recommendation": self._get_gap_recommendation(activity)
                    }
                    gaps.append(gap)

        # Limit to top 5 most critical gaps
        return gaps[:5]

    def _get_gap_impact(self, activity, stage):
        """Get impact description for gap"""
        impacts = {
            "Stakeholder meeting": "Cannot advance to Propose without stakeholder buy-in",
            "Security review": "May delay deal closure if security concerns arise later",
            "ROI analysis": "Proposal will lack financial justification",
            "Quote sent": "Cannot formally advance proposal discussions",
            "Executive briefing": "Risk of losing high-value deal without executive alignment"
        }

        return impacts.get(activity, f"Required activity for {stage} stage not completed")

    def _get_gap_recommendation(self, activity):
        """Get recommendation for gap"""
        recommendations = {
            "Stakeholder meeting": "Schedule meeting with VP and Director-level stakeholders within 5 days",
            "Security review": "Engage security team immediately, typical review takes 2 weeks",
            "ROI analysis": "Complete ROI calculator with customer data before quote",
            "Quote sent": "Finalize and send formal quote within 48 hours",
            "Product demo": "Schedule customized demo highlighting top 3 customer pain points",
            "Executive briefing": "Request executive sponsor to facilitate C-level introduction"
        }

        return recommendations.get(activity, f"Complete {activity} before advancing to next stage")

    def _generate_timeline(self, gaps):
        """Generate recommended timeline for completing gaps"""
        timeline = []
        current_date = datetime.now()

        for i, gap in enumerate(gaps[:4]):  # Top 4 gaps
            action_date = current_date + timedelta(days=(i+1)*2)
            timeline.append({
                "date": action_date.strftime('%Y-%m-%d'),
                "action": gap['recommendation']
            })

        # Add stage advancement date
        advance_date = current_date + timedelta(days=len(timeline)*2 + 5)
        timeline.append({
            "date": advance_date.strftime('%Y-%m-%d'),
            "action": "Ready to advance to next stage"
        })

        return timeline


if __name__ == "__main__":
    agent = ActivityGapAgent()
    result = agent.perform(
        opportunity_name="Wide World Importers CRM",
        current_stage="Develop"
    )
    print(json.dumps(result, indent=2))
