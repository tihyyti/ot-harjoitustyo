# Ubuntu LTS Installation Guide - Laihdutanyt

## Quick Setup for Ubuntu 20.04/22.04 LTS

This guide will help you install and run Laihdutanyt on a fresh Ubuntu LTS system.

---

## Prerequisites

- Ubuntu 20.04 LTS or 22.04 LTS (recommended)
- Internet connection
- Terminal access
- ~500 MB free disk space

---

## Step 1: System Update

```bash
sudo apt update
sudo apt upgrade -y
```

---

## Step 2: Install Python 3.11+

### For Ubuntu 22.04 (has Python 3.10):

```bash
# Add deadsnakes PPA for Python 3.11
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3.11-dev -y

# Verify installation
python3.11 --version
```

### For Ubuntu 20.04:

```bash
# Same steps as above
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev -y
```

---

## Step 3: Install Tkinter (Required for GUI)

```bash
# Install Tkinter for your Python version
# For Python 3.10:
sudo apt install python3.10-tk
# For Python 3.11:
sudo apt install python3.11-tk
# For Python 3.12:
sudo apt install python3.12-tk -y

# Verify Tkinter installation
python3.11 -m tkinter
# A small window should appear - close it
```

---

## Step 4: Install Poetry (Python Package Manager)

```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3.11 -

# Add Poetry to PATH
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc

# Verify Poetry installation
poetry --version
```

---

## Step 5: Install Git (if not already installed)

```bash
sudo apt install git -y
git --version
```

---

## Step 6: Clone the Repository

```bash
# Clone the project
cd ~
git clone https://github.com/<your-username>/ot-harjoitustyo.git
cd ot-harjoitustyo

# Or if you have the project as a ZIP file:
# unzip ot-harjoitustyo.zip
# cd ot-harjoitustyo
```

---

## Step 7: Configure Poetry to Use Python 3.11

```bash
# Tell Poetry to use Python 3.11
poetry env use python3.11

# Verify Python version
poetry run python --version
# Should show: Python 3.11.x
```

---

## Step 8: Install Project Dependencies

```bash
# Install all dependencies
poetry install

# This will:
# - Create a virtual environment
# - Install all packages from pyproject.toml
# - Set up the project for development
```

**Expected output:**
```
Installing dependencies from lock file...
Package operations: XX installs, 0 updates, 0 removals
  • Installing ...
  ...
Installing the current project: laihdutanyt (X.X.X)
```

---

## Step 9: Initialize the Database

```bash
# Create the SQLite database with tables
poetry run invoke init-db
```

**Expected output:**
```
🗄️  Initializing database...
✅ Database initialized!
```

This creates `src/data/laihdutanyt.db` with all necessary tables.

---

## Step 10: (Optional) Import Sample Data

```bash
# Import sample foods
poetry run python src/scripts/import_foods.py

# Import sample activities
poetry run python src/scripts/import_activities.py
```

---

## Step 11: Run the Application

```bash
# Start the application
poetry run invoke start
```

**Alternative:**
```bash
poetry run python src/main.py
```

---

## First-Time User Setup

1. **Login Window** will appear
2. Click **"Register New User"**
3. Fill in:
   - Username* (required)
   - Password* (required, min 4 characters)
   - Optional: Weight, Height, Age, Activity Level, etc.
4. Click **"Create User"**
5. Return to login and enter your credentials
6. Click **"User Login"**

---

## Troubleshooting

### Issue: "tkinter module not found"
```bash
sudo apt install python3.11-tk -y
```

### Issue: "poetry: command not found"
```bash
export PATH="$HOME/.local/bin:$PATH"
source ~/.bashrc
```

### Issue: "No module named 'invoke'"
```bash
poetry install  # Reinstall dependencies
```

### Issue: "Permission denied" on database
```bash
chmod 755 src/data
chmod 644 src/data/*.db
```

### Issue: Window doesn't appear
```bash
# Check if display is set
echo $DISPLAY
# Should show something like :0 or :1

# If empty, set it:
export DISPLAY=:0
```

### Issue: Font rendering issues
```bash
# Install Microsoft fonts (optional, for better Arial rendering)
sudo apt install ttf-mscorefonts-installer -y
```

### Issue: "Database is locked"
```bash
# Close all instances of the app, then:
rm src/data/laihdutanyt.db
poetry run invoke init-db
```

---

## System Requirements

**Minimum:**
- CPU: 1 GHz dual-core
- RAM: 2 GB
- Disk: 500 MB free space
- Display: 1366x768

**Recommended:**
- CPU: 2 GHz dual-core or better
- RAM: 4 GB or more
- Disk: 1 GB free space
- Display: 1920x1080 (for dual-window layout)

---

## Supported Ubuntu Versions

✅ **Tested on:**
- Ubuntu 22.04 LTS (Jammy Jellyfish)
- Ubuntu 20.04 LTS (Focal Fossa)

⚠️ **Should work on:**
- Ubuntu 23.10 (Mantic Minotaur)
- Ubuntu 24.04 LTS (Noble Numbat) - when released

❌ **Not supported:**
- Ubuntu 18.04 LTS (Python 3.11 installation more complex)

---

## Quick Command Reference

```bash
# Start application
poetry run invoke start

# Run tests
poetry run invoke test

# Run tests with coverage
poetry run invoke coverage

# Check code quality
poetry run invoke lint

# Initialize database
poetry run invoke init-db

# See all available commands
poetry run invoke --list

# Get help for specific command
poetry run invoke --help start
```

---

## Uninstallation

```bash
# Remove the project directory
cd ~
rm -rf ot-harjoitustyo

# Remove Poetry (optional)
curl -sSL https://install.python-poetry.org | python3.11 - --uninstall

# Remove Python 3.10/3.11/3.12 (optional, if you don't need it)
# Be careful not to remove the system Python!
sudo apt remove python3.10  # or python3.11 or python3.12 python3.11-tk -y
sudo apt autoremove -y
```

---

## Next Steps

1. Read `dokumentaatio/user_instructions.md` for feature guide
2. Check `dokumentaatio/POETRY_INVOKE_GUIDE.md` for workflow
3. Try the demo admin login (admin/admin) to see stub features
4. Explore dietary period templates
5. Import your own food/activity data

---

## Getting Help

- **User Guide:** `dokumentaatio/user_instructions.md`
- **Architecture:** `dokumentaatio/architecture.md`
- **Changelog:** `dokumentaatio/changelog.md`
- **Issues:** Check GitHub issues or course forum

---

## Development Setup (For Contributors)

```bash
# Install with dev dependencies
poetry install --with dev

# Run tests
poetry run pytest

# Run linter
poetry run pylint src/

# Generate coverage report
poetry run pytest --cov=src --cov-report=html

# Format code (if black is installed)
poetry run black src/
```

---

**Installation Time:** ~10-15 minutes
**First Launch:** Instant (after setup)
**Difficulty:** ⭐⭐☆☆☆ (Beginner-friendly)

---

**Last Updated:** December 21, 2025
**Version:** 2.2
**Ubuntu Support:** 20.04 LTS, 22.04 LTS
