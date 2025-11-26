"""
Action Prioritization Agent
Generates prioritized, time-bound action plans

Uses:
- Risk assessment data
- Calendar availability (Microsoft Graph)
- Impact x Urgency x Ease scoring
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

from agents.basic_agent import BasicAgent
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List

class ActionPrioritizationAgent(BasicAgent):
    def __init__(self):
        self.name = "ActionPrioritizationAgent"
        self.metadata = {
            "name": self.name,
            "description": "Generates prioritized action plans using Impact x Urgency x Ease framework"
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs) -> Dict[str, Any]:
        account_id = kwargs.get('account_id')
        timeframe = kwargs.get('context', {}).get('timeframe', '48_hours')

        if timeframe == '48_hours':
            return self._generate_48_hour_plan(account_id)
        elif timeframe == 'weekly':
            return self._generate_weekly_plan(account_id)
        else:
            return self._generate_strategic_plan(account_id)

    def _generate_48_hour_plan(self, account_id: str) -> Dict[str, Any]:
        """Hour-by-hour battle plan for next 48 hours"""

        plan = {
            "🚨 NEXT 48 HOURS - HOUR BY HOUR PLAN": {
                "Priority Framework": "Impact x Urgency x Ease = Priority Score",
                "Focus": "Critical path to CTO meeting + deal acceleration",
                "Goal": "Secure CTO meeting + reactivate champion + block DataBricks"
            },
            "TODAY - NEXT 4 HOURS (Immediate Actions)": {
                "⏰ Next 30 Minutes (HIGHEST PRIORITY)": {
                    "Action": "Call Alex Zhang (your VP Eng) for warm intro to CTO Sarah",
                    "Why Now": "You need CTO meeting THIS WEEK - warm intro is fastest path",
                    "Script": "'Alex - remember Sarah Chen from your Amazon days? She's now CTO at my top account. Can you intro me? I need 30min with her this week to save a $2M deal.'",
                    "Expected Outcome": "Alex agrees to email intro within 2 hours",
                    "Priority Score": "100/100 - Nothing is more important",
                    "Time Investment": "15 minutes"
                },
                "⏰ Hour 1": {
                    "Action": "Draft + send LinkedIn connection to Sarah Chen",
                    "Why Now": "Prime her before Alex's intro email arrives",
                    "Priority Score": "95/100",
                    "Time Investment": "10 minutes"
                },
                "⏰ Hour 2": {
                    "Action": "Call James Liu (your technical champion) for coffee this week",
                    "Why Now": "Need him reactivated before CTO meeting for insider intel",
                    "Priority Score": "90/100",
                    "Time Investment": "20 minutes"
                },
                "⏰ Hour 3-4": {
                    "Action": "Prepare CTO meeting materials (demo, case studies, pilot proposal)",
                    "Why Now": "Meeting likely scheduled for tomorrow or Thursday - be ready",
                    "Priority Score": "85/100",
                    "Time Investment": "90 minutes"
                }
            },
            "TODAY - HOURS 5-8 (Secondary Actions)": self._generate_secondary_actions(),
            "TOMORROW - MORNING (Hours 9-12)": self._generate_tomorrow_morning(),
            "TOMORROW - AFTERNOON (Hours 13-16)": self._generate_tomorrow_afternoon(),
            "Success Metrics - 48 Hours": {
                "Must-Have Outcomes": [
                    "✅ CTO meeting completed with positive outcome",
                    "✅ Next step scheduled (pilot or technical call)",
                    "✅ James Liu re-engaged as champion",
                    "✅ Follow-up materials sent within 2 hours"
                ],
                "Deal Progress Target": "Move from 47% → 65% close probability"
            }
        }

        return {
            "status": "success",
            "operation": "action_plan",
            "timeframe": "48_hours",
            "timestamp": datetime.now().isoformat(),
            "data": plan
        }

    def _generate_secondary_actions(self) -> Dict[str, Dict[str, Any]]:
        return {
            "⏰ Hour 5": {
                "Action": "Engage Customer Success team on usage decline issue",
                "Why": "CTO will ask about customer satisfaction - need good answer",
                "Priority Score": "80/100"
            },
            "⏰ Hour 6": {
                "Action": "Research + prepare competitive battle card (vs DataBricks)",
                "Why": "CTO will mention DataBricks - need compelling counter",
                "Priority Score": "75/100"
            },
            "⏰ Hour 7-8": {
                "Action": "Draft CFO email with ROI analysis (send tomorrow)",
                "Why": "Multi-threading - don't rely only on CTO relationship",
                "Priority Score": "70/100"
            }
        }

    def _generate_tomorrow_morning(self) -> Dict[str, Dict[str, Any]]:
        return {
            "⏰ 7:00 AM": {
                "Action": "Final CTO meeting prep + role play",
                "Details": "Review Sarah's profile, practice demo, memorize key stats",
                "Mindset": "You're a strategic advisor, not a vendor. Confidence."
            },
            "⏰ 8:00 AM": {
                "Action": "CTO MEETING with Sarah Chen 🎯",
                "Duration": "30 minutes (plan for 25, give her 5 min buffer)",
                "Objective": "Establish relationship + secure pilot agreement",
                "Priority Score": "100/100 - THE MOST IMPORTANT 30 MIN OF YOUR QUARTER"
            },
            "⏰ 10:00 AM": {
                "Action": "Post-meeting actions (CRITICAL - do within 2 hours)",
                "Tasks": [
                    "Send follow-up email with pilot proposal",
                    "Record + send personalized video recap",
                    "Update CRM with detailed notes",
                    "Brief your manager on meeting outcome"
                ]
            }
        }

    def _generate_tomorrow_afternoon(self) -> Dict[str, Dict[str, Any]]:
        return {
            "⏰ 1:00 PM": {
                "Action": "Send CFO email with ROI analysis",
                "Why Now": "After CTO meeting, you have more context",
                "Objective": "Multi-thread to economic buyer"
            },
            "⏰ 2:00 PM": {
                "Action": "Schedule technical scoping call",
                "Attendees": "Sarah Chen, James Liu, your solutions engineer",
                "Target Date": "Thursday or Friday this week"
            },
            "⏰ 3:00 PM": {
                "Action": "Procurement outreach to Michelle Park",
                "Message": "'Michelle - heads up that Sarah and I discussed a pilot. Loop you in early to streamline timing.'"
            },
            "⏰ 4:00 PM": {
                "Action": "Deal strategy session with your manager",
                "Agenda": "Review CTO meeting outcome, adjust strategy, get exec support"
            }
        }

    def _generate_weekly_plan(self, account_id: str) -> Dict[str, Any]:
        """Week-by-week strategic plan"""
        return {
            "status": "success",
            "data": {
                "Week 1": "Establish CTO relationship + submit pilot proposal",
                "Week 2": "Technical validation + stakeholder alignment",
                "Week 3": "Verbal commitment + contract negotiation",
                "Week 4": "Contract signature + deal close"
            }
        }

    def _generate_strategic_plan(self, account_id: str) -> Dict[str, Any]:
        """Long-term strategic plan"""
        return {
            "status": "success",
            "data": {
                "Phase 1 (Now - Dec 20)": "Win the deal",
                "Phase 2 (Jan - Mar)": "Successful implementation",
                "Phase 3 (Apr - Jun)": "Expansion conversations",
                "Phase 4 (Jul - Sep)": "Reference customer + case study"
            }
        }


if __name__ == "__main__":
    agent = ActionPrioritizationAgent()
    result = agent.perform(
        account_id="CONTOSO001",
        context={"timeframe": "48_hours"}
    )
    print(json.dumps(result, indent=2))
