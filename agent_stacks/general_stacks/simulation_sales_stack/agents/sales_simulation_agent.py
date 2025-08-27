"""
Sales Simulation Agent
Part of the Simulation Sales Stack

This agent simulates sales scenarios and customer interactions
for training and testing purposes.
"""

from typing import Dict, List, Optional
import json
import random
from datetime import datetime, timedelta

class SalesSimulationAgent:
    """Agent for simulating sales scenarios and customer interactions"""
    
    def __init__(self):
        self.scenarios = {
            "cold_call": self._simulate_cold_call,
            "product_demo": self._simulate_product_demo,
            "negotiation": self._simulate_negotiation,
            "closing": self._simulate_closing
        }
        
    def simulate_scenario(self, scenario_type: str, parameters: Dict) -> Dict:
        """
        Simulate a specific sales scenario
        
        Args:
            scenario_type: Type of scenario to simulate
            parameters: Scenario parameters
            
        Returns:
            Simulation results
        """
        if scenario_type not in self.scenarios:
            return {"error": f"Unknown scenario type: {scenario_type}"}
            
        return self.scenarios[scenario_type](parameters)
    
    def _simulate_cold_call(self, params: Dict) -> Dict:
        """Simulate a cold call scenario"""
        outcomes = ["interested", "not_interested", "callback_requested", "referred"]
        outcome = random.choice(outcomes)
        
        return {
            "scenario": "cold_call",
            "outcome": outcome,
            "duration_minutes": random.randint(2, 15),
            "notes": self._generate_call_notes(outcome),
            "next_action": self._suggest_next_action(outcome)
        }
    
    def _simulate_product_demo(self, params: Dict) -> Dict:
        """Simulate a product demonstration"""
        engagement_levels = ["high", "medium", "low"]
        questions_asked = random.randint(0, 10)
        
        return {
            "scenario": "product_demo",
            "engagement": random.choice(engagement_levels),
            "questions_asked": questions_asked,
            "features_interested": self._get_interested_features(),
            "concerns": self._get_common_concerns(),
            "follow_up_required": questions_asked > 3
        }
    
    def _simulate_negotiation(self, params: Dict) -> Dict:
        """Simulate price negotiation"""
        initial_price = params.get("initial_price", 10000)
        discount_percentage = random.uniform(0, 25)
        
        return {
            "scenario": "negotiation",
            "initial_price": initial_price,
            "discount_offered": discount_percentage,
            "final_price": initial_price * (1 - discount_percentage / 100),
            "terms": self._generate_terms(),
            "decision": random.choice(["accepted", "rejected", "thinking"])
        }
    
    def _simulate_closing(self, params: Dict) -> Dict:
        """Simulate deal closing"""
        close_probability = random.uniform(0, 1)
        
        return {
            "scenario": "closing",
            "success": close_probability > 0.3,
            "close_probability": round(close_probability, 2),
            "contract_value": params.get("contract_value", random.randint(5000, 100000)),
            "close_date": self._generate_close_date(),
            "payment_terms": self._generate_payment_terms()
        }
    
    def _generate_call_notes(self, outcome: str) -> str:
        """Generate realistic call notes based on outcome"""
        notes_templates = {
            "interested": "Customer showed interest in {product}. Scheduled follow-up for {date}.",
            "not_interested": "Not a good fit at this time. May revisit in Q{quarter}.",
            "callback_requested": "Customer busy. Requested callback on {date} at {time}.",
            "referred": "Referred to {department} team for better alignment."
        }
        
        template = notes_templates.get(outcome, "Call completed.")
        # Add placeholders logic here
        return template
    
    def _suggest_next_action(self, outcome: str) -> str:
        """Suggest next action based on call outcome"""
        actions = {
            "interested": "Schedule product demo",
            "not_interested": "Add to nurture campaign",
            "callback_requested": "Set reminder for callback",
            "referred": "Warm transfer to appropriate team"
        }
        return actions.get(outcome, "Update CRM and review")
    
    def _get_interested_features(self) -> List[str]:
        """Get list of features customer is interested in"""
        all_features = [
            "automation", "reporting", "integration", 
            "scalability", "security", "analytics",
            "mobile_access", "customization"
        ]
        return random.sample(all_features, random.randint(2, 5))
    
    def _get_common_concerns(self) -> List[str]:
        """Get common customer concerns"""
        concerns = [
            "pricing", "implementation_time", "training_requirements",
            "integration_complexity", "roi_timeline", "support_availability"
        ]
        return random.sample(concerns, random.randint(1, 3))
    
    def _generate_terms(self) -> Dict:
        """Generate negotiation terms"""
        return {
            "payment_plan": random.choice(["monthly", "quarterly", "annual"]),
            "contract_length": random.choice([12, 24, 36]),
            "support_level": random.choice(["basic", "premium", "enterprise"])
        }
    
    def _generate_close_date(self) -> str:
        """Generate expected close date"""
        days_ahead = random.randint(7, 90)
        close_date = datetime.now() + timedelta(days=days_ahead)
        return close_date.strftime("%Y-%m-%d")
    
    def _generate_payment_terms(self) -> str:
        """Generate payment terms"""
        terms = ["Net 30", "Net 60", "50% upfront, 50% on delivery", "Monthly subscription"]
        return random.choice(terms)

# Example usage
if __name__ == "__main__":
    agent = SalesSimulationAgent()
    
    # Simulate a cold call
    result = agent.simulate_scenario("cold_call", {})
    print("Cold Call Simulation:", json.dumps(result, indent=2))
    
    # Simulate a product demo
    result = agent.simulate_scenario("product_demo", {})
    print("\nProduct Demo Simulation:", json.dumps(result, indent=2))