# Ubuntu Demo - Quick Reference Card

## 🚀 Quick Start (Copy-Paste Ready)

### One-Time Setup
```bash
# 1. Clone project
cd ~
git clone <your-repo-url> ot-harjoitustyo
cd ot-harjoitustyo

# 2. Make setup script executable and run
chmod +x ubuntu_setup.sh
./ubuntu_setup.sh
```

The setup script will:
- ✅ Check Python 3.10+ & Tkinter
- ✅ Check Poetry
- ✅ Install dependencies
- ✅ Initialize database
- ✅ Import sample data
- ✅ Run tests (optional)
- ✅ Generate coverage (optional)

---

## 📝 Manual Setup (Step-by-Step)

```bash
# Install dependencies
poetry install

# Initialize database
poetry run invoke init-db

# Import sample data
poetry run python src/scripts/import_foods.py
poetry run python src/scripts/import_activities.py

# Start application
poetry run invoke start
```

---

## 🧪 Testing Commands

```bash
# Run all tests
poetry run invoke test

# Run with coverage
poetry run invoke coverage

# Show coverage report in terminal
poetry run invoke coverage-report

# Open HTML coverage report
poetry run invoke coverage
firefox htmlcov/index.html  # or xdg-open htmlcov/index.html
```

---

## 🎯 Demo Flow (5-10 minutes)

### 1. Start Application (10 sec)
```bash
poetry run invoke start
```
**Expect**: Login window at left edge (420x750)

---

### 2. Register Demo User (30 sec)
- Click "Register New User"
- Username: `demouser`
- Password: `demo123`
- Weight: 75.0 kg
- Height: 175 cm
- Age: 30
- Click "Create User"

---

### 3. Login & Auto-Open (20 sec)
- Username: `demouser`
- Password: `demo123`
- Click "User Login"
- **4 dashboards auto-open in grid**:
  - Top-left: Food Dashboard
  - Top-right: Activity Dashboard
  - Bottom-left: Weight Dashboard
  - Bottom-right: Dietary Periods Dashboard

---

### 4. Log Food Entry (30 sec)
**In Food Dashboard:**
- Food dropdown: "Apple" (no ID shown!)
- Portion: 100g
- Date: Today
- Click "Add Food"
- **Entry appears in today's log**

---

### 5. Log Activity (30 sec)
**In Activity Dashboard:**
- Activity dropdown: "Walking" (all 5 visible!)
- Duration: 30 min
- Date: Today
- Click "Log Activity"
- **Entry appears in activity log**

---

### 6. Log Weight (30 sec)
**In Weight Dashboard:**
- Weight: 75.0 kg
- Date: Today
- Notes: "Starting weight"
- Click "Log Weight"
- **Entry appears in weight history**

---

### 7. Create Dietary Period (30 sec)
**In Dietary Periods Dashboard:**
- Protocol: "Intermittent Fasting 16:8"
- Start date: Today
- End date: 7 days from today
- Click "Create Period"
- **Period appears in active periods**

---

### 8. Window Management (30 sec)
**In Main Menu:**
- Click "Cascade" → All windows cascade
- Click "Dashboard Inputs" → Back to grid
- Click "👁 Hide All" → All minimize
- Click "👁 Show All" → All restore

---

### 9. Daily Totals (30 sec)
- Click "Daily Totals" in main menu
- **Shows**:
  - Food totals (calories, carbs, protein, fat)
  - Activity totals (calories burned)
  - Net calorie balance

---

### 10. Admin Panel (1 minute)
- Click "Logout"
- Username: `admin`
- Password: `admin123`
- Click "Admin Login"
- **Admin menu appears (500x420)**
- Click "📋 View Admin Features Roadmap"
- **Admin stub opens (80% screen height)**
- **All 8 features visible** (no scrolling!)
- Click "📖 View Documentation"
- **Clean header** (no weird repetition)
- Close windows
- Click "🚪 Logout / Back to Login"

---

## 🔑 Demo Credentials

| Account | Username | Password |
|---------|----------|----------|
| Demo User | demouser | demo123 |
| Admin | admin | admin123 |

---

## 🐛 Common Issues & Fixes

### Issue: Tkinter not found
```bash
sudo apt install python3.11-tk -y
```

### Issue: Poetry not in PATH
```bash
export PATH="$HOME/.local/bin:$PATH"
source ~/.bashrc
```

### Issue: Display not set
```bash
export DISPLAY=:0
```

### Issue: Database locked
```bash
rm src/data/laihdutanyt.db
poetry run invoke init-db
```

### Issue: Window doesn't appear
```bash
# Check X11 forwarding (if using SSH)
echo $DISPLAY
# Should show :0 or :1

# Restart X server if needed
sudo systemctl restart gdm3  # or lightdm/sddm
```

---

## 📊 Coverage Testing

### Generate Coverage Report
```bash
# Run tests with coverage
poetry run invoke coverage

# View in terminal
poetry run invoke coverage-report

# Open HTML report
firefox htmlcov/index.html
```

### Expected Coverage
- **Target**: >80%
- **Core modules**:
  - `services/`: ~85-90%
  - `repositories/`: ~80-85%
  - `ui/`: ~60-70% (UI code harder to test)

---

## 🎭 Demo Tips

### Before Demo:
1. ✅ Fresh Ubuntu session
2. ✅ Run `./ubuntu_setup.sh`
3. ✅ Test full workflow once
4. ✅ Close all extra windows
5. ✅ Increase font size if needed

### During Demo:
1. 🗣️ Explain auto-opening dashboards
2. 🗣️ Point out clean dropdowns (no IDs)
3. 🗣️ Show all 5 activities in dropdown
4. 🗣️ Highlight admin stub (80% screen)
5. 🗣️ Demonstrate logout/login flow
6. 🗣️ Show coverage report

### Demo Script:
- **5 min**: Basic workflow (register, login, log entries)
- **2 min**: Window management & totals
- **2 min**: Admin panel & features
- **1 min**: Coverage testing
- **Q&A**: Remaining time

---

## 📦 Package Versions

| Package | Version | Purpose |
|---------|---------|---------|
| Python | 3.10+ | Runtime (tested: 3.9.13, 3.10.x, 3.11.x, 3.12.3) |
| Poetry | 1.7.0+ | Package manager |
| Tkinter | Built-in | GUI framework |
| Invoke | 2.0+ | Task runner |
| Pytest | Latest | Testing |
| Coverage | Latest | Code coverage |

---

## 🔧 Available Invoke Tasks

```bash
poetry run invoke --list
```

**Output:**
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

---

## 📂 Project Structure

```
ot-harjoitustyo/
├── src/
│   ├── main.py              # Application entry point
│   ├── create_db.py         # Database schema
│   ├── data/
│   │   └── laihdutanyt.db   # SQLite database
│   ├── services/            # Business logic
│   ├── repositories/        # Data access
│   ├── ui/
│   │   ├── app.py          # Main window
│   │   └── views/          # Dashboard windows
│   └── scripts/            # Import scripts
├── tests/                  # Test files
├── dokumentaatio/          # Documentation
├── pyproject.toml          # Poetry config
├── tasks.py                # Invoke tasks
└── ubuntu_setup.sh         # Quick setup script
```

---

## 🎓 University Network Notes

### VMware Horizon Client:
- ✅ Works with Ubuntu virtual desktop
- ✅ GUI applications display correctly
- ✅ Copy-paste may be limited
- ✅ File transfer via shared folders or git

### Network Considerations:
- ✅ Poetry installs packages from PyPI
- ✅ Requires internet connection for initial setup
- ✅ After setup, runs offline
- ✅ Git clone works within university network

---

## ✅ Pre-Demo Verification

```bash
# Quick system check
python3.11 --version  # Should be 3.11.x
poetry --version      # Should be 1.7.0+
echo $DISPLAY         # Should show :0 or :1

# Quick app test
cd ~/ot-harjoitustyo
poetry run invoke start

# Quick test run
poetry run invoke test

# Quick coverage check
poetry run invoke coverage-report
```

---

## 📞 Emergency Commands

### If something breaks:
```bash
# Nuclear option: Fresh start
cd ~/ot-harjoitustyo
rm -rf src/data/laihdutanyt.db
poetry env remove python3.11
poetry install
poetry run invoke init-db
poetry run python src/scripts/import_foods.py
poetry run python src/scripts/import_activities.py
poetry run invoke start
```

### If Poetry breaks:
```bash
# Remove and reinstall Poetry
curl -sSL https://install.python-poetry.org | python3.11 - --uninstall
curl -sSL https://install.python-poetry.org | python3.11 -
export PATH="$HOME/.local/bin:$PATH"
```

---

## 🎉 Success Criteria

### Installation ✅
- [ ] Python 3.10+ installed (3.10.x, 3.11.x, or 3.12.x)
- [ ] Poetry working
- [ ] Dependencies installed
- [ ] Database initialized
- [ ] Sample data imported

### Functionality ✅
- [ ] Login window appears
- [ ] 4 dashboards auto-open
- [ ] Can log food/activity/weight
- [ ] Can create dietary period
- [ ] Window management works
- [ ] Admin panel functional
- [ ] All 8 admin features visible

### Testing ✅
- [ ] Tests pass
- [ ] Coverage >80%
- [ ] No critical errors

### Demo Ready ✅
- [ ] Full workflow tested
- [ ] Demo user created
- [ ] Admin login works
- [ ] All features accessible

---

**Last Updated**: December 21, 2025  
**Document Version**: 1.0  
**Application Version**: 2.2.3

---

## 🚀 One-Command Start

After setup is complete:
```bash
cd ~/ot-harjoitustyo && poetry run invoke start
```

Good luck with your demo! 🎯
