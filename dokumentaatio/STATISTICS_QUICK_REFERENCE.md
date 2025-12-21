# 📊 Laihdutanyt Statistics Feature - Quick Reference

## 🎯 What We're Building

A comprehensive **statistics and reporting system** that allows users to:
- Track weight loss progress over time
- View daily nutrient breakdown (carbs, protein, fat)
- See weekly and monthly reports with charts
- Monitor goal adherence (calorie targets, weight loss targets)
- Get automated progress feedback

And allows coaches to:
- Generate user progress reports
- Create personalized dietary plans
- Track user adherence and outcomes

---

## 📁 Documentation Structure

```
dokumentaatio/
├── statistics_requirements_v3.md          ← Full requirements (20 pages)
├── enhanced_ERD_v3.mmd                    ← Database schema diagram
├── sequence_uc1_daily_nutrient_breakdown.mmd   ← User views daily stats
├── sequence_uc2_weekly_progress_report.mmd     ← User views weekly report
├── sequence_uc7_track_weight_goal.mmd          ← User logs weight
├── sequence_uc4_coach_generates_report.mmd     ← Coach creates report
├── sequence_uc5_coach_creates_dietary_plan.mmd ← Coach creates plan
└── STATISTICS_IMPLEMENTATION_GUIDE.md     ← This summary + steps
```

---

## 🗄️ Database Changes Summary

### ✅ Required for MVP

**1. NEW TABLE: weightlog**
- Tracks weight measurements over time
- Fields: log_id, user_id, date, weight, notes

**2. ENHANCE TABLE: statistics**
- Add nutrient columns: total_carbs_g, total_protein_g, total_fat_g
- Add activity columns: total_kcal_burned, net_kcal
- Add counts: food_entries_count, activity_entries_count

### 🔮 Optional for Future

**3. NEW TABLE: dietary_plan** (coach feature)
- Personalized meal plans created by coaches
- Fields: plan_id, coach_id, user_id, targets, duration, status

**4. NEW TABLE: user_restriction**
- Structured allergy/dietary restriction management
- Replaces simple TEXT allergies field

---

## 🚀 MVP Implementation Checklist

### Phase 1: Core Infrastructure ✅
- [ ] Update database schema (weightlog + enhanced statistics)
- [ ] Create WeightLogRepository
- [ ] Create WeightLogService
- [ ] Create StatisticsService
- [ ] Write unit tests

### Phase 2: Weight Tracking 🏋️
- [ ] Add "Log Weight" button to dashboard
- [ ] Create weight entry form (date, weight, notes)
- [ ] Display recent weight history
- [ ] Show weight trend (simple line chart)

### Phase 3: Daily Stats 📊
- [ ] Implement daily summary calculation
- [ ] Create Statistics Dashboard view
- [ ] Show total calories consumed/burned/net
- [ ] Show nutrient breakdown (carbs/protein/fat)
- [ ] Display progress bar (min ← current → max)

### Phase 4: Weekly Report 📈
- [ ] Implement weekly summary calculation
- [ ] Create Weekly Report view
- [ ] Add calorie trend line chart
- [ ] Add weight trend line chart
- [ ] Calculate and display goal adherence %
- [ ] Generate automated recommendations

### Phase 5: Polish & Test ✨
- [ ] Generate sample data (30 days)
- [ ] User acceptance testing
- [ ] Bug fixes and UI improvements
- [ ] Documentation

---

## 🎨 UI Mockups

### Daily Stats Dashboard
```
┌─────────────────────────────────────┐
│  📊 Statistics - [Date Selector]    │
├─────────────────────────────────────┤
│  Daily Summary                      │
│  ┌─────────────┐ ┌───────────────┐ │
│  │ Consumed    │ │ Nutrient      │ │
│  │ 1850 kcal   │ │ Breakdown     │ │
│  │             │ │ [Pie Chart]   │ │
│  │ Burned      │ │ Carbs: 180g   │ │
│  │  350 kcal   │ │ Protein: 95g  │ │
│  │             │ │ Fat: 65g      │ │
│  │ Net: 1500   │ │               │ │
│  │ Status: ✅  │ └───────────────┘ │
│  └─────────────┘                   │
│                                     │
│  Progress: 1500━━━━━━━━━━2500      │
│            min     current    max   │
├─────────────────────────────────────┤
│  Weight: 78.5 kg  (-0.6 this week) │
│  [Log Weight] [Weekly Report]      │
└─────────────────────────────────────┘
```

### Weekly Report
```
┌──────────────────────────────────────┐
│  📈 Weekly Progress Report           │
├──────────────────────────────────────┤
│  Summary (Last 7 Days)               │
│  ┌────────────────────────────────┐  │
│  │ Weight Loss: -0.6 kg (✅)      │  │
│  │ Target:      -0.5 kg/week      │  │
│  │ Adherence:   6/7 days (85.7%)  │  │
│  └────────────────────────────────┘  │
│                                      │
│  Calorie Trends                      │
│  [Line Chart]                        │
│  2500 ┤     ╱╲    ╱╲                │
│  2000 ┤   ╱    ╲╱    ╲               │
│  1500 ┤ ╱              ╲             │
│       └───────────────────→          │
│        Mon  Tue  Wed  Thu  Fri       │
│                                      │
│  Weight Trend                        │
│  [Line Chart]                        │
│  79 kg ┤╲                            │
│  78 kg ┤  ╲__                        │
│  77 kg ┤      ╲__                    │
│       └───────────────────→          │
│                                      │
│  Recommendations:                    │
│  ✅ Excellent progress!              │
│  💡 Consider increasing protein      │
└──────────────────────────────────────┘
```

---

## 🧮 Key Formulas

### Nutrient Calculation
```python
# User eats 150g of chicken (100g = 165 kcal, 31g protein)
actual_kcal = (150 / 100) * 165 = 247.5 kcal
actual_protein = (150 / 100) * 31 = 46.5g

# Daily total: SUM all foods
```

### Weight Progress
```python
# Weekly change
weekly_change = current_weight - weight_7_days_ago
progress_pct = (abs(weekly_change) / target) * 100

# Status
if progress_pct >= 100: "On Track ✅"
elif progress_pct >= 80: "Close 💪"
else: "Needs Attention ⚠️"
```

### Goal Adherence
```python
# Daily check
is_within_goal = (kcal_min <= net_kcal <= kcal_max)

# Weekly adherence
days_ok = COUNT(days where is_within_goal)
adherence = (days_ok / 7) * 100  # e.g., 85.7%
```

---

## 📝 Sample Data Needs

### Current State ❌
- `sample_foods.csv`: 5 foods ❌ (need 20-30)
- `sample_activities.csv`: 5 activities, wrong format ❌

### Required Improvements ✅
1. **Expand sample_foods.csv** to 20-30 items:
   - Breakfast: Cereal, Toast, Yogurt, Eggs
   - Lunch/Dinner: Chicken, Fish, Rice, Pasta, Vegetables
   - Snacks: Nuts, Fruits, Chips
   - Beverages: Juice, Milk
   - All with complete nutrient data

2. **Fix sample_activities.csv** format:
   - Change `calories_per_activity` → `kcal_per_1000_units`
   - Add unit column (steps, minutes, etc.)
   - Expand to 10-15 activities

3. **Create sample_restrictions.csv**:
   - Common allergies (Peanuts, Shellfish, Eggs)
   - Intolerances (Lactose, Gluten)
   - Preferences (Vegetarian, Vegan)

---

## 🔧 Technical Stack

| Component | Technology | Why |
|-----------|-----------|-----|
| Database | SQLite | Already in use, simple |
| Backend | Python Services | Existing architecture |
| UI | Tkinter | Current framework |
| Charts | matplotlib | Best Tkinter integration |
| Testing | pytest | Standard Python testing |

---

## 📊 Success Metrics

After MVP implementation:
- ✅ Users can log weight weekly
- ✅ Users can view daily nutrient breakdown
- ✅ Users can see weekly progress with charts
- ✅ System calculates goal adherence accurately
- ✅ UI is responsive and intuitive

---

## 🎓 Learning Resources

**Matplotlib with Tkinter:**
- [matplotlib.org/stable/gallery/user_interfaces/embedding_in_tk_sgskip.html](https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_tk_sgskip.html)

**SQLite Date Functions:**
- Use `DATE('now', '-7 days')` for date arithmetic
- Format dates as 'YYYY-MM-DD' strings

**Tkinter Layouts:**
- Use `pack()` for simple vertical stacking
- Use `grid()` for complex layouts with rows/columns
- Use `Frame` to group related widgets

---

## 🤔 Decision Points

### 1. Chart Library
**Chosen:** matplotlib  
**Why:** Best integration with Tkinter, widely used, can export images

### 2. When to Calculate Statistics
**Chosen:** On-demand (MVP)  
**Future:** Nightly batch calculation for optimization

### 3. Weight Logging Frequency
**Recommended:** Weekly (same day/time)  
**Allowed:** Daily (show trends to reduce noise)

### 4. Coach Features Priority
**Chosen:** Phase 2 (after MVP)  
**Why:** Focus on user-facing features first

---

## 📞 Questions?

Review the full documentation files for:
- **Detailed requirements:** `statistics_requirements_v3.md`
- **Database schema:** `enhanced_ERD_v3.mmd`
- **Use case flows:** `sequence_uc*.mmd` files
- **Implementation guide:** `STATISTICS_IMPLEMENTATION_GUIDE.md`

---

**Status:** Ready for Development  
**Estimated Effort:** 3-4 weeks for MVP  
**Next Step:** Begin Phase 1 (Database & Core Services)
