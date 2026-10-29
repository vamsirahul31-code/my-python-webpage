# Timesheet Validator - Complete Setup Guide

A scalable, modular web application for validating timesheet entries against team-specific rules.

## 📋 Table of Contents
- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [How to Use](#how-to-use)
- [Adding New Teams](#adding-new-teams)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)

---

## ✨ Features

- **Team-Specific Rules**: Each team can have their own validation rules via JSON configuration
- **Web-Based Interface**: Modern, responsive UI built with Bootstrap
- **Automated Validation**: Validates timesheet entries against multiple rules:
  - Hours claimed after ticket closure
  - P1/P2 priority ticket activity code validation
  - Project ticket activity code validation
  - Governance activity code validation
  - Incident hour threshold checks
  - **NEW: Planned Leaves Validation** - Validates hours < 45 against planned leaves data
  - And more...
- **Planned Leaves Support**: Upload planned leaves file to validate low hours (< 45) against approved leaves
  - Supports weekly planned leaves (Sheet 1)
  - Supports city-wise planned leaves (Sheet 2)
  - Automatic validation with detailed messages
- **Excel Output**: Generates color-coded Excel files with:
  - Raw validated data
  - Dashboard with statistics and charts
  - Summary by team and ticket type
- **Easy Extensibility**: Add new teams by simply creating a JSON rules file

---

## 💻 System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **RAM**: Minimum 4GB (8GB recommended for large files)
- **Disk Space**: 500MB free space

---

## 🚀 Installation

### Step 1: Install Python

If you don't have Python installed:

**Windows:**
1. Download Python from https://www.python.org/downloads/
2. Run the installer
3. ✅ **IMPORTANT**: Check "Add Python to PATH" during installation

**Verify Installation:**
```bash
python --version
```

### Step 2: Navigate to Project Directory

Open Command Prompt (Windows) or Terminal (Mac/Linux) and navigate to the project:

```bash
cd C:\Users\Vamsikrishna\Desktop\timesheet-validator
```

### Step 3: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Flask (Web framework)
- pandas (Data processing)
- openpyxl (Excel file handling)
- numpy (Numerical operations)

---

## 🎯 Running the Application

### Start the Server

```bash
python run.py
```

You should see:
```
============================================================
🚀 Starting Timesheet Validator Application
============================================================

📋 Application Information:
   - Server: http://localhost:5000
   - Environment: Development
   - Debug Mode: Enabled

💡 Instructions:
   1. Open your browser and go to http://localhost:5000
   2. Select your team from the dropdown
   3. Upload your timesheet and ticket data files
   4. Click 'Validate Timesheet' to process
   5. Download the results Excel file

⚠️  Press CTRL+C to stop the server
============================================================
```

### Access the Application

Open your web browser and go to:
```
http://localhost:5000
```

---

## 📖 How to Use

### Step-by-Step Guide

1. **Select Your Team**
   - Choose your team from the dropdown (e.g., FPERPBAU, Finance, DigitalIntegration)
   - The system will automatically load the rules for your team

2. **Upload Timesheet File**
   - Click "Choose File" under "Timesheet File"
   - Select your weekly timesheet Excel file (Book1 format)
   - Supported formats: .xlsx, .xls

3. **Upload Ticket Data File**
   - Click "Choose File" under "Ticket Data File"
   - Select your incident/change/RITM data file (last 6 months)
   - This file should contain: Number, State, Resolved date, Priority columns

4. **Validate**
   - Click the "Validate Timesheet" button
   - Wait for processing (usually 10-30 seconds depending on file size)

5. **Review Results**
   - View summary statistics:
     - Total records processed
     - Allowed entries
     - Violations found
   - See detailed status breakdown

6. **Download Results**
   - Click "Download Validation Results"
   - Open the Excel file to see:
     - **Raw_Data**: All entries with color-coded validation status
     - **Dashboard**: Summary statistics and charts
     - **Summary**: Aggregated data by team and ticket type

### Understanding the Output

**Color Coding in Excel:**
- 🟢 **Green**: Valid/Allowed entries
- 🔴 **Red**: Violations (closure issues, hour limits exceeded)
- 🟡 **Yellow**: No hours claimed
- 🟣 **Purple**: P1/P2 activity code mismatch
- 🟤 **Brown**: Project/Governance rule violations
- 🔵 **Light Blue**: P1/P2 valid entries
- 🟠 **Orange**: Costed non-billable entries

---

## ➕ Adding New Teams

To add a new team, create a JSON rules file in the `rules/` folder:

### Step 1: Create Rules File

Create a new file: `rules/YourTeamName.json`

### Step 2: Define Rules

Use this template:

```json
{
  "team_name": "YourTeamName",
  "description": "Your Team Description",
  "teams_list": [
    "SubTeam1",
    "SubTeam2",
    "SubTeam3"
  ],
  "project_tickets": [
    "CHG2000000",
    "RITM4000000"
  ],
  "validation_rules": {
    "claimed_after_closure": {
      "enabled": true,
      "description": "Hours claimed after ticket closed",
      "days_allowed_after_closure": 0,
      "severity": "error",
      "color": "red",
      "message": "Claimed after ticket closed"
    },
    "priority_activity_code": {
      "enabled": true,
      "description": "P1/P2 tickets must use Activity Code 100C01",
      "priorities": ["P1", "P2"],
      "required_activity_code": "100C01",
      "severity": "error",
      "color": "purple",
      "valid_message": "P1/P2 Ticket Activity Code 100C01 - Valid",
      "error_message": "P1/P2 Ticket must use Activity Code 100C01"
    },
    "incident_hour_threshold": {
      "enabled": true,
      "description": "INC tickets should not exceed hour threshold",
      "max_hours": 9,
      "ticket_types": ["INC"],
      "severity": "warning",
      "color": "red",
      "message": "More hours claimed"
    }
  },
  "column_mappings": {
    "timesheet": {
      "description": "User defined task level description",
      "activity_code": "Activity Code",
      "workitem_title": "Workitem Title"
    },
    "incident": {
      "number": "Number",
      "state": "State",
      "resolved": "Resolved",
      "priority": "Priority"
    }
  }
}
```

### Step 3: Restart Application

Stop the server (CTRL+C) and restart it. Your new team will appear in the dropdown.

---

## 📁 Project Structure

```
timesheet-validator/
├── app/
│   ├── __init__.py              # Flask app initialization
│   ├── routes.py                # API endpoints
│   ├── validation_engine.py     # Core validation logic
│   ├── rules_loader.py          # Rules configuration loader
│   ├── file_handler.py          # File operations
│   └── utils.py                 # Helper functions
├── rules/
│   ├── FPERPBAU.json           # FPERPBAU team rules
│   ├── Finance.json            # Finance team rules
│   └── DigitalIntegration.json # Digital Integration rules
├── static/
│   ├── css/
│   │   └── style.css           # Custom styles
│   └── js/
│       └── main.js             # Frontend JavaScript
├── templates/
│   └── index.html              # Main web page
├── uploads/                     # Temporary upload storage
├── outputs/                     # Generated output files
├── config.py                    # Application configuration
├── requirements.txt             # Python dependencies
├── run.py                       # Application entry point
└── README.md                    # This file
```

---

## 🔧 Troubleshooting

### Issue: "Module not found" error

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: Port 5000 already in use

**Solution:**
Edit `run.py` and change the port:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Changed to 5001
```

### Issue: File upload fails

**Possible causes:**
1. File is too large (limit: 100MB)
2. File format is not .xlsx or .xls
3. File is corrupted

**Solution:**
- Check file size and format
- Try re-saving the Excel file
- Ensure file is not password-protected

### Issue: Validation fails with error

**Common causes:**
1. Missing required columns in input files
2. Incorrect date formats
3. Empty or corrupted data

**Solution:**
- Verify your files have all required columns
- Check the error message for specific details
- Ensure timesheet has: "User defined task level description", "Activity Code", "Workitem Title"
- Ensure ticket data has: "Number", "State", "Resolved", "Priority"

### Issue: Rules not loading for team

**Solution:**
1. Check that the JSON file exists in `rules/` folder
2. Verify JSON syntax is correct (use https://jsonlint.com/)
3. Restart the application

---

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review the error message in the browser console (F12)
3. Check the terminal/command prompt for detailed error logs

---

## 🎉 Success!

You're now ready to use the Timesheet Validator! 

**Quick Start:**
1. Run: `python run.py`
2. Open: http://localhost:5000
3. Upload files and validate!

---

## 📝 Notes

- Output files are stored in the `outputs/` folder
- Uploaded files are automatically cleaned up after processing
- Old output files (>7 days) can be cleaned manually from the `outputs/` folder
- The application runs in debug mode by default (suitable for local use)

---

**Version:** 1.0  
**Last Updated:** June 2026