# 🛠️ UNIX Shell Script Automation Tool

A powerful Python-based tool that automates commenting of lines in UNIX `.sh` scripts based on user-defined exclusion keywords, with intelligent section tracking, renumbering, and global replacements.

---

## 🚀 Features

- ✅ Parses `.sh` scripts and identifies `Section N` blocks  
- 📝 Accepts a `.txt` file with comma-separated exclusion keywords  
- 🔍 Scans each section for keyword matches and comments matching lines  
- 🧠 Tracks sections where changes were made  
- ❌ Fully comments out entire sections if all lines are matched  
- 🔢 Automatically renumbers remaining sections  
- 🔁 Globally replaces all variants of `bdi` (e.g. `_bdi_`, `bdi_`) with `"war"`  
- 📄 Optional changelog summary with section-wise details  
- 💡 Skips lines that were originally commented  
- 🔐 Non-destructive and easy to use  

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
# Section 3: Data Transformation
Template="Customer"
Sort --column name
GetTransNode
normalize_data
```

**After running the tool with matching keywords:**
```bash
# Section 2: Data Transformation
# Template="Customer"
# Sort --column name
# GetTransNode
# normalize_data
```

> If all lines in a section are commented, it renumbers the next section accordingly.

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
