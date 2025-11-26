"""
LinkedIn Sales Navigator Connector (via Power Platform)

Provides access to LinkedIn data through Power Platform connector:
- Professional profiles
- Career history
- Connections & mutual connections
- Recent posts & engagement
- Skills & endorsements

This connector uses Power Platform LinkedIn connector tokens passed from Copilot Studio
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from connectors.base_connector import BaseConnector
from config import Config
from typing import Dict, Any, List
import json

class LinkedInConnector(BaseConnector):
    """
    LinkedIn Sales Navigator connector via Power Platform

    In PRODUCTION mode, this connector expects a Power Platform connector token
    to be passed from Copilot Studio via the Azure Function HTTP header.

    The token provides authenticated access to LinkedIn Sales Navigator APIs
    without requiring separate LinkedIn API credentials.
    """

    def __init__(self, connector_token: str = None):
        super().__init__(connector_token)
        self.linkedin_config = {
            'api_key': Config.LINKEDIN_API_KEY,
            'connector_url': Config.LINKEDIN_CONNECTOR_URL
        }

    def authenticate(self) -> bool:
        """Authenticate with LinkedIn (via Power Platform token)"""
        if self.is_mock:
            return True

        # Production: Use Power Platform connector token
        if not self.connector_token:
            raise ValueError("LinkedIn connector requires Power Platform connector token")

        return True

    def test_connection(self) -> Dict[str, Any]:
        """Test LinkedIn connection"""
        if self.is_mock:
            return {
                "status": "success",
                "mode": "mock",
                "message": "Mock mode - no real LinkedIn connection"
            }

        # Test Power Platform connector
        try:
            if not self.connector_token:
                return self._error_response("No Power Platform connector token provided")

            return {
                "status": "success",
                "mode": "production",
                "message": "Connected to LinkedIn via Power Platform"
            }
        except Exception as e:
            return self._error_response(f"Connection failed: {str(e)}")

    # ==================== PROFILE METHODS ====================

    def get_profile(self, contact_email: str = None, linkedin_url: str = None) -> Dict[str, Any]:
        """
        Get LinkedIn profile data

        Args:
            contact_email: Contact's email (for lookup)
            linkedin_url: Direct LinkedIn profile URL

        Returns:
            LinkedIn profile data
        """
        if self.is_mock:
            return self._mock_response(self._get_mock_profile(contact_email or linkedin_url))

        # Production: Call Power Platform LinkedIn connector
        return self._get_production_profile(contact_email, linkedin_url)

    def get_career_history(self, contact_email: str) -> Dict[str, Any]:
        """
        Get career history from LinkedIn

        Args:
            contact_email: Contact's email

        Returns:
            Career history with job timeline
        """
        if self.is_mock:
            return self._mock_response(self._get_mock_career_history(contact_email))

        # Production: Call LinkedIn API via Power Platform
        return self._get_production_career_history(contact_email)

    def get_connections(self, contact_email: str) -> Dict[str, Any]:
        """
        Get connection information and mutual connections

        Args:
            contact_email: Contact's email

        Returns:
            Connection network data
        """
        if self.is_mock:
            return self._mock_response(self._get_mock_connections(contact_email))

        # Production: Call LinkedIn API via Power Platform
        return self._get_production_connections(contact_email)

    def get_recent_activity(self, contact_email: str, days: int = 30) -> Dict[str, Any]:
        """
        Get recent LinkedIn posts and activity

        Args:
            contact_email: Contact's email
            days: Number of days to look back

        Returns:
            Recent posts, comments, shares
        """
        if self.is_mock:
            return self._mock_response(self._get_mock_recent_activity(contact_email, days))

        # Production: Call LinkedIn API via Power Platform
        return self._get_production_recent_activity(contact_email, days)

    # ==================== MOCK DATA METHODS ====================

    def _get_mock_profile(self, identifier: str) -> Dict[str, Any]:
        """Mock LinkedIn profile data"""
        profiles = {
            "sarah.chen@contoso.com": {
                "linkedin_url": "linkedin.com/in/sarahchen",
                "full_name": "Dr. Sarah Chen",
                "headline": "Chief Technology Officer at Contoso Corporation | AI & Cloud Transformation Leader",
                "location": "Seattle, Washington, United States",
                "industry": "Computer Software",
                "current_position": {
                    "title": "Chief Technology Officer",
                    "company": "Contoso Corporation",
                    "start_date": "2024-10",
                    "duration": "2 months"
                },
                "previous_positions_count": 4,
                "education": [
                    {
                        "school": "Stanford University",
                        "degree": "Ph.D.",
                        "field": "Computer Science",
                        "years": "2008-2013"
                    },
                    {
                        "school": "MIT",
                        "degree": "M.S.",
                        "field": "Electrical Engineering",
                        "years": "2006-2008"
                    }
                ],
                "connections": "500+",
                "mutual_connections": 12,
                "skills": [
                    "Cloud Architecture",
                    "AI/ML Strategy",
                    "Digital Transformation",
                    "Enterprise Software",
                    "Team Leadership"
                ],
                "endorsements_count": 247,
                "recommendations_count": 18,
                "profile_views_last_90_days": 1234,
                "recent_job_change": True,
                "open_to_opportunities": False
            },
            "james.liu@contoso.com": {
                "linkedin_url": "linkedin.com/in/jamesliu",
                "full_name": "James Liu",
                "headline": "VP Engineering at Contoso Corporation | Building Scalable Systems",
                "location": "Seattle, Washington, United States",
                "industry": "Computer Software",
                "current_position": {
                    "title": "VP Engineering",
                    "company": "Contoso Corporation",
                    "start_date": "2019-03",
                    "duration": "5 years 9 months"
                },
                "previous_positions_count": 3,
                "education": [
                    {
                        "school": "UC Berkeley",
                        "degree": "B.S.",
                        "field": "Computer Science",
                        "years": "2010-2014"
                    }
                ],
                "connections": "500+",
                "mutual_connections": 45,
                "skills": [
                    "Software Engineering",
                    "Cloud Infrastructure",
                    "Team Management",
                    "System Architecture",
                    "DevOps"
                ],
                "endorsements_count": 189,
                "recommendations_count": 12,
                "profile_views_last_90_days": 456,
                "recent_job_change": False,
                "open_to_opportunities": False
            },
            "robert.martinez@contoso.com": {
                "linkedin_url": "linkedin.com/in/robertmartinez",
                "full_name": "Robert Martinez",
                "headline": "Chief Financial Officer at Contoso Corporation",
                "location": "Seattle, Washington, United States",
                "industry": "Manufacturing",
                "current_position": {
                    "title": "Chief Financial Officer",
                    "company": "Contoso Corporation",
                    "start_date": "2022-11",
                    "duration": "2 years 1 month"
                },
                "previous_positions_count": 5,
                "education": [
                    {
                        "school": "Wharton School of Business",
                        "degree": "MBA",
                        "field": "Finance",
                        "years": "2008-2010"
                    }
                ],
                "connections": "500+",
                "mutual_connections": 8,
                "skills": [
                    "Financial Planning",
                    "Corporate Finance",
                    "M&A",
                    "Strategic Planning",
                    "P&L Management"
                ],
                "endorsements_count": 156,
                "recommendations_count": 14,
                "profile_views_last_90_days": 234,
                "recent_job_change": False,
                "open_to_opportunities": False
            }
        }

        return profiles.get(identifier, {
            "message": "Profile not found",
            "linkedin_url": identifier if "linkedin.com" in str(identifier) else None
        })

    def _get_mock_career_history(self, contact_email: str) -> Dict[str, Any]:
        """Mock career history data"""
        career_data = {
            "sarah.chen@contoso.com": {
                "full_name": "Dr. Sarah Chen",
                "current_role": {
                    "title": "Chief Technology Officer",
                    "company": "Contoso Corporation",
                    "duration": "2 months",
                    "start_date": "2024-10"
                },
                "career_timeline": [
                    {
                        "title": "VP Cloud Engineering",
                        "company": "Microsoft",
                        "duration": "3 years",
                        "dates": "2021-10 to 2024-10",
                        "description": "Led Azure infrastructure team, 200+ engineers"
                    },
                    {
                        "title": "Director of Engineering",
                        "company": "Amazon Web Services",
                        "duration": "4 years",
                        "dates": "2017-06 to 2021-09",
                        "description": "Built EC2 container services"
                    },
                    {
                        "title": "Senior Software Engineer",
                        "company": "Google",
                        "duration": "3 years",
                        "dates": "2014-06 to 2017-05",
                        "description": "Infrastructure automation"
                    },
                    {
                        "title": "Software Engineer",
                        "company": "Facebook",
                        "duration": "1 year",
                        "dates": "2013-06 to 2014-05",
                        "description": "Data center optimization"
                    }
                ],
                "career_insights": {
                    "total_years_experience": 11,
                    "companies_worked": 5,
                    "average_tenure": "2.2 years",
                    "career_trajectory": "steadily_upward",
                    "industry_expertise": ["Cloud Computing", "AI/ML", "Enterprise Software"],
                    "notable_achievements": [
                        "Built Microsoft's largest ML infrastructure",
                        "Led AWS container services to 100K+ customers",
                        "Published 12 technical papers on distributed systems"
                    ]
                },
                "relevance_to_deal": {
                    "cloud_modernization_expert": True,
                    "vendor_consolidation_experience": True,
                    "cost_optimization_focus": True,
                    "new_to_role": True,
                    "risk_level": "high - likely to re-evaluate all vendors"
                }
            },
            "james.liu@contoso.com": {
                "full_name": "James Liu",
                "current_role": {
                    "title": "VP Engineering",
                    "company": "Contoso Corporation",
                    "duration": "5 years 9 months",
                    "start_date": "2019-03"
                },
                "career_timeline": [
                    {
                        "title": "Director of Engineering",
                        "company": "Salesforce",
                        "duration": "3 years",
                        "dates": "2016-01 to 2019-02"
                    },
                    {
                        "title": "Engineering Manager",
                        "company": "Oracle",
                        "duration": "2 years",
                        "dates": "2014-06 to 2015-12"
                    }
                ],
                "career_insights": {
                    "total_years_experience": 10,
                    "companies_worked": 3,
                    "average_tenure": "3.3 years",
                    "career_trajectory": "steady",
                    "industry_expertise": ["Enterprise Software", "SaaS"],
                    "tenure_at_contoso": "longest_in_career",
                    "loyalty_indicator": "high"
                },
                "relevance_to_deal": {
                    "long_tenure": True,
                    "institutional_knowledge": True,
                    "relationship_strength": "champion",
                    "risk_level": "low - reliable advocate"
                }
            }
        }

        return career_data.get(contact_email, {
            "message": "No career history found"
        })

    def _get_mock_connections(self, contact_email: str) -> Dict[str, Any]:
        """Mock connections data"""
        connections = {
            "sarah.chen@contoso.com": {
                "full_name": "Dr. Sarah Chen",
                "total_connections": "500+",
                "mutual_connections": 12,
                "mutual_connection_names": [
                    "Alex Zhang (VP Sales, Your Company)",
                    "Maria Garcia (Enterprise Account Manager, Your Company)",
                    "Jennifer Kim (Former Microsoft colleague)",
                    "David Park (AWS connection)",
                    "Rachel Williams (Stanford classmate)"
                ],
                "connection_strength": "weak",
                "shared_groups": [
                    "Women in Technology Leadership",
                    "Cloud Architecture Forum",
                    "Stanford Alumni - Seattle"
                ],
                "introduction_paths": [
                    {
                        "path": "You → Alex Zhang → Sarah Chen",
                        "strength": "strong",
                        "recommendation": "Best path - Alex worked with Sarah at Microsoft"
                    },
                    {
                        "path": "You → Maria Garcia → Jennifer Kim → Sarah Chen",
                        "strength": "medium",
                        "recommendation": "Alternative if Alex unavailable"
                    }
                ],
                "warm_intro_available": True,
                "recommended_connector": "Alex Zhang"
            },
            "james.liu@contoso.com": {
                "full_name": "James Liu",
                "total_connections": "500+",
                "mutual_connections": 45,
                "connection_strength": "strong",
                "mutual_connection_names": [
                    "John Smith (Your Account Executive)",
                    "Sarah Johnson (Your Solutions Architect)",
                    "15 other colleagues at Your Company"
                ],
                "shared_groups": [
                    "Enterprise Software Leaders",
                    "Bay Area Tech",
                    "UC Berkeley Alumni"
                ],
                "relationship_notes": "Already well connected - champion status"
            }
        }

        return connections.get(contact_email, {
            "message": "No connection data found"
        })

    def _get_mock_recent_activity(self, contact_email: str, days: int) -> Dict[str, Any]:
        """Mock recent LinkedIn activity"""
        activity = {
            "sarah.chen@contoso.com": {
                "full_name": "Dr. Sarah Chen",
                "days_analyzed": days,
                "total_posts": 5,
                "total_comments": 3,
                "total_reactions": 247,
                "recent_posts": [
                    {
                        "date": "2024-11-28",
                        "type": "post",
                        "content": "Excited to share that we're modernizing Contoso's tech stack! Looking for partners who understand manufacturing + AI. #DigitalTransformation #CloudFirst",
                        "reactions": 156,
                        "comments": 23,
                        "shares": 12,
                        "sentiment": "positive",
                        "relevance_to_deal": "HIGH - Actively seeking technology partners",
                        "keywords": ["modernizing", "partners", "manufacturing", "AI", "cloud"]
                    },
                    {
                        "date": "2024-11-20",
                        "type": "post",
                        "content": "Day 30 of my 100-day plan at Contoso. Key focus: Vendor consolidation and cost optimization. We're auditing all software spend.",
                        "reactions": 98,
                        "comments": 15,
                        "shares": 5,
                        "sentiment": "analytical",
                        "relevance_to_deal": "CRITICAL - Vendor consolidation mentioned explicitly",
                        "keywords": ["vendor consolidation", "cost optimization", "software spend"]
                    },
                    {
                        "date": "2024-11-10",
                        "type": "comment",
                        "original_post_by": "Industry Analyst",
                        "content": "Agreed - the future is multi-cloud with AI-native architecture. Single-vendor lock-in is a risk we can't afford.",
                        "reactions": 45,
                        "relevance_to_deal": "MEDIUM - Comments on multi-cloud strategy",
                        "keywords": ["multi-cloud", "AI-native", "vendor lock-in"]
                    }
                ],
                "activity_insights": {
                    "posting_frequency": "2-3 times per week",
                    "engagement_level": "high",
                    "topics_of_interest": [
                        "Cloud modernization",
                        "AI/ML",
                        "Vendor management",
                        "Cost optimization",
                        "Manufacturing technology"
                    ],
                    "sentiment_trend": "positive_but_analytical",
                    "deal_implications": [
                        "She's actively broadcasting need for partners",
                        "Cost consciousness is TOP priority",
                        "Vendor consolidation underway - window of opportunity",
                        "Looking for manufacturing expertise"
                    ]
                }
            },
            "james.liu@contoso.com": {
                "full_name": "James Liu",
                "days_analyzed": days,
                "total_posts": 2,
                "total_comments": 5,
                "recent_posts": [
                    {
                        "date": "2024-11-15",
                        "type": "post",
                        "content": "Great Q3 business review with our technology partners. Excited about new capabilities coming in 2025.",
                        "reactions": 34,
                        "comments": 8,
                        "sentiment": "positive"
                    }
                ],
                "activity_insights": {
                    "posting_frequency": "1-2 times per month",
                    "engagement_level": "moderate",
                    "sentiment_trend": "positive"
                }
            }
        }

        return activity.get(contact_email, {
            "message": "No recent activity found"
        })

    # ==================== PRODUCTION API METHODS (Stubs) ====================

    def _get_production_profile(self, contact_email: str, linkedin_url: str) -> Dict[str, Any]:
        """Get LinkedIn profile via Power Platform connector"""
        # TODO: Call Power Platform LinkedIn connector
        # POST {connector_url}/api/profiles/lookup
        # Headers: Authorization: Bearer {connector_token}
        # Body: {"email": contact_email} or {"profile_url": linkedin_url}
        pass

    def _get_production_career_history(self, contact_email: str) -> Dict[str, Any]:
        """Get career history via Power Platform connector"""
        # TODO: Call Power Platform LinkedIn connector
        # GET {connector_url}/api/profiles/{profile_id}/experience
        pass

    def _get_production_connections(self, contact_email: str) -> Dict[str, Any]:
        """Get connections via Power Platform connector"""
        # TODO: Call Power Platform LinkedIn connector
        # GET {connector_url}/api/profiles/{profile_id}/connections
        pass

    def _get_production_recent_activity(self, contact_email: str, days: int) -> Dict[str, Any]:
        """Get recent activity via Power Platform connector"""
        # TODO: Call Power Platform LinkedIn connector
        # GET {connector_url}/api/profiles/{profile_id}/activity?days={days}
        pass


if __name__ == "__main__":
    # Test the connector in mock mode
    print("Testing LinkedIn Connector in MOCK mode...")
    connector = LinkedInConnector()

    # Test connection
    connection_test = connector.test_connection()
    print(f"\nConnection Test: {json.dumps(connection_test, indent=2)}")

    # Test profile
    print("\n=== Testing LinkedIn Profile ===")
    profile = connector.get_profile("sarah.chen@contoso.com")
    print(f"Name: {profile['data']['full_name']}")
    print(f"Headline: {profile['data']['headline']}")
    print(f"Recent Job Change: {profile['data']['recent_job_change']}")

    # Test career history
    print("\n=== Testing Career History ===")
    career = connector.get_career_history("sarah.chen@contoso.com")
    print(f"Total Experience: {career['data']['career_insights']['total_years_experience']} years")
    print(f"Previous Companies: {len(career['data']['career_timeline'])}")
    print(f"Risk Level: {career['data']['relevance_to_deal']['risk_level']}")

    # Test connections
    print("\n=== Testing Connections ===")
    connections = connector.get_connections("sarah.chen@contoso.com")
    print(f"Mutual Connections: {connections['data']['mutual_connections']}")
    print(f"Warm Intro Available: {connections['data']['warm_intro_available']}")
    print(f"Recommended Connector: {connections['data']['recommended_connector']}")

    # Test activity
    print("\n=== Testing Recent Activity ===")
    activity = connector.get_recent_activity("sarah.chen@contoso.com")
    print(f"Total Posts: {activity['data']['total_posts']}")
    print(f"Most Recent Post Relevance: {activity['data']['recent_posts'][0]['relevance_to_deal']}")

    print("\n✅ LinkedIn Connector test complete!")
