from agents.basic_agent import BasicAgent
import json
from datetime import datetime
import random
import re


class SpeechToCRMAgent(BasicAgent):
    def __init__(self):
        self.name = "SpeechToCRM"
        self.metadata = {
            "name": self.name,
            "description": "Converts speech and voice conversations into structured CRM data, automatically creating and updating records from phone calls, meetings, and voice notes.",
            "parameters": {
                "type": "object",
                "properties": {
                    "audio_transcript": {
                        "type": "string",
                        "description": "The transcribed text from speech or voice recording"
                    },
                    "audio_source": {
                        "type": "string",
                        "description": "Source of the audio",
                        "enum": ["phone_call", "meeting", "voice_note", "video_call", "voicemail"]
                    },
                    "speaker_identification": {
                        "type": "object",
                        "description": "Optional. Mapping of speaker IDs to names/roles",
                        "properties": {
                            "speakers": {"type": "array", "items": {"type": "object"}}
                        }
                    },
                    "crm_context": {
                        "type": "object",
                        "description": "Optional. Existing CRM context like account ID, contact ID",
                        "properties": {
                            "account_id": {"type": "string"},
                            "contact_id": {"type": "string"},
                            "opportunity_id": {"type": "string"}
                        }
                    },
                    "extraction_focus": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional. Specific data points to extract",
                        "enum": ["contact_info", "action_items", "requirements", "pain_points", "budget", "timeline", "competitors"]
                    }
                },
                "required": ["audio_transcript", "audio_source"]
            }
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        audio_transcript = kwargs.get('audio_transcript')
        audio_source = kwargs.get('audio_source')
        speaker_identification = kwargs.get('speaker_identification', {})
        crm_context = kwargs.get('crm_context', {})
        extraction_focus = kwargs.get('extraction_focus', ["contact_info", "action_items", "requirements"])

        try:
            # Validate required parameters
            if not audio_transcript or not audio_transcript.strip():
                raise ValueError("Audio transcript is required and cannot be empty")
            
            if not audio_source:
                raise ValueError("Audio source must be specified")

            # Process the transcript and extract CRM data
            crm_data = self._process_transcript_to_crm(
                audio_transcript,
                audio_source,
                speaker_identification,
                crm_context,
                extraction_focus
            )

            return json.dumps({
                "status": "success",
                "message": f"Successfully processed {audio_source} and extracted CRM data",
                "data": crm_data
            })

        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Failed to process speech to CRM: {str(e)}"
            })

    def _process_transcript_to_crm(self, transcript, source, speakers, context, focus):
        """Process transcript and extract structured CRM data"""
        
        # Simulate NLP processing
        crm_record = {
            "metadata": {
                "source": source,
                "processed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "transcript_length": len(transcript.split()),
                "confidence_score": round(random.uniform(0.85, 0.99), 2)
            }
        }

        # Extract contact information
        if "contact_info" in focus:
            crm_record["contact_information"] = self._extract_contact_info(transcript)

        # Extract action items
        if "action_items" in focus:
            crm_record["action_items"] = self._extract_action_items(transcript)

        # Extract requirements
        if "requirements" in focus:
            crm_record["requirements"] = self._extract_requirements(transcript)

        # Extract pain points
        if "pain_points" in focus:
            crm_record["pain_points"] = self._extract_pain_points(transcript)

        # Extract budget information
        if "budget" in focus:
            crm_record["budget_info"] = self._extract_budget_info(transcript)

        # Extract timeline
        if "timeline" in focus:
            crm_record["timeline"] = self._extract_timeline(transcript)

        # Extract competitor mentions
        if "competitors" in focus:
            crm_record["competitors"] = self._extract_competitors(transcript)

        # Generate CRM updates
        crm_record["crm_updates"] = self._generate_crm_updates(transcript, source, context)

        # Add conversation summary
        crm_record["summary"] = self._generate_summary(transcript, source)

        # Add sentiment analysis
        crm_record["sentiment_analysis"] = {
            "overall": random.choice(["Positive", "Neutral", "Mixed"]),
            "score": round(random.uniform(0.6, 0.9), 2),
            "key_emotions": random.sample(["interested", "curious", "concerned", "excited", "satisfied"], 2)
        }

        # Add follow-up recommendations
        crm_record["follow_up"] = self._generate_follow_up_recommendations(transcript, source)

        return crm_record

    def _extract_contact_info(self, transcript):
        """Extract contact information from transcript"""
        # Simulate extraction
        return {
            "name": "John Smith",
            "title": "VP of Operations",
            "company": "TechCorp Industries",
            "email": "john.smith@techcorp.com",
            "phone": "+1-555-0123",
            "location": "San Francisco, CA",
            "linkedin": "linkedin.com/in/johnsmith"
        }

    def _extract_action_items(self, transcript):
        """Extract action items from transcript"""
        return [
            {
                "item": "Send product demo video",
                "owner": "Sales Rep",
                "due_date": "2024-02-05",
                "priority": "High",
                "status": "Pending"
            },
            {
                "item": "Schedule follow-up meeting with technical team",
                "owner": "Sales Rep",
                "due_date": "2024-02-10",
                "priority": "Medium",
                "status": "Pending"
            },
            {
                "item": "Prepare custom pricing proposal",
                "owner": "Sales Manager",
                "due_date": "2024-02-08",
                "priority": "High",
                "status": "Pending"
            }
        ]

    def _extract_requirements(self, transcript):
        """Extract requirements from transcript"""
        return {
            "functional_requirements": [
                "Integration with existing ERP system",
                "Real-time reporting dashboard",
                "Mobile app for field workers",
                "Multi-language support"
            ],
            "technical_requirements": [
                "Cloud-based solution",
                "API access for custom integrations",
                "SSO authentication",
                "99.9% uptime SLA"
            ],
            "business_requirements": [
                "ROI within 12 months",
                "Training for 50+ users",
                "24/7 support coverage",
                "Compliance with ISO 27001"
            ]
        }

    def _extract_pain_points(self, transcript):
        """Extract pain points from transcript"""
        return [
            {
                "issue": "Manual data entry taking too much time",
                "impact": "High",
                "frequency": "Daily",
                "cost_impact": "$50,000/year in lost productivity"
            },
            {
                "issue": "Lack of real-time visibility into operations",
                "impact": "Medium",
                "frequency": "Weekly",
                "cost_impact": "Delayed decision making"
            },
            {
                "issue": "Disconnected systems causing data silos",
                "impact": "High",
                "frequency": "Constant",
                "cost_impact": "Unable to get unified reporting"
            }
        ]

    def _extract_budget_info(self, transcript):
        """Extract budget information from transcript"""
        return {
            "budget_range": "$100,000 - $150,000",
            "budget_cycle": "Annual",
            "approval_process": "CFO and Board approval required",
            "funding_available": "Q2 2024",
            "payment_terms": "Net 30",
            "budget_flexibility": "Medium"
        }

    def _extract_timeline(self, transcript):
        """Extract timeline information from transcript"""
        return {
            "decision_date": "2024-03-01",
            "implementation_start": "2024-04-01",
            "go_live_target": "2024-06-30",
            "phases": [
                {"phase": "Pilot", "duration": "30 days"},
                {"phase": "Rollout", "duration": "60 days"},
                {"phase": "Full deployment", "duration": "90 days"}
            ],
            "urgency": "High",
            "drivers": ["End of fiscal year", "Competitive pressure"]
        }

    def _extract_competitors(self, transcript):
        """Extract competitor mentions from transcript"""
        return [
            {
                "competitor": "CompetitorX",
                "mentioned_features": ["pricing", "support"],
                "sentiment": "Considering",
                "status": "In evaluation"
            },
            {
                "competitor": "CompetitorY",
                "mentioned_features": ["functionality", "integration"],
                "sentiment": "Rejected",
                "reason": "Too complex"
            }
        ]

    def _generate_crm_updates(self, transcript, source, context):
        """Generate CRM update records"""
        updates = []
        
        # Create activity record
        updates.append({
            "type": "activity",
            "action": "create",
            "entity": "activity",
            "data": {
                "type": source,
                "subject": f"{source.replace('_', ' ').title()} with contact",
                "description": f"Automated capture from {source}",
                "duration": random.randint(15, 60),
                "outcome": "Successful",
                "next_steps": "Follow up scheduled"
            }
        })

        # Update opportunity
        if context.get('opportunity_id'):
            updates.append({
                "type": "opportunity",
                "action": "update",
                "entity": "opportunity",
                "entity_id": context['opportunity_id'],
                "data": {
                    "stage": "Qualification",
                    "probability": 60,
                    "next_step": "Technical demo",
                    "close_date": "2024-03-31"
                }
            })

        # Create or update contact
        updates.append({
            "type": "contact",
            "action": "update",
            "entity": "contact",
            "data": {
                "last_contact_date": datetime.now().strftime("%Y-%m-%d"),
                "engagement_score": 85,
                "interest_level": "High",
                "preferred_contact_method": source
            }
        })

        # Create tasks
        updates.append({
            "type": "task",
            "action": "create",
            "entity": "task",
            "data": {
                "subject": "Send follow-up email",
                "due_date": "2024-02-05",
                "priority": "High",
                "assigned_to": "current_user"
            }
        })

        return updates

    def _generate_summary(self, transcript, source):
        """Generate conversation summary"""
        return {
            "executive_summary": f"Productive {source.replace('_', ' ')} discussing product capabilities and implementation timeline. Customer expressed strong interest in our solution with focus on integration capabilities and ROI.",
            "key_topics": [
                "Product demonstration request",
                "Integration requirements",
                "Pricing and budget discussion",
                "Implementation timeline",
                "Support requirements"
            ],
            "customer_stance": "Interested and engaged",
            "next_meeting": "Technical deep dive scheduled for next week",
            "decision_criteria": [
                "Integration capabilities",
                "Total cost of ownership",
                "Implementation timeline",
                "Support quality"
            ]
        }

    def _generate_follow_up_recommendations(self, transcript, source):
        """Generate follow-up recommendations"""
        return {
            "immediate_actions": [
                {
                    "action": "Send thank you email",
                    "timeline": "Within 24 hours",
                    "template": "post_call_followup"
                },
                {
                    "action": "Share requested resources",
                    "timeline": "Within 48 hours",
                    "resources": ["Product demo", "Case studies", "Pricing guide"]
                }
            ],
            "short_term_actions": [
                {
                    "action": "Schedule technical demo",
                    "timeline": "Next week",
                    "participants": ["Technical team", "Solution architect"]
                },
                {
                    "action": "Prepare custom proposal",
                    "timeline": "Within 5 days",
                    "include": ["Custom pricing", "Implementation plan"]
                }
            ],
            "long_term_strategy": {
                "approach": "Consultative selling",
                "focus_areas": ["ROI demonstration", "Integration proof of concept"],
                "stakeholder_mapping": "Identify and engage decision makers",
                "competitive_positioning": "Highlight differentiators vs CompetitorX"
            }
        }


if __name__ == "__main__":
    agent = SpeechToCRMAgent()
    
    # Test with sample transcript
    sample_transcript = """
    Hi, this is John Smith from TechCorp Industries. We're looking for a solution to help us 
    automate our sales processes. Currently, we're spending too much time on manual data entry 
    and our team needs better visibility into the pipeline. We have a budget of around 100-150K 
    for this fiscal year and we'd like to implement something by Q2. Can you send me more 
    information about your integration capabilities with Salesforce?
    """
    
    result = agent.perform(
        audio_transcript=sample_transcript,
        audio_source="phone_call",
        extraction_focus=["contact_info", "action_items", "requirements", "budget", "timeline"]
    )
    
    print(json.dumps(json.loads(result), indent=2))