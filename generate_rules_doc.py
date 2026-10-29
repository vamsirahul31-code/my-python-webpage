"""
Script to generate a Validation Rules Documentation Excel file.
Columns:
  A - Rule Name
  B - How It Is Validated (logic description)
  C - Applies To (ticket types)
  D - Condition / Trigger
  E - Output Message
  F - Severity
  G - Colour in Report
"""
import openpyxl
from openpyxl.styles import (
    PatternFill, Font, Alignment, Border, Side
)
from openpyxl.utils import get_column_letter

# ── colour palette ────────────────────────────────────────────────────────────
HEADER_BG   = "1F4E79"   # dark blue
HEADER_FG   = "FFFFFF"
ALT_ROW_BG  = "EBF3FB"   # light blue tint for alternate rows
WHITE       = "FFFFFF"
BORDER_CLR  = "BDD7EE"

# result-status colours (matches the app)
STATUS_COLORS = {
    "Red":        "FFCCCC",
    "Yellow":     "FFFACD",
    "Purple":     "E6CCFF",
    "Light Blue": "CCE5FF",
    "Brown":      "F2DCDB",
    "Green":      "CCFFCC",
    "Orange":     "FFE0CC",
}

def make_border():
    thin = Side(style="thin", color=BORDER_CLR)
    return Border(left=thin, right=thin, top=thin, bottom=thin)

def header_font():
    return Font(name="Calibri", bold=True, color=HEADER_FG, size=11)

def cell_font(bold=False):
    return Font(name="Calibri", bold=bold, size=10)

def wrap_align():
    return Alignment(wrap_text=True, vertical="top")

# ── rule data ─────────────────────────────────────────────────────────────────
RULES = [
    {
        "Rule Name":        "Claimed After Closure",
        "How It Is Validated": (
            "For every weekly date column that has hours > 0, the system computes "
            "the week-start date (column date − 6 days). If the ticket's Closed Date "
            "(from the ticket data file) is earlier than that week-start date, the row "
            "fails this rule.\n\n"
            "Code location: validation_engine.py → _apply_validation_rules() → "
            "\"# Rule: Claimed after closure\""
        ),
        "Applies To":       "INC, RITM, CHG, PRB (any ticket with a Closed Date)",
        "Condition / Trigger": (
            "closed_date < week_start_date  AND  hours > 0  AND  rule is enabled"
        ),
        "Output Message":   "Claimed after ticket closed",
        "Severity":         "Error",
        "Colour in Report": "Red",
    },
    {
        "Rule Name":        "No Hours Claimed",
        "How It Is Validated": (
            "All weekly date columns are iterated. If every column contains 0 (or blank), "
            "the all_zero flag stays True and this rule fires.\n\n"
            "Code location: validation_engine.py → _apply_validation_rules() → "
            "\"# Rule: No hours claimed\""
        ),
        "Applies To":       "All rows",
        "Condition / Trigger": (
            "sum of all weekly hour columns == 0  AND  rule is enabled"
        ),
        "Output Message":   "No hours claimed",
        "Severity":         "Info",
        "Colour in Report": "Yellow",
    },
    {
        "Rule Name":        "P1/P2 Activity Code — Error",
        "How It Is Validated": (
            "Checked only when: ticket starts with 'INC', priority is P1 or P2, and "
            "the rule is enabled. The Activity Code on the row is compared against the "
            "required code (100C01). If it does NOT match, the error message is returned.\n\n"
            "Code location: validation_engine.py → _apply_validation_rules() → "
            "\"# Rule: P1/P2 Activity Code\""
        ),
        "Applies To":       "INC tickets with Priority P1 or P2",
        "Condition / Trigger": (
            "ticket starts with 'INC'  AND  priority IN [P1, P2]  AND  "
            "activity_code ≠ '100C01'  AND  rule is enabled"
        ),
        "Output Message":   "P1/P2 Ticket must use Activity Code 100C01",
        "Severity":         "Error",
        "Colour in Report": "Purple",
    },
    {
        "Rule Name":        "P1/P2 Activity Code — Valid",
        "How It Is Validated": (
            "Same check as above; if the Activity Code DOES match 100C01 the row "
            "is flagged as valid (not a violation).\n\n"
            "Code location: validation_engine.py → _apply_validation_rules() → "
            "rule.get('valid_message', ...)"
        ),
        "Applies To":       "INC tickets with Priority P1 or P2",
        "Condition / Trigger": (
            "ticket starts with 'INC'  AND  priority IN [P1, P2]  AND  "
            "activity_code == '100C01'  AND  rule is enabled"
        ),
        "Output Message":   "P1/P2 Ticket Activity Code 100C01 - Valid",
        "Severity":         "Valid (not a violation)",
        "Colour in Report": "Light Blue",
    },
    {
        "Rule Name":        "Project Activity Code",
        "How It Is Validated": (
            "A ticket is classified as a project ticket if its INC_KEY appears in the "
            "team's project_tickets list (loaded from the JSON rules file). When IS_PROJECT "
            "is True:\n"
            "  • If the activity code starts with '10000' → alternate error\n"
            "  • If the activity code does NOT start with '100E' → main error\n"
            "  • Otherwise → Allowed\n\n"
            "Code location: validation_engine.py → _apply_validation_rules() → "
            "\"# Rule: Project tickets\""
        ),
        "Applies To":       "Rows whose ticket key is in the team's project_tickets list",
        "Condition / Trigger": (
            "IS_PROJECT == True  AND  activity_code does not start with '100E'  "
            "AND  rule is enabled"
        ),
        "Output Message":   (
            "Sub-project; But the claim is not on 100E*\n"
            "(alternate: Sub-project; But the claim is on 100E*)"
        ),
        "Severity":         "Warning",
        "Colour in Report": "Brown",
    },
    {
        "Rule Name":        "Governance Activity Code",
        "How It Is Validated": (
            "A row is flagged as governance when the Activity Description column contains "
            "the word 'governance' (case-insensitive). When IS_GOV is True, the activity "
            "code must start with '100G'. If it does not, the rule fires.\n\n"
            "Code location: validation_engine.py → _process_timesheet() sets IS_GOV; "
            "_apply_validation_rules() → \"# Rule: Governance\""
        ),
        "Applies To":       "Rows where Activity Description contains 'governance'",
        "Condition / Trigger": (
            "IS_GOV == True  AND  activity_code does not start with '100G'  "
            "AND  rule is enabled"
        ),
        "Output Message":   "Governance rule violated",
        "Severity":         "Warning",
        "Colour in Report": "Brown",
    },
    {
        "Rule Name":        "Incident Hour Threshold",
        "How It Is Validated": (
            "After summing all weekly hour columns into TOTAL_HOURS, if the ticket is "
            "an INC and total hours exceed 9 (max_hours from rules JSON), this rule fires.\n\n"
            "Code location: validation_engine.py → _apply_validation_rules() → "
            "\"# Rule: Incident hour threshold\""
        ),
        "Applies To":       "INC tickets only",
        "Condition / Trigger": (
            "ticket starts with 'INC'  AND  TOTAL_HOURS > 9  AND  rule is enabled"
        ),
        "Output Message":   "More hours claimed",
        "Severity":         "Warning",
        "Colour in Report": "Red",
    },
    {
        "Rule Name":        "Allowed (Pass)",
        "How It Is Validated": (
            "If a row passes all the above checks without triggering any rule, "
            "it is marked as Allowed. This is the default return value at the end "
            "of the validate_row() function.\n\n"
            "Code location: validation_engine.py → _apply_validation_rules() → "
            "\"return 'Allowed'\""
        ),
        "Applies To":       "All rows that do not match any violation condition",
        "Condition / Trigger": "No rule condition matched",
        "Output Message":   "Allowed",
        "Severity":         "Pass",
        "Colour in Report": "Green",
    },
]

HEADERS = [
    "Rule Name",
    "How It Is Validated",
    "Applies To",
    "Condition / Trigger",
    "Output Message (Final_Status)",
    "Severity",
    "Colour in Report",
]

COL_WIDTHS = [28, 72, 40, 55, 42, 18, 18]

# ── build workbook ────────────────────────────────────────────────────────────
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Validation Rules"

# Title row
ws.merge_cells("A1:G1")
title_cell = ws["A1"]
title_cell.value = "Timesheet Validator — Validation Rules Documentation"
title_cell.font = Font(name="Calibri", bold=True, size=14, color=HEADER_FG)
title_cell.fill = PatternFill("solid", fgColor=HEADER_BG)
title_cell.alignment = Alignment(horizontal="center", vertical="center")
ws.row_dimensions[1].height = 30

# Header row
for col_idx, header in enumerate(HEADERS, start=1):
    cell = ws.cell(row=2, column=col_idx, value=header)
    cell.font = header_font()
    cell.fill = PatternFill("solid", fgColor=HEADER_BG)
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    cell.border = make_border()
ws.row_dimensions[2].height = 22

# Data rows
for row_idx, rule in enumerate(RULES, start=3):
    bg = ALT_ROW_BG if row_idx % 2 == 0 else WHITE
    colour_key = rule["Colour in Report"]
    status_bg  = STATUS_COLORS.get(colour_key, WHITE)

    values = [
        rule["Rule Name"],
        rule["How It Is Validated"],
        rule["Applies To"],
        rule["Condition / Trigger"],
        rule["Output Message"],
        rule["Severity"],
        rule["Colour in Report"],
    ]

    for col_idx, value in enumerate(values, start=1):
        cell = ws.cell(row=row_idx, column=col_idx, value=value)
        cell.alignment = wrap_align()
        cell.border = make_border()

        if col_idx == 1:  # Rule Name — bold
            cell.font = cell_font(bold=True)
            cell.fill = PatternFill("solid", fgColor=bg)
        elif col_idx == 7:  # Colour column — use actual status colour
            cell.font = cell_font(bold=True)
            cell.fill = PatternFill("solid", fgColor=status_bg)
        else:
            cell.font = cell_font()
            cell.fill = PatternFill("solid", fgColor=bg)

    ws.row_dimensions[row_idx].height = 90

# Column widths
for col_idx, width in enumerate(COL_WIDTHS, start=1):
    ws.column_dimensions[get_column_letter(col_idx)].width = width

# Freeze panes below header
ws.freeze_panes = "A3"

# Auto-filter
ws.auto_filter.ref = f"A2:G{len(RULES) + 2}"

# Save
output_path = "Validation_Rules_Documentation.xlsx"
wb.save(output_path)
print(f"Saved: {output_path}")
