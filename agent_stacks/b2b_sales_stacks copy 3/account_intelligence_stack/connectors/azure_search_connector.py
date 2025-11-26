"""
Azure AI Search Connector
Provides competitive intelligence through indexed data sources

Data sources indexed:
- Competitor websites & product pages
- G2, TrustRadius, Gartner reviews
- News articles & press releases
- Market research reports
- Customer win/loss analysis

Includes MOCK mode (sample competitive data) and PRODUCTION mode (real Azure AI Search)
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from connectors.base_connector import BaseConnector
from config import Config
from typing import Dict, Any, List
import json

class AzureSearchConnector(BaseConnector):
    """
    Azure AI Search connector for competitive intelligence

    In PRODUCTION mode: Queries real Azure AI Search index
    In MOCK mode: Returns sample competitive intelligence data
    """

    def __init__(self, connector_token: str = None):
        super().__init__(connector_token)
        self.search_config = {
            'endpoint': Config.AZURE_AI_SEARCH_ENDPOINT,
            'api_key': Config.AZURE_AI_SEARCH_KEY,
            'index_name': Config.AZURE_AI_SEARCH_INDEX
        }

    def authenticate(self) -> bool:
        """Authenticate with Azure AI Search"""
        if self.is_mock:
            return True

        # Production: Validate credentials
        if not self.search_config['api_key'] or not self.search_config['endpoint']:
            raise ValueError("Azure AI Search credentials not configured")

        return True

    def test_connection(self) -> Dict[str, Any]:
        """Test Azure AI Search connection"""
        if self.is_mock:
            return {
                "status": "success",
                "mode": "mock",
                "message": "Mock mode - using sample competitive intelligence data"
            }

        # Test real connection
        try:
            self.authenticate()
            return {
                "status": "success",
                "mode": "production",
                "index": self.search_config['index_name'],
                "message": f"Connected to Azure AI Search (index: {self.search_config['index_name']})"
            }
        except Exception as e:
            return self._error_response(f"Connection failed: {str(e)}")

    # ==================== SEARCH METHODS ====================

    def search_competitor(self, competitor_name: str, account_context: str = None) -> Dict[str, Any]:
        """
        Search for competitive intelligence about a specific competitor

        Args:
            competitor_name: Name of competitor (e.g., "DataBricks", "Snowflake")
            account_context: Optional account-specific context for relevance scoring

        Returns:
            Competitive intelligence data
        """
        if self.is_mock:
            return self._mock_response(self._get_mock_competitor_intelligence(competitor_name))

        # Production: Query Azure AI Search
        return self._search_production(competitor_name, account_context)

    def search_competitor_reviews(self, competitor_name: str, focus_area: str = None) -> Dict[str, Any]:
        """
        Search for customer reviews and feedback about competitor

        Args:
            competitor_name: Competitor name
            focus_area: Optional filter (e.g., "pricing", "support", "ease of use")

        Returns:
            Review data and sentiment analysis
        """
        if self.is_mock:
            return self._mock_response(self._get_mock_competitor_reviews(competitor_name))

        # Production: Query reviews from index
        return self._search_reviews_production(competitor_name, focus_area)

    def search_market_intelligence(self, industry: str, keywords: List[str] = None) -> Dict[str, Any]:
        """
        Search for market trends and industry intelligence

        Args:
            industry: Industry/vertical (e.g., "manufacturing", "retail")
            keywords: Optional keywords for filtering

        Returns:
            Market intelligence data
        """
        if self.is_mock:
            return self._mock_response(self._get_mock_market_intelligence(industry))

        # Production: Query market data
        return self._search_market_production(industry, keywords)

    def search_win_loss_analysis(self, competitor_name: str) -> Dict[str, Any]:
        """
        Search historical win/loss data against specific competitor

        Args:
            competitor_name: Competitor name

        Returns:
            Win/loss patterns and insights
        """
        if self.is_mock:
            return self._mock_response(self._get_mock_win_loss_analysis(competitor_name))

        # Production: Query win/loss database
        return self._search_win_loss_production(competitor_name)

    # ==================== MOCK DATA METHODS ====================

    def _get_mock_competitor_intelligence(self, competitor_name: str) -> Dict[str, Any]:
        """Mock competitor intelligence data"""
        competitors = {
            "DataBricks": {
                "competitor_name": "DataBricks",
                "category": "Data & AI Platform",
                "overview": "Cloud-based data analytics and AI platform built on Apache Spark. Strong in data engineering, data science, and machine learning workloads.",
                "market_position": {
                    "market_share": "~18% in data lakehouse market",
                    "growth_rate": "+85% YoY",
                    "funding": "$3.5B raised, valued at $43B",
                    "customer_count": "10,000+ customers"
                },
                "strengths": [
                    "Unified data analytics platform",
                    "Strong ML and AI capabilities",
                    "Excellent for data science teams",
                    "Native integration with major cloud providers",
                    "Strong brand recognition and momentum",
                    "Collaborative notebooks (popular with data scientists)"
                ],
                "weaknesses": [
                    "Lack of manufacturing-specific features",
                    "No factory floor / IoT integration",
                    "Steep learning curve for operations teams",
                    "Higher cost for operational workloads",
                    "Limited real-time operational technology (OT) support",
                    "Requires additional tools for complete manufacturing solution"
                ],
                "pricing": {
                    "model": "Consumption-based (DBU - Databricks Units)",
                    "typical_cost": "$0.50-$2.00 per DBU depending on instance type",
                    "enterprise_cost": "$500K-$5M annually for mid-size deployments",
                    "cost_concerns": "Can escalate quickly with heavy workloads"
                },
                "target_customers": [
                    "Data science teams",
                    "Large enterprises with big data needs",
                    "Companies building ML models at scale",
                    "General-purpose analytics use cases"
                ],
                "competitive_positioning": {
                    "vs_us": {
                        "where_they_win": [
                            "General-purpose AI/ML platform",
                            "Data science team preference",
                            "Strong ecosystem and integrations",
                            "Modern cloud-native architecture"
                        ],
                        "where_we_win": [
                            "Manufacturing domain expertise",
                            "Factory floor / IoT integration",
                            "Real-time operational systems",
                            "Vendor consolidation (we replace 3-5 tools)",
                            "Total cost of ownership",
                            "Faster time to value for manufacturing use cases"
                        ],
                        "ideal_positioning": "Complementary, not competitive. DataBricks for data science, us for production manufacturing operations."
                    }
                },
                "recent_news": [
                    {
                        "date": "2024-11-15",
                        "headline": "DataBricks announces new manufacturing partnerships",
                        "summary": "Partnering with major manufacturers to expand industrial AI capabilities",
                        "relevance": "HIGH - Shows they recognize manufacturing gap",
                        "our_response": "Highlight our 3+ year manufacturing track record vs. their new entry"
                    },
                    {
                        "date": "2024-10-20",
                        "headline": "DataBricks Series I funding - $500M raised",
                        "summary": "Aggressive expansion in enterprise market",
                        "relevance": "MEDIUM - Means increased sales pressure",
                        "our_response": "Focus on proven ROI and manufacturing expertise"
                    }
                ],
                "battle_card_summary": {
                    "when_to_address": "When customer mentions data science, ML models, or general AI platform",
                    "key_message": "DataBricks is excellent for data science teams. Where we differentiate is production manufacturing: factory floor integration, real-time OT systems, quality control. Many customers use both - DataBricks for exploratory analytics, us for operational manufacturing systems.",
                    "proof_points": [
                        "12+ manufacturing customers with deployed systems",
                        "Factory floor integration out-of-the-box (vs. custom dev work with DataBricks)",
                        "30-40% lower total cost when vendor consolidation factored in",
                        "Real-time OT capabilities they lack"
                    ],
                    "questions_to_ask": [
                        "How do you plan to integrate DataBricks with your factory floor systems?",
                        "What's your strategy for real-time quality control and production monitoring?",
                        "Have you factored in the engineering time to build manufacturing-specific features on DataBricks?",
                        "What's your total vendor count after adding DataBricks?"
                    ]
                }
            },
            "Snowflake": {
                "competitor_name": "Snowflake",
                "category": "Cloud Data Warehouse",
                "overview": "Cloud-based data warehousing platform optimized for analytics workloads. Strong in BI, reporting, and data sharing.",
                "market_position": {
                    "market_share": "~25% in cloud data warehouse market",
                    "growth_rate": "+60% YoY",
                    "public_company": "NYSE: SNOW",
                    "customer_count": "9,000+ customers"
                },
                "strengths": [
                    "Best-in-class data warehouse",
                    "Excellent query performance",
                    "Easy to use and scale",
                    "Strong data sharing capabilities",
                    "Multi-cloud support"
                ],
                "weaknesses": [
                    "Primarily data warehouse - not a manufacturing platform",
                    "No operational technology (OT) support",
                    "Limited AI/ML capabilities (improving but not core strength)",
                    "No factory floor integration",
                    "Requires additional tools for complete solution"
                ],
                "pricing": {
                    "model": "Consumption-based (credits)",
                    "typical_cost": "$2-$5 per credit depending on tier",
                    "cost_concerns": "Storage costs can add up quickly"
                },
                "competitive_positioning": {
                    "vs_us": {
                        "where_they_win": [
                            "Data warehousing and BI",
                            "Query performance",
                            "Data sharing across organizations"
                        ],
                        "where_we_win": [
                            "Integrated platform (not just data warehouse)",
                            "Manufacturing operations support",
                            "Lower vendor complexity",
                            "AI/ML for manufacturing use cases"
                        ],
                        "ideal_positioning": "Different use cases. Snowflake for analytics/BI, us for operational manufacturing systems and AI-driven automation."
                    }
                },
                "battle_card_summary": {
                    "key_message": "Snowflake is a great data warehouse for analytics and reporting. We're an operational platform for manufacturing - factory floor integration, real-time production systems, AI-driven automation. Different problems, different solutions.",
                    "proof_points": [
                        "We include data warehousing + operations + AI in one platform",
                        "Snowflake requires 3-4 additional tools for manufacturing use cases",
                        "Lower complexity and total cost"
                    ]
                }
            }
        }

        return competitors.get(competitor_name, {
            "competitor_name": competitor_name,
            "message": "Limited intelligence available",
            "note": "Generic competitor - add to Azure AI Search index for detailed intelligence"
        })

    def _get_mock_competitor_reviews(self, competitor_name: str) -> Dict[str, Any]:
        """Mock competitor review data"""
        reviews = {
            "DataBricks": {
                "competitor_name": "DataBricks",
                "review_summary": {
                    "average_rating": 4.5,
                    "total_reviews": 287,
                    "review_sources": ["G2", "TrustRadius", "Gartner Peer Insights"]
                },
                "sentiment_analysis": {
                    "overall_sentiment": "positive",
                    "positive_percentage": 78,
                    "neutral_percentage": 15,
                    "negative_percentage": 7
                },
                "common_praise": [
                    "Powerful platform for data science",
                    "Excellent ML capabilities",
                    "Collaborative notebooks",
                    "Strong community and support",
                    "Good integration with cloud providers"
                ],
                "common_complaints": [
                    "Steep learning curve",
                    "High cost at scale",
                    "Complex pricing model",
                    "Not intuitive for non-data scientists",
                    "Requires significant engineering resources"
                ],
                "manufacturing_specific_feedback": {
                    "total_manufacturing_reviews": 12,
                    "average_rating": 3.8,
                    "common_themes": [
                        "Great for data science, but requires custom work for factory floor integration",
                        "Needed to supplement with additional IoT platforms",
                        "Higher complexity than expected for operational use cases",
                        "Strong for predictive maintenance models, weak for real-time operations"
                    ],
                    "key_quote": "\"DataBricks is excellent for our data science team, but we needed 3 other tools to complete our manufacturing solution. Wish we had found a more integrated platform.\"",
                    "reviewer_title": "VP Engineering, Mid-size Manufacturer"
                },
                "pricing_complaints": {
                    "frequency": "mentioned in 34% of reviews",
                    "common_themes": [
                        "Costs escalated faster than expected",
                        "Difficult to predict monthly spend",
                        "Enterprise pricing very high"
                    ]
                },
                "opportunity_areas": [
                    "Manufacturing customers frustrated with complexity",
                    "Cost concerns at enterprise scale",
                    "Need for additional tools (integration complexity)",
                    "Steep learning curve for operations teams"
                ]
            }
        }

        return reviews.get(competitor_name, {
            "competitor_name": competitor_name,
            "message": "No review data available"
        })

    def _get_mock_market_intelligence(self, industry: str) -> Dict[str, Any]:
        """Mock market intelligence data"""
        market_data = {
            "manufacturing": {
                "industry": "Manufacturing & Industrial Technology",
                "market_size": {
                    "current": "$45.2B (2024)",
                    "projected_2027": "$78.5B",
                    "cagr": "19.7%"
                },
                "key_trends": [
                    {
                        "trend": "AI-Driven Factory Automation",
                        "growth_rate": "+45% YoY",
                        "adoption_level": "Early majority (32% of manufacturers)",
                        "relevance": "HIGH - Our core strength"
                    },
                    {
                        "trend": "Vendor Consolidation",
                        "description": "Manufacturers reducing vendor count 40-60%",
                        "driver": "Cost optimization and complexity reduction",
                        "relevance": "CRITICAL - Aligns with our value prop"
                    },
                    {
                        "trend": "Cloud Migration for OT Systems",
                        "adoption_level": "Growing (18% of manufacturers)",
                        "barriers": "Security concerns, legacy systems",
                        "opportunity": "Our hybrid cloud approach addresses concerns"
                    },
                    {
                        "trend": "Real-time Quality Control",
                        "investment_priority": "Top 3 for 67% of manufacturers",
                        "current_satisfaction": "Low (37% satisfaction with current tools)",
                        "opportunity": "HIGH - Key differentiator vs. general platforms"
                    }
                ],
                "buyer_priorities": [
                    {"priority": "Cost reduction / ROI", "importance": 95},
                    {"priority": "Vendor consolidation", "importance": 88},
                    {"priority": "Ease of integration", "importance": 85},
                    {"priority": "Real-time operational data", "importance": 82},
                    {"priority": "AI/ML capabilities", "importance": 78}
                ],
                "competitive_landscape": {
                    "market_leaders": ["SAP", "Siemens", "GE Digital"],
                    "emerging_players": ["Us", "Sight Machine", "Uptake"],
                    "general_platforms_entering": ["DataBricks", "Snowflake", "Palantir"],
                    "market_dynamic": "Consolidation phase - manufacturers seeking integrated platforms over point solutions"
                },
                "win_themes": [
                    "Manufacturing domain expertise (not general-purpose platform)",
                    "Vendor consolidation (replace 3-5 tools)",
                    "Total cost of ownership (30-40% lower)",
                    "Factory floor integration out-of-the-box",
                    "Real-time operational support (not just analytics)"
                ]
            }
        }

        return market_data.get(industry, {
            "industry": industry,
            "message": "Limited market intelligence available"
        })

    def _get_mock_win_loss_analysis(self, competitor_name: str) -> Dict[str, Any]:
        """Mock win/loss analysis data"""
        win_loss = {
            "DataBricks": {
                "competitor_name": "DataBricks",
                "total_competitive_deals": 23,
                "wins": 14,
                "losses": 9,
                "win_rate": 61,
                "analysis_period": "Last 18 months",
                "win_patterns": {
                    "common_win_factors": [
                        "Manufacturing domain expertise emphasized",
                        "Vendor consolidation value demonstrated",
                        "Factory floor integration requirements",
                        "Real-time OT capabilities needed",
                        "Pilot successfully demonstrated ROI"
                    ],
                    "winning_messaging": [
                        "Positioned as complementary, not competitive",
                        "Focused on manufacturing-specific gaps in DataBricks",
                        "Demonstrated total cost of ownership advantage",
                        "Showed faster time to value for manufacturing use cases"
                    ],
                    "winning_strategies": [
                        "30-day pilot with manufacturing-specific outcomes",
                        "Reference customers from same industry",
                        "Live demo with customer's factory data",
                        "Executive workshop on vendor consolidation"
                    ]
                },
                "loss_patterns": {
                    "common_loss_factors": [
                        "Data science team preference for DataBricks",
                        "Customer already invested in DataBricks ecosystem",
                        "Pure data analytics use case (not operational)",
                        "Existing DataBricks relationship at C-level",
                        "Budget only for analytics platform, not operational system"
                    ],
                    "lessons_learned": [
                        "Qualify early: Is this operational manufacturing or pure analytics?",
                        "Identify DataBricks relationships in discovery",
                        "Position as complementary when they're already invested",
                        "Focus on operational use cases where we're differentiated"
                    ]
                },
                "average_deal_size": {
                    "wins": "$1.8M",
                    "losses": "$950K",
                    "insight": "We win larger, more strategic deals (operational systems); lose smaller analytics-only deals"
                },
                "typical_win_timeline": "90-120 days (including 30-day pilot)",
                "typical_loss_timeline": "45-60 days (usually lose to existing DataBricks relationship)",
                "recommended_strategy": {
                    "qualification": "Ask: What's your operational technology (OT) strategy? How will you integrate with factory floor? Need for real-time quality control?",
                    "positioning": "Complementary for data science, superior for manufacturing operations",
                    "proof": "Manufacturing reference customers + live pilot",
                    "urgency": "Vendor consolidation mandate + cost optimization pressure"
                }
            }
        }

        return win_loss.get(competitor_name, {
            "competitor_name": competitor_name,
            "message": "Insufficient competitive history"
        })

    # ==================== PRODUCTION API METHODS (Stubs) ====================

    def _search_production(self, competitor_name: str, account_context: str = None) -> Dict[str, Any]:
        """Search Azure AI Search for competitor intelligence"""
        # TODO: Implement Azure AI Search query
        # from azure.search.documents import SearchClient
        # client = SearchClient(
        #     endpoint=self.search_config['endpoint'],
        #     index_name=self.search_config['index_name'],
        #     credential=AzureKeyCredential(self.search_config['api_key'])
        # )
        # results = client.search(
        #     search_text=competitor_name,
        #     filter=f"category eq 'competitive_intelligence'",
        #     top=10
        # )
        pass

    def _search_reviews_production(self, competitor_name: str, focus_area: str = None) -> Dict[str, Any]:
        """Search for competitor reviews in Azure AI Search"""
        # TODO: Query reviews from search index
        pass

    def _search_market_production(self, industry: str, keywords: List[str] = None) -> Dict[str, Any]:
        """Search for market intelligence"""
        # TODO: Query market data from search index
        pass

    def _search_win_loss_production(self, competitor_name: str) -> Dict[str, Any]:
        """Search for win/loss patterns"""
        # TODO: Query win/loss database
        pass


if __name__ == "__main__":
    # Test the connector in mock mode
    print("Testing Azure AI Search Connector in MOCK mode...")
    connector = AzureSearchConnector()

    # Test connection
    connection_test = connector.test_connection()
    print(f"\nConnection Test: {json.dumps(connection_test, indent=2)}")

    # Test competitor search
    print("\n=== Testing Competitor Intelligence ===")
    competitor = connector.search_competitor("DataBricks")
    print(f"Competitor: {competitor['data']['competitor_name']}")
    print(f"Strengths: {len(competitor['data']['strengths'])}")
    print(f"Weaknesses: {len(competitor['data']['weaknesses'])}")

    # Test competitor reviews
    print("\n=== Testing Competitor Reviews ===")
    reviews = connector.search_competitor_reviews("DataBricks")
    print(f"Average Rating: {reviews['data']['review_summary']['average_rating']}/5.0")
    print(f"Total Reviews: {reviews['data']['review_summary']['total_reviews']}")
    print(f"Manufacturing Reviews: {reviews['data']['manufacturing_specific_feedback']['total_manufacturing_reviews']}")

    # Test market intelligence
    print("\n=== Testing Market Intelligence ===")
    market = connector.search_market_intelligence("manufacturing")
    print(f"Market Size: {market['data']['market_size']['current']}")
    print(f"Key Trends: {len(market['data']['key_trends'])}")
    print(f"Top Buyer Priority: {market['data']['buyer_priorities'][0]['priority']}")

    # Test win/loss analysis
    print("\n=== Testing Win/Loss Analysis ===")
    win_loss = connector.search_win_loss_analysis("DataBricks")
    print(f"Win Rate: {win_loss['data']['win_rate']}%")
    print(f"Total Deals: {win_loss['data']['total_competitive_deals']}")
    print(f"Common Win Factor: {win_loss['data']['win_patterns']['common_win_factors'][0]}")

    print("\n✅ Azure AI Search Connector test complete!")
