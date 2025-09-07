import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))

from agents.basic_agent import BasicAgent
import json
import random
from datetime import datetime, timedelta

class Customer360SpeechAgent(BasicAgent):
    def __init__(self):
        metadata = {
            "name": "Customer 360 Speech Agent",
            "description": "Voice-enabled CRM agent with comprehensive account details and sales history",
            "version": "1.0.0",
            "author": "Microsoft AI Agent Templates",
            "category": "B2C Sales"
        }
        super().__init__("Customer360SpeechAgent", metadata)
        
        # Simulated customer 360 database
        self.customers = {
            "CUST-001": {
                "name": "Jennifer Williams",
                "phone": "+1-555-0123",
                "email": "j.williams@email.com",
                "segment": "Premium",
                "lifetime_value": 45670,
                "account_status": "Active",
                "preferred_channel": "Voice",
                "language": "English",
                "purchase_history": [
                    {"date": "2024-10-15", "product": "Smart Home Bundle", "amount": 2499},
                    {"date": "2024-08-22", "product": "Premium Subscription", "amount": 299},
                    {"date": "2024-06-10", "product": "Device Protection Plan", "amount": 199}
                ],
                "interactions": [
                    {"date": "2024-11-01", "type": "Support Call", "duration": "15 min", "satisfaction": 5},
                    {"date": "2024-10-20", "type": "Sales Call", "duration": "8 min", "result": "Purchase"},
                    {"date": "2024-09-15", "type": "Chat", "duration": "12 min", "satisfaction": 4}
                ],
                "preferences": {
                    "contact_time": "Evenings",
                    "communication": "Voice preferred",
                    "interests": ["Smart Home", "Security", "Entertainment"]
                }
            },
            "CUST-002": {
                "name": "Robert Chen",
                "phone": "+1-555-0456",
                "email": "r.chen@email.com",
                "segment": "Standard",
                "lifetime_value": 12340,
                "account_status": "Active",
                "preferred_channel": "Email",
                "language": "English",
                "purchase_history": [
                    {"date": "2024-09-30", "product": "Basic Plan", "amount": 99},
                    {"date": "2024-07-15", "product": "Accessories Pack", "amount": 149}
                ],
                "interactions": [
                    {"date": "2024-10-10", "type": "Email", "response_time": "2 hours", "satisfaction": 4}
                ],
                "preferences": {
                    "contact_time": "Business hours",
                    "communication": "Email preferred",
                    "interests": ["Budget Options", "Deals", "Basic Services"]
                }
            }
        }
        
        # Voice command patterns
        self.voice_commands = {
            "lookup": ["find customer", "search for", "pull up", "show me"],
            "history": ["purchase history", "what did they buy", "past orders", "transaction history"],
            "profile": ["customer profile", "account details", "tell me about", "customer information"],
            "recommendations": ["what should I offer", "recommendations", "suggest products", "cross-sell"],
            "notes": ["add note", "log interaction", "update record", "save comment"]
        }

    def perform(self, **kwargs):
        """
        Main method to handle voice-enabled CRM operations
        """
        action = kwargs.get('action', 'voice_lookup')
        voice_input = kwargs.get('voice_input', '')
        
        try:
            # Process voice command if provided
            if voice_input:
                action = self._parse_voice_command(voice_input)
                kwargs['parsed_action'] = action
            
            if action == 'voice_lookup':
                return self._voice_customer_lookup(kwargs)
            elif action == 'get_customer_360':
                return self._get_customer_360(kwargs)
            elif action == 'get_purchase_history':
                return self._get_purchase_history(kwargs)
            elif action == 'get_interaction_history':
                return self._get_interaction_history(kwargs)
            elif action == 'generate_recommendations':
                return self._generate_recommendations(kwargs)
            elif action == 'update_interaction':
                return self._update_interaction(kwargs)
            elif action == 'get_voice_summary':
                return self._get_voice_summary(kwargs)
            else:
                return self._general_voice_assistance(kwargs)
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error processing voice CRM request: {str(e)}",
                "data": {},
                "errors": [str(e)]
            }

    def _parse_voice_command(self, voice_input):
        """Parse voice input to determine action"""
        voice_lower = voice_input.lower()
        
        for action, patterns in self.voice_commands.items():
            for pattern in patterns:
                if pattern in voice_lower:
                    if action == "lookup":
                        return "voice_lookup"
                    elif action == "history":
                        return "get_purchase_history"
                    elif action == "profile":
                        return "get_customer_360"
                    elif action == "recommendations":
                        return "generate_recommendations"
                    elif action == "notes":
                        return "update_interaction"
        
        return "voice_lookup"

    def _voice_customer_lookup(self, params):
        """Lookup customer by voice query"""
        search_term = params.get('search_term', '')
        voice_input = params.get('voice_input', '')
        
        # Extract customer name from voice input
        if voice_input and not search_term:
            # Simple extraction logic for demo
            words = voice_input.lower().split()
            for customer_id, customer in self.customers.items():
                name_parts = customer['name'].lower().split()
                if any(part in words for part in name_parts):
                    search_term = customer['name']
                    break
        
        # Find matching customer
        matched_customer = None
        matched_id = None
        
        for customer_id, customer in self.customers.items():
            if search_term.lower() in customer['name'].lower() or \
               search_term in customer['phone'] or \
               search_term in customer['email']:
                matched_customer = customer
                matched_id = customer_id
                break
        
        if matched_customer:
            return {
                "status": "success",
                "message": f"Customer found: {matched_customer['name']}",
                "data": {
                    "customer_id": matched_id,
                    "name": matched_customer['name'],
                    "segment": matched_customer['segment'],
                    "lifetime_value": matched_customer['lifetime_value'],
                    "account_status": matched_customer['account_status'],
                    "voice_response": f"I found {matched_customer['name']}, {matched_customer['segment']} customer with lifetime value of ${matched_customer['lifetime_value']:,}",
                    "quick_actions": [
                        "View full profile",
                        "Check purchase history",
                        "See recent interactions",
                        "Get recommendations"
                    ]
                }
            }
        else:
            return {
                "status": "not_found",
                "message": "Customer not found",
                "data": {
                    "search_term": search_term,
                    "voice_response": "I couldn't find that customer. Please try another search term.",
                    "suggestions": ["Try searching by phone number", "Use partial name match", "Check email address"]
                }
            }

    def _get_customer_360(self, params):
        """Get complete customer 360 view"""
        customer_id = params.get('customer_id', 'CUST-001')
        
        if customer_id not in self.customers:
            return {
                "status": "error",
                "message": "Customer not found",
                "data": {},
                "errors": ["Invalid customer ID"]
            }
        
        customer = self.customers[customer_id]
        
        # Calculate metrics
        avg_satisfaction = sum(i.get('satisfaction', 0) for i in customer['interactions'] if 'satisfaction' in i) / max(1, len([i for i in customer['interactions'] if 'satisfaction' in i]))
        days_since_last_purchase = (datetime.now() - datetime.strptime(customer['purchase_history'][0]['date'], "%Y-%m-%d")).days if customer['purchase_history'] else 999
        
        return {
            "status": "success",
            "message": f"Complete 360 view for {customer['name']}",
            "data": {
                "profile": {
                    "customer_id": customer_id,
                    "name": customer['name'],
                    "contact": {
                        "phone": customer['phone'],
                        "email": customer['email'],
                        "preferred_channel": customer['preferred_channel']
                    },
                    "segment": customer['segment'],
                    "lifetime_value": customer['lifetime_value'],
                    "account_status": customer['account_status']
                },
                "metrics": {
                    "total_purchases": len(customer['purchase_history']),
                    "avg_order_value": sum(p['amount'] for p in customer['purchase_history']) / max(1, len(customer['purchase_history'])),
                    "days_since_last_purchase": days_since_last_purchase,
                    "total_interactions": len(customer['interactions']),
                    "avg_satisfaction": round(avg_satisfaction, 1)
                },
                "preferences": customer['preferences'],
                "voice_summary": f"{customer['name']} is a {customer['segment']} customer with {len(customer['purchase_history'])} purchases totaling ${customer['lifetime_value']:,}. Last purchase was {days_since_last_purchase} days ago."
            }
        }

    def _get_purchase_history(self, params):
        """Get customer purchase history"""
        customer_id = params.get('customer_id', 'CUST-001')
        limit = params.get('limit', 10)
        
        if customer_id not in self.customers:
            return {
                "status": "error",
                "message": "Customer not found",
                "data": {},
                "errors": ["Invalid customer ID"]
            }
        
        customer = self.customers[customer_id]
        history = customer['purchase_history'][:limit]
        
        total_spent = sum(p['amount'] for p in history)
        
        voice_summary = f"{customer['name']} has made {len(history)} purchases totaling ${total_spent:,}. "
        if history:
            voice_summary += f"Most recent purchase was {history[0]['product']} for ${history[0]['amount']}."
        
        return {
            "status": "success",
            "message": f"Purchase history for {customer['name']}",
            "data": {
                "customer_name": customer['name'],
                "purchase_history": history,
                "total_purchases": len(history),
                "total_spent": total_spent,
                "avg_order_value": total_spent / max(1, len(history)),
                "voice_summary": voice_summary
            }
        }

    def _get_interaction_history(self, params):
        """Get customer interaction history"""
        customer_id = params.get('customer_id', 'CUST-001')
        
        if customer_id not in self.customers:
            return {
                "status": "error",
                "message": "Customer not found",
                "data": {},
                "errors": ["Invalid customer ID"]
            }
        
        customer = self.customers[customer_id]
        interactions = customer['interactions']
        
        # Analyze interaction patterns
        interaction_types = {}
        for interaction in interactions:
            int_type = interaction['type']
            interaction_types[int_type] = interaction_types.get(int_type, 0) + 1
        
        most_common = max(interaction_types.items(), key=lambda x: x[1])[0] if interaction_types else "None"
        
        return {
            "status": "success",
            "message": f"Interaction history for {customer['name']}",
            "data": {
                "customer_name": customer['name'],
                "interactions": interactions,
                "total_interactions": len(interactions),
                "interaction_breakdown": interaction_types,
                "most_common_channel": most_common,
                "last_interaction": interactions[0] if interactions else None,
                "voice_summary": f"{customer['name']} has had {len(interactions)} interactions, mostly through {most_common}."
            }
        }

    def _generate_recommendations(self, params):
        """Generate personalized product recommendations"""
        customer_id = params.get('customer_id', 'CUST-001')
        
        if customer_id not in self.customers:
            return {
                "status": "error",
                "message": "Customer not found",
                "data": {},
                "errors": ["Invalid customer ID"]
            }
        
        customer = self.customers[customer_id]
        
        # Generate recommendations based on customer profile
        recommendations = []
        
        # Based on segment
        if customer['segment'] == 'Premium':
            recommendations.append({
                "product": "VIP Support Package",
                "reason": "Premium customer benefit",
                "likelihood": 85,
                "potential_value": 499
            })
            recommendations.append({
                "product": "Exclusive Product Preview",
                "reason": "Early access for premium members",
                "likelihood": 70,
                "potential_value": 999
            })
        
        # Based on interests
        for interest in customer['preferences']['interests']:
            if interest == "Smart Home":
                recommendations.append({
                    "product": "Smart Security System",
                    "reason": f"Matches interest in {interest}",
                    "likelihood": 75,
                    "potential_value": 799
                })
            elif interest == "Entertainment":
                recommendations.append({
                    "product": "Premium Streaming Bundle",
                    "reason": f"Matches interest in {interest}",
                    "likelihood": 65,
                    "potential_value": 299
                })
        
        # Cross-sell based on history
        if any('Bundle' in p['product'] for p in customer['purchase_history']):
            recommendations.append({
                "product": "Extended Warranty",
                "reason": "Protect your bundle purchase",
                "likelihood": 60,
                "potential_value": 199
            })
        
        voice_summary = f"I recommend {len(recommendations)} products for {customer['name']}. "
        if recommendations:
            voice_summary += f"Top recommendation is {recommendations[0]['product']} with {recommendations[0]['likelihood']}% likelihood to purchase."
        
        return {
            "status": "success",
            "message": f"Recommendations generated for {customer['name']}",
            "data": {
                "customer_name": customer['name'],
                "segment": customer['segment'],
                "recommendations": recommendations,
                "total_potential_value": sum(r['potential_value'] for r in recommendations),
                "voice_summary": voice_summary
            }
        }

    def _update_interaction(self, params):
        """Update customer interaction log via voice"""
        customer_id = params.get('customer_id', 'CUST-001')
        interaction_type = params.get('type', 'Voice Call')
        notes = params.get('notes', '')
        satisfaction = params.get('satisfaction')
        
        if customer_id not in self.customers:
            return {
                "status": "error",
                "message": "Customer not found",
                "data": {},
                "errors": ["Invalid customer ID"]
            }
        
        # Create new interaction record
        new_interaction = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M"),
            "type": interaction_type,
            "notes": notes,
            "agent": "Voice Agent"
        }
        
        if satisfaction:
            new_interaction["satisfaction"] = satisfaction
        
        # Add to customer record (simulated)
        customer = self.customers[customer_id]
        customer['interactions'].insert(0, new_interaction)
        
        return {
            "status": "success",
            "message": "Interaction logged successfully",
            "data": {
                "customer_name": customer['name'],
                "interaction": new_interaction,
                "voice_confirmation": f"Interaction logged for {customer['name']}. {interaction_type} recorded with notes.",
                "crm_updated": True
            }
        }

    def _get_voice_summary(self, params):
        """Generate voice-friendly customer summary"""
        customer_id = params.get('customer_id', 'CUST-001')
        
        if customer_id not in self.customers:
            return {
                "status": "error",
                "message": "Customer not found",
                "data": {},
                "errors": ["Invalid customer ID"]
            }
        
        customer = self.customers[customer_id]
        
        # Build comprehensive voice summary
        summary_parts = [
            f"{customer['name']} is a {customer['segment']} customer.",
            f"Lifetime value is ${customer['lifetime_value']:,}.",
            f"They prefer {customer['preferred_channel']} communication."
        ]
        
        if customer['purchase_history']:
            last_purchase = customer['purchase_history'][0]
            summary_parts.append(f"Last purchase was {last_purchase['product']} on {last_purchase['date']}.")
        
        if customer['interactions']:
            summary_parts.append(f"Had {len(customer['interactions'])} recent interactions.")
        
        voice_summary = " ".join(summary_parts)
        
        return {
            "status": "success",
            "message": "Voice summary generated",
            "data": {
                "customer_name": customer['name'],
                "voice_summary": voice_summary,
                "key_points": {
                    "segment": customer['segment'],
                    "lifetime_value": customer['lifetime_value'],
                    "preferred_channel": customer['preferred_channel'],
                    "last_contact": customer['interactions'][0]['date'] if customer['interactions'] else "No recent contact"
                }
            }
        }

    def _general_voice_assistance(self, params):
        """Provide general voice CRM assistance"""
        return {
            "status": "success",
            "message": "Voice CRM Assistant ready",
            "data": {
                "voice_greeting": "Hello! I'm your voice-enabled CRM assistant. You can ask me to look up customers, check purchase history, or get recommendations.",
                "available_commands": [
                    "Find customer [name]",
                    "Show purchase history",
                    "Get customer profile",
                    "Generate recommendations",
                    "Add interaction note",
                    "Give me a summary"
                ],
                "tips": [
                    "Say 'Find customer Jennifer' to look up a customer",
                    "Say 'What did they buy?' for purchase history",
                    "Say 'Recommend products' for cross-sell opportunities"
                ]
            }
        }

if __name__ == "__main__":
    agent = Customer360SpeechAgent()
    
    print("Testing Customer 360 Speech Agent...")
    print("\n1. Voice customer lookup:")
    result = agent.perform(voice_input="Find customer Jennifer Williams")
    print(json.dumps(result, indent=2))
    
    print("\n2. Getting customer 360 view:")
    result = agent.perform(action='get_customer_360', customer_id='CUST-001')
    print(json.dumps(result, indent=2))
    
    print("\n3. Generating recommendations:")
    result = agent.perform(action='generate_recommendations', customer_id='CUST-001')
    print(json.dumps(result, indent=2))