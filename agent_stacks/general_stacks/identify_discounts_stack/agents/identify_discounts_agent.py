from agents.basic_agent import BasicAgent
import json
import random
from datetime import datetime, timedelta


class IdentifyDiscountsAgent(BasicAgent):
    def __init__(self):
        self.name = "IdentifyDiscounts"
        self.metadata = {
            "name": self.name,
            "description": "Identifies and applies available discounts, promotions, and special pricing on products and services. Maximizes savings through intelligent discount discovery.",
            "parameters": {
                "type": "object",
                "properties": {
                    "items": {
                        "type": "array",
                        "items": {"type": "object"},
                        "description": "List of items to check for discounts"
                    },
                    "customer_profile": {
                        "type": "object",
                        "description": "Optional. Customer information for personalized discounts",
                        "properties": {
                            "customer_id": {"type": "string"},
                            "membership_level": {"type": "string"},
                            "purchase_history": {"type": "object"}
                        }
                    },
                    "discount_types": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional. Types of discounts to search for",
                        "enum": ["volume", "seasonal", "loyalty", "bundle", "clearance", "coupon", "corporate"]
                    },
                    "auto_apply": {
                        "type": "boolean",
                        "description": "Optional. Automatically apply best discounts"
                    }
                },
                "required": ["items"]
            }
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        items = kwargs.get('items', [])
        customer_profile = kwargs.get('customer_profile', {})
        discount_types = kwargs.get('discount_types', ["all"])
        auto_apply = kwargs.get('auto_apply', True)

        try:
            if not items:
                raise ValueError("Items list is required")

            # Identify and calculate discounts
            discount_analysis = self._identify_discounts(
                items, customer_profile, discount_types, auto_apply
            )

            return json.dumps({
                "status": "success",
                "message": f"Identified {discount_analysis['total_discounts_found']} discounts",
                "data": discount_analysis
            })

        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Failed to identify discounts: {str(e)}"
            })

    def _identify_discounts(self, items, customer_profile, discount_types, auto_apply):
        """Identify applicable discounts"""
        
        original_total = sum(random.uniform(50, 500) for _ in range(len(items)))
        
        discounts = {
            "applicable_discounts": [
                {
                    "discount_id": f"DISC-{random.randint(1000, 9999)}",
                    "type": "Volume Discount",
                    "description": "Buy 3 or more, get 15% off",
                    "amount": original_total * 0.15,
                    "conditions": "Minimum 3 items",
                    "auto_applied": auto_apply,
                    "expires": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
                },
                {
                    "discount_id": f"DISC-{random.randint(1000, 9999)}",
                    "type": "Loyalty Reward",
                    "description": "VIP member exclusive discount",
                    "amount": original_total * 0.10,
                    "conditions": "VIP membership required",
                    "auto_applied": auto_apply and customer_profile.get('membership_level') == 'VIP',
                    "expires": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
                },
                {
                    "discount_id": f"DISC-{random.randint(1000, 9999)}",
                    "type": "Bundle Savings",
                    "description": "Complete solution bundle discount",
                    "amount": original_total * 0.20,
                    "conditions": "Purchase complete bundle",
                    "auto_applied": False,
                    "expires": (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
                }
            ],
            "coupon_codes": [
                {
                    "code": "SAVE20NOW",
                    "discount": "20% off",
                    "applicable": True,
                    "restrictions": "First-time customers only"
                },
                {
                    "code": "FREESHIP",
                    "discount": "Free shipping",
                    "applicable": original_total > 100,
                    "restrictions": "Orders over $100"
                }
            ],
            "summary": {
                "original_total": f"${original_total:.2f}",
                "total_discounts_found": 5,
                "maximum_savings": f"${original_total * 0.35:.2f}",
                "recommended_discount": "Bundle Savings - 20% off",
                "final_price_with_best": f"${original_total * 0.80:.2f}"
            },
            "optimization_tips": [
                "Add 2 more items to qualify for bulk discount",
                "Consider annual subscription for 30% savings",
                "Combine with cashback credit card for additional 2% off"
            ]
        }
        
        return discounts


if __name__ == "__main__":
    agent = IdentifyDiscountsAgent()
    
    result = agent.perform(
        items=[
            {"product_id": "P001", "name": "Product A", "price": 199.99},
            {"product_id": "P002", "name": "Product B", "price": 299.99}
        ],
        customer_profile={
            "customer_id": "CUST-123",
            "membership_level": "VIP"
        },
        discount_types=["volume", "loyalty", "bundle"],
        auto_apply=True
    )
    
    print(json.dumps(json.loads(result), indent=2))
