# Ubuntu LTS Testing & Demo - Complete Guide

## 📋 Overview

This guide helps you verify that Laihdutanyt works properly on Ubuntu LTS (via VMware Horizon Client) and is ready for demonstration at the university.

---

## 📚 Documentation Created

### 1. **UBUNTU_DEMO_CHECKLIST.md** (Most Important!)
- **Purpose**: Complete testing checklist with 32 test cases
- **Use**: Step-by-step verification of all features
- **Includes**:
  - Installation tests
  - Functional tests (A-I sections)
  - Poetry/coverage testing
  - Performance testing
  - UI/UX testing
  - Data integrity tests
  - Demo preparation
  - Issue tracking template

### 2. **UBUNTU_DEMO_QUICK_REFERENCE.md**
- **Purpose**: Quick reference card for demo day
- **Use**: Keep open during demo for fast command lookup
- **Includes**:
  - Copy-paste ready commands
  - Demo flow (5-10 minutes)
  - Common issues & fixes
  - Emergency commands
  - Success criteria

### 3. **ubuntu_setup.sh**
- **Purpose**: Automated setup script
- **Use**: One-command installation and verification
- **Features**:
  - Checks Python 3.11 & Tkinter
  - Checks Poetry
  - Installs dependencies
  - Initializes database
  - Imports sample data
  - Runs tests (optional)
  - Generates coverage (optional)
  - Starts app (optional)

### 4. **UBUNTU_INSTALLATION.md** (Already exists)
- **Purpose**: Manual installation guide
- **Use**: Step-by-step installation if script fails

### 5. **POETRY_INVOKE_WORKFLOW.md** (Already exists)
- **Purpose**: Detailed Poetry and Invoke guide
- **Use**: Reference for Poetry commands

---

## 🚀 Quick Start on University Ubuntu

### Method 1: Automated (Recommended)
```bash
# 1. Connect via VMware Horizon Client to Ubuntu virtual desktop
# 2. Open terminal
# 3. Clone and run setup

cd ~
git clone <your-repo-url> ot-harjoitustyo
cd ot-harjoitustyo
chmod +x ubuntu_setup.sh
./ubuntu_setup.sh
```

**Time**: 5-10 minutes (mostly waiting for downloads)

---

### Method 2: Manual
```bash
cd ~
git clone <your-repo-url> ot-harjoitustyo
cd ot-harjoitustyo
poetry install
poetry run invoke init-db
poetry run python src/scripts/import_foods.py
poetry run python src/scripts/import_activities.py
poetry run invoke start
```

**Time**: 5-10 minutes

---

## ✅ What to Test

### Essential Tests (20 minutes):

1. **Installation** (5 min)
   - Clone repository
   - Run setup script
   - Verify all dependencies installed

2. **Basic Functionality** (5 min)
   - Register user
   - Login
   - 4 dashboards auto-open
   - Log food entry
   - Log activity entry
   - Log weight entry

3. **Window Management** (2 min)
   - Cascade layout
   - Dashboard Inputs mode
   - Hide/Show all

4. **Admin Panel** (3 min)
   - Admin login
   - Admin stub (80% screen)
   - All 8 features visible
   - Documentation clean header
   - Logout

5. **Coverage Testing** (5 min)
   - Run tests: `poetry run invoke test`
   - Generate coverage: `poetry run invoke coverage`
   - View report: `poetry run invoke coverage-report`

---

### Comprehensive Tests (1-2 hours):

Use **UBUNTU_DEMO_CHECKLIST.md** for full 32-test verification:
- All 16 functional tests (A-I)
- 4 Poetry tests (17-20)
- 2 performance tests (21-22)
- 3 UI/UX tests (23-25)
- 2 data integrity tests (26-27)
- 2 error handling tests (28-29)
- 2 documentation tests (30-31)
- 1 clean install test (32)

---

## 🎯 Coverage Testing with Poetry

### Commands:
```bash
# Run tests
poetry run invoke test

# Run with coverage
poetry run invoke coverage

# Show coverage in terminal
poetry run invoke coverage-report

# Open HTML report
poetry run invoke coverage
firefox htmlcov/index.html
```

### What Poetry Does:
- ✅ Manages virtual environment
- ✅ Installs exact package versions (from poetry.lock)
- ✅ Runs tests in isolated environment
- ✅ Generates coverage reports
- ✅ Executes Invoke tasks

### Expected Coverage:
- **Overall**: >80%
- **Services**: ~85-90%
- **Repositories**: ~80-85%
- **UI**: ~60-70%

---

## 🐛 Common Issues & Solutions

### Issue 1: Tkinter Not Found
```bash
sudo apt install python3.11-tk -y
```

### Issue 2: Poetry Not in PATH
```bash
export PATH="$HOME/.local/bin:$PATH"
source ~/.bashrc
```

### Issue 3: Display Not Set
```bash
export DISPLAY=:0
# Or for your specific display
echo $DISPLAY
```

### Issue 4: Database Locked
```bash
rm src/data/laihdutanyt.db
poetry run invoke init-db
```

### Issue 5: Dependencies Not Installing
```bash
# Remove virtual env and try again
poetry env remove python3.11
poetry install
```

---

## 📊 Demo Flow (5-10 minutes)

### Preparation (Before Demo):
1. Fresh Ubuntu session via Horizon Client
2. Run `./ubuntu_setup.sh`
3. Test complete workflow once
4. Note any issues
5. Have quick reference open

### During Demo:

**Minute 1**: Login & Auto-Open
- Show login window
- Register/login as user
- **Highlight**: 4 dashboards auto-open in grid

**Minute 2**: Food Logging
- Select food from dropdown
- **Highlight**: Clean names (no IDs!)
- Log entry

**Minute 3**: Activity Logging
- Show activity dropdown
- **Highlight**: All 5 activities visible!
- Log activity

**Minute 4**: Weight & Periods
- Log weight entry
- Create dietary period
- Show period templates

**Minute 5**: Window Management
- Demonstrate Cascade
- Demonstrate Dashboard Inputs
- Demonstrate Hide/Show

**Minute 6**: Daily Totals
- Open totals dashboard
- Show calorie calculations

**Minute 7-8**: Admin Panel
- Logout, login as admin
- Open admin stub
- **Highlight**: 80% screen height, all features visible
- View documentation
- **Highlight**: Clean header
- Logout

**Minute 9**: Coverage Testing
- Run: `poetry run invoke coverage`
- Show coverage report
- **Highlight**: >80% coverage

**Minute 10**: Q&A

---

## 🎓 University Network Specifics

### VMware Horizon Client:
- ✅ Provides Ubuntu virtual desktop
- ✅ GUI applications work properly
- ✅ X11 display configured
- ✅ Network access available

### What Works:
- ✅ Git clone from GitHub
- ✅ Poetry package installation
- ✅ Tkinter GUI applications
- ✅ File operations in home directory
- ✅ Terminal commands

### What to Check:
- [ ] Display variable set (echo $DISPLAY)
- [ ] Python 3.10+ available (3.10.x, 3.11.x, or 3.12.x)
- [ ] Internet access for Poetry
- [ ] Sufficient disk space (~500 MB)

---

## 📦 Pre-Demo Verification Checklist

### Before Demo Day:

**Week Before:**
- [ ] Test complete installation on university Ubuntu
- [ ] Verify all features work via Horizon Client
- [ ] Run coverage tests
- [ ] Note any issues
- [ ] Prepare workarounds

**Day Before:**
- [ ] Test connection to university network
- [ ] Verify Horizon Client access
- [ ] Clone repository to university system
- [ ] Run `./ubuntu_setup.sh`
- [ ] Complete full workflow test
- [ ] Generate coverage report

**Day of Demo:**
- [ ] Login to Horizon Client
- [ ] Navigate to project directory
- [ ] Run quick verification:
  ```bash
  cd ~/ot-harjoitustyo
  poetry run invoke test
  poetry run invoke start
  ```
- [ ] Have quick reference open
- [ ] Have credentials ready (admin/admin123)

---

## 🎬 Demo Success Criteria

### Installation ✅
- [ ] Setup completes in <10 minutes
- [ ] No errors during installation
- [ ] Database initializes correctly
- [ ] Sample data imports successfully

### Functionality ✅
- [ ] Login window appears
- [ ] 4 dashboards auto-open properly
- [ ] Can log entries in all dashboards
- [ ] Window management works
- [ ] Admin panel fully functional
- [ ] All 8 admin features visible

### Testing ✅
- [ ] Tests run successfully
- [ ] Coverage >80%
- [ ] Coverage report generates
- [ ] No critical test failures

### Performance ✅
- [ ] App starts in <3 seconds
- [ ] No lag or freezing
- [ ] Smooth window operations
- [ ] Database operations fast

### UI/UX ✅
- [ ] All text readable
- [ ] Fonts render correctly
- [ ] Emojis display properly
- [ ] Colors appropriate
- [ ] Windows positioned correctly

---

## 📞 Emergency Contacts

### If Something Goes Wrong:

1. **Don't panic** - Use quick reference
2. **Check common issues** - Most are documented
3. **Try emergency commands** - Nuclear reset if needed
4. **Use manual installation** - Fallback option
5. **Explain issue** - Be honest if demo hits bug

### Nuclear Reset:
```bash
cd ~/ot-harjoitustyo
rm -rf src/data/laihdutanyt.db
poetry env remove python3.11
rm -rf ~/.cache/pypoetry/
poetry install
poetry run invoke init-db
poetry run python src/scripts/import_foods.py
poetry run python src/scripts/import_activities.py
poetry run invoke start
```

---

## 📝 Post-Demo Notes

### After Demo, Document:
- [ ] What worked well
- [ ] What issues occurred
- [ ] Questions asked
- [ ] Feedback received
- [ ] Improvements needed

### Follow-Up Actions:
- [ ] Fix any bugs found
- [ ] Update documentation
- [ ] Add to changelog
- [ ] Consider feature requests

---

## 🎯 Key Points to Emphasize

### During Demo:

1. **Auto-Opening Dashboards**
   - "Notice how 4 input dashboards automatically open in a grid layout"

2. **Clean Dropdowns**
   - "Food and activity dropdowns show clean names, not database IDs"

3. **All Activities Visible**
   - "Fixed bug - now all 5 activities appear in dropdown"

4. **Admin Panel Height**
   - "Admin stub now uses 80% screen height so all features are visible"

5. **Logout Functionality**
   - "Can easily logout and switch between user/admin accounts"

6. **Coverage Testing**
   - "Poetry manages testing, coverage >80%"

7. **Ubuntu Compatibility**
   - "Works perfectly on Ubuntu LTS with Python 3.10+"

---

## 📚 Documentation Files Summary

| File | Purpose | When to Use |
|------|---------|-------------|
| UBUNTU_DEMO_CHECKLIST.md | Complete 32-test verification | Before demo (testing phase) |
| UBUNTU_DEMO_QUICK_REFERENCE.md | Quick commands & demo flow | During demo (reference) |
| ubuntu_setup.sh | Automated setup | First-time installation |
| UBUNTU_INSTALLATION.md | Manual installation | If script fails |
| POETRY_INVOKE_WORKFLOW.md | Poetry guide | Learning Poetry/Invoke |
| USER_INSTRUCTIONS_v2.2.md | End-user manual | For users |
| ADMIN_IMPROVEMENTS.md | Admin changes | Development reference |

---

## ✨ Final Checklist

### You Are Demo-Ready When:

- [x] All admin improvements complete
- [x] Ubuntu documentation complete
- [x] Setup script created
- [x] Testing checklist created
- [x] Quick reference created
- [ ] Tested on university Ubuntu
- [ ] Coverage >80%
- [ ] All features verified
- [ ] Demo script practiced
- [ ] Credentials ready

---

## 🎉 You're Almost There!

**Next Steps:**

1. **Connect to University Ubuntu** (via Horizon Client)
2. **Run setup script**: `./ubuntu_setup.sh`
3. **Complete testing**: Use UBUNTU_DEMO_CHECKLIST.md
4. **Practice demo**: Follow UBUNTU_DEMO_QUICK_REFERENCE.md
5. **Generate coverage**: `poetry run invoke coverage`
6. **Report back**: Any issues found?

---

## 📧 Need Help?

If you encounter issues during Ubuntu testing:

1. **Check documentation** first (UBUNTU_DEMO_QUICK_REFERENCE.md)
2. **Try common fixes** (documented in guide)
3. **Check terminal output** for error messages
4. **Try nuclear reset** if all else fails
5. **Document the issue** for future reference

---

**Remember**: The application is demo-ready on Windows. Ubuntu testing is to verify it works equally well on the university system!

Good luck with your testing! 🚀

---

**Created**: December 21, 2025  
**Version**: 1.0  
**Application Version**: 2.2.3  
**Status**: Ready for Ubuntu verification
