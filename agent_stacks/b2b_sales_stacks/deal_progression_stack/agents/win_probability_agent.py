import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from agents.d365_base_agent import D365BaseAgent
import json
import random


class WinProbabilityAgent(D365BaseAgent):
    """
    Calculates data-driven win probability based on deal characteristics and historical patterns
    Uses AI to analyze multiple factors and predict deal success
    """

    def __init__(self):
        self.name = "WinProbabilityAgent"
        self.metadata = {
            "name": self.name,
            "description": "Calculates AI-driven win probability based on deal characteristics, process completion, engagement, and historical patterns",
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

        # Probability factor weights
        self.weights = {
            "deal_characteristics": 0.15,
            "sales_process": 0.30,
            "engagement_metrics": 0.25,
            "competitive_situation": 0.15,
            "timeline_alignment": 0.15
        }

    def perform(self, **kwargs):
        """Calculate win probability"""
        opportunity_id = kwargs.get('opportunity_id')
        opportunity_name = kwargs.get('opportunity_name', 'Unknown Opportunity')

        try:
            if self.d365 and not self.d365.demo_mode and opportunity_id:
                probability_data = self._calculate_from_d365(opportunity_id)
            else:
                probability_data = self._generate_demo_probability(opportunity_name)

            return {
                "status": "success",
                "message": f"Win probability calculated: {probability_data['calculated_win_probability']}% (adjusted from {probability_data['sales_rep_probability']}%)",
                "data": probability_data
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to calculate win probability: {str(e)}",
                "data": {}
            }

    def _calculate_from_d365(self, opportunity_id):
        """Calculate probability from D365 data"""
        return {}

    def _generate_demo_probability(self, opportunity_name):
        """Generate realistic demo probability calculation"""
        # Sales rep's subjective probability
        sales_rep_prob = random.randint(65, 85)

        # Generate factor scores
        factors = {
            "deal_characteristics": self._generate_deal_characteristics(),
            "sales_process": self._generate_sales_process(),
            "engagement_metrics": self._generate_engagement_metrics(),
            "competitive_situation": self._generate_competitive_situation(),
            "timeline_alignment": self._generate_timeline_alignment()
        }

        # Calculate weighted probability
        calculated_prob = 0
        for factor_name, factor_data in factors.items():
            calculated_prob += factor_data['score'] * self.weights[factor_name]

        calculated_prob = int(calculated_prob)

        # Calculate confidence interval
        confidence_low = max(40, calculated_prob - random.randint(5, 10))
        confidence_high = min(95, calculated_prob + random.randint(5, 10))

        # Generate risk adjustments
        risk_adjustments = self._generate_risk_adjustments(factors)

        # Generate recommendations
        recommendations = self._generate_recommendations(factors)

        # Generate similar historical deals
        similar_deals = {
            "sample_size": random.randint(18, 35),
            "won": random.randint(10, 20),
            "lost": 0,
            "win_rate": 0,
            "avg_deal_size": random.randint(350000, 550000),
            "similarity_score": round(random.uniform(0.80, 0.90), 2)
        }
        similar_deals["lost"] = similar_deals["sample_size"] - similar_deals["won"]
        similar_deals["win_rate"] = round(similar_deals["won"] / similar_deals["sample_size"], 2)

        return {
            "opportunity_id": f"opp-{random.randint(1000, 9999)}",
            "opportunity_name": opportunity_name,
            "sales_rep_probability": sales_rep_prob,
            "calculated_win_probability": calculated_prob,
            "confidence_interval": {
                "low": confidence_low,
                "high": confidence_high
            },
            "probability_factors": factors,
            "risk_adjustments": risk_adjustments,
            "recommendations_to_improve": recommendations,
            "similar_historical_deals": similar_deals
        }

    def _generate_deal_characteristics(self):
        """Generate deal characteristics factor"""
        deal_size = random.randint(300000, 600000)
        industry_win_rate = random.uniform(0.60, 0.75)
        fit_score = random.randint(75, 92)

        score = int((industry_win_rate * 100 + fit_score) / 2)

        return {
            "contribution": self.weights["deal_characteristics"],
            "score": score,
            "factors": {
                "deal_size": {
                    "value": deal_size,
                    "value_formatted": self.format_currency(deal_size),
                    "category": "Medium Enterprise",
                    "historical_win_rate": round(industry_win_rate, 2),
                    "impact": "Positive"
                },
                "industry": {
                    "value": random.choice(["Technology", "Manufacturing", "Retail", "Healthcare"]),
                    "historical_win_rate": round(industry_win_rate, 2),
                    "impact": "Positive"
                },
                "account_size": {
                    "value": f"${random.randint(50, 200)}M revenue",
                    "fit_score": fit_score,
                    "impact": "Positive"
                }
            }
        }

    def _generate_sales_process(self):
        """Generate sales process factor"""
        days_in_stage = random.randint(10, 30)
        completion_rate = random.uniform(0.55, 0.75)
        stage_win_rate = random.uniform(0.55, 0.70)

        score = int((completion_rate * 100 + stage_win_rate * 100) / 2)

        return {
            "contribution": self.weights["sales_process"],
            "score": score,
            "factors": {
                "stage_progression": {
                    "current_stage": random.choice(["Develop", "Propose"]),
                    "historical_win_rate_from_stage": round(stage_win_rate, 2),
                    "days_in_stage": days_in_stage,
                    "typical_days": 14,
                    "impact": "Neutral" if days_in_stage < 20 else "Negative"
                },
                "activity_completion": {
                    "completed": int(completion_rate * 15),
                    "required": 15,
                    "completion_rate": round(completion_rate, 2),
                    "impact": "Neutral" if completion_rate >= 0.65 else "Negative"
                }
            }
        }

    def _generate_engagement_metrics(self):
        """Generate engagement metrics factor"""
        engaged_stakeholders = random.randint(2, 4)
        decision_makers_engaged = random.randint(1, 2)
        activities_30days = random.randint(5, 15)

        champion_identified = random.choice([True, False])

        score_base = (engaged_stakeholders / 4) * 50 + (decision_makers_engaged / 3) * 30
        score_activity = min(20, (activities_30days / 12) * 20)
        score = int(score_base + score_activity)

        return {
            "contribution": self.weights["engagement_metrics"],
            "score": score,
            "factors": {
                "stakeholder_engagement": {
                    "engaged_stakeholders": engaged_stakeholders,
                    "decision_makers_engaged": decision_makers_engaged,
                    "champion_identified": champion_identified,
                    "impact": "Positive" if champion_identified and decision_makers_engaged >= 2 else "Neutral"
                },
                "activity_frequency": {
                    "activities_last_30_days": activities_30days,
                    "expected": 12,
                    "trend": "Increasing" if activities_30days >= 12 else "Declining",
                    "impact": "Positive" if activities_30days >= 10 else "Negative"
                }
            }
        }

    def _generate_competitive_situation(self):
        """Generate competitive situation factor"""
        num_competitors = random.randint(0, 3)
        win_rate_vs_comp = random.uniform(0.45, 0.65)

        score = int((1 - (num_competitors * 0.15)) * 100)
        score = max(30, score)

        competitors = []
        if num_competitors > 0:
            possible_competitors = ["Salesforce", "HubSpot", "Microsoft", "Oracle"]
            competitors = random.sample(possible_competitors, min(num_competitors, len(possible_competitors)))

        return {
            "contribution": self.weights["competitive_situation"],
            "score": score,
            "factors": {
                "competitors_present": num_competitors,
                "competitor_names": competitors,
                "historical_win_rate_vs_competition": round(win_rate_vs_comp, 2),
                "impact": "Low" if num_competitors == 0 else "Negative"
            }
        }

    def _generate_timeline_alignment(self):
        """Generate timeline alignment factor"""
        days_to_close = random.randint(20, 70)
        urgency = days_to_close < 40

        score = 85 if urgency else 65

        return {
            "contribution": self.weights["timeline_alignment"],
            "score": score,
            "factors": {
                "days_to_close": days_to_close,
                "alignment_with_buyer_timeline": "Good" if urgency else "Moderate",
                "urgency_indicators": urgency,
                "impact": "Positive" if urgency else "Neutral"
            }
        }

    def _generate_risk_adjustments(self, factors):
        """Generate risk adjustments"""
        adjustments = []

        # Check engagement
        engagement_score = factors["engagement_metrics"]["score"]
        if engagement_score < 55:
            adjustments.append({
                "risk": "Below-average stakeholder engagement",
                "probability_impact": random.randint(-10, -5),
                "reasoning": "Limited decision maker engagement reduces win likelihood"
            })

        # Check competition
        num_competitors = factors["competitive_situation"]["factors"]["competitors_present"]
        if num_competitors >= 2:
            adjustments.append({
                "risk": "Multiple competitors",
                "probability_impact": random.randint(-8, -4),
                "reasoning": f"Historical win rate drops with {num_competitors}+ competitors"
            })

        # Check process
        process_score = factors["sales_process"]["score"]
        if process_score < 60:
            adjustments.append({
                "risk": "Slow stage progression",
                "probability_impact": random.randint(-6, -3),
                "reasoning": "Longer than typical deal cycle indicates potential issues"
            })

        return adjustments

    def _generate_recommendations(self, factors):
        """Generate recommendations to improve probability"""
        recommendations = []

        engagement = factors["engagement_metrics"]["factors"]["stakeholder_engagement"]
        if not engagement["champion_identified"] or engagement["decision_makers_engaged"] < 2:
            recommendations.append({
                "action": "Engage remaining decision makers and identify champion",
                "potential_impact": "+10-15% probability",
                "priority": "High"
            })

        process = factors["sales_process"]["factors"]["activity_completion"]
        if process["completion_rate"] < 0.70:
            recommendations.append({
                "action": "Complete pending stage activities",
                "potential_impact": "+5-8% probability",
                "priority": "High"
            })

        competitive = factors["competitive_situation"]["factors"]
        if competitive["competitors_present"] > 0:
            recommendations.append({
                "action": "Share competitive differentiators and customer references",
                "potential_impact": "+5-7% probability",
                "priority": "Medium"
            })

        engagement_freq = factors["engagement_metrics"]["factors"]["activity_frequency"]
        if engagement_freq["activities_last_30_days"] < 12:
            recommendations.append({
                "action": "Increase engagement frequency to weekly touchpoints",
                "potential_impact": "+4-6% probability",
                "priority": "Medium"
            })

        return recommendations[:4]


if __name__ == "__main__":
    agent = WinProbabilityAgent()
    result = agent.perform(opportunity_name="Tailspin Toys Digital Platform")
    print(json.dumps(result, indent=2))
