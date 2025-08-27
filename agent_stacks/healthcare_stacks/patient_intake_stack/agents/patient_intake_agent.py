import json
from datetime import datetime, timedelta
import random
import sys
import os

# Add parent directory to path to import BasicAgent
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))
from agents.basic_agent import BasicAgent

class PatientIntakeSchedulingAgent(BasicAgent):
    """
    Automates patient intake, appointment coordination, and reminders to reduce no-shows.
    Integrates with Epic, Cerner, D365 CRM, and Salesforce Health Cloud.
    """
    
    def __init__(self):
        metadata = {
            "name": "Patient Intake & Scheduling Agent",
            "description": "Automates intake, appointment coordination, and reminders to reduce no-shows",
            "version": "1.0.0",
            "category": "healthcare",
            "lob_systems": ["Epic", "Cerner", "D365 CRM", "Salesforce Health Cloud"],
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["schedule_appointment", "patient_intake", "send_reminder", "check_availability", "update_record"],
                        "description": "The action to perform"
                    },
                    "patient_data": {
                        "type": "object",
                        "properties": {
                            "first_name": {"type": "string"},
                            "last_name": {"type": "string"},
                            "dob": {"type": "string", "format": "date"},
                            "phone": {"type": "string"},
                            "email": {"type": "string", "format": "email"},
                            "insurance_provider": {"type": "string"},
                            "reason_for_visit": {"type": "string"}
                        }
                    },
                    "appointment_details": {
                        "type": "object",
                        "properties": {
                            "preferred_date": {"type": "string", "format": "date"},
                            "preferred_time": {"type": "string"},
                            "provider": {"type": "string"},
                            "department": {"type": "string"},
                            "visit_type": {"type": "string"}
                        }
                    }
                },
                "required": ["action"]
            }
        }
        super().__init__("PatientIntakeSchedulingAgent", metadata)
    
    def perform(self, **kwargs):
        action = kwargs.get('action')
        
        try:
            if action == 'schedule_appointment':
                return self._schedule_appointment(kwargs)
            elif action == 'patient_intake':
                return self._patient_intake(kwargs)
            elif action == 'send_reminder':
                return self._send_reminder(kwargs)
            elif action == 'check_availability':
                return self._check_availability(kwargs)
            elif action == 'update_record':
                return self._update_record(kwargs)
            else:
                return {
                    "status": "error",
                    "message": f"Unknown action: {action}"
                }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    def _schedule_appointment(self, params):
        patient_data = params.get('patient_data', {})
        appointment_details = params.get('appointment_details', {})
        
        # Simulate appointment scheduling
        appointment_id = f"APT-{random.randint(100000, 999999)}"
        
        # Generate appointment time slot
        preferred_date = appointment_details.get('preferred_date', datetime.now().strftime('%Y-%m-%d'))
        preferred_time = appointment_details.get('preferred_time', '14:00')
        
        return {
            "status": "success",
            "message": "Appointment scheduled successfully",
            "data": {
                "appointment_id": appointment_id,
                "patient_name": f"{patient_data.get('first_name', 'John')} {patient_data.get('last_name', 'Doe')}",
                "date": preferred_date,
                "time": preferred_time,
                "provider": appointment_details.get('provider', 'Dr. Sarah Johnson'),
                "department": appointment_details.get('department', 'Primary Care'),
                "location": "Medical Center - Building A, Suite 200",
                "confirmation_sent": True,
                "ehr_updated": "Epic",
                "crm_updated": "Salesforce Health Cloud"
            }
        }
    
    def _patient_intake(self, params):
        patient_data = params.get('patient_data', {})
        
        # Simulate patient intake process
        patient_id = f"PAT-{random.randint(100000, 999999)}"
        
        intake_forms = [
            "Medical History",
            "Insurance Verification",
            "HIPAA Consent",
            "Patient Demographics",
            "Emergency Contacts"
        ]
        
        return {
            "status": "success",
            "message": "Patient intake completed",
            "data": {
                "patient_id": patient_id,
                "intake_status": "Complete",
                "forms_completed": intake_forms,
                "insurance_verified": True,
                "eligibility_status": "Eligible",
                "copay_amount": "$25.00",
                "systems_updated": ["Epic", "Cerner", "D365 CRM"],
                "next_steps": "Proceed to appointment scheduling"
            }
        }
    
    def _send_reminder(self, params):
        appointment_id = params.get('appointment_id', f"APT-{random.randint(100000, 999999)}")
        
        # Simulate sending appointment reminders
        reminder_channels = ["SMS", "Email", "Phone Call"]
        
        return {
            "status": "success",
            "message": "Appointment reminders sent",
            "data": {
                "appointment_id": appointment_id,
                "reminders_sent": {
                    "sms": {
                        "status": "delivered",
                        "timestamp": datetime.now().isoformat()
                    },
                    "email": {
                        "status": "delivered",
                        "timestamp": datetime.now().isoformat()
                    },
                    "voice_call": {
                        "status": "scheduled",
                        "scheduled_time": (datetime.now() + timedelta(days=1)).isoformat()
                    }
                },
                "confirmation_required": True,
                "response_tracking": "Enabled"
            }
        }
    
    def _check_availability(self, params):
        appointment_details = params.get('appointment_details', {})
        
        # Simulate checking provider availability
        available_slots = []
        base_date = datetime.now()
        
        for i in range(5):
            date = base_date + timedelta(days=i+1)
            for hour in [9, 10, 14, 15, 16]:
                available_slots.append({
                    "date": date.strftime('%Y-%m-%d'),
                    "time": f"{hour:02d}:00",
                    "provider": appointment_details.get('provider', 'Dr. Sarah Johnson'),
                    "duration": "30 minutes"
                })
        
        return {
            "status": "success",
            "message": "Available appointment slots retrieved",
            "data": {
                "available_slots": available_slots[:10],
                "provider": appointment_details.get('provider', 'Dr. Sarah Johnson'),
                "location": "Medical Center",
                "booking_window": "Next 5 business days"
            }
        }
    
    def _update_record(self, params):
        patient_id = params.get('patient_id', f"PAT-{random.randint(100000, 999999)}")
        
        return {
            "status": "success",
            "message": "Patient record updated",
            "data": {
                "patient_id": patient_id,
                "systems_updated": ["Epic", "Cerner", "D365 CRM", "Salesforce Health Cloud"],
                "update_type": "Comprehensive",
                "timestamp": datetime.now().isoformat(),
                "audit_logged": True
            }
        }

if __name__ == "__main__":
    agent = PatientIntakeSchedulingAgent()
    
    # Test appointment scheduling
    result = agent.perform(
        action="schedule_appointment",
        patient_data={
            "first_name": "Jane",
            "last_name": "Smith",
            "phone": "555-0123",
            "email": "jane.smith@email.com"
        },
        appointment_details={
            "preferred_date": "2024-01-25",
            "preferred_time": "10:00",
            "provider": "Dr. Michael Chen",
            "department": "Cardiology"
        }
    )
    
    print(json.dumps(result, indent=2))