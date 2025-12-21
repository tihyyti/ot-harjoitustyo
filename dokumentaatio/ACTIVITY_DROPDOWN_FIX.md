# Activity Dropdown Fix - December 21, 2025

## Issue
Activity dropdown only showed one item: "walking"

## Root Causes Found

### 1. CSV File Format Error ❌
**Problem:** `sample_activities.csv` had a comment line on first row:
```csv
# week4: 
name,calories_per_activity
Running,300
...
```

**Impact:** CSV reader treated `# week4:` as the header, causing all activities to be imported with `NULL` names.

**Fix:** ✅ Removed comment line from CSV:
```csv
name,calories_per_activity
Running,300
Cycling,250
Swimming,400
Walking,150
Yoga,100
```

---

### 2. Import Script Column Mismatch ❌
**Problem:** Import script used wrong column name:
```python
cur.execute("""
    INSERT INTO activity (activity_id, name, calories_per_activity)
    VALUES (?, ?, ?)
""", (activity_id, name, calories))
```

**Actual Schema:**
```
activity_id TEXT
name TEXT
unit TEXT
kcal_per_unit REAL  ← Correct column name
```

**Fix:** ✅ Updated import script to use correct column:
```python
# Support both old and new CSV formats
calories = float(row.get("calories_per_activity") or row.get("kcal_per_unit") or 0.0)

# Use correct column name
cur.execute("""
    INSERT INTO activity (activity_id, name, kcal_per_unit)
    VALUES (?, ?, ?)
""", (activity_id, name, calories))
```

---

## Solution Applied

### Files Fixed:
1. **src/data/sample_activities.csv** - Removed comment line
2. **src/scripts/import_activities.py** - Fixed column name and added backward compatibility

### Database Actions:
1. Deleted all activities with NULL names
2. Re-imported from fixed CSV file
3. Verified all 5 activities loaded correctly

---

## Verification

### Before Fix:
```
Activity dropdown:
  - walking (only 1 item)
```

### After Fix:
```
Activity dropdown:
  - Cycling
  - Running
  - Swimming
  - Walking
  - Yoga
(5 items total)
```

---

## Technical Details

### Import Script Improvements:
```python
# Now supports both CSV formats
calories = float(row.get("calories_per_activity") or row.get("kcal_per_unit") or 0.0)

# Uses correct column name matching schema
cur.execute("""
    INSERT INTO activity (activity_id, name, kcal_per_unit)
    VALUES (?, ?, ?)
""", (activity_id, name, calories))
```

**Benefits:**
- Backward compatible with old CSV format
- Matches actual database schema
- Prevents future import failures

---

## Testing

```powershell
# Re-import activities
poetry run python src/scripts/import_activities.py src/data/sample_activities.csv

# Test activity loading
poetry run python test_activities.py
```

**Expected Output:**
```
Testing get_activity_name_only_list() (new format):
  Count: 5
    - Cycling
    - Running
    - Swimming
    - Walking
    - Yoga
```

---

## Files Modified
1. `src/data/sample_activities.csv` - Removed `# week4:` comment line
2. `src/scripts/import_activities.py` - Fixed column name from `calories_per_activity` to `kcal_per_unit`

---

**Status:** ✅ Fixed - All 5 activities now appear in dropdown
**Verified:** Activity logging works correctly with all options
**Version:** 2.3.1 (Bug fix)
**Date:** December 21, 2025
