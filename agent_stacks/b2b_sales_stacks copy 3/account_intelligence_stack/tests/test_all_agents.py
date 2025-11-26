"""
Comprehensive Test Suite for Account Intelligence Stack
Simulates demo scenarios and validates all agents
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../agents')))

import json
from datetime import datetime

# Import orchestrator and all agents
from account_intelligence_orchestrator import AccountIntelligenceOrchestrator
from stakeholder_intelligence_agent import StakeholderIntelligenceAgent
from competitive_intelligence_agent import CompetitiveIntelligenceAgent
from meeting_prep_agent import MeetingPrepAgent
from messaging_agent import MessagingAgent
from risk_assessment_agent import RiskAssessmentAgent
from action_prioritization_agent import ActionPrioritizationAgent
from deal_tracking_agent import DealTrackingAgent

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_test_header(title):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{title:^80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}\n")

def print_success(message):
    print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")

def print_info(message):
    print(f"{Colors.OKCYAN}ℹ {message}{Colors.ENDC}")

def print_warning(message):
    print(f"{Colors.WARNING}⚠ {message}{Colors.ENDC}")

def print_error(message):
    print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")

def print_result(result, truncate=True):
    """Print JSON result with optional truncation"""
    result_str = json.dumps(result, indent=2)
    if truncate and len(result_str) > 1000:
        lines = result_str.split('\n')[:30]
        print('\n'.join(lines))
        print(f"{Colors.WARNING}... (truncated, {len(result_str)} total chars){Colors.ENDC}")
    else:
        print(result_str)

# Test scenarios matching the demo
TEST_SCENARIOS = {
    "account_briefing": {
        "name": "Complete Account Briefing",
        "description": "Get comprehensive overview of Contoso Corporation",
        "params": {
            "operation": "account_briefing",
            "account_id": "CONTOSO001"
        }
    },
    "stakeholder_analysis": {
        "name": "Buying Committee Analysis",
        "description": "Analyze all stakeholders with influence scores",
        "params": {
            "operation": "stakeholder_analysis",
            "account_id": "CONTOSO001"
        }
    },
    "competitive_intelligence": {
        "name": "Competitive Threat Detection",
        "description": "Identify DataBricks and Snowflake threats",
        "params": {
            "operation": "competitive_intelligence",
            "account_id": "CONTOSO001"
        }
    },
    "meeting_prep": {
        "name": "CTO Meeting Preparation",
        "description": "Generate brief for Sarah Chen meeting",
        "params": {
            "operation": "meeting_prep",
            "account_id": "CONTOSO001",
            "contact_id": "CONT001",
            "context": {"meeting_type": "executive_briefing"}
        }
    },
    "generate_messaging": {
        "name": "LinkedIn Message Generation",
        "description": "Create personalized LinkedIn connection request",
        "params": {
            "operation": "generate_messaging",
            "account_id": "CONTOSO001",
            "contact_id": "CONT001",
            "context": {"message_type": "linkedin_connection"}
        }
    },
    "risk_assessment": {
        "name": "Deal Risk Analysis",
        "description": "Assess risks and calculate win probability",
        "params": {
            "operation": "risk_assessment",
            "account_id": "CONTOSO001",
            "opportunity_id": "OPP001"
        }
    },
    "action_plan": {
        "name": "Next Actions Plan",
        "description": "Prioritized action plan for next 48 hours",
        "params": {
            "operation": "action_plan",
            "account_id": "CONTOSO001",
            "context": {"timeframe": "48_hours"}
        }
    },
    "deal_dashboard": {
        "name": "Real-Time Deal Tracking",
        "description": "Live deal metrics and progress tracking",
        "params": {
            "operation": "deal_dashboard",
            "account_id": "CONTOSO001",
            "opportunity_id": "OPP001"
        }
    }
}

def test_orchestrator():
    """Test the main orchestrator with all operations"""
    print_test_header("ORCHESTRATOR INTEGRATION TEST")

    orchestrator = AccountIntelligenceOrchestrator()
    print_info(f"Orchestrator initialized: {orchestrator.name}")
    print_info(f"Version: {orchestrator.metadata['version']}")
    print_info(f"Copilot Studio enabled: {orchestrator.metadata['copilot_studio_enabled']}")

    test_results = {
        "passed": 0,
        "failed": 0,
        "errors": []
    }

    for scenario_key, scenario in TEST_SCENARIOS.items():
        print(f"\n{Colors.BOLD}Test: {scenario['name']}{Colors.ENDC}")
        print(f"Description: {scenario['description']}")

        try:
            result = orchestrator.perform(**scenario['params'])

            # Validate response structure
            assert result.get('status') == 'success', f"Expected success, got {result.get('status')}"
            assert 'operation' in result, "Missing 'operation' field"
            assert 'data' in result, "Missing 'data' field"
            assert 'timestamp' in result, "Missing 'timestamp' field"

            print_success(f"Test passed: {scenario['name']}")
            print_info(f"Operation: {result.get('operation')}")
            print_info(f"Response size: {len(json.dumps(result))} chars")

            test_results['passed'] += 1

        except Exception as e:
            print_error(f"Test failed: {scenario['name']}")
            print_error(f"Error: {str(e)}")
            test_results['failed'] += 1
            test_results['errors'].append({
                "scenario": scenario['name'],
                "error": str(e)
            })

    return test_results

def test_individual_agents():
    """Test each specialized agent directly"""
    print_test_header("INDIVIDUAL AGENT TESTS")

    agents_to_test = [
        ("Stakeholder Intelligence", StakeholderIntelligenceAgent, {
            "operation": "analyze_buying_committee",
            "account_id": "CONTOSO001"
        }),
        ("Competitive Intelligence", CompetitiveIntelligenceAgent, {
            "operation": "detect_active_threats",
            "account_id": "CONTOSO001"
        }),
        ("Meeting Prep", MeetingPrepAgent, {
            "account_id": "CONTOSO001",
            "contact_id": "CONT001",
            "context": {"meeting_type": "executive_briefing"}
        }),
        ("Messaging", MessagingAgent, {
            "account_id": "CONTOSO001",
            "contact_id": "CONT001",
            "context": {"message_type": "linkedin_connection"}
        }),
        ("Risk Assessment", RiskAssessmentAgent, {
            "operation": "assess_opportunity",
            "account_id": "CONTOSO001",
            "opportunity_id": "OPP001"
        }),
        ("Action Prioritization", ActionPrioritizationAgent, {
            "operation": "action_plan",
            "account_id": "CONTOSO001",
            "context": {"timeframe": "48_hours"}
        }),
        ("Deal Tracking", DealTrackingAgent, {
            "operation": "deal_dashboard",
            "account_id": "CONTOSO001",
            "opportunity_id": "OPP001"
        })
    ]

    test_results = {
        "passed": 0,
        "failed": 0
    }

    for agent_name, AgentClass, params in agents_to_test:
        print(f"\n{Colors.BOLD}Testing: {agent_name} Agent{Colors.ENDC}")

        try:
            agent = AgentClass()
            result = agent.perform(**params)

            assert result.get('status') == 'success', f"Expected success"
            assert 'data' in result, "Missing data field"

            print_success(f"{agent_name} agent test passed")
            test_results['passed'] += 1

        except Exception as e:
            print_error(f"{agent_name} agent test failed: {str(e)}")
            test_results['failed'] += 1

    return test_results

def test_demo_simulation():
    """Simulate the complete demo flow"""
    print_test_header("DEMO SIMULATION - COMPLETE WORKFLOW")

    orchestrator = AccountIntelligenceOrchestrator()

    demo_steps = [
        {
            "step": 1,
            "user": "Give me a briefing on Contoso Corporation",
            "operation": "account_briefing",
            "account_id": "CONTOSO001"
        },
        {
            "step": 2,
            "user": "Who are the key stakeholders?",
            "operation": "stakeholder_analysis",
            "account_id": "CONTOSO001"
        },
        {
            "step": 3,
            "user": "What competitive threats are active?",
            "operation": "competitive_intelligence",
            "account_id": "CONTOSO001"
        },
        {
            "step": 4,
            "user": "Prepare me for my meeting with Sarah Chen",
            "operation": "meeting_prep",
            "account_id": "CONTOSO001",
            "contact_id": "CONT001",
            "context": {"meeting_type": "executive_briefing"}
        },
        {
            "step": 5,
            "user": "Draft a LinkedIn message to Sarah Chen",
            "operation": "generate_messaging",
            "account_id": "CONTOSO001",
            "contact_id": "CONT001",
            "context": {"message_type": "linkedin_connection"}
        },
        {
            "step": 6,
            "user": "What are the risks to closing this deal?",
            "operation": "risk_assessment",
            "account_id": "CONTOSO001",
            "opportunity_id": "OPP001"
        },
        {
            "step": 7,
            "user": "What should I do next?",
            "operation": "action_plan",
            "account_id": "CONTOSO001",
            "context": {"timeframe": "48_hours"}
        },
        {
            "step": 8,
            "user": "Show me the deal dashboard",
            "operation": "deal_dashboard",
            "account_id": "CONTOSO001",
            "opportunity_id": "OPP001"
        }
    ]

    print_info(f"Simulating {len(demo_steps)}-step demo conversation...")

    for step_info in demo_steps:
        step = step_info['step']
        user_query = step_info['user']
        params = {k: v for k, v in step_info.items() if k not in ['step', 'user']}

        print(f"\n{Colors.OKCYAN}{'─'*80}{Colors.ENDC}")
        print(f"{Colors.BOLD}Step {step}: {user_query}{Colors.ENDC}")
        print(f"{Colors.OKCYAN}{'─'*80}{Colors.ENDC}")

        try:
            result = orchestrator.perform(**params)

            if result.get('status') == 'success':
                print_success(f"Response generated successfully")
                print_info(f"Operation: {result.get('operation')}")

                # Print key data points
                data = result.get('data', {})
                if isinstance(data, dict):
                    # Print first few keys
                    for i, (key, value) in enumerate(list(data.items())[:3]):
                        if isinstance(value, (str, int, float)):
                            print_info(f"  {key}: {value}")
                        elif isinstance(value, dict):
                            print_info(f"  {key}: {len(value)} fields")
                        elif isinstance(value, list):
                            print_info(f"  {key}: {len(value)} items")

            else:
                print_error(f"Step {step} failed")

        except Exception as e:
            print_error(f"Step {step} error: {str(e)}")

def run_all_tests():
    """Run complete test suite"""
    print_test_header("ACCOUNT INTELLIGENCE STACK - COMPREHENSIVE TEST SUITE")

    print_info(f"Test started: {datetime.now().isoformat()}")
    print_info("Running in MOCK mode (no API credentials required)\n")

    start_time = datetime.now()

    # Run tests
    print("\n" + "="*80)
    orchestrator_results = test_orchestrator()

    print("\n" + "="*80)
    agent_results = test_individual_agents()

    print("\n" + "="*80)
    test_demo_simulation()

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    # Print summary
    print_test_header("TEST SUMMARY")

    total_passed = orchestrator_results['passed'] + agent_results['passed']
    total_failed = orchestrator_results['failed'] + agent_results['failed']
    total_tests = total_passed + total_failed

    print(f"{Colors.BOLD}Orchestrator Tests:{Colors.ENDC}")
    print(f"  ✓ Passed: {orchestrator_results['passed']}")
    print(f"  ✗ Failed: {orchestrator_results['failed']}")

    print(f"\n{Colors.BOLD}Individual Agent Tests:{Colors.ENDC}")
    print(f"  ✓ Passed: {agent_results['passed']}")
    print(f"  ✗ Failed: {agent_results['failed']}")

    print(f"\n{Colors.BOLD}Overall Results:{Colors.ENDC}")
    print(f"  Total Tests: {total_tests}")
    print(f"  Passed: {total_passed} ({(total_passed/total_tests*100):.1f}%)")
    print(f"  Failed: {total_failed}")
    print(f"  Duration: {duration:.2f} seconds")

    if total_failed == 0:
        print(f"\n{Colors.OKGREEN}{Colors.BOLD}🎉 ALL TESTS PASSED! 🎉{Colors.ENDC}")
        print(f"{Colors.OKGREEN}The Account Intelligence Stack is ready for deployment!{Colors.ENDC}")
    else:
        print(f"\n{Colors.FAIL}{Colors.BOLD}⚠️  SOME TESTS FAILED{Colors.ENDC}")
        print(f"{Colors.FAIL}Please review the errors above{Colors.ENDC}")

        if orchestrator_results.get('errors'):
            print(f"\n{Colors.BOLD}Errors:{Colors.ENDC}")
            for error in orchestrator_results['errors']:
                print(f"  - {error['scenario']}: {error['error']}")

    return total_failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
