import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from agents.d365_base_agent import D365BaseAgent
import json
import random
from datetime import datetime, timedelta


class DealRiskAssessmentAgent(D365BaseAgent):
    """
    Identifies and quantifies risks threatening deal closure
    Analyzes timeline, engagement, competitive, budget, stakeholder, and process risks
    """

    def __init__(self):
        self.name = "DealRiskAssessmentAgent"
        self.metadata = {
            "name": self.name,
            "description": "Comprehensive risk assessment identifying timeline, engagement, competitive, budget, stakeholder, and process risks",
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
        """Perform comprehensive risk assessment"""
        opportunity_id = kwargs.get('opportunity_id')
        opportunity_name = kwargs.get('opportunity_name', 'Unknown Opportunity')

        try:
            if self.d365 and not self.d365.demo_mode and opportunity_id:
                risk_data = self._assess_d365_risks(opportunity_id)
            else:
                risk_data = self._generate_demo_risk_assessment(opportunity_name)

            return {
                "status": "success",
                "message": f"Risk assessment complete: {risk_data['overall_risk_level']} risk level with {risk_data['total_identified_risks']} risks",
                "data": risk_data
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to assess risks: {str(e)}",
                "data": {}
            }

    def _assess_d365_risks(self, opportunity_id):
        """Assess risks from D365 data"""
        return {}

    def _generate_demo_risk_assessment(self, opportunity_name):
        """Generate realistic demo risk assessment"""
        # Generate risk categories with realistic data
        timeline_risks = self._generate_timeline_risks()
        engagement_risks = self._generate_engagement_risks()
        competitive_risks = self._generate_competitive_risks()
        budget_risks = self._generate_budget_risks()
        stakeholder_risks = self._generate_stakeholder_risks()
        process_risks = self._generate_process_risks()

        risk_categories = {
            "timeline_risks": timeline_risks,
            "engagement_risks": engagement_risks,
            "competitive_risks": competitive_risks,
            "budget_risks": budget_risks,
            "stakeholder_risks": stakeholder_risks,
            "process_risks": process_risks
        }

        # Calculate overall risk
        total_risks = sum(len(cat["risks"]) for cat in risk_categories.values())
        avg_severity_score = sum(cat["score"] for cat in risk_categories.values()) / len(risk_categories)

        if avg_severity_score >= 70:
            overall_risk = "High"
        elif avg_severity_score >= 50:
            overall_risk = "Medium"
        else:
            overall_risk = "Low"

        # Generate immediate actions
        immediate_actions = []
        for category_name, category in risk_categories.items():
            if category["severity"] == "High" and category["risks"]:
                immediate_actions.append(category["risks"][0]["mitigation"])

        return {
            "opportunity_id": f"opp-{random.randint(1000, 9999)}",
            "opportunity_name": opportunity_name,
            "overall_risk_level": overall_risk,
            "risk_score": round(avg_severity_score),
            "total_identified_risks": total_risks,
            "risk_categories": risk_categories,
            "recommended_immediate_actions": immediate_actions[:3]
        }

    def _generate_timeline_risks(self):
        """Generate timeline-related risks"""
        days_to_close = random.randint(10, 60)
        days_in_stage = random.randint(5, 35)

        risks = []

        if days_to_close < 20:
            risks.append({
                "risk": f"Close date in {days_to_close} days",
                "impact": "High",
                "probability": 0.9,
                "mitigation": "Expedite proposal review, schedule urgency call with decision makers"
            })

        if days_in_stage > 20:
            risks.append({
                "risk": f"In current stage for {days_in_stage} days (average is 14)",
                "impact": "Medium",
                "probability": 0.8,
                "mitigation": "Identify and address blockers, escalate internally if needed"
            })

        severity = "High" if len(risks) >= 2 else "Medium" if len(risks) == 1 else "Low"
        score = 85 if severity == "High" else 60 if severity == "Medium" else 30

        return {
            "severity": severity,
            "score": score,
            "risks": risks
        }

    def _generate_engagement_risks(self):
        """Generate engagement-related risks"""
        days_since_activity = random.randint(0, 20)
        days_since_exec_contact = random.randint(15, 60)

        risks = []

        if days_since_activity > 10:
            risks.append({
                "risk": f"No activities in {days_since_activity} days",
                "impact": "High",
                "probability": 0.7,
                "mitigation": "Immediate outreach to primary contact, schedule follow-up meeting"
            })

        if days_since_exec_contact > 30:
            risks.append({
                "risk": f"Executive stakeholder not engaged in {days_since_exec_contact} days",
                "impact": "High",
                "probability": 0.85,
                "mitigation": "Request executive briefing with C-level stakeholders"
            })

        severity = "High" if len(risks) >= 2 else "Medium" if len(risks) == 1 else "Low"
        score = 75 if severity == "High" else 50 if severity == "Medium" else 25

        return {
            "severity": severity,
            "score": score,
            "risks": risks
        }

    def _generate_competitive_risks(self):
        """Generate competitive risks"""
        num_competitors = random.randint(0, 3)

        risks = []

        if num_competitors >= 2:
            risks.append({
                "risk": f"{num_competitors} competitors identified",
                "impact": "Medium",
                "probability": 0.6,
                "mitigation": "Share competitive differentiators and battle cards, provide comparison matrix"
            })

        severity = "Medium" if num_competitors >= 2 else "Low"
        score = 60 if severity == "Medium" else 30

        return {
            "severity": severity,
            "score": score,
            "risks": risks
        }

    def _generate_budget_risks(self):
        """Generate budget-related risks"""
        budget_confirmed = random.choice([True, False])

        risks = []

        if not budget_confirmed:
            risks.append({
                "risk": "Budget status unconfirmed",
                "impact": "High",
                "probability": 0.4,
                "mitigation": "Qualify budget in next call, provide ROI justification"
            })

        severity = "Low" if budget_confirmed else "Medium"
        score = 30 if budget_confirmed else 55

        return {
            "severity": severity,
            "score": score,
            "risks": risks
        }

    def _generate_stakeholder_risks(self):
        """Generate stakeholder risks"""
        decision_maker_mapped = random.choice([True, False])

        risks = []

        if not decision_maker_mapped:
            risks.append({
                "risk": "Final decision maker not identified",
                "impact": "High",
                "probability": 0.9,
                "mitigation": "Work with champion to identify and engage decision maker"
            })

        severity = "High" if not decision_maker_mapped else "Low"
        score = 80 if severity == "High" else 20

        return {
            "severity": severity,
            "score": score,
            "risks": risks
        }

    def _generate_process_risks(self):
        """Generate process risks"""
        quote_sent = random.choice([True, False])

        risks = []

        if not quote_sent:
            risks.append({
                "risk": "Formal quote not yet sent",
                "impact": "Medium",
                "probability": 0.7,
                "mitigation": "Complete and send quote within 48 hours with clear value justification"
            })

        severity = "Medium" if not quote_sent else "Low"
        score = 55 if not quote_sent else 25

        return {
            "severity": severity,
            "score": score,
            "risks": risks
        }


if __name__ == "__main__":
    agent = DealRiskAssessmentAgent()
    result = agent.perform(opportunity_name="Fabrikam Digital Transformation")
    print(json.dumps(result, indent=2))
