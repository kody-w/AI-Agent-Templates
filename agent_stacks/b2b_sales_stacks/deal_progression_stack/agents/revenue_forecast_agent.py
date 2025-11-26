import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from agents.d365_base_agent import D365BaseAgent
import json
import random
from datetime import datetime, timedelta


class RevenueForecastAgent(D365BaseAgent):
    """
    Analyzes forecast reliability and predicts deal closure timing
    Compares estimated vs actual patterns, calculates slip rates
    """

    def __init__(self):
        self.name = "RevenueForecastAgent"
        self.metadata = {
            "name": self.name,
            "description": "Analyzes forecast accuracy, predicts deal closure timing, and identifies forecast reliability patterns",
            "parameters": {
                "type": "object",
                "properties": {
                    "forecast_period": {
                        "type": "string",
                        "description": "Forecast period to analyze (e.g., 'Q4 2025')",
                        "default": "Q4 2025"
                    }
                },
                "required": []
            }
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        """Analyze revenue forecast accuracy"""
        forecast_period = kwargs.get('forecast_period', 'Q4 2025')

        try:
            if self.d365 and not self.d365.demo_mode:
                forecast_data = self._analyze_d365_forecast(forecast_period)
            else:
                forecast_data = self._generate_demo_forecast_data(forecast_period)

            return {
                "status": "success",
                "message": f"Forecast analysis complete for {forecast_period}",
                "data": forecast_data
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to analyze forecast: {str(e)}",
                "data": {}
            }

    def _analyze_d365_forecast(self, forecast_period):
        """Analyze forecast from D365 data"""
        return {}

    def _generate_demo_forecast_data(self, forecast_period):
        """Generate realistic demo forecast data"""
        total_pipeline = random.randint(4000000, 6000000)
        weighted_forecast = int(total_pipeline * random.uniform(0.45, 0.55))
        adjusted_forecast = int(weighted_forecast * random.uniform(0.85, 0.95))
        confidence = random.uniform(0.75, 0.85)
        last_quarter_accuracy = random.uniform(0.78, 0.88)

        # Generate deal predictions
        deal_predictions = []
        num_deals = random.randint(8, 12)

        for i in range(num_deals):
            est_value = random.randint(150000, 750000)
            probability = random.randint(60, 90)
            days_slip = random.randint(-5, 25)

            est_close = datetime.now() + timedelta(days=random.randint(10, 60))
            pred_close = est_close + timedelta(days=days_slip)

            slip_risk = "Low" if days_slip < 7 else "Medium" if days_slip < 14 else "High"

            deal = {
                "opportunity_id": f"opp-{random.randint(1000, 9999)}",
                "opportunity_name": f"{random.choice(['Contoso', 'Fabrikam', 'Northwind', 'Adventure Works', 'Wide World'])} {random.choice(['Enterprise Suite', 'Cloud Platform', 'Digital Solution'])}",
                "estimated_value": est_value,
                "estimated_value_formatted": self.format_currency(est_value),
                "current_close_probability": probability,
                "estimated_close_date": est_close.strftime('%Y-%m-%d'),
                "predicted_close_date": pred_close.strftime('%Y-%m-%d'),
                "prediction_confidence": round(random.uniform(0.75, 0.92), 2),
                "slip_risk": slip_risk,
                "factors": {
                    "current_stage": random.choice(["Develop", "Propose", "Close"]),
                    "days_in_stage": random.randint(5, 25),
                    "velocity": random.choice(["Fast", "Normal", "Slow"]),
                    "historical_pattern": self._get_slip_pattern()
                },
                "adjusted_probability": max(50, probability - random.randint(0, 15)),
                "adjusted_value": int(est_value * (max(50, probability - random.randint(0, 15)) / 100))
            }

            deal_predictions.append(deal)

        # Generate accuracy insights
        insights = [
            {
                "insight": f"Deals >${self.format_currency(500000)} slip {random.randint(2, 4)} weeks on average",
                "sample_size": random.randint(20, 30),
                "confidence": round(random.uniform(0.85, 0.92), 2)
            },
            {
                "insight": f"Proposal stage has {random.randint(35, 50)}% slip rate",
                "sample_size": random.randint(50, 80),
                "confidence": round(random.uniform(0.88, 0.95), 2)
            },
            {
                "insight": f"Deals with 2+ competitors close {random.randint(20, 30)}% slower",
                "sample_size": random.randint(25, 40),
                "confidence": round(random.uniform(0.78, 0.86), 2)
            }
        ]

        # Generate recommendations
        recommendations = [
            f"Adjust {forecast_period} forecast down by {random.randint(8, 15)}% based on historical patterns",
            "Focus on accelerating Proposal stage (highest slip rate)",
            f"Increase oversight on deals >{self.format_currency(500000)}",
            "Implement weekly forecast review for high-value opportunities"
        ]

        return {
            "forecast_period": forecast_period,
            "forecast_summary": {
                "total_pipeline_value": total_pipeline,
                "total_pipeline_value_formatted": self.format_currency(total_pipeline),
                "weighted_forecast": weighted_forecast,
                "weighted_forecast_formatted": self.format_currency(weighted_forecast),
                "adjusted_forecast": adjusted_forecast,
                "adjusted_forecast_formatted": self.format_currency(adjusted_forecast),
                "confidence_level": round(confidence, 2),
                "forecast_accuracy": {
                    "last_quarter": round(last_quarter_accuracy, 2),
                    "trend": "Improving" if last_quarter_accuracy > 0.82 else "Stable"
                }
            },
            "deal_predictions": deal_predictions[:5],  # Top 5 deals
            "accuracy_insights": insights,
            "recommendations": recommendations
        }

    def _get_slip_pattern(self):
        """Get realistic slip pattern description"""
        patterns = [
            "Deals in Proposal typically slip 2-3 weeks",
            "Similar deals close on time 65% of the time",
            "High-value deals in this stage slip 40% of the time",
            "Enterprise deals average 2 week delay from estimate"
        ]
        return random.choice(patterns)


if __name__ == "__main__":
    agent = RevenueForecastAgent()
    result = agent.perform(forecast_period="Q4 2025")
    print(json.dumps(result, indent=2))
