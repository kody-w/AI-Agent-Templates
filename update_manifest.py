#!/usr/bin/env python3
"""
Simple script to update manifest.json before pushing to GitHub.
Run this locally to regenerate the manifest with all agent/stack information.
"""

import json
import os
from pathlib import Path
from datetime import datetime

def format_file_size(size):
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f}{unit}"
        size /= 1024.0
    return f"{size:.1f}TB"

def get_agent_features(filename):
    """Get default features for an agent based on its filename"""
    # Default features that apply to all agents
    default_features = [
        "AI-powered automation",
        "Easy integration",
        "Scalable architecture",
        "Production ready"
    ]
    
    # Specific features based on agent type
    feature_map = {
        "email": ["Email composition", "Smart templates", "Auto-response", "Attachment handling"],
        "calendar": ["Schedule management", "Meeting coordination", "Availability tracking", "Time zone support"],
        "crm": ["CRM integration", "Data synchronization", "Record management", "Pipeline automation"],
        "dynamics": ["Dynamics 365 integration", "Entity management", "Workflow automation", "API connectivity"],
        "sharepoint": ["Document extraction", "SharePoint integration", "File management", "Metadata handling"],
        "memory": ["Context retention", "State management", "Memory optimization", "Conversation tracking"],
        "image": ["Image generation", "AI creativity", "Format support", "Batch processing"],
        "powerpoint": ["Presentation creation", "Slide automation", "Template support", "Export options"],
        "servicenow": ["Ticket management", "Workflow automation", "ServiceNow integration", "Incident tracking"],
        "salesforce": ["Salesforce queries", "Data extraction", "Report generation", "SOQL support"],
        "search": ["Web search", "Result aggregation", "Content filtering", "API integration"],
        "review": ["Code analysis", "Quality metrics", "Best practices", "Automated feedback"],
        "adaptive": ["Card generation", "Dynamic layouts", "Multi-platform", "Interactive elements"],
        "hacker": ["News aggregation", "Content monitoring", "Trend analysis", "Real-time updates"],
        "motivational": ["Quote generation", "Daily inspiration", "Category selection", "API integration"],
        "wikipedia": ["Article fetching", "Random content", "Knowledge extraction", "API connectivity"],
        "beehiiv": ["Newsletter integration", "Subscriber management", "Content automation", "Analytics"],
        "demo": ["Data generation", "Test scenarios", "Bulk operations", "Realistic samples"],
        "meeting": ["Meeting preparation", "Agenda creation", "Note taking", "Action items"]
    }
    
    # Check filename for keywords and return appropriate features
    filename_lower = filename.lower()
    for keyword, features in feature_map.items():
        if keyword in filename_lower:
            return features
    
    return default_features

def get_agent_description(filename):
    """Get a description for an agent based on its filename"""
    description_map = {
        "email": "Intelligent email drafting and automation agent",
        "calendar": "Calendar management and scheduling automation",
        "crm": "CRM integration and data management",
        "dynamics": "Microsoft Dynamics 365 integration agent",
        "sharepoint": "SharePoint document extraction and management",
        "memory": "Context and memory management for conversations",
        "image": "AI-powered image generation and processing",
        "powerpoint": "PowerPoint presentation automation",
        "servicenow": "ServiceNow ticket and workflow management",
        "salesforce": "Salesforce data query and integration",
        "search": "Web search and content aggregation",
        "review": "Automated code review and analysis",
        "adaptive": "Adaptive card generation for multiple platforms",
        "hacker": "Hacker News content aggregation and monitoring",
        "motivational": "Motivational quote generation and inspiration",
        "wikipedia": "Wikipedia article fetching and knowledge extraction",
        "beehiiv": "Beehiiv newsletter platform integration",
        "demo": "Demo data generation and seeding",
        "meeting": "Meeting preparation and coordination agent"
    }
    
    filename_lower = filename.lower()
    for keyword, description in description_map.items():
        if keyword in filename_lower:
            return description
    
    return "AI agent for task automation and workflow optimization"

def scan_agents():
    """Scan the agents directory"""
    agents = []
    agents_dir = Path("agents")
    
    if not agents_dir.exists():
        return agents
    
    for py_file in agents_dir.glob("*.py"):
        if py_file.name == "__init__.py":
            continue
        
        size = py_file.stat().st_size
        agent_id = py_file.stem
        
        agents.append({
            "id": agent_id,
            "name": agent_id.replace('_', ' ').title(),
            "filename": py_file.name,
            "path": f"agents/{py_file.name}",
            "url": f"https://raw.githubusercontent.com/kody-w/AI-Agent-Templates/main/agents/{py_file.name}",
            "size": size,
            "size_formatted": format_file_size(size),
            "type": "singular",
            "description": get_agent_description(py_file.name),
            "features": get_agent_features(py_file.name)
        })
    
    return agents

def scan_stacks():
    """Scan the agent_stacks directory"""
    stacks = []
    stacks_dir = Path("agent_stacks")
    
    if not stacks_dir.exists():
        return stacks
    
    for stack_dir in stacks_dir.iterdir():
        if not stack_dir.is_dir():
            continue
        
        stack_info = {
            "id": stack_dir.name,
            "name": stack_dir.name.replace('_', ' ').title(),
            "path": f"agent_stacks/{stack_dir.name}",
            "agents": [],
            "metadata": None
        }
        
        # Load metadata.json if it exists
        metadata_file = stack_dir / "metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                stack_info["metadata"] = json.load(f)
        
        # Scan agents subdirectory
        agents_dir = stack_dir / "agents"
        if agents_dir.exists():
            for py_file in agents_dir.glob("*.py"):
                if py_file.name == "__init__.py":
                    continue
                
                size = py_file.stat().st_size
                agent = {
                    "id": f"{stack_dir.name}_{py_file.stem}",
                    "name": py_file.stem.replace('_', ' ').title(),
                    "filename": py_file.name,
                    "path": f"agent_stacks/{stack_dir.name}/agents/{py_file.name}",
                    "url": f"https://raw.githubusercontent.com/kody-w/AI-Agent-Templates/main/agent_stacks/{stack_dir.name}/agents/{py_file.name}",
                    "size": size,
                    "size_formatted": format_file_size(size),
                    "type": "stack",
                    "stack_name": stack_info["name"],
                    "stack_path": stack_dir.name,
                    "description": get_agent_description(py_file.name),
                    "features": get_agent_features(py_file.name)
                }
                stack_info["agents"].append(agent)
        
        stacks.append(stack_info)
    
    return stacks

def main():
    print("\n🔄 Updating manifest.json...")
    print("-" * 40)
    
    # Build manifest
    manifest = {
        "version": "1.0.0",
        "generated": datetime.utcnow().isoformat() + "Z",
        "repository": "kody-w/AI-Agent-Templates",
        "branch": "main",
        "agents": [],
        "stacks": []
    }
    
    # Scan agents
    print("📂 Scanning agents directory...")
    manifest["agents"] = scan_agents()
    print(f"   Found {len(manifest['agents'])} agents")
    
    # Also create agents/index.json for raw URL loading
    agents_index = {
        "agents": [agent["filename"] for agent in manifest["agents"]]
    }
    with open("agents/index.json", 'w') as f:
        json.dump(agents_index, f, indent=2)
    print("   Created agents/index.json")
    
    # Scan stacks
    print("📂 Scanning agent_stacks directory...")
    manifest["stacks"] = scan_stacks()
    print(f"   Found {len(manifest['stacks'])} stacks")
    
    # Count total stack agents
    total_stack_agents = sum(len(stack['agents']) for stack in manifest['stacks'])
    print(f"   Total stack agents: {total_stack_agents}")
    
    # Write manifest
    with open("manifest.json", 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print("-" * 40)
    print("✅ manifest.json updated successfully!")
    print("\n📝 Next steps:")
    print("   1. Review changes: git diff manifest.json agents/index.json")
    print("   2. Commit: git add manifest.json agents/index.json && git commit -m 'Update manifest'")
    print("   3. Push: git push")
    print("\n")

if __name__ == "__main__":
    main()