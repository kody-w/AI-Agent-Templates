"""
Configuration for Account Intelligence Stack
Supports MOCK mode (for testing) and PRODUCTION mode (for live data)
"""

import os
from enum import Enum

class Mode(Enum):
    """Execution mode"""
    MOCK = "mock"  # Use fake data for testing
    PRODUCTION = "production"  # Use real API connections

class CRMSystem(Enum):
    """Supported CRM systems"""
    DYNAMICS_365 = "dynamics_365"
    SALESFORCE = "salesforce"
    MONDAY = "monday"
    HUBSPOT = "hubspot"

class Config:
    """
    Global configuration for Account Intelligence Stack

    Environment Variables:
    - MODE: 'mock' or 'production' (default: mock)
    - CRM_SYSTEM: 'dynamics_365', 'salesforce', 'monday', 'hubspot' (default: dynamics_365)
    - DYNAMICS_365_URL: Dynamics 365 organization URL
    - SALESFORCE_INSTANCE_URL: Salesforce instance URL
    - SALESFORCE_API_VERSION: Salesforce API version (default: v58.0)
    - MONDAY_API_URL: Monday.com API URL (default: https://api.monday.com/v2)
    - AZURE_OPENAI_ENDPOINT: Azure OpenAI endpoint
    - AZURE_OPENAI_KEY: Azure OpenAI API key
    - AZURE_OPENAI_DEPLOYMENT: Deployment name (default: gpt-4o)
    - GRAPH_API_CLIENT_ID: Microsoft Graph API client ID
    - GRAPH_API_CLIENT_SECRET: Microsoft Graph API client secret
    - GRAPH_API_TENANT_ID: Azure AD tenant ID
    - AZURE_AI_SEARCH_ENDPOINT: Azure AI Search endpoint
    - AZURE_AI_SEARCH_KEY: Azure AI Search API key
    - LINKEDIN_API_KEY: LinkedIn API key (via Power Platform connector)
    """

    # Execution mode
    MODE = Mode.MOCK if os.getenv('MODE', 'mock').lower() == 'mock' else Mode.PRODUCTION

    # CRM System Selection
    CRM_SYSTEM = CRMSystem(os.getenv('CRM_SYSTEM', 'dynamics_365'))

    # Dynamics 365 Configuration
    DYNAMICS_365_URL = os.getenv('DYNAMICS_365_URL', 'https://org.crm.dynamics.com')
    DYNAMICS_365_CLIENT_ID = os.getenv('DYNAMICS_365_CLIENT_ID', '')
    DYNAMICS_365_CLIENT_SECRET = os.getenv('DYNAMICS_365_CLIENT_SECRET', '')
    DYNAMICS_365_TENANT_ID = os.getenv('DYNAMICS_365_TENANT_ID', '')

    # Salesforce Configuration
    SALESFORCE_INSTANCE_URL = os.getenv('SALESFORCE_INSTANCE_URL', 'https://yourinstance.salesforce.com')
    SALESFORCE_USERNAME = os.getenv('SALESFORCE_USERNAME', '')
    SALESFORCE_PASSWORD = os.getenv('SALESFORCE_PASSWORD', '')
    SALESFORCE_SECURITY_TOKEN = os.getenv('SALESFORCE_SECURITY_TOKEN', '')
    SALESFORCE_API_VERSION = os.getenv('SALESFORCE_API_VERSION', 'v58.0')

    # Monday.com Configuration
    MONDAY_API_URL = os.getenv('MONDAY_API_URL', 'https://api.monday.com/v2')
    MONDAY_API_KEY = os.getenv('MONDAY_API_KEY', '')

    # HubSpot Configuration
    HUBSPOT_API_KEY = os.getenv('HUBSPOT_API_KEY', '')
    HUBSPOT_API_URL = os.getenv('HUBSPOT_API_URL', 'https://api.hubapi.com')

    # Azure OpenAI Configuration
    AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT', '')
    AZURE_OPENAI_KEY = os.getenv('AZURE_OPENAI_KEY', '')
    AZURE_OPENAI_DEPLOYMENT = os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-4o')
    AZURE_OPENAI_API_VERSION = os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-01')
    AZURE_OPENAI_TEMPERATURE = float(os.getenv('AZURE_OPENAI_TEMPERATURE', '0.7'))

    # Microsoft Graph API Configuration
    GRAPH_API_CLIENT_ID = os.getenv('GRAPH_API_CLIENT_ID', '')
    GRAPH_API_CLIENT_SECRET = os.getenv('GRAPH_API_CLIENT_SECRET', '')
    GRAPH_API_TENANT_ID = os.getenv('GRAPH_API_TENANT_ID', '')
    GRAPH_API_SCOPES = ['https://graph.microsoft.com/.default']

    # Azure AI Search Configuration
    AZURE_AI_SEARCH_ENDPOINT = os.getenv('AZURE_AI_SEARCH_ENDPOINT', '')
    AZURE_AI_SEARCH_KEY = os.getenv('AZURE_AI_SEARCH_KEY', '')
    AZURE_AI_SEARCH_INDEX = os.getenv('AZURE_AI_SEARCH_INDEX', 'competitive_intelligence')

    # LinkedIn Configuration (via Power Platform connector)
    LINKEDIN_API_KEY = os.getenv('LINKEDIN_API_KEY', '')
    LINKEDIN_CONNECTOR_URL = os.getenv('LINKEDIN_CONNECTOR_URL', '')  # Power Platform connector endpoint

    # Power Platform Connector Support
    # When Copilot Studio calls Azure Function, it can pass connector tokens
    POWER_PLATFORM_CONNECTOR_TOKEN = os.getenv('POWER_PLATFORM_CONNECTOR_TOKEN', '')

    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    # Cache TTL (seconds)
    CACHE_TTL_ACCOUNT_DATA = int(os.getenv('CACHE_TTL_ACCOUNT_DATA', '900'))  # 15 minutes
    CACHE_TTL_STAKEHOLDER_DATA = int(os.getenv('CACHE_TTL_STAKEHOLDER_DATA', '3600'))  # 1 hour
    CACHE_TTL_COMPETITIVE_DATA = int(os.getenv('CACHE_TTL_COMPETITIVE_DATA', '14400'))  # 4 hours

    @classmethod
    def is_mock_mode(cls) -> bool:
        """Check if running in mock mode"""
        return cls.MODE == Mode.MOCK

    @classmethod
    def is_production_mode(cls) -> bool:
        """Check if running in production mode"""
        return cls.MODE == Mode.PRODUCTION

    @classmethod
    def get_crm_config(cls):
        """Get configuration for the selected CRM system"""
        if cls.CRM_SYSTEM == CRMSystem.DYNAMICS_365:
            return {
                'type': 'dynamics_365',
                'url': cls.DYNAMICS_365_URL,
                'client_id': cls.DYNAMICS_365_CLIENT_ID,
                'client_secret': cls.DYNAMICS_365_CLIENT_SECRET,
                'tenant_id': cls.DYNAMICS_365_TENANT_ID
            }
        elif cls.CRM_SYSTEM == CRMSystem.SALESFORCE:
            return {
                'type': 'salesforce',
                'instance_url': cls.SALESFORCE_INSTANCE_URL,
                'username': cls.SALESFORCE_USERNAME,
                'password': cls.SALESFORCE_PASSWORD,
                'security_token': cls.SALESFORCE_SECURITY_TOKEN,
                'api_version': cls.SALESFORCE_API_VERSION
            }
        elif cls.CRM_SYSTEM == CRMSystem.MONDAY:
            return {
                'type': 'monday',
                'api_url': cls.MONDAY_API_URL,
                'api_key': cls.MONDAY_API_KEY
            }
        elif cls.CRM_SYSTEM == CRMSystem.HUBSPOT:
            return {
                'type': 'hubspot',
                'api_url': cls.HUBSPOT_API_URL,
                'api_key': cls.HUBSPOT_API_KEY
            }
        else:
            raise ValueError(f"Unsupported CRM system: {cls.CRM_SYSTEM}")

    @classmethod
    def validate_production_config(cls):
        """Validate that all required production configuration is present"""
        if cls.is_mock_mode():
            return True  # No validation needed in mock mode

        errors = []

        # Validate CRM configuration
        crm_config = cls.get_crm_config()
        if cls.CRM_SYSTEM == CRMSystem.DYNAMICS_365:
            if not crm_config['client_id'] or not crm_config['client_secret']:
                errors.append("Dynamics 365 credentials not configured")
        elif cls.CRM_SYSTEM == CRMSystem.SALESFORCE:
            if not crm_config['username'] or not crm_config['password']:
                errors.append("Salesforce credentials not configured")
        elif cls.CRM_SYSTEM == CRMSystem.MONDAY:
            if not crm_config['api_key']:
                errors.append("Monday.com API key not configured")

        # Validate Azure OpenAI
        if not cls.AZURE_OPENAI_ENDPOINT or not cls.AZURE_OPENAI_KEY:
            errors.append("Azure OpenAI not configured")

        # Validate Microsoft Graph
        if not cls.GRAPH_API_CLIENT_ID or not cls.GRAPH_API_CLIENT_SECRET:
            errors.append("Microsoft Graph API not configured")

        # Validate Azure AI Search
        if not cls.AZURE_AI_SEARCH_ENDPOINT or not cls.AZURE_AI_SEARCH_KEY:
            errors.append("Azure AI Search not configured")

        if errors:
            raise ValueError(f"Production configuration errors: {', '.join(errors)}")

        return True


# Print configuration on import (for debugging)
if __name__ == "__main__":
    print(f"Mode: {Config.MODE.value}")
    print(f"CRM System: {Config.CRM_SYSTEM.value}")
    print(f"Mock Mode: {Config.is_mock_mode()}")
    print(f"Production Mode: {Config.is_production_mode()}")
