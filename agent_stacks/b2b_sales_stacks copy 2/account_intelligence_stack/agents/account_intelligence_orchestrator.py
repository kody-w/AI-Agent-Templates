"""
Account Intelligence Orchestrator Agent
Routes requests to specialized sub-agents and integrates with Copilot Studio

This orchestrator connects to:
- Dynamics 365 (CRM data)
- Microsoft Graph API (LinkedIn Sales Navigator, stakeholder data)
- Azure OpenAI (synthesis and generation)
- Azure AI Search (competitive intelligence)
- Power Automate (workflow automation)
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

from agents.basic_agent import BasicAgent
import json
from datetime import datetime, timedelta
import os
from typing import Dict, Any, List

# Import specialized agents (lazy loading to avoid circular imports)
# These will be imported dynamically when needed

class AccountIntelligenceOrchestrator(BasicAgent):
    """
    Main orchestrator for Account Intelligence operations
    Integrates with Microsoft Copilot Studio as a plugin/action
    """

    def __init__(self, connector_token: str = None):
        self.name = "AccountIntelligenceOrchestrator"
        self.connector_token = connector_token
        self.metadata = {
            "name": self.name,
            "description": "Comprehensive B2B account intelligence for sales professionals. Provides stakeholder analysis, competitive intelligence, meeting prep, messaging, risk assessment, and deal tracking.",
            "version": "2.0.0",
            "copilot_studio_enabled": True,
            "azure_function_ready": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": [
                            "account_briefing",
                            "stakeholder_analysis",
                            "competitive_intelligence",
                            "meeting_prep",
                            "generate_messaging",
                            "risk_assessment",
                            "action_plan",
                            "deal_dashboard"
                        ],
                        "description": "Type of intelligence operation to perform"
                    },
                    "account_id": {
                        "type": "string",
                        "description": "Dynamics 365 Account ID or company name"
                    },
                    "contact_id": {
                        "type": "string",
                        "description": "Dynamics 365 Contact ID for stakeholder-specific operations"
                    },
                    "opportunity_id": {
                        "type": "string",
                        "description": "Dynamics 365 Opportunity ID for deal-specific operations"
                    },
                    "context": {
                        "type": "object",
                        "description": "Additional context (meeting type, message type, etc.)"
                    }
                },
                "required": ["operation", "account_id"]
            },
            "data_sources": {
                "dynamics_365": {
                    "enabled": True,
                    "entities": ["accounts", "contacts", "opportunities", "activities"]
                },
                "microsoft_graph": {
                    "enabled": True,
                    "scopes": ["User.Read", "Contacts.Read", "Mail.Read", "Calendars.Read"]
                },
                "linkedin_sales_navigator": {
                    "enabled": True,
                    "integration": "via_dynamics_365"
                },
                "azure_openai": {
                    "enabled": True,
                    "deployment": "gpt-4o",
                    "temperature": 0.7
                },
                "azure_ai_search": {
                    "enabled": True,
                    "index": "competitive_intelligence"
                }
            }
        }
        super().__init__(name=self.name, metadata=self.metadata)

        # Lazy-load specialized agents when needed
        self.stakeholder_agent = None
        self.competitive_agent = None
        self.meeting_prep_agent = None
        self.messaging_agent = None
        self.risk_agent = None
        self.action_agent = None
        self.deal_tracking_agent = None

    def _get_stakeholder_agent(self):
        if self.stakeholder_agent is None:
            from stakeholder_intelligence_agent import StakeholderIntelligenceAgent
            self.stakeholder_agent = StakeholderIntelligenceAgent(self.connector_token)
        return self.stakeholder_agent

    def _get_competitive_agent(self):
        if self.competitive_agent is None:
            from competitive_intelligence_agent import CompetitiveIntelligenceAgent
            self.competitive_agent = CompetitiveIntelligenceAgent(self.connector_token)
        return self.competitive_agent

    def _get_meeting_prep_agent(self):
        if self.meeting_prep_agent is None:
            from meeting_prep_agent import MeetingPrepAgent
            self.meeting_prep_agent = MeetingPrepAgent(self.connector_token)
        return self.meeting_prep_agent

    def _get_messaging_agent(self):
        if self.messaging_agent is None:
            from messaging_agent import MessagingAgent
            self.messaging_agent = MessagingAgent(self.connector_token)
        return self.messaging_agent

    def _get_risk_agent(self):
        if self.risk_agent is None:
            from risk_assessment_agent import RiskAssessmentAgent
            self.risk_agent = RiskAssessmentAgent(self.connector_token)
        return self.risk_agent

    def _get_action_agent(self):
        if self.action_agent is None:
            from action_prioritization_agent import ActionPrioritizationAgent
            self.action_agent = ActionPrioritizationAgent(self.connector_token)
        return self.action_agent

    def _get_deal_tracking_agent(self):
        if self.deal_tracking_agent is None:
            from deal_tracking_agent import DealTrackingAgent
            self.deal_tracking_agent = DealTrackingAgent(self.connector_token)
        return self.deal_tracking_agent

    def perform(self, **kwargs) -> Dict[str, Any]:
        """
        Main entry point for Copilot Studio integration
        Routes to appropriate specialized agent based on operation
        """
        operation = kwargs.get('operation')
        account_id = kwargs.get('account_id')

        if not operation or not account_id:
            return self._error_response("Missing required parameters: operation and account_id")

        # Route to appropriate handler
        operation_map = {
            "account_briefing": self._account_briefing,
            "stakeholder_analysis": self._stakeholder_analysis,
            "competitive_intelligence": self._competitive_intelligence,
            "meeting_prep": self._meeting_prep,
            "generate_messaging": self._generate_messaging,
            "risk_assessment": self._risk_assessment,
            "action_plan": self._action_plan,
            "deal_dashboard": self._deal_dashboard
        }

        handler = operation_map.get(operation)
        if not handler:
            return self._error_response(f"Unknown operation: {operation}")

        try:
            return handler(kwargs)
        except Exception as e:
            return self._error_response(f"Operation failed: {str(e)}")

    def _account_briefing(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive account briefing - calls multiple agents
        """
        account_id = params['account_id']

        # Call Dynamics 365 for CRM data
        crm_data = self._get_dynamics_365_account(account_id)

        # Call stakeholder agent for buying committee
        stakeholder_data = self._get_stakeholder_agent().perform(
            account_id=account_id,
            operation="analyze_buying_committee"
        )

        # Call competitive agent for market intelligence
        competitive_data = self._get_competitive_agent().perform(
            account_id=account_id,
            operation="detect_active_threats"
        )

        # Call risk agent for opportunity assessment
        risk_data = self._get_risk_agent().perform(
            account_id=account_id,
            operation="assess_opportunity"
        )

        # Synthesize with Azure OpenAI
        briefing = self._synthesize_briefing(
            crm_data, stakeholder_data, competitive_data, risk_data
        )

        return {
            "status": "success",
            "operation": "account_briefing",
            "account_id": account_id,
            "timestamp": datetime.now().isoformat(),
            "data": briefing,
            "sources": ["Dynamics 365", "LinkedIn Sales Navigator", "Azure AI Search", "Microsoft Graph"],
            "confidence": 0.92
        }

    def _stakeholder_analysis(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deep dive on specific stakeholder or buying committee
        """
        # Transform params for stakeholder agent
        agent_params = {k: v for k, v in params.items() if k != 'operation'}
        agent_params['operation'] = 'analyze_buying_committee'
        return self._get_stakeholder_agent().perform(**agent_params)

    def _competitive_intelligence(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Competitive battle card and market intelligence
        """
        # Transform params for competitive agent
        agent_params = {k: v for k, v in params.items() if k != 'operation'}
        agent_params['operation'] = 'detect_active_threats'
        return self._get_competitive_agent().perform(**agent_params)

    def _meeting_prep(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate complete meeting preparation brief
        """
        # Meeting prep agent doesn't use operation parameter
        agent_params = {k: v for k, v in params.items() if k != 'operation'}
        return self._get_meeting_prep_agent().perform(**agent_params)

    def _generate_messaging(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate personalized messages (email, LinkedIn, etc.)
        """
        # Messaging agent doesn't use operation parameter
        agent_params = {k: v for k, v in params.items() if k != 'operation'}
        return self._get_messaging_agent().perform(**agent_params)

    def _risk_assessment(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess deal risks and win probability
        """
        # Transform params for risk agent
        agent_params = {k: v for k, v in params.items() if k != 'operation'}
        agent_params['operation'] = 'assess_opportunity'
        return self._get_risk_agent().perform(**agent_params)

    def _action_plan(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate prioritized action plan
        """
        # Transform params for action agent
        agent_params = {k: v for k, v in params.items() if k != 'operation'}
        agent_params['operation'] = 'action_plan'
        return self._get_action_agent().perform(**agent_params)

    def _deal_dashboard(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Real-time deal tracking dashboard
        """
        # Transform params for deal tracking agent
        agent_params = {k: v for k, v in params.items() if k != 'operation'}
        agent_params['operation'] = 'deal_dashboard'
        return self._get_deal_tracking_agent().perform(**agent_params)

    def _get_dynamics_365_account(self, account_id: str) -> Dict[str, Any]:
        """
        Connect to Dynamics 365 and retrieve account data
        Uses Microsoft Dataverse API
        """
        # In production, this would use actual Dynamics 365 API
        # For now, return realistic mock data structure

        return {
            "account_id": account_id,
            "name": "Contoso Corporation",
            "industry": "Manufacturing & Industrial Technology",
            "revenue": 2300000000,
            "employees": 12400,
            "headquarters": "Seattle, WA",
            "relationship_start": "2021-04-15",
            "current_arr": 340000,
            "health_score": 72,
            "usage_trend": -0.12,
            "renewal_date": "2025-02-15",
            "owner_id": "USER123",
            "opportunities": [
                {
                    "id": "OPP001",
                    "name": "Digital Transformation Initiative",
                    "value": 2100000,
                    "stage": "Qualification",
                    "probability": 47,
                    "close_date": "2025-01-20"
                }
            ]
        }

    def _synthesize_briefing(self, crm_data, stakeholder_data, competitive_data, risk_data) -> Dict[str, Any]:
        """
        Use Azure OpenAI to synthesize all data into coherent briefing
        """
        # In production, this would call Azure OpenAI GPT-4
        # For now, return structured synthesis

        return {
            "Company Overview": {
                "Name": crm_data["name"],
                "Industry": crm_data["industry"],
                "Size": f"{crm_data['employees']:,} employees | ${crm_data['revenue']/1e9:.1f}B revenue",
                "Relationship Length": f"{(datetime.now() - datetime.fromisoformat(crm_data['relationship_start'])).days // 365} years",
                "Health Score": f"{crm_data['health_score']}/100 - {'Yellow' if crm_data['health_score'] < 80 else 'Green'}"
            },
            "CRM Status": {
                "Current Products": f"${crm_data['current_arr']:,} ARR",
                "Contract Status": f"Renewal in {(datetime.fromisoformat('2025-02-15') - datetime.now()).days} days",
                "Usage Trend": f"{'Down' if crm_data['usage_trend'] < 0 else 'Up'} {abs(crm_data['usage_trend']*100):.0f}%",
                "Risk Level": risk_data.get('data', {}).get('risk_level', 'Moderate')
            },
            "Key Stakeholders": stakeholder_data.get('data', {}).get('stakeholder_count', 5),
            "Competitive Threats": competitive_data.get('data', {}).get('active_threats', 2),
            "Opportunity Value": f"${crm_data['opportunities'][0]['value']:,}",
            "Win Probability": f"{crm_data['opportunities'][0]['probability']}%",
            "Priority": "HIGH - At-risk renewal + expansion opportunity"
        }

    def _error_response(self, message: str) -> Dict[str, Any]:
        """Standard error response"""
        return {
            "status": "error",
            "message": message,
            "timestamp": datetime.now().isoformat()
        }


def deploy_to_azure_function():
    """
    Helper function to deploy this agent as an Azure Function
    for Copilot Studio integration
    """
    return {
        "function_name": "AccountIntelligenceOrchestrator",
        "runtime": "python",
        "version": "3.11",
        "trigger_type": "HTTP",
        "authentication": "function_key",
        "cors_enabled": True,
        "allowed_origins": ["https://copilotstudio.microsoft.com"],
        "environment_variables": {
            "DYNAMICS_365_URL": "https://org.crm.dynamics.com",
            "AZURE_OPENAI_ENDPOINT": "https://your-openai.openai.azure.com",
            "AZURE_OPENAI_KEY": "SET_IN_AZURE_KEY_VAULT",
            "GRAPH_API_CLIENT_ID": "SET_IN_APP_REGISTRATION",
            "GRAPH_API_CLIENT_SECRET": "SET_IN_AZURE_KEY_VAULT"
        }
    }


if __name__ == "__main__":
    # Test the orchestrator
    orchestrator = AccountIntelligenceOrchestrator()

    # Test account briefing
    result = orchestrator.perform(
        operation="account_briefing",
        account_id="CONTOSO001"
    )

    print(json.dumps(result, indent=2))
