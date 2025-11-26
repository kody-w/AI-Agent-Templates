import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from agents.d365_base_agent import D365BaseAgent
import json
import random


class CompetitorIntelligenceAgent(D365BaseAgent):
    """
    Identifies and analyzes competitor presence in deals
    Provides competitive insights and win strategies
    """

    def __init__(self):
        self.name = "CompetitorIntelligenceAgent"
        self.metadata = {
            "name": self.name,
            "description": "Analyzes competitive landscape, identifies competitor presence, and recommends positioning strategies",
            "parameters": {
                "type": "object",
                "properties": {
                    "opportunity_id": {
                        "type": "string",
                        "description": "D365 opportunity ID to analyze"
                    },
                    "include_landscape": {
                        "type": "boolean",
                        "description": "Include overall competitive landscape analysis",
                        "default": True
                    }
                },
                "required": []
            }
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        """Analyze competitive intelligence"""
        opportunity_id = kwargs.get('opportunity_id')
        include_landscape = kwargs.get('include_landscape', True)

        try:
            if self.d365 and not self.d365.demo_mode and opportunity_id:
                # Real D365 query
                competitive_data = self._analyze_d365_competitors(opportunity_id, include_landscape)
            else:
                # Demo mode
                competitive_data = self._generate_demo_competitive_data(include_landscape)

            return {
                "status": "success",
                "message": "Competitive intelligence analysis complete",
                "data": competitive_data
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to analyze competitors: {str(e)}",
                "data": {}
            }

    def _analyze_d365_competitors(self, opportunity_id, include_landscape):
        """Analyze competitors from D365 data"""
        return {}

    def _generate_demo_competitive_data(self, include_landscape):
        """Generate realistic demo competitive data"""
        competitors_db = [
            {
                "name": "Salesforce",
                "strengths": ["Brand recognition", "Ecosystem", "Features"],
                "weaknesses": ["Price", "Complexity", "Implementation time"],
                "positioning": "Better TCO, faster implementation, superior support"
            },
            {
                "name": "HubSpot",
                "strengths": ["Ease of use", "Marketing tools", "Price"],
                "weaknesses": ["Enterprise features", "Scalability", "Advanced reporting"],
                "positioning": "Enterprise capabilities, better analytics, advanced automation"
            },
            {
                "name": "Microsoft Dynamics",
                "strengths": ["M365 integration", "Enterprise support", "Customization"],
                "weaknesses": ["Learning curve", "Cost", "Implementation complexity"],
                "positioning": "Specialized industry solutions, faster time-to-value, dedicated support"
            }
        ]

        # Generate competitive landscape
        competitor_analysis = []
        for comp in random.sample(competitors_db, random.randint(2, 3)):
            deals_present = random.randint(5, 15)
            total_value = random.randint(1000000, 5000000)

            competitor_analysis.append({
                "competitor_name": comp["name"],
                "deals_present": deals_present,
                "total_value": total_value,
                "total_value_formatted": self.format_currency(total_value),
                "win_rate_against": round(random.uniform(0.40, 0.75), 2),
                "avg_deal_size": total_value // deals_present,
                "avg_deal_size_formatted": self.format_currency(total_value // deals_present),
                "common_strengths": comp["strengths"],
                "common_weaknesses": comp["weaknesses"],
                "our_positioning": comp["positioning"]
            })

        # Generate active competitive deals
        active_deals = []
        for i in range(random.randint(2, 4)):
            competitors = random.sample([c["competitor_name"] for c in competitor_analysis],
                                       random.randint(1, 2))

            deal = {
                "opportunity_id": f"opp-{random.randint(1000, 9999)}",
                "opportunity_name": f"{random.choice(['Contoso', 'Fabrikam', 'Northwind', 'Adventure Works'])} {random.choice(['Cloud Suite', 'Digital Platform', 'Enterprise System'])}",
                "value": random.randint(200000, 800000),
                "value_formatted": self.format_currency(random.randint(200000, 800000)),
                "stage": random.choice(["Develop", "Propose", "Close"]),
                "competitors": competitors,
                "competitive_strategy": self._get_competitive_strategy(competitors),
                "recommended_actions": self._get_competitive_actions(competitors)
            }
            active_deals.append(deal)

        result = {}

        if include_landscape:
            total_deals = sum(c["deals_present"] for c in competitor_analysis)
            total_value = sum(c["total_value"] for c in competitor_analysis)

            result["competitive_landscape"] = {
                "total_deals_with_competition": total_deals,
                "total_competitive_value": total_value,
                "total_competitive_value_formatted": self.format_currency(total_value)
            }
            result["competitor_analysis"] = competitor_analysis

        result["active_competitive_deals"] = active_deals

        return result

    def _get_competitive_strategy(self, competitors):
        """Get competitive strategy based on competitors"""
        strategies = {
            "Salesforce": "Emphasize integration capabilities, TCO advantage, and faster implementation",
            "HubSpot": "Focus on enterprise scalability, advanced features, and long-term platform stability",
            "Microsoft Dynamics": "Highlight specialized industry solutions and superior support model"
        }

        primary_competitor = competitors[0] if competitors else "General"
        return strategies.get(primary_competitor, "Position on value, implementation speed, and customer success")

    def _get_competitive_actions(self, competitors):
        """Get recommended actions for competitive deal"""
        actions = [
            "Share TCO calculator demonstrating 5-year cost savings",
            "Provide customer references in similar industry facing same competition",
            "Schedule technical comparison session highlighting key differentiators"
        ]

        if "Salesforce" in competitors:
            actions.append("Emphasize implementation timeline - show 3-month vs 9-month advantage")

        if "HubSpot" in competitors:
            actions.append("Demo advanced enterprise features not available in competitor solution")

        return actions[:3]


if __name__ == "__main__":
    agent = CompetitorIntelligenceAgent()
    result = agent.perform(include_landscape=True)
    print(json.dumps(result, indent=2))
