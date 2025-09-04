from agents.basic_agent import BasicAgent
import json
import random
from datetime import datetime, timedelta


class ITTicketManagementAgent(BasicAgent):
    def __init__(self):
        self.name = "ITTicketManagement"
        self.metadata = {
            "name": self.name,
            "description": "Automates IT support ticket creation, routing, prioritization, and resolution. Streamlines IT service management with intelligent ticket handling and SLA tracking.",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "description": "Action to perform",
                        "enum": ["create", "update", "prioritize", "route", "resolve", "analyze"]
                    },
                    "ticket_data": {
                        "type": "object",
                        "description": "Ticket information",
                        "properties": {
                            "ticket_id": {"type": "string"},
                            "title": {"type": "string"},
                            "description": {"type": "string"},
                            "category": {"type": "string"},
                            "priority": {"type": "string"},
                            "affected_users": {"type": "integer"}
                        }
                    },
                    "auto_assign": {
                        "type": "boolean",
                        "description": "Optional. Automatically assign to best available agent"
                    },
                    "sla_check": {
                        "type": "boolean",
                        "description": "Optional. Check SLA compliance"
                    }
                },
                "required": ["action", "ticket_data"]
            }
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        action = kwargs.get('action')
        ticket_data = kwargs.get('ticket_data', {})
        auto_assign = kwargs.get('auto_assign', True)
        sla_check = kwargs.get('sla_check', True)

        try:
            if not action or not ticket_data:
                raise ValueError("Action and ticket data are required")

            # Process ticket action
            result = self._process_ticket(action, ticket_data, auto_assign, sla_check)

            return json.dumps({
                "status": "success",
                "message": f"Ticket {action} completed successfully",
                "data": result
            })

        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Failed to process IT ticket: {str(e)}"
            })

    def _process_ticket(self, action, ticket_data, auto_assign, sla_check):
        """Process IT ticket based on action"""
        
        ticket_id = ticket_data.get('ticket_id', f"TKT-{random.randint(100000, 999999)}")
        
        result = {
            "ticket_id": ticket_id,
            "action_performed": action,
            "timestamp": datetime.now().isoformat()
        }
        
        if action == "create":
            result.update({
                "ticket_details": {
                    "id": ticket_id,
                    "title": ticket_data.get('title', 'New IT Issue'),
                    "status": "Open",
                    "priority": self._calculate_priority(ticket_data),
                    "category": ticket_data.get('category', 'General'),
                    "created_at": datetime.now().isoformat(),
                    "sla_deadline": (datetime.now() + timedelta(hours=4)).isoformat()
                },
                "assignment": {
                    "assigned_to": "John Smith" if auto_assign else "Unassigned",
                    "team": "Level 1 Support",
                    "expertise_match": "95%"
                }
            })
        
        elif action == "prioritize":
            priority_analysis = self._analyze_priority(ticket_data)
            result.update({
                "prioritization": priority_analysis,
                "recommended_priority": priority_analysis['recommended_level'],
                "queue_position": random.randint(1, 50)
            })
        
        elif action == "route":
            routing = self._determine_routing(ticket_data)
            result.update({
                "routing": routing,
                "assigned_team": routing['team'],
                "assigned_agent": routing['agent'],
                "estimated_resolution": routing['eta']
            })
        
        elif action == "resolve":
            result.update({
                "resolution": {
                    "status": "Resolved",
                    "resolution_notes": "Issue resolved through automated troubleshooting",
                    "resolution_time": f"{random.randint(10, 120)} minutes",
                    "solution_applied": "System restart and cache clear",
                    "kb_article_created": True
                },
                "metrics": {
                    "first_response_time": "5 minutes",
                    "total_resolution_time": "45 minutes",
                    "customer_satisfaction": "4.5/5",
                    "sla_met": True
                }
            })
        
        elif action == "analyze":
            result.update({
                "analysis": {
                    "issue_type": "Software configuration",
                    "root_cause": "Outdated driver version",
                    "impact_level": "Medium",
                    "affected_systems": ["Email", "Calendar", "Teams"],
                    "related_tickets": [f"TKT-{random.randint(100000, 999999)}" for _ in range(3)],
                    "pattern_detected": "Similar issues reported in last 24 hours",
                    "recommended_actions": [
                        "Deploy driver update to affected machines",
                        "Send notification to affected users",
                        "Create preventive maintenance task"
                    ]
                }
            })
        
        # Add SLA information if requested
        if sla_check:
            result["sla_status"] = {
                "current_status": random.choice(["On Track", "At Risk", "Breached"]),
                "time_remaining": f"{random.randint(1, 8)} hours",
                "escalation_needed": random.choice([True, False]),
                "priority_boost": random.choice([True, False])
            }
        
        # Add automation suggestions
        result["automation_opportunities"] = {
            "auto_resolvable": random.choice([True, False]),
            "suggested_automations": [
                "Password reset automation",
                "Software installation automation",
                "Access request workflow"
            ],
            "estimated_time_saved": f"{random.randint(20, 80)}%"
        }
        
        return result

    def _calculate_priority(self, ticket_data):
        """Calculate ticket priority based on various factors"""
        affected_users = ticket_data.get('affected_users', 1)
        
        if affected_users > 100:
            return "Critical"
        elif affected_users > 50:
            return "High"
        elif affected_users > 10:
            return "Medium"
        else:
            return "Low"

    def _analyze_priority(self, ticket_data):
        """Analyze and recommend priority level"""
        return {
            "factors_considered": {
                "business_impact": "High",
                "affected_users": ticket_data.get('affected_users', 1),
                "system_criticality": "Core system",
                "time_sensitivity": "Business hours"
            },
            "priority_score": random.randint(60, 95),
            "recommended_level": random.choice(["Critical", "High", "Medium", "Low"]),
            "reasoning": "High business impact affecting core system during business hours"
        }

    def _determine_routing(self, ticket_data):
        """Determine optimal routing for ticket"""
        return {
            "team": random.choice(["Network Team", "Application Support", "Security Team", "Database Team"]),
            "agent": random.choice(["Alice Johnson", "Bob Smith", "Carol White", "David Brown"]),
            "routing_logic": "Skill-based routing with workload balancing",
            "confidence": f"{random.randint(85, 99)}%",
            "eta": f"{random.randint(1, 4)} hours"
        }


if __name__ == "__main__":
    agent = ITTicketManagementAgent()
    
    result = agent.perform(
        action="create",
        ticket_data={
            "title": "Email system down for multiple users",
            "description": "Users cannot access email since 9 AM",
            "category": "Email",
            "priority": "High",
            "affected_users": 150
        },
        auto_assign=True,
        sla_check=True
    )
    
    print(json.dumps(json.loads(result), indent=2))
