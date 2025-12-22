# Laihdutanyt User Instructions

## Comprehensive Guide to Weight Loss Tracking Application

**Version:** 2.2
**Last Updated:** December 21, 2025

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [First Time Setup](#first-time-setup)
3. [Login Window](#login-window)
4. [Main Menu Dashboard](#main-menu-dashboard)
5. [Window Management](#window-management)
6. [Food Tracking](#food-tracking)
7. [Activity Tracking](#activity-tracking)
8. [Weight Logging](#weight-logging)
9. [Dietary Periods](#dietary-periods)
10. [Daily Totals](#daily-totals)
11. [Tips & Tricks](#tips--tricks)
12. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Prerequisites
- Python 3.10+ (tested with 3.9.13, 3.10.x, 3.11.x, and 3.12.3)
- Tkinter installed
- Database initialized
- (Optional) Sample data imported

### Launch Application
```bash
poetry run invoke start
```

---

## First Time Setup

### 1. Database Initialization

```bash
# Initialize the database
poetry run invoke init-db
```

This creates `src/data/laihdutanyt.db` with all necessary tables.

### 2. (Optional) Import Sample Data

```bash
# Import sample foods
poetry run python src/scripts/import_foods.py

# Import sample activities
poetry run python src/scripts/import_activities.py
```

**Sample foods include:** Apple, Banana, Boiled Egg, Chicken Breast, Rice

**Sample activities include:** Running, Cycling, Swimming, Walking, Yoga

---

## Login Window

### Application Description

When you launch the app, you'll see:

```
┌─────────────────────────────────┐
│     Laihdutanyt Login           │
├─────────────────────────────────┤
│ Username: [            ]        │
│ Password: [            ]        │
│                                 │
│ [User Login] [Admin Login]      │
│ [Register New User]             │
│                                 │
│ ┌──────────────────────────┐   │
│ │ 📊 Application Info      │   │
│ │ • Food & Activity        │   │
│ │ • Weight Tracking        │   │
│ │ • Period Analysis        │   │
│ │ • 8 Protocol Templates   │   │
│ │ ⚠ Admin features are stubs│   │
│ └──────────────────────────┘   │
└─────────────────────────────────┘
```

### Demo Credentials

**Regular User:**
- Username: `user`
- Password: `pass`

**Admin (Stub Only):**
- Username: `admin`
- Password: `apass`

### Creating a New Account

1. Click **"Register New User"**
2. Fill in required fields:
   - **Username*** (required)
   - **Password*** (required, minimum 4 characters)
3. Optional fields:
   - Weight (kg)
   - Height (cm)
   - Age (years)
   - Activity Level (1-5)
   - Allergies
   - Daily Kcal Min/Max
   - Target Weight (kg)
4. Click **"Create User"**
5. Return to login screen and enter your credentials

**Validation:**
- Username cannot be empty
- Password minimum 4 characters
- Weight: 0-500 kg
- Height: 50-300 cm
- Age: 10-120 years
- Activity Level: 1-5
- Kcal Min < Kcal Max

---

## Main Menu Dashboard

After logging in, you'll see the main button menu (420x750 px):

```
┌──────────────────────────┐
│ Welcome, <username>!     │
├──────────────────────────┤
│ [1] Food Dashboard       │
│ [2] Activity Dashboard   │
│ [3] Daily Food Totals    │
│ [4] Daily Activity       │
│     Totals               │
│ [5] Weight Logging       │
│ [6] Dietary Periods      │
├──────────────────────────┤
│ Window Management:       │
│ [Grid Layout]            │
│ [Cascade]                │
│ [Hide/Show]              │
└──────────────────────────┘
```

### Button Functions

**Dashboard Buttons (1-6):**
- **Button 1:** Food tracking and logging
- **Button 2:** Activity tracking and logging
- **Button 3:** Daily food calorie totals
- **Button 4:** Daily activity calorie totals
- **Button 5:** Weight tracking with period annotations
- **Button 6:** Dietary period management

**Window Management:**
- **Grid Layout:** Organize all windows in a grid
- **Cascade:** Arrange windows in cascading layout
- **Hide/Show:** Toggle all windows at once

---

## Window Management

### Grid Layout Mode

Click **"Grid Layout"** to arrange windows in a 2x3 grid:

```
LEFT HALF (Analysis):      RIGHT HALF (Logging):
┌──────────────────┐      ┌──────────────────┐
│ 1. Periods       │      │ 3. Food          │
│    Dashboard     │      │    Dashboard     │
├──────────────────┤      ├──────────────────┤
│ 2. Weight        │      │ 4. Activity      │
│    Logging       │      │    Dashboard     │
├──────────────────┤      ├──────────────────┤
│ 5. Food Totals   │      │ 6. Activity      │
│                  │      │    Totals        │
└──────────────────┘      └──────────────────┘
```

**Features:**
- Opens all 6 dashboards automatically
- Positions them in logical groupings
- Analysis tools on left (Periods, Weight)
- Logging tools on right (Food, Activity)
- Independent of menu position

**Best for:**
- Large displays (27"+ or dual monitor)
- Working with multiple dashboards
- Comparing different data views

### Cascade Layout Mode

Click **"Cascade"** for overlapping windows:

```
  ┌──────┐
  │ Win1 │
  └┬─────┘
   └┬─────┐
    │ Win2│
    └┬────┘
     └────┐
      Win3│
      ────┘
```

**Features:**
- Windows follow the menu position
- Click title bars to bring window to front
- Drag windows to reposition
- Buttons 5 & 6 toggle expand/shrink

**Best for:**
- Laptop screens
- Single monitor setups
- Focusing on one dashboard at a time

### Toggle Expand/Shrink (Buttons 5 & 6)

**For Weight Logging (Button 5):**
- First click: Opens at full size (900x700)
- Next click: Shrinks to card size (450x400)
- Next click: Expands back to full size

**For Dietary Periods (Button 6):**
- First click: Opens at full size (1000x750)
- Next click: Shrinks to card size (450x400)
- Next click: Expands back to full size

**Use cases:**
- Quickly minimize to see other windows
- Expand when you need details
- Great for Cascade mode workflow

### Hide/Show Button

- **First click:** Hides all open dashboards
- **Second click:** Shows all hidden dashboards
- Menu stays visible
- Useful for quick desktop clearing

---

## Food Tracking

### Opening Food Dashboard

1. Click **Button 1 - Food Dashboard**
2. Dashboard opens (520x850 px or card size)

### Dashboard Layout

```
┌─────────────────────────────────┐
│ Food Log - <date>               │
├─────────────────────────────────┤
│ Date: [YYYY-MM-DD] [Pick]       │
│                                 │
│ Food: [Select ▼]                │
│ Portions: [1.0]                 │
│                                 │
│ [Add Food Log]                  │
├─────────────────────────────────┤
│ Today's Food Logs:              │
│ ┌─────────────────────────────┐ │
│ │ Apple  - 1.0 port - 52 kcal │ │
│ │ Banana - 2.0 port - 178 kcal│ │
│ └─────────────────────────────┘ │
│                                 │
│ Total Calories: 230 kcal        │
│                                 │
│ [View All Food Logs]            │
└─────────────────────────────────┘
```

### Adding Food Log

1. **Select Date:**
   - Default: Today
   - Click calendar icon to pick date
   - Can log for past or future dates

2. **Choose Food:**
   - Click dropdown
   - Select from available foods
   - Or start typing to filter

3. **Enter Portions:**
   - Default: 1.0
   - Use decimal (e.g., 0.5, 1.5, 2.0)
   - Represents standard serving size

4. **Click "Add Food Log"**
   - Log saves to database
   - Appears in today's list
   - Calories automatically calculated

### View All Food Logs

1. Click **"View All Food Logs"** button
2. New window opens with complete history
3. Shows: Date, Food, Portions, Calories, Actions

### Editing/Deleting Logs

1. In "All Food Logs" window:
2. **Click a row** to select it
3. Options appear:
   - **Edit:** Change portions, date
   - **Delete:** Remove log entry
4. Changes save immediately

### Adding New Foods

Currently, new foods must be added directly to the database:

```bash
# Option 1: Using Python
poetry run python
>>> from services import FoodService
>>> service = FoodService('src/data/laihdutanyt.db')
>>> service.add_food('Pizza', 250, 30, 12, 10)

# Option 2: Import from CSV
# Edit src/data/sample_foods.csv, then:
poetry run python src/scripts/import_foods.py
```

---

## Activity Tracking

### Opening Activity Dashboard

1. Click **Button 2 - Activity Dashboard**
2. Dashboard opens (520x850 px or card size)

### Dashboard Layout

```
┌─────────────────────────────────┐
│ Activity Log - <date>           │
├─────────────────────────────────┤
│ Date: [YYYY-MM-DD] [Pick]       │
│                                 │
│ Activity: [Select ▼]            │
│ Duration: [30] minutes          │
│                                 │
│ [Add Activity Log]              │
├─────────────────────────────────┤
│ Today's Activity Logs:          │
│ ┌─────────────────────────────┐ │
│ │ Running - 30min - 300 kcal  │ │
│ │ Walking - 45min - 225 kcal  │ │
│ └─────────────────────────────┘ │
│                                 │
│ Total Burned: 525 kcal          │
│                                 │
│ [View All Activity Logs]        │
└─────────────────────────────────┘
```

### Adding Activity Log

1. **Select Date:**
   - Default: Today
   - Can log activities from past

2. **Choose Activity:**
   - Dropdown list
   - Running, Cycling, Swimming, Walking, Yoga, etc.

3. **Enter Duration:**
   - In minutes
   - Whole numbers (e.g., 30, 45, 60)

4. **Click "Add Activity Log"**
   - Calculates calories burned
   - Shows in today's list

### Activity Calorie Calculation

Calories = (Calories per activity) × (Duration / 60)

**Example:**
- Running: 300 kcal/hour
- Duration: 30 minutes
- Burned: 300 × (30/60) = 150 kcal

---

## Weight Logging

### Opening Weight Dashboard

1. Click **Button 5 - Weight Logging**
2. Opens at 900x700 (full) or 450x400 (card)
3. **Toggle:** Click button 5 again to shrink/expand

### Dashboard Features

```
┌─────────────────────────────────────┐
│ Weight Tracking - <username>        │
├─────────────────────────────────────┤
│ 📍 Active Periods (3): Low Carb...  │
├─────────────────────────────────────┤
│ Date: [YYYY-MM-DD]                  │
│ Weight (kg): [75.5]                 │
│ Notes: [Feeling great!]             │
│                                     │
│ [Log Weight]                        │
├─────────────────────────────────────┤
│ Weight History:                     │
│ ┌─────────────────────────────────┐ │
│ │Date│Week│Weight│Change│Periods│  │
│ ├────┼────┼──────┼──────┼───────┤  │
│ │2025│W51 │75.5kg│-0.5  │Low... │  │
│ │2025│W50 │76.0kg│-0.3  │Low... │  │
│ └─────────────────────────────────┘ │
│                                     │
│ Progress: Start: 78kg → Current: 75.5│
│ Total Loss: -2.5 kg                 │
│ Weekly Avg: -0.4 kg/week            │
└─────────────────────────────────────┘
```

### Logging Your Weight

1. **Select Date:**
   - Default: Today
   - Can log historical weights

2. **Enter Weight:**
   - In kilograms (decimal allowed)
   - Example: 75.5, 68.3, 82.0

3. **Add Notes (Optional):**
   - How you're feeling
   - Special events
   - Observations

4. **Click "Log Weight"**
   - Saves to database
   - Updates history table
   - Recalculates progress

### Understanding the History Table

**Columns:**
- **Date:** When weight was logged
- **Week:** ISO week number (W01-W52)
- **Weight:** Recorded weight in kg
- **Change:** Difference from previous entry
- **Periods:** Active dietary periods (shows first 3)

**Color Coding:**
- **Yellow:** Today's date
- **Green:** Future dates (planning)
- **White:** Past dates

### Active Periods Header

Shows which dietary periods are currently active:
- **0-3 periods:** Shows all names
- **4+ periods:** Shows first 3 + count
  - Example: "Low Carb, Time Restricted, Portion Control... (+2 more)"

### Progress Summary

Bottom panel shows:
- **Start Weight:** First recorded weight
- **Current Weight:** Most recent entry
- **Total Loss/Gain:** Overall change
- **Weekly Average:** Average change per week
- **Weight Change:** Last entry vs previous

---

## Dietary Periods

### Opening Periods Dashboard

1. Click **Button 6 - Dietary Periods**
2. Opens at 1000x750 (full) or 450x400 (card)
3. **Toggle:** Click button 6 again to shrink/expand

### Dashboard Layout

```
┌──────────────────┬──────────────────┐
│ Create Period    │ Your Periods     │
│                  │                  │
│ Period Name:     │ ┌──────────────┐ │
│ [______]         │ │📍 Active     │ │
│                  │ │ Low Carb     │ │
│ Protocol Type:   │ │ 14 days      │ │
│ [Select ▼]       │ └──────────────┘ │
│                  │                  │
│ Start: [Date]    │ ┌──────────────┐ │
│ End: [Date]      │ │✓ Completed   │ │
│                  │ │ IF 5:2       │ │
│ Description:     │ │ -1.5 kg      │ │
│ [________]       │ └──────────────┘ │
│                  │                  │
│ [Create Period]  │ [View Details]   │
│                  │ [End Period]     │
├──────────────────┴──────────────────┤
│ 💡 Suggested Protocols (Click!)     │
│ ┌────────────────────────────────┐  │
│ │ Time-Restricted Eating (16:8)  │  │
│ │ Fast for 16 hours...           │  │
│ │ Duration: 2-4 weeks [Use This] │  │
│ ├────────────────────────────────┤  │
│ │ Intermittent Fasting (5:2)     │  │
│ │ Eat normally 5 days...         │  │
│ │ Duration: 3-4 weeks [Use This] │  │
│ └────────────────────────────────┘  │
└─────────────────────────────────────┘
```

### Creating a Dietary Period

**Method 1: From Scratch**

1. Enter **Period Name**
   - Example: "My Low Carb Trial"

2. Select **Protocol Type:**
   - custom
   - time_restricted
   - meal_timing
   - intermittent_fasting
   - low_carb
   - calorie_cycling
   - portion_control
   - food_elimination

3. Choose **Start Date**
   - Usually today or near future

4. (Optional) **End Date**
   - Leave blank for ongoing
   - Or set trial duration

5. Add **Description** (optional)
   - Your goals
   - Rules you'll follow
   - Notes

6. Click **"Create Period"**

**Method 2: Use Suggested Template**

1. Scroll to "Suggested Protocols" section
2. Read template descriptions
3. Click **"Use This"** on desired template
4. Form auto-fills with template data
5. Modify if needed
6. Click **"Create Period"**

### 8 Built-In Templates

1. **Time-Restricted Eating (16:8)**
   - Eat within 8-hour window
   - Fast for 16 hours
   - Duration: 2-4 weeks

2. **Meal Timing Optimization**
   - Strategic meal scheduling
   - Larger breakfast, lighter dinner
   - Duration: 2-3 weeks

3. **Intermittent Fasting (5:2)**
   - Normal eating 5 days
   - 500-600 kcal on 2 days
   - Duration: 3-4 weeks

4. **Low-Carb Focus**
   - 50-100g carbs daily
   - Increase protein/fats
   - Duration: 3-4 weeks

5. **Calorie Cycling**
   - Alternate high/low calorie days
   - Prevents metabolic adaptation
   - Duration: 2-4 weeks

6. **Mindful Portion Control**
   - Reduce portions 20-30%
   - Eat slowly, mindfully
   - Duration: 3-4 weeks

7. **Food Elimination (Triggers)**
   - Remove sugar, processed foods
   - Identify sensitivities
   - Duration: 2-3 weeks

8. **Climate Friendly & Animal Protection**
   - Plant-based focus
   - Local, seasonal ingredients
   - Ethical and sustainable
   - Duration: 3-4 weeks

### Managing Active Periods

**View Period Details:**
1. Select period from list
2. Click **"View Details"**
3. See complete information including:
   - Period info (dates, duration)
   - Weight change data
   - All weight logs during period

**End a Period:**
1. Select active period
2. Click **"End Period"**
3. Confirm action
4. End date set to today
5. Period moves to "Completed" tab

**Double-Click Navigation:**
- Double-click any active period
- Opens Weight Logging dashboard
- Quick way to log weight during period

### Analyzing Effectiveness

**Period Summary includes:**
- Start and end dates
- Total duration (days)
- Start weight vs end weight
- Total weight change
- Average weekly change
- All weight logs during period

**Example:**
```
Period: Low Carb Trial
Duration: 21 days
Start Weight: 78.0 kg
End Weight: 75.5 kg
Change: -2.5 kg
Weekly Avg: -0.83 kg/week
```

---

## Daily Totals

### Food Totals (Button 3)

```
┌─────────────────────────────────┐
│ Daily Food Totals               │
├─────────────────────────────────┤
│ Date│Food       │Port│Kcal│Total│
│ ────┼───────────┼────┼────┼─────│
│2025-│Apple      │1.0 │52  │     │
│12-21│Banana     │2.0 │178 │     │
│     │Chicken    │1.5 │248 │ 478 │
│ ────┼───────────┼────┼────┼─────│
│2025-│Rice       │2.0 │260 │     │
│12-20│Egg        │1.0 │155 │ 415 │
└─────────────────────────────────┘

Summary:
Total Foods Logged: 45
Average Daily: 458 kcal
```

**Features:**
- Groups by date
- Shows daily totals
- Color codes today
- Export capability

### Activity Totals (Button 4)

```
┌─────────────────────────────────┐
│ Daily Activity Totals           │
├─────────────────────────────────┤
│ Date│Activity   │Min │Kcal│Total│
│ ────┼───────────┼────┼────┼─────│
│2025-│Running    │30  │300 │     │
│12-21│Walking    │45  │225 │ 525 │
│ ────┼───────────┼────┼────┼─────│
│2025-│Cycling    │60  │500 │ 500 │
│12-20│           │    │    │     │
└─────────────────────────────────┘

Summary:
Total Activities Logged: 23
Average Daily: 412 kcal burned
```

### Net Calorie Analysis

Manually calculate:
```
Net Calories = Food Calories - Activity Calories
Example: 478 kcal eaten - 525 kcal burned = -47 kcal (deficit)
```

---

## Tips & Tricks

### Workflow Optimization

**Daily Routine:**
1. Morning: Log weight (Button 5)
2. After meals: Log foods (Button 1)
3. After exercise: Log activities (Button 2)
4. Evening: Check totals (Buttons 3 & 4)

**Weekly Review:**
1. Open Weight Logging (Button 5)
2. Review weekly change
3. Analyze effectiveness
4. Adjust if needed

**Period Workflow:**
1. Start new protocol (Button 6)
2. Log weight regularly (Button 5)
3. After 2-4 weeks: End period (Button 6)
4. View results in period details
5. Decide to continue or try new protocol

### Keyboard Shortcuts

**While application running:**
- `Tab` - Navigate between fields
- `Enter` - Submit forms
- `Esc` - Close dialogs
- `Ctrl+C` - Close application (in terminal)

### Multi-Monitor Setup

**Optimal setup:**
1. Place Menu on primary screen
2. Click "Cascade" - windows follow menu
3. Drag menu to secondary display
4. Windows reposition automatically
5. Or use "Grid Layout" for automatic positioning

**Single Monitor:**
- Use "Cascade" mode
- Click button 5 & 6 to toggle window sizes
- Use "Hide/Show" to quickly clear desktop

### Data Entry Tips

**Food Logging:**
- Log immediately after eating
- Use consistent portion sizes
- Add notes for special meals
- Plan ahead with future dates

**Activity Logging:**
- Round to nearest 5 minutes
- Be consistent with intensity
- Include daily activities (walking, stairs)
- Track outdoor activities separately

**Weight Logging:**
- Weigh at same time daily
- Use same scale
- Record before breakfast
- Weekly consistency more important than daily

### Planning Features

**Meal Planning:**
- Log food for future dates (green highlight)
- Plan weekly menus
- Calculate expected calories

**Activity Planning:**
- Schedule workouts in advance
- Set weekly activity goals
- Track planned vs actual

---

## Troubleshooting

### Login Issues

**Problem:** Can't login with credentials

**Solutions:**
1. Check caps lock
2. Verify username is correct (case-sensitive)
3. Password minimum 4 characters
4. Register new user if forgotten

### Window Issues

**Problem:** Windows appear off-screen

**Solutions:**
1. Click "Hide/Show" twice to reset
2. Use "Grid Layout" for automatic positioning
3. Drag menu window on-screen first
4. Click "Cascade" to reposition relative to menu

**Problem:** Can't see all windows in Grid mode

**Solution:**
- Works best on displays 1920x1080 or larger
- Try "Cascade" mode for smaller screens
- Use toggle shrink/expand (buttons 5 & 6)

### Data Issues

**Problem:** Food/Activity not appearing in dropdown

**Solutions:**
1. Check if data imported:
   ```bash
   poetry run python src/scripts/import_foods.py
   ```
2. Add manually to database
3. Check database connection

**Problem:** Weight history not showing

**Solutions:**
1. Verify weight logs exist in database
2. Check date filter
3. Refresh by closing and reopening window

**Problem:** Period not appearing in weight logs

**Solutions:**
1. Verify period is active (not ended)
2. Check period dates overlap with weight log dates
3. Refresh weight dashboard

### Performance Issues

**Problem:** Application running slow

**Solutions:**
1. Close unused dashboard windows
2. Clear old log entries
3. Compact database:
   ```bash
   sqlite3 src/data/laihdutanyt.db "VACUUM;"
   ```

**Problem:** Changes not saving

**Solutions:**
1. Check database file permissions
2. Close all instances of app
3. Restart application
4. Reinitialize database if corrupted:
   ```bash
   poetry run invoke init-db
   ```

---

## Admin Features (Stub)

### Admin Login

1. Click "Admin Login" on login screen
2. Enter admin credentials (admin/admin)
3. Admin stub window opens
4. Shows planned features roadmap

### Planned Features

- User management dashboard
- Password reset tool
- Food/Activity database editors
- Client progress viewer
- System reports export
- Custom protocol templates
- Bulk user import

**Note:** Admin features are placeholders for future development. Current version operates in self-service mode where users manage their own data.

---

## Data Management

### Backup Your Data

```bash
# Copy database file
cp src/data/laihdutanyt.db src/data/laihdutanyt.db.backup

# With timestamp
cp src/data/laihdutanyt.db src/data/laihdutanyt_$(date +%Y%m%d).db
```

### Export Data

Currently manual export via SQL:
```bash
sqlite3 src/data/laihdutanyt.db
.mode csv
.output weight_logs.csv
SELECT * FROM weight_logs;
.quit
```

### Import Custom Data

Edit CSV files then run import scripts:
```bash
# Edit files
nano src/data/sample_foods.csv
nano src/data/sample_activities.csv

# Import
poetry run python src/scripts/import_foods.py
poetry run python src/scripts/import_activities.py
```

---

## Keyboard Reference

| Key | Action |
|-----|--------|
| Tab | Next field |
| Shift+Tab | Previous field |
| Enter | Submit form |
| Esc | Cancel/Close |
| Ctrl+C | Quit (terminal) |
| F1 | Help (future) |

---

## Screen Size Recommendations

**Optimal:**
- 1920x1080 or larger (Grid mode)
- Dual monitor setup
- 27" or 32" display

**Works well:**
- 1366x768 (Cascade mode)
- 15" laptop (Cascade + toggle)
- Single monitor

**Not recommended:**
- < 1280x720 resolution
- Very small displays (< 13")

---

## Getting Help

1. **Documentation:**
   - This file (user_instructions.md)
   - POETRY_INVOKE_WORKFLOW.md
   - UBUNTU_INSTALLATION.md

2. **Technical Issues:**
   - Check troubleshooting section
   - Review terminal errors
   - Restart application

3. **Feature Requests:**
   - Check dokumentaatio/NEW_FEATURES_v2.2.md
   - See architecture.md for planned features

---

**Version:** 2.2
**Release Date:** December 21, 2025
**Support:** See course forum or GitHub issues
**License:** Educational use (University of Helsinki course project)

---

**Enjoy tracking your weight loss journey!** 🎯📊💪
