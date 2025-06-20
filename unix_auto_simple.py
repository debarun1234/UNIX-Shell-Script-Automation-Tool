#!/usr/bin/env python3
"""
unix_auto_simple.py - Simplified version with basic keyword commenting

Simple logic:
1. Comment lines containing keywords
2. Basic section detection and renumbering
3. Global replacements
4. No complex loop or case handling
"""

import re
import argparse
import sys
from pathlib import Path
from datetime import datetime

def parse_args():
    p = argparse.ArgumentParser(description="Simple shell script automation tool")
    p.add_argument("script", type=Path, help="Input .sh script")
    p.add_argument("keywords", type=Path, help="Keywords file")
    p.add_argument("-o", "--output", type=Path, default=Path("modified.sh"), help="Output file")
    p.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    return p.parse_args()

def load_keywords(txt_path):
    """Load keywords from file."""
    try:
        text = txt_path.read_text(encoding="utf-8")
        keywords = [kw.strip() for kw in text.split(",") if kw.strip()]
        return keywords
    except Exception as e:
        print(f"Error loading keywords: {e}")
        return []

def comment_line(line):
    """Add comment to a line if not already commented."""
    if line.lstrip().startswith("#"):
        return line  # Already commented
    
    # Find indentation
    indent_match = re.match(r'^(\s*)', line)
    indent = indent_match.group(1) if indent_match else ""
    content = line.lstrip()
    
    # Different comment styles
    if content.startswith("if ") or content.strip() == "fi":
        return f"{indent}#{content.rstrip()} -> commented due to 2AOR Migration\n"
    else:
        return f"{indent}# {content.rstrip()} -> commented due to 2AOR Migration\n"

def find_sections(lines):
    """Find JobStep sections."""
    sections = []
    section_pattern = re.compile(r'if\s+JobStep\s+"Section\s+(\d+):\s*([^"]*)"', re.IGNORECASE)
    
    for i, line in enumerate(lines):
        if line.lstrip().startswith("#"):
            continue
        match = section_pattern.search(line)
        if match:
            sections.append({
                'num': int(match.group(1)),
                'description': match.group(2).strip(),
                'start': i,
                'end': None
            })
    
    # Find end of each section
    for i, section in enumerate(sections):
        # Find the closing 'fi' for this section
        brace_count = 1
        j = section['start'] + 1
        
        while j < len(lines) and brace_count > 0:
            line = lines[j].strip()
            if not lines[j].lstrip().startswith("#"):
                if line.startswith("if "):
                    brace_count += 1
                elif line == "fi":
                    brace_count -= 1
            j += 1
        
        section['end'] = j - 1 if brace_count == 0 else len(lines) - 1
    
    return sections

def process_script(lines, keywords):
    """Process the script with basic keyword commenting."""
    new_lines = lines.copy()
    stats = {
        'lines_modified': 0,
        'modified_sections': set()
    }
    
    # Track which lines were originally commented
    originally_commented = [line.lstrip().startswith("#") for line in lines]
    
    # Comment lines containing keywords
    for i, line in enumerate(new_lines):
        if originally_commented[i]:
            continue
        
        for keyword in keywords:
            if keyword in line:
                new_lines[i] = comment_line(line)
                stats['lines_modified'] += 1
                break
    
    return new_lines, stats

def renumber_sections(lines, sections):
    """Renumber sections sequentially."""
    # Check which sections are fully commented
    fully_commented_sections = set()
    
    for section in sections:
        all_content_commented = True
        has_content = False
        
        for i in range(section['start'] + 1, section['end']):
            line_content = lines[i].strip()
            
            # Skip empty lines
            if line_content == "":
                continue
            
            has_content = True
            
            # If this line is not commented, section is not fully commented
            if not lines[i].lstrip().startswith("#"):
                all_content_commented = False
                break
        
        # If section has content and all content is commented, mark it as fully commented
        if has_content and all_content_commented:
            fully_commented_sections.add(section['num'])
            
            # Comment header and footer if not already commented
            if not lines[section['start']].lstrip().startswith("#"):
                lines[section['start']] = comment_line(lines[section['start']])
            if not lines[section['end']].lstrip().startswith("#"):
                lines[section['end']] = comment_line(lines[section['end']])
    
    # Renumber only active sections
    active_sections = [s for s in sections if s['num'] not in fully_commented_sections]
    active_sections.sort(key=lambda s: s['start'])
    
    for i, section in enumerate(active_sections):
        new_num = i + 1
        old_num = section['num']
        
        # Update section header
        header_line = lines[section['start']]
        updated_header = re.sub(
            r'(Section\s+)\d+(:)',
            f'\\g<1>{new_num}\\g<2>',
            header_line,
            flags=re.IGNORECASE
        )
        lines[section['start']] = updated_header
    
    return fully_commented_sections

def apply_global_replacements(lines):
    """Apply global replacements."""
    replacements = 0
    
    for i, line in enumerate(lines):
        original_line = line
        # Replace bdi variants with war
        for pattern in ['_bdi_', '_bdi', 'bdi_', 'bdi']:
            if pattern in line:
                line = line.replace(pattern, pattern.replace('bdi', 'war'))
                replacements += 1
        lines[i] = line
    
    return replacements

def insert_changelog(lines):
    """Insert changelog after documentation block."""
    changelog = [
        "\n",
        "# CHANGELOG SUMMARY\n",
        f"# Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
        "#\n",
        "# Lines containing keywords have been commented out due to 2AOR Migration.\n",
        "# Sections with all content commented have been fully commented and renumbered.\n",
        "# Global replacements: 'bdi' variants → 'war' variants\n",
        "# END OF CHANGELOG\n",
        "\n"
    ]
    
    # Find where to insert (after documentation block, before main execution)
    insert_pos = 0
    in_doc_block = True
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Skip initial comments and empty lines
        if stripped.startswith("#") or stripped == "":
            continue
        
        # Found first non-comment line
        if in_doc_block:
            insert_pos = i
            in_doc_block = False
            break
    
    # Insert changelog
    for j, changelog_line in enumerate(changelog):
        lines.insert(insert_pos + j, changelog_line)
    
    return len(changelog)

def main():
    args = parse_args()
    
    try:
        script_path = args.script
        keywords_path = args.keywords
        output_path = args.output
        
        # Load files
        lines = script_path.read_text(encoding='utf-8').splitlines(keepends=True)
        keywords = load_keywords(keywords_path)
        
        if args.verbose:
            print(f"Processing: {script_path}")
            print(f"Loaded {len(keywords)} keywords: {keywords}")
            print(f"Processing {len(lines)} lines...")
        
    except Exception as e:
        print(f"Error reading files: {e}")
        return
    
    # Find sections
    sections = find_sections(lines)
    
    if args.verbose:
        print(f"Found {len(sections)} sections")
        for section in sections:
            print(f"  Section {section['num']}: {section['description']}")
    
    # Process script
    new_lines, stats = process_script(lines, keywords)
    
    # Insert changelog
    changelog_lines_added = insert_changelog(new_lines)
    
    # Adjust section positions for changelog insertion
    for section in sections:
        section['start'] += changelog_lines_added
        section['end'] += changelog_lines_added
    
    # Renumber sections
    fully_commented_sections = renumber_sections(new_lines, sections)
    
    # Apply global replacements
    global_replacements = apply_global_replacements(new_lines)
    
    # Write output
    try:
        output_path.write_text(''.join(new_lines), encoding='utf-8')
        print(f"Output written to: {output_path}")
    except Exception as e:
        print(f"Error writing output: {e}")
        return
    
    # Print summary
    if args.verbose:
        print(f"\nSUMMARY:")
        print(f"- Lines modified by keywords: {stats['lines_modified']}")
        print(f"- Sections fully commented: {len(fully_commented_sections)}")
        print(f"- Global replacements: {global_replacements}")

if __name__ == "__main__":
    main()
