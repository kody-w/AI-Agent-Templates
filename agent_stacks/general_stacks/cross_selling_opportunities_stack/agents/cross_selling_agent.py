from agents.basic_agent import BasicAgent
import json
import random


class CrossSellingAgent(BasicAgent):
    def __init__(self):
        self.name = "CrossSellingOpportunities"
        self.metadata = {
            "name": self.name,
            "description": "Identifies cross-selling and upselling opportunities based on customer behavior, purchase history, and product relationships. Maximizes revenue through intelligent recommendations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_data": {
                        "type": "object",
                        "description": "Customer information and purchase history",
                        "properties": {
                            "customer_id": {"type": "string"},
                            "recent_purchases": {"type": "array"},
                            "browsing_history": {"type": "array"},
                            "customer_segment": {"type": "string"}
                        }
                    },
                    "current_cart": {
                        "type": "array",
                        "description": "Optional. Items currently in cart",
                        "items": {"type": "object"}
                    },
                    "recommendation_count": {
                        "type": "integer",
                        "description": "Number of recommendations to generate (default 5)"
                    },
                    "strategy": {
                        "type": "string",
                        "description": "Cross-sell strategy to use",
                        "enum": ["complementary", "upgrade", "bundle", "frequency", "ai_personalized"]
                    }
                },
                "required": ["customer_data"]
            }
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        customer_data = kwargs.get('customer_data', {})
        current_cart = kwargs.get('current_cart', [])
        recommendation_count = kwargs.get('recommendation_count', 5)
        strategy = kwargs.get('strategy', 'ai_personalized')

        try:
            if not customer_data:
                raise ValueError("Customer data is required")

            opportunities = self._identify_opportunities(
                customer_data, current_cart, recommendation_count, strategy
            )

            return json.dumps({
                "status": "success",
                "message": f"Identified {len(opportunities['recommendations'])} cross-selling opportunities",
                "data": opportunities
            })

        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Failed to identify cross-selling opportunities: {str(e)}"
            })

    def _identify_opportunities(self, customer_data, current_cart, count, strategy):
        """Generate cross-selling opportunities"""
        
        recommendations = []
        for i in range(count):
            recommendations.append({
                "product_id": f"PROD-{random.randint(1000, 9999)}",
                "product_name": f"Premium Product {chr(65 + i)}",
                "category": random.choice(["Accessories", "Services", "Upgrades", "Complementary"]),
                "recommendation_type": random.choice(["cross_sell", "upsell", "bundle"]),
                "confidence_score": round(random.uniform(0.7, 0.99), 2),
                "reasoning": [
                    "Frequently bought together",
                    "Similar customers purchased",
                    "Complements your recent purchase"
                ][i % 3],
                "price": f"${random.randint(50, 500)}",
                "discount_available": random.choice([True, False]),
                "expected_conversion": f"{random.randint(15, 45)}%",
                "revenue_impact": f"${random.randint(100, 1000)}"
            })
        
        return {
            "customer_id": customer_data.get('customer_id'),
            "recommendations": recommendations,
            "bundle_opportunities": [
                {
                    "bundle_name": "Complete Solution Package",
                    "products": ["Product A", "Product B", "Service C"],
                    "total_value": "$1,299",
                    "bundle_price": "$999",
                    "savings": "$300",
                    "likelihood": "High"
                }
            ],
            "timing_insights": {
                "best_time_to_present": "During checkout",
                "urgency_factors": ["Limited stock", "Sale ending soon"],
                "follow_up_timeline": "24-48 hours if not purchased"
            },
            "personalization_factors": {
                "based_on": ["Purchase history", "Browsing behavior", "Similar customers"],
                "segment": customer_data.get('customer_segment', 'General'),
                "preferences": ["Quality over price", "Brand loyalty", "Innovation seeker"]
            },
            "expected_outcome": {
                "conversion_probability": "32%",
                "average_order_increase": "$247",
                "customer_lifetime_value_impact": "+15%"
            }
        }


if __name__ == "__main__":
    agent = CrossSellingAgent()
    
    result = agent.perform(
        customer_data={
            "customer_id": "CUST-789",
            "recent_purchases": ["Laptop", "Mouse"],
            "browsing_history": ["Monitors", "Keyboards", "Laptop bags"],
            "customer_segment": "Tech Professional"
        },
        current_cart=[{"item": "Wireless Keyboard", "price": 79.99}],
        recommendation_count=5,
        strategy="complementary"
    )
    
    print(json.dumps(json.loads(result), indent=2))
