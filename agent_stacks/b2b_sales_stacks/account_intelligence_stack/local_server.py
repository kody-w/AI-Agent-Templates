"""
Local Test Server for Account Intelligence Stack
Serves the test HTML interface and provides API endpoints for testing with mock data

Usage:
    python local_server.py

Then open:
    http://localhost:5001
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import sys
import os
import json
from datetime import datetime

# Add agents directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'agents')))

from account_intelligence_orchestrator import AccountIntelligenceOrchestrator

app = Flask(__name__)
CORS(app)  # Enable CORS for local testing

# Initialize orchestrator (in mock mode by default)
orchestrator = AccountIntelligenceOrchestrator()

@app.route('/')
def index():
    """Serve the test HTML interface"""
    return send_file('test_interface.html')

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for server status"""
    return jsonify({
        "status": "healthy",
        "mode": "mock",
        "server": "Account Intelligence Stack - Local Test Server",
        "version": orchestrator.metadata.get('version', '2.0.0'),
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "/": "Test HTML interface",
            "/health": "Server health check",
            "/intelligence": "POST - Run intelligence operations"
        }
    })

@app.route('/intelligence', methods=['POST'])
def run_intelligence_operation():
    """
    Main endpoint for running intelligence operations

    Expected payload:
    {
        "operation": "account_briefing|stakeholder_analysis|...",
        "account_id": "CONTOSO001",
        "contact_id": "CONT001",  // optional
        "opportunity_id": "OPP001",  // optional
        "context": {}  // optional
    }
    """
    try:
        # Get request payload
        payload = request.get_json()

        if not payload:
            return jsonify({
                "status": "error",
                "message": "No JSON payload provided",
                "timestamp": datetime.now().isoformat()
            }), 400

        # Validate required fields
        if 'operation' not in payload:
            return jsonify({
                "status": "error",
                "message": "Missing required field: operation",
                "timestamp": datetime.now().isoformat()
            }), 400

        if 'account_id' not in payload:
            return jsonify({
                "status": "error",
                "message": "Missing required field: account_id",
                "timestamp": datetime.now().isoformat()
            }), 400

        # Log request
        print(f"\n{'='*80}")
        print(f"📥 Incoming Request: {payload.get('operation')}")
        print(f"{'='*80}")
        print(f"Account ID: {payload.get('account_id')}")
        if payload.get('contact_id'):
            print(f"Contact ID: {payload.get('contact_id')}")
        if payload.get('opportunity_id'):
            print(f"Opportunity ID: {payload.get('opportunity_id')}")
        print(f"Timestamp: {datetime.now().isoformat()}\n")

        # Run the operation
        result = orchestrator.perform(**payload)

        # Log response
        print(f"✅ Operation completed: {result.get('status')}")
        print(f"Response size: {len(json.dumps(result))} chars")
        print(f"{'='*80}\n")

        return jsonify(result)

    except Exception as e:
        # Log error
        print(f"\n❌ Error processing request:")
        print(f"   {str(e)}\n")

        return jsonify({
            "status": "error",
            "message": f"Server error: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/operations', methods=['GET'])
def list_operations():
    """List all available operations"""
    return jsonify({
        "status": "success",
        "operations": orchestrator.metadata.get('parameters', {}).get('properties', {}).get('operation', {}).get('enum', []),
        "description": "Available intelligence operations",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/metadata', methods=['GET'])
def get_metadata():
    """Get orchestrator metadata"""
    return jsonify({
        "status": "success",
        "metadata": orchestrator.metadata,
        "timestamp": datetime.now().isoformat()
    })

def main():
    """Start the local test server"""
    print("\n" + "="*80)
    print("🚀 ACCOUNT INTELLIGENCE STACK - LOCAL TEST SERVER")
    print("="*80)
    print(f"\nMode: MOCK (no API credentials required)")
    print(f"Version: {orchestrator.metadata.get('version', '2.0.0')}")
    print(f"Orchestrator: {orchestrator.name}")
    print(f"\nEndpoints:")
    print(f"  - Home:         http://localhost:5001")
    print(f"  - Health:       http://localhost:5001/health")
    print(f"  - Intelligence: http://localhost:5001/intelligence (POST)")
    print(f"  - Operations:   http://localhost:5001/operations")
    print(f"  - Metadata:     http://localhost:5001/metadata")
    print(f"\n📋 Available Operations:")
    for i, op in enumerate(orchestrator.metadata['parameters']['properties']['operation']['enum'], 1):
        print(f"  {i}. {op}")
    print(f"\n✅ Server is ready!")
    print(f"   Open http://localhost:5001 in your browser to start testing\n")
    print("="*80 + "\n")

    # Start Flask server
    app.run(host='0.0.0.0', port=5001, debug=True)

if __name__ == "__main__":
    main()
