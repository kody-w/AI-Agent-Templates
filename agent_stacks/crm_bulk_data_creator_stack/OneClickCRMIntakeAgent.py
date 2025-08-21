import json
import os
import requests
import time
from urllib.parse import quote_plus
from agents.basic_agent import BasicAgent

class OneClickCRMIntakeAgent(BasicAgent):
    def __init__(self):
        self.name = "OneClickCRMIntakeAgent"
        self.metadata = {
            "name": self.name,
            "description": "Generic CRM data insertion engine that creates interconnected Dynamics 365 records based entirely on caller-provided data. Creates accounts, contacts, opportunities, cases, and connections using the provided field mappings and values. Automatically fills in additional realistic details to make records look complete.",
            "parameters": {
                "type": "object",
                "properties": {
                    "account_data": {
                        "type": "string",
                        "description": "JSON string containing account fields and values. ACCOUNT FIELD REFERENCE: Core fields: 'name' (string, required), 'description' (string), 'websiteurl' (string, full URL), 'telephone1' (string), 'fax' (string), 'emailaddress1' (string), 'address1_line1' (string), 'address1_city' (string), 'address1_stateorprovince' (string), 'address1_postalcode' (string), 'address1_country' (string). Business fields: 'revenue' (decimal), 'numberofemployees' (integer), 'sic' (string), 'tickersymbol' (string). Option sets: 'accountcategorycode' (1=Preferred Customer, 2=Standard), 'customertypecode' (1=Competitor, 2=Consultant, 3=Customer, 4=Investor, 5=Partner, 6=Influencer, 7=Press, 8=Prospect, 9=Reseller, 10=Supplier, 11=Vendor, 12=Other), 'industrycode' (1=Accounting, 2=Agriculture, 3=Broadcasting, 4=Consulting, 5=Education, 6=Government, 7=Manufacturing, 8=Financial Services, etc). Example: '{\"name\": \"TechCorp Inc\", \"description\": \"Technology consulting\", \"websiteurl\": \"https://techcorp.com\", \"telephone1\": \"+1-555-0123\", \"customertypecode\": 3, \"industrycode\": 4}'"
                    },
                    "contacts_data": {
                        "type": "string",
                        "description": "JSON string containing array of contact records. CONTACT FIELD REFERENCE: Core fields: 'firstname' (string), 'lastname' (string), 'fullname' (string, auto-calculated), 'jobtitle' (string), 'emailaddress1' (string), 'telephone1' (string), 'mobilephone' (string), 'fax' (string). Address fields: 'address1_line1' (string), 'address1_city' (string), 'address1_stateorprovince' (string), 'address1_postalcode' (string), 'address1_country' (string). Business fields: 'department' (string), 'managername' (string), 'assistantname' (string), 'spousesname' (string), 'birthdate' (date: YYYY-MM-DD), 'anniversary' (date: YYYY-MM-DD). Option sets: 'gendercode' (1=Male, 2=Female), 'familystatuscode' (1=Single, 2=Married, 3=Divorced, 4=Widowed), 'preferredcontactmethodcode' (1=Any, 2=Email, 3=Phone, 4=Fax, 5=Mail), 'leadsourcecode' (1=Advertisement, 2=Employee Referral, 3=External Referral, 4=Partner, 5=Public Relations, 6=Seminar, 7=Trade Show, 8=Web, 9=Word of Mouth, 10=Other). Example: '[{\"firstname\": \"John\", \"lastname\": \"Smith\", \"jobtitle\": \"Manager\", \"emailaddress1\": \"john@example.com\", \"gendercode\": 1, \"preferredcontactmethodcode\": 2}]'"
                    },
                    "opportunities_data": {
                        "type": "string",
                        "description": "JSON string containing array of opportunity records. OPPORTUNITY FIELD REFERENCE: Core fields: 'name' (string, required), 'description' (string), 'estimatedvalue' (decimal), 'actualvalue' (decimal), 'budgetamount' (decimal), 'estimatedclosedate' (date: YYYY-MM-DD), 'actualclosedate' (date: YYYY-MM-DD), 'closeprobability' (integer, 0-100%). Business fields: 'customerneed' (string), 'proposedsolution' (string), 'currentsituation' (string), 'qualificationcomments' (string), 'quotecomments' (string). Option sets: 'prioritycode' (1=High - NOTE: Some environments only accept value 1), 'salesstagecode' (1=Develop - NOTE: Some environments only accept value 1, not 0), 'statuscode' (1=In Progress, 2=On Hold, 3=Won, 4=Canceled, 5=Out-Sold), 'budgetstatus' (0=No Committed Budget, 1=May Buy, 2=Can Buy, 3=Will Buy), 'purchaseprocess' (0=Individual, 1=Committee, 2=Unknown), 'purchasetimeframe' (0=Immediate, 1=This Quarter, 2=Next Quarter, 3=This Year, 4=Unknown), 'need' (0=Must have, 1=Should have, 2=Good to have, 3=No need), 'timeline' (0=Immediate, 1=This Quarter, 2=Next Quarter, 3=This Year, 4=Unknown), 'opportunityratingcode' (1=Hot, 2=Warm, 3=Cold). Boolean fields: 'confirminterest' (true/false), 'decisionmaker' (true/false), 'pursuitdecision' (true/false). IMPORTANT: If you get validation errors about option set values, use only the accepted values shown in the error message. Example: '[{\"name\": \"Q4 Software Deal\", \"estimatedvalue\": 250000, \"estimatedclosedate\": \"2025-12-31\", \"prioritycode\": 1, \"salesstagecode\": 1, \"budgetstatus\": 2, \"closeprobability\": 75}]'"
                    },
                    "cases_data": {
                        "type": "string",
                        "description": "JSON string containing array of case/incident records. CASE FIELD REFERENCE: Core fields: 'title' (string, required), 'description' (string), 'ticketnumber' (string, auto-generated if blank). Option sets: 'prioritycode' (1=High - NOTE: Some environments only accept value 1), 'severitycode' (1=High - NOTE: Some environments only accept value 1), 'casetypecode' (1=Question, 2=Problem, 3=Request), 'caseorigincode' (1=Phone, 2=Email, 3=Web, 4=Facebook, 5=Twitter), 'statecode' (0=Active, 1=Resolved, 2=Canceled), 'statuscode' varies by state (Active: 1=In Progress, 2=On Hold, 5=Waiting for Details, 1000=Information Provided; Resolved: 5=Problem Solved, 1000=Information Provided; Canceled: 6=Canceled, 2000=Merged). Date fields: 'createdon' (datetime: YYYY-MM-DDTHH:MM:SSZ), 'modifiedon' (datetime), 'followupby' (datetime), 'resolveby' (datetime). IMPORTANT: Do NOT use 'customercontactname' or 'existingcase' as these fields either don't exist or require complex object references. The customerid linkage is handled automatically by the agent. Example: '[{\"title\": \"Login Issue\", \"description\": \"User cannot access system\", \"prioritycode\": 1, \"severitycode\": 1, \"casetypecode\": 2, \"caseorigincode\": 2}]'"
                    },
                    "system_user_search": {
                        "type": "string",
                        "description": "Partial name to search for system users to assign to opportunities and create connections. Example: 'Jean-Paul' will find users with names containing that text. SYSTEM USER SEARCH: The search uses 'contains' filter on the 'fullname' field. Common system user fields returned: 'systemuserid' (GUID), 'fullname' (string), 'domainname' (string), 'internalemailaddress' (string), 'title' (string). Active users only are returned by default."
                    },
                    "connection_role_ids": {
                        "type": "string",
                        "description": "JSON string containing connection role GUIDs for creating user-opportunity connections. CONNECTION ROLES REFERENCE: Common built-in connection roles include Sales Team, Account Manager, Influencer, Decision Maker, etc. Format: '{\"record1_role\": \"GUID\", \"record2_role\": \"GUID\"}' where record1_role is for the opportunity side and record2_role is for the user side. To find role GUIDs, query: /connectionroles?$select=connectionroleid,name,category. Categories: 1=Business (Stakeholder, Decision Maker), 2=Family, 3=Social, 4=Sales (Sales Team, Account Manager), 5=Other, 6=Stakeholder, 7=Sales Team. If not provided, connections will be created without specific roles."
                    },
                    "dynamics_base_url": {
                        "type": "string",
                        "description": "Base URL for Dynamics links generation (without /api/data/v9.2). URL FORMAT: 'https://[org].crm[region].dynamics.com' where [org] is your organization unique name and [region] is geographic region (blank for North America, .crm2 for South America, .crm3 for Canada, .crm4 for Europe/Africa, .crm5 for Asia Pacific, .crm6 for Oceania, .crm7 for Japan, .crm8 for India, .crm9 for North America 2). Example: 'https://contoso.crm.dynamics.com'. If not provided, uses DYNAMICS_365_RESOURCE environment variable."
                    },
                    "app_id": {
                        "type": "string", 
                        "description": "Dynamics 365 app ID for link generation. APP ID REFERENCE: This is the unique identifier for the Dynamics 365 app that determines the interface and available features when opening records. Common app IDs: Sales Hub='f8fabdac-0f25-f011-8c4d-6045bdff5943', Customer Service Hub='d8fc1185-3c04-f011-bae4-7c1e527db3bb', Field Service='cf9d4df6-d2f3-4f46-964f-92ba1969daba', Project Service Automation='6a8b2d6e-d2c9-4e91-9b26-9d2b9244c8b5'. Default: 'd8fc1185-3c04-f011-bae4-7c1e527db3bb' (Customer Service Hub). To find your custom app IDs, query: /appmodules?$select=appmoduleid,name,description."
                    },
                    "currency_code": {
                        "type": "string",
                        "description": "ISO currency code for monetary fields (estimatedvalue, budgetamount, etc.). CURRENCY REFERENCE: Common codes: 'USD' (US Dollar), 'EUR' (Euro), 'GBP' (British Pound), 'CAD' (Canadian Dollar), 'AUD' (Australian Dollar), 'JPY' (Japanese Yen), 'INR' (Indian Rupee), 'CNY' (Chinese Yuan). If provided, will bind to transaction currency: 'transactioncurrencyid@odata.bind' with value '/transactioncurrencies(currencycode='{code}')'. If not provided, uses organization default currency."
                    },
                    "auto_fill_details": {
                        "type": "boolean",
                        "description": "Whether to automatically fill in additional string and number fields to make records look complete. When true, the agent will populate fields like addresses, phone numbers, descriptions, revenue, employee counts, etc. with realistic values based on the provided core data. Default: true."
                    },
                    "detail_level": {
                        "type": "string",
                        "description": "Level of detail to add when auto_fill_details is true. OPTIONS: 'minimal' (only core required fields), 'standard' (common business fields), 'comprehensive' (all available string/number fields). Default: 'standard'.",
                        "enum": ["minimal", "standard", "comprehensive"]
                    },
                    "business_theme": {
                        "type": "string", 
                        "description": "Business theme to use for generating realistic field values when auto_fill_details is true. This affects phone numbers, addresses, industry-specific descriptions, etc. OPTIONS: 'technology', 'manufacturing', 'healthcare', 'retail', 'financial', 'consulting', 'generic'. Default: 'generic'."
                    }
                },
                "required": ["account_data", "contacts_data", "opportunities_data", "cases_data"]
            }
        }
        super().__init__(name=self.name, metadata=self.metadata)
        
        # Load Dynamics 365 configuration from environment variables
        self.client_id = os.environ.get('DYNAMICS_365_CLIENT_ID')
        self.client_secret = os.environ.get('DYNAMICS_365_CLIENT_SECRET')
        self.tenant_id = os.environ.get('DYNAMICS_365_TENANT_ID')
        self.resource = os.environ.get('DYNAMICS_365_RESOURCE')
        self.token_url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        self.access_token = None
        self.max_retries = 3
        self.retry_delay = 2

    def authenticate(self):
        """Authenticate with Dynamics 365 using OAuth"""
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': f'{self.resource}/.default',
            'grant_type': 'client_credentials'
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(self.token_url, data=data, headers=headers)
        response.raise_for_status()
        self.access_token = response.json().get('access_token')

    def get_headers(self):
        """Get authentication headers for Dynamics API calls"""
        if not self.access_token:
            self.authenticate()
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'OData-MaxVersion': '4.0',
            'OData-Version': '4.0',
            'Accept': 'application/json'
        }

    def create_dynamics_record(self, entity, data):
        """Create a record in Dynamics 365"""
        url = f"{self.resource}/api/data/v9.2/{entity}"
        response = requests.post(url, headers=self.get_headers(), data=json.dumps(data))
        
        if response.status_code == 204:
            entity_url = response.headers.get('OData-EntityId')
            if entity_url:
                guid = entity_url.split('(')[1].split(')')[0]
                return guid
        elif response.status_code != 204:
            # Return error details for debugging
            return {"error": f"Failed to create {entity}", "status": response.status_code, "details": response.text}
        return None

    def find_system_users(self, name_part):
        """Find system users by partial name match"""
        if not name_part:
            return []
        
        url = f"{self.resource}/api/data/v9.2/systemusers?$filter=contains(fullname,'{name_part}')&$select=fullname,systemuserid"
        response = requests.get(url, headers=self.get_headers())
        if response.status_code == 200:
            data = response.json()
            return data.get('value', [])
        return []

    def find_currency(self, currency_code):
        """Find currency by ISO code"""
        url = f"{self.resource}/api/data/v9.2/transactioncurrencies?$filter=isocurrencycode eq '{currency_code}'&$select=transactioncurrencyid,currencyname"
        response = requests.get(url, headers=self.get_headers())
        if response.status_code == 200:
            data = response.json()
            if data.get('value'):
                return data['value'][0]['transactioncurrencyid']
        return None

    def generate_record_link(self, entity, record_id, base_url, app_id):
        """Generate a Dynamics 365 record link"""
        return f"{base_url}/main.aspx?appid={app_id}&pagetype=entityrecord&etn={entity}&id={record_id}"

    def safe_json_parse(self, json_string, default=None):
        """Safely parse JSON string with fallback"""
        if not json_string:
            return default or {}
        try:
            return json.loads(json_string)
        except (json.JSONDecodeError, TypeError):
            return default or {}

    def enhance_record_data(self, record_data, entity_type, detail_level, business_theme):
        """Enhance record data with additional realistic fields based on parameters"""
        if not record_data:
            return record_data
            
        enhanced = record_data.copy()
        
        # Business theme-specific data generators
        theme_data = {
            'technology': {
                'phone_prefix': '+1-555-01',
                'address_city': 'San Francisco', 
                'address_state': 'CA',
                'website_domain': 'tech-innovate.com',
                'industry_keywords': ['cloud', 'AI', 'software', 'digital transformation', 'automation']
            },
            'manufacturing': {
                'phone_prefix': '+1-555-02',
                'address_city': 'Detroit',
                'address_state': 'MI', 
                'website_domain': 'manufacturing-solutions.com',
                'industry_keywords': ['production', 'assembly', 'quality control', 'logistics', 'efficiency']
            },
            'healthcare': {
                'phone_prefix': '+1-555-03',
                'address_city': 'Boston',
                'address_state': 'MA',
                'website_domain': 'healthcare-systems.com', 
                'industry_keywords': ['patient care', 'medical', 'compliance', 'healthcare', 'wellness']
            },
            'retail': {
                'phone_prefix': '+1-555-04',
                'address_city': 'New York',
                'address_state': 'NY',
                'website_domain': 'retail-solutions.com',
                'industry_keywords': ['customer experience', 'omnichannel', 'inventory', 'sales', 'retail']
            },
            'financial': {
                'phone_prefix': '+1-555-05', 
                'address_city': 'Chicago',
                'address_state': 'IL',
                'website_domain': 'financial-group.com',
                'industry_keywords': ['investment', 'banking', 'financial services', 'compliance', 'risk management']
            },
            'consulting': {
                'phone_prefix': '+1-555-06',
                'address_city': 'Washington',
                'address_state': 'DC',
                'website_domain': 'consulting-experts.com',
                'industry_keywords': ['strategy', 'optimization', 'transformation', 'advisory', 'expertise']
            },
            'generic': {
                'phone_prefix': '+1-555-99',
                'address_city': 'Austin',
                'address_state': 'TX',
                'website_domain': 'business-corp.com',
                'industry_keywords': ['business', 'solutions', 'services', 'professional', 'corporate']
            }
        }
        
        theme = theme_data.get(business_theme, theme_data['generic'])
        
        if entity_type == 'account':
            if detail_level in ['standard', 'comprehensive']:
                # Standard business fields
                if 'telephone1' not in enhanced:
                    enhanced['telephone1'] = f"{theme['phone_prefix']}{str(hash(enhanced.get('name', 'default')) % 100).zfill(2)}"
                if 'fax' not in enhanced:
                    enhanced['fax'] = f"{theme['phone_prefix']}{str(hash(enhanced.get('name', 'default')) % 100 + 10).zfill(2)}"
                if 'websiteurl' not in enhanced and 'name' in enhanced:
                    company_slug = enhanced['name'].lower().replace(' ', '-').replace(',', '').replace('.', '')[:20]
                    enhanced['websiteurl'] = f"https://www.{company_slug}.{theme['website_domain'].split('.')[-1]}"
                if 'emailaddress1' not in enhanced and 'name' in enhanced:
                    company_slug = enhanced['name'].lower().replace(' ', '').replace(',', '').replace('.', '')[:15]
                    enhanced['emailaddress1'] = f"info@{company_slug}.com"
                    
            if detail_level == 'comprehensive':
                # Comprehensive fields
                if 'address1_line1' not in enhanced:
                    street_num = hash(enhanced.get('name', 'default')) % 9999 + 1
                    enhanced['address1_line1'] = f"{street_num} Business Blvd"
                if 'address1_city' not in enhanced:
                    enhanced['address1_city'] = theme['address_city']
                if 'address1_stateorprovince' not in enhanced:
                    enhanced['address1_stateorprovince'] = theme['address_state']
                if 'address1_postalcode' not in enhanced:
                    enhanced['address1_postalcode'] = str(hash(enhanced.get('name', 'default')) % 90000 + 10000)
                if 'address1_country' not in enhanced:
                    enhanced['address1_country'] = 'United States'
                if 'revenue' not in enhanced:
                    enhanced['revenue'] = (hash(enhanced.get('name', 'default')) % 50000000) + 1000000  # 1M to 51M
                if 'numberofemployees' not in enhanced:
                    enhanced['numberofemployees'] = (hash(enhanced.get('name', 'default')) % 1000) + 10  # 10 to 1010
                if 'sic' not in enhanced:
                    enhanced['sic'] = str(hash(enhanced.get('name', 'default')) % 9000 + 1000)  # 4-digit SIC
                    
        elif entity_type == 'contact':
            if detail_level in ['standard', 'comprehensive']:
                # Standard contact fields  
                if 'telephone1' not in enhanced and ('firstname' in enhanced or 'lastname' in enhanced):
                    name_hash = hash(f"{enhanced.get('firstname', '')}{enhanced.get('lastname', '')}")
                    enhanced['telephone1'] = f"{theme['phone_prefix']}{str(name_hash % 100).zfill(2)}"
                if 'mobilephone' not in enhanced:
                    name_hash = hash(f"{enhanced.get('firstname', '')}{enhanced.get('lastname', '')}")
                    enhanced['mobilephone'] = f"+1-555-{str((name_hash % 900) + 100)}-{str((name_hash % 9000) + 1000)}"
                    
            if detail_level == 'comprehensive':
                # Comprehensive contact fields
                if 'address1_line1' not in enhanced:
                    name_hash = hash(f"{enhanced.get('firstname', '')}{enhanced.get('lastname', '')}")
                    street_num = (name_hash % 9999) + 1
                    enhanced['address1_line1'] = f"{street_num} Main St"
                if 'address1_city' not in enhanced:
                    enhanced['address1_city'] = theme['address_city']
                if 'address1_stateorprovince' not in enhanced:
                    enhanced['address1_stateorprovince'] = theme['address_state']
                if 'address1_postalcode' not in enhanced:
                    name_hash = hash(f"{enhanced.get('firstname', '')}{enhanced.get('lastname', '')}")
                    enhanced['address1_postalcode'] = str((name_hash % 90000) + 10000)
                if 'department' not in enhanced:
                    departments = ['Sales', 'Marketing', 'Operations', 'Finance', 'IT', 'HR', 'Engineering']
                    name_hash = hash(f"{enhanced.get('firstname', '')}{enhanced.get('lastname', '')}")
                    enhanced['department'] = departments[name_hash % len(departments)]
                    
        elif entity_type == 'opportunity':
            if detail_level in ['standard', 'comprehensive']:
                # Standard opportunity fields
                if 'customerneed' not in enhanced and 'name' in enhanced:
                    keywords = theme['industry_keywords']
                    keyword = keywords[hash(enhanced['name']) % len(keywords)]
                    enhanced['customerneed'] = f"Client requires comprehensive {keyword} solution to improve operational efficiency"
                if 'currentsituation' not in enhanced:
                    enhanced['currentsituation'] = f"Current systems are outdated and require modernization to meet {business_theme} industry standards"
                    
            if detail_level == 'comprehensive':
                # Comprehensive opportunity fields
                if 'proposedsolution' not in enhanced and 'name' in enhanced:
                    keywords = theme['industry_keywords']
                    keyword = keywords[hash(enhanced['name']) % len(keywords)]
                    enhanced['proposedsolution'] = f"Implement state-of-the-art {keyword} platform with training and ongoing support"
                if 'qualificationcomments' not in enhanced:
                    enhanced['qualificationcomments'] = "Decision maker identified, budget confirmed, timeline established"
                if 'quotecomments' not in enhanced:
                    enhanced['quotecomments'] = "Competitive pricing provided with implementation timeline and ROI projections"
                    
        elif entity_type == 'case':
            if detail_level in ['standard', 'comprehensive']:
                # Standard case fields - only use simple string/date fields
                pass  # No standard fields to add for cases
                    
            if detail_level == 'comprehensive':
                # Comprehensive case fields - using valid incident fields only
                if 'resolveby' not in enhanced:
                    # Add resolve by date (7 days from now)
                    from datetime import datetime, timedelta
                    resolve_date = datetime.now() + timedelta(days=7)
                    enhanced['resolveby'] = resolve_date.strftime('%Y-%m-%d')
                if 'followupby' not in enhanced:
                    # Add follow up date (2 days from now)
                    from datetime import datetime, timedelta
                    followup_date = datetime.now() + timedelta(days=2)
                    enhanced['followupby'] = followup_date.strftime('%Y-%m-%d')
                    
        return enhanced

    def perform(self, **kwargs):
        """Main execution method - Creates all records fresh and handles ALL linking automatically"""
        # Parse input parameters
        account_data = self.safe_json_parse(kwargs.get('account_data'), {})
        contacts_data = self.safe_json_parse(kwargs.get('contacts_data'), [])
        opportunities_data = self.safe_json_parse(kwargs.get('opportunities_data'), [])
        cases_data = self.safe_json_parse(kwargs.get('cases_data'), [])
        connection_role_ids = self.safe_json_parse(kwargs.get('connection_role_ids'), {})
        system_user_search = kwargs.get('system_user_search', '')
        currency_code = kwargs.get('currency_code', '')
        
        # Auto-fill parameters
        auto_fill_details = kwargs.get('auto_fill_details', True)
        detail_level = kwargs.get('detail_level', 'standard')
        business_theme = kwargs.get('business_theme', 'generic')
        
        # URL generation parameters
        base_url = kwargs.get('dynamics_base_url', self.resource.replace('/api/data/v9.2', ''))
        app_id = kwargs.get('app_id', 'd8fc1185-3c04-f011-bae4-7c1e527db3bb')

        results = {
            "created_records": {},
            "links": {},
            "errors": [],
            "summary": {},
            "linking_report": [],
            "auto_fill_applied": auto_fill_details
        }

        try:
            # Currency lookup (if specified)
            currency_id = None
            if currency_code:
                currency_id = self.find_currency(currency_code)
                if currency_id:
                    results["linking_report"].append(f"Found currency {currency_code}: {currency_id}")
                else:
                    results["linking_report"].append(f"Currency {currency_code} not found, using default")

            # STEP 1: Create Account (if data provided)
            account_id = None
            if account_data and len(account_data) > 0:
                # Enhance with additional details if requested
                if auto_fill_details:
                    account_data = self.enhance_record_data(account_data, 'account', detail_level, business_theme)
                    results["linking_report"].append(f"🔧 Enhanced account data with {detail_level} level details using {business_theme} theme")
                
                # Add currency binding if available
                if currency_id:
                    account_data["transactioncurrencyid@odata.bind"] = f"/transactioncurrencies({currency_id})"
                
                account_id = self.create_dynamics_record("accounts", account_data)
                if isinstance(account_id, dict) and 'error' in account_id:
                    results["errors"].append(f"Account creation failed: {account_id}")
                elif account_id:
                    results["created_records"]["account"] = account_id
                    results["links"]["account"] = self.generate_record_link("account", account_id, base_url, app_id)
                    results["linking_report"].append(f"✅ Created account: {account_id}")
            else:
                results["linking_report"].append("⚠️ No account data provided - skipping account creation")

            # STEP 2: Create Contacts (if data provided)
            contact_ids = []
            if contacts_data and len(contacts_data) > 0:
                results["linking_report"].append(f"📋 Processing {len(contacts_data)} contact records...")
                
                for i, contact_template in enumerate(contacts_data):
                    # Create fresh copy to avoid modifying original
                    contact = contact_template.copy()
                    
                    # Enhance with additional details if requested
                    if auto_fill_details:
                        contact = self.enhance_record_data(contact, 'contact', detail_level, business_theme)
                        results["linking_report"].append(f"🔧 Enhanced contact {i+1} data with {detail_level} level details")
                    
                    # AUTO-LINK: Link to created account if available
                    if account_id:
                        contact["parentcustomerid_account@odata.bind"] = f"/accounts({account_id})"
                        results["linking_report"].append(f"🔗 Contact {i+1} will be linked to account {account_id}")
                    
                    # Add currency binding if available
                    if currency_id:
                        contact["transactioncurrencyid@odata.bind"] = f"/transactioncurrencies({currency_id})"
                    
                    contact_id = self.create_dynamics_record("contacts", contact)
                    if isinstance(contact_id, dict) and 'error' in contact_id:
                        results["errors"].append(f"Contact {i+1} creation failed: {contact_id}")
                        results["linking_report"].append(f"❌ Failed to create contact {i+1}: {contact_id}")
                    elif contact_id:
                        contact_ids.append(contact_id)
                        results["linking_report"].append(f"✅ Created contact {i+1}: {contact_id}")

                results["created_records"]["contacts"] = contact_ids
                results["links"]["contacts"] = [
                    self.generate_record_link("contact", cid, base_url, app_id) for cid in contact_ids
                ]
            else:
                results["linking_report"].append("⚠️ No contact data provided - skipping contact creation")

            # STEP 3: Create Opportunities (if data provided)
            opportunity_ids = []
            if opportunities_data and len(opportunities_data) > 0:
                results["linking_report"].append(f"📋 Processing {len(opportunities_data)} opportunity records...")
                
                for i, opp_template in enumerate(opportunities_data):
                    # Create fresh copy to avoid modifying original
                    opportunity = opp_template.copy()
                    
                    # Enhance with additional details if requested
                    if auto_fill_details:
                        opportunity = self.enhance_record_data(opportunity, 'opportunity', detail_level, business_theme)
                        results["linking_report"].append(f"🔧 Enhanced opportunity {i+1} data with {detail_level} level details")
                    
                    # AUTO-LINK: Link to created account if available
                    if account_id:
                        opportunity["parentaccountid@odata.bind"] = f"/accounts({account_id})"
                        results["linking_report"].append(f"🔗 Opportunity {i+1} will be linked to account {account_id}")
                    
                    # AUTO-LINK: Link to contact (round-robin if more opportunities than contacts)
                    if contact_ids and len(contact_ids) > 0:
                        contact_index = i % len(contact_ids)
                        selected_contact = contact_ids[contact_index]
                        opportunity["customerid_contact@odata.bind"] = f"/contacts({selected_contact})"
                        results["linking_report"].append(f"🔗 Opportunity {i+1} will be linked to contact {contact_index+1}: {selected_contact}")
                    
                    # Add currency binding if available
                    if currency_id:
                        opportunity["transactioncurrencyid@odata.bind"] = f"/transactioncurrencies({currency_id})"
                    
                    opportunity_id = self.create_dynamics_record("opportunities", opportunity)
                    if isinstance(opportunity_id, dict) and 'error' in opportunity_id:
                        results["errors"].append(f"Opportunity {i+1} creation failed: {opportunity_id}")
                        results["linking_report"].append(f"❌ Failed to create opportunity {i+1}: {opportunity_id}")
                    elif opportunity_id:
                        opportunity_ids.append(opportunity_id)
                        results["linking_report"].append(f"✅ Created opportunity {i+1}: {opportunity_id}")

                results["created_records"]["opportunities"] = opportunity_ids
                results["links"]["opportunities"] = [
                    self.generate_record_link("opportunity", oid, base_url, app_id) for oid in opportunity_ids
                ]
            else:
                results["linking_report"].append("⚠️ No opportunity data provided - skipping opportunity creation")

            # STEP 4: Create Cases (if data provided)
            case_ids = []
            if cases_data and len(cases_data) > 0:
                results["linking_report"].append(f"📋 Processing {len(cases_data)} case records...")
                
                for i, case_template in enumerate(cases_data):
                    # Create fresh copy to avoid modifying original
                    case = case_template.copy()
                    
                    # Enhance with additional details if requested
                    if auto_fill_details:
                        case = self.enhance_record_data(case, 'case', detail_level, business_theme)
                        results["linking_report"].append(f"🔧 Enhanced case {i+1} data with {detail_level} level details")
                    
                    # AUTO-LINK: Link to contact (round-robin distribution)
                    if contact_ids and len(contact_ids) > 0:
                        contact_index = i % len(contact_ids)
                        selected_contact = contact_ids[contact_index]
                        case["customerid_contact@odata.bind"] = f"/contacts({selected_contact})"
                        results["linking_report"].append(f"🔗 Case {i+1} will be linked to contact {contact_index+1}: {selected_contact}")
                    
                    case_id = self.create_dynamics_record("incidents", case)
                    if isinstance(case_id, dict) and 'error' in case_id:
                        results["errors"].append(f"Case {i+1} creation failed: {case_id}")
                        results["linking_report"].append(f"❌ Failed to create case {i+1}: {case_id}")
                    elif case_id:
                        case_ids.append(case_id)
                        results["linking_report"].append(f"✅ Created case {i+1}: {case_id}")

                results["created_records"]["cases"] = case_ids
                results["links"]["cases"] = [
                    self.generate_record_link("incident", cid, base_url, app_id) for cid in case_ids
                ]
            else:
                results["linking_report"].append("⚠️ No case data provided - skipping case creation")

            # STEP 5: Create System User Connections (if user search provided and opportunities exist)
            connection_ids = []
            system_users_found = []
            if system_user_search and system_user_search.strip() and opportunity_ids and len(opportunity_ids) > 0:
                results["linking_report"].append(f"🔍 Searching for system users matching '{system_user_search}'...")
                system_users_found = self.find_system_users(system_user_search.strip())
                results["linking_report"].append(f"Found {len(system_users_found)} system users matching '{system_user_search}'")
                
                # Create connections: Each found user connected to each opportunity
                if system_users_found and len(system_users_found) > 0:
                    results["linking_report"].append(f"📋 Creating connections: {len(system_users_found)} users × {len(opportunity_ids)} opportunities = {len(system_users_found) * len(opportunity_ids)} connections...")
                    
                    for user in system_users_found:
                        user_id = user.get('systemuserid')
                        user_name = user.get('fullname', 'Unknown')
                        
                        if user_id:
                            for j, opp_id in enumerate(opportunity_ids):
                                connection_data = {
                                    "record1id_opportunity@odata.bind": f"/opportunities({opp_id})",
                                    "record2id_systemuser@odata.bind": f"/systemusers({user_id})"
                                }
                                
                                # Add connection roles if provided
                                if connection_role_ids.get('record1_role'):
                                    connection_data["record1roleid@odata.bind"] = f"/connectionroles({connection_role_ids['record1_role']})"
                                if connection_role_ids.get('record2_role'):
                                    connection_data["record2roleid@odata.bind"] = f"/connectionroles({connection_role_ids['record2_role']})"
                                
                                connection_id = self.create_dynamics_record("connections", connection_data)
                                if isinstance(connection_id, dict) and 'error' in connection_id:
                                    results["errors"].append(f"Connection failed - {user_name} to opportunity {j+1}: {connection_id}")
                                    results["linking_report"].append(f"❌ Failed to connect {user_name} to opportunity {j+1}: {connection_id}")
                                elif connection_id:
                                    connection_ids.append(connection_id)
                                    results["linking_report"].append(f"✅ Connected {user_name} to opportunity {j+1}: {connection_id}")
                else:
                    results["linking_report"].append(f"⚠️ No system users found matching '{system_user_search}' - no connections created")

                results["created_records"]["connections"] = connection_ids
                results["created_records"]["system_users_found"] = system_users_found
            elif not system_user_search or not system_user_search.strip():
                results["linking_report"].append("⚠️ No system user search provided - skipping user connections")
            elif not opportunity_ids or len(opportunity_ids) == 0:
                results["linking_report"].append("⚠️ No opportunities created - cannot create user connections")

            # STEP 6: Generate Comprehensive Summary
            total_created = (1 if account_id else 0) + len(contact_ids) + len(opportunity_ids) + len(case_ids) + len(connection_ids)
            
            summary_parts = [
                f"🏭 FRESH RECORD CREATION COMPLETE - {total_created} total records created"
            ]
            
            if auto_fill_details:
                summary_parts.append(f"🔧 Auto-filled with {detail_level} level details using {business_theme} theme")
            
            if account_id:
                summary_parts.append(f"🏢 Account: 1 created ({account_id})")
            if contact_ids and len(contact_ids) > 0:
                summary_parts.append(f"👥 Contacts: {len(contact_ids)} created, auto-linked to account")
            if opportunity_ids and len(opportunity_ids) > 0:
                summary_parts.append(f"💼 Opportunities: {len(opportunity_ids)} created, auto-linked to account + contacts")
            if case_ids and len(case_ids) > 0:
                summary_parts.append(f"🎫 Cases: {len(case_ids)} created, auto-linked to contacts")
            if connection_ids and len(connection_ids) > 0:
                summary_parts.append(f"🤝 Connections: {len(connection_ids)} created ({len(system_users_found)} users × {len(opportunity_ids)} opportunities)")
            
            if results["errors"] and len(results["errors"]) > 0:
                summary_parts.append(f"⚠️ Errors: {len(results['errors'])} encountered")

            summary_parts.append("🔗 All record relationships handled automatically using fresh GUIDs")

            results["summary"] = {
                "total_records_created": total_created,
                "accounts": 1 if account_id else 0,
                "contacts": len(contact_ids),
                "opportunities": len(opportunity_ids),
                "cases": len(case_ids),
                "connections": len(connection_ids),
                "system_users_found": len(system_users_found),
                "errors": len(results["errors"]),
                "fresh_guids_used": True,
                "auto_linking_applied": True,
                "auto_fill_details": auto_fill_details,
                "detail_level": detail_level,
                "business_theme": business_theme,
                "data_provided": {
                    "account_data": bool(account_data and len(account_data) > 0),
                    "contacts_data": bool(contacts_data and len(contacts_data) > 0),
                    "opportunities_data": bool(opportunities_data and len(opportunities_data) > 0),
                    "cases_data": bool(cases_data and len(cases_data) > 0),
                    "system_user_search": bool(system_user_search and system_user_search.strip())
                },
                "message": "\n".join(summary_parts)
            }

            return json.dumps(results, indent=2)

        except Exception as e:
            results["errors"].append(f"Critical error in fresh record creation: {str(e)}")
            results["linking_report"].append(f"💥 Critical error: {str(e)}")
            return json.dumps(results, indent=2)