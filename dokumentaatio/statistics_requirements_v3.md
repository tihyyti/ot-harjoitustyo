# Laihdutanyt - Statistics & Reporting Requirements v2.1

**Technical Name:** `laihdutanyt_statistics_requirements_v2_1.md`  
**Version:** v2.1.0  
**Date:** 2025-12-20  
**Status:** Release Candidate  
**Target Release:** v2.1.0 "Statistics Core"

---

## Document Information

| Field | Value |
|-------|-------|
| **Document Type** | Requirements Specification |
| **Target Audience** | Developers, Architects |
| **Related Artifacts** | `laihdutanyt_erd_v2_1.mmd`, `MVP_RELEASE_PLAN_v2.1.md` |
| **Supersedes** | `laihdutanyt_requirements_specification_v2.md` (core features) |

---

## 1. Executive Summary

This document extends the Laihdutanyt application requirements to include comprehensive statistics, reporting, and progress tracking features. The focus is on:
- Weekly and monthly progress tracking
- Nutrient breakdown analysis
- Weight loss goal monitoring
- Coach/admin reporting capabilities

---

## 2. Enhanced Data Model Requirements

### 2.1 Food Entity (Enhanced)
Current implementation is **COMPLETE** ✅
- `food_id` (PRIMARY KEY)
- `name` (TEXT)
- `kcal_per_portion` (REAL) - per 100g
- `carbs_per_portion` (REAL) - grams per 100g
- `protein_per_portion` (REAL) - grams per 100g
- `fat_per_portion` (REAL) - grams per 100g

**Status:** Already implemented in database schema

### 2.2 Activity Entity (Enhanced)
Current implementation is **COMPLETE** ✅
- `activity_id` (PRIMARY KEY)
- `name` (TEXT)
- `unit` (TEXT) - e.g., "steps", "minutes"
- `kcal_per_unit` (REAL) - per 1000 units

**Status:** Already implemented in database schema

### 2.3 User Entity (Enhanced)
Current implementation includes:
- Basic profile: weight, height, age, activity_level
- Goals: kcal_min, kcal_max, weight_loss_target
- Restrictions: allergies (TEXT field)

**Missing for Statistics:**
- `current_weight` tracking over time (use Statistics table)
- `weight_history` (implement via Statistics table)

### 2.4 NEW: WeightLog Entity
**Purpose:** Track weight measurements over time for progress monitoring

```sql
CREATE TABLE IF NOT EXISTS weightlog (
    log_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    date TEXT NOT NULL,
    weight REAL NOT NULL,
    notes TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES "user"(user_id) ON DELETE CASCADE
);
```

**Rationale:** 
- Current `statistics` table has `total_weight` but no clear weight tracking mechanism
- Users need to log weight measurements to track progress
- Separate table allows multiple measurements per day if needed

### 2.5 Enhanced Statistics Entity
Current implementation has basic structure. Needs enhancement:

```sql
CREATE TABLE IF NOT EXISTS statistics (
    stats_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    date TEXT NOT NULL,
    
    -- Calorie tracking (existing)
    total_kcal_consumed REAL,
    total_kcal_burned REAL,  -- NEW
    net_kcal REAL,            -- NEW: consumed - burned
    
    -- Nutrient breakdown (NEW)
    total_carbs_g REAL,
    total_protein_g REAL,
    total_fat_g REAL,
    
    -- Weight tracking (existing, clarified)
    current_weight REAL,      -- Weight at this date
    weight_change REAL,       -- Change from previous day
    
    -- Meal breakdown (NEW - optional)
    breakfast_kcal REAL,
    lunch_kcal REAL,
    dinner_kcal REAL,
    snacks_kcal REAL,
    
    -- Aggregation metadata
    food_entries_count INTEGER,
    activity_entries_count INTEGER,
    
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES "user"(user_id) ON DELETE CASCADE,
    UNIQUE(user_id, date)  -- One stats record per user per day
);
```

### 2.6 NEW: DietaryPlan Entity (Coach Feature)
**Purpose:** Coaches can create recommended dietary plans for users

```sql
CREATE TABLE IF NOT EXISTS dietary_plan (
    plan_id TEXT PRIMARY KEY,
    coach_id TEXT NOT NULL,  -- admin_id
    user_id TEXT,            -- NULL for template plans
    plan_name TEXT NOT NULL,
    description TEXT,
    
    -- Daily targets
    target_kcal_min REAL,
    target_kcal_max REAL,
    target_protein_g REAL,
    target_carbs_g REAL,
    target_fat_g REAL,
    
    -- Weekly targets
    weekly_weight_loss_kg REAL,
    weekly_exercise_minutes INTEGER,
    
    -- Plan duration
    start_date TEXT,
    end_date TEXT,
    
    -- Status
    status TEXT DEFAULT 'active',  -- active, completed, cancelled
    
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(coach_id) REFERENCES admin(admin_id) ON DELETE CASCADE,
    FOREIGN KEY(user_id) REFERENCES "user"(user_id) ON DELETE CASCADE
);
```

### 2.7 NEW: UserRestrictions Entity (Enhanced Allergy Management)
**Purpose:** Replace simple TEXT allergies field with structured data

```sql
CREATE TABLE IF NOT EXISTS user_restriction (
    restriction_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    restriction_type TEXT NOT NULL,  -- 'allergy', 'intolerance', 'preference', 'medical'
    food_ingredient TEXT,            -- e.g., 'lactose', 'gluten', 'nuts'
    severity TEXT,                   -- 'mild', 'moderate', 'severe', 'life-threatening'
    notes TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES "user"(user_id) ON DELETE CASCADE
);
```

---

## 3. Statistics & Reporting Use Cases

### 3.1 User Progress Tracking

#### UC-1: View Daily Nutrient Breakdown
**Actor:** User  
**Precondition:** User has logged food entries for the day  
**Main Flow:**
1. User navigates to Statistics Dashboard
2. System displays today's date by default
3. System shows:
   - Total calories consumed (from food logs)
   - Total calories burned (from activity logs)
   - Net calorie balance (consumed - burned)
   - Nutrient breakdown: Carbs, Protein, Fat (grams and kcal)
   - Visual progress bars showing % of daily goals
4. User can select different dates to view historical data

**Postcondition:** User understands their daily nutrient intake

**Implementation Notes:**
- Calculate from FoodLog entries: `SUM((portion_size_g / 100) * nutrient_per_portion)`
- Display as pie chart (carbs/protein/fat) and bar charts (vs goals)

---

#### UC-2: View Weekly Progress Report
**Actor:** User  
**Precondition:** User has at least 1 week of logged data  
**Main Flow:**
1. User clicks "Weekly Report" button
2. System calculates for last 7 days:
   - Average daily calories consumed
   - Average daily calories burned
   - Total net calorie deficit/surplus
   - Average nutrient breakdown (g/day)
   - Weight change (if weight logs exist)
   - Days within calorie goal range
3. System displays:
   - Line chart: Daily calories over 7 days
   - Bar chart: Nutrient trends
   - Weight trend line
   - Summary statistics with color coding (green=on track, yellow=warning, red=off track)

**Success Metrics:**
- Weight loss progress toward weekly target
- Adherence to calorie goals (% of days in range)

---

#### UC-3: View Monthly Progress Report
**Actor:** User  
**Precondition:** User has at least 1 month of logged data  
**Main Flow:**
1. User clicks "Monthly Report" button
2. System calculates for last 30 days:
   - Weekly averages (4 weeks)
   - Total weight change
   - Total exercise minutes/activities
   - Most/least consumed foods
   - Most/least performed activities
   - Goal adherence percentage
3. System displays:
   - Multi-line chart: Calories, Weight over 30 days
   - Heatmap: Daily adherence calendar
   - Top 10 foods consumed (by frequency and calories)
   - Achievement badges (if goals met)

**Success Metrics:**
- Monthly weight loss vs target
- Consistency (days logged / total days)

---

### 3.2 Coach/Admin Reporting

#### UC-4: Generate User Progress Report
**Actor:** Coach/Admin  
**Precondition:** Coach has access to user's data  
**Main Flow:**
1. Coach logs into admin dashboard
2. Coach selects user from list
3. Coach clicks "Generate Progress Report"
4. System prompts for date range (default: last 30 days)
5. System generates comprehensive report:
   - User profile summary (age, weight, goals)
   - Calorie trends (line chart)
   - Weight progress (line chart with target line)
   - Nutrient balance analysis
   - Goal adherence metrics
   - Recommendations section (system-generated)
6. Coach can:
   - View report on screen
   - Export as PDF
   - Add personal notes
   - Create dietary plan recommendation

**Postcondition:** Coach has actionable insights to advise user

---

#### UC-5: Create Dietary Plan Recommendation
**Actor:** Coach/Admin  
**Precondition:** Coach has reviewed user's progress report  
**Main Flow:**
1. Coach clicks "Create Dietary Plan" from user's profile
2. System displays form:
   - Plan name (e.g., "2-Month Weight Loss Plan")
   - Description
   - Daily targets: kcal min/max, protein, carbs, fat
   - Weekly targets: weight loss (kg), exercise minutes
   - Start/End dates
3. Coach fills form based on:
   - User's current stats
   - Weight loss goals
   - Dietary restrictions
   - Progress to date
4. System validates inputs (realistic targets)
5. Coach saves plan
6. System:
   - Links plan to user
   - Sends notification to user
   - Updates user's dashboard to show new plan

**Postcondition:** User has personalized dietary plan

---

### 3.3 Goal Tracking & Constraints

#### UC-6: Monitor Daily Calorie Constraints
**Actor:** System (automated)  
**Trigger:** User logs food or activity  
**Main Flow:**
1. After food/activity log entry, system calculates:
   - Current day's total consumed calories
   - Current day's total burned calories
   - Net calories
2. System checks against user's constraints:
   - Is net calories < kcal_min? → Warning: "Under minimum"
   - Is net calories > kcal_max? → Warning: "Over maximum"
3. System displays visual indicator:
   - Green: Within range
   - Yellow: Approaching limit (±10%)
   - Red: Out of range
4. System can show:
   - "You have 500 kcal remaining today"
   - "You've exceeded your daily max by 200 kcal"

---

#### UC-7: Track Weekly Weight Loss Goal
**Actor:** System (automated)  
**Trigger:** User logs weight measurement  
**Main Flow:**
1. User enters new weight in WeightLog
2. System calculates:
   - Weight change from 7 days ago
   - Weight change from 30 days ago
   - Weight change from plan start date
3. System compares to targets:
   - Weekly target (from user profile or dietary plan)
   - Monthly target
4. System displays progress:
   - "You've lost 0.8 kg this week (target: 0.5 kg) 🎉"
   - "Monthly progress: -2.1 kg of -2.0 kg goal 🎯"
5. System stores progress metrics in Statistics table

---

## 4. UI Requirements

### 4.1 New Dashboard Components

#### Statistics Dashboard (User View)
**Location:** Main menu → "View Statistics"

**Components:**
1. **Date Selector**
   - Today / This Week / This Month / Custom Range
   
2. **Daily Summary Card**
   - Total Calories Consumed: XXX kcal
   - Total Calories Burned: XXX kcal
   - Net Balance: ±XXX kcal
   - Progress bar: min ←→ current ←→ max
   
3. **Nutrient Breakdown Card**
   - Pie chart: Carbs (%), Protein (%), Fat (%)
   - Bar chart: g consumed vs recommended
   - Calorie contribution per nutrient
   
4. **Weight Progress Card**
   - Current weight
   - Change this week
   - Change this month
   - Line chart with target line
   
5. **Goal Status Card**
   - Weekly weight loss: X.X kg / target kg
   - Daily calorie adherence: X/7 days
   - Activity minutes: XXX / target

6. **Action Buttons**
   - "Log Weight"
   - "View Weekly Report"
   - "View Monthly Report"
   - "Export Data"

---

#### Weekly/Monthly Report View
**Layout:**
- Header: Date range, user info
- Section 1: Calorie Trends (line chart)
- Section 2: Weight Progress (line chart with target)
- Section 3: Nutrient Balance (stacked bar chart)
- Section 4: Top Foods & Activities (tables)
- Section 5: Achievements & Recommendations

---

#### Coach Dashboard (Admin View)
**Location:** Admin login → "User Management"

**Components:**
1. **User List**
   - Filter: by adherence, by progress, by last activity
   - Sort: alphabetical, by weight loss, by goal adherence
   
2. **User Detail View**
   - Profile summary
   - Quick stats (last 7 days)
   - "Generate Report" button
   - "Create Dietary Plan" button
   
3. **Report Generation Interface**
   - Date range selector
   - Report type: Progress / Nutrient Analysis / Activity Summary
   - Export options: PDF / CSV
   
4. **Dietary Plan Creator**
   - Form with all plan fields
   - Template library (predefined plans)
   - Save as template option

---

## 5. Implementation Decisions & Recommendations

### 5.1 Database Changes (Priority Order)

**Phase 1 (Core Statistics):**
1. ✅ Enhance `statistics` table with nutrient columns
2. ✅ Create `weightlog` table
3. ✅ Add indexes for date-range queries

**Phase 2 (Coach Features):**
4. Create `dietary_plan` table
5. Create `user_restriction` table (replace simple allergies field)
6. Add coach-user relationship tracking

**Phase 3 (Advanced Features):**
7. Create `achievement` table (badges/milestones)
8. Create `food_recommendation` table (AI-based suggestions)

---

### 5.2 Data Ingestion Improvements

**Current State:**
- `sample_foods.csv` has 5 foods with nutrients ✅
- `sample_activities.csv` has 5 activities ❌ (missing kcal_per_unit format)

**Required Improvements:**

#### 5.2.1 Enhanced sample_foods.csv
```csv
name,kcal_per_portion,carbs_per_portion,protein_per_portion,fat_per_portion,category,common_allergens
Apple,52,14,0.3,0.2,Fruit,
Banana,89,23,1.1,0.3,Fruit,
Boiled Egg,155,1.1,13,11,Protein,Eggs
Chicken Breast,165,0,31,3.6,Protein,
Rice (cooked),130,28,2.7,0.3,Carbs,
Milk (200ml),122,9.4,6.4,4.6,Dairy,Lactose
Greek Yogurt,59,3.6,10,0.4,Dairy,Lactose
Salmon (100g),206,0,22,13,Protein,Fish
Broccoli,55,11,3.7,0.6,Vegetable,
Almonds (30g),170,6,6,15,Snack,Nuts
Whole Wheat Bread (slice),69,12,3.6,1.1,Carbs,Gluten
Peanut Butter (2 tbsp),188,7,8,16,Snack,Nuts
```

#### 5.2.2 Enhanced sample_activities.csv
```csv
name,unit,kcal_per_1000_units,category
Running,steps,80,Cardio
Cycling,minutes,60,Cardio
Swimming,minutes,70,Cardio
Walking,steps,40,Light Exercise
Yoga,minutes,30,Flexibility
Weight Training,minutes,50,Strength
Dancing,minutes,55,Cardio
Stairs Climbing,floors,8,Light Exercise
```

#### 5.2.3 NEW sample_restrictions.csv
```csv
restriction_type,food_ingredient,severity,description
allergy,Peanuts,severe,Anaphylaxis risk
allergy,Tree Nuts,severe,Anaphylaxis risk
allergy,Shellfish,severe,Anaphylaxis risk
allergy,Eggs,moderate,Digestive issues
intolerance,Lactose,moderate,Digestive discomfort
intolerance,Gluten,moderate,Celiac disease
preference,Meat,mild,Vegetarian
preference,Animal Products,mild,Vegan
medical,High Sodium,moderate,Hypertension
```

---

### 5.3 Service Layer Requirements

**New Services to Implement:**

#### 5.3.1 StatisticsService
```python
class StatisticsService:
    def get_daily_summary(user_id, date) -> Dict
    def get_weekly_summary(user_id, start_date) -> Dict
    def get_monthly_summary(user_id, start_date) -> Dict
    def calculate_nutrient_breakdown(user_id, date) -> Dict
    def calculate_weight_progress(user_id, period) -> Dict
    def generate_user_report(user_id, start_date, end_date) -> Dict
```

#### 5.3.2 WeightLogService
```python
class WeightLogService:
    def log_weight(user_id, date, weight, notes) -> Dict
    def get_weight_history(user_id, days=30) -> List[Dict]
    def get_latest_weight(user_id) -> float
    def calculate_weight_trend(user_id, period) -> Dict
```

#### 5.3.3 DietaryPlanService (Coach)
```python
class DietaryPlanService:
    def create_plan(coach_id, user_id, plan_data) -> Dict
    def get_user_active_plan(user_id) -> Dict
    def update_plan(plan_id, updates) -> Dict
    def get_plan_adherence(user_id, plan_id) -> Dict
```

---

### 5.4 Calculation Formulas

#### Nutrient Breakdown Calculation
```python
# For each food log entry:
actual_carbs_g = (portion_size_g / 100) * food.carbs_per_portion
actual_protein_g = (portion_size_g / 100) * food.protein_per_portion
actual_fat_g = (portion_size_g / 100) * food.fat_per_portion

# Total daily nutrients:
daily_carbs = SUM(actual_carbs_g for all food logs)
daily_protein = SUM(actual_protein_g for all food logs)
daily_fat = SUM(actual_fat_g for all food logs)

# Calorie contribution:
carbs_kcal = daily_carbs * 4  # 4 kcal per gram
protein_kcal = daily_protein * 4  # 4 kcal per gram
fat_kcal = daily_fat * 9  # 9 kcal per gram
```

#### Weight Loss Progress Calculation
```python
# Weekly progress:
week_start_weight = get_weight_on_date(date - 7_days)
current_weight = get_latest_weight()
weekly_change = current_weight - week_start_weight
weekly_target = user.weekly_weight_loss_target

progress_percentage = (weekly_change / weekly_target) * 100

# Status:
if progress_percentage >= 100:
    status = "On Track ✅"
elif progress_percentage >= 80:
    status = "Close 💪"
else:
    status = "Needs Attention ⚠️"
```

---

## 6. MVP Scope Recommendation

### What to Implement First (MVP):
1. ✅ **WeightLog table** - Simple weight tracking
2. ✅ **Enhanced Statistics table** - Add nutrient columns
3. ✅ **Daily Nutrient Breakdown view** - Show carbs/protein/fat
4. ✅ **Weekly Progress Report** - Basic calorie and weight trends
5. ✅ **Log Weight button** - Add to dashboards

### What to Defer (Future Versions):
- 🔮 Monthly reports (complex charts)
- 🔮 Coach dietary plan creation
- 🔮 Advanced user restrictions management
- 🔮 AI-based recommendations
- 🔮 Achievement badges
- 🔮 PDF export functionality

---

## 7. Next Steps

1. **Review this requirements document** - Confirm scope and priorities
2. **Create ERD diagram** - Visual database schema
3. **Create sequence diagrams** - For 3-5 core use cases
4. **Update database schema** - Add WeightLog, enhance Statistics
5. **Enhance sample data** - Improve CSV files with more realistic data
6. **Implement StatisticsService** - Core calculation logic
7. **Create Statistics Dashboard UI** - New view with cards and charts
8. **Add "Log Weight" feature** - Simple weight entry form
9. **Implement Weekly Report** - Basic version with line charts
10. **Testing & Refinement** - User acceptance testing

---

## 8. Open Questions for Discussion

1. **Meal categorization**: Should we automatically categorize meals by time?
   - Breakfast: 5-11 AM
   - Lunch: 11 AM - 3 PM
   - Dinner: 3-9 PM
   - Snacks: Other times
   
2. **Weight logging frequency**: How often should users log weight?
   - Recommendation: Once per week (same day/time)
   - Allow daily but show trend lines to reduce noise
   
3. **Coach features priority**: Should we implement coach features in MVP?
   - Recommendation: Start with user-facing statistics first
   - Add coach reporting in v2
   
4. **Chart library**: What charting library to use with Tkinter?
   - Options: matplotlib (recommended), plotly, tkinter-charts
   
5. **Data aggregation**: When to calculate statistics?
   - Option A: Real-time (calculate on demand)
   - Option B: Daily batch (pre-calculate at midnight)
   - Recommendation: Real-time for MVP, batch for optimization

---

## 9. Document Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v2.1.0 | 2025-12-20 | Development Team | Initial release for Statistics Core MVP |

---

**Document Version:** v2.1.0  
**Technical Name:** `laihdutanyt_statistics_requirements_v2_1.md`  
**Date:** 2025-12-20  
**Status:** Release Candidate  
**Next Review:** After v2.1.0 implementation complete
