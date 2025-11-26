"""
Risk Assessment Agent
Predicts deal risks and calculates win probability

Data Sources:
- Dynamics 365 (deal history, health scores)
- Azure Machine Learning (predictive models)
- Historical win/loss data
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

from agents.basic_agent import BasicAgent
import json
from datetime import datetime
from typing import Dict, Any, List

class RiskAssessmentAgent(BasicAgent):
    def __init__(self):
        self.name = "RiskAssessmentAgent"
        self.metadata = {
            "name": self.name,
            "description": "Predicts deal risks and win probability using historical data and ML models"
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs) -> Dict[str, Any]:
        operation = kwargs.get('operation', 'assess_opportunity')
        account_id = kwargs.get('account_id')
        opportunity_id = kwargs.get('opportunity_id')

        if operation == "assess_opportunity":
            return self._assess_opportunity(account_id, opportunity_id)
        elif operation == "detailed_risk_analysis":
            return self._detailed_risk_analysis(account_id, opportunity_id)

    def _assess_opportunity(self, account_id: str, opportunity_id: str = None) -> Dict[str, Any]:
        """High-level opportunity assessment"""
        return {
            "status": "success",
            "operation": "assess_opportunity",
            "timestamp": datetime.now().isoformat(),
            "data": {
                "risk_level": "🟡 MODERATE-HIGH",
                "win_probability": 47,
                "trending": "⬇️ Declining (was 52% last month)",
                "priority": "HIGH - At-risk renewal + expansion opportunity",
                "action_required": "URGENT - Immediate intervention needed"
            }
        }

    def _detailed_risk_analysis(self, account_id: str, opportunity_id: str = None) -> Dict[str, Any]:
        """Detailed risk breakdown with mitigation strategies"""

        # Analyze multiple risk dimensions
        relationship_risks = self._analyze_relationship_risks(account_id)
        competitive_risks = self._analyze_competitive_risks(account_id)
        process_risks = self._analyze_process_risks(account_id)
        timing_risks = self._analyze_timing_risks(account_id)

        # Calculate overall risk score
        overall_risk = self._calculate_overall_risk(
            relationship_risks, competitive_risks, process_risks, timing_risks
        )

        # Generate mitigation plan
        mitigation_plan = self._generate_mitigation_plan(
            relationship_risks, competitive_risks, process_risks, timing_risks
        )

        return {
            "status": "success",
            "operation": "detailed_risk_analysis",
            "timestamp": datetime.now().isoformat(),
            "data": {
                "Deal Health Score": {
                    "Overall Risk": "🟡 MODERATE-HIGH (62/100)",
                    "Close Probability": "47% → Can improve to 75% with action plan",
                    "Trending": "⬇️ Declining (was 52% last month due to CTO change)",
                    "Risk Category": "At-risk expansion + renewal jeopardy"
                },
                "🔴 CRITICAL RISKS (Must Fix Now)": relationship_risks['critical'],
                "🟡 MODERATE RISKS (Monitor Closely)": competitive_risks['moderate'],
                "🟢 LOW RISKS (Standard Vigilance)": process_risks['low'],
                "Risk Mitigation Action Plan": mitigation_plan,
                "Success Probability Roadmap": self._probability_roadmap()
            }
        }

    def _analyze_relationship_risks(self, account_id: str) -> Dict[str, Any]:
        """Analyze stakeholder relationship risks"""
        return {
            "critical": {
                "Risk #1: CTO Relationship Gap": {
                    "Impact": "SEVERE - She controls budget + decision",
                    "Probability": "95% (zero contact in 6 weeks)",
                    "Consequence": "Deal dies or goes to competitor she knows",
                    "Mitigation": "Leverage Alex Zhang intro + schedule meeting THIS WEEK",
                    "Status": "🔴 UNMITIGATED - Your #1 priority",
                    "Timeline": "Must meet her within 5 days or lose deal"
                },
                "Risk #3: Usage Declining 12%": {
                    "Impact": "HIGH - Signals dissatisfaction",
                    "Probability": "100% (confirmed in CRM data)",
                    "Consequence": "Renewal at risk, expansion impossible",
                    "Mitigation": "Customer success intervention + quick win",
                    "Status": "🔴 UNMITIGATED - CS team needed ASAP"
                }
            },
            "moderate": {
                "Champion Neutralized": "James Liu going silent (70% probability)"
            }
        }

    def _analyze_competitive_risks(self, account_id: str) -> Dict[str, Any]:
        """Analyze competitive threat risks"""
        return {
            "moderate": {
                "Risk #2: DataBricks Inside Track": {
                    "Impact": "SEVERE - Personal relationship with CTO",
                    "Probability": "80% (their AE is her ex-colleague)",
                    "Consequence": "They win on relationship despite higher price",
                    "Mitigation": "Counter with technical superiority + manufacturing expertise",
                    "Status": "🟡 PARTIALLY MITIGATED - Need stronger positioning"
                }
            }
        }

    def _analyze_process_risks(self, account_id: str) -> Dict[str, Any]:
        """Analyze procurement/process risks"""
        return {
            "low": {
                "Technical Fit": "LOW - Your platform proven with James",
                "Budget Availability": "LOW - $12M allocated, confirmed",
                "Legal/Security": "LOW - Already approved vendor"
            }
        }

    def _analyze_timing_risks(self, account_id: str) -> Dict[str, Any]:
        """Analyze timeline risks"""
        return {
            "moderate": {
                "Holiday Compression": "Risk of delay due to Dec holidays",
                "Procurement Consultant": "New consultant may slow process"
            }
        }

    def _calculate_overall_risk(self, *risk_categories) -> int:
        """Calculate overall risk score (0-100)"""
        # Simplified calculation - in production, use ML model
        return 62

    def _generate_mitigation_plan(self, *risk_categories) -> Dict[str, List[str]]:
        """Generate time-based mitigation plan"""
        return {
            "THIS WEEK (Dec 10-14)": [
                "Mon: Alex Zhang intro email to CTO Sarah",
                "Tue: CTO meeting (8am) - establish relationship",
                "Wed: CS team audit usage decline + recovery plan",
                "Thu: James Liu reactivation lunch + get his buy-in",
                "Fri: CFO email with ROI analysis + meeting request"
            ],
            "NEXT WEEK (Dec 16-20)": [
                "Mon: Pilot proposal submission with 3 pricing tiers",
                "Tue: Technical scoping call (James + CTO's engineering team)",
                "Wed: Competitive battle card to CTO (neutralize DataBricks)",
                "Thu: Procurement process kickoff with Michelle",
                "Fri: Executive alignment call (CTO + CFO + you)"
            ],
            "WEEK 3 (Dec 23-27)": [
                "Holiday week - limited availability",
                "Tue: Check-in call with CTO (keep momentum)",
                "Thu: Year-end close push (if timing works)",
                "Fri: Verbal commitment target"
            ]
        }

    def _probability_roadmap(self) -> Dict[str, str]:
        """Show how probability improves with each action"""
        return {
            "Current State": "47% win probability",
            "After CTO Meeting": "→ 58% (relationship established)",
            "After Pilot Proposal": "→ 65% (concrete next step)",
            "After James Reactivation": "→ 72% (internal champion)",
            "After CFO Buy-in": "→ 78% (economic buyer aligned)",
            "After Verbal Commitment": "→ 90% (deal essentially won)",
            "Target": "75%+ by Dec 20 (verbal commitment)"
        }


if __name__ == "__main__":
    agent = RiskAssessmentAgent()
    result = agent.perform(
        operation="detailed_risk_analysis",
        account_id="CONTOSO001",
        opportunity_id="OPP001"
    )
    print(json.dumps(result, indent=2))
