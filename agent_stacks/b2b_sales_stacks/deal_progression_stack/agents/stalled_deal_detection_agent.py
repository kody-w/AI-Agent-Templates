import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from agents.d365_base_agent import D365BaseAgent
import json
from datetime import datetime, timedelta


class StalledDealDetectionAgent(D365BaseAgent):
    """
    Identifies opportunities with no recent activity
    Queries D365 for stalled deals based on last modification date and activity history
    """

    def __init__(self):
        self.name = "StalledDealDetectionAgent"
        self.metadata = {
            "name": self.name,
            "description": "Identifies stalled deals with no recent activity and calculates risk metrics",
            "parameters": {
                "type": "object",
                "properties": {
                    "days_threshold": {
                        "type": "integer",
                        "description": "Number of days without activity to consider a deal stalled",
                        "default": 14
                    },
                    "min_value": {
                        "type": "integer",
                        "description": "Minimum deal value to include in analysis",
                        "default": 0
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of stalled deals to return",
                        "default": 50
                    }
                },
                "required": []
            }
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        """Execute stalled deal detection"""
        days_threshold = kwargs.get('days_threshold', 14)
        min_value = kwargs.get('min_value', 0)
        max_results = kwargs.get('max_results', 50)

        try:
            if self.d365 and not self.d365.demo_mode:
                # Real D365 query
                cutoff_date = self.calculate_days_ago(days_threshold)

                filter_str = f"statecode eq 0 and modifiedon lt {cutoff_date}"
                if min_value > 0:
                    filter_str += f" and estimatedvalue ge {min_value}"

                result = self.d365.query_opportunities(
                    filter_str=filter_str,
                    expand="customerid_account($select=name),ownerid($select=fullname)",
                    select="name,estimatedvalue,closeprobability,stepname,modifiedon,estimatedclosedate",
                    orderby="modifiedon asc",
                    top=max_results
                )

                opportunities = result.get('value', [])
                stalled_deals = self._process_opportunities(opportunities, days_threshold)

            else:
                # Demo mode with realistic sample data
                stalled_deals = self._generate_demo_data(days_threshold, max_results)

            # Calculate summary metrics
            summary = self._calculate_summary(stalled_deals)

            return {
                "status": "success",
                "message": f"Found {len(stalled_deals)} stalled deals (no activity in {days_threshold}+ days)",
                "data": {
                    "stalled_deals": stalled_deals,
                    "summary": summary,
                    "query_parameters": {
                        "days_threshold": days_threshold,
                        "min_value": min_value,
                        "max_results": max_results
                    }
                }
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to detect stalled deals: {str(e)}",
                "data": {}
            }

    def _process_opportunities(self, opportunities, days_threshold):
        """Process D365 opportunity data into stalled deal format"""
        stalled_deals = []

        for opp in opportunities:
            days_stalled = self.calculate_days_between(opp.get('modifiedon'))

            deal = {
                "opportunity_id": opp.get('opportunityid'),
                "name": opp.get('name'),
                "value": opp.get('estimatedvalue', 0),
                "value_formatted": self.format_currency(opp.get('estimatedvalue', 0)),
                "days_stalled": days_stalled,
                "current_stage": opp.get('stepname', 'Unknown'),
                "last_activity": opp.get('modifiedon', ''),
                "estimated_close_date": opp.get('estimatedclosedate', ''),
                "owner": opp.get('_ownerid_value@OData.Community.Display.V1.FormattedValue', 'Unknown'),
                "account": opp.get('_customerid_value@OData.Community.Display.V1.FormattedValue', 'Unknown'),
                "close_probability": opp.get('closeprobability', 0),
                "risk_level": self._calculate_risk_level(days_stalled, opp.get('estimatedvalue', 0))
            }

            stalled_deals.append(deal)

        return stalled_deals

    def _calculate_risk_level(self, days_stalled, value):
        """Calculate risk level based on stall duration and deal value"""
        if days_stalled >= 30 and value >= 250000:
            return "Critical"
        elif days_stalled >= 21 or value >= 500000:
            return "High"
        elif days_stalled >= 14:
            return "Medium"
        else:
            return "Low"

    def _calculate_summary(self, stalled_deals):
        """Calculate summary metrics"""
        if not stalled_deals:
            return {
                "total_stalled": 0,
                "total_value_at_risk": 0,
                "total_value_at_risk_formatted": "$0",
                "avg_days_stalled": 0,
                "risk_breakdown": {
                    "Critical": 0,
                    "High": 0,
                    "Medium": 0,
                    "Low": 0
                }
            }

        total_value = sum(deal['value'] for deal in stalled_deals)
        avg_days = sum(deal['days_stalled'] for deal in stalled_deals) / len(stalled_deals)

        risk_breakdown = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
        for deal in stalled_deals:
            risk_breakdown[deal['risk_level']] += 1

        return {
            "total_stalled": len(stalled_deals),
            "total_value_at_risk": total_value,
            "total_value_at_risk_formatted": self.format_currency(total_value),
            "avg_days_stalled": round(avg_days, 1),
            "risk_breakdown": risk_breakdown
        }

    def _generate_demo_data(self, days_threshold, max_results):
        """Generate realistic demo data"""
        import random

        demo_accounts = [
            "Contoso Electronics", "Fabrikam Industries", "Adventure Works",
            "Wide World Importers", "Northwind Traders", "Tailspin Toys",
            "Proseware Inc", "Fourth Coffee", "Woodgrove Bank", "Blue Yonder Airlines"
        ]

        demo_stages = ["Qualify", "Develop", "Propose", "Close"]
        demo_owners = ["Sarah Johnson", "Mike Chen", "Emily Rodriguez", "David Kim", "Lisa Anderson"]

        stalled_deals = []
        num_deals = min(random.randint(8, 15), max_results)

        for i in range(num_deals):
            days_stalled = random.randint(days_threshold, 45)
            value = random.randint(50000, 1000000)

            deal = {
                "opportunity_id": f"opp-{random.randint(1000, 9999)}",
                "name": f"{random.choice(demo_accounts)} {random.choice(['Enterprise Suite', 'Cloud Migration', 'Digital Platform', 'CRM Implementation', 'Data Analytics'])}",
                "value": value,
                "value_formatted": self.format_currency(value),
                "days_stalled": days_stalled,
                "current_stage": random.choice(demo_stages),
                "last_activity": (datetime.now() - timedelta(days=days_stalled)).strftime('%Y-%m-%d'),
                "estimated_close_date": (datetime.now() + timedelta(days=random.randint(10, 60))).strftime('%Y-%m-%d'),
                "owner": random.choice(demo_owners),
                "account": random.choice(demo_accounts),
                "close_probability": random.randint(30, 85),
                "risk_level": self._calculate_risk_level(days_stalled, value)
            }

            stalled_deals.append(deal)

        # Sort by risk level and value
        risk_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
        stalled_deals.sort(key=lambda x: (risk_order[x['risk_level']], -x['value']))

        return stalled_deals


if __name__ == "__main__":
    agent = StalledDealDetectionAgent()

    # Test execution
    result = agent.perform(days_threshold=14, max_results=10)
    print(json.dumps(result, indent=2))
