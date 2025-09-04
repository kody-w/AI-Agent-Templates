from agents.basic_agent import BasicAgent
import json
from datetime import datetime, timedelta
import random


class SalesCoachAgent(BasicAgent):
    def __init__(self):
        self.name = "SalesCoach"
        self.metadata = {
            "name": self.name,
            "description": "AI-powered sales coaching and training system that provides personalized feedback, role-playing scenarios, and performance improvement recommendations for sales teams.",
            "parameters": {
                "type": "object",
                "properties": {
                    "coaching_type": {
                        "type": "string",
                        "description": "Type of coaching requested",
                        "enum": ["call_review", "role_play", "objection_handling", "pitch_practice", "negotiation", "performance_review"]
                    },
                    "scenario_context": {
                        "type": "object",
                        "description": "Optional. Context for the coaching scenario",
                        "properties": {
                            "industry": {"type": "string"},
                            "product": {"type": "string"},
                            "customer_type": {"type": "string"},
                            "deal_size": {"type": "string"},
                            "sales_stage": {"type": "string"}
                        }
                    },
                    "rep_profile": {
                        "type": "object",
                        "description": "Optional. Sales rep profile for personalized coaching",
                        "properties": {
                            "experience_level": {"type": "string", "enum": ["junior", "intermediate", "senior"]},
                            "strengths": {"type": "array", "items": {"type": "string"}},
                            "improvement_areas": {"type": "array", "items": {"type": "string"}}
                        }
                    },
                    "transcript": {
                        "type": "string",
                        "description": "Optional. Call transcript or conversation for review"
                    },
                    "focus_areas": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional. Specific areas to focus on"
                    }
                },
                "required": ["coaching_type"]
            }
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        coaching_type = kwargs.get('coaching_type')
        scenario_context = kwargs.get('scenario_context', {})
        rep_profile = kwargs.get('rep_profile', {})
        transcript = kwargs.get('transcript', '')
        focus_areas = kwargs.get('focus_areas', [])

        try:
            if not coaching_type:
                raise ValueError("Coaching type is required")

            # Generate coaching session
            coaching_session = self._generate_coaching_session(
                coaching_type, scenario_context, rep_profile, transcript, focus_areas
            )

            return json.dumps({
                "status": "success",
                "message": f"Generated {coaching_type.replace('_', ' ')} coaching session",
                "data": coaching_session
            })

        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Failed to generate coaching session: {str(e)}"
            })

    def _generate_coaching_session(self, coaching_type, context, rep_profile, transcript, focus_areas):
        """Generate personalized coaching session"""
        
        session = {
            "session_id": f"COACH-{random.randint(10000, 99999)}",
            "type": coaching_type,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "duration_estimate": f"{random.randint(15, 45)} minutes"
        }

        # Generate content based on coaching type
        if coaching_type == "call_review":
            session.update(self._generate_call_review(transcript, context))
        elif coaching_type == "role_play":
            session.update(self._generate_role_play(context, rep_profile))
        elif coaching_type == "objection_handling":
            session.update(self._generate_objection_handling(context))
        elif coaching_type == "pitch_practice":
            session.update(self._generate_pitch_practice(context, rep_profile))
        elif coaching_type == "negotiation":
            session.update(self._generate_negotiation_training(context))
        elif coaching_type == "performance_review":
            session.update(self._generate_performance_review(rep_profile))

        # Add personalized recommendations
        session["personalized_recommendations"] = self._generate_recommendations(rep_profile, coaching_type)
        
        # Add learning resources
        session["learning_resources"] = self._generate_learning_resources(coaching_type, focus_areas)
        
        # Add practice exercises
        session["practice_exercises"] = self._generate_practice_exercises(coaching_type)

        return session

    def _generate_call_review(self, transcript, context):
        """Generate call review analysis"""
        return {
            "analysis": {
                "overall_score": random.randint(70, 95),
                "strengths": [
                    "Strong opening and rapport building",
                    "Good use of open-ended questions",
                    "Effective value proposition presentation"
                ],
                "improvements": [
                    "Could probe deeper into customer pain points",
                    "Missed opportunity to discuss implementation timeline",
                    "Should have confirmed next steps more clearly"
                ],
                "talk_ratio": {
                    "rep": "35%",
                    "customer": "65%",
                    "ideal": "30/70",
                    "feedback": "Good balance, customer was engaged"
                }
            },
            "key_moments": [
                {
                    "timestamp": "02:15",
                    "type": "Positive",
                    "moment": "Excellent discovery question about current challenges",
                    "impact": "Customer opened up about critical pain points"
                },
                {
                    "timestamp": "08:43",
                    "type": "Improvement",
                    "moment": "Missed buying signal when customer asked about pricing",
                    "suggestion": "Should have explored budget and decision criteria"
                },
                {
                    "timestamp": "15:20",
                    "type": "Positive",
                    "moment": "Great objection handling on competitive comparison",
                    "impact": "Successfully differentiated our solution"
                }
            ],
            "conversation_flow": {
                "opening": {"score": 85, "feedback": "Strong, but could be more personalized"},
                "discovery": {"score": 75, "feedback": "Good questions, need more depth"},
                "presentation": {"score": 90, "feedback": "Clear and customer-focused"},
                "objection_handling": {"score": 88, "feedback": "Confident and well-prepared"},
                "closing": {"score": 70, "feedback": "Needs stronger commitment for next steps"}
            },
            "language_analysis": {
                "positive_phrases": 15,
                "filler_words": 8,
                "confidence_level": "High",
                "clarity_score": 82,
                "enthusiasm_score": 78
            }
        }

    def _generate_role_play(self, context, rep_profile):
        """Generate role-play scenario"""
        return {
            "scenario": {
                "title": "Enterprise Software Sale - Budget Objection",
                "setting": "Virtual meeting with CFO and IT Director",
                "company": "GlobalTech Manufacturing Inc.",
                "participants": {
                    "customer_1": {
                        "name": "Sarah Chen",
                        "role": "CFO",
                        "personality": "Analytical, cost-conscious, ROI-focused",
                        "concerns": ["Budget constraints", "ROI timeline", "Integration costs"]
                    },
                    "customer_2": {
                        "name": "Michael Torres",
                        "role": "IT Director",
                        "personality": "Technical, detail-oriented, risk-averse",
                        "concerns": ["Technical compatibility", "Implementation complexity", "Security"]
                    }
                },
                "background": "Company evaluating digital transformation solutions. Current systems are outdated but functional. Budget approved but tight.",
                "your_objective": "Secure commitment for pilot program within approved budget",
                "key_information": {
                    "budget": "$150,000 annually",
                    "timeline": "Decision needed within 30 days",
                    "competitors": "Currently evaluating 2 other vendors",
                    "pain_points": ["Manual processes", "Data silos", "Reporting delays"]
                }
            },
            "conversation_starters": [
                "Thank you both for taking the time today. I understand you're evaluating solutions for your digital transformation initiative.",
                "I've reviewed your RFP and I'm excited to show how we can address your specific challenges.",
                "Before we dive in, what's the most critical issue you're hoping to solve?"
            ],
            "anticipated_objections": [
                {
                    "objection": "Your solution seems expensive compared to competitors",
                    "suggested_response": "I understand cost is important. Let's look at the total value and ROI. Our clients typically see payback within 8 months...",
                    "key_points": ["TCO comparison", "Hidden costs of alternatives", "ROI timeline"]
                },
                {
                    "objection": "We're concerned about the implementation timeline",
                    "suggested_response": "That's a valid concern. Our phased approach minimizes disruption. We can have your critical processes running in 30 days...",
                    "key_points": ["Phased rollout", "Dedicated support", "Success stories"]
                }
            ],
            "success_criteria": [
                "Uncover at least 3 specific pain points",
                "Demonstrate clear ROI within 12 months",
                "Address both technical and financial concerns",
                "Secure agreement for pilot program",
                "Schedule follow-up with broader team"
            ]
        }

    def _generate_objection_handling(self, context):
        """Generate objection handling training"""
        return {
            "common_objections": [
                {
                    "objection": "It's too expensive",
                    "type": "Price",
                    "frequency": "Very High",
                    "responses": {
                        "acknowledge": "I understand price is an important factor in your decision...",
                        "reframe": "Let's look at this as an investment rather than a cost. What's the cost of not solving this problem?",
                        "value_stack": "When you consider [benefit 1], [benefit 2], and [benefit 3], the ROI becomes clear...",
                        "comparison": "Compared to the cost of [current pain/alternative], our solution actually saves you..."
                    },
                    "tips": [
                        "Never immediately drop price",
                        "Focus on value and ROI",
                        "Use customer's own numbers when possible",
                        "Break down cost per user/unit/month"
                    ]
                },
                {
                    "objection": "We need to think about it",
                    "type": "Stall",
                    "frequency": "High",
                    "responses": {
                        "probe": "I appreciate you want to make the right decision. What specifically would you like to think about?",
                        "urgency": "I understand. While you're considering, remember that [time-sensitive benefit/offer]...",
                        "support": "What information can I provide to help you make the best decision?",
                        "timeline": "When do you think you'll be ready to move forward? I can follow up then."
                    },
                    "tips": [
                        "Identify the real concern behind the stall",
                        "Create urgency without being pushy",
                        "Offer to address specific concerns",
                        "Set a clear follow-up timeline"
                    ]
                },
                {
                    "objection": "We're happy with our current solution",
                    "type": "Status Quo",
                    "frequency": "Medium",
                    "responses": {
                        "curiosity": "That's great! What do you like most about it? What would make it even better?",
                        "change": "I understand. What prompted you to take this meeting if everything is working well?",
                        "future": "Markets change quickly. How is your current solution preparing you for [future trend]?",
                        "complement": "Our solution actually works alongside [current solution] to enhance..."
                    },
                    "tips": [
                        "Don't attack their current solution",
                        "Find gaps or future needs",
                        "Position as enhancement, not replacement",
                        "Focus on missed opportunities"
                    ]
                }
            ],
            "objection_framework": {
                "steps": [
                    "1. Listen completely without interrupting",
                    "2. Acknowledge and empathize",
                    "3. Clarify and probe for real concern",
                    "4. Reframe or provide perspective",
                    "5. Provide proof or evidence",
                    "6. Confirm resolution and move forward"
                ],
                "key_principles": [
                    "Objections are buying signals",
                    "Address emotions before logic",
                    "Use questions to let them solve it",
                    "Have proof points ready"
                ]
            }
        }

    def _generate_pitch_practice(self, context, rep_profile):
        """Generate pitch practice session"""
        return {
            "pitch_structure": {
                "elevator_pitch": {
                    "duration": "30 seconds",
                    "template": "We help [target customer] achieve [desired outcome] by [unique method] resulting in [specific benefit]",
                    "example": "We help enterprise sales teams increase win rates by 35% through AI-powered coaching that provides real-time feedback and personalized training, resulting in $2M+ additional revenue per quarter.",
                    "practice_tips": [
                        "Keep it conversational, not memorized",
                        "Focus on outcomes, not features",
                        "Include a specific metric",
                        "End with a question to engage"
                    ]
                },
                "discovery_pitch": {
                    "duration": "2-3 minutes",
                    "structure": [
                        "Hook: Relevant industry insight or challenge",
                        "Problem: Specific pain points we solve",
                        "Solution: High-level approach",
                        "Proof: Quick success story",
                        "Engagement: Transition to discovery questions"
                    ],
                    "example_opening": "I was just reading that 67% of enterprise sales teams miss quota. In talking with VPs of Sales, the main challenge is inconsistent rep performance. We've developed a way to..."
                },
                "demo_pitch": {
                    "duration": "15-20 minutes",
                    "structure": [
                        "Recap their situation (2 min)",
                        "Show 3 key capabilities (10 min)",
                        "Demonstrate specific use case (5 min)",
                        "Discuss next steps (3 min)"
                    ],
                    "best_practices": [
                        "Tell a story, don't feature dump",
                        "Show their specific use case",
                        "Let them interact with the product",
                        "Check for understanding frequently"
                    ]
                }
            },
            "personalization_tips": {
                "research_checklist": [
                    "Company recent news and initiatives",
                    "Industry trends affecting them",
                    "Competitor moves in their space",
                    "Key stakeholder backgrounds",
                    "Current tech stack and tools"
                ],
                "customization_points": [
                    "Use their industry terminology",
                    "Reference their specific competitors",
                    "Mention their public goals/initiatives",
                    "Show ROI in their metrics"
                ]
            },
            "practice_scenarios": [
                {
                    "scenario": "Cold outreach to Fortune 500 CTO",
                    "time_limit": "90 seconds",
                    "goal": "Secure a discovery meeting"
                },
                {
                    "scenario": "Trade show booth interaction",
                    "time_limit": "3 minutes",
                    "goal": "Capture contact and qualify"
                },
                {
                    "scenario": "Executive presentation",
                    "time_limit": "10 minutes",
                    "goal": "Get buying committee buy-in"
                }
            ]
        }

    def _generate_negotiation_training(self, context):
        """Generate negotiation training content"""
        return {
            "negotiation_tactics": {
                "preparation": {
                    "know_your_numbers": {
                        "walk_away_point": "Minimum acceptable terms",
                        "target_price": "Ideal outcome",
                        "opening_position": "Starting point with room to move",
                        "trade_offs": "What you can give to get"
                    },
                    "understand_theirs": {
                        "budget_range": "Research and probe for limits",
                        "decision_process": "Who needs to approve",
                        "timeline_pressure": "Their urgency factors",
                        "alternatives": "Their BATNA"
                    }
                },
                "tactics": [
                    {
                        "name": "Anchoring",
                        "description": "Set the initial reference point high",
                        "example": "Our enterprise package starts at $100K, but based on your needs...",
                        "counter": "Reset anchor with your own reference point"
                    },
                    {
                        "name": "Bundling",
                        "description": "Package multiple items to increase value perception",
                        "example": "If we include training and premium support, the total package...",
                        "counter": "Unbundle to reduce if needed"
                    },
                    {
                        "name": "Scarcity",
                        "description": "Limited time or availability",
                        "example": "This pricing is available through end of quarter...",
                        "counter": "Don't overuse or lose credibility"
                    },
                    {
                        "name": "Silence",
                        "description": "Let them fill uncomfortable pauses",
                        "example": "State your position and wait...",
                        "counter": "Be comfortable with silence yourself"
                    }
                ],
                "concession_strategy": {
                    "rules": [
                        "Never give without getting",
                        "Make smaller concessions over time",
                        "Keep a concession bank",
                        "Act like concessions hurt"
                    ],
                    "examples": [
                        "If I can get you that price, can you sign this week?",
                        "I might be able to include training if you commit to 3 years",
                        "That's really pushing it, but if you can be a reference..."
                    ]
                }
            },
            "difficult_situations": [
                {
                    "situation": "Prospect demands 40% discount",
                    "approach": "Redirect to value and explore what's driving the request",
                    "response": "Help me understand what's driving that number. Is it budget constraints or value perception?",
                    "resolution": "Find creative ways to meet budget without destroying value"
                },
                {
                    "situation": "Competitive bid situation",
                    "approach": "Differentiate beyond price",
                    "response": "Price is important, but what happens if the cheaper option fails?",
                    "resolution": "Win on value, support, and risk mitigation"
                }
            ]
        }

    def _generate_performance_review(self, rep_profile):
        """Generate performance review and improvement plan"""
        return {
            "performance_metrics": {
                "current_quarter": {
                    "quota_attainment": f"{random.randint(80, 120)}%",
                    "deals_closed": random.randint(5, 20),
                    "average_deal_size": f"${random.randint(20, 100)}K",
                    "win_rate": f"{random.randint(20, 40)}%",
                    "sales_cycle": f"{random.randint(30, 90)} days"
                },
                "trends": {
                    "quota_trend": random.choice(["Improving", "Stable", "Declining"]),
                    "deal_size_trend": random.choice(["Growing", "Stable", "Shrinking"]),
                    "activity_trend": random.choice(["Increasing", "Consistent", "Decreasing"])
                },
                "benchmarks": {
                    "vs_team_average": random.choice(["Above", "At", "Below"]),
                    "vs_top_performer": f"{random.randint(60, 95)}%",
                    "industry_percentile": f"{random.randint(40, 90)}th"
                }
            },
            "strengths_analysis": [
                {
                    "strength": "Relationship building",
                    "evidence": "High customer satisfaction scores (4.8/5)",
                    "impact": "Strong renewal and upsell rates",
                    "development": "Leverage for strategic account growth"
                },
                {
                    "strength": "Product knowledge",
                    "evidence": "Technical certification completed",
                    "impact": "Credibility with technical buyers",
                    "development": "Become internal trainer/mentor"
                }
            ],
            "improvement_areas": [
                {
                    "area": "Pipeline generation",
                    "current_state": "Below target for new opportunities",
                    "impact": "Inconsistent quarterly performance",
                    "action_plan": [
                        "Increase prospecting activities by 20%",
                        "Attend 2 networking events monthly",
                        "Implement social selling strategy"
                    ],
                    "timeline": "30 days",
                    "success_metric": "15 new qualified opportunities per month"
                },
                {
                    "area": "Negotiation skills",
                    "current_state": "Giving discounts too quickly",
                    "impact": "Lower average deal value",
                    "action_plan": [
                        "Complete negotiation training",
                        "Role-play with manager weekly",
                        "Document negotiation strategy before calls"
                    ],
                    "timeline": "60 days",
                    "success_metric": "Reduce average discount by 5%"
                }
            ],
            "development_plan": {
                "short_term": {
                    "goals": [
                        "Improve discovery questioning technique",
                        "Build stronger business cases",
                        "Develop industry expertise"
                    ],
                    "activities": [
                        "Shadow top performer on 3 calls",
                        "Complete business acumen course",
                        "Read 1 industry publication weekly"
                    ],
                    "timeline": "Next 90 days"
                },
                "long_term": {
                    "career_path": "Senior AE → Enterprise AE → Sales Manager",
                    "required_skills": [
                        "Strategic account planning",
                        "Cross-functional collaboration",
                        "Team leadership"
                    ],
                    "development_opportunities": [
                        "Lead product launch team",
                        "Mentor junior reps",
                        "Own vertical market strategy"
                    ]
                }
            }
        }

    def _generate_recommendations(self, rep_profile, coaching_type):
        """Generate personalized recommendations"""
        experience = rep_profile.get('experience_level', 'intermediate')
        
        recommendations = {
            "immediate_focus": [
                "Practice active listening in your next 3 calls",
                "Prepare 5 industry-specific insights",
                "Document your talk track for consistency"
            ],
            "skill_development": [
                {
                    "skill": "Consultative selling",
                    "priority": "High",
                    "resources": ["Book: SPIN Selling", "Course: Challenger Sale"],
                    "practice": "Apply to next opportunity"
                },
                {
                    "skill": "Executive presence",
                    "priority": "Medium",
                    "resources": ["Workshop: C-Suite Selling", "Mentor: Senior AE"],
                    "practice": "Present to leadership team"
                }
            ],
            "habits_to_build": [
                "Daily prospecting block (9-10 AM)",
                "Weekly pipeline review and forecasting",
                "Post-call debriefs within 24 hours",
                "Monthly skill practice sessions"
            ],
            "accountability": {
                "check_ins": "Weekly with manager",
                "peer_practice": "Bi-weekly role-play sessions",
                "self_assessment": "Monthly scorecard review",
                "coaching_frequency": "Based on performance gaps"
            }
        }
        
        return recommendations

    def _generate_learning_resources(self, coaching_type, focus_areas):
        """Generate relevant learning resources"""
        return {
            "recommended_content": [
                {
                    "type": "Video",
                    "title": f"Mastering {coaching_type.replace('_', ' ').title()}",
                    "duration": "15 minutes",
                    "link": "internal.training/video/12345"
                },
                {
                    "type": "Article",
                    "title": "Top 10 Techniques for Sales Success",
                    "read_time": "5 minutes",
                    "link": "internal.kb/article/sales-techniques"
                },
                {
                    "type": "Podcast",
                    "title": "Sales Excellence Weekly",
                    "episode": "Handling Difficult Customers",
                    "link": "internal.podcast/episode/47"
                }
            ],
            "skill_courses": [
                {
                    "name": "Advanced Selling Techniques",
                    "provider": "Sales Academy",
                    "duration": "4 weeks",
                    "format": "Self-paced online"
                },
                {
                    "name": f"{coaching_type.replace('_', ' ').title()} Masterclass",
                    "provider": "Internal Training",
                    "duration": "2 days",
                    "format": "Virtual instructor-led"
                }
            ],
            "practice_tools": [
                "Conversation simulator",
                "Objection handling flashcards",
                "Pitch recorder and analyzer",
                "Role-play partner matching"
            ]
        }

    def _generate_practice_exercises(self, coaching_type):
        """Generate practice exercises"""
        return [
            {
                "exercise": "Record yourself delivering a 60-second pitch",
                "objective": "Improve clarity and confidence",
                "evaluation": "Self-review for filler words and energy",
                "frequency": "Daily for 1 week"
            },
            {
                "exercise": "Write 10 different value propositions",
                "objective": "Flexibility in positioning",
                "evaluation": "Test with colleagues for feedback",
                "frequency": "Complete within 3 days"
            },
            {
                "exercise": "Practice objection responses with peer",
                "objective": "Natural, confident responses",
                "evaluation": "Peer feedback on effectiveness",
                "frequency": "Weekly 30-minute sessions"
            }
        ]


if __name__ == "__main__":
    agent = SalesCoachAgent()
    
    # Test sales coaching session
    result = agent.perform(
        coaching_type="call_review",
        scenario_context={
            "industry": "Technology",
            "product": "Enterprise Software",
            "deal_size": "$100K+",
            "sales_stage": "Discovery"
        },
        rep_profile={
            "experience_level": "intermediate",
            "strengths": ["product knowledge", "rapport building"],
            "improvement_areas": ["closing", "objection handling"]
        },
        transcript="Sample call transcript here...",
        focus_areas=["discovery", "objection_handling"]
    )
    
    print(json.dumps(json.loads(result), indent=2))