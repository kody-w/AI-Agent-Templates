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
            "type": "singular"
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
                    "stack_path": stack_dir.name
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