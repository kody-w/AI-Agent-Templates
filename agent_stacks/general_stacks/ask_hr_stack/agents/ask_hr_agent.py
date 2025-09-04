from agents.basic_agent import BasicAgent
import json
import random
from datetime import datetime, timedelta


class AskHRAgent(BasicAgent):
    def __init__(self):
        self.name = "AskHR"
        self.metadata = {
            "name": self.name,
            "description": "AI-powered HR assistant that answers employee questions about policies, benefits, time off, and workplace matters. Provides instant, accurate HR guidance while maintaining confidentiality.",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "Employee's HR-related question"
                    },
                    "question_category": {
                        "type": "string",
                        "description": "Optional. Category of the question",
                        "enum": ["benefits", "time_off", "policies", "payroll", "career", "compliance", "workplace", "other"]
                    },
                    "employee_context": {
                        "type": "object",
                        "description": "Optional. Employee information for personalized response",
                        "properties": {
                            "employee_id": {"type": "string"},
                            "department": {"type": "string"},
                            "location": {"type": "string"},
                            "tenure_years": {"type": "number"}
                        }
                    },
                    "confidential": {
                        "type": "boolean",
                        "description": "Optional. Whether this is a confidential inquiry"
                    }
                },
                "required": ["question"]
            }
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        question = kwargs.get('question')
        question_category = kwargs.get('question_category', 'other')
        employee_context = kwargs.get('employee_context', {})
        confidential = kwargs.get('confidential', False)

        try:
            if not question:
                raise ValueError("Question is required")

            # Process HR inquiry
            hr_response = self._process_hr_inquiry(
                question, question_category, employee_context, confidential
            )

            return json.dumps({
                "status": "success",
                "message": "HR inquiry processed successfully",
                "data": hr_response
            })

        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Failed to process HR inquiry: {str(e)}"
            })

    def _process_hr_inquiry(self, question, category, context, confidential):
        """Process and respond to HR inquiry"""
        
        # Simulate response generation
        response = {
            "inquiry_id": f"HR-{random.randint(100000, 999999)}",
            "question": question,
            "category": category or self._detect_category(question),
            "confidentiality_level": "High" if confidential else "Standard",
            
            "answer": {
                "summary": self._generate_answer_summary(category),
                "detailed_response": self._generate_detailed_answer(category),
                "policy_references": [
                    {"policy": "Employee Handbook", "section": "4.2.1", "page": "45"},
                    {"policy": "Benefits Guide", "section": "Health Insurance", "page": "12"}
                ],
                "relevant_forms": [
                    {"form": "Time Off Request", "form_id": "HR-FORM-001", "link": "/forms/time-off"},
                    {"form": "Benefits Change", "form_id": "HR-FORM-007", "link": "/forms/benefits"}
                ]
            },
            
            "personalized_info": self._get_personalized_info(context, category),
            
            "follow_up": {
                "suggested_actions": [
                    "Submit time off request through employee portal",
                    "Review your current benefits elections",
                    "Schedule meeting with HR representative"
                ],
                "deadlines": [
                    {"action": "Benefits enrollment", "deadline": "December 15, 2024"},
                    {"action": "Performance review submission", "deadline": "January 31, 2024"}
                ],
                "reminders_set": ["Annual benefits review", "Vacation balance check"]
            },
            
            "resources": {
                "helpful_links": [
                    {"title": "Employee Self-Service Portal", "url": "/portal"},
                    {"title": "HR Knowledge Base", "url": "/hr/knowledge"},
                    {"title": "Benefits Calculator", "url": "/benefits/calculator"}
                ],
                "contact_options": {
                    "hr_hotline": "1-800-HR-HELP",
                    "email": "askhr@company.com",
                    "chat": "Available 9 AM - 5 PM EST",
                    "in_person": "HR Office - Building A, Floor 3"
                },
                "related_faqs": [
                    "How do I check my vacation balance?",
                    "When is open enrollment?",
                    "How do I update my tax withholdings?"
                ]
            },
            
            "compliance_check": {
                "legal_considerations": random.choice([True, False]),
                "requires_documentation": random.choice([True, False]),
                "manager_approval_needed": category in ["time_off", "career"],
                "hr_review_required": confidential
            },
            
            "analytics": {
                "question_frequency": f"Asked {random.randint(10, 100)} times this month",
                "typical_resolution_time": "Immediate",
                "satisfaction_score": f"{random.randint(85, 98)}%",
                "escalation_rate": f"{random.randint(5, 15)}%"
            }
        }
        
        return response

    def _detect_category(self, question):
        """Detect question category from text"""
        question_lower = question.lower()
        
        if any(word in question_lower for word in ["vacation", "pto", "sick", "leave", "time off"]):
            return "time_off"
        elif any(word in question_lower for word in ["insurance", "401k", "benefits", "health", "dental"]):
            return "benefits"
        elif any(word in question_lower for word in ["pay", "salary", "paycheck", "tax", "w2"]):
            return "payroll"
        elif any(word in question_lower for word in ["policy", "handbook", "rule", "guideline"]):
            return "policies"
        elif any(word in question_lower for word in ["promotion", "career", "development", "training"]):
            return "career"
        else:
            return "other"

    def _generate_answer_summary(self, category):
        """Generate answer summary based on category"""
        summaries = {
            "benefits": "You're eligible for comprehensive health, dental, and vision coverage. Open enrollment begins November 1st.",
            "time_off": "You have 15 days of PTO remaining this year. Submit requests at least 2 weeks in advance through the employee portal.",
            "policies": "Our remote work policy allows up to 3 days per week from home with manager approval.",
            "payroll": "Paychecks are deposited bi-weekly on Fridays. Access pay stubs through the employee portal.",
            "career": "Career development opportunities include tuition reimbursement, mentorship programs, and internal mobility.",
            "compliance": "All employees must complete annual compliance training by December 31st.",
            "workplace": "Our workplace guidelines promote inclusivity, respect, and professional conduct.",
            "other": "I'll help you with your HR question. Let me find the most relevant information for you."
        }
        return summaries.get(category, summaries["other"])

    def _generate_detailed_answer(self, category):
        """Generate detailed answer based on category"""
        return f"""Based on your question about {category}, here's what you need to know:

1. **Current Policy**: Our {category} policy has been recently updated to better serve employees.

2. **Eligibility**: All full-time employees are eligible after 90 days of employment.

3. **Process**: You can initiate requests through the employee self-service portal or by contacting HR directly.

4. **Timeline**: Most requests are processed within 3-5 business days.

5. **Additional Support**: For complex situations, schedule a confidential meeting with your HR representative.

Please refer to the Employee Handbook for complete details, or contact HR if you need personalized assistance."""

    def _get_personalized_info(self, context, category):
        """Get personalized information based on employee context"""
        info = {
            "your_balance": {},
            "your_eligibility": {},
            "your_deadlines": []
        }
        
        if category == "time_off":
            info["your_balance"] = {
                "pto_days": random.randint(5, 20),
                "sick_days": random.randint(3, 10),
                "personal_days": 2,
                "carryover_deadline": "March 31, 2024"
            }
        elif category == "benefits":
            info["your_eligibility"] = {
                "health_insurance": "Active - PPO Plan",
                "dental": "Active - Standard Plan",
                "401k_match": "100% up to 6%",
                "next_enrollment": "November 1, 2024"
            }
        
        tenure = context.get('tenure_years', 1)
        if tenure >= 5:
            info["your_eligibility"]["sabbatical"] = "Eligible after 5 years"
        
        return info


if __name__ == "__main__":
    agent = AskHRAgent()
    
    result = agent.perform(
        question="How much vacation time do I have left and what's the policy for carrying over to next year?",
        question_category="time_off",
        employee_context={
            "employee_id": "EMP-12345",
            "department": "Engineering",
            "location": "New York",
            "tenure_years": 3.5
        },
        confidential=False
    )
    
    print(json.dumps(json.loads(result), indent=2))
