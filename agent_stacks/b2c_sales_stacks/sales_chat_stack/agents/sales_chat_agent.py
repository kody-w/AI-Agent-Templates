import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))

from agents.basic_agent import BasicAgent
import json
import random
from datetime import datetime, timedelta

class SalesChatAgent(BasicAgent):
    def __init__(self):
        metadata = {
            "name": "Sales Chat Agent",
            "description": "Improves sales access to CRM info, product inventory, and pricing opportunities",
            "version": "1.0.0",
            "author": "Microsoft AI Agent Templates",
            "category": "B2C Sales"
        }
        super().__init__("SalesChatAgent", metadata)
        
        # Simulated product inventory
        self.products = {
            "PROD-001": {"name": "Premium Laptop", "price": 1299.99, "stock": 45, "category": "Electronics"},
            "PROD-002": {"name": "Wireless Mouse", "price": 49.99, "stock": 150, "category": "Accessories"},
            "PROD-003": {"name": "4K Monitor", "price": 599.99, "stock": 23, "category": "Electronics"},
            "PROD-004": {"name": "Mechanical Keyboard", "price": 149.99, "stock": 67, "category": "Accessories"},
            "PROD-005": {"name": "USB-C Hub", "price": 79.99, "stock": 89, "category": "Accessories"}
        }
        
        # Simulated CRM data
        self.customers = {
            "CUST-001": {"name": "Sarah Johnson", "tier": "Gold", "last_purchase": "2024-10-15", "lifetime_value": 15230},
            "CUST-002": {"name": "Mike Chen", "tier": "Silver", "last_purchase": "2024-11-20", "lifetime_value": 8450},
            "CUST-003": {"name": "Emily Davis", "tier": "Platinum", "last_purchase": "2024-12-01", "lifetime_value": 32100}
        }

    def perform(self, **kwargs):
        """
        Main method to handle sales chat interactions
        """
        action = kwargs.get('action', 'get_product_info')
        
        try:
            if action == 'get_product_info':
                return self._get_product_info(kwargs)
            elif action == 'check_inventory':
                return self._check_inventory(kwargs)
            elif action == 'get_customer_info':
                return self._get_customer_info(kwargs)
            elif action == 'generate_pricing_opportunity':
                return self._generate_pricing_opportunity(kwargs)
            elif action == 'get_recommendations':
                return self._get_product_recommendations(kwargs)
            else:
                return self._general_sales_assistance(kwargs)
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error processing sales chat request: {str(e)}",
                "data": {},
                "errors": [str(e)]
            }

    def _get_product_info(self, params):
        """Get detailed product information"""
        product_id = params.get('product_id')
        
        if not product_id:
            # Return all products
            return {
                "status": "success",
                "message": "Product catalog retrieved successfully",
                "data": {
                    "products": self.products,
                    "total_products": len(self.products)
                }
            }
        
        if product_id in self.products:
            product = self.products[product_id]
            return {
                "status": "success",
                "message": f"Product information for {product['name']}",
                "data": {
                    "product_id": product_id,
                    "details": product,
                    "availability": "In Stock" if product['stock'] > 0 else "Out of Stock"
                }
            }
        else:
            return {
                "status": "error",
                "message": f"Product {product_id} not found",
                "data": {},
                "errors": ["Product not found in inventory"]
            }

    def _check_inventory(self, params):
        """Check current inventory levels"""
        category = params.get('category')
        low_stock_threshold = params.get('threshold', 30)
        
        inventory_report = {
            "low_stock_items": [],
            "out_of_stock": [],
            "healthy_stock": []
        }
        
        for product_id, product in self.products.items():
            if category and product['category'] != category:
                continue
                
            if product['stock'] == 0:
                inventory_report['out_of_stock'].append({
                    "id": product_id,
                    "name": product['name'],
                    "stock": 0
                })
            elif product['stock'] < low_stock_threshold:
                inventory_report['low_stock_items'].append({
                    "id": product_id,
                    "name": product['name'],
                    "stock": product['stock']
                })
            else:
                inventory_report['healthy_stock'].append({
                    "id": product_id,
                    "name": product['name'],
                    "stock": product['stock']
                })
        
        return {
            "status": "success",
            "message": "Inventory check completed",
            "data": inventory_report
        }

    def _get_customer_info(self, params):
        """Retrieve customer information from CRM"""
        customer_id = params.get('customer_id')
        
        if not customer_id:
            return {
                "status": "error",
                "message": "Customer ID is required",
                "data": {},
                "errors": ["Missing customer_id parameter"]
            }
        
        if customer_id in self.customers:
            customer = self.customers[customer_id]
            
            # Calculate days since last purchase
            last_purchase = datetime.strptime(customer['last_purchase'], "%Y-%m-%d")
            days_since_purchase = (datetime.now() - last_purchase).days
            
            return {
                "status": "success",
                "message": f"Customer profile for {customer['name']}",
                "data": {
                    "customer_id": customer_id,
                    "profile": customer,
                    "days_since_last_purchase": days_since_purchase,
                    "engagement_recommendation": self._get_engagement_recommendation(customer['tier'], days_since_purchase)
                }
            }
        else:
            return {
                "status": "error",
                "message": f"Customer {customer_id} not found",
                "data": {},
                "errors": ["Customer not found in CRM"]
            }

    def _generate_pricing_opportunity(self, params):
        """Generate dynamic pricing opportunities based on customer and product data"""
        customer_id = params.get('customer_id')
        product_id = params.get('product_id')
        
        opportunities = []
        
        # Bundle opportunities
        if product_id and product_id in self.products:
            base_product = self.products[product_id]
            complementary_products = [
                p for pid, p in self.products.items() 
                if pid != product_id and p['category'] == 'Accessories'
            ]
            
            if complementary_products:
                bundle_discount = random.randint(10, 20)
                opportunities.append({
                    "type": "bundle",
                    "description": f"Bundle {base_product['name']} with accessories",
                    "discount_percentage": bundle_discount,
                    "estimated_value": base_product['price'] * (bundle_discount / 100)
                })
        
        # Loyalty discount
        if customer_id and customer_id in self.customers:
            customer = self.customers[customer_id]
            if customer['tier'] in ['Gold', 'Platinum']:
                loyalty_discount = 15 if customer['tier'] == 'Platinum' else 10
                opportunities.append({
                    "type": "loyalty",
                    "description": f"{customer['tier']} member exclusive discount",
                    "discount_percentage": loyalty_discount,
                    "applicable_to": "All products"
                })
        
        # Volume discount
        opportunities.append({
            "type": "volume",
            "description": "Buy 3 or more items, get 5% off",
            "discount_percentage": 5,
            "minimum_quantity": 3
        })
        
        return {
            "status": "success",
            "message": "Pricing opportunities generated",
            "data": {
                "opportunities": opportunities,
                "total_opportunities": len(opportunities)
            }
        }

    def _get_product_recommendations(self, params):
        """Get personalized product recommendations"""
        customer_id = params.get('customer_id')
        current_product = params.get('current_product')
        
        recommendations = []
        
        # Cross-sell recommendations
        if current_product and current_product in self.products:
            product = self.products[current_product]
            
            # Recommend accessories for electronics
            if product['category'] == 'Electronics':
                accessories = [
                    {"id": pid, **p} for pid, p in self.products.items()
                    if p['category'] == 'Accessories' and p['stock'] > 0
                ]
                recommendations.extend(accessories[:2])
        
        # Upsell recommendations
        all_products = [
            {"id": pid, **p} for pid, p in self.products.items()
            if p['stock'] > 0
        ]
        
        # Sort by price descending and recommend higher-value items
        all_products.sort(key=lambda x: x['price'], reverse=True)
        
        for product in all_products[:3]:
            if {"id": product['id'], **product} not in recommendations:
                recommendations.append(product)
        
        return {
            "status": "success",
            "message": "Product recommendations generated",
            "data": {
                "recommendations": recommendations[:5],
                "recommendation_type": "cross_sell_and_upsell"
            }
        }

    def _get_engagement_recommendation(self, tier, days_since_purchase):
        """Generate customer engagement recommendations"""
        if days_since_purchase > 60:
            return "Re-engagement campaign recommended - customer hasn't purchased in 60+ days"
        elif tier == "Platinum":
            return "VIP treatment - offer exclusive preview of new products"
        elif tier == "Gold":
            return "Loyalty reward eligible - offer special discount"
        else:
            return "Standard engagement - focus on product value propositions"

    def _general_sales_assistance(self, params):
        """Provide general sales assistance"""
        query = params.get('query', '')
        
        return {
            "status": "success",
            "message": "Sales assistance provided",
            "data": {
                "response": "I'm here to help with product information, inventory checks, customer data, and pricing opportunities. How can I assist you today?",
                "available_actions": [
                    "get_product_info",
                    "check_inventory",
                    "get_customer_info",
                    "generate_pricing_opportunity",
                    "get_recommendations"
                ]
            }
        }

if __name__ == "__main__":
    agent = SalesChatAgent()
    
    # Test various functionalities
    print("Testing Sales Chat Agent...")
    print("\n1. Getting product info:")
    result = agent.perform(action='get_product_info', product_id='PROD-001')
    print(json.dumps(result, indent=2))
    
    print("\n2. Checking inventory:")
    result = agent.perform(action='check_inventory', threshold=50)
    print(json.dumps(result, indent=2))
    
    print("\n3. Getting customer info:")
    result = agent.perform(action='get_customer_info', customer_id='CUST-001')
    print(json.dumps(result, indent=2))
    
    print("\n4. Generating pricing opportunities:")
    result = agent.perform(action='generate_pricing_opportunity', customer_id='CUST-001', product_id='PROD-001')
    print(json.dumps(result, indent=2))