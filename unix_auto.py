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
    text = txt_path.read_text()
    # split on commas, strip whitespace, ignore empty
    return [kw.strip() for kw in text.split(",") if kw.strip()]

def detect_sections(lines):
    """
    Detect "Section N" headers anywhere in the file.
    Returns a list of dicts with keys:
      - orig_num (int)
      - header_idx (int)
      - header_prefix (str)
      - header_rest (str)
      - start_idx (int), end_idx (int) to be filled later
    """
    sec_re = re.compile(r'^(?P<prefix>\s*(?:#\s*)*Section\s+)(?P<num>\d+)(?P<rest>.*)$')
    secs = []
    for i, ln in enumerate(lines):
        m = sec_re.match(ln)
        if m:
            secs.append({
                "orig_num": int(m.group("num")),
                "header_idx": i,
                "header_prefix": m.group("prefix"),
                "header_rest": m.group("rest"),
                # placeholders
                "start_idx": i,
                "end_idx": None,
            })
    # set end_idx for each section
    for idx, sec in enumerate(secs):
        start = sec["header_idx"]
        end = (secs[idx+1]["header_idx"] - 1) if idx+1 < len(secs) else (len(lines)-1)
        sec["start_idx"] = start
        sec["end_idx"] = end
    return secs

def prefix_comment(line):
    # preserve leading whitespace indent, then "# "
    indent = re.match(r'^(\s*)', line).group(1)
    return f"{indent}# {line.lstrip()}"

def main():
    args = parse_args()

    # 1. Load files
    orig_lines = args.script.read_text(encoding="utf-8").splitlines(keepends=True)
    keywords = load_keywords(args.keywords)
    if not keywords:
        print("No keywords found in your .txt file; exiting.")
        sys.exit(1)

    # original commented flags
    orig_commented = [ln.lstrip().startswith("#") for ln in orig_lines]
    new_lines = orig_lines.copy()

    # 2. Detect sections
    sections = detect_sections(orig_lines)
    if not sections:
        print("No sections detected (no 'Section N' headers). Exiting.")
        sys.exit(1)

    # 3. Keyword-based line commenting
    mod_sections = set()
    for sec in sections:
        num = sec["orig_num"]
        for i in range(sec["start_idx"]+1, sec["end_idx"]+1):
            line = new_lines[i]
            if orig_commented[i]:
                continue
            for kw in keywords:
                if kw in line:
                    new_lines[i] = prefix_comment(line)
                    mod_sections.add(num)
                    break

    # 4. Detect fully commented sections
    fully_commented = set()
    for sec in sections:
        num = sec["orig_num"]
        # check all non-blank lines in section
        all_commented = True
        for i in range(sec["start_idx"]+1, sec["end_idx"]+1):
            ln = new_lines[i]
            if ln.strip() == "":
                continue
            if not ln.lstrip().startswith("#"):
                all_commented = False
                break
        if all_commented and num in mod_sections:
            fully_commented.add(num)
            # comment the header too, if not already
            hi = sec["header_idx"]
            if not new_lines[hi].lstrip().startswith("#"):
                new_lines[hi] = prefix_comment(new_lines[hi])

    # 5. Renumber remaining sections
    # build mapping old → new
    remaining = [sec["orig_num"] for sec in sections if sec["orig_num"] not in fully_commented]
    remaining.sort()
    renum_map = {old: new for new, old in enumerate(remaining, start=1)}

    sec_re = re.compile(r'^(?P<prefix>\s*(?:#\s*)*Section\s+)(?P<num>\d+)(?P<rest>.*)$')
    for idx, ln in enumerate(new_lines):
        m = sec_re.match(ln)
        if m:
            old = int(m.group("num"))
            if old in renum_map:
                new_num = renum_map[old]
                new_lines[idx] = f"{m.group('prefix')}{new_num}{m.group('rest')}\n"

    # 6. Global replacement of bdi variants → "war"
    # longest patterns first
    patterns = ["_bdi_", "_bdi", "bdi_", "bdi"]
    for idx, ln in enumerate(new_lines):
        for pat in patterns:
            if pat in ln:
                new_lines[idx] = new_lines[idx].replace(pat, "war")

    # 7. Write output
    args.output.write_text("".join(new_lines), encoding="utf-8")
    print(f"\nModified script saved to: {args.output}")

    # 8. Optional changelog summary
    want = input("Do you want a changelog summary? (y/n): ").strip().lower()
    if want == "y":
        print("\n===== CHANGELOG SUMMARY =====")
        if not mod_sections:
            print("No lines matched the keywords; no changes were made.")
        else:
            print("Sections with keyword-based commenting:")
            for num in sorted(mod_sections):
                print(f"  • Section {num}")
            if fully_commented:
                print("\nSections fully commented-out and removed:")
                for num in sorted(fully_commented):
                    print(f"  • Original Section {num}")
                print("\nRenumbering applied to remaining sections as follows:")
                for old, new in renum_map.items():
                    print(f"  • {old} → {new}")
            print("\nGlobal replacements:")
            print("  • All occurrences of '_bdi', '_bdi_', 'bdi_', 'bdi' replaced with 'war'.")
        print("=============================\n")
    else:
        print("Done. No summary requested.")

if __name__ == "__main__":
    main()
