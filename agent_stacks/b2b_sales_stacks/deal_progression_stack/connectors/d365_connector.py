import os
import requests
from datetime import datetime, timedelta
import json

class D365Connector:
    """
    Dynamics 365 Sales API Connector
    Handles authentication and API calls to Dynamics 365 Sales
    """

    def __init__(self):
        self.client_id = os.environ.get('DYNAMICS_365_CLIENT_ID')
        self.client_secret = os.environ.get('DYNAMICS_365_CLIENT_SECRET')
        self.tenant_id = os.environ.get('DYNAMICS_365_TENANT_ID')
        self.resource_url = os.environ.get('DYNAMICS_365_RESOURCE')

        if not all([self.client_id, self.client_secret, self.tenant_id, self.resource_url]):
            # For demo/testing purposes, initialize without credentials
            self.demo_mode = True
            self.api_base = "https://demo.crm.dynamics.com/api/data/v9.2"
        else:
            self.demo_mode = False
            self.api_base = f"{self.resource_url}/api/data/v9.2"

        self.token = None
        self.token_expiry = None

    def get_token(self):
        """Acquire OAuth token for D365 API"""
        if self.demo_mode:
            return "demo_token"

        if self.token and self.token_expiry > datetime.now():
            return self.token

        try:
            import msal

            authority = f"https://login.microsoftonline.com/{self.tenant_id}"
            app = msal.ConfidentialClientApplication(
                self.client_id,
                authority=authority,
                client_credential=self.client_secret
            )

            result = app.acquire_token_for_client(scopes=[f"{self.resource_url}/.default"])

            if "access_token" in result:
                self.token = result['access_token']
                self.token_expiry = datetime.now() + timedelta(seconds=result['expires_in'] - 60)
                return self.token
            else:
                raise Exception(f"Failed to acquire token: {result.get('error_description')}")
        except ImportError:
            raise Exception("msal library not installed. Install with: pip install msal")

    def query(self, endpoint, params=None):
        """
        Execute OData query against D365 API

        Args:
            endpoint: API endpoint (e.g., 'opportunities', 'accounts')
            params: Dictionary of OData query parameters ($filter, $expand, etc.)

        Returns:
            Dictionary containing response data
        """
        if self.demo_mode:
            return {"value": [], "demo_mode": True}

        headers = {
            'Authorization': f'Bearer {self.get_token()}',
            'OData-MaxVersion': '4.0',
            'OData-Version': '4.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Prefer': 'odata.include-annotations="*"'
        }

        url = f"{self.api_base}/{endpoint}"

        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                # Token expired, refresh and retry
                self.token = None
                headers['Authorization'] = f'Bearer {self.get_token()}'
                response = requests.get(url, headers=headers, params=params, timeout=30)

                if response.status_code == 200:
                    return response.json()
                else:
                    raise Exception(f"Query failed after token refresh: {response.status_code} - {response.text}")
            else:
                raise Exception(f"Query failed: {response.status_code} - {response.text}")

        except requests.exceptions.Timeout:
            raise Exception("Request timed out after 30 seconds")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    def query_opportunities(self, filter_str=None, expand=None, select=None, orderby=None, top=None):
        """
        Query opportunities with common parameters

        Args:
            filter_str: OData filter expression
            expand: Related entities to expand
            select: Fields to select
            orderby: Sort order
            top: Limit number of results

        Returns:
            Dictionary containing opportunity data
        """
        params = {}
        if filter_str:
            params['$filter'] = filter_str
        if expand:
            params['$expand'] = expand
        if select:
            params['$select'] = select
        if orderby:
            params['$orderby'] = orderby
        if top:
            params['$top'] = top

        return self.query('opportunities', params)

    def query_activities(self, activity_type, filter_str=None, expand=None, select=None, orderby=None, top=None):
        """
        Query activities (tasks, appointments, phonecalls, emails)

        Args:
            activity_type: Type of activity ('tasks', 'appointments', 'phonecalls', 'emails')
            filter_str: OData filter expression
            expand: Related entities to expand
            select: Fields to select
            orderby: Sort order
            top: Limit number of results

        Returns:
            Dictionary containing activity data
        """
        params = {}
        if filter_str:
            params['$filter'] = filter_str
        if expand:
            params['$expand'] = expand
        if select:
            params['$select'] = select
        if orderby:
            params['$orderby'] = orderby
        if top:
            params['$top'] = top

        return self.query(activity_type, params)

    def query_accounts(self, filter_str=None, expand=None, select=None, orderby=None, top=None):
        """Query account records"""
        params = {}
        if filter_str:
            params['$filter'] = filter_str
        if expand:
            params['$expand'] = expand
        if select:
            params['$select'] = select
        if orderby:
            params['$orderby'] = orderby
        if top:
            params['$top'] = top

        return self.query('accounts', params)

    def query_contacts(self, filter_str=None, expand=None, select=None, orderby=None, top=None):
        """Query contact records"""
        params = {}
        if filter_str:
            params['$filter'] = filter_str
        if expand:
            params['$expand'] = expand
        if select:
            params['$select'] = select
        if orderby:
            params['$orderby'] = orderby
        if top:
            params['$top'] = top

        return self.query('contacts', params)

    def get_opportunity_by_id(self, opportunity_id, expand=None, select=None):
        """
        Get single opportunity by ID

        Args:
            opportunity_id: GUID of opportunity
            expand: Related entities to expand
            select: Fields to select

        Returns:
            Dictionary containing opportunity data
        """
        params = {}
        if expand:
            params['$expand'] = expand
        if select:
            params['$select'] = select

        return self.query(f'opportunities({opportunity_id})', params)

    def calculate_date_filter(self, days_ago):
        """
        Generate date filter for queries

        Args:
            days_ago: Number of days in the past

        Returns:
            ISO formatted date string for use in OData filters
        """
        target_date = datetime.now() - timedelta(days=days_ago)
        return target_date.strftime('%Y-%m-%dT%H:%M:%SZ')


if __name__ == "__main__":
    # Test the connector
    connector = D365Connector()

    if connector.demo_mode:
        print("Running in demo mode (no credentials configured)")
        print("To use live data, set environment variables:")
        print("  DYNAMICS_365_CLIENT_ID")
        print("  DYNAMICS_365_CLIENT_SECRET")
        print("  DYNAMICS_365_TENANT_ID")
        print("  DYNAMICS_365_RESOURCE")
    else:
        print("Connector initialized with credentials")
        print(f"API Base: {connector.api_base}")

        # Test query
        try:
            result = connector.query_opportunities(
                select="name,estimatedvalue,closeprobability",
                top=5
            )
            print(f"Successfully queried opportunities: {len(result.get('value', []))} records")
        except Exception as e:
            print(f"Query failed: {str(e)}")
