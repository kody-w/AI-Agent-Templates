from agents.basic_agent import BasicAgent
import json
import random
from datetime import datetime, timedelta


class ProcurementSupportAgent(BasicAgent):
    def __init__(self):
        self.name = "ProcurementSupport"
        self.metadata = {
            "name": self.name,
            "description": "Streamlines procurement processes by automating vendor selection, purchase order creation, approval workflows, and spend analysis. Ensures compliance and optimizes purchasing decisions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "procurement_action": {
                        "type": "string",
                        "description": "Type of procurement action",
                        "enum": ["vendor_selection", "create_po", "approval_request", "spend_analysis", "contract_review", "supplier_evaluation"]
                    },
                    "request_details": {
                        "type": "object",
                        "description": "Details of the procurement request",
                        "properties": {
                            "item_description": {"type": "string"},
                            "quantity": {"type": "integer"},
                            "budget": {"type": "number"},
                            "urgency": {"type": "string"},
                            "department": {"type": "string"}
                        }
                    },
                    "compliance_check": {
                        "type": "boolean",
                        "description": "Optional. Perform compliance verification"
                    },
                    "preferred_vendors": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional. List of preferred vendors"
                    }
                },
                "required": ["procurement_action", "request_details"]
            }
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        procurement_action = kwargs.get('procurement_action')
        request_details = kwargs.get('request_details', {})
        compliance_check = kwargs.get('compliance_check', True)
        preferred_vendors = kwargs.get('preferred_vendors', [])

        try:
            if not procurement_action or not request_details:
                raise ValueError("Procurement action and request details are required")

            # Process procurement request
            result = self._process_procurement(
                procurement_action, request_details, compliance_check, preferred_vendors
            )

            return json.dumps({
                "status": "success",
                "message": f"Procurement {procurement_action} completed successfully",
                "data": result
            })

        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Failed to process procurement request: {str(e)}"
            })

    def _process_procurement(self, action, details, compliance_check, preferred_vendors):
        """Process procurement request based on action type"""
        
        result = {
            "request_id": f"PRO-{random.randint(100000, 999999)}",
            "action": action,
            "timestamp": datetime.now().isoformat(),
            "department": details.get('department', 'General')
        }
        
        if action == "vendor_selection":
            result.update(self._select_vendors(details, preferred_vendors))
        
        elif action == "create_po":
            result.update(self._create_purchase_order(details))
        
        elif action == "approval_request":
            result.update(self._process_approval(details))
        
        elif action == "spend_analysis":
            result.update(self._analyze_spend(details))
        
        elif action == "contract_review":
            result.update(self._review_contract(details))
        
        elif action == "supplier_evaluation":
            result.update(self._evaluate_suppliers(preferred_vendors))
        
        # Add compliance check if requested
        if compliance_check:
            result["compliance"] = self._check_compliance(details)
        
        # Add recommendations
        result["recommendations"] = self._generate_recommendations(action, details)
        
        return result

    def _select_vendors(self, details, preferred_vendors):
        """Select optimal vendors based on criteria"""
        vendors = []
        for i in range(3):
            vendors.append({
                "vendor_id": f"VEN-{random.randint(1000, 9999)}",
                "name": preferred_vendors[i] if i < len(preferred_vendors) else f"Vendor {chr(65 + i)}",
                "score": round(random.uniform(75, 98), 1),
                "price_quote": f"${random.randint(1000, 10000):,}",
                "delivery_time": f"{random.randint(3, 30)} days",
                "quality_rating": round(random.uniform(4.0, 5.0), 1),
                "compliance_status": "Verified",
                "payment_terms": random.choice(["Net 30", "Net 60", "2/10 Net 30"]),
                "certifications": ["ISO 9001", "ISO 14001"],
                "past_performance": {
                    "on_time_delivery": f"{random.randint(85, 100)}%",
                    "quality_issues": random.randint(0, 3),
                    "total_orders": random.randint(10, 100)
                }
            })
        
        return {
            "vendor_selection": {
                "recommended_vendor": vendors[0]["name"],
                "vendors_evaluated": vendors,
                "selection_criteria": {
                    "price_weight": "40%",
                    "quality_weight": "30%",
                    "delivery_weight": "20%",
                    "compliance_weight": "10%"
                },
                "savings_opportunity": f"${random.randint(500, 5000):,}",
                "negotiation_points": [
                    "Volume discount available",
                    "Payment terms improvement possible",
                    "Free shipping on orders over $5000"
                ]
            }
        }

    def _create_purchase_order(self, details):
        """Create purchase order"""
        po_number = f"PO-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
        
        return {
            "purchase_order": {
                "po_number": po_number,
                "status": "Draft",
                "items": [
                    {
                        "description": details.get('item_description', 'Standard Item'),
                        "quantity": details.get('quantity', 1),
                        "unit_price": random.uniform(100, 1000),
                        "total": details.get('quantity', 1) * random.uniform(100, 1000)
                    }
                ],
                "total_amount": f"${random.randint(1000, 50000):,}",
                "tax": f"${random.randint(50, 500):,}",
                "shipping": f"${random.randint(20, 200):,}",
                "grand_total": f"${random.randint(1100, 51000):,}",
                "delivery_date": (datetime.now() + timedelta(days=random.randint(7, 30))).strftime("%Y-%m-%d"),
                "payment_terms": "Net 30",
                "approval_status": "Pending",
                "approvers": [
                    {"name": "Manager", "status": "Pending"},
                    {"name": "Finance", "status": "Pending"}
                ]
            }
        }

    def _process_approval(self, details):
        """Process approval workflow"""
        budget = details.get('budget', 10000)
        
        approval_levels = []
        if budget < 5000:
            approval_levels = ["Direct Manager"]
        elif budget < 25000:
            approval_levels = ["Direct Manager", "Department Head"]
        else:
            approval_levels = ["Direct Manager", "Department Head", "CFO"]
        
        return {
            "approval_workflow": {
                "approval_required": approval_levels,
                "current_approver": approval_levels[0],
                "approval_status": "In Progress",
                "estimated_completion": f"{random.randint(1, 5)} business days",
                "approval_chain": [
                    {
                        "approver": level,
                        "status": "Pending" if i > 0 else "In Review",
                        "sla": f"{random.randint(1, 3)} days"
                    }
                    for i, level in enumerate(approval_levels)
                ],
                "auto_escalation": True,
                "escalation_time": "48 hours"
            }
        }

    def _analyze_spend(self, details):
        """Analyze procurement spend"""
        return {
            "spend_analysis": {
                "total_spend_ytd": f"${random.randint(100000, 1000000):,}",
                "department_spend": f"${random.randint(10000, 100000):,}",
                "category_breakdown": {
                    "IT Equipment": "35%",
                    "Office Supplies": "20%",
                    "Services": "25%",
                    "Software": "20%"
                },
                "vendor_concentration": {
                    "top_vendor": "Vendor A (40%)",
                    "vendor_count": 25,
                    "single_source_risk": "Medium"
                },
                "savings_achieved": f"${random.randint(5000, 50000):,}",
                "maverick_spend": f"{random.randint(5, 15)}%",
                "contract_compliance": f"{random.randint(85, 98)}%",
                "opportunities": [
                    "Consolidate vendors for better pricing",
                    "Negotiate volume discounts",
                    "Implement purchase cards for small purchases"
                ]
            }
        }

    def _review_contract(self, details):
        """Review contract terms"""
        return {
            "contract_review": {
                "contract_id": f"CTR-{random.randint(1000, 9999)}",
                "review_status": "Completed",
                "risk_assessment": {
                    "overall_risk": random.choice(["Low", "Medium", "High"]),
                    "financial_risk": "Low",
                    "operational_risk": "Medium",
                    "compliance_risk": "Low"
                },
                "key_terms": {
                    "duration": "12 months",
                    "value": f"${random.randint(10000, 100000):,}",
                    "payment_terms": "Net 30",
                    "termination_clause": "30 days notice",
                    "liability_cap": "Contract value",
                    "sla_defined": True
                },
                "red_flags": [
                    "Auto-renewal clause needs review",
                    "Penalty clauses seem excessive"
                ],
                "recommendations": [
                    "Negotiate liability cap increase",
                    "Add performance metrics",
                    "Include right to audit clause"
                ]
            }
        }

    def _evaluate_suppliers(self, suppliers):
        """Evaluate supplier performance"""
        evaluations = []
        for supplier in suppliers[:3]:
            evaluations.append({
                "supplier": supplier or f"Supplier {random.randint(1, 100)}",
                "overall_score": round(random.uniform(70, 95), 1),
                "performance_metrics": {
                    "quality": round(random.uniform(4.0, 5.0), 1),
                    "delivery": round(random.uniform(4.0, 5.0), 1),
                    "cost": round(random.uniform(3.5, 5.0), 1),
                    "service": round(random.uniform(4.0, 5.0), 1),
                    "innovation": round(random.uniform(3.0, 5.0), 1)
                },
                "risk_profile": random.choice(["Low", "Medium"]),
                "recommendation": random.choice(["Preferred", "Approved", "Under Review"])
            })
        
        return {
            "supplier_evaluation": {
                "evaluations": evaluations,
                "top_performers": [e["supplier"] for e in evaluations if e["overall_score"] > 85],
                "improvement_needed": [e["supplier"] for e in evaluations if e["overall_score"] < 75],
                "certification_status": {
                    "iso_certified": len([e for e in evaluations if random.choice([True, False])]),
                    "diversity_certified": len([e for e in evaluations if random.choice([True, False])])
                }
            }
        }

    def _check_compliance(self, details):
        """Check procurement compliance"""
        return {
            "policy_compliant": True,
            "budget_approved": details.get('budget', 0) < 50000,
            "vendor_approved": True,
            "competitive_bid": details.get('budget', 0) > 10000,
            "documentation_complete": random.choice([True, False]),
            "audit_trail": "Maintained",
            "flags": [] if random.choice([True, False]) else ["Missing approval signature"]
        }

    def _generate_recommendations(self, action, details):
        """Generate procurement recommendations"""
        return {
            "cost_savings": [
                "Consider bulk purchasing for additional 10% discount",
                "Negotiate annual contract for better rates",
                "Explore alternative suppliers for price comparison"
            ],
            "process_improvements": [
                "Implement e-procurement system",
                "Standardize purchase requisition forms",
                "Set up preferred vendor agreements"
            ],
            "risk_mitigation": [
                "Diversify supplier base",
                "Maintain safety stock for critical items",
                "Regular supplier audits"
            ]
        }


if __name__ == "__main__":
    agent = ProcurementSupportAgent()
    
    result = agent.perform(
        procurement_action="vendor_selection",
        request_details={
            "item_description": "Laptop computers for new hires",
            "quantity": 50,
            "budget": 75000,
            "urgency": "Medium",
            "department": "IT"
        },
        compliance_check=True,
        preferred_vendors=["TechSupply Corp", "Digital Solutions Inc"]
    )
    
    print(json.dumps(json.loads(result), indent=2))
