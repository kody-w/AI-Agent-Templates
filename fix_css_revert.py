#!/usr/bin/env python3
"""
Script to fix CSS content properties that were incorrectly converted to template literals,
and properly handle JavaScript content properties with apostrophes.
"""

import os
import re
import sys
from pathlib import Path

def fix_file(file_path):
    """Fix CSS and JavaScript issues in a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix CSS content properties that were incorrectly converted to template literals
        # Convert content: `` back to content: ''
        content = re.sub(r"(\s*content:\s*)`([^`]*)`;", r"\1'\2';", content)
        
        # Fix apiKey properties that were incorrectly converted
        content = re.sub(r"apiKey:\s*`[^`]*`,", "apiKey: '',", content)
        
        # Now fix JavaScript content strings with unescaped apostrophes
        # Only in JavaScript context (not CSS)
        def fix_js_content(match):
            full_match = match.group(0)
            quote = match.group(1)
            inner_content = match.group(2)
            
            # If it contains unescaped apostrophes and it's JavaScript (has comma at end)
            if "'" in inner_content and full_match.endswith(','):
                # Replace with template literal
                escaped_content = inner_content.replace('`', '\\`')
                return f"content: `{escaped_content}`,"
            else:
                # Return original
                return full_match
        
        # Fix JavaScript content properties with apostrophes
        content = re.sub(r"content:\s*(['\"])(.*?)\1(,)", fix_js_content, content, flags=re.DOTALL)
        
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
    
    # Find all demo HTML files
    demo_files = []
    for pattern in ["**/demos/*_demo.html"]:
        demo_files.extend(base_dir.glob(pattern))
    
    print(f"Found {len(demo_files)} demo files to check")
    
    fixed_count = 0
    for file_path in demo_files:
        if fix_file(file_path):
            fixed_count += 1
    
    print(f"\nCompleted: Fixed {fixed_count} files out of {len(demo_files)} total files")

if __name__ == "__main__":
    main()