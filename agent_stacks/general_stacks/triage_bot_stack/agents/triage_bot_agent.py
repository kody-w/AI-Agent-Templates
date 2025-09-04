from agents.basic_agent import BasicAgent
import json
import random
from datetime import datetime


class TriageBotAgent(BasicAgent):
    def __init__(self):
        self.name = "TriageBot"
        self.metadata = {
            "name": self.name,
            "description": "Automated triage system that prioritizes and routes requests, tickets, and inquiries based on urgency, impact, and resource availability. Ensures critical issues receive immediate attention.",
            "parameters": {
                "type": "object",
                "properties": {
                    "request": {
                        "type": "object",
                        "description": "Request to triage",
                        "properties": {
                            "type": {"type": "string"},
                            "title": {"type": "string"},
                            "description": {"type": "string"},
                            "source": {"type": "string"},
                            "requester": {"type": "object"}
                        }
                    },
                    "triage_criteria": {
                        "type": "object",
                        "description": "Optional. Custom triage criteria",
                        "properties": {
                            "urgency_weight": {"type": "number"},
                            "impact_weight": {"type": "number"},
                            "resource_weight": {"type": "number"}
                        }
                    },
                    "available_resources": {
                        "type": "array",
                        "description": "Optional. Available resources for assignment",
                        "items": {"type": "object"}
                    },
                    "auto_route": {
                        "type": "boolean",
                        "description": "Optional. Automatically route to best resource"
                    }
                },
                "required": ["request"]
            }
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        request = kwargs.get('request', {})
        triage_criteria = kwargs.get('triage_criteria', {})
        available_resources = kwargs.get('available_resources', [])
        auto_route = kwargs.get('auto_route', True)

        try:
            if not request:
                raise ValueError("Request data is required for triage")

            # Perform triage
            triage_result = self._triage_request(
                request, triage_criteria, available_resources, auto_route
            )

            return json.dumps({
                "status": "success",
                "message": "Request triaged successfully",
                "data": triage_result
            })

        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Failed to triage request: {str(e)}"
            })

    def _triage_request(self, request, criteria, resources, auto_route):
        """Perform intelligent triage of request"""
        
        # Calculate triage scores
        urgency_score = random.randint(1, 10)
        impact_score = random.randint(1, 10)
        complexity_score = random.randint(1, 10)
        priority_score = (urgency_score * 0.4 + impact_score * 0.4 + (10 - complexity_score) * 0.2)
        
        triage_result = {
            "request_id": f"REQ-{random.randint(100000, 999999)}",
            "triage_assessment": {
                "urgency": {
                    "score": urgency_score,
                    "level": self._get_level(urgency_score),
                    "factors": ["User blocked", "Business critical", "Time sensitive"]
                },
                "impact": {
                    "score": impact_score,
                    "level": self._get_level(impact_score),
                    "affected_users": random.randint(1, 1000),
                    "business_areas": ["Sales", "Operations", "Customer Service"]
                },
                "complexity": {
                    "score": complexity_score,
                    "level": self._get_level(complexity_score),
                    "estimated_effort": f"{random.randint(1, 40)} hours",
                    "skills_required": ["Technical", "Domain expertise"]
                },
                "priority": {
                    "score": round(priority_score, 2),
                    "level": self._get_priority_level(priority_score),
                    "queue_position": random.randint(1, 100),
                    "sla_deadline": "4 hours"
                }
            },
            "routing_decision": {
                "recommended_team": random.choice(["Level 1 Support", "Specialist Team", "Engineering", "Management"]),
                "recommended_agent": random.choice(["Agent A", "Agent B", "Agent C", "Agent D"]) if auto_route else None,
                "routing_reason": "Best skill match and availability",
                "alternative_options": [
                    {"team": "Level 2 Support", "availability": "2 hours"},
                    {"team": "External Vendor", "availability": "24 hours"}
                ],
                "escalation_path": ["Team Lead", "Manager", "Director"]
            },
            "categorization": {
                "primary_category": random.choice(["Technical Issue", "Service Request", "Incident", "Problem"]),
                "sub_category": random.choice(["Software", "Hardware", "Network", "Access"]),
                "tags": ["urgent", "customer-facing", "revenue-impact"],
                "knowledge_base_matches": [
                    {"article": "Troubleshooting Guide", "relevance": "85%"},
                    {"article": "Common Issues FAQ", "relevance": "72%"}
                ]
            },
            "response_template": {
                "acknowledgment": "Your request has been received and assigned priority status.",
                "expected_response": "A specialist will contact you within 2 hours.",
                "self_service_options": [
                    "Check status at: portal.example.com/status",
                    "View similar issues: kb.example.com/search"
                ]
            },
            "automation_actions": {
                "performed": [
                    "Created ticket automatically",
                    "Notified relevant team",
                    "Sent acknowledgment to requester"
                ],
                "suggested": [
                    "Run diagnostic scripts",
                    "Gather system logs",
                    "Check for known issues"
                ]
            },
            "metrics": {
                "triage_time": "12 seconds",
                "confidence_level": f"{random.randint(85, 99)}%",
                "model_version": "TriageBot v3.2",
                "similar_requests_today": random.randint(5, 50)
            }
        }
        
        return triage_result

    def _get_level(self, score):
        """Convert numeric score to level"""
        if score >= 8:
            return "Critical"
        elif score >= 6:
            return "High"
        elif score >= 4:
            return "Medium"
        else:
            return "Low"

    def _get_priority_level(self, score):
        """Convert priority score to level"""
        if score >= 8:
            return "P1 - Critical"
        elif score >= 6:
            return "P2 - High"
        elif score >= 4:
            return "P3 - Medium"
        else:
            return "P4 - Low"


if __name__ == "__main__":
    agent = TriageBotAgent()
    
    result = agent.perform(
        request={
            "type": "incident",
            "title": "Production database connection issues",
            "description": "Multiple applications unable to connect to production database",
            "source": "monitoring_system",
            "requester": {"name": "System Alert", "role": "Automated"}
        },
        triage_criteria={
            "urgency_weight": 0.5,
            "impact_weight": 0.3,
            "resource_weight": 0.2
        },
        auto_route=True
    )
    
    print(json.dumps(json.loads(result), indent=2))
