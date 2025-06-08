#!/usr/bin/env python3
"""
unix_auto.py

Automates commenting-out of lines in a UNIX shell script based on exclusion keywords,
tracks changes per section, renumbers sections, performs global replacements of "bdi" → "war",
and optionally prints a changelog summary.

Usage:
    python3 unix_auto.py script.sh keywords.txt [-o modified.sh]
"""

import re
import argparse
import sys
from pathlib import Path

def parse_args():
    p = argparse.ArgumentParser(description="Automate commenting and renumbering of a .sh file.")
    p.add_argument("script", type=Path, help="Path to the input .sh script")
    p.add_argument("keywords", type=Path, help="Path to .txt file with comma-separated keywords (exclusion list)")
    p.add_argument("-o", "--output", type=Path, default=Path("mod1.sh"), help="Path for the modified output script")
    return p.parse_args()

def load_keywords(txt_path):
    text = txt_path.read_text(encoding="utf-8")
    return [kw.strip() for kw in text.split(",") if kw.strip()]

def detect_sections(lines):
    """
    Detect active sections defined using:
      if Jobstep "Section N: description" ; then
      ...
      fi
    Ignore commented-out headers.
    """
    sections = []
    start_re = re.compile(r'^.*Section\s+(\d+):.*$', re.IGNORECASE)
    end_re   = re.compile(r'^\s*fi\s*$', re.IGNORECASE)
    i = 0
    while i < len(lines):
        if lines[i].lstrip().startswith("#"):
            i += 1
            continue
        m = start_re.match(lines[i])
        if m:
            sec_num = int(m.group(1))
            start_idx = i
            i += 1
            while i < len(lines) and not end_re.match(lines[i]):
                i += 1
            end_idx = i if i < len(lines) else len(lines) - 1
            sections.append({
                "orig_num": sec_num,
                "header_idx": start_idx,
                "start_idx": start_idx,
                "end_idx": end_idx
            })
        i += 1
    return sections

def prefix_comment(line):
    """
    Comment a line, using '#' for headers/footers and '# ' for others.
    """
    indent = re.match(r'^(\s*)', line).group(1)
    stripped = line.lstrip().rstrip('\n')
    if stripped.startswith("if ") or stripped == "fi":
        return f"{indent}#{stripped}\n"
    else:
        return f"{indent}# {stripped}\n"

def main():
    args = parse_args()
    # Load and preprocess inline `; then fi` lines
    raw = args.script.read_text(encoding="utf-8").splitlines(keepends=True)
    orig_lines = []
    for ln in raw:
        stripped = ln.rstrip("\r\n")
        if '; then' in stripped and stripped.strip().endswith('fi'):
            head = stripped[:stripped.rfind('; then') + len('; then')]
            orig_lines.append(f"{head}\n")
            orig_lines.append("fi\n")
        else:
            orig_lines.append(ln)
    new_lines = orig_lines.copy()

    # Load keywords
    keywords = load_keywords(args.keywords)
    if not keywords:
        print("No keywords found in your .txt file; exiting.")
        sys.exit(1)

    # Mark originally commented lines
    orig_commented = [ln.lstrip().startswith("#") for ln in orig_lines]

    # Detect sections
    sections = detect_sections(orig_lines)
    if not sections:
        print("No sections detected. Exiting.")
        sys.exit(1)

    # Comment lines matching keywords
    mod_sections = set()
    for sec in sections:
        num = sec["orig_num"]
        for i in range(sec["start_idx"] + 1, sec["end_idx"]):
            if orig_commented[i]:
                continue
            for kw in keywords:
                if kw in new_lines[i]:
                    new_lines[i] = prefix_comment(new_lines[i])
                    mod_sections.add(num)
                    break

    # Detect fully commented sections and comment header/footer
    fully_commented = set()
    for sec in sections:
        num = sec["orig_num"]
        start = sec["start_idx"]
        end = sec["end_idx"]
        all_commented = True

        for i in range(start, end + 1):
            if new_lines[i].strip() == "":
                continue
            if not new_lines[i].lstrip().startswith("#"):
                all_commented = False
                break

        if all_commented:
            fully_commented.add(num)
        else:
            # Now check if all lines EXCEPT the header and fi are commented
            body_commented = True
            for i in range(start + 1, end):  # body only
                if new_lines[i].strip() == "":
                    continue
                if not new_lines[i].lstrip().startswith("#"):
                    body_commented = False
                    break

            if body_commented:
                fully_commented.add(num)
                # Comment the header and fi if not already
                if not new_lines[start].lstrip().startswith("#"):
                    new_lines[start] = prefix_comment(new_lines[start])
                if not new_lines[end].lstrip().startswith("#"):
                    new_lines[end] = prefix_comment(new_lines[end])

    # Build renumber map: only active sections, in file order
    active = [s for s in sections if s["orig_num"] not in fully_commented]
    active.sort(key=lambda s: s["header_idx"])
    renum_map = {s["orig_num"]: idx + 1 for idx, s in enumerate(active)}

    # Apply header renumbering by Section N
    header_re = re.compile(r'^(#?.*Section\s+)(\d+)(:.*)$', re.IGNORECASE)
    for idx, ln in enumerate(new_lines):
        m = header_re.search(ln)
        if m:
            old = int(m.group(2))
            if old in renum_map:
                new_lines[idx] = f"{m.group(1)}{renum_map[old]}{m.group(3)}\n"


    # Global replace of bdi variants → war
    for idx, ln in enumerate(new_lines):
        for pat in ("_bdi_", "_bdi", "bdi_", "bdi"):
            if pat in ln:
                new_lines[idx] = new_lines[idx].replace(pat, "war")

    # Write output
    args.output.write_text("".join(new_lines), encoding="utf-8")
    print(f"\nModified script saved to: {args.output}")

    # Changelog summary
    if input("Do you want a changelog summary? (y/n): ").strip().lower() == "y":
        print("\n===== CHANGELOG SUMMARY =====")
        if not mod_sections:
            print("No lines matched; no changes made.")
        else:
            print("Sections with keyword-based commenting:")
            for n in sorted(mod_sections):
                print(f"  • Section {n}")
            if fully_commented:
                print("\nSections fully commented-out and removed:")
                for n in sorted(fully_commented):
                    print(f"  • Original Section {n}")
                print("\nRenumbering applied to remaining sections:")
                for old, new in renum_map.items():
                    print(f"  • {old} → {new}")
            print("\nGlobal replacements:")
            print("  • All occurrences of '_bdi', '_bdi_', 'bdi_', 'bdi' → 'war'")
        print("=============================")

if __name__ == "__main__":
    main()