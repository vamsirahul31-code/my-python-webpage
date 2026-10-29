# Planned Leaves Validation Feature

## Overview
This feature validates timesheet entries with less than 45 hours against planned leaves data. When an employee's weekly timesheet shows less than 45 hours, the system checks if they have planned leaves to justify the reduced hours.

## How It Works

### 1. Planned Leaves File Format
Upload an Excel file with **two sheets**:

#### Sheet 1: Weekly Planned Leaves
Contains weekly planned leaves for all employees.

**Required Columns:**
- `Employee ID` (or `Emp ID`, `ID`, `Employee`)
- Week date columns in `DD-MM-YYYY` format (e.g., `28-06-2026`)
- Leave values in cells (e.g., "PL", "SL", "CL", "Vacation")

**Example:**
```
| Employee ID | Employee Name | 21-06-2026 | 28-06-2026 | 05-07-2026 |
|-------------|---------------|------------|------------|------------|
| EMP001      | John Doe      | PL         |            | SL         |
| EMP002      | Jane Smith    |            | CL         |            |
```

#### Sheet 2: City-wise Planned Leaves
Contains planned leaves organized by city/location (e.g., Bangalore, Mumbai, etc.).

**Required Columns:**
- `City` (or `Location`, `Office`)
- `Employee ID` (or `Emp ID`, `ID`, `Employee`)
- Week date columns in `DD-MM-YYYY` format
- Leave values in cells

**Example:**
```
| City      | Employee ID | Employee Name | 21-06-2026 | 28-06-2026 |
|-----------|-------------|---------------|------------|------------|
| Bangalore | EMP001      | John Doe      | PL         |            |
| Mumbai    | EMP003      | Bob Wilson    |            | CL         |
```

### 2. Validation Logic

When processing timesheets, the system:

1. **Calculates total hours** for each employee entry
2. **If total hours < 45**, checks for planned leaves:
   - First checks Sheet 1 (Weekly Planned Leaves) for the employee
   - Then checks Sheet 2 (City-wise Planned Leaves) if city information is available
3. **Validation Results:**
   - ✅ **Valid**: Employee has planned leave for the week(s) with low hours
   - ❌ **Invalid**: No planned leave found - requires justification
   - ⚠️ **Warning**: Planned leaves file not provided or employee ID missing

### 3. Validation Messages

The system generates specific messages based on the validation:

- `"Hours < 45 but has planned leave: 21-06-2026 (PL), 28-06-2026 (SL)"` - Valid with leave details
- `"Hours < 45 (38.5h) with NO planned leave - Requires justification"` - Invalid, needs explanation
- `"Hours < 45 (42.0h) - Cannot validate (Employee ID missing)"` - Cannot validate without employee ID
- `"Hours < 45 (40.0h) - Planned leaves file not provided"` - File not uploaded

### 4. Configuration

Enable/disable this validation in your team's rules JSON file:

```json
{
  "validation_rules": {
    "low_hours_planned_leave": {
      "enabled": true,
      "description": "Validate hours < 45 against planned leaves",
      "min_hours_threshold": 45,
      "severity": "warning",
      "color": "light_yellow",
      "message": "Hours less than 45 - Check planned leaves"
    }
  }
}
```

## Usage Instructions

### Step 1: Prepare Your Planned Leaves File
1. Create an Excel file with two sheets as described above
2. Ensure employee IDs match those in your timesheet
3. Use consistent date format: `DD-MM-YYYY`
4. Fill in leave types (PL, SL, CL, etc.) for planned leave weeks

### Step 2: Upload Files
1. Go to the Timesheet Validator web interface
2. Select your team
3. Upload your timesheet file
4. Upload ticket data files (Incident, RITM, Problem, Change)
5. **Upload your Planned Leaves file** (optional but recommended)
6. Click "Validate Timesheet"

### Step 3: Review Results
The validation results will show:
- Color-coded entries based on validation status
- Detailed messages for entries with < 45 hours
- Summary of planned leaves found/not found

## Benefits

✅ **Automated Validation**: No manual checking of leave records  
✅ **Compliance**: Ensures low hours are justified with planned leaves  
✅ **Transparency**: Clear messages about leave status  
✅ **Flexibility**: Works with or without the planned leaves file  
✅ **Multi-location Support**: Handles city-wise leave data

## Technical Details

### Files Modified/Created
- `app/planned_leaves_handler.py` - New module for handling planned leaves
- `app/validation_engine.py` - Updated with planned leaves validation logic
- `app/routes.py` - Added planned leaves file upload handling
- `templates/index.html` - Added UI for planned leaves file upload
- `rules/FPERPBAU.json` - Added `low_hours_planned_leave` rule configuration

### Key Classes
- `PlannedLeavesHandler`: Manages loading and querying planned leaves data
- `ValidationEngine`: Integrates planned leaves validation into timesheet validation

### API Changes
The `/api/validate` endpoint now accepts an additional optional parameter:
- `planned_leaves_file`: Excel file with planned leaves data

## Troubleshooting

### Issue: "Cannot validate (Employee ID missing)"
**Solution**: Ensure your timesheet contains an Employee ID column (Employee ID, Emp ID, Resource ID, or Resource)

### Issue: Planned leaves not being detected
**Solution**: 
- Check that employee IDs match exactly between timesheet and planned leaves file
- Verify date columns are in `DD-MM-YYYY` format
- Ensure leave values are not empty in the planned leaves file

### Issue: City-wise leaves not working
**Solution**:
- Verify Sheet 2 has a City/Location column
- Check that city names match between timesheet and planned leaves file
- Ensure employee-to-city mapping is correct

## Example Scenario

**Timesheet Entry:**
- Employee: EMP001
- Week: 21-06-2026 to 27-06-2026
- Total Hours: 32 hours (< 45)

**Planned Leaves File (Sheet 1):**
- EMP001 has "PL" marked for 21-06-2026

**Validation Result:**
✅ `"Hours < 45 but has planned leave: 21-06-2026 (PL)"`

---

**Made with Bob** 🤖