#!/usr/bin/env python3
"""
Script to automatically fix common markdownlint issues in Markdown files.
"""

import re
import sys
from pathlib import Path

def fix_fenced_code_blocks(content):
    """Add language specifications to fenced code blocks."""
    # Find all code blocks and add appropriate language
    lines = content.split('\n')
    i = 0
    while i < len(lines):
        if lines[i].strip() == '```':
            # Look at context to determine language
            if i > 0:
                prev_line = lines[i-1].strip().lower()
                if any(word in prev_line for word in ['bash', 'shell', 'command', 'cli']):
                    lines[i] = '```bash'
                elif any(word in prev_line for word in ['python', 'python3']):
                    lines[i] = '```python'
                elif any(word in prev_line for word in ['json', 'yaml', 'yml', 'toml']):
                    ext = 'json' if 'json' in prev_line else ('yaml' if 'yaml' in prev_line else ('yml' if 'yml' in prev_line else 'toml'))
                    lines[i] = f'```{ext}`'
                elif i < len(lines) - 1 and lines[i+1].strip() and not lines[i+1].strip().startswith('#'):
                    # Check if next line looks like code
                    next_line = lines[i+1].strip()
                    if next_line.startswith('$') or next_line.startswith('panos-agent') or 'import ' in next_line:
                        lines[i] = '```bash' if next_line.startswith('$') else '```python'
                    else:
                        lines[i] = '```text'
                else:
                    lines[i] = '```text'
        i += 1
    return '\n'.join(lines)

def fix_long_lines(content, max_length=100):
    """Fix lines that are too long by breaking them at reasonable points."""
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        if len(line) <= max_length:
            new_lines.append(line)
            continue
            
        # Skip tables, code blocks, and URLs
        if '|' in line or line.strip().startswith('```') or 'http' in line:
            new_lines.append(line)
            continue
            
        # Try to break at natural points
        break_points = [', ', '. ', ' - ', ' and ', ' with ', ' for ', ' in ']
        
        for break_point in break_points:
            if break_point in line:
                parts = line.split(break_point)
                current_line = parts[0] + break_point
                
                for i, part in enumerate(parts[1:], 1):
                    if len(current_line + part) <= max_length - 2:  # Account for continuation
                        current_line += part + (break_point if i < len(parts) - 1 else '')
                    else:
                        new_lines.append(current_line.rstrip())
                        current_line = '  ' + part + (break_point if i < len(parts) - 1 else '')
                
                if current_line.strip():
                    new_lines.append(current_line.rstrip())
                break
        else:
            # If no natural break points, break at word boundaries
            words = line.split()
            current_line = ''
            for word in words:
                if len(current_line + ' ' + word) <= max_length:
                    current_line += (' ' + word if current_line else word)
                else:
                    if current_line:
                        new_lines.append(current_line)
                    current_line = '  ' + word
            if current_line:
                new_lines.append(current_line)
    
    return '\n'.join(new_lines)

def fix_blank_lines_around_lists(content):
    """Add blank lines around lists."""
    lines = content.split('\n')
    new_lines = []
    
    for i, line in enumerate(lines):
        # Check if this is a list item
        if re.match(r'^\s*[-*+]\s+', line) or re.match(r'^\s*\d+\.\s+', line):
            # Add blank line before if not already present
            if i > 0 and new_lines and new_lines[-1].strip() and not new_lines[-1].strip().startswith(('---', '#', '**', '*', '-', '+')):
                new_lines.append('')
            new_lines.append(line)
            # Add blank line after if next line is not a list item
            if i < len(lines) - 1 and not (re.match(r'^\s*[-*+]\s+', lines[i+1]) or re.match(r'^\s*\d+\.\s+', lines[i+1])):
                if lines[i+1].strip() and not lines[i+1].strip().startswith(('---', '#', '**', '*', '-', '+')):
                    new_lines.append('')
        else:
            new_lines.append(line)
    
    return '\n'.join(new_lines)

def fix_blank_lines_around_code_blocks(content):
    """Add blank lines around fenced code blocks."""
    lines = content.split('\n')
    new_lines = []
    
    for i, line in enumerate(lines):
        if line.strip().startswith('```'):
            # Add blank line before if not already present
            if i > 0 and new_lines and new_lines[-1].strip():
                new_lines.append('')
            new_lines.append(line)
            # Add blank line after if next line exists and is not blank
            if i < len(lines) - 1 and lines[i+1].strip():
                new_lines.append('')
        else:
            new_lines.append(line)
    
    return '\n'.join(new_lines)

def fix_bare_urls(content):
    """Wrap bare URLs in angle brackets."""
    # Find bare URLs (not already in brackets or parentheses)
    url_pattern = r'(?<!\[)(?<!\()(https?://[^\s\)]+)(?!\])(?!\))'
    return re.sub(url_pattern, r'<\1>', content)

def process_file(filepath):
    """Process a single markdown file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply fixes
        content = fix_fenced_code_blocks(content)
        content = fix_long_lines(content)
        content = fix_blank_lines_around_lists(content)
        content = fix_blank_lines_around_code_blocks(content)
        content = fix_bare_urls(content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Fixed: {filepath}")
            return True
        else:
            print(f"✓ No changes needed: {filepath}")
            return False
            
    except Exception as e:
        print(f"❌ Error processing {filepath}: {e}")
        return False

def main():
    """Main function."""
    if len(sys.argv) > 1:
        # Process specific files
        files = sys.argv[1:]
    else:
        # Process all markdown files in project
        project_root = Path("/Users/cdot/development/cdot65/paloaltonetworks-automation-examples/python/ai-agent-panos")
        files = []
        for md_file in project_root.rglob("*.md"):
            if ".venv" not in str(md_file):
                files.append(str(md_file))
    
    fixed_count = 0
    for filepath in files:
        if process_file(filepath):
            fixed_count += 1
    
    print(f"\n🎉 Processed {len(files)} files, fixed {fixed_count} files.")

if __name__ == "__main__":
    main()