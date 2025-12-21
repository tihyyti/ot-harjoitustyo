# Laihdutanyt Statistics & Reporting - Implementation Summary

## 📋 Document Overview

This directory contains comprehensive specifications for implementing statistics and reporting features in the Laihdutanyt application.

---

## 📚 Documentation Files

### 1. **statistics_requirements_v3.md**
**Purpose:** Detailed requirements specification for statistics and reporting features

**Contents:**
- Enhanced data model (8 entities with full schemas)
- 7 detailed use cases with flows
- UI component specifications
- Implementation decisions and recommendations
- MVP scope definition
- Sample data improvements
- Service layer requirements
- Calculation formulas

**Key Decisions:**
- Add `weightlog` table for weight tracking
- Enhance `statistics` table with nutrient breakdown
- Create `dietary_plan` table for coach features
- Create `user_restriction` table for structured allergies
- Implement StatisticsService, WeightLogService, DietaryPlanService

**MVP Scope:**
1. ✅ Weight tracking (WeightLog table)
2. ✅ Nutrient breakdown (carbs/protein/fat calculations)
3. ✅ Daily summary dashboard
4. ✅ Weekly progress report
5. ✅ Log weight button

---

### 2. **enhanced_ERD_v3.mmd**
**Purpose:** Entity-Relationship Diagram showing complete database schema

**Entities Included:**
- **Existing:** USER, ADMIN, FOOD, FOODLOG, ACTIVITY, ACTIVITYLOG, STATISTICS, RECOMMENDATION
- **New:** WEIGHTLOG, DIETARY_PLAN, USER_RESTRICTION

**Key Relationships:**
- USER ←→ WEIGHTLOG (one-to-many)
- USER ←→ STATISTICS (one-to-many, unique per date)
- USER ←→ DIETARY_PLAN (one-to-many)
- USER ←→ USER_RESTRICTION (one-to-many)
- ADMIN ←→ DIETARY_PLAN (coach creates plans)

**View Diagram:**
```bash
# View in VS Code with Mermaid extension or at https://mermaid.live
```

---

### 3. **Sequence Diagrams**

#### **sequence_uc1_daily_nutrient_breakdown.mmd**
**Use Case:** View Daily Nutrient Breakdown (User)

**Flow:**
1. User opens Statistics Dashboard
2. System fetches food and activity logs for selected date
3. System calculates:
   - Total calories consumed (from food)
   - Total calories burned (from activities)
   - Net balance (consumed - burned)
   - Nutrient breakdown (carbs, protein, fat in grams)
4. System displays:
   - Daily Summary Card with calorie balance
   - Nutrient Breakdown pie chart
   - Progress bar (min ← current → max)

**Key Formula:**
```
actual_nutrient_g = (portion_size_g / 100) * nutrient_per_portion
daily_total = SUM(actual_nutrient_g for all foods)
```

---

#### **sequence_uc2_weekly_progress_report.mmd**
**Use Case:** View Weekly Progress Report (User)

**Flow:**
1. User clicks "Weekly Report"
2. System fetches 7 days of statistics and weight logs
3. System calculates:
   - Average daily calories consumed/burned
   - Total net calorie deficit
   - Weight change over 7 days
   - Goal adherence percentage (days within calorie range)
4. System displays:
   - Line charts (calories over time, weight trend)
   - Bar chart (nutrient averages)
   - Summary cards with status indicators
   - Recommendations based on progress

**Success Criteria:**
- Green "On Track ✅" if meeting weekly weight loss goal
- Yellow "Close 💪" if achieving 80%+ of goal
- Red "Needs Attention ⚠️" if below 80%

---

#### **sequence_uc7_track_weight_goal.mmd**
**Use Case:** Track Weekly Weight Loss Goal (Automated)

**Flow:**
1. User logs new weight measurement
2. System validates input (weight > 0, < 500 kg)
3. System saves to WeightLog table
4. System calculates progress:
   - Weekly change (current - 7 days ago)
   - Monthly change (current - 30 days ago)
5. System compares to user's targets
6. System evaluates status and displays:
   - "You've lost 0.6 kg this week (target: 0.5 kg) 🎉"
   - Monthly progress indicator
7. System updates Statistics table with current_weight
8. System checks for milestones (e.g., 5kg total loss)

**Alerts:**
- Warning if weight change > 1.5 kg/week (too fast)
- Reminder if no weight logged in 14 days

---

#### **sequence_uc4_coach_generates_report.mmd**
**Use Case:** Generate User Progress Report (Coach/Admin)

**Flow:**
1. Coach logs in and selects user
2. Coach clicks "Generate Progress Report"
3. Coach selects date range (default: last 30 days)
4. System gathers:
   - User profile summary
   - 30 days of statistics
   - Weight history
   - Top 10 foods and activities
   - Goal adherence metrics
5. System analyzes patterns and generates recommendations
6. System displays comprehensive report:
   - Weight progress chart (actual vs target)
   - Calorie trends chart
   - Nutrient balance analysis
   - Goal adherence metrics (% of days in range)
   - System recommendations
   - Coach notes area
7. Coach can:
   - Add personal notes
   - Export as PDF
   - Create dietary plan
   - Send report to user

---

#### **sequence_uc5_coach_creates_dietary_plan.mmd**
**Use Case:** Create Dietary Plan Recommendation (Coach/Admin)

**Flow:**
1. Coach clicks "Create Dietary Plan" from user profile
2. System pre-fills form with:
   - User's current goals (kcal_min/max)
   - Recent nutrient averages (last 30 days)
3. Coach fills plan details:
   - Plan name and description
   - Daily targets (kcal, protein, carbs, fat)
   - Weekly targets (weight loss, exercise minutes)
   - Duration (start and end dates)
4. System validates:
   - Realistic calorie ranges (1200-3500 kcal)
   - Safe weight loss rate (≤ 1.0 kg/week)
   - Nutrient balance
   - Date logic (start < end)
5. If user has active plan, coach can deactivate it
6. System creates new plan in dietary_plan table
7. System updates user's kcal_min/max to match plan
8. System creates notification for user
9. User sees active plan card in their dashboard

**Validation Rules:**
- kcal_min >= 1200 (minimum safe intake)
- kcal_max <= 3500 (maximum reasonable)
- weekly_loss <= 1.0 kg (safe rate: 0.5-1.0 kg/week)
- start_date < end_date

---

## 🗄️ Database Schema Changes

### **Required Changes (MVP):**

#### 1. Create WEIGHTLOG table
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

#### 2. Enhance STATISTICS table
```sql
-- Add new columns to existing statistics table
ALTER TABLE statistics ADD COLUMN total_kcal_burned REAL;
ALTER TABLE statistics ADD COLUMN net_kcal REAL;
ALTER TABLE statistics ADD COLUMN total_carbs_g REAL;
ALTER TABLE statistics ADD COLUMN total_protein_g REAL;
ALTER TABLE statistics ADD COLUMN total_fat_g REAL;
ALTER TABLE statistics ADD COLUMN food_entries_count INTEGER;
ALTER TABLE statistics ADD COLUMN activity_entries_count INTEGER;

-- Add unique constraint
CREATE UNIQUE INDEX idx_statistics_user_date ON statistics(user_id, date);
```

### **Optional Changes (Future):**

#### 3. Create DIETARY_PLAN table (Coach feature)
```sql
CREATE TABLE IF NOT EXISTS dietary_plan (
    plan_id TEXT PRIMARY KEY,
    coach_id TEXT NOT NULL,
    user_id TEXT,
    plan_name TEXT NOT NULL,
    description TEXT,
    target_kcal_min REAL,
    target_kcal_max REAL,
    target_protein_g REAL,
    target_carbs_g REAL,
    target_fat_g REAL,
    weekly_weight_loss_kg REAL,
    weekly_exercise_minutes INTEGER,
    start_date TEXT,
    end_date TEXT,
    status TEXT DEFAULT 'active',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(coach_id) REFERENCES admin(admin_id) ON DELETE CASCADE,
    FOREIGN KEY(user_id) REFERENCES "user"(user_id) ON DELETE CASCADE
);
```

#### 4. Create USER_RESTRICTION table
```sql
CREATE TABLE IF NOT EXISTS user_restriction (
    restriction_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    restriction_type TEXT NOT NULL,
    food_ingredient TEXT,
    severity TEXT,
    notes TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES "user"(user_id) ON DELETE CASCADE
);
```

---

## 🚀 Implementation Steps

### **Phase 1: Database & Core Services (Week 1)**
1. [ ] Update `src/create_db.py` with WeightLog and enhanced Statistics tables
2. [ ] Create `src/repositories/weightlog_repository.py`
3. [ ] Create `src/services/weightlog_service.py`
4. [ ] Create `src/services/statistics_service.py`
5. [ ] Write unit tests for new services

### **Phase 2: Weight Tracking UI (Week 1-2)**
6. [ ] Create "Log Weight" button in main dashboard
7. [ ] Create weight entry form (date, weight, notes)
8. [ ] Add weight history display (simple list or line chart)
9. [ ] Test weight logging workflow

### **Phase 3: Daily Nutrient Breakdown (Week 2)**
10. [ ] Implement `get_daily_summary()` in StatisticsService
11. [ ] Calculate nutrient breakdown from FoodLogs
12. [ ] Create Statistics Dashboard UI
13. [ ] Add Daily Summary Card (calories, net balance)
14. [ ] Add Nutrient Breakdown visualization (pie chart or bars)
15. [ ] Add progress bar (min ← current → max)

### **Phase 4: Weekly Progress Report (Week 3)**
16. [ ] Implement `get_weekly_summary()` in StatisticsService
17. [ ] Calculate weekly averages and trends
18. [ ] Create Weekly Report UI view
19. [ ] Add calorie trend line chart (matplotlib)
20. [ ] Add weight trend line chart
21. [ ] Add goal adherence metrics
22. [ ] Add recommendations based on progress

### **Phase 5: Testing & Refinement (Week 4)**
23. [ ] Generate sample data (30 days of logs)
24. [ ] User acceptance testing
25. [ ] Fix bugs and improve UI
26. [ ] Documentation and user guide
27. [ ] Performance optimization (if needed)

### **Phase 6: Coach Features (Future)**
28. [ ] Implement DietaryPlanService
29. [ ] Create Coach Dashboard
30. [ ] Create User Progress Report generation
31. [ ] Create Dietary Plan creation UI
32. [ ] Add PDF export functionality

---

## 📊 Sample Data Requirements

### **Enhanced sample_foods.csv**
Current file has 5 foods. Need to expand to 20-30 common foods with:
- Breakfast items (cereal, toast, yogurt, eggs)
- Lunch/dinner items (chicken, fish, rice, pasta, vegetables)
- Snacks (nuts, fruits, chips)
- Beverages (juice, milk, coffee)
- Complete nutrient data (carbs, protein, fat)

### **Enhanced sample_activities.csv**
Current file has 5 activities but wrong format. Fix to include:
- `kcal_per_1000_units` instead of `calories_per_activity`
- More activities (10-15 types)
- Categories: Cardio, Strength, Flexibility, Light Exercise

### **NEW sample_restrictions.csv**
Create file with common dietary restrictions:
- Allergies: Peanuts, Tree Nuts, Shellfish, Eggs
- Intolerances: Lactose, Gluten
- Preferences: Vegetarian, Vegan
- Medical: Low sodium, Low sugar

---

## 🧮 Key Calculation Formulas

### **Nutrient Calculation**
```python
# For each food log entry
actual_carbs_g = (portion_size_g / 100) * food.carbs_per_portion
actual_protein_g = (portion_size_g / 100) * food.protein_per_portion
actual_fat_g = (portion_size_g / 100) * food.fat_per_portion

# Daily totals
daily_carbs = SUM(actual_carbs_g for all food logs today)
daily_protein = SUM(actual_protein_g for all food logs today)
daily_fat = SUM(actual_fat_g for all food logs today)

# Calorie contribution (1g carbs = 4 kcal, 1g protein = 4 kcal, 1g fat = 9 kcal)
carbs_kcal = daily_carbs * 4
protein_kcal = daily_protein * 4
fat_kcal = daily_fat * 9
total_kcal = carbs_kcal + protein_kcal + fat_kcal
```

### **Weight Progress Calculation**
```python
# Weekly progress
week_start_weight = get_weight_on_date(today - 7 days)
current_weight = get_latest_weight()
weekly_change = current_weight - week_start_weight
weekly_target = user.weight_loss_target

progress_pct = (abs(weekly_change) / weekly_target) * 100

# Status
if progress_pct >= 100:
    status = "On Track ✅"
elif progress_pct >= 80:
    status = "Close 💪"
else:
    status = "Needs Attention ⚠️"
```

### **Goal Adherence Calculation**
```python
# Daily adherence
is_within_goal = (user.kcal_min <= net_kcal <= user.kcal_max)

# Weekly adherence
days_within_goal = COUNT(days where is_within_goal == True)
adherence_pct = (days_within_goal / 7) * 100
```

---

## 🎨 UI Component Specifications

### **Statistics Dashboard Layout**
```
┌─────────────────────────────────────────────┐
│  Statistics Dashboard - [Username]          │
├─────────────────────────────────────────────┤
│  Date: [Today ▼] [This Week] [This Month]  │
├──────────────────┬──────────────────────────┤
│ Daily Summary    │  Nutrient Breakdown      │
│ ─────────────    │  ────────────────        │
│ Consumed: 1850   │   [Pie Chart]            │
│ Burned:    350   │   Carbs: 180g (39%)      │
│ Net:      1500   │   Protein: 95g (21%)     │
│ Status: ✅       │   Fat: 65g (32%)         │
│                  │                           │
│ [Progress Bar]   │   [Bar Chart vs Goals]   │
│ 1500 ━━━━ 2500  │                           │
├──────────────────┴──────────────────────────┤
│ Weight Progress                              │
│ ─────────────────                            │
│ Current: 78.5 kg   This week: -0.6 kg 🎉   │
│ [Line Chart: 30 days]                        │
├──────────────────────────────────────────────┤
│ Goal Status                                  │
│ ─────────────                                │
│ ✅ Weekly weight loss: On track              │
│ ✅ Calorie adherence: 6/7 days (85.7%)       │
│ ⚠️  Activity minutes: 120/150                │
├──────────────────────────────────────────────┤
│ [Log Weight] [Weekly Report] [Monthly]      │
└──────────────────────────────────────────────┘
```

---

## 🔧 Technical Decisions

### **Chart Library: matplotlib**
- ✅ **Pros:** Well-established, feature-rich, good Tkinter integration
- ✅ **Pros:** Can export to images for PDF reports
- ❌ **Cons:** Requires `matplotlib` dependency
- **Alternative:** Custom Tkinter Canvas drawings (more work, less features)

### **Data Aggregation Strategy: Real-time (MVP)**
- Calculate statistics on-demand when user requests
- No background jobs or scheduled tasks
- **Future:** Implement daily batch calculation at midnight for optimization

### **Weight Tracking Frequency: Flexible**
- Allow daily logging but recommend weekly
- Use trend lines to smooth out daily fluctuations
- Show weekly/monthly averages to reduce noise

### **Coach Features Priority: Phase 2**
- Focus on user-facing statistics first (MVP)
- Add coach reporting and dietary plans in Phase 2
- Simplifies initial implementation

---

## 📝 Open Questions

1. **Meal categorization:** Automatically categorize by time or let user choose?
   - Recommendation: Auto-categorize (Breakfast: 5-11 AM, Lunch: 11 AM-3 PM, etc.)

2. **Statistics persistence:** Pre-calculate daily stats or calculate on-demand?
   - Recommendation: On-demand for MVP, batch calculation for v2

3. **Chart interactivity:** Static images or interactive charts?
   - Recommendation: Static images for MVP (matplotlib), consider plotly for v2

4. **PDF export:** Essential for MVP or defer to v2?
   - Recommendation: Defer to v2, focus on on-screen reports first

5. **Achievement system:** Implement badges/milestones?
   - Recommendation: Simple milestone popups in MVP (e.g., "5kg lost!"), full system in v2

---

## 📈 Success Metrics

### **MVP Success Criteria:**
- [ ] Users can log weight measurements
- [ ] Users can view daily nutrient breakdown
- [ ] Users can see weekly progress report with charts
- [ ] System calculates and displays goal adherence
- [ ] UI is intuitive and responsive
- [ ] All calculations are accurate and tested

### **User Satisfaction Indicators:**
- Users log weight at least weekly
- Users check statistics dashboard regularly
- Users report motivation from progress visualization
- Users understand their nutrient intake

---

## 📚 Related Documentation

- **Original Requirements:** `laihdutanyt_requirements_specification_v2.md`
- **Architecture:** `laihdutanyt_v2_architecture.drawio`
- **Current ERD:** `laihdutanyt_ERD_v2.pdf`
- **Class Diagram:** `laihdutanyt_v2_classes.drawio`

---

**Last Updated:** 2025-12-20  
**Status:** Ready for Implementation  
**Next Action:** Review with team and begin Phase 1 (Database & Core Services)
