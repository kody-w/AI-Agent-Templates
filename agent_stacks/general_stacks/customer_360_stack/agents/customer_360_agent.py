from agents.basic_agent import BasicAgent
import json
from datetime import datetime, timedelta
import random


class Customer360Agent(BasicAgent):
    def __init__(self):
        self.name = "Customer360"
        self.metadata = {
            "name": self.name,
            "description": "Provides a comprehensive 360-degree view of customer data by aggregating information from multiple touchpoints, including purchase history, support interactions, preferences, and behavioral analytics.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "Unique identifier for the customer"
                    },
                    "data_sources": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional. Specific data sources to query (e.g., 'crm', 'support', 'sales', 'marketing', 'social')"
                    },
                    "include_predictions": {
                        "type": "boolean",
                        "description": "Optional. Include predictive analytics like churn risk and lifetime value"
                    },
                    "time_range": {
                        "type": "string",
                        "description": "Optional. Time range for historical data (e.g., '30d', '6m', '1y')",
                        "enum": ["7d", "30d", "90d", "6m", "1y", "all"]
                    },
                    "include_segments": {
                        "type": "boolean",
                        "description": "Optional. Include customer segmentation data"
                    }
                },
                "required": ["customer_id"]
            }
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        customer_id = kwargs.get('customer_id')
        data_sources = kwargs.get('data_sources', ['crm', 'support', 'sales', 'marketing'])
        include_predictions = kwargs.get('include_predictions', True)
        time_range = kwargs.get('time_range', '1y')
        include_segments = kwargs.get('include_segments', True)

        try:
            # Validate customer_id
            if not customer_id or not customer_id.strip():
                raise ValueError("Customer ID is required and cannot be empty")

            # Generate mock customer 360 data
            customer_data = self._generate_customer_360_data(
                customer_id, data_sources, include_predictions, time_range, include_segments
            )

            return json.dumps({
                "status": "success",
                "message": f"Successfully retrieved 360-degree view for customer {customer_id}",
                "data": customer_data
            })

        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Failed to retrieve customer 360 data: {str(e)}"
            })

    def _generate_customer_360_data(self, customer_id, data_sources, include_predictions, time_range, include_segments):
        """Generate realistic mock customer 360 data"""
        
        # Base customer profile
        profile = {
            "customer_id": customer_id,
            "personal_info": {
                "name": f"Customer {customer_id[-4:]}",
                "email": f"customer.{customer_id[-4:]}@example.com",
                "phone": f"+1-555-{customer_id[-4:]}",
                "account_created": "2021-03-15",
                "preferred_language": "English",
                "time_zone": "EST"
            },
            "demographics": {
                "age_group": random.choice(["18-24", "25-34", "35-44", "45-54", "55+"]),
                "location": {
                    "city": random.choice(["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]),
                    "state": random.choice(["NY", "CA", "IL", "TX", "AZ"]),
                    "country": "USA"
                },
                "income_bracket": random.choice(["$25-50k", "$50-75k", "$75-100k", "$100-150k", "$150k+"])
            }
        }

        # Purchase history
        if 'sales' in data_sources:
            profile["purchase_history"] = {
                "total_purchases": random.randint(5, 50),
                "total_spent": f"${random.randint(500, 50000):,}",
                "average_order_value": f"${random.randint(50, 500)}",
                "last_purchase_date": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),
                "favorite_categories": random.sample(["Electronics", "Clothing", "Home & Garden", "Sports", "Books"], 3),
                "recent_items": [
                    {"name": "Premium Laptop", "price": "$1,299", "date": "2024-01-15"},
                    {"name": "Wireless Headphones", "price": "$249", "date": "2024-01-10"},
                    {"name": "Smart Watch", "price": "$399", "date": "2023-12-28"}
                ],
                "purchase_frequency": random.choice(["Weekly", "Monthly", "Quarterly", "Seasonal"])
            }

        # Support interactions
        if 'support' in data_sources:
            profile["support_interactions"] = {
                "total_tickets": random.randint(0, 15),
                "open_tickets": random.randint(0, 2),
                "average_resolution_time": f"{random.randint(2, 48)} hours",
                "satisfaction_score": round(random.uniform(3.5, 5.0), 1),
                "last_interaction": (datetime.now() - timedelta(days=random.randint(1, 60))).strftime("%Y-%m-%d"),
                "common_issues": random.sample(["Shipping", "Product Information", "Returns", "Technical Support"], 2),
                "preferred_channel": random.choice(["Email", "Phone", "Chat", "Self-Service"])
            }

        # Marketing engagement
        if 'marketing' in data_sources:
            profile["marketing_engagement"] = {
                "email_subscription": True,
                "email_open_rate": f"{random.randint(20, 80)}%",
                "email_click_rate": f"{random.randint(5, 30)}%",
                "campaign_responses": random.randint(2, 20),
                "preferred_content": random.sample(["Product Updates", "Promotions", "Educational", "Events"], 2),
                "channel_preferences": {
                    "email": random.choice(["High", "Medium", "Low"]),
                    "sms": random.choice(["High", "Medium", "Low"]),
                    "push": random.choice(["High", "Medium", "Low"]),
                    "social": random.choice(["High", "Medium", "Low"])
                },
                "last_campaign_interaction": "2024-01-20"
            }

        # Behavioral analytics
        profile["behavioral_analytics"] = {
            "engagement_score": random.randint(60, 100),
            "activity_level": random.choice(["Highly Active", "Active", "Moderate", "Low"]),
            "preferred_shopping_time": random.choice(["Morning", "Afternoon", "Evening", "Weekend"]),
            "device_preferences": {
                "mobile": f"{random.randint(30, 70)}%",
                "desktop": f"{random.randint(20, 60)}%",
                "tablet": f"{random.randint(5, 20)}%"
            },
            "average_session_duration": f"{random.randint(3, 15)} minutes",
            "pages_per_session": random.randint(3, 12)
        }

        # Predictive analytics
        if include_predictions:
            profile["predictive_analytics"] = {
                "churn_risk": {
                    "score": random.randint(0, 100),
                    "level": random.choice(["Low", "Medium", "High"]),
                    "factors": random.sample([
                        "Decreased purchase frequency",
                        "Lower engagement",
                        "Support issues",
                        "Competitive offers"
                    ], 2)
                },
                "lifetime_value": {
                    "estimated": f"${random.randint(5000, 100000):,}",
                    "confidence": f"{random.randint(70, 95)}%"
                },
                "next_purchase_prediction": {
                    "timeframe": random.choice(["Within 7 days", "Within 30 days", "Within 60 days"]),
                    "likely_categories": random.sample(["Electronics", "Clothing", "Home", "Sports"], 2),
                    "confidence": f"{random.randint(60, 90)}%"
                },
                "upsell_opportunities": [
                    {"product": "Premium Subscription", "likelihood": "High", "value": "$199/year"},
                    {"product": "Extended Warranty", "likelihood": "Medium", "value": "$99"}
                ]
            }

        # Customer segments
        if include_segments:
            profile["segmentation"] = {
                "primary_segment": random.choice(["VIP", "Loyal", "Growth", "New", "At-Risk"]),
                "value_tier": random.choice(["Platinum", "Gold", "Silver", "Bronze"]),
                "behavioral_segments": random.sample([
                    "Tech Enthusiast",
                    "Price Conscious",
                    "Brand Loyal",
                    "Trendsetter",
                    "Convenience Seeker"
                ], 2),
                "lifecycle_stage": random.choice(["Acquisition", "Activation", "Retention", "Revenue", "Referral"])
            }

        # Loyalty program
        profile["loyalty_program"] = {
            "member": True,
            "tier": random.choice(["Platinum", "Gold", "Silver", "Bronze"]),
            "points_balance": random.randint(100, 10000),
            "points_earned_ytd": random.randint(500, 5000),
            "rewards_redeemed": random.randint(0, 10),
            "member_since": "2021-06-01"
        }

        # Social data (if available)
        if 'social' in data_sources:
            profile["social_presence"] = {
                "connected_accounts": random.sample(["Twitter", "Facebook", "Instagram", "LinkedIn"], 2),
                "sentiment_score": random.choice(["Positive", "Neutral", "Mixed"]),
                "influence_score": random.randint(1, 100),
                "brand_mentions": random.randint(0, 20),
                "community_participation": random.choice(["Active", "Occasional", "Observer"])
            }

        # Recommendations
        profile["recommendations"] = {
            "next_best_action": random.choice([
                "Send personalized product recommendation",
                "Offer loyalty reward",
                "Proactive support outreach",
                "VIP upgrade invitation",
                "Birthday discount"
            ]),
            "engagement_strategies": [
                "Personalized email campaign",
                "Exclusive preview access",
                "Customer feedback survey"
            ],
            "retention_tactics": [
                "Loyalty point bonus",
                "Free shipping offer",
                "Personal shopper service"
            ]
        }

        # Add summary statistics
        profile["summary"] = {
            "customer_value_score": random.randint(70, 100),
            "engagement_trend": random.choice(["Increasing", "Stable", "Decreasing"]),
            "risk_indicators": random.randint(0, 3),
            "opportunities_identified": random.randint(2, 8),
            "data_completeness": f"{random.randint(75, 100)}%",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        return profile


if __name__ == "__main__":
    agent = Customer360Agent()
    
    # Test with sample customer ID
    result = agent.perform(
        customer_id="CUST-2024-0001",
        data_sources=["crm", "support", "sales", "marketing", "social"],
        include_predictions=True,
        time_range="1y",
        include_segments=True
    )
    
    print(json.dumps(json.loads(result), indent=2))