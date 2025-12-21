# Laihdutanyt v2.1.0 - Quick Start Guide

**Last Updated:** 2025-12-20  
**For:** Fresh setup or migration to v2.1.0

## DO THIS FIRST (Total: ~10 minutes)

### STEP 1: Install Poetry 

**Poetry is NOT currently installed on your system.**

# Method 1: Official installer (RECOMMENDED)  
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

# Verify it works:
poetry --version
# Should show: Poetry (version 2.2.1)


###   STEP 2: Install Project Dependencies 

# Navigate to project root:

# Install all dependencies from poetry.lock:
poetry install

# Wait for completion (installs pytest, pylint, invoke, etc.)

**Expected output:** "Installing the current project: laihdutanyt (2.1.0)"


###   STEP 3: Run Database Migration 

**IMPORTANT: This adds new tables/columns for v2.1 statistics features**

# Run migration script:
poetry run python src/migrations/migrate_to_v2_1.py

# You should see:
#  weightlog table created
#  Column total_kcal_burned added
#  Database is ready for v2.1!

  **Safe to run multiple times** - Script checks what's already done


###   STEP 4: Start Application 

# Launch the app:
poetry run python src/main.py

# OR using invoke task (if configured):
poetry run invoke start
  - Login window should appear


## Quick Command Reference

Once setup is complete, use these commands:

# Start application
poetry run python src/main.py
poetry run invoke start

# Run tests
poetry run invoke test
poetry run pytest -v

# Test with coverage
poetry run invoke coverage
poetry run pytest --cov=src tests/

# Lint code
poetry run invoke lint

# List all available tasks
poetry run invoke --list

# Clean cache files
poetry run invoke clean


## Checklist:

- [x ] `poetry --version` works (shows version 2.x.x)
- [x] `poetry install` completed successfully
- [x] Migration ran (shows "Database is ready for v2.1!")
- [x] Application launches (`poetry run python src/main.py`)
- [x] You can login/register in the app


## Full Documentation

For complete details, see:

| Guide | Purpose |
|-------|---------|
| **SETUP_GUIDE.md** | Complete setup with troubleshooting |
| **dokumentaatio/POETRY_INVOKE_GUIDE.md**   | Poetry and Invoke details |
| **dokumentaatio/MVP_RELEASE_PLAN_v2.1.md** | Implementation roadmap |
| **dokumentaatio/NAMING_CONVENTIONS.md**    | Project standards |


## Next Steps After Setup

### Optional: Generate Demo Data

# Create 30 days of sample data:
poetry run python src/scripts/generate_demo_data.py


### Start Development

Follow the implementation plan:
- Read `dokumentaatio/MVP_RELEASE_PLAN_v2.1.md`
- Read `dokumentaatio/statistics_requirements_v3.md`

---

**Guide Version:** 2.1.0  
**Status:** Ready to Execute  
**Tested On:** Python 3.11.9
