import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from agents.d365_base_agent import D365BaseAgent
import json
from datetime import datetime
import random


class DealHealthScoreAgent(D365BaseAgent):
    """
    Calculates comprehensive health score (0-100) for opportunities
    Analyzes engagement, momentum, alignment, completeness, and risk factors
    """

    def __init__(self):
        self.name = "DealHealthScoreAgent"
        self.metadata = {
            "name": self.name,
            "description": "Calculates comprehensive deal health score based on engagement, momentum, alignment, completeness, and risk",
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

        # Health factor weights
        self.weights = {
            "engagement": 0.30,
            "momentum": 0.25,
            "alignment": 0.20,
            "completeness": 0.15,
            "risk": 0.10
        }

    def perform(self, **kwargs):
        """Calculate deal health score"""
        opportunity_id = kwargs.get('opportunity_id')
        opportunity_name = kwargs.get('opportunity_name', 'Unknown Opportunity')

        try:
            if self.d365 and not self.d365.demo_mode and opportunity_id:
                # Real D365 query
                result = self.d365.get_opportunity_by_id(
                    opportunity_id,
                    expand="Opportunity_Tasks,Opportunity_Appointments,Opportunity_Emails",
                    select="name,stepname,estimatedvalue,closeprobability,estimatedclosedate,createdon,modifiedon"
                )
                health_data = self._calculate_health_from_d365(result)
            else:
                # Demo mode
                health_data = self._calculate_health_demo(opportunity_name)

            # Calculate overall health score
            overall_score = self._calculate_overall_score(health_data['factors'])
            health_data['health_score'] = overall_score
            health_data['health_rating'] = self.get_health_rating(overall_score)
            health_data['trend'] = self._determine_trend(health_data['factors'])

            return {
                "status": "success",
                "message": f"Health score calculated: {overall_score}/100 ({health_data['health_rating']})",
                "data": health_data
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to calculate health score: {str(e)}",
                "data": {}
            }

    def _calculate_health_from_d365(self, opp_data):
        """Calculate health metrics from D365 data"""
        # This would contain real D365 data processing logic
        # For now, returning structured format
        return {
            "opportunity_id": opp_data.get('opportunityid'),
            "opportunity_name": opp_data.get('name'),
            "factors": {
                "engagement": self._calculate_engagement_score(opp_data),
                "momentum": self._calculate_momentum_score(opp_data),
                "alignment": self._calculate_alignment_score(opp_data),
                "completeness": self._calculate_completeness_score(opp_data),
                "risk": self._calculate_risk_score(opp_data)
            }
        }

    def _calculate_health_demo(self, opportunity_name):
        """Generate realistic demo health data"""
        # Generate realistic scores for demo
        engagement_score = random.randint(65, 95)
        momentum_score = random.randint(60, 85)
        alignment_score = random.randint(70, 90)
        completeness_score = random.randint(50, 80)
        risk_score = random.randint(75, 95)

        return {
            "opportunity_id": f"opp-{random.randint(1000, 9999)}",
            "opportunity_name": opportunity_name,
            "factors": {
                "engagement": {
                    "score": engagement_score,
                    "weight": self.weights["engagement"],
                    "indicators": {
                        "activities_last_30_days": random.randint(10, 25),
                        "stakeholder_meetings": random.randint(3, 8),
                        "response_rate": f"{random.randint(75, 95)}%",
                        "email_engagement": f"{random.randint(60, 90)}%"
                    }
                },
                "momentum": {
                    "score": momentum_score,
                    "weight": self.weights["momentum"],
                    "indicators": {
                        "days_in_current_stage": random.randint(5, 20),
                        "stage_progression_rate": random.choice(["Fast", "Normal", "Slow"]),
                        "last_activity": f"{random.randint(1, 5)} days ago",
                        "velocity_vs_average": f"{random.randint(-15, 25):+d}%"
                    }
                },
                "alignment": {
                    "score": alignment_score,
                    "weight": self.weights["alignment"],
                    "indicators": {
                        "budget_confirmed": random.choice([True, False]),
                        "timeline_fit": random.choice(["Q4 2025", "Q1 2026", "H1 2026"]),
                        "decision_process_mapped": random.choice([True, False]),
                        "champion_identified": random.choice([True, False])
                    }
                },
                "completeness": {
                    "score": completeness_score,
                    "weight": self.weights["completeness"],
                    "indicators": {
                        "activities_complete": f"{random.randint(10, 18)}/20",
                        "documents_shared": random.randint(5, 15),
                        "quote_sent": random.choice([True, False]),
                        "stakeholder_coverage": f"{random.randint(60, 90)}%"
                    }
                },
                "risk": {
                    "score": risk_score,
                    "weight": self.weights["risk"],
                    "indicators": {
                        "competitors_present": random.randint(0, 2),
                        "stalled_days": random.randint(0, 5),
                        "past_due_activities": random.randint(0, 3),
                        "budget_risk": random.choice(["Low", "Medium"])
                    }
                }
            }
        }

    def _calculate_engagement_score(self, opp_data):
        """Calculate engagement score from D365 activities"""
        # Placeholder - would analyze actual activity data
        return {
            "score": 80,
            "weight": self.weights["engagement"],
            "indicators": {}
        }

    def _calculate_momentum_score(self, opp_data):
        """Calculate momentum score from D365 stage history"""
        return {
            "score": 75,
            "weight": self.weights["momentum"],
            "indicators": {}
        }

    def _calculate_alignment_score(self, opp_data):
        """Calculate alignment score from D365 opportunity fields"""
        return {
            "score": 85,
            "weight": self.weights["alignment"],
            "indicators": {}
        }

    def _calculate_completeness_score(self, opp_data):
        """Calculate completeness score from activities and documents"""
        return {
            "score": 70,
            "weight": self.weights["completeness"],
            "indicators": {}
        }

    def _calculate_risk_score(self, opp_data):
        """Calculate risk score (higher = lower risk)"""
        return {
            "score": 82,
            "weight": self.weights["risk"],
            "indicators": {}
        }

    def _calculate_overall_score(self, factors):
        """Calculate weighted overall health score"""
        total_score = 0
        for factor_name, factor_data in factors.items():
            total_score += factor_data['score'] * factor_data['weight']

        return round(total_score)

    def _determine_trend(self, factors):
        """Determine health trend based on momentum and engagement"""
        momentum_score = factors['momentum']['score']
        engagement_score = factors['engagement']['score']

        avg_score = (momentum_score + engagement_score) / 2

        if avg_score >= 75:
            return "Improving"
        elif avg_score >= 60:
            return "Stable"
        else:
            return "Declining"


if __name__ == "__main__":
    agent = DealHealthScoreAgent()

    # Test execution
    result = agent.perform(opportunity_name="Northwind SaaS Implementation")
    print(json.dumps(result, indent=2))
