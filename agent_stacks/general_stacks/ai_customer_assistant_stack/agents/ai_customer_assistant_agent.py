from agents.basic_agent import BasicAgent
import json
import random
from datetime import datetime


class AICustomerAssistantAgent(BasicAgent):
    def __init__(self):
        self.name = "AICustomerAssistant"
        self.metadata = {
            "name": self.name,
            "description": "AI-powered customer service assistant that handles inquiries, resolves issues, and provides personalized support across multiple channels with natural language understanding.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_query": {
                        "type": "string",
                        "description": "Customer's question or issue"
                    },
                    "interaction_channel": {
                        "type": "string",
                        "description": "Channel of interaction",
                        "enum": ["chat", "email", "voice", "social_media", "in_app"]
                    },
                    "customer_context": {
                        "type": "object",
                        "description": "Optional. Customer information and history",
                        "properties": {
                            "customer_id": {"type": "string"},
                            "account_type": {"type": "string"},
                            "previous_interactions": {"type": "array"},
                            "sentiment": {"type": "string"}
                        }
                    },
                    "language": {
                        "type": "string",
                        "description": "Optional. Customer's preferred language (default: English)"
                    },
                    "escalation_enabled": {
                        "type": "boolean",
                        "description": "Optional. Allow escalation to human agent if needed"
                    }
                },
                "required": ["customer_query", "interaction_channel"]
            }
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        customer_query = kwargs.get('customer_query')
        interaction_channel = kwargs.get('interaction_channel')
        customer_context = kwargs.get('customer_context', {})
        language = kwargs.get('language', 'English')
        escalation_enabled = kwargs.get('escalation_enabled', True)

        try:
            if not customer_query:
                raise ValueError("Customer query is required")

            # Process customer inquiry
            response = self._handle_customer_inquiry(
                customer_query, interaction_channel, customer_context, 
                language, escalation_enabled
            )

            return json.dumps({
                "status": "success",
                "message": "Customer inquiry processed successfully",
                "data": response
            })

        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Failed to process customer inquiry: {str(e)}"
            })

    def _handle_customer_inquiry(self, query, channel, context, language, escalation_enabled):
        """Process and respond to customer inquiry"""
        
        # Simulate NLP analysis
        intent = random.choice(["order_status", "technical_support", "billing", "product_info", "complaint"])
        sentiment = random.choice(["positive", "neutral", "negative", "frustrated"])
        confidence = round(random.uniform(0.75, 0.99), 2)
        
        response = {
            "query_analysis": {
                "original_query": query,
                "detected_intent": intent,
                "sentiment": sentiment,
                "language": language,
                "confidence_score": confidence,
                "entities_extracted": {
                    "product": "Premium Service",
                    "issue_type": "Access problem",
                    "urgency": "High"
                }
            },
            "response": {
                "message": self._generate_response(intent, sentiment),
                "suggested_actions": [
                    "Check order status",
                    "View troubleshooting guide",
                    "Schedule callback",
                    "Browse FAQ"
                ],
                "relevant_articles": [
                    {"title": "How to track your order", "url": "/help/track-order"},
                    {"title": "Common login issues", "url": "/help/login-issues"},
                    {"title": "Billing FAQ", "url": "/help/billing-faq"}
                ]
            },
            "resolution": {
                "status": random.choice(["resolved", "pending", "escalated"]),
                "resolution_type": random.choice(["automated", "self_service", "agent_assisted"]),
                "time_to_resolve": f"{random.randint(1, 10)} minutes",
                "satisfaction_predicted": f"{random.randint(70, 95)}%"
            },
            "next_steps": {
                "immediate": "Provided solution and resources",
                "follow_up": "Check satisfaction in 24 hours",
                "escalation": {
                    "needed": confidence < 0.8 and escalation_enabled,
                    "reason": "Complex technical issue" if confidence < 0.8 else None,
                    "agent_type": "Technical specialist" if confidence < 0.8 else None
                }
            },
            "interaction_metadata": {
                "channel": channel,
                "session_id": f"SESS-{random.randint(100000, 999999)}",
                "timestamp": datetime.now().isoformat(),
                "ai_model": "CustomerAssistant-v2.1",
                "tokens_used": random.randint(100, 500)
            }
        }
        
        return response

    def _generate_response(self, intent, sentiment):
        """Generate appropriate response based on intent and sentiment"""
        
        responses = {
            "order_status": "I can help you track your order. Your order #12345 is currently in transit and expected to arrive within 2-3 business days. You can track it in real-time using the link I've sent to your email.",
            "technical_support": "I understand you're experiencing technical difficulties. Let me help you resolve this. I've identified the issue as a connection problem. Please try these steps: 1) Restart your device, 2) Clear your cache, 3) Check your internet connection.",
            "billing": "I see you have a question about your billing. Your current balance is $125.00, due on the 15th. Would you like to review your detailed statement or set up a payment?",
            "product_info": "I'd be happy to provide information about our products. Our Premium Service includes unlimited access, priority support, and exclusive features. Would you like to learn more about specific features?",
            "complaint": "I sincerely apologize for the inconvenience you've experienced. Your satisfaction is our priority. I've escalated this issue to our resolution team who will contact you within 2 hours with a solution."
        }
        
        # Adjust tone based on sentiment
        if sentiment == "frustrated" or sentiment == "negative":
            return "I understand your frustration and I'm here to help. " + responses.get(intent, "Let me assist you with your concern.")
        else:
            return responses.get(intent, "I'm here to help with your inquiry.")


if __name__ == "__main__":
    agent = AICustomerAssistantAgent()
    
    result = agent.perform(
        customer_query="I can't access my account and I need to check my order status urgently",
        interaction_channel="chat",
        customer_context={
            "customer_id": "CUST-456",
            "account_type": "Premium",
            "sentiment": "frustrated"
        },
        language="English",
        escalation_enabled=True
    )
    
    print(json.dumps(json.loads(result), indent=2))
