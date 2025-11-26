import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../')))

from agents.basic_agent import BasicAgent
from datetime import datetime, timedelta
import json


class D365BaseAgent(BasicAgent):
    """
    Base class for all Dynamics 365-powered agents
    Provides common D365 connectivity and utility methods
    """

    def __init__(self, name, metadata):
        super().__init__(name, metadata)
        self.d365 = None
        self._init_d365_connector()

    def _init_d365_connector(self):
        """Initialize D365 connector (lazy loading)"""
        try:
            sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
            from connectors.d365_connector import D365Connector
            self.d365 = D365Connector()
        except ImportError as e:
            self.d365 = None
            print(f"Warning: Could not initialize D365 connector: {e}")

    def calculate_days_ago(self, days):
        """Calculate date N days ago in ISO format for D365 queries"""
        target_date = datetime.now() - timedelta(days=days)
        return target_date.strftime('%Y-%m-%dT%H:%M:%SZ')

    def calculate_days_between(self, date_str):
        """Calculate days between given date string and now"""
        try:
            if isinstance(date_str, str):
                date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            else:
                date_obj = date_str

            delta = datetime.now(date_obj.tzinfo) - date_obj
            return delta.days
        except:
            return 0

    def format_currency(self, value):
        """Format currency values"""
        if not value:
            return "$0"
        return f"${value:,.0f}"

    def calculate_percentage(self, numerator, denominator):
        """Calculate percentage safely"""
        if not denominator or denominator == 0:
            return 0
        return round((numerator / denominator) * 100, 1)

    def get_risk_level(self, score):
        """Convert numeric score to risk level"""
        if score >= 75:
            return "Low"
        elif score >= 50:
            return "Medium"
        elif score >= 25:
            return "High"
        else:
            return "Critical"

    def get_health_rating(self, score):
        """Convert numeric score to health rating"""
        if score >= 80:
            return "Excellent"
        elif score >= 65:
            return "Good"
        elif score >= 50:
            return "Fair"
        elif score >= 35:
            return "Poor"
        else:
            return "Critical"

    def perform(self, **kwargs):
        """Override in child classes"""
        raise NotImplementedError("Child classes must implement perform() method")
