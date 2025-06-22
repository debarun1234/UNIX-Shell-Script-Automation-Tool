# 🛠️ UNIX Shell Script Automation Tool

A powerful Python-based tool that automates commenting of lines and blocks in UNIX `.sh` scripts based on user-defined exclusion keywords, with intelligent section tracking, full-block and nested structure commenting, renumbering, and global replacements.

---

## 🚀 Features

- ✅ Parses `.sh` scripts and identifies `Section N:` blocks (with case-insensitive and position-flexible matching)
- 📝 Accepts a `.txt` file with comma-separated exclusion keywords
- 🔍 Scans each section for keyword matches and comments matching lines (exact word match, not substring)
- 🧠 Tracks which sections, functions, and loops were modified
- ❌ Fully comments out the entire section (`if`, lines, and `fi`) if all lines get commented
- 🔢 Automatically renumbers remaining sections using `Section N:` logic, even inside commented lines
- 🔁 Globally replaces all variants of `bdi` (`_bdi_`, `_bdi`, `bdi_`, `bdi`) with `"war"`
- 📄 Changelog summary with section/function/loop breakdown and renumbering map
- 💡 Skips originally commented lines (doesn't double-comment)
- 🔐 Works on mixed-style shell scripts with `; then fi`, varying indentation, and flexible formats
- 🧩 **NEW:** Handles `case` branches (restricted/unrestricted) independently; comments entire `case` if all branches are commented
- 🌀 **NEW:** Handles `for`, `while`, `until`, `select` loops and nested structures (inside-out scanning)
- 🏗️ **NEW:** Comments entire function if all inside components (lines, cases, loops) are commented
- 📝 **NEW:** Changelog and renumbering now reflect all advanced block/structure logic

---

## 📁 Directory Structure

```
├── unix_auto.py         # Main Python automation script
├── test_script.sh       # Sample shell script to test the tool
├── keywords.txt         # Comma-separated list of exclusion keywords
└── README.md            # This documentation file
```

---

## 🧑‍💻 How to Use

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/unix-script-automation.git
cd unix-script-automation
```

### 2. Prepare Your Files

- Place your shell script (e.g. `myscript.sh`) in the repo
- Prepare a `keywords.txt` file with comma-separated keywords (e.g., `db2_connect,db2_sql,GetTransNode`)

### 3. Run the Tool

```bash
python3 unix_auto.py myscript.sh keywords.txt -o modified_script.sh
```

> ✅ Optional: View changelog when prompted

---

## 🧪 Sample Output

**Input Section with Nested Structures:**
```bash
function processDataFiles {
    select mode in "FAST" "NORMAL"; do
        case $mode in
            FAST)
                process_fast
                break
            ;;
            NORMAL)
                # ChunkSql -> commented due to 2AOR Migration
                # Sqlstats -> commented due to 2AOR Migration
                break
            ;;
        esac
    done
    return 0
}
```

**After running the tool with matching keywords:**
```bash
#function processDataFiles { -> commented due to 2AOR Migration
#    select mode in "FAST" "NORMAL"; do -> commented due to 2AOR Migration
#        case $mode in -> commented due to 2AOR Migration
#            FAST) -> commented due to 2AOR Migration
#                process_fast -> commented due to 2AOR Migration
#                break -> commented due to 2AOR Migration
#            ;; -> commented due to 2AOR Migration
#            NORMAL) -> commented due to 2AOR Migration
#                # ChunkSql -> commented due to 2AOR Migration
#                # Sqlstats -> commented due to 2AOR Migration
#                break -> commented due to 2AOR Migration
#            ;; -> commented due to 2AOR Migration
#        esac -> commented due to 2AOR Migration
#    done -> commented due to 2AOR Migration
#    return 0 -> commented due to 2AOR Migration
#} -> commented due to 2AOR Migration
```

> If all lines in a section, function, or case/loop block are commented, the tool comments the entire block and renumbers subsequent sections.

**Changelog Example:**
```
===== CHANGELOG SUMMARY =====
Sections/Functions/Loops with keyword-based commenting:
  • Section 2
  • Function: processDataFiles
  • Loop: select at line 3
  • Case: $mode in at line 4

Sections/functions fully commented-out and removed:
  • Original Section 2
  • Function: processDataFiles

Renumbering applied to remaining sections:
  • 1 → 1
  • 4 → 2
  • 5 → 3
  • 6 → 4

Global replacements:
  • All occurrences of '_bdi', '_bdi_', 'bdi_', 'bdi' → 'war'
=============================
```

---

## 🧠 Supported Replacements

After script processing, the tool will also replace these variants globally:

| Original   | Replaced With |
|------------|----------------|
| `_bdi_`    | `war`          |
| `_bdi`     | `war`          |
| `bdi_`     | `war`          |
| `bdi`      | `war`          |

---

## 🛑 No External Dependencies

This tool is 100% Python standard library. No pip installs needed.

**Compatible with:**
- Python 3.6+
- Linux, macOS, or Windows (with bash script support)

---

## 👨‍💻 Author

Built by **Debarun Ghosh**

📫 Reach me on GitHub for contributions, issues, or feature requests.

---

## 📜 License

**MIT License** — Free to use, modify, and distribute with credit.
