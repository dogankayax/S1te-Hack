
# SQL Injection Scanner 🔍



> Professional SQL Injection vulnerability detection tool powered by SQLMap

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![SQLMap](https://img.shields.io/badge/powered%20by-sqlmap-red)](https://sqlmap.org/)

## 🚀 Features

- ✅ **Automated SQL Injection Detection**
- ✅ **Multiple Scan Levels** (Quick, Medium, Detailed)
- ✅ **Database Exploration** (Databases, Tables, Columns)
- ✅ **Data Extraction Capabilities**
- ✅ **Real-time Progress Tracking**
- ✅ **User-friendly Interface**
- ✅ **Color-coded Output**

## 📋 Requirements

### System Requirements
- **Kali Linux** (Recommended) or any Linux distribution
- **Python 3.6+**
- **SQLMap** (Automatically checked)

### Python Dependencies
```bash
pip install -r requirements.txt
🛠 Installation
Method 1: Quick Install
bash
git clone https://github.com/yourusername/sql-injection-scanner.git
cd sql-injection-scanner
pip install -r requirements.txt
chmod +x sql_scanner.py
Method 2: Manual Install
bash
# Install SQLMap (Kali Linux)
sudo apt update && sudo apt install sqlmap

# Install Python dependencies
pip install colorama

# Run the tool
python3 sql_scanner.py
🎯 Usage
Basic Usage
bash
python3 sql_scanner.py
Scan Modes
Simple Mode - Direct SQLMap execution (Recommended)

Advanced Mode - Interactive step-by-step scanning

Example Target URLs
text
http://testphp.vulnweb.com/artists.php?artist=1
https://example.com/page.php?id=1
http://test.site/products.php?category=2
🔧 Scan Levels
Level	Description	Command
🟢 Quick	Fast basic checks	--level 1 --risk 1
🟡 Medium	Balanced approach	--level 3 --risk 2
🔴 Detailed	Comprehensive scan	--level 5 --risk 3
⚡ Quick Start
bash
# Clone repository
git clone https://github.com/yourusername/sql-injection-scanner.git
cd sql-injection-scanner

# Install dependencies
pip install -r requirements.txt

# Run tool
python3 sql_scanner.py

# Follow the interactive prompts
🎮 Interactive Features
URL Validation - Checks for proper URL format

SQLMap Detection - Verifies SQLMap installation

Real-time Output - Live scanning progress

Database Navigation - Explore databases interactively

Data Export - Dump table contents

🛡️ Legal Disclaimer
⚠️ This tool is for educational and authorized testing purposes only.

Only use on websites you own or have explicit permission to test

Unauthorized testing is illegal and unethical

Developers are not responsible for misuse

Comply with all applicable laws and regulations

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments
SQLMap Team - For the amazing SQLMap tool

Colorama - For cross-platform colored terminal text