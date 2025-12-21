# Font Standardization Plan

## Current Issues
- Many UI elements use small fonts (8, 9, 10, 11 pt)
- Buttons and links in period details hard to see
- Weight logs display font too small
- Inconsistent across different views

## Standard Font Sizes

### Primary Standard: **Arial 12**
- All user-facing text
- Form labels
- Input fields  
- Buttons
- Log displays
- Tree views
- List boxes

### Headers: **Arial 14 bold**
- Window titles
- Section headers
- Panel titles

### Large Headers: **Arial 16 bold**  
- Main dashboard titles
- Top-level navigation

### Small Text: **Arial 10 italic**
- Help text
- Info messages
- Legends

## Files to Update

### Priority 1: Period Management
- `period_view.py` - Many 8-10pt fonts
- Protocol suggestions: 8-9pt → 12pt
- Buttons: 10pt → 12pt
- Details window: 10pt → 12pt

### Priority 2: Weight Logging  
- `weight_view.py` - Check all fonts
- Log form: ensure 12pt
- History tree: ensure 12pt

### Priority 3: Other Views
- `food_view.py`
- `activity_view.py`  
- `logs_view.py`

## Implementation
Run global search/replace for each font size:
- `font=("Arial", 8` → `font=("Arial", 12`
- `font=("Arial", 9` → `font=("Arial", 12`  
- `font=("Arial", 10` → `font=("Arial", 12`
- `font=("Arial", 11` → `font=("Arial", 12`

Exceptions (keep as is):
- Headers already 14-16pt
- Very specific UI elements
