import json
import random
import time
from datetime import datetime, timedelta
from agents.basic_agent import BasicAgent
from agents.OneClickCRMIntakeAgent import OneClickCRMIntakeAgent

class BulkCRMDataGeneratorAgent(BasicAgent):
    def __init__(self):
        self.name = "BulkCRMDataGenerator"
        self.metadata = {
            "name": self.name,
            "description": "Generates bulk CRM data by calling OneClickCRMIntakeAgent multiple times in a loop. ALL data must be provided by caller - no hardcoded values.",
            "parameters": {
                "type": "object",
                "properties": {
                    "iterations": {
                        "type": "integer",
                        "description": "Number of times to run the OneClickCRMIntakeAgent. Each iteration creates one account with related records.",
                        "minimum": 1,
                        "maximum": 100
                    },
                    "company_name_components": {
                        "type": "object",
                        "description": "Components for generating unique company names. REQUIRED - no defaults.",
                        "properties": {
                            "prefixes": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Company name prefixes. Example: ['Global', 'Advanced', 'Premier', 'Elite', 'Professional', 'Strategic', 'Dynamic']"
                            },
                            "industry_terms": {
                                "type": "object",
                                "description": "Industry-specific terms by theme. Example: {'technology': ['Tech', 'Software', 'Digital'], 'healthcare': ['Health', 'Medical', 'Care']}",
                                "additionalProperties": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                }
                            },
                            "suffixes": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Company name suffixes. Example: ['Corporation', 'Inc', 'Solutions', 'Group', 'Partners', 'LLC']"
                            }
                        },
                        "required": ["prefixes", "industry_terms", "suffixes"]
                    },
                    "contact_name_pools": {
                        "type": "object",
                        "description": "Name pools for generating contacts. REQUIRED - no defaults.",
                        "properties": {
                            "first_names": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Pool of first names. Example: ['James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda']"
                            },
                            "last_names": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Pool of last names. Example: ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller']"
                            },
                            "job_titles": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Pool of job titles. Example: ['Manager', 'Director', 'Vice President', 'Analyst', 'Specialist', 'Coordinator']"
                            }
                        },
                        "required": ["first_names", "last_names", "job_titles"]
                    },
                    "opportunity_templates": {
                        "type": "object",
                        "description": "Templates for generating opportunities. REQUIRED - no defaults.",
                        "properties": {
                            "name_templates": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Opportunity name templates. Example: ['Enterprise Software Upgrade', 'Cloud Migration Project', 'Digital Transformation']"
                            },
                            "value_range": {
                                "type": "object",
                                "properties": {
                                    "min": {"type": "integer", "description": "Minimum opportunity value"},
                                    "max": {"type": "integer", "description": "Maximum opportunity value"}
                                },
                                "required": ["min", "max"]
                            },
                            "probability_range": {
                                "type": "object",
                                "properties": {
                                    "min": {"type": "integer", "description": "Minimum close probability (0-100)"},
                                    "max": {"type": "integer", "description": "Maximum close probability (0-100)"}
                                },
                                "required": ["min", "max"]
                            },
                            "close_date_range": {
                                "type": "object",
                                "properties": {
                                    "min_days": {"type": "integer", "description": "Minimum days from today for close date"},
                                    "max_days": {"type": "integer", "description": "Maximum days from today for close date"}
                                },
                                "required": ["min_days", "max_days"]
                            },
                            "budget_status_values": {
                                "type": "array",
                                "items": {"type": "integer"},
                                "description": "Valid budget status values to randomly select from. Example: [1, 2, 3] for May Buy, Can Buy, Will Buy"
                            },
                            "purchase_process_values": {
                                "type": "array",
                                "items": {"type": "integer"},
                                "description": "Valid purchase process values. Example: [0, 1] for Individual, Committee"
                            }
                        },
                        "required": ["name_templates", "value_range", "probability_range", "close_date_range", "budget_status_values", "purchase_process_values"]
                    },
                    "case_templates": {
                        "type": "object",
                        "description": "Templates for generating cases. REQUIRED - no defaults.",
                        "properties": {
                            "title_templates": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Case title templates. Example: ['Login Authentication Issue', 'Performance Degradation', 'Data Sync Error']"
                            },
                            "description_template": {
                                "type": "string",
                                "description": "Template for case descriptions. Use {date} placeholder for current date. Example: 'Customer reported issue on {date}. Requires investigation.'"
                            },
                            "case_type_values": {
                                "type": "array",
                                "items": {"type": "integer"},
                                "description": "Valid case type codes. Example: [1, 2, 3] for Question, Problem, Request"
                            },
                            "case_origin_values": {
                                "type": "array",
                                "items": {"type": "integer"},
                                "description": "Valid case origin codes. Example: [1, 2, 3] for Phone, Email, Web"
                            }
                        },
                        "required": ["title_templates", "description_template", "case_type_values", "case_origin_values"]
                    },
                    "business_themes": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of business themes to randomly select from for each iteration. Must match keys in company_name_components.industry_terms. Example: ['technology', 'healthcare', 'financial']"
                    },
                    "record_count_ranges": {
                        "type": "object",
                        "description": "Min/max ranges for number of each record type per iteration. REQUIRED.",
                        "properties": {
                            "contacts": {
                                "type": "object",
                                "properties": {
                                    "min": {"type": "integer", "minimum": 0},
                                    "max": {"type": "integer", "minimum": 0}
                                },
                                "required": ["min", "max"]
                            },
                            "opportunities": {
                                "type": "object",
                                "properties": {
                                    "min": {"type": "integer", "minimum": 0},
                                    "max": {"type": "integer", "minimum": 0}
                                },
                                "required": ["min", "max"]
                            },
                            "cases": {
                                "type": "object",
                                "properties": {
                                    "min": {"type": "integer", "minimum": 0},
                                    "max": {"type": "integer", "minimum": 0}
                                },
                                "required": ["min", "max"]
                            }
                        },
                        "required": ["contacts", "opportunities", "cases"]
                    },
                    "account_configurations": {
                        "type": "object",
                        "description": "Configuration for account field values by theme. REQUIRED.",
                        "properties": {
                            "descriptions": {
                                "type": "object",
                                "description": "Description templates by theme. Example: {'technology': 'Leading technology company...', 'healthcare': 'Premier healthcare provider...'}",
                                "additionalProperties": {"type": "string"}
                            },
                            "customer_type_codes": {
                                "type": "array",
                                "items": {"type": "integer"},
                                "description": "Valid customer type codes to randomly select. Example: [3, 8] for Customer, Prospect"
                            },
                            "industry_codes": {
                                "type": "object",
                                "description": "Industry codes by theme. Example: {'technology': 4, 'healthcare': 11, 'financial': 6}",
                                "additionalProperties": {"type": "integer"}
                            }
                        },
                        "required": ["descriptions", "customer_type_codes", "industry_codes"]
                    },
                    "contact_preferences": {
                        "type": "object",
                        "description": "Configuration for contact field values. REQUIRED.",
                        "properties": {
                            "email_domain_suffix": {
                                "type": "string",
                                "description": "Domain suffix for email addresses. Example: '.com'"
                            },
                            "preferred_contact_methods": {
                                "type": "array",
                                "items": {"type": "integer"},
                                "description": "Valid preferred contact method codes. Example: [1, 2, 3] for Any, Email, Phone"
                            },
                            "gender_codes": {
                                "type": "array",
                                "items": {"type": "integer"},
                                "description": "Valid gender codes. Example: [1, 2] for Male, Female"
                            }
                        },
                        "required": ["email_domain_suffix", "preferred_contact_methods", "gender_codes"]
                    },
                    "dynamics_configuration": {
                        "type": "object",
                        "description": "Dynamics 365 specific configuration to pass to OneClickCRMIntakeAgent",
                        "properties": {
                            "system_user_search": {
                                "type": "string",
                                "description": "Partial name to search for system users to connect to opportunities"
                            },
                            "base_url": {
                                "type": "string",
                                "description": "Base URL for Dynamics 365 instance"
                            },
                            "app_id": {
                                "type": "string",
                                "description": "Dynamics 365 app ID for link generation"
                            },
                            "currency_code": {
                                "type": "string",
                                "description": "ISO currency code for monetary fields"
                            },
                            "detail_level": {
                                "type": "string",
                                "enum": ["minimal", "standard", "comprehensive"],
                                "description": "Level of detail for auto-filled fields"
                            },
                            "priority_code": {
                                "type": "integer",
                                "description": "Priority code value for opportunities and cases. Example: 1 for High"
                            },
                            "sales_stage_code": {
                                "type": "integer",
                                "description": "Sales stage code for opportunities. Example: 1 for Develop"
                            },
                            "severity_code": {
                                "type": "integer",
                                "description": "Severity code for cases. Example: 1 for High"
                            }
                        }
                    },
                    "execution_settings": {
                        "type": "object",
                        "description": "Settings for execution behavior",
                        "properties": {
                            "delay_between_iterations": {
                                "type": "number",
                                "description": "Seconds to wait between iterations to avoid rate limiting",
                                "minimum": 0,
                                "maximum": 60
                            },
                            "stop_on_error": {
                                "type": "boolean",
                                "description": "Whether to stop execution if an iteration fails"
                            },
                            "create_connections": {
                                "type": "boolean",
                                "description": "Whether to create system user connections (requires system_user_search)"
                            }
                        }
                    }
                },
                "required": [
                    "iterations",
                    "company_name_components",
                    "contact_name_pools",
                    "opportunity_templates",
                    "case_templates",
                    "business_themes",
                    "record_count_ranges",
                    "account_configurations",
                    "contact_preferences"
                ]
            }
        }
        super().__init__(name=self.name, metadata=self.metadata)
        
        # Initialize the OneClickCRMIntakeAgent
        self.crm_agent = OneClickCRMIntakeAgent()

    def validate_parameters(self, kwargs):
        """Validate all required parameters are present and properly structured"""
        errors = []
        
        # Check top-level required parameters
        required_params = [
            "iterations", "company_name_components", "contact_name_pools",
            "opportunity_templates", "case_templates", "business_themes",
            "record_count_ranges", "account_configurations", "contact_preferences"
        ]
        
        for param in required_params:
            if param not in kwargs:
                errors.append(f"Missing required parameter: '{param}'")
        
        # Validate nested required fields if parent exists
        if "company_name_components" in kwargs:
            comp = kwargs["company_name_components"]
            for field in ["prefixes", "industry_terms", "suffixes"]:
                if field not in comp:
                    errors.append(f"Missing required field 'company_name_components.{field}'")
                elif field != "industry_terms" and not isinstance(comp.get(field), list):
                    errors.append(f"'company_name_components.{field}' must be an array")
                elif field != "industry_terms" and len(comp.get(field, [])) == 0:
                    errors.append(f"'company_name_components.{field}' cannot be empty")
        
        if "contact_name_pools" in kwargs:
            pools = kwargs["contact_name_pools"]
            for field in ["first_names", "last_names", "job_titles"]:
                if field not in pools:
                    errors.append(f"Missing required field 'contact_name_pools.{field}'")
                elif not isinstance(pools.get(field), list) or len(pools.get(field, [])) == 0:
                    errors.append(f"'contact_name_pools.{field}' must be a non-empty array")
        
        if "opportunity_templates" in kwargs:
            opp = kwargs["opportunity_templates"]
            required_opp_fields = ["name_templates", "value_range", "probability_range", 
                                  "close_date_range", "budget_status_values", "purchase_process_values"]
            for field in required_opp_fields:
                if field not in opp:
                    errors.append(f"Missing required field 'opportunity_templates.{field}'")
            
            # Validate ranges
            for range_field in ["value_range", "probability_range", "close_date_range"]:
                if range_field in opp:
                    range_obj = opp[range_field]
                    if range_field == "close_date_range":
                        min_key, max_key = "min_days", "max_days"
                    else:
                        min_key, max_key = "min", "max"
                    
                    if min_key not in range_obj or max_key not in range_obj:
                        errors.append(f"'opportunity_templates.{range_field}' must have '{min_key}' and '{max_key}'")
        
        if "case_templates" in kwargs:
            case = kwargs["case_templates"]
            for field in ["title_templates", "description_template", "case_type_values", "case_origin_values"]:
                if field not in case:
                    errors.append(f"Missing required field 'case_templates.{field}'")
        
        if "record_count_ranges" in kwargs:
            ranges = kwargs["record_count_ranges"]
            for record_type in ["contacts", "opportunities", "cases"]:
                if record_type not in ranges:
                    errors.append(f"Missing required field 'record_count_ranges.{record_type}'")
                elif "min" not in ranges.get(record_type, {}) or "max" not in ranges.get(record_type, {}):
                    errors.append(f"'record_count_ranges.{record_type}' must have 'min' and 'max'")
        
        if "account_configurations" in kwargs:
            acc = kwargs["account_configurations"]
            for field in ["descriptions", "customer_type_codes", "industry_codes"]:
                if field not in acc:
                    errors.append(f"Missing required field 'account_configurations.{field}'")
            
            # Validate descriptions has entries for all themes
            if "descriptions" in acc and "business_themes" in kwargs:
                for theme in kwargs["business_themes"]:
                    if theme not in acc["descriptions"]:
                        errors.append(f"Missing description for theme '{theme}' in 'account_configurations.descriptions'")
        
        if "contact_preferences" in kwargs:
            prefs = kwargs["contact_preferences"]
            for field in ["email_domain_suffix", "preferred_contact_methods", "gender_codes"]:
                if field not in prefs:
                    errors.append(f"Missing required field 'contact_preferences.{field}'")
        
        # Validate business_themes matches industry_terms keys
        if "business_themes" in kwargs and "company_name_components" in kwargs:
            themes = kwargs["business_themes"]
            if "industry_terms" in kwargs["company_name_components"]:
                industry_terms = kwargs["company_name_components"]["industry_terms"]
                for theme in themes:
                    if theme not in industry_terms:
                        errors.append(f"Theme '{theme}' not found in 'company_name_components.industry_terms'")
        
        return errors

    def generate_company_name(self, theme, components, used_names):
        """Generate a unique company name based on theme and provided components"""
        attempts = 0
        while attempts < 50:
            prefix = random.choice(components['prefixes'])
            
            # Get industry terms for the theme, with fallback
            industry_terms = components['industry_terms'].get(theme, components['industry_terms'].get('generic', ['Business']))
            middle = random.choice(industry_terms)
            
            suffix = random.choice(components['suffixes'])
            
            name = f"{prefix} {middle} {suffix}"
            if name not in used_names:
                used_names.add(name)
                return name
            attempts += 1
        
        # Fallback with timestamp to ensure uniqueness
        timestamp = datetime.now().strftime('%H%M%S')
        name = f"{prefix} {middle} {suffix} {timestamp}"
        used_names.add(name)
        return name

    def perform(self, **kwargs):
        """Execute bulk CRM data generation using only provided parameters"""
        # Validate parameters first
        validation_errors = self.validate_parameters(kwargs)
        if validation_errors:
            return json.dumps({
                "status": "error",
                "message": "Parameter validation failed",
                "validation_errors": validation_errors,
                "required_structure": {
                    "iterations": "integer (1-100)",
                    "company_name_components": {
                        "prefixes": ["array of strings"],
                        "industry_terms": {"theme_name": ["array of terms"]},
                        "suffixes": ["array of strings"]
                    },
                    "contact_name_pools": {
                        "first_names": ["array of strings"],
                        "last_names": ["array of strings"],
                        "job_titles": ["array of strings"]
                    },
                    "opportunity_templates": {
                        "name_templates": ["array of strings"],
                        "value_range": {"min": "integer", "max": "integer"},
                        "probability_range": {"min": "integer", "max": "integer"},
                        "close_date_range": {"min_days": "integer", "max_days": "integer"},
                        "budget_status_values": ["array of integers"],
                        "purchase_process_values": ["array of integers"]
                    },
                    "case_templates": {
                        "title_templates": ["array of strings"],
                        "description_template": "string with {date} placeholder",
                        "case_type_values": ["array of integers"],
                        "case_origin_values": ["array of integers"]
                    },
                    "business_themes": ["array matching industry_terms keys"],
                    "record_count_ranges": {
                        "contacts": {"min": "integer", "max": "integer"},
                        "opportunities": {"min": "integer", "max": "integer"},
                        "cases": {"min": "integer", "max": "integer"}
                    },
                    "account_configurations": {
                        "descriptions": {"theme_name": "description string"},
                        "customer_type_codes": ["array of integers"],
                        "industry_codes": {"theme_name": "integer code"}
                    },
                    "contact_preferences": {
                        "email_domain_suffix": "string",
                        "preferred_contact_methods": ["array of integers"],
                        "gender_codes": ["array of integers"]
                    }
                }
            }, indent=2)
        
        # Extract all parameters
        iterations = kwargs['iterations']
        company_components = kwargs['company_name_components']
        contact_pools = kwargs['contact_name_pools']
        opportunity_templates = kwargs['opportunity_templates']
        case_templates = kwargs['case_templates']
        business_themes = kwargs['business_themes']
        record_ranges = kwargs['record_count_ranges']
        account_config = kwargs['account_configurations']
        contact_prefs = kwargs['contact_preferences']
        dynamics_config = kwargs.get('dynamics_configuration', {})
        exec_settings = kwargs.get('execution_settings', {})
        
        # Track results
        results = {
            "iterations_completed": 0,
            "total_records_created": 0,
            "records_by_type": {
                "accounts": 0,
                "contacts": 0,
                "opportunities": 0,
                "cases": 0,
                "connections": 0
            },
            "iteration_results": [],
            "errors": [],
            "summary": ""
        }
        
        # Track used names to avoid duplicates
        used_company_names = set()
        used_opportunity_names = set()
        
        # Main loop
        for i in range(iterations):
            try:
                # Select random theme for this iteration
                theme = random.choice(business_themes)
                
                # Generate account data
                company_name = self.generate_company_name(theme, company_components, used_company_names)
                account_data = {
                    "name": company_name,
                    "description": account_config['descriptions'].get(theme, f"Company operating in {theme} industry"),
                    "customertypecode": random.choice(account_config['customer_type_codes']),
                    "industrycode": account_config['industry_codes'].get(theme, account_config['industry_codes'].get('generic', 34))
                }
                
                # Generate contacts
                num_contacts = random.randint(record_ranges['contacts']['min'], record_ranges['contacts']['max'])
                contacts_data = []
                
                for c in range(num_contacts):
                    first = random.choice(contact_pools['first_names'])
                    last = random.choice(contact_pools['last_names'])
                    email_base = company_name.lower().replace(' ', '').replace(',', '').replace('.', '')[:20]
                    
                    contacts_data.append({
                        "firstname": first,
                        "lastname": last,
                        "jobtitle": random.choice(contact_pools['job_titles']),
                        "emailaddress1": f"{first.lower()}.{last.lower()}@{email_base}{contact_prefs['email_domain_suffix']}",
                        "preferredcontactmethodcode": random.choice(contact_prefs['preferred_contact_methods']),
                        "gendercode": random.choice(contact_prefs['gender_codes'])
                    })
                
                # Generate opportunities
                num_opportunities = random.randint(record_ranges['opportunities']['min'], record_ranges['opportunities']['max'])
                opportunities_data = []
                
                for o in range(num_opportunities):
                    # Select or create unique opportunity name
                    base_name = random.choice(opportunity_templates['name_templates'])
                    opp_name = base_name
                    counter = 1
                    while opp_name in used_opportunity_names:
                        opp_name = f"{base_name} - Phase {counter}"
                        counter += 1
                    used_opportunity_names.add(opp_name)
                    
                    # Calculate dates
                    days_until = random.randint(
                        opportunity_templates['close_date_range']['min_days'],
                        opportunity_templates['close_date_range']['max_days']
                    )
                    close_date = (datetime.now() + timedelta(days=days_until)).strftime('%Y-%m-%d')
                    
                    opp_data = {
                        "name": opp_name,
                        "estimatedvalue": random.randint(
                            opportunity_templates['value_range']['min'],
                            opportunity_templates['value_range']['max']
                        ),
                        "closeprobability": random.randint(
                            opportunity_templates['probability_range']['min'],
                            opportunity_templates['probability_range']['max']
                        ),
                        "estimatedclosedate": close_date,
                        "budgetstatus": random.choice(opportunity_templates['budget_status_values']),
                        "purchaseprocess": random.choice(opportunity_templates['purchase_process_values'])
                    }
                    
                    # Add priority and sales stage if provided
                    if dynamics_config.get('priority_code'):
                        opp_data["prioritycode"] = dynamics_config['priority_code']
                    if dynamics_config.get('sales_stage_code'):
                        opp_data["salesstagecode"] = dynamics_config['sales_stage_code']
                    
                    opportunities_data.append(opp_data)
                
                # Generate cases
                num_cases = random.randint(record_ranges['cases']['min'], record_ranges['cases']['max'])
                cases_data = []
                
                for cs in range(num_cases):
                    case_data = {
                        "title": random.choice(case_templates['title_templates']),
                        "description": case_templates['description_template'].replace('{date}', datetime.now().strftime('%Y-%m-%d')),
                        "casetypecode": random.choice(case_templates['case_type_values']),
                        "caseorigincode": random.choice(case_templates['case_origin_values'])
                    }
                    
                    # Add priority and severity if provided
                    if dynamics_config.get('priority_code'):
                        case_data["prioritycode"] = dynamics_config['priority_code']
                    if dynamics_config.get('severity_code'):
                        case_data["severitycode"] = dynamics_config['severity_code']
                    
                    cases_data.append(case_data)
                
                # Prepare parameters for OneClickCRMIntakeAgent
                crm_params = {
                    "account_data": json.dumps(account_data),
                    "contacts_data": json.dumps(contacts_data),
                    "opportunities_data": json.dumps(opportunities_data),
                    "cases_data": json.dumps(cases_data),
                    "auto_fill_details": True,
                    "detail_level": dynamics_config.get('detail_level', 'standard'),
                    "business_theme": theme
                }
                
                # Add optional Dynamics configuration
                if dynamics_config.get('system_user_search') and exec_settings.get('create_connections', True):
                    crm_params["system_user_search"] = dynamics_config['system_user_search']
                if dynamics_config.get('base_url'):
                    crm_params["dynamics_base_url"] = dynamics_config['base_url']
                if dynamics_config.get('app_id'):
                    crm_params["app_id"] = dynamics_config['app_id']
                if dynamics_config.get('currency_code'):
                    crm_params["currency_code"] = dynamics_config['currency_code']
                
                # Call OneClickCRMIntakeAgent
                iteration_result = self.crm_agent.perform(**crm_params)
                
                # Parse results
                try:
                    parsed_result = json.loads(iteration_result)
                    
                    # Update totals
                    if 'summary' in parsed_result:
                        summary = parsed_result['summary']
                        results["records_by_type"]["accounts"] += summary.get("accounts", 0)
                        results["records_by_type"]["contacts"] += summary.get("contacts", 0)
                        results["records_by_type"]["opportunities"] += summary.get("opportunities", 0)
                        results["records_by_type"]["cases"] += summary.get("cases", 0)
                        results["records_by_type"]["connections"] += summary.get("connections", 0)
                        results["total_records_created"] += summary.get("total_records_created", 0)
                    
                    # Store iteration details
                    results["iteration_results"].append({
                        "iteration": i + 1,
                        "theme": theme,
                        "company_name": company_name,
                        "records_created": parsed_result.get("summary", {}).get("total_records_created", 0),
                        "errors": len(parsed_result.get("errors", [])),
                        "links": parsed_result.get("links", {})
                    })
                    
                    # Collect any errors
                    if parsed_result.get("errors"):
                        for error in parsed_result["errors"]:
                            results["errors"].append(f"Iteration {i+1}: {error}")
                        
                        # Stop on error if configured
                        if exec_settings.get('stop_on_error', False) and parsed_result.get("errors"):
                            results["errors"].append(f"Stopping execution at iteration {i+1} due to errors (stop_on_error=true)")
                            break
                    
                    results["iterations_completed"] += 1
                    
                except json.JSONDecodeError as e:
                    error_msg = f"Iteration {i+1}: Failed to parse CRM agent response - {str(e)}"
                    results["errors"].append(error_msg)
                    
                    if exec_settings.get('stop_on_error', False):
                        results["errors"].append(f"Stopping execution at iteration {i+1} due to parsing error (stop_on_error=true)")
                        break
                
                # Delay between iterations if specified
                delay = exec_settings.get('delay_between_iterations', 0)
                if delay > 0 and i < iterations - 1:
                    time.sleep(delay)
                    
            except Exception as e:
                error_msg = f"Iteration {i+1}: Critical error - {str(e)}"
                results["errors"].append(error_msg)
                
                if exec_settings.get('stop_on_error', False):
                    results["errors"].append(f"Stopping execution at iteration {i+1} due to critical error (stop_on_error=true)")
                    break
        
        # Generate summary
        summary_parts = [
            f"🏭 BULK CRM DATA GENERATION COMPLETE",
            f"📊 Total Iterations: {results['iterations_completed']}/{iterations}",
            f"📈 Total Records Created: {results['total_records_created']}",
            "",
            "📋 Records by Type:",
            f"  • Accounts: {results['records_by_type']['accounts']}",
            f"  • Contacts: {results['records_by_type']['contacts']}",
            f"  • Opportunities: {results['records_by_type']['opportunities']}",
            f"  • Cases: {results['records_by_type']['cases']}",
            f"  • Connections: {results['records_by_type']['connections']}",
            "",
            f"🎨 Themes Used: {', '.join(business_themes)}",
            f"📏 Detail Level: {dynamics_config.get('detail_level', 'standard')}"
        ]
        
        if results["errors"]:
            summary_parts.append(f"\n⚠️ Errors Encountered: {len(results['errors'])}")
        
        if dynamics_config.get('system_user_search') and exec_settings.get('create_connections', True):
            summary_parts.append(f"🤝 Connected to users matching: '{dynamics_config['system_user_search']}'")
        
        results["summary"] = "\n".join(summary_parts)
        
        return json.dumps(results, indent=2)