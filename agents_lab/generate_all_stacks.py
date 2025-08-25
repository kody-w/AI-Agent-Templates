#!/usr/bin/env python3

import os
import json
from pathlib import Path

# Define all remaining agent stacks
AGENT_STACKS = {
    "healthcare_stack": [
        {
            "name": "clinical_notes_summarizer",
            "display_name": "Clinical Notes Summarizer",
            "description": "Generates real-time summaries from provider-patient conversations",
            "systems": ["Epic", "Cerner", "Power Platform", "Azure OpenAI"],
            "benefits": ["Reduces documentation time by 60%", "Improves note accuracy", "Enables real-time decision support"],
            "use_cases": ["Real-time visit summarization", "Post-visit documentation", "Clinical decision support"]
        },
        {
            "name": "care_gap_closure",
            "display_name": "Care Gap Closure Agent",
            "description": "Identifies missing screenings and automates patient outreach",
            "systems": ["EHR", "CRM", "Azure Data Lake", "Power Automate"],
            "benefits": ["Improves quality scores", "Increases preventive care compliance", "Reduces readmission rates"],
            "use_cases": ["Preventive care reminders", "Chronic disease management", "Quality measure tracking"]
        },
        {
            "name": "staff_credentialing",
            "display_name": "Staff Credentialing Agent",
            "description": "Automates tracking and renewal of healthcare staff credentials",
            "systems": ["Workday", "SAP SuccessFactors", "Kronos", "SharePoint"],
            "benefits": ["Ensures compliance", "Reduces credential lapses", "Automates renewal notifications"],
            "use_cases": ["License renewal tracking", "Certification management", "Compliance reporting"]
        }
    ],
    "energy_stack": [
        {
            "name": "asset_maintenance_forecast",
            "display_name": "Asset Maintenance Forecast Agent",
            "description": "Predicts equipment failure and schedules maintenance proactively",
            "systems": ["SAP PM", "IBM Maximo", "D365 F&O", "Azure IoT"],
            "benefits": ["Reduces unplanned downtime by 40%", "Extends equipment life", "Optimizes maintenance costs"],
            "use_cases": ["Predictive maintenance", "Equipment lifecycle management", "Maintenance scheduling"]
        },
        {
            "name": "regulatory_reporting",
            "display_name": "Regulatory Reporting Agent",
            "description": "Auto-generates EPA/FERC/OSHA compliance documents",
            "systems": ["Oracle", "OpenText", "Azure Compliance Manager", "SharePoint"],
            "benefits": ["Ensures regulatory compliance", "Reduces reporting time by 70%", "Minimizes compliance risks"],
            "use_cases": ["Environmental reporting", "Safety compliance", "Regulatory submissions"]
        },
        {
            "name": "field_service_dispatch",
            "display_name": "Field Service Dispatch Agent",
            "description": "Optimizes technician dispatch based on skills, location, and urgency",
            "systems": ["D365 Field Service", "SAP FSM", "Oracle Field Service", "ServiceNow"],
            "benefits": ["Improves first-time fix rate", "Reduces travel time", "Increases technician utilization"],
            "use_cases": ["Emergency dispatch", "Routine maintenance scheduling", "Resource optimization"]
        },
        {
            "name": "emission_tracking",
            "display_name": "Emission Tracking Agent",
            "description": "Tracks, analyzes, and reports carbon emissions across operations",
            "systems": ["Azure IoT", "SAP", "Enablon", "Power BI"],
            "benefits": ["Ensures environmental compliance", "Supports sustainability goals", "Provides real-time emissions data"],
            "use_cases": ["Carbon footprint tracking", "Emissions reporting", "Sustainability monitoring"]
        },
        {
            "name": "permit_license_management",
            "display_name": "Permit & License Management Agent",
            "description": "Automates renewal and tracking of operational permits",
            "systems": ["SharePoint", "SAP", "Power Platform", "D365"],
            "benefits": ["Prevents permit lapses", "Automates renewal processes", "Maintains compliance"],
            "use_cases": ["Permit renewal tracking", "License management", "Compliance monitoring"]
        }
    ],
    "manufacturing_stack": [
        {
            "name": "supplier_risk_monitoring",
            "display_name": "Supplier Risk Monitoring Agent",
            "description": "Detects supply chain risks and recommends mitigation strategies",
            "systems": ["SAP Ariba", "D365 SCM", "Oracle SCM", "Azure AI"],
            "benefits": ["Reduces supply chain disruptions", "Improves supplier reliability", "Enables proactive risk management"],
            "use_cases": ["Supplier performance tracking", "Risk assessment", "Alternative sourcing"]
        },
        {
            "name": "production_line_optimization",
            "display_name": "Production Line Optimization Agent",
            "description": "Analyzes production output and suggests efficiency improvements",
            "systems": ["MES", "D365 SCM", "Siemens", "Azure IoT"],
            "benefits": ["Increases OEE by 15%", "Reduces waste", "Improves throughput"],
            "use_cases": ["Line balancing", "Bottleneck analysis", "Quality optimization"]
        },
        {
            "name": "inventory_rebalancing",
            "display_name": "Inventory Rebalancing Agent",
            "description": "Prevents overstock and stockouts through intelligent rebalancing",
            "systems": ["D365 F&O", "SAP", "NetSuite", "Power BI"],
            "benefits": ["Reduces inventory costs by 25%", "Improves order fulfillment", "Optimizes working capital"],
            "use_cases": ["Stock level optimization", "Demand forecasting", "Warehouse transfers"]
        },
        {
            "name": "maintenance_scheduling",
            "display_name": "Maintenance Scheduling Agent",
            "description": "Reduces downtime by predicting equipment failures",
            "systems": ["IBM Maximo", "SAP PM", "Azure IoT", "D365"],
            "benefits": ["Reduces maintenance costs by 30%", "Minimizes production disruptions", "Extends equipment life"],
            "use_cases": ["Predictive maintenance", "Scheduled maintenance", "Resource planning"]
        },
        {
            "name": "order_status_communication",
            "display_name": "Order Status Communication Agent",
            "description": "Provides live updates on manufacturing and delivery status",
            "systems": ["D365 CRM", "Salesforce", "SAP", "Power Automate"],
            "benefits": ["Improves customer satisfaction", "Reduces support inquiries", "Enables proactive communication"],
            "use_cases": ["Order tracking", "Delivery notifications", "Production updates"]
        }
    ],
    "software_dp_stack": [
        {
            "name": "support_ticket_resolution",
            "display_name": "Support Ticket Resolution Agent",
            "description": "Resolves L1/L2 support tickets autonomously",
            "systems": ["Zendesk", "Salesforce Service Cloud", "ServiceNow", "Azure OpenAI"],
            "benefits": ["Reduces ticket resolution time by 60%", "Improves customer satisfaction", "Frees up support staff"],
            "use_cases": ["Automated ticket triage", "Knowledge base search", "Solution recommendation"]
        },
        {
            "name": "customer_onboarding",
            "display_name": "Customer Onboarding Agent",
            "description": "Walks users through setup and configuration processes",
            "systems": ["Gainsight", "Salesforce", "D365 CE", "Power Platform"],
            "benefits": ["Reduces time to value", "Improves adoption rates", "Decreases support tickets"],
            "use_cases": ["Guided setup", "Configuration assistance", "Training delivery"]
        },
        {
            "name": "competitive_intel",
            "display_name": "Competitive Intelligence Agent",
            "description": "Pulls competitor news, pricing, and feature updates",
            "systems": ["CRM", "Sales Enablement Platforms", "Copilot Studio", "Power BI"],
            "benefits": ["Enables competitive positioning", "Informs product strategy", "Supports sales enablement"],
            "use_cases": ["Market analysis", "Competitive tracking", "Win/loss analysis"]
        },
        {
            "name": "product_feedback_synthesizer",
            "display_name": "Product Feedback Synthesizer",
            "description": "Analyzes customer feedback for feature requests and fixes",
            "systems": ["Azure OpenAI", "Jira", "DevOps", "GitHub"],
            "benefits": ["Improves product-market fit", "Prioritizes development efforts", "Reduces churn"],
            "use_cases": ["Feature prioritization", "Bug tracking", "Customer sentiment analysis"]
        },
        {
            "name": "license_renewal_expansion",
            "display_name": "License Renewal & Expansion Agent",
            "description": "Flags expiring licenses and triggers customer success motions",
            "systems": ["Salesforce CPQ", "D365", "NetSuite", "Gainsight"],
            "benefits": ["Increases renewal rates", "Identifies expansion opportunities", "Reduces revenue leakage"],
            "use_cases": ["Renewal forecasting", "Upsell identification", "Churn prevention"]
        }
    ],
    "professional_services_stack": [
        {
            "name": "contract_risk_review",
            "display_name": "Contract Risk Review Agent",
            "description": "Reviews contracts for risk and compliance issues",
            "systems": ["DocuSign", "Adobe Sign", "SharePoint", "Azure OpenAI"],
            "benefits": ["Reduces contract review time by 70%", "Minimizes legal risks", "Ensures compliance"],
            "use_cases": ["Contract analysis", "Risk assessment", "Compliance checking"]
        },
        {
            "name": "time_entry_billing",
            "display_name": "Time Entry & Billing Agent",
            "description": "Auto-logs time and generates accurate invoices",
            "systems": ["NetSuite", "SAP Concur", "D365 Project Ops", "QuickBooks"],
            "benefits": ["Improves billing accuracy", "Reduces revenue leakage", "Accelerates cash flow"],
            "use_cases": ["Automated time tracking", "Invoice generation", "Expense management"]
        },
        {
            "name": "proposal_copilot",
            "display_name": "Proposal Co-Pilot Agent",
            "description": "Builds proposals from requirements and templates",
            "systems": ["SharePoint", "PowerPoint", "Word", "D365 CE"],
            "benefits": ["Reduces proposal creation time by 50%", "Improves win rates", "Ensures consistency"],
            "use_cases": ["RFP responses", "SOW creation", "Proposal customization"]
        },
        {
            "name": "resource_utilization",
            "display_name": "Resource Utilization Agent",
            "description": "Matches staff skills to project requirements optimally",
            "systems": ["Workday", "D365 HR", "SAP SuccessFactors", "ProjectPro"],
            "benefits": ["Improves utilization rates", "Reduces bench time", "Optimizes project staffing"],
            "use_cases": ["Resource planning", "Skills matching", "Capacity forecasting"]
        },
        {
            "name": "client_health_score",
            "display_name": "Client Health Score Agent",
            "description": "Aggregates sentiment, usage, and satisfaction metrics",
            "systems": ["D365 CE", "Gainsight", "Power BI", "ServiceNow"],
            "benefits": ["Predicts churn risk", "Identifies growth opportunities", "Improves client retention"],
            "use_cases": ["Health scoring", "Risk monitoring", "Success planning"]
        }
    ],
    "retail_cpg_stack": [
        {
            "name": "inventory_visibility",
            "display_name": "Inventory Visibility Agent",
            "description": "Provides real-time inventory across all channels",
            "systems": ["SAP", "Oracle Retail", "D365 Commerce", "Power BI"],
            "benefits": ["Reduces stockouts by 30%", "Improves customer satisfaction", "Optimizes inventory levels"],
            "use_cases": ["Stock checking", "Transfer management", "Replenishment planning"]
        },
        {
            "name": "personalized_marketing",
            "display_name": "Personalized Marketing Agent",
            "description": "Creates targeted campaigns based on customer behavior",
            "systems": ["Adobe", "D365 Marketing", "Salesforce Marketing", "Power Platform"],
            "benefits": ["Increases conversion rates", "Improves customer engagement", "Reduces marketing costs"],
            "use_cases": ["Campaign personalization", "Customer segmentation", "Behavioral targeting"]
        },
        {
            "name": "store_associate_copilot",
            "display_name": "Store Associate Copilot",
            "description": "Assists staff with product information and promotions",
            "systems": ["POS", "D365", "Salesforce", "Power Platform"],
            "benefits": ["Improves sales conversion", "Enhances customer service", "Reduces training time"],
            "use_cases": ["Product lookup", "Promotion assistance", "Customer service support"]
        },
        {
            "name": "returns_complaints_resolution",
            "display_name": "Returns & Complaints Resolution Agent",
            "description": "Handles customer issues and return processing",
            "systems": ["ServiceNow", "D365 CE", "Zendesk", "SAP"],
            "benefits": ["Reduces resolution time", "Improves customer satisfaction", "Decreases return rates"],
            "use_cases": ["Return processing", "Complaint handling", "Issue resolution"]
        },
        {
            "name": "supply_chain_disruption_alert",
            "display_name": "Supply Chain Disruption Alert Agent",
            "description": "Notifies of disruptions and recommends alternatives",
            "systems": ["SAP SCM", "Oracle", "Azure IoT", "Power BI"],
            "benefits": ["Minimizes stockouts", "Enables proactive planning", "Reduces supply chain risks"],
            "use_cases": ["Disruption monitoring", "Alternative sourcing", "Risk mitigation"]
        }
    ],
    "financial_services_stack": [
        {
            "name": "customer_onboarding_fs",
            "display_name": "Customer Onboarding Agent",
            "description": "Automates KYC and account setup processes",
            "systems": ["Salesforce Financial Services Cloud", "D365 CE", "Workday", "Oracle"],
            "benefits": ["Reduces onboarding time by 60%", "Improves compliance", "Enhances customer experience"],
            "use_cases": ["KYC verification", "Account opening", "Document collection"]
        },
        {
            "name": "fraud_detection_alert",
            "display_name": "Fraud Detection & Alert Agent",
            "description": "Monitors transactions for suspicious activity patterns",
            "systems": ["Core Banking", "Azure AI", "Fraud Platforms", "Power BI"],
            "benefits": ["Reduces fraud losses", "Improves detection accuracy", "Enables real-time prevention"],
            "use_cases": ["Transaction monitoring", "Pattern detection", "Alert generation"]
        },
        {
            "name": "loan_origination_assistant",
            "display_name": "Loan Origination Assistant",
            "description": "Streamlines loan application and credit assessment",
            "systems": ["nCino", "Salesforce", "Temenos", "D365 CE"],
            "benefits": ["Accelerates loan processing", "Improves approval rates", "Reduces operational costs"],
            "use_cases": ["Application processing", "Credit scoring", "Document verification"]
        },
        {
            "name": "financial_advisor_copilot",
            "display_name": "Financial Advisor Copilot",
            "description": "Surfaces investment strategies and client insights",
            "systems": ["CRM", "Bloomberg", "Power BI", "Advisor Portals"],
            "benefits": ["Improves advisor productivity", "Enhances client outcomes", "Increases AUM"],
            "use_cases": ["Portfolio recommendations", "Client insights", "Market analysis"]
        },
        {
            "name": "claims_processing",
            "display_name": "Claims Processing Agent",
            "description": "Automates insurance claim intake and processing",
            "systems": ["Guidewire", "Duck Creek", "Salesforce", "D365 CE"],
            "benefits": ["Reduces processing time by 50%", "Improves accuracy", "Enhances customer satisfaction"],
            "use_cases": ["Claim submission", "Document processing", "Status tracking"]
        },
        {
            "name": "regulatory_compliance_fs",
            "display_name": "Regulatory Compliance Agent",
            "description": "Ensures AML and GDPR compliance adherence",
            "systems": ["GRC Platforms", "Azure Compliance", "Oracle", "SAP"],
            "benefits": ["Reduces compliance risks", "Automates reporting", "Ensures audit readiness"],
            "use_cases": ["AML monitoring", "GDPR compliance", "Regulatory reporting"]
        },
        {
            "name": "customer_sentiment_churn",
            "display_name": "Customer Sentiment & Churn Risk Agent",
            "description": "Analyzes interactions to identify at-risk customers",
            "systems": ["Salesforce", "D365", "Genesys", "Power BI"],
            "benefits": ["Reduces churn by 25%", "Improves retention", "Enables proactive intervention"],
            "use_cases": ["Sentiment analysis", "Churn prediction", "Retention campaigns"]
        },
        {
            "name": "portfolio_rebalancing",
            "display_name": "Portfolio Rebalancing Agent",
            "description": "Detects drift and recommends rebalancing actions",
            "systems": ["Investment Platforms", "Bloomberg", "CRM", "Risk Engines"],
            "benefits": ["Maintains target allocations", "Reduces risk", "Improves returns"],
            "use_cases": ["Drift detection", "Rebalancing recommendations", "Risk management"]
        },
        {
            "name": "wealth_insights_generator",
            "display_name": "Wealth Insights Generator",
            "description": "Consolidates assets and generates comprehensive reports",
            "systems": ["CRM", "D365 CE", "Power BI", "Core Banking"],
            "benefits": ["Provides holistic view", "Improves advisory quality", "Increases client engagement"],
            "use_cases": ["Wealth reporting", "Performance analysis", "Goal tracking"]
        },
        {
            "name": "underwriting_support",
            "display_name": "Underwriting Support Agent",
            "description": "Pulls risk data and summarizes applications",
            "systems": ["Underwriting Engines", "CRM", "Azure OpenAI", "SharePoint"],
            "benefits": ["Accelerates underwriting", "Improves risk assessment", "Reduces manual effort"],
            "use_cases": ["Risk analysis", "Application review", "Decision support"]
        }
    ],
    "slg_government_stack": [
        {
            "name": "citizen_service_request",
            "display_name": "Citizen Service Request Agent",
            "description": "24/7 intake and routing of non-emergency issues",
            "systems": ["D365 CE", "Salesforce", "ServiceNow", "Accela"],
            "benefits": ["Improves citizen satisfaction", "Reduces response times", "Increases efficiency"],
            "use_cases": ["Service requests", "Issue reporting", "Status tracking"]
        },
        {
            "name": "grants_management",
            "display_name": "Grants Management Agent",
            "description": "Automates grant intake, scoring, and tracking",
            "systems": ["Salesforce Grants360", "D365", "SAP", "PowerApps"],
            "benefits": ["Streamlines grant process", "Improves transparency", "Ensures compliance"],
            "use_cases": ["Application processing", "Scoring automation", "Performance tracking"]
        },
        {
            "name": "building_permit_processing",
            "display_name": "Building Permit Processing Agent",
            "description": "Reviews applications and tracks permit status",
            "systems": ["Tyler Technologies", "Accela", "SharePoint", "D365"],
            "benefits": ["Reduces processing time", "Improves accuracy", "Enhances transparency"],
            "use_cases": ["Permit applications", "Review automation", "Status notifications"]
        },
        {
            "name": "utility_billing_assistance",
            "display_name": "Utility Billing & Assistance Agent",
            "description": "Manages utility bills and assistance programs",
            "systems": ["SAP", "Oracle", "Munis", "D365 Finance"],
            "benefits": ["Improves payment rates", "Reduces delinquencies", "Enhances citizen services"],
            "use_cases": ["Bill inquiries", "Payment processing", "Assistance applications"]
        },
        {
            "name": "foia_request_assistant",
            "display_name": "FOIA Request Assistant",
            "description": "Automates document search and redaction for FOIA",
            "systems": ["SharePoint", "OpenText", "Adobe", "Azure AI Search"],
            "benefits": ["Reduces response time", "Ensures compliance", "Improves transparency"],
            "use_cases": ["Request processing", "Document search", "Redaction automation"]
        }
    ],
    "federal_government_stack": [
        {
            "name": "regulatory_compliance_fed",
            "display_name": "Regulatory Compliance Agent",
            "description": "Monitors and reports FedRAMP/NIST compliance",
            "systems": ["SAP", "ServiceNow GRC", "OpenText", "Power BI"],
            "benefits": ["Ensures compliance", "Automates reporting", "Reduces audit findings"],
            "use_cases": ["Compliance monitoring", "Audit preparation", "Risk assessment"]
        },
        {
            "name": "federal_grants_oversight",
            "display_name": "Federal Grants Oversight Agent",
            "description": "Tracks grant spending, risk, and reporting",
            "systems": ["Oracle Grants", "Salesforce", "D365 Finance", "SAP"],
            "benefits": ["Improves oversight", "Ensures compliance", "Reduces waste"],
            "use_cases": ["Spending tracking", "Risk monitoring", "Performance reporting"]
        },
        {
            "name": "acquisition_support",
            "display_name": "Acquisition Support Agent",
            "description": "Summarizes proposals and checks procurement compliance",
            "systems": ["PRISM", "ConcurGov", "SAP Ariba", "D365 Project Ops"],
            "benefits": ["Accelerates procurement", "Ensures compliance", "Improves decisions"],
            "use_cases": ["Proposal evaluation", "Compliance checking", "Vendor assessment"]
        },
        {
            "name": "workforce_clearance_onboarding",
            "display_name": "Workforce Clearance & Onboarding Agent",
            "description": "Streamlines background checks and training",
            "systems": ["Workday GovCloud", "D365 HR", "Oracle HCM", "USAccess"],
            "benefits": ["Reduces onboarding time", "Ensures compliance", "Improves tracking"],
            "use_cases": ["Clearance processing", "Training management", "Compliance tracking"]
        },
        {
            "name": "mission_reporting_assistant",
            "display_name": "Mission Reporting Assistant",
            "description": "Generates reports from classified and unclassified sources",
            "systems": ["SharePoint", "Azure GovCloud", "Palantir", "Power BI"],
            "benefits": ["Improves decision-making", "Accelerates reporting", "Enhances visibility"],
            "use_cases": ["Mission reporting", "Data aggregation", "Executive briefings"]
        }
    ],
    "b2b_sales_stack": [
        {
            "name": "sales_qualification",
            "display_name": "Sales Qualification Agent",
            "description": "Assesses leads and prioritizes by fit and intent",
            "systems": ["D365 Sales", "Salesforce", "LinkedIn Sales Navigator", "6sense"],
            "benefits": ["Improves conversion rates", "Focuses sales efforts", "Reduces sales cycle"],
            "use_cases": ["Lead scoring", "Qualification automation", "Priority ranking"]
        },
        {
            "name": "account_intelligence",
            "display_name": "Account Intelligence Agent",
            "description": "Surfaces org charts, news, and stakeholder interests",
            "systems": ["CRM", "LinkedIn", "Power BI", "Sales Enablement"],
            "benefits": ["Improves account penetration", "Enables strategic selling", "Increases deal size"],
            "use_cases": ["Account mapping", "Stakeholder analysis", "Opportunity identification"]
        },
        {
            "name": "proposal_generation",
            "display_name": "Proposal Generation Agent",
            "description": "Creates tailored proposals from prior successful deals",
            "systems": ["SharePoint", "Word", "D365", "Salesforce"],
            "benefits": ["Reduces proposal time", "Improves win rates", "Ensures consistency"],
            "use_cases": ["Proposal creation", "Content customization", "Pricing optimization"]
        },
        {
            "name": "deal_progression",
            "display_name": "Deal Progression Agent",
            "description": "Flags stalled deals and recommends next actions",
            "systems": ["Salesforce", "D365", "Power BI", "Gong"],
            "benefits": ["Reduces deal slippage", "Improves forecast accuracy", "Accelerates closure"],
            "use_cases": ["Pipeline management", "Risk identification", "Action recommendations"]
        },
        {
            "name": "win_loss_analysis",
            "display_name": "Win/Loss Analysis Agent",
            "description": "Analyzes closed deals for trends and insights",
            "systems": ["CRM", "Power BI", "Copilot Studio", "Clari"],
            "benefits": ["Improves win rates", "Identifies success patterns", "Informs strategy"],
            "use_cases": ["Deal analysis", "Competitive insights", "Process improvement"]
        }
    ],
    "b2c_sales_stack": [
        {
            "name": "personalized_shopping_assistant",
            "display_name": "Personalized Shopping Assistant",
            "description": "Guides product discovery and purchase decisions",
            "systems": ["Commerce Platforms", "D365 Commerce", "Adobe Experience", "Shopify"],
            "benefits": ["Increases conversion", "Improves AOV", "Enhances experience"],
            "use_cases": ["Product recommendations", "Guided selling", "Virtual assistance"]
        },
        {
            "name": "cart_abandonment_recovery",
            "display_name": "Cart Abandonment Recovery Agent",
            "description": "Follows up to convert abandoned carts to sales",
            "systems": ["Shopify", "Magento", "Salesforce Commerce", "Email Platforms"],
            "benefits": ["Recovers lost revenue", "Improves conversion", "Reduces abandonment"],
            "use_cases": ["Abandonment campaigns", "Incentive offers", "Retargeting"]
        },
        {
            "name": "omnichannel_engagement",
            "display_name": "Omnichannel Engagement Agent",
            "description": "Coordinates messaging across all customer channels",
            "systems": ["Adobe", "Salesforce Marketing Cloud", "D365 Marketing", "Braze"],
            "benefits": ["Improves consistency", "Increases engagement", "Enhances experience"],
            "use_cases": ["Cross-channel campaigns", "Journey orchestration", "Personalization"]
        },
        {
            "name": "returns_exchange",
            "display_name": "Returns & Exchange Agent",
            "description": "Automates return and refund workflows",
            "systems": ["ERP", "Commerce Engines", "Service Platforms", "D365"],
            "benefits": ["Reduces processing time", "Improves satisfaction", "Minimizes losses"],
            "use_cases": ["Return processing", "Exchange management", "Refund automation"]
        },
        {
            "name": "customer_loyalty_rewards",
            "display_name": "Customer Loyalty & Rewards Agent",
            "description": "Manages loyalty programs and redemptions",
            "systems": ["CRM", "Loyalty Platforms", "D365 Marketing", "Salesforce"],
            "benefits": ["Increases retention", "Drives repeat purchases", "Improves engagement"],
            "use_cases": ["Points management", "Reward redemption", "Tier progression"]
        }
    ]
}

def create_agent_file(stack_dir, agent_info):
    """Create the Python agent file"""
    agent_code = f'''import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

from agents.basic_agent import BasicAgent
import json
from datetime import datetime, timedelta
import random

class {agent_info["name"].replace("_", " ").title().replace(" ", "")}Agent(BasicAgent):
    def __init__(self):
        self.name = "{agent_info['name'].replace('_', ' ').title().replace(' ', '')}Agent"
        self.metadata = {{
            "name": self.name,
            "description": "{agent_info['description']}",
            "parameters": {{
                "type": "object",
                "properties": {{
                    "action": {{
                        "type": "string",
                        "enum": ["execute", "analyze", "report", "optimize"],
                        "description": "Action to perform"
                    }},
                    "entity_id": {{
                        "type": "string",
                        "description": "Unique identifier for the entity"
                    }},
                    "data": {{
                        "type": "object",
                        "description": "Additional data for the operation"
                    }},
                    "mode": {{
                        "type": "string",
                        "enum": ["real-time", "batch", "scheduled"],
                        "description": "Processing mode"
                    }}
                }},
                "required": ["action"]
            }}
        }}
        super().__init__(name=self.name, metadata=self.metadata)
    
    def perform(self, **kwargs):
        action = kwargs.get('action', 'execute')
        
        if action == 'execute':
            return self._execute(kwargs)
        elif action == 'analyze':
            return self._analyze(kwargs)
        elif action == 'report':
            return self._report(kwargs)
        elif action == 'optimize':
            return self._optimize(kwargs)
        else:
            return {{"status": "error", "message": f"Unknown action: {{action}}"}}
    
    def _execute(self, params):
        """Execute primary operation"""
        return {{
            "status": "success",
            "message": "{agent_info['display_name']} executed successfully",
            "data": {{
                "operation_id": f"OP{{random.randint(100000, 999999)}}",
                "entity_id": params.get('entity_id', f"ENT{{random.randint(1000, 9999)}}"),
                "timestamp": datetime.now().isoformat(),
                "integrated_systems": {json.dumps(agent_info['systems'])},
                "results": {{
                    "processed_items": random.randint(10, 100),
                    "success_rate": f"{{random.randint(85, 99)}}%",
                    "processing_time": f"{{random.randint(1, 10)}} seconds"
                }}
            }}
        }}
    
    def _analyze(self, params):
        """Perform analysis operation"""
        return {{
            "status": "success",
            "message": "Analysis completed",
            "data": {{
                "analysis_id": f"AN{{random.randint(10000, 99999)}}",
                "insights": [
                    "Key insight from {agent_info['display_name']}",
                    "Optimization opportunity identified",
                    "Risk factor detected and mitigated"
                ],
                "recommendations": {json.dumps(agent_info['use_cases'])},
                "confidence_score": random.randint(75, 95)
            }}
        }}
    
    def _report(self, params):
        """Generate report"""
        return {{
            "status": "success",
            "message": "Report generated",
            "data": {{
                "report_id": f"RPT{{random.randint(10000, 99999)}}",
                "summary": "{agent_info['description']}",
                "benefits": {json.dumps(agent_info['benefits'])},
                "metrics": {{
                    "efficiency_gain": f"{{random.randint(20, 70)}}%",
                    "cost_reduction": f"${{random.randint(1000, 50000)}}",
                    "time_saved": f"{{random.randint(5, 40)}} hours/week"
                }}
            }}
        }}
    
    def _optimize(self, params):
        """Perform optimization"""
        return {{
            "status": "success",
            "message": "Optimization completed",
            "data": {{
                "optimization_id": f"OPT{{random.randint(10000, 99999)}}",
                "improvements": {{
                    "before": {{
                        "efficiency": f"{{random.randint(40, 60)}}%",
                        "throughput": f"{{random.randint(100, 500)}} units/hour"
                    }},
                    "after": {{
                        "efficiency": f"{{random.randint(70, 95)}}%",
                        "throughput": f"{{random.randint(600, 1000)}} units/hour"
                    }}
                }},
                "next_steps": ["Monitor performance", "Adjust parameters", "Scale operations"]
            }}
        }}

if __name__ == "__main__":
    agent = {agent_info['name'].replace('_', ' ').title().replace(' ', '')}Agent()
    
    # Test execution
    result = agent.perform(
        action="execute",
        entity_id="TEST123",
        mode="real-time"
    )
    print(json.dumps(result, indent=2))
'''
    
    agent_path = os.path.join(stack_dir, "agents", f"{agent_info['name']}_agent.py")
    os.makedirs(os.path.dirname(agent_path), exist_ok=True)
    
    with open(agent_path, 'w') as f:
        f.write(agent_code)
    
    print(f"Created agent: {agent_path}")

def create_demo_file(stack_dir, agent_info):
    """Create the HTML demo file"""
    demo_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{agent_info["display_name"]} - Interactive Demo</title>
    <style>
        :root {{
            --primary: #742774;
            --secondary: #00a651;
            --accent: #4a90e2;
            --dark: #1e1e1e;
            --light: #f5f5f5;
            --error: #e74c3c;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }}

        .container {{
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 1200px;
            width: 100%;
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        .mode-toggle {{
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 20px;
        }}

        .mode-btn {{
            padding: 10px 20px;
            border: 2px solid white;
            background: transparent;
            color: white;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: bold;
        }}

        .mode-btn.active {{
            background: white;
            color: var(--primary);
        }}

        .content {{
            padding: 30px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
        }}

        .panel {{
            background: var(--light);
            border-radius: 15px;
            padding: 25px;
        }}

        .form-group {{
            margin-bottom: 20px;
        }}

        .form-group label {{
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: var(--dark);
        }}

        .form-group input, .form-group select {{
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
        }}

        .btn {{
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
            margin-top: 10px;
        }}

        .btn-primary {{
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
        }}

        .btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}

        .results {{
            margin-top: 20px;
            padding: 20px;
            background: white;
            border-radius: 10px;
            display: none;
        }}

        .results.active {{
            display: block;
        }}

        .metrics {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-top: 20px;
        }}

        .metric {{
            text-align: center;
            padding: 15px;
            background: var(--light);
            border-radius: 10px;
        }}

        .metric-value {{
            font-size: 24px;
            font-weight: bold;
            color: var(--primary);
        }}

        .metric-label {{
            color: #666;
            margin-top: 5px;
        }}

        .systems {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 15px;
        }}

        .system-badge {{
            padding: 5px 12px;
            background: var(--secondary);
            color: white;
            border-radius: 15px;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 {agent_info["display_name"]}</h1>
            <p>{agent_info["description"]}</p>
            <div class="mode-toggle">
                <button class="mode-btn active" onclick="setMode('demo')">Demo Mode</button>
                <button class="mode-btn" onclick="setMode('live')">Live Mode</button>
            </div>
        </div>

        <div class="content">
            <div class="panel">
                <h2>Configuration</h2>
                
                <div class="form-group">
                    <label>Entity ID</label>
                    <input type="text" id="entityId" placeholder="Enter entity ID" value="DEMO123">
                </div>

                <div class="form-group">
                    <label>Action</label>
                    <select id="action">
                        <option value="execute">Execute</option>
                        <option value="analyze">Analyze</option>
                        <option value="report">Generate Report</option>
                        <option value="optimize">Optimize</option>
                    </select>
                </div>

                <div class="form-group">
                    <label>Processing Mode</label>
                    <select id="mode">
                        <option value="real-time">Real-time</option>
                        <option value="batch">Batch</option>
                        <option value="scheduled">Scheduled</option>
                    </select>
                </div>

                <button class="btn btn-primary" onclick="executeAgent()">Execute Agent</button>
            </div>

            <div class="panel">
                <h2>Results</h2>
                
                <div class="results" id="results">
                    <h3>Operation Complete</h3>
                    <div class="metrics">
                        <div class="metric">
                            <div class="metric-value" id="processed">-</div>
                            <div class="metric-label">Items Processed</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value" id="efficiency">-</div>
                            <div class="metric-label">Efficiency</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value" id="time">-</div>
                            <div class="metric-label">Time Saved</div>
                        </div>
                    </div>
                    
                    <h4 style="margin-top: 20px;">Integrated Systems</h4>
                    <div class="systems" id="systems">
                        {' '.join([f'<span class="system-badge">{system}</span>' for system in agent_info["systems"]])}
                    </div>
                    
                    <h4 style="margin-top: 20px;">Benefits</h4>
                    <ul id="benefits">
                        {''.join([f'<li>{benefit}</li>' for benefit in agent_info["benefits"]])}
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <script>
        let currentMode = 'demo';

        function setMode(mode) {{
            currentMode = mode;
            document.querySelectorAll('.mode-btn').forEach(btn => {{
                btn.classList.remove('active');
            }});
            event.target.classList.add('active');
        }}

        function executeAgent() {{
            const results = document.getElementById('results');
            results.classList.add('active');
            
            // Simulate results
            document.getElementById('processed').textContent = Math.floor(Math.random() * 90) + 10;
            document.getElementById('efficiency').textContent = Math.floor(Math.random() * 30) + 70 + '%';
            document.getElementById('time').textContent = Math.floor(Math.random() * 35) + 5 + ' hours';
        }}
    </script>
</body>
</html>'''
    
    demo_path = os.path.join(stack_dir, "demos", f"{agent_info['name']}_demo.html")
    os.makedirs(os.path.dirname(demo_path), exist_ok=True)
    
    with open(demo_path, 'w') as f:
        f.write(demo_html)
    
    print(f"Created demo: {demo_path}")

def create_metadata_file(stack_dir, agent_info, sector):
    """Create the metadata.json file"""
    metadata = {
        "id": f"{agent_info['name']}_stack",
        "name": f"{agent_info['display_name']} Stack",
        "version": "1.0.0",
        "description": agent_info["description"],
        "category": sector.replace("_stack", ""),
        "complexity": "intermediate",
        "features": agent_info["use_cases"],
        "benefits": agent_info["benefits"],
        "technicalRequirements": {
            "platforms": ["Windows", "macOS", "Linux"],
            "dependencies": ["Python 3.8+", "requests", "json"],
            "apiKeys": [f"{system.upper().replace(' ', '_')}_API_KEY" for system in agent_info["systems"][:2]],
            "integrations": agent_info["systems"]
        },
        "components": [
            {
                "name": f"{agent_info['name']}_agent.py",
                "description": agent_info["description"],
                "role": "Primary processing engine"
            }
        ],
        "demo": {
            "available": True,
            "url": f"agents_lab/{sector}/{agent_info['name']}_stack/demos/{agent_info['name']}_demo.html",
            "title": f"{agent_info['display_name']} Interactive Demo",
            "description": f"Interactive demonstration of {agent_info['display_name']} capabilities"
        },
        "useCases": agent_info["use_cases"]
    }
    
    metadata_path = os.path.join(stack_dir, "metadata.json")
    
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Created metadata: {metadata_path}")

def main():
    base_dir = Path("/Users/kodyw/Documents/GitHub/AI-Agent-Templates/agents_lab")
    
    for sector, agents in AGENT_STACKS.items():
        sector_dir = base_dir / sector
        sector_dir.mkdir(exist_ok=True)
        
        for agent_info in agents:
            stack_dir = sector_dir / f"{agent_info['name']}_stack"
            stack_dir.mkdir(exist_ok=True)
            
            # Create agent file
            create_agent_file(stack_dir, agent_info)
            
            # Create demo file
            create_demo_file(stack_dir, agent_info)
            
            # Create metadata file
            create_metadata_file(stack_dir, agent_info, sector)
            
            print(f"✓ Completed: {sector}/{agent_info['name']}_stack")

if __name__ == "__main__":
    main()
    print("\n✅ All agent stacks created successfully!")