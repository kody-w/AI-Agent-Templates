import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))

from agents.basic_agent import BasicAgent
import json
import random
from datetime import datetime, timedelta

class ProcurementAgent(BasicAgent):
    def __init__(self):
        metadata = {
            "name": "Procurement Agent",
            "description": "Streamlines procurement processes with Microsoft Teams integration",
            "version": "1.0.0",
            "author": "Microsoft AI Agent Templates",
            "category": "B2E General Purpose"
        }
        super().__init__("ProcurementAgent", metadata)
        
        # Simulated vendor database
        self.vendors = {
            "VEND-001": {"name": "TechSupply Co", "category": "IT Equipment", "rating": 4.8, "lead_time": 3},
            "VEND-002": {"name": "Office Plus", "category": "Office Supplies", "rating": 4.5, "lead_time": 2},
            "VEND-003": {"name": "Global Manufacturing", "category": "Raw Materials", "rating": 4.6, "lead_time": 7},
            "VEND-004": {"name": "ServicePro", "category": "Professional Services", "rating": 4.9, "lead_time": 1}
        }
        
        # Simulated purchase orders
        self.purchase_orders = {
            "PO-2024-001": {
                "vendor": "VEND-001",
                "items": [{"name": "Laptops", "quantity": 50, "unit_price": 1200}],
                "status": "Approved",
                "total": 60000,
                "date": "2024-11-15"
            },
            "PO-2024-002": {
                "vendor": "VEND-002",
                "items": [{"name": "Office Chairs", "quantity": 25, "unit_price": 350}],
                "status": "Pending",
                "total": 8750,
                "date": "2024-11-20"
            }
        }
        
        # Approval thresholds
        self.approval_thresholds = {
            "auto": 5000,
            "manager": 25000,
            "director": 100000,
            "cfo": float('inf')
        }

    def perform(self, **kwargs):
        """
        Main method to handle procurement operations
        """
        action = kwargs.get('action', 'get_vendor_list')
        
        try:
            if action == 'get_vendor_list':
                return self._get_vendor_list(kwargs)
            elif action == 'create_purchase_order':
                return self._create_purchase_order(kwargs)
            elif action == 'check_approval_status':
                return self._check_approval_status(kwargs)
            elif action == 'compare_vendors':
                return self._compare_vendors(kwargs)
            elif action == 'get_spending_analytics':
                return self._get_spending_analytics(kwargs)
            elif action == 'request_quote':
                return self._request_quote(kwargs)
            else:
                return self._general_procurement_help(kwargs)
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error processing procurement request: {str(e)}",
                "data": {},
                "errors": [str(e)]
            }

    def _get_vendor_list(self, params):
        """Get list of approved vendors"""
        category = params.get('category')
        
        vendor_list = []
        for vendor_id, vendor in self.vendors.items():
            if not category or vendor['category'] == category:
                vendor_list.append({
                    "id": vendor_id,
                    **vendor
                })
        
        return {
            "status": "success",
            "message": f"Found {len(vendor_list)} vendors",
            "data": {
                "vendors": vendor_list,
                "total_count": len(vendor_list)
            }
        }

    def _create_purchase_order(self, params):
        """Create a new purchase order"""
        vendor_id = params.get('vendor_id')
        items = params.get('items', [])
        requester = params.get('requester', 'Employee')
        
        if not vendor_id or vendor_id not in self.vendors:
            return {
                "status": "error",
                "message": "Invalid vendor ID",
                "data": {},
                "errors": ["Vendor not found"]
            }
        
        if not items:
            return {
                "status": "error",
                "message": "No items specified",
                "data": {},
                "errors": ["Items list is empty"]
            }
        
        # Calculate total
        total = sum(item.get('quantity', 0) * item.get('unit_price', 0) for item in items)
        
        # Determine approval requirement
        approval_level = self._determine_approval_level(total)
        
        # Generate PO number
        po_number = f"PO-{datetime.now().year}-{random.randint(1000, 9999)}"
        
        # Create the purchase order
        new_po = {
            "po_number": po_number,
            "vendor_id": vendor_id,
            "vendor_name": self.vendors[vendor_id]['name'],
            "items": items,
            "total": total,
            "status": "Pending" if approval_level != "auto" else "Approved",
            "approval_level": approval_level,
            "requester": requester,
            "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "estimated_delivery": (datetime.now() + timedelta(days=self.vendors[vendor_id]['lead_time'])).strftime("%Y-%m-%d")
        }
        
        # Add to purchase orders
        self.purchase_orders[po_number] = new_po
        
        # Send Teams notification (simulated)
        teams_notification = self._send_teams_notification(po_number, approval_level)
        
        return {
            "status": "success",
            "message": f"Purchase order {po_number} created successfully",
            "data": {
                "purchase_order": new_po,
                "teams_notification": teams_notification
            }
        }

    def _check_approval_status(self, params):
        """Check approval status of purchase orders"""
        po_number = params.get('po_number')
        
        if po_number:
            if po_number in self.purchase_orders:
                po = self.purchase_orders[po_number]
                return {
                    "status": "success",
                    "message": f"Purchase order {po_number} status retrieved",
                    "data": {
                        "po_number": po_number,
                        "status": po['status'],
                        "details": po
                    }
                }
            else:
                return {
                    "status": "error",
                    "message": f"Purchase order {po_number} not found",
                    "data": {},
                    "errors": ["PO not found"]
                }
        else:
            # Return all pending approvals
            pending_pos = {
                po_id: po for po_id, po in self.purchase_orders.items()
                if po['status'] == 'Pending'
            }
            
            return {
                "status": "success",
                "message": f"Found {len(pending_pos)} pending approvals",
                "data": {
                    "pending_approvals": pending_pos
                }
            }

    def _compare_vendors(self, params):
        """Compare vendors for specific requirements"""
        category = params.get('category')
        requirements = params.get('requirements', {})
        
        comparison = []
        for vendor_id, vendor in self.vendors.items():
            if not category or vendor['category'] == category:
                score = self._calculate_vendor_score(vendor, requirements)
                comparison.append({
                    "vendor_id": vendor_id,
                    "vendor_name": vendor['name'],
                    "rating": vendor['rating'],
                    "lead_time": vendor['lead_time'],
                    "score": score,
                    "recommendation": "Recommended" if score > 80 else "Consider" if score > 60 else "Alternative"
                })
        
        # Sort by score
        comparison.sort(key=lambda x: x['score'], reverse=True)
        
        return {
            "status": "success",
            "message": "Vendor comparison completed",
            "data": {
                "comparison": comparison,
                "best_vendor": comparison[0] if comparison else None
            }
        }

    def _get_spending_analytics(self, params):
        """Get procurement spending analytics"""
        time_period = params.get('period', 'month')
        
        # Calculate spending by category
        spending_by_category = {}
        total_spending = 0
        
        for po in self.purchase_orders.values():
            if po['status'] == 'Approved':
                vendor_id = po.get('vendor', po.get('vendor_id'))
                if vendor_id in self.vendors:
                    category = self.vendors[vendor_id]['category']
                    spending_by_category[category] = spending_by_category.get(category, 0) + po['total']
                    total_spending += po['total']
        
        # Calculate savings opportunities
        savings_opportunities = []
        if total_spending > 100000:
            savings_opportunities.append({
                "type": "Volume Discount",
                "potential_savings": total_spending * 0.05,
                "description": "Negotiate volume discounts with top vendors"
            })
        
        if len(self.vendors) > 3:
            savings_opportunities.append({
                "type": "Vendor Consolidation",
                "potential_savings": total_spending * 0.03,
                "description": "Consolidate purchases with fewer vendors for better rates"
            })
        
        return {
            "status": "success",
            "message": "Spending analytics generated",
            "data": {
                "total_spending": total_spending,
                "spending_by_category": spending_by_category,
                "active_vendors": len(self.vendors),
                "total_purchase_orders": len(self.purchase_orders),
                "savings_opportunities": savings_opportunities,
                "period": time_period
            }
        }

    def _request_quote(self, params):
        """Request quotes from vendors"""
        items = params.get('items', [])
        category = params.get('category')
        urgent = params.get('urgent', False)
        
        if not items:
            return {
                "status": "error",
                "message": "No items specified for quote",
                "data": {},
                "errors": ["Items list is empty"]
            }
        
        # Find relevant vendors
        relevant_vendors = []
        for vendor_id, vendor in self.vendors.items():
            if not category or vendor['category'] == category:
                relevant_vendors.append({
                    "vendor_id": vendor_id,
                    "vendor_name": vendor['name']
                })
        
        # Generate RFQ
        rfq_number = f"RFQ-{datetime.now().year}-{random.randint(1000, 9999)}"
        
        # Simulate quote generation
        quotes = []
        for vendor in relevant_vendors:
            base_price = sum(item.get('quantity', 1) * random.uniform(50, 500) for item in items)
            discount = random.uniform(0, 15) if not urgent else 0
            
            quotes.append({
                "vendor_id": vendor['vendor_id'],
                "vendor_name": vendor['vendor_name'],
                "base_price": round(base_price, 2),
                "discount_percentage": round(discount, 1),
                "final_price": round(base_price * (1 - discount/100), 2),
                "delivery_days": self.vendors[vendor['vendor_id']]['lead_time'] if not urgent else 1,
                "validity_days": 30
            })
        
        # Sort by final price
        quotes.sort(key=lambda x: x['final_price'])
        
        return {
            "status": "success",
            "message": f"RFQ {rfq_number} sent to {len(quotes)} vendors",
            "data": {
                "rfq_number": rfq_number,
                "items_requested": items,
                "quotes_received": quotes,
                "best_quote": quotes[0] if quotes else None,
                "teams_channel_notified": True
            }
        }

    def _determine_approval_level(self, amount):
        """Determine approval level based on amount"""
        if amount <= self.approval_thresholds['auto']:
            return "auto"
        elif amount <= self.approval_thresholds['manager']:
            return "manager"
        elif amount <= self.approval_thresholds['director']:
            return "director"
        else:
            return "cfo"

    def _calculate_vendor_score(self, vendor, requirements):
        """Calculate vendor score based on requirements"""
        base_score = vendor['rating'] * 20  # Max 100
        
        # Adjust for lead time
        if requirements.get('urgent'):
            base_score -= vendor['lead_time'] * 5
        
        # Random factors for demo
        base_score += random.uniform(-10, 10)
        
        return max(0, min(100, base_score))

    def _send_teams_notification(self, po_number, approval_level):
        """Simulate sending Teams notification"""
        return {
            "channel": "Procurement",
            "message": f"New PO {po_number} requires {approval_level} approval",
            "sent": True,
            "timestamp": datetime.now().isoformat()
        }

    def _general_procurement_help(self, params):
        """Provide general procurement assistance"""
        return {
            "status": "success",
            "message": "Procurement Agent ready to assist",
            "data": {
                "available_actions": [
                    "get_vendor_list",
                    "create_purchase_order",
                    "check_approval_status",
                    "compare_vendors",
                    "get_spending_analytics",
                    "request_quote"
                ],
                "teams_integration": "Active",
                "help_text": "I can help you streamline procurement processes, manage vendors, create purchase orders, and track approvals through Microsoft Teams."
            }
        }

if __name__ == "__main__":
    agent = ProcurementAgent()
    
    print("Testing Procurement Agent...")
    print("\n1. Getting vendor list:")
    result = agent.perform(action='get_vendor_list')
    print(json.dumps(result, indent=2))
    
    print("\n2. Creating purchase order:")
    result = agent.perform(
        action='create_purchase_order',
        vendor_id='VEND-001',
        items=[{"name": "Laptops", "quantity": 10, "unit_price": 1200}],
        requester="John Doe"
    )
    print(json.dumps(result, indent=2))
    
    print("\n3. Getting spending analytics:")
    result = agent.perform(action='get_spending_analytics')
    print(json.dumps(result, indent=2))