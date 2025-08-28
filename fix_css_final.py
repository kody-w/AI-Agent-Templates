#!/usr/bin/env python3
"""
Script to fix CSS content properties that were broken by the conversion.
"""

import os
import re
import sys
from pathlib import Path

def fix_file(file_path):
    """Fix broken CSS content properties in a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix the specific broken pattern: content: `'; -> content: '';
        content = re.sub(r"content:\s*`([^`]*)`;\s*", r"content: '\1';", content)
        
        # Also fix the apiKey pattern: apiKey: ``, -> apiKey: '',
        content = re.sub(r"apiKey:\s*`[^`]*`,", "apiKey: '',", content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {file_path}")
            return True
        else:
            print(f"No changes needed: {file_path}")
            return False
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main function to process all demo HTML files."""
    base_dir = Path("/Users/kodyw/Documents/GitHub/AI-Agent-Templates")
    
    # Find all demo HTML files that have the issue
    demo_files = []
    for pattern in ["**/demos/*_demo.html"]:
        demo_files.extend(base_dir.glob(pattern))
    
    # Filter to only files that contain the broken pattern
    broken_files = []
    for file_path in demo_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'content: `' in content or 'apiKey: `' in content:
                    broken_files.append(file_path)
        except:
            pass
    
    print(f"Found {len(broken_files)} files with broken CSS/JS patterns")
    
    fixed_count = 0
    for file_path in broken_files:
        if fix_file(file_path):
            fixed_count += 1
    
    print(f"\nCompleted: Fixed {fixed_count} files out of {len(broken_files)} total files")

if __name__ == "__main__":
    main()