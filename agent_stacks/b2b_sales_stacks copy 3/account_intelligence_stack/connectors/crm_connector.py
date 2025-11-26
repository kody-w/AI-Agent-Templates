"""
CRM Connector - Supports multiple CRM systems
- Microsoft Dynamics 365
- Salesforce
- Monday.com
- HubSpot

Includes MOCK mode for testing and PRODUCTION mode for real APIs
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from connectors.base_connector import BaseConnector
from config import Config, CRMSystem
from typing import Dict, Any, List
import json

class CRMConnector(BaseConnector):
    """
    Multi-CRM connector with Power Platform integration support

    Supports:
    - Dynamics 365 (via Dataverse API)
    - Salesforce (via REST API)
    - Monday.com (via GraphQL API)
    - HubSpot (via REST API)
    """

    def __init__(self, connector_token: str = None):
        super().__init__(connector_token)
        self.crm_system = Config.CRM_SYSTEM
        self.crm_config = Config.get_crm_config()

    def authenticate(self) -> bool:
        """Authenticate with CRM system"""
        if self.is_mock:
            return True

        # Production authentication (implement based on CRM system)
        if self.crm_system == CRMSystem.DYNAMICS_365:
            return self._authenticate_dynamics()
        elif self.crm_system == CRMSystem.SALESFORCE:
            return self._authenticate_salesforce()
        elif self.crm_system == CRMSystem.MONDAY:
            return self._authenticate_monday()
        elif self.crm_system == CRMSystem.HUBSPOT:
            return self._authenticate_hubspot()

    def test_connection(self) -> Dict[str, Any]:
        """Test CRM connection"""
        if self.is_mock:
            return {
                "status": "success",
                "mode": "mock",
                "crm_system": self.crm_system.value,
                "message": "Mock mode - no real connection"
            }

        # Test real connection
        try:
            self.authenticate()
            return {
                "status": "success",
                "mode": "production",
                "crm_system": self.crm_system.value,
                "message": f"Connected to {self.crm_system.value}"
            }
        except Exception as e:
            return self._error_response(f"Connection failed: {str(e)}")

    # ==================== ACCOUNT OPERATIONS ====================

    def get_account(self, account_id: str) -> Dict[str, Any]:
        """
        Get account/company data from CRM

        Args:
            account_id: Account identifier (can be ID or name)

        Returns:
            Account data dict
        """
        if self.is_mock:
            return self._mock_response(self._get_mock_account(account_id))

        # Production: Call real CRM API
        if self.crm_system == CRMSystem.DYNAMICS_365:
            return self._get_dynamics_account(account_id)
        elif self.crm_system == CRMSystem.SALESFORCE:
            return self._get_salesforce_account(account_id)
        elif self.crm_system == CRMSystem.MONDAY:
            return self._get_monday_account(account_id)
        elif self.crm_system == CRMSystem.HUBSPOT:
            return self._get_hubspot_account(account_id)

    def get_contacts(self, account_id: str) -> Dict[str, Any]:
        """
        Get contacts/people associated with account

        Args:
            account_id: Account identifier

        Returns:
            List of contacts
        """
        if self.is_mock:
            return self._mock_response(self._get_mock_contacts(account_id))

        # Production: Call real CRM API
        if self.crm_system == CRMSystem.DYNAMICS_365:
            return self._get_dynamics_contacts(account_id)
        elif self.crm_system == CRMSystem.SALESFORCE:
            return self._get_salesforce_contacts(account_id)
        elif self.crm_system == CRMSystem.MONDAY:
            return self._get_monday_contacts(account_id)
        elif self.crm_system == CRMSystem.HUBSPOT:
            return self._get_hubspot_contacts(account_id)

    def get_opportunities(self, account_id: str) -> Dict[str, Any]:
        """
        Get opportunities/deals associated with account

        Args:
            account_id: Account identifier

        Returns:
            List of opportunities
        """
        if self.is_mock:
            return self._mock_response(self._get_mock_opportunities(account_id))

        # Production: Call real CRM API
        if self.crm_system == CRMSystem.DYNAMICS_365:
            return self._get_dynamics_opportunities(account_id)
        elif self.crm_system == CRMSystem.SALESFORCE:
            return self._get_salesforce_opportunities(account_id)
        elif self.crm_system == CRMSystem.MONDAY:
            return self._get_monday_deals(account_id)
        elif self.crm_system == CRMSystem.HUBSPOT:
            return self._get_hubspot_deals(account_id)

    def get_activities(self, account_id: str) -> Dict[str, Any]:
        """
        Get activities/interactions for account

        Args:
            account_id: Account identifier

        Returns:
            List of activities
        """
        if self.is_mock:
            return self._mock_response(self._get_mock_activities(account_id))

        # Production implementation for each CRM
        if self.crm_system == CRMSystem.DYNAMICS_365:
            return self._get_dynamics_activities(account_id)
        elif self.crm_system == CRMSystem.SALESFORCE:
            return self._get_salesforce_activities(account_id)
        elif self.crm_system == CRMSystem.MONDAY:
            return self._get_monday_updates(account_id)
        elif self.crm_system == CRMSystem.HUBSPOT:
            return self._get_hubspot_activities(account_id)

    # ==================== MOCK DATA METHODS ====================

    def _get_mock_account(self, account_id: str) -> Dict[str, Any]:
        """Mock account data"""
        return {
            "account_id": account_id,
            "name": "Contoso Corporation",
            "industry": "Manufacturing & Industrial Technology",
            "revenue": 2300000000,
            "employees": 12400,
            "headquarters": "Seattle, WA",
            "country": "United States",
            "website": "www.contoso.com",
            "phone": "+1-206-555-0100",
            "relationship_start": "2021-04-15",
            "current_arr": 340000,
            "health_score": 72,
            "usage_trend": -0.12,
            "renewal_date": "2025-02-15",
            "account_owner": "John Smith",
            "account_owner_email": "john.smith@yourcompany.com",
            "crm_system": self.crm_system.value,
            "last_modified": "2024-12-10T10:00:00Z"
        }

    def _get_mock_contacts(self, account_id: str) -> List[Dict[str, Any]]:
        """Mock contacts data"""
        return [
            {
                "contact_id": "CONT001",
                "full_name": "Dr. Sarah Chen",
                "job_title": "Chief Technology Officer",
                "email": "sarah.chen@contoso.com",
                "phone": "+1-206-555-0101",
                "mobile": "+1-206-555-0102",
                "decision_role": "Economic Buyer",
                "tenure": "6 weeks",
                "department": "Technology",
                "reports_to": "CEO - Patricia Miller",
                "linkedin_url": "linkedin.com/in/sarahchen",
                "last_contact": "2024-10-18",
                "email_interactions": 12,
                "meeting_count": 3,
                "relationship_strength": "strong"
            },
            {
                "contact_id": "CONT002",
                "full_name": "Robert Martinez",
                "job_title": "Chief Financial Officer",
                "email": "robert.martinez@contoso.com",
                "phone": "+1-206-555-0103",
                "decision_role": "Budget Approver",
                "tenure": "2 years",
                "department": "Finance",
                "linkedin_url": "linkedin.com/in/robertmartinez",
                "last_contact": "2023-06-15",
                "email_interactions": 5,
                "meeting_count": 1,
                "relationship_strength": "weak"
            },
            {
                "contact_id": "CONT003",
                "full_name": "James Liu",
                "job_title": "VP Engineering",
                "email": "james.liu@contoso.com",
                "phone": "+1-206-555-0104",
                "decision_role": "Technical Evaluator",
                "tenure": "5 years",
                "department": "Engineering",
                "linkedin_url": "linkedin.com/in/jamesliu",
                "last_contact": "2024-11-20",
                "email_interactions": 45,
                "meeting_count": 12,
                "relationship_strength": "champion"
            },
            {
                "contact_id": "CONT004",
                "full_name": "Michelle Park",
                "job_title": "Director of Procurement",
                "email": "michelle.park@contoso.com",
                "decision_role": "Gatekeeper",
                "tenure": "8 years",
                "department": "Procurement",
                "last_contact": "2024-09-10",
                "email_interactions": 8,
                "relationship_strength": "neutral"
            },
            {
                "contact_id": "CONT005",
                "full_name": "David Kumar",
                "job_title": "VP Operations",
                "email": "david.kumar@contoso.com",
                "decision_role": "End User",
                "tenure": "12 years",
                "department": "Operations",
                "last_contact": "Never",
                "email_interactions": 0,
                "relationship_strength": "unknown"
            }
        ]

    def _get_mock_opportunities(self, account_id: str) -> List[Dict[str, Any]]:
        """Mock opportunities data"""
        return [
            {
                "opportunity_id": "OPP001",
                "name": "Contoso Digital Transformation - Renewal + Expansion",
                "account_id": account_id,
                "stage": "Qualification",
                "probability": 47,
                "amount": 2100000,
                "currency": "USD",
                "close_date": "2025-01-20",
                "created_date": "2024-09-15",
                "owner": "John Smith",
                "products": ["Platform License", "AI Add-on", "Professional Services"],
                "competitors": ["DataBricks", "Snowflake"],
                "next_step": "CTO meeting scheduled",
                "deal_type": "renewal_expansion",
                "contract_term": "3 years",
                "win_factors": [
                    "Existing relationship (3.5 years)",
                    "Technical champion (James Liu)",
                    "Manufacturing expertise"
                ],
                "risk_factors": [
                    "New CTO (no relationship)",
                    "Usage declining 12%",
                    "Competitive pressure"
                ],
                "budget_confirmed": True,
                "decision_timeline": "45-60 days"
            }
        ]

    def _get_mock_activities(self, account_id: str) -> List[Dict[str, Any]]:
        """Mock activities data"""
        return [
            {
                "activity_id": "ACT001",
                "type": "email",
                "subject": "Q3 Business Review",
                "date": "2024-11-15",
                "contact": "James Liu",
                "direction": "outbound",
                "status": "completed"
            },
            {
                "activity_id": "ACT002",
                "type": "meeting",
                "subject": "Technical Deep Dive",
                "date": "2024-11-10",
                "contact": "James Liu",
                "duration_minutes": 60,
                "status": "completed"
            },
            {
                "activity_id": "ACT003",
                "type": "phone",
                "subject": "Support Escalation",
                "date": "2024-10-18",
                "contact": "James Liu",
                "duration_minutes": 30,
                "status": "completed"
            },
            {
                "activity_id": "ACT004",
                "type": "email",
                "subject": "Renewal Discussion",
                "date": "2024-09-20",
                "contact": "Michelle Park",
                "direction": "inbound",
                "status": "completed"
            }
        ]

    # ==================== PRODUCTION API METHODS (Stubs) ====================
    # These would contain real API calls in production

    def _authenticate_dynamics(self) -> bool:
        """Authenticate with Dynamics 365"""
        # TODO: Implement OAuth 2.0 flow for Dynamics 365
        # Use MSAL library to get access token
        pass

    def _authenticate_salesforce(self) -> bool:
        """Authenticate with Salesforce"""
        # TODO: Implement Salesforce OAuth or username/password flow
        pass

    def _authenticate_monday(self) -> bool:
        """Authenticate with Monday.com"""
        # TODO: Use API key authentication
        pass

    def _authenticate_hubspot(self) -> bool:
        """Authenticate with HubSpot"""
        # TODO: Use API key or OAuth
        pass

    def _get_dynamics_account(self, account_id: str) -> Dict[str, Any]:
        """Get account from Dynamics 365"""
        # TODO: Call Dataverse API
        # GET https://{org}.crm.dynamics.com/api/data/v9.2/accounts({id})
        pass

    def _get_salesforce_account(self, account_id: str) -> Dict[str, Any]:
        """Get account from Salesforce"""
        # TODO: Call Salesforce REST API
        # GET https://{instance}.salesforce.com/services/data/v58.0/sobjects/Account/{id}
        pass

    def _get_monday_account(self, account_id: str) -> Dict[str, Any]:
        """Get account from Monday.com"""
        # TODO: Call Monday.com GraphQL API
        pass

    def _get_hubspot_account(self, account_id: str) -> Dict[str, Any]:
        """Get company from HubSpot"""
        # TODO: Call HubSpot API
        # GET https://api.hubapi.com/crm/v3/objects/companies/{id}
        pass

    def _get_dynamics_contacts(self, account_id: str) -> Dict[str, Any]:
        """Get contacts from Dynamics 365"""
        # TODO: Query contacts related to account
        pass

    def _get_salesforce_contacts(self, account_id: str) -> Dict[str, Any]:
        """Get contacts from Salesforce"""
        # TODO: SOQL query for contacts
        pass

    def _get_monday_contacts(self, account_id: str) -> Dict[str, Any]:
        """Get people from Monday.com"""
        # TODO: GraphQL query for contacts
        pass

    def _get_hubspot_contacts(self, account_id: str) -> Dict[str, Any]:
        """Get contacts from HubSpot"""
        # TODO: Query contacts associated with company
        pass

    def _get_dynamics_opportunities(self, account_id: str) -> Dict[str, Any]:
        """Get opportunities from Dynamics 365"""
        # TODO: Query opportunities
        pass

    def _get_salesforce_opportunities(self, account_id: str) -> Dict[str, Any]:
        """Get opportunities from Salesforce"""
        # TODO: SOQL query for opportunities
        pass

    def _get_monday_deals(self, account_id: str) -> Dict[str, Any]:
        """Get deals from Monday.com"""
        # TODO: GraphQL query for deals
        pass

    def _get_hubspot_deals(self, account_id: str) -> Dict[str, Any]:
        """Get deals from HubSpot"""
        # TODO: Query deals
        pass

    def _get_dynamics_activities(self, account_id: str) -> Dict[str, Any]:
        """Get activities from Dynamics 365"""
        # TODO: Query activities
        pass

    def _get_salesforce_activities(self, account_id: str) -> Dict[str, Any]:
        """Get activities from Salesforce"""
        # TODO: Query tasks, events, etc.
        pass

    def _get_monday_updates(self, account_id: str) -> Dict[str, Any]:
        """Get updates from Monday.com"""
        # TODO: Query updates
        pass

    def _get_hubspot_activities(self, account_id: str) -> Dict[str, Any]:
        """Get activities from HubSpot"""
        # TODO: Query engagements
        pass


if __name__ == "__main__":
    # Test the connector in mock mode
    print("Testing CRM Connector in MOCK mode...")
    connector = CRMConnector()

    # Test connection
    connection_test = connector.test_connection()
    print(f"\nConnection Test: {json.dumps(connection_test, indent=2)}")

    # Get account
    account = connector.get_account("CONTOSO001")
    print(f"\nAccount Data: {json.dumps(account, indent=2)}")

    # Get contacts
    contacts = connector.get_contacts("CONTOSO001")
    print(f"\nContacts Count: {len(contacts['data'])}")

    # Get opportunities
    opportunities = connector.get_opportunities("CONTOSO001")
    print(f"\nOpportunities Count: {len(opportunities['data'])}")

    print("\n✅ CRM Connector test complete!")
