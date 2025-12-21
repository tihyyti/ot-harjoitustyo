# Ubuntu LTS Demo Verification Checklist

## Test Environment
- **Platform**: Ubuntu LTS via VMware Horizon Client
- **Network**: University network
- **Access**: Virtual Desktop
- **Date**: December 21, 2025

---

## Pre-Demo Checklist

### 1. System Information
```bash
# Check Ubuntu version
lsb_release -a

# Check Python version
python3.11 --version

# Check Poetry version
poetry --version

# Check Git version
git --version

# Check display settings
echo $DISPLAY
```

**Expected:**
- Ubuntu 20.04 or 22.04 LTS
- Python 3.10+ (tested: 3.10.x, 3.11.x, 3.12.3)
- Poetry 1.7.0+
- Git 2.x
- DISPLAY should show :0 or :1

---

## Installation Test (First Time Setup)

### Step 1: Clone Repository
```bash
cd ~
git clone <your-repo-url> ot-harjoitustyo
cd ot-harjoitustyo
```

**Time Expected**: 1-2 minutes  
**Success Criteria**: `pyproject.toml` exists in directory

---

### Step 2: Configure Poetry Environment
```bash
# Set Python version
poetry env use python3.11

# Verify
poetry run python --version
```

**Time Expected**: 10-20 seconds  
**Success Criteria**: Shows "Python 3.10.x" or newer (3.11.x, 3.12.x)

---

### Step 3: Install Dependencies
```bash
poetry install
```

**Time Expected**: 2-5 minutes  
**Success Criteria**: 
- No errors
- Message: "Installing the current project: laihdutanyt"
- Virtual environment created in `~/.cache/pypoetry/virtualenvs/`

---

### Step 4: Initialize Database
```bash
poetry run invoke init-db
```

**Time Expected**: < 5 seconds  
**Success Criteria**: 
- ✅ Database initialized!
- File exists: `src/data/laihdutanyt.db`

---

### Step 5: Import Sample Data
```bash
# Import foods (52 items)
poetry run python src/scripts/import_foods.py

# Import activities (5 items)
poetry run python src/scripts/import_activities.py
```

**Time Expected**: < 5 seconds each  
**Success Criteria**: 
- Foods: "Imported 52 foods"
- Activities: "Imported 5 activities"

---

### Step 6: Launch Application
```bash
poetry run invoke start
```

**Time Expected**: 2-3 seconds  
**Success Criteria**: 
- Login window appears
- Window size: ~420x750 pixels
- Positioned at left edge of screen
- No error messages in terminal

---

## Functional Testing Checklist

### A. User Registration & Login

#### Test 1: Register New User
- [ ] Click "Register New User"
- [ ] Window opens (400x550)
- [ ] Enter username: `testuser`
- [ ] Enter password: `test123`
- [ ] Enter weight: `75.0`
- [ ] Enter height: `175`
- [ ] Enter age: `30`
- [ ] Click "Create User"
- [ ] Success message appears
- [ ] Window closes

**Time**: 1 minute  
**Notes**: ___________________

#### Test 2: User Login
- [ ] Enter username: `testuser`
- [ ] Enter password: `test123`
- [ ] Click "User Login"
- [ ] Main menu appears (420x750)
- [ ] Username shown in title

**Time**: 10 seconds  
**Notes**: ___________________

---

### B. Dashboard Inputs Mode (Auto-Open)

#### Test 3: Auto-Open Input Dashboards
After login, 4 windows should auto-open:

- [ ] Food Dashboard (window 1)
- [ ] Activity Dashboard (window 2)
- [ ] Weight Dashboard (window 5)
- [ ] Dietary Periods Dashboard (window 6)

**Windows arranged in grid:**
- Top-left: Food Dashboard
- Top-right: Activity Dashboard
- Bottom-left: Weight Dashboard
- Bottom-right: Dietary Periods Dashboard

**Time**: Immediate (within 0.3 seconds)  
**Notes**: ___________________

---

### C. Food Dashboard Testing

#### Test 4: Log Food Entry
- [ ] Food Dashboard visible
- [ ] Food dropdown shows clean names (no IDs)
- [ ] Select "Apple"
- [ ] Portion: 100g (default)
- [ ] Date: Today's date (default)
- [ ] Click "Add Food"
- [ ] Entry appears in "Today's Food Log"

**Time**: 20 seconds  
**Notes**: ___________________

#### Test 5: View All Food Logs
- [ ] Click "View All Food Logs"
- [ ] New window opens
- [ ] Shows logged entries with calories
- [ ] Can see date, food name, portion, calories

**Time**: 10 seconds  
**Notes**: ___________________

---

### D. Activity Dashboard Testing

#### Test 6: Log Activity Entry
- [ ] Activity Dashboard visible
- [ ] Activity dropdown shows all 5 activities:
  - Cycling
  - Running
  - Swimming
  - Walking
  - Yoga
- [ ] Select "Walking"
- [ ] Duration: 30 minutes (default)
- [ ] Date: Today's date (default)
- [ ] Click "Log Activity"
- [ ] Entry appears in activity log

**Time**: 20 seconds  
**Notes**: ___________________

---

### E. Weight Dashboard Testing

#### Test 7: Log Weight Entry
- [ ] Weight Dashboard visible
- [ ] Weight field: Enter 75.0
- [ ] Date: Today's date (default)
- [ ] Notes: "Initial weight" (optional)
- [ ] Click "Log Weight"
- [ ] Success message appears
- [ ] Entry appears in weight history table

**Time**: 20 seconds  
**Notes**: ___________________

---

### F. Dietary Periods Dashboard Testing

#### Test 8: Create Dietary Period
- [ ] Dietary Periods Dashboard visible
- [ ] Protocol dropdown shows templates
- [ ] Select a protocol (e.g., "Intermittent Fasting 16:8")
- [ ] Start date: Today
- [ ] End date: 7 days from now
- [ ] Click "Create Period"
- [ ] Success message appears
- [ ] Period appears in active periods list

**Time**: 30 seconds  
**Notes**: ___________________

---

### G. Window Management Testing

#### Test 9: Cascade Layout
- [ ] Click "Cascade" button in main menu
- [ ] All 8 windows cascade diagonally
- [ ] Each window offset by 30 pixels
- [ ] All windows visible

**Time**: 5 seconds  
**Notes**: ___________________

#### Test 10: Dashboard Inputs Mode
- [ ] Click "Dashboard Inputs" button
- [ ] Only 4 input dashboards open
- [ ] Arranged in grid layout
- [ ] Other windows close if open

**Time**: 5 seconds  
**Notes**: ___________________

#### Test 11: Hide/Show All
- [ ] Click "👁 Hide All" button
- [ ] All dashboard windows minimize
- [ ] Button changes to "👁 Show All"
- [ ] Click again
- [ ] All windows restore

**Time**: 5 seconds  
**Notes**: ___________________

---

### H. Totals Dashboard Testing

#### Test 12: View Daily Totals
- [ ] Click "Daily Totals" button in main menu
- [ ] Totals window opens
- [ ] Shows food totals for today
- [ ] Shows activity totals for today
- [ ] Displays calorie balance

**Time**: 10 seconds  
**Notes**: ___________________

---

### I. Admin Panel Testing

#### Test 13: Admin Login
- [ ] Logout from user account
- [ ] Username: `admin`
- [ ] Password: `admin123`
- [ ] Click "Admin Login"
- [ ] Admin menu appears (500x420)

**Time**: 15 seconds  
**Notes**: ___________________

#### Test 14: Admin Stub Window
- [ ] Click "📋 View Admin Features Roadmap"
- [ ] Admin stub window opens
- [ ] Window height: ~80% of screen
- [ ] All 8 planned features visible in table:
  1. User Management Dashboard
  2. Password Reset Tool
  3. Food Database Editor
  4. Activity Database Editor
  5. Client Progress Viewer
  6. System Reports Export
  7. Custom Protocol Templates
  8. Bulk User Import
- [ ] No scrolling needed to see all features

**Time**: 10 seconds  
**Notes**: ___________________

#### Test 15: Admin Documentation
- [ ] Click "📖 View Documentation"
- [ ] Documentation window opens (700x600)
- [ ] Header shows clean line: "ADMIN FEATURE ROADMAP"
- [ ] Shows 4 phases of planned features
- [ ] No weird character repetition

**Time**: 10 seconds  
**Notes**: ___________________

#### Test 16: Admin Logout
- [ ] Close admin stub window
- [ ] Click "🚪 Logout / Back to Login"
- [ ] Returns to login window
- [ ] Can log in as user again

**Time**: 10 seconds  
**Notes**: ___________________

---

## Poetry Testing (Coverage & Commands)

### Test 17: Run Tests
```bash
poetry run invoke test
```

**Expected:**
- All tests pass
- Shows test summary
- No failures

**Time**: 10-30 seconds  
**Notes**: ___________________

---

### Test 18: Coverage Report
```bash
poetry run invoke coverage
```

**Expected:**
- Tests run with coverage tracking
- Coverage report generated
- HTML report in `htmlcov/`
- Can open `htmlcov/index.html` in browser

**Time**: 10-30 seconds  
**Coverage %**: ___________  
**Notes**: ___________________

---

### Test 19: Coverage Report (Terminal)
```bash
poetry run invoke coverage-report
```

**Expected:**
- Shows coverage table in terminal
- Lists all source files
- Shows line coverage percentages

**Time**: 10-30 seconds  
**Notes**: ___________________

---

### Test 20: List All Tasks
```bash
poetry run invoke --list
```

**Expected output:**
```
Available tasks:

  coverage          Run tests with coverage
  coverage-report   Generate and display coverage report
  format            Format code with autopep8
  init-db           Initialize database
  lint              Run pylint
  start             Start the application
  test              Run tests
```

**Time**: < 1 second  
**Notes**: ___________________

---

## Performance Testing

### Test 21: Startup Time
```bash
time poetry run invoke start
```

**Expected:**
- Application starts in < 3 seconds
- Login window appears quickly

**Actual Time**: ___________  
**Notes**: ___________________

---

### Test 22: Database Performance
- [ ] Log 10 food entries quickly
- [ ] Log 10 activity entries
- [ ] Log 10 weight entries
- [ ] All operations complete quickly (< 1 second each)
- [ ] No lag or freezing

**Time**: 2-3 minutes total  
**Notes**: ___________________

---

## UI/UX Testing

### Test 23: Font Rendering
- [ ] All text readable
- [ ] Arial font renders correctly
- [ ] Emojis display (📊, 🏋️, 🚪, etc.)
- [ ] No character encoding issues

**Notes**: ___________________

---

### Test 24: Window Positioning
- [ ] Main menu at left edge (+10, +50)
- [ ] Dashboards positioned correctly
- [ ] No windows off-screen
- [ ] Grid layout organized properly

**Notes**: ___________________

---

### Test 25: Color Scheme
- [ ] Headers: Light blue backgrounds
- [ ] Buttons: Appropriate colors (blue, red, orange)
- [ ] Text: Dark on light backgrounds
- [ ] Good contrast throughout

**Notes**: ___________________

---

## Data Integrity Testing

### Test 26: Data Persistence
- [ ] Close application
- [ ] Relaunch: `poetry run invoke start`
- [ ] Login with same user
- [ ] All previous entries still visible
- [ ] No data loss

**Time**: 1 minute  
**Notes**: ___________________

---

### Test 27: Multi-User Support
- [ ] Logout
- [ ] Register second user: `testuser2`
- [ ] Login as `testuser2`
- [ ] Log some entries
- [ ] Logout and login as `testuser`
- [ ] Original user's data intact
- [ ] Second user's data separate

**Time**: 3 minutes  
**Notes**: ___________________

---

## Error Handling Testing

### Test 28: Invalid Login
- [ ] Enter wrong username
- [ ] Error message appears
- [ ] Enter wrong password
- [ ] Error message appears
- [ ] Can retry login

**Time**: 30 seconds  
**Notes**: ___________________

---

### Test 29: Invalid Registration
- [ ] Try to register with existing username
- [ ] Error message appears
- [ ] Try password < 4 characters
- [ ] Error message appears
- [ ] Try invalid weight (negative)
- [ ] Error message appears

**Time**: 1 minute  
**Notes**: ___________________

---

## Documentation Verification

### Test 30: README Accuracy
- [ ] `README.md` installation steps work
- [ ] All commands execute correctly
- [ ] Links functional (if any)
- [ ] Screenshots up-to-date (if any)

**Time**: 5 minutes  
**Notes**: ___________________

---

### Test 31: User Instructions
- [ ] Check `dokumentaatio/user_instructions.md`
- [ ] All features documented
- [ ] Instructions clear and accurate
- [ ] No outdated information

**Time**: 5 minutes  
**Notes**: ___________________

---

## Clean Uninstall Test (Optional)

### Test 32: Remove and Reinstall
```bash
# Remove virtual environment
poetry env remove python3.11

# Remove dependencies cache
rm -rf ~/.cache/pypoetry/

# Reinstall fresh
poetry install
poetry run invoke init-db
poetry run invoke start
```

**Expected:**
- Clean reinstall works
- No leftover issues
- App runs normally

**Time**: 5 minutes  
**Notes**: ___________________

---

## Demo Preparation Checklist

### Before Demo:
- [ ] Fresh Ubuntu session
- [ ] All updates installed
- [ ] Python 3.10+ installed (3.10.x, 3.11.x, or 3.12.x)
- [ ] Poetry installed
- [ ] Project cloned
- [ ] Dependencies installed
- [ ] Database initialized
- [ ] Sample data imported
- [ ] Test user created
- [ ] Tested full workflow once

---

## Demo Script (5-10 minutes)

### 1. Login & Auto-Open (1 minute)
- Show login window
- Login as demo user
- 4 dashboards auto-open in grid

### 2. Food Logging (1 minute)
- Log a food entry
- Show dropdown with clean names
- Show today's log

### 3. Activity Logging (1 minute)
- Log walking activity
- Show all 5 activities in dropdown

### 4. Weight Tracking (1 minute)
- Log weight entry
- Show weight history with periods

### 5. Dietary Periods (1 minute)
- Create new period
- Show protocol templates

### 6. Window Management (1 minute)
- Show Cascade layout
- Show Dashboard Inputs mode
- Show Hide/Show All

### 7. Daily Totals (1 minute)
- Open totals dashboard
- Show calorie calculations

### 8. Admin Panel (2 minutes)
- Logout and login as admin
- Show admin menu
- Open admin stub (80% screen height)
- Show 8 planned features
- View documentation
- Logout back to login

### 9. Q&A (remaining time)

---

## Issue Tracking

### Issues Found:
1. Issue: ___________________  
   Severity: [ ] Critical [ ] Major [ ] Minor  
   Workaround: ___________________

2. Issue: ___________________  
   Severity: [ ] Critical [ ] Major [ ] Minor  
   Workaround: ___________________

3. Issue: ___________________  
   Severity: [ ] Critical [ ] Major [ ] Minor  
   Workaround: ___________________

---

## Sign-Off

**Tester**: ___________________  
**Date**: ___________________  
**Ubuntu Version**: ___________________  
**Python Version**: ___________________  
**Poetry Version**: ___________________  

**Overall Assessment**:
- [ ] Ready for demo
- [ ] Minor issues (acceptable)
- [ ] Major issues (needs fixes)

**Notes**: ___________________
___________________
___________________

---

## Quick Command Reference

```bash
# Install everything
poetry install

# Initialize database
poetry run invoke init-db

# Start application
poetry run invoke start

# Run tests
poetry run invoke test

# Coverage report
poetry run invoke coverage

# Check tasks
poetry run invoke --list

# Format code
poetry run invoke format

# Run linter
poetry run invoke lint
```

---

## Emergency Fixes

### If Tkinter doesn't work:
```bash
sudo apt install python3.11-tk -y
```

### If Poetry not in PATH:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### If database locked:
```bash
rm src/data/laihdutanyt.db
poetry run invoke init-db
```

### If display issues:
```bash
export DISPLAY=:0
```

---

**Last Updated**: December 21, 2025  
**Document Version**: 1.0  
**Application Version**: 2.2.3
