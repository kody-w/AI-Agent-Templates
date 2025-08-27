# Voice to CRM Integration Stack

## Overview
This agent stack provides an end-to-end solution for capturing sales call data and automatically integrating it with your CRM system. It extracts information from SharePoint documents (including call transcripts), loads data into Dynamics 365, and sends follow-up emails - all through a modular AI agent system.

## Directory Structure
```
voice_to_crm_stack/
├── agents/                                         # Agent implementations
│   ├── extract_sharepoint_document_url_agent.py   # SharePoint document extractor
│   ├── dynamics_365_agent.py                      # Dynamics 365 CRUD operations
│   ├── email_drafting_agent.py                    # Email drafting and sending
│   └── servicenow-agent.py                        # ServiceNow integration (optional)
├── MSFTAIBASMultiAgentCopilot_1_0_0_1_managed.zip # Power Platform managed solution
├── index_voice.html                                # Web interface (optional)
└── README.md                                       # This documentation
```

## Key Features
- **SharePoint Document Extraction**: Extract content from documents, PDFs, and images stored in SharePoint
- **Dynamics 365 Integration**: Create, read, update, and delete records in Dynamics 365
- **Email Automation**: Draft and send meeting recap emails through Power Automate
- **Modular Architecture**: Drop-in agents that work with any compatible AI system

## Agents Included

### 1. SharePoint Document Extractor Agent (`agents/extract_sharepoint_document_url_agent.py`)
Extracts complete content from SharePoint documents including:
- Word documents (.docx)
- PDF files
- Text files
- Images (with Vision AI analysis)
- Entire folders of documents

### 2. Dynamics 365 CRUD Agent (`agents/dynamics_365_agent.py`)
Performs full CRUD operations with Dynamics 365:
- Create new records (contacts, leads, opportunities)
- Read existing records
- Update record fields
- Delete records
- Execute complex FetchXML queries

### 3. Email Drafting Agent (`agents/email_drafting_agent.py`)
Drafts professional emails and sends them via Power Automate:
- HTML formatted emails
- Multiple recipients (To, CC, BCC)
- Attachment support
- Priority settings

## Installation & Setup

### Prerequisites
- Python 3.8+
- Azure Active Directory (Entra ID) app registration
- Dynamics 365 instance
- SharePoint site access
- Power Automate flow for email sending
- Azure OpenAI service (for document analysis)

### Step 1: Deploy the Managed Solution

#### Option A: Import the Managed Solution
1. Navigate to your Power Platform environment
2. Go to **Solutions** in the left navigation
3. Click **Import solution**
4. Upload `MSFTAIBASMultiAgentCopilot_1_0_0_1_managed.zip`
5. Follow the import wizard to complete installation

#### Option B: Manual Setup
If you prefer to set up components manually, skip the managed solution and configure each service individually.

### Step 2: Configure Azure App Registration

1. **Create App Registration in Azure Portal**:
   ```
   Portal > Azure Active Directory > App registrations > New registration
   - Name: VoiceToCRM-Integration
   - Supported account types: Single tenant
   ```

2. **Generate Client Secret**:
   ```
   Certificates & secrets > New client secret
   - Description: VoiceToCRM Secret
   - Copy the secret value immediately
   ```

3. **Configure API Permissions**:
   
   For SharePoint access:
   - Microsoft Graph > Application permissions:
     - `Sites.Read.All`
     - `Files.Read.All`
   
   For Dynamics 365 access:
   - Dynamics CRM > Application permissions:
     - `user_impersonation`

4. **Grant Admin Consent** for all permissions

### Step 3: Set Environment Variables

Create a `.env` file or set system environment variables:

```bash
# SharePoint Configuration
SHAREPOINT_CLIENT_ID=your-app-client-id
SHAREPOINT_CLIENT_SECRET=your-app-client-secret
SHAREPOINT_TENANT_ID=your-tenant-id
SHAREPOINT_TENANT_URL=https://yourcompany.sharepoint.com
SHAREPOINT_SITE_NAME=Sales
SHAREPOINT_DOCUMENT_PATH=Shared Documents/CallTranscripts

# Dynamics 365 Configuration
DYNAMICS_365_CLIENT_ID=your-app-client-id
DYNAMICS_365_CLIENT_SECRET=your-app-client-secret
DYNAMICS_365_TENANT_ID=your-tenant-id
DYNAMICS_365_RESOURCE=https://yourorg.crm.dynamics.com

# Email Configuration
EMAIL_POWER_AUTOMATE_URL=https://prod-xx.westus.logic.azure.com/workflows/xxx/triggers/manual/paths/invoke

# Azure OpenAI (for document analysis)
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/

# Azure Storage (for document caching)
AzureWebJobsStorage=DefaultEndpointsProtocol=https;AccountName=xxx;AccountKey=xxx
AZURE_FILES_SHARE_NAME=voicetocrm
```

### Step 4: Deploy Agents to Modular AI System

1. **Copy agents to your AI system's agents folder**:
   ```bash
   cp -r agent_stacks/voice_to_crm_stack/agents/*.py /path/to/your/ai/system/agents/
   ```

2. **Install required dependencies**:
   ```bash
   pip install requests msal pypdf python-docx Pillow azure-storage-file openai
   ```

3. **Register agents with your AI system** (varies by system):
   ```python
   # Example registration code
   # Note: Update import paths based on your AI system's structure
   from agents.extract_sharepoint_document_url_agent import SharePointDocumentExtractorAgent
   from agents.dynamics_365_agent import Dynamics365CRUDAgent
   from agents.email_drafting_agent import EmailDraftingAgent
   
   agent_registry.register(SharePointDocumentExtractorAgent())
   agent_registry.register(Dynamics365CRUDAgent())
   agent_registry.register(EmailDraftingAgent())
   ```

## Usage Examples

### End-to-End Sales Call Processing Workflow

#### 1. Extract Sales Call Transcript from SharePoint

```python
# Extract a specific call transcript
response = sharepoint_agent.perform(
    document_url="https://company.sharepoint.com/sites/Sales/Shared Documents/CallTranscripts/2024-01-15-AcmeCorp.docx",
    extract_full_content=True,
    analyze_images=True
)

# Or extract all transcripts from a folder
response = sharepoint_agent.perform(
    document_url="https://company.sharepoint.com/sites/Sales/Shared Documents/CallTranscripts/",
    extract_full_content=True
)
```

#### 2. Parse and Load Data into Dynamics 365

```python
# Create a new lead from extracted data
lead_data = {
    "subject": "Acme Corp - Enterprise Solution Interest",
    "firstname": "John",
    "lastname": "Smith",
    "companyname": "Acme Corporation",
    "emailaddress1": "john.smith@acme.com",
    "telephone1": "+1-555-0100",
    "description": extracted_transcript_summary,
    "leadsourcecode": 2,  # Phone
    "estimatedvalue": 150000
}

response = dynamics_agent.perform(
    operation="create",
    entity="leads",
    data=json.dumps(lead_data)
)

# Create a related opportunity
opportunity_data = {
    "name": "Acme Corp - Q1 2024 Enterprise Deal",
    "estimatedvalue": 150000,
    "estimatedclosedate": "2024-03-31",
    "description": meeting_notes,
    "parentcontactid@odata.bind": f"/contacts({contact_id})"
}

response = dynamics_agent.perform(
    operation="create",
    entity="opportunities",
    data=json.dumps(opportunity_data)
)
```

#### 3. Send Follow-up Email Recap

```python
# Draft and send meeting recap
email_body = f"""
Dear John,

Thank you for taking the time to discuss Acme Corporation's enterprise needs today.

Key Points Discussed:
• Your current challenges with inventory management
• Our enterprise solution capabilities
• Integration with your existing SAP system
• Potential timeline for Q1 2024 implementation

Next Steps:
1. I'll send over the detailed proposal by Friday
2. Technical demo scheduled for next Tuesday at 2 PM
3. Introduction call with our implementation team

Please find attached the product specifications we discussed.

Best regards,
Sarah Johnson
Enterprise Sales Manager
"""

response = email_agent.perform(
    subject="Follow-up: Acme Corp Enterprise Solution Discussion",
    to="john.smith@acme.com",
    cc=["manager@yourcompany.com"],
    body=email_body,
    importance="high"
)
```

### Complete Automation Script

```python
import json
from datetime import datetime

def process_sales_call(transcript_url):
    """
    Complete workflow to process a sales call transcript
    """
    
    # Step 1: Extract transcript from SharePoint
    print("Extracting transcript from SharePoint...")
    extract_response = sharepoint_agent.perform(
        document_url=transcript_url,
        extract_full_content=True
    )
    
    transcript_data = json.loads(extract_response)
    if transcript_data["status"] != "success":
        raise Exception(f"Failed to extract transcript: {transcript_data['message']}")
    
    full_content = transcript_data["full_content"]
    
    # Step 2: Parse key information (you might use AI to extract these)
    # This is a simplified example - in practice, use NLP to extract
    contact_info = {
        "firstname": "John",  # Extract from transcript
        "lastname": "Smith",
        "emailaddress1": "john.smith@example.com",
        "companyname": "Example Corp",
        "telephone1": "+1-555-0100"
    }
    
    # Step 3: Create or update contact in Dynamics 365
    print("Creating contact in Dynamics 365...")
    
    # First check if contact exists
    query_response = dynamics_agent.perform(
        operation="query",
        entity="contacts",
        fetchxml=f"<fetch><entity name='contact'><filter><condition attribute='emailaddress1' operator='eq' value='{contact_info['emailaddress1']}'/></filter></entity></fetch>"
    )
    
    query_data = json.loads(query_response)
    
    if query_data.get("value") and len(query_data["value"]) > 0:
        # Update existing contact
        contact_id = query_data["value"][0]["contactid"]
        dynamics_response = dynamics_agent.perform(
            operation="update",
            entity="contacts",
            record_id=contact_id,
            data=json.dumps(contact_info)
        )
    else:
        # Create new contact
        dynamics_response = dynamics_agent.perform(
            operation="create",
            entity="contacts",
            data=json.dumps(contact_info)
        )
        contact_data = json.loads(dynamics_response)
        contact_id = contact_data.get("guid")
    
    # Step 4: Create activity record for the call
    print("Creating activity record...")
    activity_data = {
        "subject": f"Sales Call - {contact_info['companyname']}",
        "description": full_content[:4000],  # Dynamics has field length limits
        "actualdurationminutes": 30,
        "phonenumber": contact_info["telephone1"],
        "regardingobjectid_contact@odata.bind": f"/contacts({contact_id})"
    }
    
    activity_response = dynamics_agent.perform(
        operation="create",
        entity="phonecalls",
        data=json.dumps(activity_data)
    )
    
    # Step 5: Send follow-up email
    print("Sending follow-up email...")
    email_response = email_agent.perform(
        subject=f"Thank you for our call - {contact_info['companyname']}",
        to=contact_info["emailaddress1"],
        body=f"""
        Dear {contact_info['firstname']},
        
        Thank you for our productive discussion today. As promised, I'm sending this follow-up 
        with a summary of our conversation and next steps.
        
        Key Discussion Points:
        [AI would extract and insert key points from transcript here]
        
        Next Steps:
        [AI would extract and insert action items here]
        
        Please don't hesitate to reach out if you have any questions.
        
        Best regards,
        Your Sales Team
        """,
        importance="normal"
    )
    
    print("Sales call processing completed successfully!")
    return {
        "contact_id": contact_id,
        "transcript_stored": transcript_data["storage"]["storage_path"],
        "email_sent": json.loads(email_response)["status"] == "success"
    }

# Run the workflow
result = process_sales_call(
    "https://company.sharepoint.com/sites/Sales/Shared Documents/CallTranscripts/2024-01-15-call.docx"
)
```

## Power Automate Flow Setup

### Create Email Sending Flow

1. **Create new Instant Cloud Flow** in Power Automate
2. **Add trigger**: "When a HTTP request is received"
3. **Configure Request Body JSON Schema**:
   ```json
   {
     "type": "object",
     "properties": {
       "subject": {"type": "string"},
       "to": {"type": "string"},
       "cc": {"type": "array"},
       "bcc": {"type": "array"},
       "body": {"type": "string"},
       "attachments": {"type": "array"},
       "metadata": {
         "type": "object",
         "properties": {
           "importance": {"type": "string"},
           "isHtml": {"type": "boolean"}
         }
       }
     }
   }
   ```
4. **Add action**: "Send an email (V2)" from Office 365 Outlook
5. **Map fields** from the trigger to email action
6. **Save and copy** the HTTP POST URL to `EMAIL_POWER_AUTOMATE_URL`

## Troubleshooting

### Common Issues and Solutions

1. **SharePoint Access Denied**
   - Verify app permissions include `Sites.Read.All`
   - Ensure admin consent is granted
   - Check site URL and document path are correct

2. **Dynamics 365 Authentication Fails**
   - Verify client credentials are correct
   - Check resource URL matches your Dynamics instance
   - Ensure app has Dynamics CRM permissions

3. **Email Not Sending**
   - Verify Power Automate flow is turned on
   - Check flow run history for errors
   - Ensure URL is correctly set in environment variable

4. **Document Extraction Errors**
   - Install required Python packages (pypdf, python-docx)
   - Check file permissions in SharePoint
   - Verify Azure OpenAI credentials for image analysis

## Security Best Practices

1. **Store credentials securely** - Use Azure Key Vault or secure environment variables
2. **Implement least privilege** - Grant only necessary permissions to app registrations
3. **Enable audit logging** - Track all CRM operations and document access
4. **Use managed identities** when running in Azure
5. **Encrypt sensitive data** in transit and at rest
6. **Regular credential rotation** - Update client secrets periodically

## Support and Contributions

For issues, questions, or contributions:
- Open an issue in the repository
- Check existing documentation
- Contact your system administrator

## License

[Your License Here]
