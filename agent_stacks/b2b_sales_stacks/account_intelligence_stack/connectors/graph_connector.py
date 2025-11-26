"""
Microsoft Graph API Connector
Provides access to Microsoft 365 data:
- Emails (stakeholder communication)
- Meetings (calendar interactions)
- Org charts (company structure)
- User profiles

Includes MOCK mode for testing and PRODUCTION mode for real API calls
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from connectors.base_connector import BaseConnector
from config import Config
from typing import Dict, Any, List
import json

class GraphConnector(BaseConnector):
    """
    Microsoft Graph API connector for M365 data

    Supports:
    - Email interactions (sent/received)
    - Meeting history (calendar events)
    - Org charts (reporting structures)
    - User profiles (contact info, job titles)
    """

    def __init__(self, connector_token: str = None):
        super().__init__(connector_token)
        self.graph_config = {
            'client_id': Config.GRAPH_API_CLIENT_ID,
            'client_secret': Config.GRAPH_API_CLIENT_SECRET,
            'tenant_id': Config.GRAPH_API_TENANT_ID,
            'scopes': Config.GRAPH_API_SCOPES
        }

    def authenticate(self) -> bool:
        """Authenticate with Microsoft Graph API"""
        if self.is_mock:
            return True

        # Production authentication using MSAL
        # TODO: Implement MSAL authentication flow
        # from azure.identity import ClientSecretCredential
        # credential = ClientSecretCredential(
        #     tenant_id=self.graph_config['tenant_id'],
        #     client_id=self.graph_config['client_id'],
        #     client_secret=self.graph_config['client_secret']
        # )
        pass

    def test_connection(self) -> Dict[str, Any]:
        """Test Graph API connection"""
        if self.is_mock:
            return {
                "status": "success",
                "mode": "mock",
                "message": "Mock mode - no real Graph API connection"
            }

        # Test real connection
        try:
            self.authenticate()
            return {
                "status": "success",
                "mode": "production",
                "message": "Connected to Microsoft Graph API"
            }
        except Exception as e:
            return self._error_response(f"Connection failed: {str(e)}")

    # ==================== EMAIL METHODS ====================

    def get_email_interactions(self, contact_email: str, days: int = 90) -> Dict[str, Any]:
        """
        Get email interactions with a specific contact

        Args:
            contact_email: Contact's email address
            days: Number of days to look back (default 90)

        Returns:
            Email interaction summary
        """
        if self.is_mock:
            return self._mock_response(self._get_mock_email_interactions(contact_email, days))

        # Production: Call Graph API
        # GET /me/messages?$filter=from/emailAddress/address eq '{contact_email}'
        return self._get_production_email_interactions(contact_email, days)

    def get_email_sentiment(self, contact_email: str) -> Dict[str, Any]:
        """
        Analyze sentiment of email communications

        Args:
            contact_email: Contact's email address

        Returns:
            Sentiment analysis
        """
        if self.is_mock:
            return self._mock_response(self._get_mock_email_sentiment(contact_email))

        # Production: Fetch emails and analyze sentiment
        return self._get_production_email_sentiment(contact_email)

    # ==================== MEETING METHODS ====================

    def get_meeting_history(self, contact_email: str, days: int = 90) -> Dict[str, Any]:
        """
        Get meeting history with a contact

        Args:
            contact_email: Contact's email address
            days: Number of days to look back

        Returns:
            Meeting history
        """
        if self.is_mock:
            return self._mock_response(self._get_mock_meeting_history(contact_email, days))

        # Production: Call Graph API calendar events
        # GET /me/calendar/events?$filter=attendees/any(a:a/emailAddress/address eq '{contact_email}')
        return self._get_production_meeting_history(contact_email, days)

    # ==================== ORG CHART METHODS ====================

    def get_org_chart(self, contact_email: str) -> Dict[str, Any]:
        """
        Get organizational chart for a contact

        Args:
            contact_email: Contact's email address

        Returns:
            Org chart data (manager, direct reports, peers)
        """
        if self.is_mock:
            return self._mock_response(self._get_mock_org_chart(contact_email))

        # Production: Call Graph API
        # GET /users/{contact_email}/manager
        # GET /users/{contact_email}/directReports
        return self._get_production_org_chart(contact_email)

    def get_user_profile(self, contact_email: str) -> Dict[str, Any]:
        """
        Get user profile from Microsoft 365

        Args:
            contact_email: Contact's email address

        Returns:
            User profile data
        """
        if self.is_mock:
            return self._mock_response(self._get_mock_user_profile(contact_email))

        # Production: Call Graph API
        # GET /users/{contact_email}
        return self._get_production_user_profile(contact_email)

    # ==================== MOCK DATA METHODS ====================

    def _get_mock_email_interactions(self, contact_email: str, days: int) -> Dict[str, Any]:
        """Mock email interaction data"""
        # Map contacts to interaction data
        contact_data = {
            "sarah.chen@contoso.com": {
                "contact_email": "sarah.chen@contoso.com",
                "contact_name": "Dr. Sarah Chen",
                "days_analyzed": days,
                "total_emails": 0,
                "sent_by_you": 0,
                "received_from_contact": 0,
                "average_response_time_hours": None,
                "last_contact": None,
                "communication_trend": "no_contact",
                "engagement_score": 0,
                "recent_topics": []
            },
            "james.liu@contoso.com": {
                "contact_email": "james.liu@contoso.com",
                "contact_name": "James Liu",
                "days_analyzed": days,
                "total_emails": 45,
                "sent_by_you": 23,
                "received_from_contact": 22,
                "average_response_time_hours": 3.5,
                "last_contact": "2024-11-20",
                "communication_trend": "increasing",
                "engagement_score": 92,
                "recent_topics": [
                    "Q3 Business Review",
                    "Technical Deep Dive",
                    "Platform Performance Issues",
                    "Renewal Discussion"
                ],
                "email_timeline": [
                    {
                        "date": "2024-11-20",
                        "subject": "Q3 Business Review Follow-up",
                        "direction": "received",
                        "sentiment": "positive"
                    },
                    {
                        "date": "2024-11-15",
                        "subject": "Re: Technical Deep Dive - Next Steps",
                        "direction": "sent",
                        "sentiment": "neutral"
                    },
                    {
                        "date": "2024-11-10",
                        "subject": "Platform Performance Concerns",
                        "direction": "received",
                        "sentiment": "concerned"
                    }
                ]
            },
            "robert.martinez@contoso.com": {
                "contact_email": "robert.martinez@contoso.com",
                "contact_name": "Robert Martinez",
                "days_analyzed": days,
                "total_emails": 5,
                "sent_by_you": 3,
                "received_from_contact": 2,
                "average_response_time_hours": 48,
                "last_contact": "2023-06-15",
                "communication_trend": "declining",
                "engagement_score": 15,
                "recent_topics": [
                    "Budget Approval Request",
                    "Contract Terms Discussion"
                ]
            }
        }

        return contact_data.get(contact_email, {
            "contact_email": contact_email,
            "contact_name": "Unknown Contact",
            "days_analyzed": days,
            "total_emails": 0,
            "message": "No interaction data found"
        })

    def _get_mock_email_sentiment(self, contact_email: str) -> Dict[str, Any]:
        """Mock email sentiment analysis"""
        sentiment_data = {
            "sarah.chen@contoso.com": {
                "overall_sentiment": "neutral",
                "sentiment_score": 0.5,
                "sentiment_trend": "stable",
                "note": "No communication history - neutral baseline"
            },
            "james.liu@contoso.com": {
                "overall_sentiment": "positive_with_concerns",
                "sentiment_score": 0.68,
                "sentiment_trend": "declining",
                "positive_indicators": [
                    "Responsive communication",
                    "Collaborative tone",
                    "Solution-oriented"
                ],
                "concern_indicators": [
                    "Platform performance issues mentioned 3 times",
                    "Response time increasing",
                    "Less proactive engagement"
                ],
                "recent_sentiment_shift": "Shifted from 0.85 (3 months ago) to 0.68 (current)"
            },
            "robert.martinez@contoso.com": {
                "overall_sentiment": "disengaged",
                "sentiment_score": 0.35,
                "sentiment_trend": "declining",
                "concern_indicators": [
                    "18 months since last contact",
                    "Slow response times (48 hours)",
                    "Minimal engagement"
                ]
            }
        }

        return sentiment_data.get(contact_email, {
            "overall_sentiment": "unknown",
            "sentiment_score": 0.5,
            "message": "No sentiment data available"
        })

    def _get_mock_meeting_history(self, contact_email: str, days: int) -> Dict[str, Any]:
        """Mock meeting history data"""
        meeting_data = {
            "sarah.chen@contoso.com": {
                "contact_email": "sarah.chen@contoso.com",
                "contact_name": "Dr. Sarah Chen",
                "days_analyzed": days,
                "total_meetings": 0,
                "upcoming_meetings": [],
                "past_meetings": [],
                "meeting_frequency": "never",
                "note": "No meetings scheduled or attended"
            },
            "james.liu@contoso.com": {
                "contact_email": "james.liu@contoso.com",
                "contact_name": "James Liu",
                "days_analyzed": days,
                "total_meetings": 12,
                "upcoming_meetings": [
                    {
                        "date": "2024-12-15",
                        "subject": "Q4 Planning Session",
                        "duration_minutes": 60,
                        "attendees": 5,
                        "organizer": "john.smith@yourcompany.com"
                    }
                ],
                "past_meetings": [
                    {
                        "date": "2024-11-10",
                        "subject": "Technical Deep Dive",
                        "duration_minutes": 60,
                        "attendees": 4,
                        "organizer": "john.smith@yourcompany.com",
                        "notes_captured": True
                    },
                    {
                        "date": "2024-10-15",
                        "subject": "Platform Performance Review",
                        "duration_minutes": 45,
                        "attendees": 6,
                        "organizer": "james.liu@contoso.com",
                        "notes_captured": True
                    },
                    {
                        "date": "2024-09-20",
                        "subject": "Executive Business Review",
                        "duration_minutes": 90,
                        "attendees": 8,
                        "organizer": "john.smith@yourcompany.com",
                        "notes_captured": True
                    }
                ],
                "meeting_frequency": "bi-weekly",
                "average_duration_minutes": 65,
                "meeting_acceptance_rate": 0.95
            },
            "robert.martinez@contoso.com": {
                "contact_email": "robert.martinez@contoso.com",
                "contact_name": "Robert Martinez",
                "days_analyzed": days,
                "total_meetings": 1,
                "past_meetings": [
                    {
                        "date": "2023-06-10",
                        "subject": "Contract Negotiation",
                        "duration_minutes": 30,
                        "attendees": 3,
                        "organizer": "john.smith@yourcompany.com"
                    }
                ],
                "meeting_frequency": "rare",
                "note": "Limited meeting history - 18 months since last meeting"
            }
        }

        return meeting_data.get(contact_email, {
            "contact_email": contact_email,
            "days_analyzed": days,
            "total_meetings": 0,
            "message": "No meeting data found"
        })

    def _get_mock_org_chart(self, contact_email: str) -> Dict[str, Any]:
        """Mock org chart data"""
        org_data = {
            "sarah.chen@contoso.com": {
                "user": {
                    "email": "sarah.chen@contoso.com",
                    "name": "Dr. Sarah Chen",
                    "title": "Chief Technology Officer",
                    "department": "Technology"
                },
                "manager": {
                    "email": "patricia.miller@contoso.com",
                    "name": "Patricia Miller",
                    "title": "Chief Executive Officer"
                },
                "direct_reports": [
                    {
                        "email": "james.liu@contoso.com",
                        "name": "James Liu",
                        "title": "VP Engineering"
                    },
                    {
                        "email": "michael.brown@contoso.com",
                        "name": "Michael Brown",
                        "title": "VP Product"
                    },
                    {
                        "email": "lisa.nguyen@contoso.com",
                        "name": "Lisa Nguyen",
                        "title": "VP Security"
                    }
                ],
                "peers": [
                    {
                        "email": "robert.martinez@contoso.com",
                        "name": "Robert Martinez",
                        "title": "Chief Financial Officer"
                    },
                    {
                        "email": "david.kumar@contoso.com",
                        "name": "David Kumar",
                        "title": "VP Operations"
                    }
                ]
            },
            "james.liu@contoso.com": {
                "user": {
                    "email": "james.liu@contoso.com",
                    "name": "James Liu",
                    "title": "VP Engineering",
                    "department": "Engineering"
                },
                "manager": {
                    "email": "sarah.chen@contoso.com",
                    "name": "Dr. Sarah Chen",
                    "title": "Chief Technology Officer"
                },
                "direct_reports": [
                    {
                        "email": "alex.kim@contoso.com",
                        "name": "Alex Kim",
                        "title": "Director of Engineering"
                    },
                    {
                        "email": "rachel.patel@contoso.com",
                        "name": "Rachel Patel",
                        "title": "Engineering Manager"
                    }
                ],
                "peers": [
                    {
                        "email": "michael.brown@contoso.com",
                        "name": "Michael Brown",
                        "title": "VP Product"
                    }
                ]
            }
        }

        return org_data.get(contact_email, {
            "user": {
                "email": contact_email,
                "name": "Unknown User"
            },
            "message": "No org chart data found"
        })

    def _get_mock_user_profile(self, contact_email: str) -> Dict[str, Any]:
        """Mock user profile data"""
        profiles = {
            "sarah.chen@contoso.com": {
                "email": "sarah.chen@contoso.com",
                "display_name": "Dr. Sarah Chen",
                "given_name": "Sarah",
                "surname": "Chen",
                "job_title": "Chief Technology Officer",
                "department": "Technology",
                "office_location": "Seattle, WA",
                "mobile_phone": "+1-206-555-0102",
                "business_phones": ["+1-206-555-0101"],
                "preferred_language": "en-US"
            },
            "james.liu@contoso.com": {
                "email": "james.liu@contoso.com",
                "display_name": "James Liu",
                "given_name": "James",
                "surname": "Liu",
                "job_title": "VP Engineering",
                "department": "Engineering",
                "office_location": "Seattle, WA",
                "mobile_phone": "+1-206-555-0104",
                "business_phones": ["+1-206-555-0104"],
                "preferred_language": "en-US"
            }
        }

        return profiles.get(contact_email, {
            "email": contact_email,
            "message": "Profile not found"
        })

    # ==================== PRODUCTION API METHODS (Stubs) ====================

    def _get_production_email_interactions(self, contact_email: str, days: int) -> Dict[str, Any]:
        """Get email interactions from Graph API"""
        # TODO: Implement Graph API call
        # GET /me/messages?$filter=from/emailAddress/address eq '{contact_email}' or recipients/any(r:r/emailAddress/address eq '{contact_email}')
        # GET /me/mailFolders/sentitems/messages?$filter=recipients/any(r:r/emailAddress/address eq '{contact_email}')
        pass

    def _get_production_email_sentiment(self, contact_email: str) -> Dict[str, Any]:
        """Analyze sentiment using Azure Text Analytics"""
        # TODO: Fetch emails and analyze with Azure Cognitive Services
        pass

    def _get_production_meeting_history(self, contact_email: str, days: int) -> Dict[str, Any]:
        """Get meeting history from Graph API"""
        # TODO: Implement Graph API call
        # GET /me/calendar/events?$filter=attendees/any(a:a/emailAddress/address eq '{contact_email}')
        pass

    def _get_production_org_chart(self, contact_email: str) -> Dict[str, Any]:
        """Get org chart from Graph API"""
        # TODO: Implement Graph API calls
        # GET /users/{contact_email}/manager
        # GET /users/{contact_email}/directReports
        pass

    def _get_production_user_profile(self, contact_email: str) -> Dict[str, Any]:
        """Get user profile from Graph API"""
        # TODO: Implement Graph API call
        # GET /users/{contact_email}
        pass


if __name__ == "__main__":
    # Test the connector in mock mode
    print("Testing Graph Connector in MOCK mode...")
    connector = GraphConnector()

    # Test connection
    connection_test = connector.test_connection()
    print(f"\nConnection Test: {json.dumps(connection_test, indent=2)}")

    # Test email interactions
    print("\n=== Testing Email Interactions ===")
    email_data = connector.get_email_interactions("james.liu@contoso.com")
    print(f"James Liu - Total Emails: {email_data['data']['total_emails']}")
    print(f"Engagement Score: {email_data['data']['engagement_score']}")

    # Test sentiment
    print("\n=== Testing Email Sentiment ===")
    sentiment = connector.get_email_sentiment("james.liu@contoso.com")
    print(f"Overall Sentiment: {sentiment['data']['overall_sentiment']}")
    print(f"Score: {sentiment['data']['sentiment_score']}")

    # Test meetings
    print("\n=== Testing Meeting History ===")
    meetings = connector.get_meeting_history("james.liu@contoso.com")
    print(f"Total Meetings: {meetings['data']['total_meetings']}")
    print(f"Meeting Frequency: {meetings['data']['meeting_frequency']}")

    # Test org chart
    print("\n=== Testing Org Chart ===")
    org_chart = connector.get_org_chart("sarah.chen@contoso.com")
    print(f"User: {org_chart['data']['user']['name']} - {org_chart['data']['user']['title']}")
    print(f"Direct Reports: {len(org_chart['data']['direct_reports'])}")

    print("\n✅ Graph Connector test complete!")
