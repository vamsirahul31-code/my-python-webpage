# ⚡ Quick Start Guide

Get up and running in 5 minutes!

## 🚀 Installation (One-Time Setup)

### 1. Open Command Prompt / Terminal

**Windows:** Press `Win + R`, type `cmd`, press Enter

### 2. Navigate to Project

```bash
cd C:\Users\Vamsikrishna\Desktop\timesheet-validator
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Wait for installation to complete (~2-3 minutes).

---

## ▶️ Running the Application

### Every Time You Want to Use It:

1. **Open Command Prompt / Terminal**

2. **Navigate to Project**
   ```bash
   cd C:\Users\Vamsikrishna\Desktop\timesheet-validator
   ```

3. **Start the Server**
   ```bash
   python run.py
   ```

4. **Open Browser**
   - Go to: http://localhost:5000
   - Or click the link in the terminal

5. **Use the Application**
   - Select your team
   - Upload timesheet file
   - Upload ticket data file
   - Click "Validate Timesheet"
   - Download results

6. **Stop the Server**
   - Press `CTRL + C` in the terminal

---

## 📝 Usage Example

### Input Files Required:

1. **Timesheet File** (Book1 format)
   - Must have columns: "User defined task level description", "Activity Code", "Workitem Title"
   - Date columns for each week

2. **Ticket Data File** (Last 6 months)
   - Must have columns: "Number", "State", "Resolved", "Priority"
   - Contains INC, CHG, RITM, PRB tickets

### Steps:

1. Select Team: `FPERPBAU`
2. Upload: `Book1 testing.xlsx`
3. Upload: `All Streams_Resolved_Incidents_This Month_v1.0.xlsx`
4. Click: `Validate Timesheet`
5. Wait: ~10-30 seconds
6. Download: `Validation_Result_FPERPBAU_YYYYMMDD_HHMMSS.xlsx`

---

## 🎨 Understanding Results

### Excel Output Contains:

1. **Raw_Data Sheet**
   - All your timesheet entries
   - Color-coded by validation status
   - Final_Status column shows result

2. **Dashboard Sheet**
   - Total records
   - Allowed vs Violations
   - Pie chart of status distribution

3. **Summary Sheet**
   - Breakdown by team and ticket type
   - Hours, count, and cost summaries

### Color Meanings:

- 🟢 **Green** = Valid entry
- 🔴 **Red** = Violation (fix required)
- 🟡 **Yellow** = No hours claimed
- 🟣 **Purple** = P1/P2 code issue
- 🟤 **Brown** = Project/Governance issue

---

## ❓ Common Issues

### "Module not found"
```bash
pip install -r requirements.txt
```

### "Port already in use"
- Close other applications using port 5000
- Or change port in `run.py` to 5001

### "File upload failed"
- Check file is .xlsx or .xls
- File size must be < 100MB
- File must not be password-protected

---

## 🎯 Tips

- Keep your ticket data file updated (last 6 months)
- Use the same file format as your original timesheet
- Download results immediately (files auto-cleanup after 7 days)
- Each team can have different rules

---

## 📞 Need Help?

1. Check the full README.md for detailed instructions
2. Look at error messages in browser (F12 for console)
3. Check terminal for detailed logs

---

**That's it! You're ready to validate timesheets! 🎉**