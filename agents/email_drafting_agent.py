from agents.basic_agent import BasicAgent
import json
import requests
from typing import Optional, List

class EmailDraftingAgent(BasicAgent):
    def __init__(self):
        self.name = "EmailDrafting"
        self.metadata = {
            "name": self.name,
            "description": "Drafts an email with proper formatting and sends it to a Microsoft Power Automate flow endpoint for processing and delivery.",
            "parameters": {
                "type": "object",
                "properties": {
                    "subject": {
                        "type": "string",
                        "description": "The subject line of the email."
                    },
                    "to": {
                        "type": "string",
                        "description": "Email address of the primary recipient."
                    },
                    "cc": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional. List of email addresses to CC."
                    },
                    "bcc": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional. List of email addresses to BCC."
                    },
                    "body": {
                        "type": "string",
                        "description": "The full body of the email. This can include any content the caller desires."
                    },
                    "attachments": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional. List of attachment file names or identifiers."
                    },
                    "importance": {
                        "type": "string",
                        "description": "Optional. Importance level of the email.",
                        "enum": ["low", "normal", "high"]
                    }
                },
                "required": ["subject", "to", "body"]
            }
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, **kwargs):
        subject = kwargs.get('subject')
        to = kwargs.get('to')
        body = kwargs.get('body')
        cc = kwargs.get('cc', [])
        bcc = kwargs.get('bcc', [])
        attachments = kwargs.get('attachments', [])
        importance = kwargs.get('importance', 'normal')

        try:
            if not subject.strip():
                raise ValueError("The 'subject' parameter is required and cannot be empty.")
            if not to.strip():
                raise ValueError("The 'to' parameter is required and cannot be empty.")
            if not body.strip():
                raise ValueError("The 'body' parameter is required and cannot be empty.")

            body_html = body.replace('\n', '<br>')

            email_draft = {
                "subject": subject,
                "to": to,
                "cc": cc,
                "bcc": bcc,
                "body": body_html,
                "attachments": attachments,
                "metadata": {
                    "importance": importance,
                    "isHtml": True
                }
            }

            url = (
                "https://2ecf0a25a2e7eb6a9aec43400e2b67.02.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/88c0a2ef519442de832239db26d89fc7/triggers/manual/paths/invoke/?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=MEZuCMaL6Y2KCHl9QlMV9eyDLNHZ5MGd7pbrnDD6kV8"
            )

            headers = {
                "Content-Type": "application/json"
            }

            response = requests.post(url, json=email_draft, headers=headers)

            if response.status_code in [200, 202]:
                return json.dumps({
                    "status": "success",
                    "message": "Email draft sent to Power Automate successfully",
                    "response": response.text[:1000]
                })
            else:
                return json.dumps({
                    "status": "error",
                    "message": f"Failed to send email draft to Power Automate. Status code: {response.status_code}",
                    "response": response.text[:1000]
                })

        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"An error occurred: {str(e)}"
            })