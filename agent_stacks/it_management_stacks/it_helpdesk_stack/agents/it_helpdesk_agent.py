import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))

from agents.basic_agent import BasicAgent
import json
import random
from datetime import datetime, timedelta

class ITHelpdeskAgent(BasicAgent):
    def __init__(self):
        metadata = {
            "name": "IT Helpdesk Agent",
            "description": "Empowers employees to resolve IT and hardware issues themselves",
            "version": "1.0.0",
            "author": "Microsoft AI Agent Templates",
            "category": "B2E IT Management"
        }
        super().__init__("ITHelpdeskAgent", metadata)
        
        # Common IT issues and solutions
        self.knowledge_base = {
            "password_reset": {
                "category": "Account",
                "steps": [
                    "Go to https://passwordreset.company.com",
                    "Enter your employee email",
                    "Click 'Send Reset Link'",
                    "Check your alternate email for the reset link",
                    "Create a new password following the requirements"
                ],
                "estimated_time": "5 minutes",
                "self_service": True
            },
            "vpn_connection": {
                "category": "Network",
                "steps": [
                    "Open VPN client",
                    "Enter server: vpn.company.com",
                    "Use your network credentials",
                    "Select 'Company Network' profile",
                    "Click Connect"
                ],
                "estimated_time": "2 minutes",
                "self_service": True
            },
            "printer_not_working": {
                "category": "Hardware",
                "steps": [
                    "Check printer is powered on",
                    "Verify network/USB connection",
                    "Clear print queue",
                    "Restart print spooler service",
                    "Reinstall printer drivers if needed"
                ],
                "estimated_time": "10 minutes",
                "self_service": True
            },
            "software_installation": {
                "category": "Software",
                "steps": [
                    "Open Software Center",
                    "Search for required application",
                    "Click 'Install'",
                    "Wait for installation to complete",
                    "Restart if prompted"
                ],
                "estimated_time": "15 minutes",
                "self_service": True
            },
            "email_not_syncing": {
                "category": "Email",
                "steps": [
                    "Check internet connection",
                    "Verify email settings",
                    "Clear email cache",
                    "Remove and re-add account",
                    "Check server status"
                ],
                "estimated_time": "10 minutes",
                "self_service": True
            }
        }
        
        # Ticket system
        self.tickets = {}
        self.ticket_counter = 1000

    def perform(self, **kwargs):
        """
        Main method to handle IT helpdesk requests
        """
        action = kwargs.get('action', 'diagnose_issue')
        
        try:
            if action == 'diagnose_issue':
                return self._diagnose_issue(kwargs)
            elif action == 'get_solution':
                return self._get_solution(kwargs)
            elif action == 'create_ticket':
                return self._create_ticket(kwargs)
            elif action == 'check_ticket_status':
                return self._check_ticket_status(kwargs)
            elif action == 'get_hardware_info':
                return self._get_hardware_info(kwargs)
            elif action == 'system_health_check':
                return self._system_health_check(kwargs)
            elif action == 'request_equipment':
                return self._request_equipment(kwargs)
            else:
                return self._general_it_support(kwargs)
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error processing IT support request: {str(e)}",
                "data": {},
                "errors": [str(e)]
            }

    def _diagnose_issue(self, params):
        """Diagnose IT issue based on symptoms"""
        symptoms = params.get('symptoms', '')
        category = params.get('category', '')
        
        if not symptoms:
            return {
                "status": "error",
                "message": "Please describe the issue",
                "data": {},
                "errors": ["No symptoms provided"]
            }
        
        # Analyze symptoms
        symptoms_lower = symptoms.lower()
        possible_issues = []
        
        # Match against knowledge base
        for issue_key, issue_data in self.knowledge_base.items():
            issue_keywords = issue_key.replace('_', ' ').split()
            if any(keyword in symptoms_lower for keyword in issue_keywords):
                possible_issues.append({
                    "issue": issue_key,
                    "category": issue_data['category'],
                    "confidence": random.randint(70, 95),
                    "self_service": issue_data['self_service']
                })
        
        if not possible_issues:
            # Generic diagnosis
            possible_issues.append({
                "issue": "general_support",
                "category": "General",
                "confidence": 50,
                "self_service": False
            })
        
        # Sort by confidence
        possible_issues.sort(key=lambda x: x['confidence'], reverse=True)
        
        return {
            "status": "success",
            "message": "Issue diagnosis complete",
            "data": {
                "symptoms": symptoms,
                "possible_issues": possible_issues,
                "primary_diagnosis": possible_issues[0],
                "recommendation": "Try self-service solution" if possible_issues[0]['self_service'] else "Create support ticket"
            }
        }

    def _get_solution(self, params):
        """Get solution for specific IT issue"""
        issue_type = params.get('issue_type', '')
        
        if issue_type in self.knowledge_base:
            solution = self.knowledge_base[issue_type]
            
            return {
                "status": "success",
                "message": f"Solution found for {issue_type.replace('_', ' ')}",
                "data": {
                    "issue": issue_type,
                    "category": solution['category'],
                    "solution_steps": solution['steps'],
                    "estimated_time": solution['estimated_time'],
                    "self_service_available": solution['self_service'],
                    "additional_resources": {
                        "kb_article": f"https://kb.company.com/{issue_type}",
                        "video_tutorial": f"https://help.company.com/videos/{issue_type}"
                    }
                }
            }
        else:
            # Provide general troubleshooting steps
            return {
                "status": "success",
                "message": "General troubleshooting steps",
                "data": {
                    "general_steps": [
                        "Restart your computer",
                        "Check all cable connections",
                        "Update your software",
                        "Clear cache and temporary files",
                        "Run system diagnostics"
                    ],
                    "escalation": "If issue persists, create a support ticket"
                }
            }

    def _create_ticket(self, params):
        """Create IT support ticket"""
        issue_description = params.get('description', '')
        priority = params.get('priority', 'Medium')
        user_id = params.get('user_id', 'EMP001')
        category = params.get('category', 'General')
        
        if not issue_description:
            return {
                "status": "error",
                "message": "Issue description is required",
                "data": {},
                "errors": ["Missing issue description"]
            }
        
        # Generate ticket
        ticket_id = f"INC{self.ticket_counter:06d}"
        self.ticket_counter += 1
        
        # Estimate resolution time based on priority
        resolution_times = {
            "Critical": "2 hours",
            "High": "4 hours",
            "Medium": "1 business day",
            "Low": "3 business days"
        }
        
        ticket = {
            "ticket_id": ticket_id,
            "description": issue_description,
            "category": category,
            "priority": priority,
            "status": "Open",
            "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "estimated_resolution": resolution_times.get(priority, "2 business days"),
            "assigned_to": "IT Support Team",
            "user_id": user_id
        }
        
        self.tickets[ticket_id] = ticket
        
        return {
            "status": "success",
            "message": f"Support ticket {ticket_id} created",
            "data": {
                "ticket": ticket,
                "next_steps": [
                    "You will receive email confirmation",
                    "IT team will contact you within SLA",
                    "Track status in IT portal"
                ],
                "self_help_url": f"https://it.company.com/ticket/{ticket_id}"
            }
        }

    def _check_ticket_status(self, params):
        """Check status of support ticket"""
        ticket_id = params.get('ticket_id')
        
        if not ticket_id:
            # Return all open tickets for user
            user_id = params.get('user_id', 'EMP001')
            user_tickets = {
                tid: ticket for tid, ticket in self.tickets.items()
                if ticket['user_id'] == user_id
            }
            
            return {
                "status": "success",
                "message": f"Found {len(user_tickets)} tickets",
                "data": {
                    "tickets": user_tickets,
                    "summary": {
                        "open": len([t for t in user_tickets.values() if t['status'] == 'Open']),
                        "in_progress": len([t for t in user_tickets.values() if t['status'] == 'In Progress']),
                        "resolved": len([t for t in user_tickets.values() if t['status'] == 'Resolved'])
                    }
                }
            }
        
        if ticket_id in self.tickets:
            ticket = self.tickets[ticket_id]
            
            # Simulate status updates
            created_time = datetime.strptime(ticket['created_date'], "%Y-%m-%d %H:%M:%S")
            time_elapsed = datetime.now() - created_time
            
            if time_elapsed.total_seconds() > 3600:  # More than 1 hour
                ticket['status'] = "In Progress"
            
            return {
                "status": "success",
                "message": f"Ticket {ticket_id} status",
                "data": {
                    "ticket": ticket,
                    "updates": [
                        {"timestamp": ticket['created_date'], "message": "Ticket created"},
                        {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "message": "Status checked"}
                    ]
                }
            }
        else:
            return {
                "status": "error",
                "message": "Ticket not found",
                "data": {},
                "errors": [f"Ticket {ticket_id} does not exist"]
            }

    def _get_hardware_info(self, params):
        """Get hardware information and recommendations"""
        device_type = params.get('device_type', 'laptop')
        
        # Simulated hardware catalog
        hardware_catalog = {
            "laptop": {
                "standard": {"model": "Dell Latitude 5420", "specs": "i5, 16GB RAM, 512GB SSD", "price": 1200},
                "developer": {"model": "MacBook Pro 14", "specs": "M3 Pro, 32GB RAM, 1TB SSD", "price": 2499},
                "executive": {"model": "Surface Laptop Studio", "specs": "i7, 32GB RAM, 1TB SSD", "price": 2799}
            },
            "monitor": {
                "standard": {"model": "Dell 24\" FHD", "specs": "1920x1080, 60Hz", "price": 199},
                "premium": {"model": "LG 27\" 4K", "specs": "3840x2160, 60Hz", "price": 399}
            },
            "accessories": {
                "keyboard": {"model": "Logitech MX Keys", "price": 99},
                "mouse": {"model": "Logitech MX Master 3", "price": 79},
                "headset": {"model": "Jabra Evolve2 65", "price": 249}
            }
        }
        
        if device_type in hardware_catalog:
            return {
                "status": "success",
                "message": f"Hardware options for {device_type}",
                "data": {
                    "device_type": device_type,
                    "available_options": hardware_catalog[device_type],
                    "ordering_process": [
                        "Select hardware option",
                        "Get manager approval",
                        "Submit purchase request",
                        "IT will configure and deliver"
                    ],
                    "delivery_time": "5-7 business days"
                }
            }
        else:
            return {
                "status": "success",
                "message": "Hardware catalog",
                "data": {
                    "available_categories": list(hardware_catalog.keys()),
                    "request_custom": "For special requirements, create a ticket"
                }
            }

    def _system_health_check(self, params):
        """Perform system health check"""
        device_id = params.get('device_id', 'DEVICE001')
        
        # Simulated health metrics
        health_metrics = {
            "cpu_usage": random.randint(20, 80),
            "memory_usage": random.randint(40, 90),
            "disk_usage": random.randint(30, 85),
            "network_latency": random.randint(10, 100),
            "uptime_days": random.randint(1, 30),
            "pending_updates": random.randint(0, 10),
            "security_status": "Protected" if random.random() > 0.2 else "Action Required"
        }
        
        # Generate recommendations
        recommendations = []
        
        if health_metrics['cpu_usage'] > 70:
            recommendations.append("High CPU usage detected. Consider closing unused applications.")
        
        if health_metrics['memory_usage'] > 80:
            recommendations.append("High memory usage. Restart may improve performance.")
        
        if health_metrics['disk_usage'] > 75:
            recommendations.append("Disk space running low. Clean up temporary files.")
        
        if health_metrics['pending_updates'] > 5:
            recommendations.append(f"{health_metrics['pending_updates']} updates pending. Schedule installation.")
        
        overall_health = "Good" if len(recommendations) <= 1 else "Needs Attention" if len(recommendations) <= 3 else "Critical"
        
        return {
            "status": "success",
            "message": "System health check complete",
            "data": {
                "device_id": device_id,
                "health_metrics": health_metrics,
                "overall_health": overall_health,
                "recommendations": recommendations,
                "next_scheduled_maintenance": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
            }
        }

    def _request_equipment(self, params):
        """Request new equipment or replacement"""
        equipment_type = params.get('equipment_type')
        reason = params.get('reason', 'Replacement')
        urgency = params.get('urgency', 'Standard')
        
        if not equipment_type:
            return {
                "status": "error",
                "message": "Equipment type is required",
                "data": {},
                "errors": ["Specify equipment type"]
            }
        
        # Generate request
        request_id = f"EQR{self.ticket_counter:06d}"
        self.ticket_counter += 1
        
        approval_required = True if equipment_type in ['laptop', 'desktop'] else False
        
        return {
            "status": "success",
            "message": "Equipment request submitted",
            "data": {
                "request_id": request_id,
                "equipment_type": equipment_type,
                "reason": reason,
                "urgency": urgency,
                "status": "Pending Approval" if approval_required else "Processing",
                "approval_required": approval_required,
                "estimated_delivery": "3-5 business days" if urgency == "Urgent" else "7-10 business days",
                "next_steps": [
                    "Manager approval required" if approval_required else "Request processing",
                    "IT will contact you for specifications",
                    "Delivery notification will be sent"
                ]
            }
        }

    def _general_it_support(self, params):
        """Provide general IT support information"""
        return {
            "status": "success",
            "message": "IT Helpdesk ready to assist",
            "data": {
                "greeting": "Welcome to IT Helpdesk! I can help you resolve technical issues, request equipment, and check system health.",
                "available_services": [
                    "Diagnose technical issues",
                    "Get step-by-step solutions",
                    "Create support tickets",
                    "Check ticket status",
                    "Request new equipment",
                    "System health check",
                    "Hardware information"
                ],
                "self_service_portal": "https://it.company.com",
                "emergency_hotline": "x5555",
                "business_hours": "24/7 automated support, Live support Mon-Fri 8AM-6PM"
            }
        }

if __name__ == "__main__":
    agent = ITHelpdeskAgent()
    
    print("Testing IT Helpdesk Agent...")
    print("\n1. Diagnosing issue:")
    result = agent.perform(action='diagnose_issue', symptoms='cannot connect to VPN from home')
    print(json.dumps(result, indent=2))
    
    print("\n2. Getting solution:")
    result = agent.perform(action='get_solution', issue_type='vpn_connection')
    print(json.dumps(result, indent=2))
    
    print("\n3. System health check:")
    result = agent.perform(action='system_health_check')
    print(json.dumps(result, indent=2))