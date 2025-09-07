import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))

from agents.basic_agent import BasicAgent
import json
import random
from datetime import datetime, timedelta

class AskHRAgent(BasicAgent):
    def __init__(self):
        metadata = {
            "name": "Ask HR Agent",
            "description": "AI Employee HR Agent for Microsoft Teams providing instant HR support",
            "version": "1.0.0",
            "author": "Microsoft AI Agent Templates",
            "category": "B2E Human Resources"
        }
        super().__init__("AskHRAgent", metadata)
        
        # HR Knowledge Base
        self.policies = {
            "vacation": {
                "accrual_rate": "1.25 days per month",
                "max_balance": "30 days",
                "rollover": "Up to 5 days annually",
                "blackout_periods": ["Dec 15 - Jan 5", "End of fiscal quarters"]
            },
            "benefits": {
                "health_insurance": ["PPO Plan", "HMO Plan", "HSA Plan"],
                "dental": "Full coverage with $2000 annual max",
                "vision": "$150 annual allowance",
                "401k": "6% match, immediate vesting",
                "life_insurance": "2x annual salary"
            },
            "remote_work": {
                "eligibility": "After 90 days employment",
                "max_days": "3 days per week",
                "equipment": "$1000 home office stipend",
                "requirements": "Manager approval required"
            },
            "parental_leave": {
                "maternity": "16 weeks paid",
                "paternity": "8 weeks paid",
                "adoption": "12 weeks paid",
                "eligibility": "After 12 months employment"
            }
        }
        
        # Employee data simulation
        self.employee_data = {
            "EMP001": {
                "name": "John Smith",
                "department": "Engineering",
                "vacation_balance": 15.5,
                "hire_date": "2022-03-15",
                "manager": "Sarah Johnson"
            },
            "EMP002": {
                "name": "Emily Chen",
                "department": "Marketing",
                "vacation_balance": 8.25,
                "hire_date": "2023-06-01",
                "manager": "Mike Davis"
            }
        }
        
        # Common HR requests
        self.request_types = [
            "time_off_request",
            "benefits_inquiry",
            "policy_clarification",
            "payroll_question",
            "document_request",
            "training_enrollment"
        ]

    def perform(self, **kwargs):
        """
        Main method to handle HR inquiries and requests
        """
        action = kwargs.get('action', 'general_inquiry')
        
        try:
            if action == 'check_vacation_balance':
                return self._check_vacation_balance(kwargs)
            elif action == 'submit_time_off':
                return self._submit_time_off(kwargs)
            elif action == 'get_benefits_info':
                return self._get_benefits_info(kwargs)
            elif action == 'policy_lookup':
                return self._policy_lookup(kwargs)
            elif action == 'request_document':
                return self._request_document(kwargs)
            elif action == 'get_team_directory':
                return self._get_team_directory(kwargs)
            elif action == 'submit_complaint':
                return self._submit_complaint(kwargs)
            else:
                return self._general_hr_assistance(kwargs)
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error processing HR request: {str(e)}",
                "data": {},
                "errors": [str(e)]
            }

    def _check_vacation_balance(self, params):
        """Check employee vacation balance"""
        employee_id = params.get('employee_id', 'EMP001')
        
        if employee_id in self.employee_data:
            employee = self.employee_data[employee_id]
            
            # Calculate accrual
            hire_date = datetime.strptime(employee['hire_date'], "%Y-%m-%d")
            months_employed = (datetime.now() - hire_date).days // 30
            total_accrued = months_employed * 1.25
            
            return {
                "status": "success",
                "message": f"Vacation balance for {employee['name']}",
                "data": {
                    "current_balance": employee['vacation_balance'],
                    "total_accrued": round(total_accrued, 2),
                    "used_this_year": round(total_accrued - employee['vacation_balance'], 2),
                    "accrual_rate": self.policies['vacation']['accrual_rate'],
                    "max_balance": self.policies['vacation']['max_balance']
                }
            }
        else:
            return {
                "status": "error",
                "message": "Employee not found",
                "data": {},
                "errors": ["Invalid employee ID"]
            }

    def _submit_time_off(self, params):
        """Submit time off request"""
        employee_id = params.get('employee_id', 'EMP001')
        start_date = params.get('start_date')
        end_date = params.get('end_date')
        request_type = params.get('type', 'vacation')
        reason = params.get('reason', '')
        
        if not start_date or not end_date:
            return {
                "status": "error",
                "message": "Start and end dates are required",
                "data": {},
                "errors": ["Missing required dates"]
            }
        
        # Calculate days requested
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        days_requested = (end - start).days + 1
        
        # Check balance
        if employee_id in self.employee_data:
            employee = self.employee_data[employee_id]
            
            if days_requested > employee['vacation_balance']:
                return {
                    "status": "warning",
                    "message": "Insufficient vacation balance",
                    "data": {
                        "days_requested": days_requested,
                        "current_balance": employee['vacation_balance'],
                        "shortfall": days_requested - employee['vacation_balance'],
                        "suggestion": "Consider unpaid leave for additional days"
                    }
                }
            
            # Create request
            request_id = f"REQ-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
            
            return {
                "status": "success",
                "message": "Time off request submitted successfully",
                "data": {
                    "request_id": request_id,
                    "employee": employee['name'],
                    "type": request_type,
                    "start_date": start_date,
                    "end_date": end_date,
                    "days_requested": days_requested,
                    "status": "Pending Manager Approval",
                    "manager_notified": employee['manager'],
                    "teams_notification_sent": True
                }
            }

    def _get_benefits_info(self, params):
        """Get benefits information"""
        benefit_type = params.get('benefit_type')
        
        if benefit_type and benefit_type in self.policies['benefits']:
            return {
                "status": "success",
                "message": f"Benefits information for {benefit_type}",
                "data": {
                    "benefit_type": benefit_type,
                    "details": self.policies['benefits'][benefit_type],
                    "enrollment_period": "Open enrollment: Nov 1-30",
                    "effective_date": "January 1"
                }
            }
        else:
            return {
                "status": "success",
                "message": "Complete benefits package information",
                "data": {
                    "benefits": self.policies['benefits'],
                    "enrollment_period": "Open enrollment: Nov 1-30",
                    "contact": "benefits@company.com for detailed information"
                }
            }

    def _policy_lookup(self, params):
        """Look up company policies"""
        policy_area = params.get('policy_area')
        
        if policy_area and policy_area in self.policies:
            return {
                "status": "success",
                "message": f"Policy information for {policy_area}",
                "data": {
                    "policy_area": policy_area,
                    "details": self.policies[policy_area],
                    "last_updated": "2024-01-01",
                    "full_policy_link": f"https://hr.company.com/policies/{policy_area}"
                }
            }
        else:
            return {
                "status": "success",
                "message": "Available policy areas",
                "data": {
                    "available_policies": list(self.policies.keys()),
                    "policy_portal": "https://hr.company.com/policies",
                    "help_text": "Specify a policy area for detailed information"
                }
            }

    def _request_document(self, params):
        """Request HR documents"""
        document_type = params.get('document_type', 'employment_verification')
        employee_id = params.get('employee_id', 'EMP001')
        
        document_types = [
            "employment_verification",
            "salary_certificate",
            "tax_documents",
            "benefits_summary",
            "performance_review"
        ]
        
        if document_type not in document_types:
            return {
                "status": "error",
                "message": "Invalid document type",
                "data": {
                    "available_types": document_types
                },
                "errors": ["Document type not recognized"]
            }
        
        # Generate request
        request_id = f"DOC-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
        
        return {
            "status": "success",
            "message": "Document request submitted",
            "data": {
                "request_id": request_id,
                "document_type": document_type,
                "processing_time": "2-3 business days",
                "delivery_method": "Secure email to registered address",
                "status": "Processing",
                "teams_notification": "You will be notified when ready"
            }
        }

    def _get_team_directory(self, params):
        """Get team directory information"""
        department = params.get('department')
        
        # Simulated directory
        directory = [
            {"name": "Sarah Johnson", "role": "Engineering Manager", "department": "Engineering", "email": "sarah.j@company.com"},
            {"name": "Mike Davis", "role": "Marketing Director", "department": "Marketing", "email": "mike.d@company.com"},
            {"name": "Lisa Wong", "role": "HR Business Partner", "department": "Human Resources", "email": "lisa.w@company.com"},
            {"name": "Tom Anderson", "role": "Finance Manager", "department": "Finance", "email": "tom.a@company.com"}
        ]
        
        if department:
            filtered = [d for d in directory if d['department'] == department]
            return {
                "status": "success",
                "message": f"Directory for {department}",
                "data": {
                    "department": department,
                    "team_members": filtered,
                    "count": len(filtered)
                }
            }
        else:
            return {
                "status": "success",
                "message": "Company directory",
                "data": {
                    "total_employees": len(directory),
                    "directory": directory,
                    "departments": list(set(d['department'] for d in directory))
                }
            }

    def _submit_complaint(self, params):
        """Submit confidential HR complaint"""
        complaint_type = params.get('type', 'general')
        description = params.get('description', '')
        anonymous = params.get('anonymous', False)
        
        if not description:
            return {
                "status": "error",
                "message": "Description is required",
                "data": {},
                "errors": ["Please provide complaint details"]
            }
        
        # Generate case number
        case_number = f"HR-CASE-{datetime.now().strftime('%Y%m%d')}-{random.randint(10000, 99999)}"
        
        return {
            "status": "success",
            "message": "Complaint submitted successfully",
            "data": {
                "case_number": case_number,
                "type": complaint_type,
                "anonymous": anonymous,
                "status": "Under Review",
                "assigned_to": "HR Investigation Team",
                "expected_response": "Within 48 hours",
                "confidentiality": "All complaints are handled with strict confidentiality"
            }
        }

    def _general_hr_assistance(self, params):
        """Provide general HR assistance"""
        query = params.get('query', '')
        
        return {
            "status": "success",
            "message": "HR Assistant ready to help",
            "data": {
                "greeting": "Hello! I'm your AI HR Assistant. I can help with vacation balances, benefits, policies, time-off requests, and more.",
                "available_services": [
                    "Check vacation balance",
                    "Submit time off request",
                    "Benefits information",
                    "Policy lookups",
                    "Document requests",
                    "Team directory",
                    "Submit confidential complaints"
                ],
                "quick_links": {
                    "HR Portal": "https://hr.company.com",
                    "Benefits": "https://benefits.company.com",
                    "Payroll": "https://payroll.company.com"
                },
                "teams_integration": "Available in Microsoft Teams"
            }
        }

if __name__ == "__main__":
    agent = AskHRAgent()
    
    print("Testing Ask HR Agent...")
    print("\n1. Checking vacation balance:")
    result = agent.perform(action='check_vacation_balance', employee_id='EMP001')
    print(json.dumps(result, indent=2))
    
    print("\n2. Getting benefits info:")
    result = agent.perform(action='get_benefits_info')
    print(json.dumps(result, indent=2))
    
    print("\n3. Submitting time off request:")
    result = agent.perform(
        action='submit_time_off',
        employee_id='EMP001',
        start_date='2024-12-23',
        end_date='2024-12-27',
        type='vacation'
    )
    print(json.dumps(result, indent=2))