#!/usr/bin/env python3
"""
unix_auto_complete.py - Complete version with all sophisticated features

Features:
1. Function-level commenting when all content is commented
2. Subsection detection and handling (stamp commands)
3. Section commenting when all body content is commented
4. Proper renumbering of only active sections
5. Detailed subsection tracking in changelog
"""

import re
import argparse
import sys
from pathlib import Path
from datetime import datetime

def parse_args():
    p = argparse.ArgumentParser(description="Complete shell script automation tool")
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
    if content.startswith("if ") or content.strip() == "fi" or content.startswith("function "):
        return f"{indent}#{content.rstrip()} -> **\n"
    else:
        return f"{indent}# {content.rstrip()} -> **\n"

def find_sections(lines):
    """Find JobStep sections with subsection detection."""
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
                'end': None,
                'subsections': []
            })
    
    # Find end of each section and detect subsections
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
        
        # Detect subsections (stamp commands)
        section['subsections'] = find_subsections(lines, section['start'] + 1, section['end'])
    
    return sections

def find_subsections(lines, start, end):
    """Find subsections marked by stamp commands."""
    subsections = []
    stamp_pattern = re.compile(r'^\s*stamp\s+"([^"]*)"', re.IGNORECASE)
    
    current_subsection = None
    
    for i in range(start, end):
        line = lines[i]
        match = stamp_pattern.match(line)
        
        if match:
            # Close previous subsection
            if current_subsection:
                current_subsection['end'] = i - 1
                subsections.append(current_subsection)
            
            # Start new subsection
            current_subsection = {
                'description': match.group(1).strip(),
                'start': i,
                'end': end - 1,
                'lines_commented': []
            }
    
    # Add last subsection
    if current_subsection:
        subsections.append(current_subsection)
    
    return subsections

def find_functions(lines):
    """Find function definitions."""
    functions = []
    func_pattern = re.compile(r'^\s*(?:function\s+(\w+)|(\w+)\s*\(\s*\))', re.IGNORECASE)
    
    for i, line in enumerate(lines):
        if line.lstrip().startswith("#"):
            continue
            
        match = func_pattern.match(line)
        if match:
            func_name = match.group(1) or match.group(2)
            start = i
            
            # Find function end - look for closing brace or next function/section
            end = len(lines) - 1
            for j in range(i + 1, len(lines)):
                line_content = lines[j].strip()
                
                # Look for closing brace
                if line_content == "}":
                    end = j
                    break
                
                # Look for next function or section
                if (re.match(r'^\s*(?:function\s+\w+|\w+\s*\(\s*\))', lines[j]) or
                    re.match(r'^\s*if\s+JobStep', lines[j])):
                    end = j - 1
                    break
            
            functions.append({
                'name': func_name,
                'start': start,
                'end': end,
                'lines_commented': []
            })    
    return functions

def find_loops(lines):
    """Find all loop structures (for, while, until, select, case) in the script."""
    loops = []
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Skip commented lines
        if stripped.startswith("#"):
            continue
            
        # Look for loop starters
        loop_patterns = [
            (r'^\s*for\s+', 'for'),
            (r'^\s*while\s+', 'while'),
            (r'^\s*until\s+', 'until'),
            (r'^\s*select\s+', 'select'),
            (r'^\s*case\s+', 'case')
        ]
        
        for pattern, loop_type in loop_patterns:
            if re.match(pattern, line):
                start = i
                
                # Find loop end
                end = len(lines) - 1
                bracket_count = 1  # We found the opening
                
                for j in range(i + 1, len(lines)):
                    inner_line = lines[j].strip()
                    
                    # Count nested loops
                    for inner_pattern, _ in loop_patterns:
                        if re.match(inner_pattern, lines[j]):
                            bracket_count += 1
                            break
                    
                    # Look for closing keywords
                    if loop_type == 'case' and inner_line == 'esac':
                        bracket_count -= 1
                    elif loop_type in ['for', 'while', 'until', 'select'] and inner_line == 'done':
                        bracket_count -= 1
                    
                    if bracket_count == 0:
                        end = j
                        break
                
                loops.append({
                    'type': loop_type,
                    'start': start,
                    'end': end,
                    'lines_commented': []
                })
                break  # Don't check other patterns for this line
    
    return loops

def find_case_statements(lines):
    """Find all case statements and their branches."""
    cases = []
    for i, line in enumerate(lines):
        if re.match(r'^\s*case\b', line) and not line.lstrip().startswith('#'):
            case_start = i
            # Find matching esac
            depth, j = 1, i + 1
            while j < len(lines) and depth > 0:
                l = lines[j]
                if re.match(r'^\s*case\b', l) and not l.lstrip().startswith('#'):
                    depth += 1
                elif re.match(r'^\s*esac\b', l) and not l.lstrip().startswith('#'):
                    depth -= 1
                j += 1
            case_end = j - 1
            # Find branches
            branches = []
            branch_start = None
            for k in range(case_start + 1, case_end):
                if re.match(r'^\s*[^#\s].*\)\s*$', lines[k]):
                    if branch_start is not None:
                        branches.append({'start': branch_start, 'end': k - 1})
                    branch_start = k
                elif re.match(r'^\s*;;\s*$', lines[k]):
                    if branch_start is not None:
                        branches.append({'start': branch_start, 'end': k})
                        branch_start = None
            cases.append({'start': case_start, 'end': case_end, 'branches': branches})
    return cases

def comment_case_branches_and_cases(lines, cases, keywords):
    """Comment case branches independently, and comment the whole case if all branches are commented."""
    for case in cases:
        all_branches_commented = True
        for branch in case['branches']:
            branch_lines = range(branch['start'], branch['end'] + 1)
            has_keyword = False
            all_commented = True
            for i in branch_lines:
                if any(re.search(rf'\b{re.escape(k)}\b', lines[i]) for k in keywords):
                    has_keyword = True
                    if not lines[i].lstrip().startswith('#'):
                        all_commented = False
                        break
            if has_keyword and all_commented:
                # Comment the branch pattern and all lines
                for i in branch_lines:
                    if not lines[i].lstrip().startswith('#') and lines[i].strip():
                        lines[i] = comment_line(lines[i])
            else:
                all_branches_commented = False
        # If all branches are commented, comment the whole case
        if all_branches_commented:
            for i in range(case['start'], case['end'] + 1):
                if not lines[i].lstrip().startswith('#') and lines[i].strip():
                    lines[i] = comment_line(lines[i])

def process_keyword_matching(lines, keywords, sections, functions, loops, orig_commented):
    """Process keyword matching with detailed tracking."""
    new_lines = lines.copy()
    stats = {
        'modified_sections': set(),
        'modified_functions': set(),
        'modified_loops': set(),
        'keyword_matches': {},
        'lines_modified': 0
    }
    
    # Process sections and subsections
    for section in sections:
        section_modified = False
        
        for subsection in section['subsections']:
            for i in range(subsection['start'], subsection['end'] + 1):
                if orig_commented[i]:
                    continue
                
                for keyword in keywords:
                    if keyword in new_lines[i]:
                        new_lines[i] = comment_line(new_lines[i])
                        subsection['lines_commented'].append(i)
                        section_modified = True
                        stats['lines_modified'] += 1
                        
                        # Track keyword usage
                        if keyword not in stats['keyword_matches']:
                            stats['keyword_matches'][keyword] = []
                        stats['keyword_matches'][keyword].append({
                            'line_num': i + 1,
                            'section': section['num'],
                            'subsection': subsection['description']
                        })
                        break
        
        # Also check lines outside subsections but inside the section
        for i in range(section['start'] + 1, section['end']):
            if orig_commented[i]:
                continue
                
            # Skip lines that are part of subsections
            in_subsection = any(sub['start'] <= i <= sub['end'] for sub in section['subsections'])
            if in_subsection:
                continue
            
            for keyword in keywords:
                if keyword in new_lines[i]:
                    new_lines[i] = comment_line(new_lines[i])
                    section_modified = True
                    stats['lines_modified'] += 1
                    
                    if keyword not in stats['keyword_matches']:
                        stats['keyword_matches'][keyword] = []
                    stats['keyword_matches'][keyword].append({
                        'line_num': i + 1,
                        'section': section['num'],
                        'subsection': 'General section content'
                    })
                    break
        
        if section_modified:
            stats['modified_sections'].add(section['num'])
    
    # Process functions
    for function in functions:
        function_modified = False
        
        for i in range(function['start'] + 1, function['end'] + 1):
            if orig_commented[i]:
                continue
            
            # Skip closing brace
            if lines[i].strip() == "}":
                continue
                
            for keyword in keywords:
                if keyword in new_lines[i]:
                    new_lines[i] = comment_line(new_lines[i])
                    function['lines_commented'].append(i)
                    function_modified = True
                    stats['lines_modified'] += 1
                    
                    if keyword not in stats['keyword_matches']:
                        stats['keyword_matches'][keyword] = []
                    stats['keyword_matches'][keyword].append({
                        'line_num': i + 1,
                        'function': function['name']
                    })
                    break
        
        if function_modified:
            stats['modified_functions'].add(function['name'])
    
    # Process loops
    for loop in loops:
        loop_modified = False
        
        for i in range(loop['start'] + 1, loop['end']):
            if orig_commented[i]:
                continue
            
            # Skip loop terminators and non-meaningful lines
            line_content = lines[i].strip()
            if (line_content in ['done', 'esac', ';;'] or
                line_content.endswith(')') and not line_content.startswith('stamp') or
                line_content.startswith('#') or
                not line_content):
                continue
                
            for keyword in keywords:
                if keyword in new_lines[i]:
                    new_lines[i] = comment_line(new_lines[i])
                    loop['lines_commented'].append(i)
                    loop_modified = True
                    stats['lines_modified'] += 1
                    
                    if keyword not in stats['keyword_matches']:
                        stats['keyword_matches'][keyword] = []
                    stats['keyword_matches'][keyword].append({
                        'line_num': i + 1,
                        'loop': f"{loop['type']} loop at line {loop['start'] + 1}"
                    })
                    break
        
        if loop_modified:
            stats['modified_loops'].add(f"{loop['type']}_line_{loop['start'] + 1}")
    
    return new_lines, stats

def check_fully_commented_structures(lines, sections, functions, loops, keywords):
    """Check and handle fully commented sections, functions, and loops with sophisticated logic."""
    fully_comented_sections = set()
    fully_comented_functions = set()
    fully_comented_loops = set()
    
    # Check sections - more sophisticated logic
    for section in sections:
        # Check if all non-empty, non-stamp content lines are commented
        all_content_commented = True
        has_content = False
        
        for i in range(section['start'] + 1, section['end']):
            line = lines[i]
            line_content = line.strip()
            
            # Skip empty lines
            if line_content == "":
                continue
                
            # Skip stamp lines (they are section structure, not content)
            if re.match(r'^\s*stamp\s+"', line, re.IGNORECASE):
                continue
            
            has_content = True
            
            # If this line is not commented, section is not fully commented
            if not line.lstrip().startswith("#"):
                all_content_commented = False
                break
        
        # If section has content and all content is commented, comment the whole section
        if has_content and all_content_commented:
            fully_comented_sections.add(section['num'])
            print(f"Section {section['num']} is fully commented - commenting header/footer")
            
            # Comment header and footer
            if not lines[section['start']].lstrip().startswith("#"):
                lines[section['start']] = comment_line(lines[section['start']])
            if not lines[section['end']].lstrip().startswith("#"):
                lines[section['end']] = comment_line(lines[section['end']])
                
            # Also comment all stamp lines in this section
            for subsection in section['subsections']:
                if not lines[subsection['start']].lstrip().startswith("#"):
                    lines[subsection['start']] = comment_line(lines[subsection['start']])    # Check functions - more sophisticated logic
    for function in functions:
        all_meaningful_content_commented = True
        has_meaningful_content = False
        
        for i in range(function['start'] + 1, function['end'] + 1):
            line = lines[i]
            line_content = line.strip()
            
            # Skip empty lines, closing braces, simple return statements, and stamp commands
            if (line_content == "" or 
                line_content == "}" or 
                line_content == "return 0" or 
                line_content == "return" or
                re.match(r'^\s*stamp\s+"', line, re.IGNORECASE)):
                continue
                
            has_meaningful_content = True
            
            # If this meaningful content line is not commented, function is not fully commented
            if not line.lstrip().startswith("#"):
                all_meaningful_content_commented = False
                break
        
        # If function has meaningful content and all meaningful content is commented, comment the whole function
        if has_meaningful_content and all_meaningful_content_commented:
            fully_comented_functions.add(function['name'])
            print(f"Function {function['name']} is fully commented - commenting declaration and all content")
            
            # Comment function declaration
            if not lines[function['start']].lstrip().startswith("#"):
                lines[function['start']] = comment_line(lines[function['start']])
            
            # Comment all lines within the function (including stamps)
            for i in range(function['start'] + 1, function['end']):
                if not lines[i].lstrip().startswith("#") and lines[i].strip():
                    lines[i] = comment_line(lines[i])
              # Comment closing brace if it exists
            if (function['end'] < len(lines) and 
                lines[function['end']].strip() == "}" and
                not lines[function['end']].lstrip().startswith("#")):
                lines[function['end']] = comment_line(lines[function['end']])    # Check loops for full commenting
    for loop in loops:
        has_keyword_content = False
        all_keyword_content_commented = True
        
        for i in range(loop['start'] + 1, loop['end']):
            line = lines[i]
            line_content = line.strip()
            
            # Skip empty lines and comments
            if (line_content == "" or line.lstrip().startswith("#")):
                continue
            
            # Skip loop structural elements
            if (line_content in ['done', 'esac', ';;'] or
                re.match(r'^\s*\w+.*\)\s*$', line_content) or  # case patterns  
                re.match(r'^\s*\*\)\s*$', line_content)):
                continue
            
            # Check if this line contains any keywords
            contains_keywords = any(keyword in line for keyword in keywords)
            
            if contains_keywords:
                has_keyword_content = True
                # If this keyword line is not commented, loop is not fully commented
                if not line.lstrip().startswith("#"):
                    all_keyword_content_commented = False
                    break
        
        # If loop has keyword content and all keyword content is commented, comment the whole loop
        if has_keyword_content and all_keyword_content_commented:
            fully_comented_loops.add(f"{loop['type']}_line_{loop['start'] + 1}")
            print(f"Loop {loop['type']} at line {loop['start'] + 1} is fully commented - commenting entire loop structure")
            
            # Comment loop start
            if not lines[loop['start']].lstrip().startswith("#"):
                lines[loop['start']] = comment_line(lines[loop['start']])
            
            # Comment all lines within the loop
            for i in range(loop['start'] + 1, loop['end']):
                if not lines[i].lstrip().startswith("#") and lines[i].strip():
                    lines[i] = comment_line(lines[i])
            
            # Comment loop end
            if (loop['end'] < len(lines) and 
                not lines[loop['end']].lstrip().startswith("#")):
                lines[loop['end']] = comment_line(lines[loop['end']])
    
    return fully_comented_sections, fully_comented_functions, fully_comented_loops

def renumber_sections(lines, sections, fully_comented_sections):
    """Renumber only active (non-fully-commented) sections and their stamp commands."""
    active_sections = [s for s in sections if s['num'] not in fully_comented_sections]
    active_sections.sort(key=lambda s: s['start'])
    
    renumber_map = {}
    
    for i, section in enumerate(active_sections):
        new_num = i + 1
        old_num = section['num']
        renumber_map[old_num] = new_num
        
        # Update section header
        header_line = lines[section['start']]
        updated_header = re.sub(
            r'(Section\s+)\d+(:)',
            f'\\g<1>{new_num}\\g<2>',
            header_line,
            flags=re.IGNORECASE
        )
        lines[section['start']] = updated_header
        
        # Update stamp commands within this section to use new section numbering
        update_stamp_commands_in_section(lines, section, new_num)
    
    return renumber_map

def update_stamp_commands_in_section(lines, section, new_section_num):
    """Update stamp commands within a section to use the new section numbering."""
    
    # Pattern 1: stamp "Section X.Y: description" 
    stamp_pattern_subsection = re.compile(r'^(\s*#?\s*stamp\s+"[^"]*Section\s+)(\d+)(\.\d+[^"]*")', re.IGNORECASE)
    
    # Pattern 2: stamp "Section X: description" (should become Section X.1: description)
    stamp_pattern_main = re.compile(r'^(\s*#?\s*stamp\s+"[^"]*Section\s+)(\d+)(:[^"]*")', re.IGNORECASE)
    
    for i in range(section['start'], section['end'] + 1):
        line = lines[i]
        
        # First check for subsection pattern (Section X.Y)
        match = stamp_pattern_subsection.match(line)
        if match:
            old_section_num = int(match.group(2))
            if old_section_num == section['num']:
                # Update the section number but keep the subsection number
                # Get everything after the matched pattern
                rest_of_line = line[match.end():]
                updated_line = f"{match.group(1)}{new_section_num}{match.group(3)}{rest_of_line}"
                lines[i] = updated_line
                continue
        
        # Then check for main section pattern (Section X:) and convert to Section X.1:
        match = stamp_pattern_main.match(line)
        if match:
            old_section_num = int(match.group(2))
            if old_section_num == section['num']:
                # Convert "Section X:" to "Section X.1:"
                description = match.group(3)[1:]  # Remove the colon, keep the closing quote
                # Get everything after the matched pattern
                rest_of_line = line[match.end():]
                updated_line = f"{match.group(1)}{new_section_num}.1:{description}{rest_of_line}"
                lines[i] = updated_line
                continue

def apply_global_replacements(lines):
    """Apply global text replacements."""
    replacement_count = 0
    patterns = ["_bdi_", "_bdi", "bdi_", "bdi"]
    target = "war"
    
    for i, line in enumerate(lines):
        original = line
        for pattern in patterns:
            if pattern in line:
                lines[i] = lines[i].replace(pattern, target)
        if lines[i] != original:
            replacement_count += 1
    
    return replacement_count

def generate_changelog(stats, sections, functions, fully_comented_sections, 
                      fully_comented_functions, renumber_map, global_replacements):
    """Generate detailed changelog."""
    changelog = []
    changelog.append("# ** CHANGELOG SUMMARY")
    changelog.append(f"# Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    changelog.append("#")
    
    if not stats['modified_sections'] and not stats['modified_functions']:
        changelog.append("# No modifications were made to the script.")
    else:
        # Modified sections with subsection details
        if stats['modified_sections']:
            changelog.append("# SECTIONS MODIFIED:")
            for sec_num in sorted(stats['modified_sections']):
                section = next(s for s in sections if s['num'] == sec_num)
                changelog.append(f"#   • Section {sec_num}: {section['description']}")
                
                # Show modified subsections
                for subsection in section['subsections']:
                    if subsection['lines_commented']:
                        changelog.append(f"#     - Subsection: {subsection['description']}")
            changelog.append("#")
        
        # Modified functions
        if stats['modified_functions']:
            changelog.append("# FUNCTIONS MODIFIED:")
            for func_name in sorted(stats['modified_functions']):
                changelog.append(f"#   • Function: {func_name}")
            changelog.append("#")
        
        # Fully commented sections
        if fully_comented_sections:
            changelog.append("# SECTIONS FULLY COMMENTED OUT:")
            for sec_num in sorted(fully_comented_sections):
                section = next(s for s in sections if s['num'] == sec_num)
                changelog.append(f"#   • Section {sec_num}: {section['description']}")
            changelog.append("#")
        
        # Fully commented functions
        if fully_comented_functions:
            changelog.append("# FUNCTIONS FULLY COMMENTED OUT:")
            for func_name in sorted(fully_comented_functions):
                changelog.append(f"#   • Function: {func_name}")
            changelog.append("#")
        
        # Section renumbering
        if renumber_map:
            changelog.append("# SECTION RENUMBERING:")
            for old, new in sorted(renumber_map.items()):
                changelog.append(f"#   • Section {old} → {new}")
            changelog.append("#")
        
        # Keyword match details
        if stats['keyword_matches']:
            changelog.append("# KEYWORD MATCH DETAILS:")
            for keyword, matches in stats['keyword_matches'].items():
                changelog.append(f"#   • Keyword '{keyword}' found in {len(matches)} locations:")
                for match in matches:
                    if 'section' in match:
                        changelog.append(f"#     - Line {match['line_num']}: Section {match['section']}, {match['subsection']}")
                    elif 'function' in match:
                        changelog.append(f"#     - Line {match['line_num']}: Function {match['function']}")
            changelog.append("#")
        
        # Global replacements
        if global_replacements > 0:
            changelog.append("# GLOBAL REPLACEMENTS:")
            changelog.append(f"#   • {global_replacements} lines modified")
            changelog.append("#   • All 'bdi' variants → 'war'")
            changelog.append("#")
    
    changelog.append("# END OF CHANGELOG")
    return "\n".join(changelog)

def insert_changelog(lines, changelog):
    """Insert changelog at the appropriate location - after header/docs but before script execution."""
    marker = "# ** CHANGELOG SUMMARY below"
    separator = "###############################################################"
    
    # First, try to find the explicit marker
    marker_idx = None
    separator_idx = None
    
    for i, line in enumerate(lines):
        if marker in line:
            marker_idx = i
        elif marker_idx is not None and separator in line:
            separator_idx = i
            break
    
    if marker_idx is not None and separator_idx is not None:
        # Insert between marker and separator
        result = lines[:marker_idx + 1]
        result.append("\n")
        result.extend([f"{line}\n" for line in changelog.split("\n")])
        result.append("\n")
        result.extend(lines[separator_idx:])
        return result
    
    # If no explicit marker found, find the smart insertion point
    insertion_point = find_smart_insertion_point(lines)
    
    if insertion_point is not None:
        result = lines[:insertion_point]
        result.append("\n")
        result.extend([f"{line}\n" for line in changelog.split("\n")])
        result.append("\n")
        result.extend(lines[insertion_point:])
        return result
    else:
        # Fallback: append to end
        print("Warning: Could not find appropriate insertion point. Appending to end.")
        lines.append(f"\n{changelog}\n")
        return lines

def find_smart_insertion_point(lines):
    """Find the appropriate insertion point after documentation but before script execution."""
    
    # Look for patterns that indicate the end of documentation and start of script execution
    script_start_patterns = [
        r'^\s*\.\s+\$HOME/',           # . $HOME/profile_*
        r'^\s*source\s+',              # source commands
        r'^\s*[A-Z_]+=',               # Variable assignments like vSrcFile=
        r'^\s*Init\s+',                # Init commands
        r'^\s*function\s+\w+',         # Function definitions
        r'^\s*if\s+JobStep',           # JobStep sections
        r'^\s*[a-zA-Z_][a-zA-Z0-9_]*\s*\(\s*\)\s*{',  # Function definitions
    ]
    
    # Look for the last comment block (usually REVISIONS HISTORY) followed by script execution
    last_comment_block_end = None
    in_comment_block = False
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Track comment blocks
        if stripped.startswith("#") and stripped != "#":
            in_comment_block = True
        elif stripped == "#" or stripped == "":
            # Empty line or just # - continue comment block
            continue
        else:
            # Non-comment line
            if in_comment_block:
                last_comment_block_end = i
                in_comment_block = False
            
            # Check if this line matches script execution patterns
            for pattern in script_start_patterns:
                if re.match(pattern, line):
                    # Found script execution start
                    if last_comment_block_end is not None:
                        # Insert after the last comment block but before script execution
                        return last_comment_block_end
                    else:
                        # Insert before this line if no comment block found
                        return i
    
    # If we reach here, try to find insertion point after shebang and initial comments
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Skip shebang, empty lines, and initial comment header
        if (stripped.startswith("#!") or 
            stripped == "" or 
            stripped.startswith("# SCRIPT") or
            stripped.startswith("# Purpose") or
            stripped.startswith("# Input") or
            stripped.startswith("# Output") or
            stripped.startswith("# Frequency") or
            stripped == "#"):
            continue
        
        # Look for REVISIONS HISTORY section
        if "REVISIONS HISTORY" in stripped or "REVISION HISTORY" in stripped:
            # Find the end of this section
            for j in range(i + 1, len(lines)):
                next_line = lines[j].strip()
                if next_line and not next_line.startswith("#"):
                    return j
        
        # If we find a non-comment line that looks like script execution, insert before it
        for pattern in script_start_patterns:
            if re.match(pattern, line):
                return i
      # Fallback: insert after line 10 if nothing else works
    return min(10, len(lines) - 1)

def fix_indentation(lines):
    """Fix indentation for lines inside if/fi blocks and function blocks."""
    fixed_lines = []
    block_stack = []  # Stack to track block types and indentation
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Skip empty lines
        if not stripped:
            fixed_lines.append(line)
            continue
        
        # Get original indentation
        indent_match = re.match(r'^(\s*)', line)
        original_indent = indent_match.group(1) if indent_match else ""
        
        # Fix lines that have multiple commands separated by excessive spaces
        # Look for pattern like: command1 >> file        command2
        if re.search(r'\S\s{6,}\S', line) and not stripped.startswith("#"):
            # Split on 6+ spaces and treat as separate lines
            parts = re.split(r'\s{6,}', line.strip())
            if len(parts) > 1:
                # First part
                if block_stack:
                    base_indent = block_stack[-1]['indent']
                    fixed_lines.append(f"{base_indent}    {parts[0]}\n")
                else:
                    fixed_lines.append(f"{original_indent}{parts[0]}\n")
                
                # Remaining parts
                for part in parts[1:]:
                    if part.strip():
                        if block_stack:
                            base_indent = block_stack[-1]['indent']
                            fixed_lines.append(f"{base_indent}    {part.strip()}\n")
                        else:
                            fixed_lines.append(f"{original_indent}{part.strip()}\n")
                continue
        
        # Comments - preserve as-is but adjust indentation if inside blocks
        if stripped.startswith("#"):
            if block_stack:
                # Inside a block - indent comments to match block level
                base_indent = block_stack[-1]['indent']
                content = line.lstrip()
                fixed_lines.append(f"{base_indent}    {content}")
            else:
                fixed_lines.append(line)
            continue        # Check for block starters
        if (re.match(r'^\s*if\s+', stripped) or 
            re.match(r'^\s*function\s+', stripped) or
            re.match(r'^\s*case\s+', stripped) or
            re.match(r'^\s*select\s+', stripped)):
            
            # This line starts a new block
            block_type = 'if'
            if stripped.startswith('function'):
                block_type = 'function'
            elif stripped.startswith('case'):
                block_type = 'case'
            elif stripped.startswith('for'):
                block_type = 'for'
            elif stripped.startswith('while'):
                block_type = 'while'
            elif stripped.startswith('until'):
                block_type = 'until'
            elif stripped.startswith('select'):
                block_type = 'select'
                
            block_stack.append({
                'type': block_type,
                'indent': original_indent
            })
            fixed_lines.append(line)  # Keep block starter line as-is
            continue
        
        # Check for block enders
        if (stripped == "fi" or stripped == "}" or stripped == "esac" or 
            stripped == "done"):
            # This line ends a block
            if block_stack:
                block_info = block_stack.pop()
                # Use the same indentation as the opening statement
                content = line.lstrip()
                fixed_lines.append(f"{block_info['indent']}{content}")
            else:
                fixed_lines.append(line)
            continue
        
        # Special handling for case patterns (lines ending with ) or ;;)
        if (re.match(r'^\s*\w+.*\)\s*$', stripped) or 
            re.match(r'^\s*\*\)\s*$', stripped) or
            stripped == ";;"):
            # Case pattern or case terminator - use base case indentation + 4 spaces
            if block_stack and block_stack[-1]['type'] == 'case':
                base_indent = block_stack[-1]['indent']
                content = line.lstrip()
                fixed_lines.append(f"{base_indent}    {content}")
            else:
                fixed_lines.append(line)
            continue
          # For lines inside blocks, add extra indentation
        if block_stack:
            # We're inside a block, add 4 spaces to the base block indentation
            base_indent = block_stack[-1]['indent']
            content = line.lstrip()
            
            # Special handling for case statements - content inside case patterns gets double indent
            if (block_stack[-1]['type'] == 'case' and 
                not re.match(r'^\s*\w+.*\)\s*$', stripped) and
                not re.match(r'^\s*\*\)\s*$', stripped) and
                stripped != ";;" and
                not stripped.startswith('case')):
                # This is content inside a case pattern - double indent
                new_indent = base_indent + "        "  # 8 spaces for case content
            else:
                # Regular block content - single indent
                new_indent = base_indent + "    "  # 4 spaces
                
            fixed_lines.append(f"{new_indent}{content}")
        else:
            # Not inside a block, keep original line
            fixed_lines.append(line)
    
    return fixed_lines

def process_script(script_path, keywords_path, output_path, verbose=False):
    """Main processing function."""
    print(f"Processing: {script_path}")
    
    # Load files
    try:
        lines = script_path.read_text(encoding="utf-8").splitlines(keepends=True)
        keywords = load_keywords(keywords_path)
        
        if not keywords:
            print("No keywords found!")
            return
        
        if verbose:
            print(f"Loaded {len(keywords)} keywords: {keywords}")
        print(f"Processing {len(lines)} lines...")
        
    except Exception as e:
        print(f"Error reading files: {e}")
        return
    
    # Mark originally commented lines
    orig_commented = [line.lstrip().startswith("#") for line in lines]
    new_lines = lines.copy()
      # Find structures
    sections = find_sections(lines)
    functions = find_functions(lines)
    loops = find_loops(lines)
    cases = find_case_statements(lines)
    
    if verbose:
        print(f"Found {len(sections)} sections, {len(functions)} functions, {len(loops)} loops, {len(cases)} cases")
        for section in sections:
            print(f"  Section {section['num']}: {section['description']} ({len(section['subsections'])} subsections)")
        for function in functions:
            print(f"  Function: {function['name']}")
        for loop in loops:
            print(f"  Loop: {loop['type']} at line {loop['start'] + 1}")
    
    # Process modifications
    new_lines, stats = process_keyword_matching(new_lines, keywords, sections, functions, loops, orig_commented)
    # Handle case branches and cases
    comment_case_branches_and_cases(new_lines, cases, keywords)
    # Check for fully commented structures (sections, functions, loops) and comment them if needed
    fully_comented_sections, fully_comented_functions, fully_comented_loops = check_fully_commented_structures(
        new_lines, sections, functions, loops, keywords
    )
    # Renumber active sections
    renumber_map = renumber_sections(new_lines, sections, fully_comented_sections)
    # Apply global replacements
    global_replacements = apply_global_replacements(new_lines)
    # Generate and insert changelog
    changelog = generate_changelog(stats, sections, functions, fully_comented_sections,
                                 fully_comented_functions, renumber_map, global_replacements)
    final_lines = insert_changelog(new_lines, changelog)
    # Fix indentation
    final_lines = fix_indentation(final_lines)
    # Write output
    try:
        output_path.write_text("".join(final_lines), encoding="utf-8")
        print(f"Output written to: {output_path}")
        
        # Print summary
        print(f"\nSUMMARY:")
        print(f"- Lines modified by keywords: {stats['lines_modified']}")
        print(f"- Sections modified: {len(stats['modified_sections'])}")
        print(f"- Functions modified: {len(stats['modified_functions'])}")
        print(f"- Sections fully commented: {len(fully_comented_sections)}")
        print(f"- Functions fully commented: {len(fully_comented_functions)}")
        print(f"- Global replacements: {global_replacements}")
        print(f"- Active sections renumbered: {len(renumber_map)}")
        
    except Exception as e:
        print(f"Error writing output: {e}")

def main():
    args = parse_args()
    
    if not args.script.exists():
        print(f"Error: Script file not found: {args.script}")
        sys.exit(1)
    
    if not args.keywords.exists():
        print(f"Error: Keywords file not found: {args.keywords}")
        sys.exit(1)
    
    process_script(args.script, args.keywords, args.output, args.verbose)

if __name__ == "__main__":
    main()
