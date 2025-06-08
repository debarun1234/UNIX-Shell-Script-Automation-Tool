# 🛠️ UNIX Shell Script Automation Tool

A powerful Python-based tool that automates commenting of lines in UNIX `.sh` scripts based on user-defined exclusion keywords, with intelligent section tracking, full-block commenting, renumbering, and global replacements.

---

## 🚀 Features

- ✅ Parses `.sh` scripts and identifies `Section N:` blocks (with case-insensitive and position-flexible matching)
- 📝 Accepts a `.txt` file with comma-separated exclusion keywords
- 🔍 Scans each section for keyword matches and comments matching lines
- 🧠 Tracks which sections were modified
- ❌ Fully comments out the entire section (`if`, lines, and `fi`) if all lines get commented
- 🔢 Automatically renumbers remaining sections using `Section N:` logic, even inside commented lines
- 🔁 Globally replaces all variants of `bdi` (`_bdi_`, `_bdi`, `bdi_`, `bdi`) with `"war"`
- 📄 Optional changelog summary with section-wise breakdown and renumbering map
- 💡 Skips originally commented lines (doesn't double-comment)
- 🔐 Works on mixed-style shell scripts with `; then fi`, varying indentation, and flexible formats

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

**Input Section:**
```bash
if JobStep "Section 3: Data Transformation" ; then
Template="Customer"
Sort --column name
GetTransNode
normalize_data
fi
```

**After running the tool with matching keywords:**
```bash
#if JobStep "Section 2: Data Transformation" ; then
# Template="Customer"
# Sort --column name
# GetTransNode
# normalize_data
#fi
```

> If all lines in a section are commented, it comments the entire block and renumbers subsequent sections.

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

Built by **Your Name**

📫 Reach me on GitHub for contributions, issues, or feature requests.

---

## 📜 License

**MIT License** — Free to use, modify, and distribute with credit.
