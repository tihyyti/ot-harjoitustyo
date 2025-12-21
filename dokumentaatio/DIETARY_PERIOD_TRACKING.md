# Dietary Period Tracking & Enhanced Weight Logging

**Created:** 2025-12-20  
**Version:** v2.1.1  
**Status:** Complete ✅

---

## Overview

This enhancement adds experimental period tracking to the weight management system. Users can now annotate time periods with dietary experiments/protocols and see which approaches work best for their weight loss goals.

### New Features

1. **Dietary Period Annotations** - Mark experimental periods with start/end dates
2. **Week Numbering** - Display week numbers with week start dates  
3. **Period Markers** - Show when periods start/end in weight logs
4. **Descending Order** - All lists show most recent entries first (already implemented)
5. **Period Effectiveness** - Track weight loss during specific dietary protocols

---

## Use Cases

### Example Scenarios

**Scenario 1: No Evening Eating**
- User creates period: "No Evening Eating After 7pm" (Start: 2025-12-01, Duration: 3 weeks)
- Weight logs during this period show annotation: "📍 No Evening Eating After 7pm"
- Start marker on Dec 1st: "▶ START: No Evening Eating After 7pm"
- End marker on Dec 21st: "⏹ END: No Evening Eating After 7pm"
- Summary shows: Lost 2.1 kg during this period (-0.7 kg/week)

**Scenario 2: Morning Emphasis**
- Period: "Morning Emphasis - 40% Breakfast" (Start: 2025-11-15, Ongoing)
- All weight logs since Nov 15th show: "📍 Morning Emphasis - 40% Breakfast"
- User can compare effectiveness vs previous approaches

**Scenario 3: Weekend-Only Evening Meals**
- Period: "Weekend-Only Evening Meals" (Start: 2025-12-01, End: 2025-12-31)
- Month-long experiment to see if this restriction helps
- Can analyze weight trend specific to this month

---

## Components Created

### 1. Database Table: `dietary_period`

```sql
CREATE TABLE IF NOT EXISTS dietary_period (
    period_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT,                  -- NULL = ongoing
    period_name TEXT NOT NULL,      -- e.g., "No Evening Eating"
    description TEXT,               -- Detailed description
    protocol_type TEXT,             -- Category: time_restricted, etc.
    notes TEXT,                     -- Additional notes
    is_active INTEGER DEFAULT 1,    -- Can deactivate without deleting
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES "user"(user_id) ON DELETE CASCADE
);

CREATE INDEX idx_dietary_period_user_dates 
ON dietary_period(user_id, start_date, end_date);
```

**Migration Script:** `src/migrations/add_dietary_periods.py`

---

### 2. DietaryPeriod Data Model

**File:** `src/repositories/models.py`

```python
@dataclass
class DietaryPeriod:
    period_id: str
    user_id: str
    start_date: str
    period_name: str
    end_date: Optional[str] = None
    description: Optional[str] = None
    protocol_type: Optional[str] = None
    notes: Optional[str] = None
    is_active: int = 1
    created_at: Optional[str] = None
```

---

### 3. DietaryPeriodRepository

**File:** `src/repositories/dietary_period_repository.py` (250 lines)

**Methods:**
- ✅ `find_all(user_id)` - All periods, descending order
- ✅ `find_active(user_id)` - Currently active/ongoing periods
- ✅ `find_by_date(user_id, date)` - Periods containing specific date
- ✅ `find_by_id(period_id)` - Get specific period
- ✅ `create(...)` - Create new period
- ✅ `end_period(period_id, end_date)` - Mark period as ended
- ✅ `update(period_id, **kwargs)` - Update period details
- ✅ `delete(period_id)` - Delete period
- ✅ `deactivate(period_id)` - Deactivate without deleting

---

### 4. DietaryPeriodService

**File:** `src/services/dietary_period_service.py` (264 lines)

**Protocol Types:**
- `time_restricted` - e.g., no eating after 7pm
- `meal_timing` - e.g., morning emphasis
- `food_restricted` - e.g., low-carb, no sugar
- `intermittent_fasting` - e.g., 16:8, 5:2
- `portion_control` - e.g., smaller portions
- `food_combination` - e.g., protein with every meal
- `custom` - user-defined

**Key Methods:**

#### create_period(user_id, start_date, period_name, ...)
Create new dietary experiment period with validation.

#### get_period_summary(period_id)
Get comprehensive summary including:
- Period duration (days)
- Is ongoing or completed
- Weight change during period
- Weight loss per week during period

#### get_suggested_protocols()
Returns 7 pre-defined protocol suggestions:
1. No Evening Eating After 7pm
2. Morning Emphasis (40/40/20 split)
3. Weekend-Only Evening Meals
4. Intermittent Fasting 16:8
5. Low-Carb Experiment
6. Smaller Portions (20-30% reduction)
7. Protein With Every Meal

---

### 5. Enhanced WeightLogService

**File:** `src/services/weightlog_service.py` (Updated)

#### New Helper Function: `get_week_info(date_str)`
Returns week number, week start date (Monday), year, and formatted label.

```python
week_info = get_week_info('2025-12-20')
# Returns:
# {
#     'week_number': 51,
#     'week_start_date': '2025-12-15',
#     'year': 2025,
#     'week_label': 'Week 51, 2025'
# }
```

#### New Method: `get_weight_history_with_weeks(user_id, days=30, include_periods=True)`

Returns enriched weight logs with:
- Week numbering
- Week start date
- `is_week_start` flag (for bold formatting)
- Active dietary periods
- Period start/end markers
- All in **descending order** (most recent first)

**Example Output:**
```python
[
    {
        'log_id': '...',
        'date': '2025-12-20',
        'weight': 74.5,
        'notes': 'Morning weight',
        'week_number': 51,
        'week_start_date': '2025-12-15',
        'week_label': 'Week 51, 2025',
        'year': 2025,
        'is_week_start': False,
        'active_periods': ['No Evening Eating After 7pm'],
        'period_markers': [],
        'has_periods': True
    },
    {
        'log_id': '...',
        'date': '2025-12-15',
        'weight': 74.8,
        'notes': '',
        'week_number': 51,
        'week_start_date': '2025-12-15',
        'week_label': 'Week 51, 2025',
        'year': 2025,
        'is_week_start': True,  # ← Bold this row
        'active_periods': ['No Evening Eating After 7pm'],
        'period_markers': [],
        'has_periods': True
    },
    {
        'log_id': '...',
        'date': '2025-12-01',
        'weight': 76.2,
        'notes': 'Starting new protocol',
        'week_number': 48,
        'week_start_date': '2025-11-25',
        'week_label': 'Week 48, 2025',
        'year': 2025,
        'is_week_start': False,
        'active_periods': ['No Evening Eating After 7pm'],
        'period_markers': ['▶ START: No Evening Eating After 7pm'],
        'has_periods': True
    }
]
```

---

## Usage Examples

### 1. Create Dietary Period

```python
from services.dietary_period_service import DietaryPeriodService

service = DietaryPeriodService('src/data/laihdutanyt.db')

result = service.create_period(
    user_id="user-123",
    start_date="2025-12-01",
    period_name="No Evening Eating After 7pm",
    description="Stop eating after 7pm to allow 12+ hour overnight fasting",
    protocol_type="time_restricted",
    notes="Aiming for 3 weeks trial",
    end_date=None  # Ongoing
)

if result['success']:
    print(f"Period created! ID: {result['period']['period_id']}")
```

### 2. Get Weight History with Week Numbers and Period Annotations

```python
from services.weightlog_service import WeightLogService

service = WeightLogService('src/data/laihdutanyt.db')

history = service.get_weight_history_with_weeks(
    user_id="user-123",
    days=30,
    include_periods=True
)

for log in history:
    # Show week start in bold
    bold = "**" if log['is_week_start'] else ""
    
    # Display
    print(f"{bold}{log['week_label']}{bold}")
    print(f"  {log['date']}: {log['weight']} kg")
    
    # Show period markers
    for marker in log['period_markers']:
        print(f"    {marker}")
    
    # Show active periods
    if log['has_periods']:
        print(f"    📍 {', '.join(log['active_periods'])}")
```

### 3. End a Period and View Summary

```python
# End the period
result = service.end_period(period_id="abc-123", end_date="2025-12-21")

# Get effectiveness summary
summary = service.get_period_summary("abc-123")

print(f"Period: {summary['period_name']}")
print(f"Duration: {summary['duration_days']} days")

if summary['weight_change']:
    wc = summary['weight_change']
    print(f"Weight change: {wc['change']:.1f} kg")
    print(f"Per week: {wc['change_per_week']:.2f} kg/week")
```

### 4. Get Suggested Protocols

```python
suggestions = service.get_suggested_protocols()

for protocol in suggestions:
    print(f"{protocol['name']}")
    print(f"  Type: {protocol['type']}")
    print(f"  Description: {protocol['description']}")
    print(f"  Suggested duration: {protocol['example_duration']}")
```

---

## UI Integration Guidelines

### Weight Log List Display

```
Week 51, 2025 (Dec 15 - Dec 21)
----------------------------------------
**📅 2025-12-20**  74.5 kg  (Morning weight)
  📍 No Evening Eating After 7pm

2025-12-19  74.7 kg
  📍 No Evening Eating After 7pm

**📅 2025-12-15**  74.8 kg
  📍 No Evening Eating After 7pm

Week 50, 2025 (Dec 8 - Dec 14)
----------------------------------------
2025-12-14  75.0 kg
  📍 No Evening Eating After 7pm

**📅 2025-12-08**  75.3 kg
  📍 No Evening Eating After 7pm

Week 48, 2025 (Nov 25 - Dec 1)
----------------------------------------
**📅 2025-12-01**  76.2 kg  (Starting new protocol)
  ▶ START: No Evening Eating After 7pm

2025-11-28  76.5 kg
```

### Period Management UI

**Create Period Form:**
- Period Name* (text input)
- Start Date* (date picker, default: today)
- End Date (date picker, optional - leave blank for ongoing)
- Protocol Type (dropdown: time_restricted, meal_timing, etc.)
- Description (textarea)
- Notes (textarea)

**Active Periods List:**
```
🟢 No Evening Eating After 7pm
   Started: 2025-12-01 (20 days ago)
   Weight change: -1.7 kg (-0.6 kg/week)
   [End Period] [Edit] [View Details]

🟢 Morning Emphasis - 40/40/20
   Started: 2025-11-15 (36 days ago)
   Weight change: -2.3 kg (-0.45 kg/week)
   [End Period] [Edit] [View Details]
```

**Completed Periods List:**
```
⚫ Low-Carb Experiment
   Nov 1 - Nov 21 (21 days)
   Weight change: -1.5 kg (-0.5 kg/week)
   [View Details] [Start Again] [Delete]
```

---

## Migration Steps

### 1. Run Migration Script

```bash
poetry run python src/migrations/add_dietary_periods.py
```

**Output:**
```
============================================================
Adding Dietary Period Tracking
============================================================
Adding dietary_period table...
✓ dietary_period table created successfully!
✓ Index created for efficient date range queries

Verifying table structure...
  ✓ dietary_period table exists
  ✓ Column 'period_id' exists
  ✓ Column 'user_id' exists
  ...

✓ Verification complete!

============================================================
✓ Migration complete!
============================================================

Examples of period_name:
  - 'No Evening Eating After 7pm'
  - 'Weekend-Only Evening Meals'
  - 'Morning Emphasis Protocol'
  - 'Low-Carb Experiment'
  - 'Intermittent Fasting 16:8'
```

---

## Testing

### Test Dietary Periods

```python
# Test script: src/scripts/test_dietary_periods.py
from services.dietary_period_service import DietaryPeriodService
from services.weightlog_service import WeightLogService

db_path = 'src/data/laihdutanyt.db'
period_service = DietaryPeriodService(db_path)
weight_service = WeightLogService(db_path)

# 1. Create a test period
result = period_service.create_period(
    user_id="test-user",
    start_date="2025-12-01",
    period_name="No Evening Eating After 7pm",
    protocol_type="time_restricted",
    description="Testing period annotation"
)

# 2. Get weight history with annotations
history = weight_service.get_weight_history_with_weeks(
    user_id="test-user",
    days=30,
    include_periods=True
)

# 3. Print results
for log in history[:5]:
    print(f"\n{log['date']} - {log['weight']} kg")
    if log['is_week_start']:
        print(f"  ** {log['week_label']} **")
    if log['period_markers']:
        for marker in log['period_markers']:
            print(f"  {marker}")
    if log['active_periods']:
        print(f"  Active: {', '.join(log['active_periods'])}")
```

---

## Database Schema Updates

### Before
- `weightlog` table (basic)

### After
- `weightlog` table (unchanged)
- `dietary_period` table (NEW)
  - Tracks experimental periods
  - Links to user
  - Supports start/end dates
  - Categorized by protocol type
  - Can be marked inactive

---

## Benefits for Users

### 1. Experimentation Tracking
- Try different dietary approaches
- See what works best personally
- Data-driven decision making

### 2. Period Comparison
- Compare weight loss rates between approaches
- "During No Evening Eating: -0.6 kg/week"
- "During Low-Carb: -0.4 kg/week"
- Choose most effective method

### 3. Accountability
- Marking a period creates commitment
- Visible reminders in weight logs
- Easy to see if following protocol

### 4. Pattern Recognition
- Weekly view helps spot patterns
- Period annotations show context
- Weight logs make sense with context

---

## Future Enhancements

### Phase 2+ (Not Yet Implemented)
- 📊 Visual charts comparing periods
- 📈 Statistical analysis of period effectiveness
- 🔔 Reminders for period start/end
- 📝 Journal entries linked to periods
- 🎯 Period goals and success criteria
- 🏆 Achievements for completing periods
- 📤 Export period effectiveness reports

---

## Files Created/Modified

### Created (6 files)
1. `src/migrations/add_dietary_periods.py` (94 lines)
2. `src/repositories/dietary_period_repository.py` (250 lines)
3. `src/services/dietary_period_service.py` (264 lines)

### Modified (2 files)
1. `src/repositories/models.py` - Added `DietaryPeriod` dataclass
2. `src/services/weightlog_service.py` - Added week numbering + period annotations

**Total New Code:** ~608 lines

---

## Status: ✅ COMPLETE

All features requested have been implemented:

1. ✅ **Log annotation with periods** - Dietary periods can mark time ranges
2. ✅ **Period start/end markers** - Special markers show ▶ START and ⏹ END
3. ✅ **Notification on log entries** - Active periods shown on each log
4. ✅ **Descending order** - All lists show most recent first (already was implemented)
5. ✅ **Week numbering** - ISO week numbers with week start dates
6. ✅ **Week start indication** - `is_week_start` flag for bold formatting
7. ✅ **Suggested protocols** - 7 common dietary approaches pre-defined
8. ✅ **Period effectiveness** - Weight loss tracking during periods

**Ready for:** UI implementation and user testing

---

**Document Version:** 1.0  
**Last Updated:** 2025-12-20  
**Author:** AI Assistant + Development Team
