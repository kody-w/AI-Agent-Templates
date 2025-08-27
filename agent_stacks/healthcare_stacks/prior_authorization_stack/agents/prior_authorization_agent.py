import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

from agents.basic_agent import BasicAgent
import json
from datetime import datetime, timedelta
import random

class PriorAuthorizationAgent(BasicAgent):
    def __init__(self):
        self.name = "PriorAuthorizationAgent"
        self.metadata = {
            "name": self.name,
            "description": "Automates prior authorization processes by integrating with EHR systems and payer portals to speed up approvals and reduce manual interactions",
            "parameters": {
                "type": "object",
                "properties": {
                    "patient_id": {
                        "type": "string",
                        "description": "Unique patient identifier"
                    },
                    "procedure_code": {
                        "type": "string",
                        "description": "CPT/HCPCS code for the procedure requiring authorization"
                    },
                    "diagnosis_codes": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "ICD-10 diagnosis codes supporting medical necessity"
                    },
                    "provider_id": {
                        "type": "string",
                        "description": "Provider NPI number"
                    },
                    "insurance_plan": {
                        "type": "string",
                        "description": "Patient's insurance plan identifier"
                    },
                    "urgency": {
                        "type": "string",
                        "enum": ["routine", "urgent", "emergency"],
                        "description": "Urgency level of the authorization request"
                    },
                    "clinical_notes": {
                        "type": "string",
                        "description": "Supporting clinical documentation"
                    },
                    "action": {
                        "type": "string",
                        "enum": ["submit", "check_status", "appeal", "get_requirements"],
                        "description": "Action to perform"
                    }
                },
                "required": ["patient_id", "action"]
            }
        }
        super().__init__(name=self.name, metadata=self.metadata)
    
    def perform(self, **kwargs):
        action = kwargs.get('action', 'submit')
        patient_id = kwargs.get('patient_id')
        
        if action == 'submit':
            return self._submit_authorization(kwargs)
        elif action == 'check_status':
            return self._check_status(patient_id, kwargs.get('authorization_id'))
        elif action == 'appeal':
            return self._appeal_denial(kwargs)
        elif action == 'get_requirements':
            return self._get_requirements(kwargs)
        else:
            return {"status": "error", "message": f"Unknown action: {action}"}
    
    def _submit_authorization(self, params):
        """Submit a new prior authorization request"""
        auth_id = f"PA{random.randint(100000, 999999)}"
        procedure_code = params.get('procedure_code', 'CPT-99213')
        urgency = params.get('urgency', 'routine')
        
        # Simulate different approval scenarios
        approval_scenarios = [
            {
                "status": "approved",
                "determination": "Medical necessity criteria met",
                "approval_code": f"APV{random.randint(10000, 99999)}",
                "valid_from": datetime.now().isoformat(),
                "valid_to": (datetime.now() + timedelta(days=90)).isoformat(),
                "approved_units": 12
            },
            {
                "status": "pending_review",
                "determination": "Additional clinical documentation required",
                "required_documents": ["Recent lab results", "Specialist consultation notes"],
                "expected_decision": (datetime.now() + timedelta(days=3)).isoformat()
            },
            {
                "status": "approved_with_modifications",
                "determination": "Approved for alternative treatment",
                "approval_code": f"APV{random.randint(10000, 99999)}",
                "modifications": "Approved for 6 sessions instead of 12",
                "valid_from": datetime.now().isoformat(),
                "valid_to": (datetime.now() + timedelta(days=60)).isoformat()
            }
        ]
        
        result = random.choice(approval_scenarios)
        
        return {
            "status": "success",
            "message": f"Prior authorization request submitted successfully",
            "data": {
                "authorization_id": auth_id,
                "patient_id": params.get('patient_id'),
                "procedure_code": procedure_code,
                "submission_timestamp": datetime.now().isoformat(),
                "urgency_level": urgency,
                "determination": result,
                "integrated_systems": ["Epic EHR", "Anthem Payer Portal", "Dynamics 365 Health"],
                "processing_time_minutes": random.randint(1, 15)
            }
        }
    
    def _check_status(self, patient_id, auth_id):
        """Check status of existing authorization"""
        if not auth_id:
            auth_id = f"PA{random.randint(100000, 999999)}"
        
        statuses = ["approved", "pending_review", "denied", "expired", "in_progress"]
        current_status = random.choice(statuses)
        
        return {
            "status": "success",
            "message": "Authorization status retrieved",
            "data": {
                "authorization_id": auth_id,
                "patient_id": patient_id,
                "current_status": current_status,
                "last_updated": datetime.now().isoformat(),
                "days_in_process": random.randint(1, 10),
                "reviewer": f"Dr. {random.choice(['Smith', 'Johnson', 'Williams', 'Brown'])}",
                "next_action": "Awaiting medical director review" if current_status == "pending_review" else "None"
            }
        }
    
    def _appeal_denial(self, params):
        """Appeal a denied authorization"""
        appeal_id = f"APL{random.randint(10000, 99999)}"
        
        return {
            "status": "success",
            "message": "Appeal submitted successfully",
            "data": {
                "appeal_id": appeal_id,
                "original_authorization": params.get('authorization_id', f"PA{random.randint(100000, 999999)}"),
                "appeal_reason": params.get('appeal_reason', 'Additional clinical evidence provided'),
                "supporting_documents": ["Updated clinical notes", "Peer-reviewed studies", "Specialist recommendation"],
                "expected_review_date": (datetime.now() + timedelta(days=5)).isoformat(),
                "appeal_level": "Level 1 - Reconsideration",
                "success_probability": f"{random.randint(60, 85)}%"
            }
        }
    
    def _get_requirements(self, params):
        """Get prior authorization requirements for a procedure"""
        procedure_code = params.get('procedure_code', 'CPT-99213')
        
        return {
            "status": "success",
            "message": "Authorization requirements retrieved",
            "data": {
                "procedure_code": procedure_code,
                "requires_prior_auth": True,
                "medical_necessity_criteria": [
                    "Documented failure of conservative treatment",
                    "Functional impairment affecting daily activities",
                    "Supporting imaging or diagnostic test results"
                ],
                "required_documentation": [
                    "Clinical notes from last 3 visits",
                    "Relevant diagnostic test results",
                    "Treatment history and outcomes"
                ],
                "typical_approval_time": "3-5 business days",
                "auto_approval_eligible": random.choice([True, False]),
                "payer_specific_requirements": {
                    "pre_certification_needed": True,
                    "quantity_limits": "12 sessions per year",
                    "network_restrictions": "In-network providers only"
                }
            }
        }

if __name__ == "__main__":
    agent = PriorAuthorizationAgent()
    
    # Test submission
    result = agent.perform(
        action="submit",
        patient_id="PT123456",
        procedure_code="CPT-97110",
        diagnosis_codes=["M25.511", "M79.3"],
        provider_id="1234567890",
        insurance_plan="BCBS-PPO-GOLD",
        urgency="urgent",
        clinical_notes="Patient presents with chronic knee pain limiting mobility..."
    )
    print(json.dumps(result, indent=2))