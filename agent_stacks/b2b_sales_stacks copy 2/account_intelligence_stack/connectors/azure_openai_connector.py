"""
Azure OpenAI Connector
Provides AI-powered intelligence synthesis using GPT-4o

Use cases:
- Intelligence synthesis and summarization
- Message generation (emails, LinkedIn messages)
- Meeting brief creation
- Risk analysis summaries
- Competitive intelligence analysis

Includes MOCK mode (returns templated responses) and PRODUCTION mode (real GPT-4o calls)
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from connectors.base_connector import BaseConnector
from config import Config
from typing import Dict, Any, List
import json

class AzureOpenAIConnector(BaseConnector):
    """
    Azure OpenAI connector for AI-powered intelligence synthesis

    In PRODUCTION mode: Calls real Azure OpenAI GPT-4o API
    In MOCK mode: Returns realistic templated responses
    """

    def __init__(self, connector_token: str = None):
        super().__init__(connector_token)
        self.openai_config = {
            'endpoint': Config.AZURE_OPENAI_ENDPOINT,
            'api_key': Config.AZURE_OPENAI_KEY,
            'deployment': Config.AZURE_OPENAI_DEPLOYMENT,
            'api_version': Config.AZURE_OPENAI_API_VERSION,
            'temperature': Config.AZURE_OPENAI_TEMPERATURE
        }

    def authenticate(self) -> bool:
        """Authenticate with Azure OpenAI"""
        if self.is_mock:
            return True

        # Production: Validate API key
        if not self.openai_config['api_key'] or not self.openai_config['endpoint']:
            raise ValueError("Azure OpenAI credentials not configured")

        return True

    def test_connection(self) -> Dict[str, Any]:
        """Test Azure OpenAI connection"""
        if self.is_mock:
            return {
                "status": "success",
                "mode": "mock",
                "message": "Mock mode - using templated AI responses"
            }

        # Test real connection
        try:
            self.authenticate()
            return {
                "status": "success",
                "mode": "production",
                "deployment": self.openai_config['deployment'],
                "message": f"Connected to Azure OpenAI ({self.openai_config['deployment']})"
            }
        except Exception as e:
            return self._error_response(f"Connection failed: {str(e)}")

    # ==================== INTELLIGENCE SYNTHESIS METHODS ====================

    def synthesize_account_briefing(self, account_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synthesize comprehensive account briefing from multiple data sources

        Args:
            account_data: Combined data from CRM, Graph, LinkedIn, etc.

        Returns:
            AI-synthesized briefing
        """
        if self.is_mock:
            return self._mock_response(self._get_mock_account_briefing())

        # Production: Call GPT-4o
        prompt = self._build_account_briefing_prompt(account_data)
        return self._call_gpt4o(prompt, "account_briefing")

    def generate_meeting_brief(self, contact_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate executive meeting preparation brief

        Args:
            contact_data: Contact profile and interaction data
            context: Deal context, objectives, etc.

        Returns:
            AI-generated meeting brief
        """
        if self.is_mock:
            return self._mock_response(self._get_mock_meeting_brief(contact_data.get('name', 'Executive')))

        # Production: Call GPT-4o
        prompt = self._build_meeting_brief_prompt(contact_data, context)
        return self._call_gpt4o(prompt, "meeting_brief")

    def generate_message(self, message_type: str, contact_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate AI-powered messages (email, LinkedIn, etc.)

        Args:
            message_type: 'email', 'linkedin', 'follow_up'
            contact_data: Contact information
            context: Message context and objectives

        Returns:
            AI-generated message
        """
        if self.is_mock:
            return self._mock_response(self._get_mock_message(message_type, contact_data.get('name', 'Executive')))

        # Production: Call GPT-4o
        prompt = self._build_message_prompt(message_type, contact_data, context)
        return self._call_gpt4o(prompt, "message_generation")

    def analyze_competitive_intelligence(self, account_data: Dict[str, Any], competitor_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze competitive landscape and generate battle cards

        Args:
            account_data: Account information
            competitor_data: Data about competitors in the deal

        Returns:
            AI-analyzed competitive intelligence
        """
        if self.is_mock:
            return self._mock_response(self._get_mock_competitive_analysis())

        # Production: Call GPT-4o
        prompt = self._build_competitive_analysis_prompt(account_data, competitor_data)
        return self._call_gpt4o(prompt, "competitive_analysis")

    def assess_deal_risk(self, deal_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        AI-powered deal risk assessment

        Args:
            deal_data: Complete deal context

        Returns:
            Risk assessment with recommendations
        """
        if self.is_mock:
            return self._mock_response(self._get_mock_risk_assessment())

        # Production: Call GPT-4o
        prompt = self._build_risk_assessment_prompt(deal_data)
        return self._call_gpt4o(prompt, "risk_assessment")

    # ==================== MOCK DATA METHODS ====================

    def _get_mock_account_briefing(self) -> Dict[str, Any]:
        """Mock account briefing synthesis"""
        return {
            "executive_summary": "Contoso Corporation is a $2.3B manufacturing company with 12,400 employees facing a critical inflection point. Their new CTO (Dr. Sarah Chen, 6 weeks in role) is conducting aggressive vendor consolidation with explicit cost optimization mandate. Current $340K ARR renewal at HIGH RISK due to declining usage (-12%), zero CTO relationship, and competitive pressure from DataBricks.",
            "key_insights": [
                "New CTO (Sarah Chen) brings cloud modernization expertise from Microsoft/AWS - will re-evaluate ALL vendors",
                "Usage declining 12% signals product dissatisfaction or changing needs",
                "Champion (James Liu) showing reduced engagement despite 5-year tenure",
                "CFO (Robert Martinez) unreachable for 18 months - budget approval risk",
                "DataBricks has inside track via Sarah's ex-colleague relationship"
            ],
            "opportunity_assessment": {
                "deal_size": "$2.1M (renewal + expansion)",
                "current_stage": "Qualification",
                "win_probability": "47%",
                "timeline": "45-60 days",
                "risk_level": "HIGH"
            },
            "immediate_priorities": [
                "Secure CTO meeting within 7 days (use Alex Zhang for warm intro)",
                "Diagnose usage decline with customer success intervention",
                "Re-engage champion James Liu before he goes fully silent",
                "Build CFO relationship for budget approval",
                "Counter DataBricks with manufacturing industry expertise"
            ],
            "confidence_score": 92,
            "data_sources_used": ["Dynamics 365", "Microsoft Graph", "LinkedIn Sales Navigator", "Azure AI Search"],
            "last_updated": "2024-12-10T10:00:00Z"
        }

    def _get_mock_meeting_brief(self, contact_name: str) -> Dict[str, Any]:
        """Mock meeting brief generation"""
        if "Chen" in contact_name or "Sarah" in contact_name:
            return {
                "contact": {
                    "name": "Dr. Sarah Chen",
                    "title": "Chief Technology Officer",
                    "company": "Contoso Corporation"
                },
                "meeting_objective": "Establish credibility, understand her AI vision, and secure 30-day pilot agreement",
                "opening": {
                    "duration": "0-5 minutes",
                    "approach": "Acknowledge her transition and demonstrate you've done homework",
                    "script": "Sarah, thanks for making time. I know you're in week 6 of your 100-day plan, and vendor consolidation is a top priority. I've been following your LinkedIn posts about modernizing Contoso's tech stack - really insightful perspective on multi-cloud architecture."
                },
                "core_message": {
                    "duration": "5-20 minutes",
                    "key_points": [
                        "We've helped 12 manufacturers reduce cloud costs 30% while accelerating AI adoption",
                        "Unlike general-purpose platforms, we're purpose-built for manufacturing + industrial IoT",
                        "Our customers consolidate 3-5 vendors into our platform (addresses her consolidation goal)",
                        "Average ROI: 4.2x in first year"
                    ],
                    "proof_points": [
                        "Fabrikam (similar size) reduced vendor count from 7 to 2 in 90 days",
                        "Northwind achieved 99.9% uptime for factory automation",
                        "Fourth Coffee cut ML infrastructure costs 40%"
                    ]
                },
                "discovery_questions": [
                    "What's the #1 technical bottleneck you'd eliminate with a magic wand?",
                    "When you look at your current vendor landscape, where's the most complexity?",
                    "How are you thinking about AI/ML infrastructure for manufacturing use cases?",
                    "What did vendor consolidation look like at Microsoft when you were there?"
                ],
                "the_ask": {
                    "duration": "25-30 minutes",
                    "proposal": "30-day pilot with zero financial risk",
                    "terms": "3 measurable outcomes agreed upfront - if we don't hit all 3, you pay $0",
                    "pilot_scope": [
                        "Migrate 2 manufacturing workloads",
                        "Demonstrate 20%+ cost reduction",
                        "Prove vendor consolidation path (eliminate 1-2 current vendors)"
                    ]
                },
                "materials_to_bring": [
                    "Demo environment pre-loaded with Contoso data",
                    "3 manufacturing case studies: Fabrikam, Northwind, Fourth Coffee",
                    "ROI calculator on tablet (interactive)",
                    "1-page pilot proposal (leave-behind)"
                ],
                "objection_handling": {
                    "databricks_mention": "They're excellent for general AI workloads. Where we differentiate is manufacturing-specific: factory floor integration, industrial IoT, real-time quality control. Our customers often use both - DataBricks for data science, us for production manufacturing systems.",
                    "cost_concerns": "Let's run the numbers together [pull out ROI calculator]. When you factor in vendor consolidation, reduced maintenance overhead, and improved uptime, our customers see 30-40% total cost reduction despite higher per-unit pricing.",
                    "timing_concerns": "I respect that. The pilot is designed to answer your questions in 30 days with zero commitment. What if we aligned it to your 100-day plan? You'd have concrete data for your day-90 executive review."
                },
                "success_metrics": [
                    "Pilot agreement signed",
                    "Technical champion identified on her team",
                    "Follow-up meeting scheduled within 2 weeks"
                ],
                "prep_notes": {
                    "relationship_status": "First meeting - zero prior contact",
                    "influence_level": "100/100 - Economic buyer",
                    "personality_insights": "Data-driven, cost-conscious, moving fast. Appreciates directness and measurable outcomes. Her LinkedIn shows she values partners who understand manufacturing + AI.",
                    "risk_factors": "DataBricks connection, aggressive timeline, will be skeptical of sales pitch"
                }
            }
        else:
            return {
                "contact": {
                    "name": contact_name,
                    "title": "Executive",
                    "company": "Contoso Corporation"
                },
                "meeting_objective": "Build relationship and understand priorities",
                "note": "Generic meeting brief - customize with specific contact data"
            }

    def _get_mock_message(self, message_type: str, contact_name: str) -> Dict[str, Any]:
        """Mock message generation"""
        if message_type == "linkedin":
            return {
                "message_type": "linkedin_connection_request",
                "subject": "Connection Request",
                "body": f"Hi {contact_name},\n\nI noticed your recent post about modernizing Contoso's tech stack - your perspective on vendor consolidation really resonated. We've helped several manufacturers streamline their technology landscape while accelerating AI adoption.\n\nI'd love to connect and share some insights from companies in similar situations. Would you be open to a brief conversation?\n\nBest regards",
                "character_count": 347,
                "tone": "professional_and_relevant",
                "personalization_elements": [
                    "References recent LinkedIn activity",
                    "Addresses stated priority (vendor consolidation)",
                    "Offers value before asking for meeting"
                ],
                "send_timing_recommendation": "Tuesday or Wednesday, 8-10am PST (highest acceptance rate for executives)"
            }
        elif message_type == "email":
            return {
                "message_type": "email_follow_up",
                "subject": "Following up on Contoso's tech modernization initiative",
                "body": f"""Hi {contact_name},

I hope this email finds you well. I've been following Contoso's growth and was particularly interested in your recent LinkedIn post about vendor consolidation and cost optimization.

We've worked with 12+ manufacturers facing similar challenges - companies like Fabrikam and Northwind who successfully reduced vendor complexity while accelerating their AI roadmaps.

**What stood out in your LinkedIn post:**
• Vendor consolidation focus (we help customers go from 5-7 vendors → 2-3)
• Cost optimization priority (avg. 30% reduction for our manufacturing customers)
• AI-native architecture (purpose-built for manufacturing + industrial IoT)

I'd love to share a few quick insights from similar initiatives - would you be open to a brief 20-minute conversation next week?

**Here's what we'd cover:**
✓ How manufacturers are consolidating their tech stacks (real examples)
✓ ROI benchmarks for your situation
✓ A potential 30-day pilot approach with zero risk

I have Tuesday or Thursday afternoon available if that works for you.

Best regards""",
                "tone": "consultative_and_data_driven",
                "personalization_score": 95,
                "likely_response_rate": "35-40% (high for cold outreach)",
                "subject_line_alternatives": [
                    "Quick question about Contoso's vendor consolidation initiative",
                    "Sharing insights on manufacturing tech modernization",
                    "30% cost reduction case studies for manufacturers like Contoso"
                ]
            }
        else:
            return {
                "message_type": message_type,
                "note": "Message generated",
                "body": f"Generated {message_type} message for {contact_name}"
            }

    def _get_mock_competitive_analysis(self) -> Dict[str, Any]:
        """Mock competitive intelligence analysis"""
        return {
            "primary_competitors": [
                {
                    "name": "DataBricks",
                    "threat_level": "CRITICAL",
                    "threat_score": 85,
                    "strengths": [
                        "Strong general AI/ML platform",
                        "Sarah Chen's ex-colleague is their account executive",
                        "Recent funding + aggressive expansion",
                        "Modern, cloud-native architecture"
                    ],
                    "weaknesses": [
                        "Lack of manufacturing-specific features",
                        "No factory floor / IoT integration",
                        "Higher complexity for operational technology (OT)",
                        "Limited real-time processing for production systems"
                    ],
                    "our_advantages": [
                        "Purpose-built for manufacturing + industrial IoT",
                        "Proven track record with 12+ manufacturers",
                        "Factory floor integration out-of-the-box",
                        "Real-time quality control capabilities",
                        "Lower total cost when vendor consolidation factored in"
                    ],
                    "battle_card_talking_points": [
                        "DataBricks is excellent for data science teams - we complement each other. Where we shine is production manufacturing: factory floor integration, real-time OT systems, quality control.",
                        "Our customers often use both: DataBricks for exploratory data science, us for production manufacturing operations.",
                        "Key question: Does DataBricks integrate with your existing factory automation systems? That's where we've invested heavily."
                    ],
                    "win_strategy": [
                        "Position as complementary, not competitive",
                        "Focus on manufacturing expertise and factory floor integration",
                        "Highlight vendor consolidation benefits",
                        "Offer pilot to prove manufacturing-specific value"
                    ]
                },
                {
                    "name": "Snowflake",
                    "threat_level": "MODERATE",
                    "threat_score": 55,
                    "strengths": [
                        "Strong data warehousing platform",
                        "Good performance and scalability",
                        "Growing AI capabilities"
                    ],
                    "weaknesses": [
                        "Primarily data warehouse, not manufacturing platform",
                        "No OT/IoT integration",
                        "Requires additional tools for complete solution"
                    ],
                    "our_advantages": [
                        "Integrated platform (data + operations + AI)",
                        "Lower complexity (one vendor vs. multiple)",
                        "Manufacturing domain expertise"
                    ]
                }
            ],
            "competitive_positioning": "We position as the manufacturing-specialized platform that reduces vendor complexity while delivering AI capabilities. DataBricks/Snowflake are general-purpose tools that require extensive integration work for manufacturing use cases.",
            "win_themes": [
                "Manufacturing expertise & domain knowledge",
                "Vendor consolidation (reduce from 5-7 → 2-3)",
                "Total cost of ownership (30-40% reduction)",
                "Factory floor integration out-of-the-box",
                "Faster time to value (30-day pilots)",
                "Risk mitigation (zero-risk pilot approach)"
            ]
        }

    def _get_mock_risk_assessment(self) -> Dict[str, Any]:
        """Mock risk assessment"""
        return {
            "overall_risk_score": 62,
            "risk_level": "MODERATE-HIGH",
            "win_probability": {
                "current": 47,
                "potential_after_actions": 75,
                "improvement_path": "28 percentage point improvement possible"
            },
            "critical_risks": [
                {
                    "risk": "CTO Relationship Gap",
                    "severity": "CRITICAL",
                    "probability": 95,
                    "impact": "Deal killer - she controls all technology decisions",
                    "mitigation": [
                        "Immediate: Call Alex Zhang for warm introduction (he worked with her at Microsoft)",
                        "Within 48 hours: Send LinkedIn connection request",
                        "Within 7 days: Secure face-to-face meeting",
                        "Prepare manufacturing-specific pitch addressing her priorities"
                    ],
                    "time_sensitivity": "URGENT - Must act within 7 days"
                },
                {
                    "risk": "DataBricks Inside Track",
                    "severity": "CRITICAL",
                    "probability": 80,
                    "impact": "Personal relationship gives them unfair advantage",
                    "mitigation": [
                        "Position as complementary, not competitive",
                        "Focus on manufacturing differentiation",
                        "Offer pilot to prove ROI empirically",
                        "Leverage James Liu relationship for internal advocacy"
                    ],
                    "time_sensitivity": "HIGH - They're likely already in active discussions"
                },
                {
                    "risk": "Usage Declining 12%",
                    "severity": "HIGH",
                    "probability": 100,
                    "impact": "Signals product dissatisfaction or changing needs",
                    "mitigation": [
                        "Customer success intervention ASAP",
                        "Diagnose root cause (training? features? integration issues?)",
                        "Quick win: Address top pain point in next 2 weeks",
                        "Use as pilot opportunity to demonstrate improved value"
                    ],
                    "time_sensitivity": "IMMEDIATE - Usage trends continue to decline"
                }
            ],
            "moderate_risks": [
                {
                    "risk": "Champion Going Silent",
                    "severity": "MODERATE",
                    "probability": 70,
                    "impact": "Lose internal advocate",
                    "mitigation": "Coffee meeting with James Liu this week - understand his concerns"
                },
                {
                    "risk": "Budget Approval Uncertainty",
                    "severity": "MODERATE",
                    "probability": 60,
                    "impact": "CFO unreachable for 18 months",
                    "mitigation": "Build CFO relationship through CTO + show clear ROI"
                }
            ],
            "success_probability_roadmap": [
                {"milestone": "Current State", "probability": 47},
                {"milestone": "After CTO Meeting", "probability": 58},
                {"milestone": "After Usage Issue Resolved", "probability": 65},
                {"milestone": "After Pilot Agreement", "probability": 75}
            ],
            "action_plan_next_48_hours": [
                {
                    "hour": 1,
                    "action": "Call Alex Zhang for CTO warm intro",
                    "expected_outcome": "Introduction email sent",
                    "success_metric": "Meeting scheduled within 7 days"
                },
                {
                    "hour": 2,
                    "action": "Send LinkedIn connection to Sarah Chen",
                    "expected_outcome": "Connection accepted",
                    "success_metric": "Opens door for direct communication"
                },
                {
                    "hour": 3-4,
                    "action": "Customer success deep dive on usage decline",
                    "expected_outcome": "Root cause identified",
                    "success_metric": "Action plan to reverse trend"
                }
            ]
        }

    # ==================== PRODUCTION API METHODS ====================

    def _call_gpt4o(self, prompt: str, operation: str) -> Dict[str, Any]:
        """Call Azure OpenAI GPT-4o API"""
        # TODO: Implement Azure OpenAI API call
        # from openai import AzureOpenAI
        # client = AzureOpenAI(
        #     api_key=self.openai_config['api_key'],
        #     api_version=self.openai_config['api_version'],
        #     azure_endpoint=self.openai_config['endpoint']
        # )
        # response = client.chat.completions.create(
        #     model=self.openai_config['deployment'],
        #     messages=[{"role": "user", "content": prompt}],
        #     temperature=self.openai_config['temperature']
        # )
        # return self._production_response(response.choices[0].message.content, "Azure OpenAI")
        pass

    def _build_account_briefing_prompt(self, account_data: Dict[str, Any]) -> str:
        """Build prompt for account briefing synthesis"""
        # TODO: Construct comprehensive prompt from account_data
        pass

    def _build_meeting_brief_prompt(self, contact_data: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Build prompt for meeting brief generation"""
        # TODO: Construct prompt for meeting preparation
        pass

    def _build_message_prompt(self, message_type: str, contact_data: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Build prompt for message generation"""
        # TODO: Construct prompt for message creation
        pass

    def _build_competitive_analysis_prompt(self, account_data: Dict[str, Any], competitor_data: List[Dict[str, Any]]) -> str:
        """Build prompt for competitive analysis"""
        # TODO: Construct prompt for competitive intelligence
        pass

    def _build_risk_assessment_prompt(self, deal_data: Dict[str, Any]) -> str:
        """Build prompt for risk assessment"""
        # TODO: Construct prompt for risk analysis
        pass


if __name__ == "__main__":
    # Test the connector in mock mode
    print("Testing Azure OpenAI Connector in MOCK mode...")
    connector = AzureOpenAIConnector()

    # Test connection
    connection_test = connector.test_connection()
    print(f"\nConnection Test: {json.dumps(connection_test, indent=2)}")

    # Test account briefing synthesis
    print("\n=== Testing Account Briefing Synthesis ===")
    briefing = connector.synthesize_account_briefing({})
    print(f"Executive Summary Length: {len(briefing['data']['executive_summary'])} chars")
    print(f"Confidence Score: {briefing['data']['confidence_score']}%")
    print(f"Key Insights: {len(briefing['data']['key_insights'])} identified")

    # Test meeting brief generation
    print("\n=== Testing Meeting Brief Generation ===")
    meeting_brief = connector.generate_meeting_brief({"name": "Dr. Sarah Chen"}, {})
    print(f"Meeting Objective: {meeting_brief['data']['meeting_objective']}")
    print(f"Discovery Questions: {len(meeting_brief['data']['discovery_questions'])}")

    # Test message generation
    print("\n=== Testing Message Generation ===")
    linkedin_msg = connector.generate_message("linkedin", {"name": "Sarah Chen"}, {})
    print(f"Message Type: {linkedin_msg['data']['message_type']}")
    print(f"Character Count: {linkedin_msg['data']['character_count']}")

    # Test competitive analysis
    print("\n=== Testing Competitive Analysis ===")
    competitive = connector.analyze_competitive_intelligence({}, [])
    print(f"Primary Competitors: {len(competitive['data']['primary_competitors'])}")
    print(f"Top Threat: {competitive['data']['primary_competitors'][0]['name']} ({competitive['data']['primary_competitors'][0]['threat_level']})")

    # Test risk assessment
    print("\n=== Testing Risk Assessment ===")
    risk = connector.assess_deal_risk({})
    print(f"Overall Risk Score: {risk['data']['overall_risk_score']}/100")
    print(f"Win Probability: {risk['data']['win_probability']['current']}% → {risk['data']['win_probability']['potential_after_actions']}%")
    print(f"Critical Risks: {len(risk['data']['critical_risks'])}")

    print("\n✅ Azure OpenAI Connector test complete!")
