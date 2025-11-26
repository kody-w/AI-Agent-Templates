"""
Base connector class for all data source integrations
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from config import Config

class BaseConnector(ABC):
    """
    Abstract base class for all data source connectors

    All connectors must:
    1. Support MOCK mode (for testing with fake data)
    2. Support PRODUCTION mode (for real API calls)
    3. Handle authentication
    4. Handle errors gracefully
    5. Support Power Platform connector tokens
    """

    def __init__(self, connector_token: str = None):
        """
        Initialize connector

        Args:
            connector_token: Optional Power Platform connector token
                            (passed from Copilot Studio via Azure Function)
        """
        self.mode = Config.MODE
        self.connector_token = connector_token or Config.POWER_PLATFORM_CONNECTOR_TOKEN
        self.is_mock = Config.is_mock_mode()

    @abstractmethod
    def authenticate(self) -> bool:
        """
        Authenticate with the data source

        Returns:
            bool: True if authentication successful

        In MOCK mode: Always returns True
        In PRODUCTION mode: Performs real authentication
        """
        pass

    @abstractmethod
    def test_connection(self) -> Dict[str, Any]:
        """
        Test connection to data source

        Returns:
            Dict with status, message, and connection details
        """
        pass

    def _mock_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Wrap mock data in standard response format

        Args:
            data: Mock data to return

        Returns:
            Standardized response dict
        """
        return {
            "status": "success",
            "mode": "mock",
            "data": data,
            "message": "Mock data returned (not from real API)"
        }

    def _production_response(self, data: Dict[str, Any], source: str) -> Dict[str, Any]:
        """
        Wrap production data in standard response format

        Args:
            data: Real API data
            source: Data source name

        Returns:
            Standardized response dict
        """
        return {
            "status": "success",
            "mode": "production",
            "data": data,
            "source": source,
            "message": f"Data retrieved from {source}"
        }

    def _error_response(self, error: str, details: str = None) -> Dict[str, Any]:
        """
        Standard error response

        Args:
            error: Error message
            details: Optional error details

        Returns:
            Standardized error dict
        """
        return {
            "status": "error",
            "mode": self.mode.value,
            "error": error,
            "details": details
        }
