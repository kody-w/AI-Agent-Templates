"""
Azure Function Entry Point for Account Intelligence Stack
Integrates with Microsoft Copilot Studio

This function receives HTTP requests from Copilot Studio and routes them
to the Account Intelligence Orchestrator.
"""

import azure.functions as func
import json
import logging
import sys
import os

# Add agents directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'agents'))

from agents.account_intelligence_orchestrator import AccountIntelligenceOrchestrator

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Azure Function HTTP trigger for Account Intelligence

    Expected request body:
    {
        "operation": "account_briefing|stakeholder_analysis|competitive_intelligence|...",
        "account_id": "string",
        "contact_id": "string (optional)",
        "opportunity_id": "string (optional)",
        "context": {
            "meeting_type": "string (optional)",
            "message_type": "string (optional)",
            "timeframe": "string (optional)"
        }
    }
    """

    logging.info('Account Intelligence Function triggered')

    try:
        # Parse request body
        try:
            req_body = req.get_json()
        except ValueError:
            return func.HttpResponse(
                json.dumps({
                    "status": "error",
                    "message": "Invalid JSON in request body"
                }),
                status_code=400,
                mimetype="application/json"
            )

        # Validate required parameters
        if 'operation' not in req_body or 'account_id' not in req_body:
            return func.HttpResponse(
                json.dumps({
                    "status": "error",
                    "message": "Missing required parameters: operation and account_id"
                }),
                status_code=400,
                mimetype="application/json"
            )

        # Log the operation
        logging.info(f"Operation: {req_body['operation']} for Account: {req_body['account_id']}")

        # Initialize orchestrator
        orchestrator = AccountIntelligenceOrchestrator()

        # Execute operation
        result = orchestrator.perform(**req_body)

        # Log success
        logging.info(f"Operation completed successfully: {result.get('status')}")

        # Return response
        return func.HttpResponse(
            json.dumps(result, indent=2),
            status_code=200,
            mimetype="application/json",
            headers={
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",  # For Copilot Studio
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            }
        )

    except Exception as e:
        # Log error
        logging.error(f"Error processing request: {str(e)}", exc_info=True)

        # Return error response
        return func.HttpResponse(
            json.dumps({
                "status": "error",
                "message": f"Internal server error: {str(e)}",
                "operation": req_body.get('operation', 'unknown')
            }),
            status_code=500,
            mimetype="application/json"
        )
