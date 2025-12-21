# Poetry & Invoke Workflow Guide

## Complete Guide to Development Workflow with Poetry and Invoke

This guide explains all available commands and recommended workflows for developing and using Laihdutanyt.

---

## Table of Contents

1. [Poetry Basics](#poetry-basics)
2. [Invoke Tasks](#invoke-tasks)
3. [Daily Workflows](#daily-workflows)
4. [Development Workflow](#development-workflow)
5. [Testing Workflow](#testing-workflow)
6. [Troubleshooting](#troubleshooting)

---

## Poetry Basics

### What is Poetry?

Poetry is a modern Python dependency manager that:
- Manages virtual environments automatically
- Handles dependencies declared in `pyproject.toml`
- Ensures reproducible builds with `poetry.lock`
- Simplifies package installation

### Essential Poetry Commands

```bash
# Install all dependencies
poetry install

# Add a new package
poetry add <package-name>

# Add a development-only package
poetry add --group dev <package-name>

# Update dependencies
poetry update

# Show installed packages
poetry show

# Show project info
poetry env info

# Activate virtual environment
poetry shell

# Run a command in the virtual environment
poetry run <command>

# Exit virtual environment (when using poetry shell)
exit
```

---

## Invoke Tasks

### What is Invoke?

Invoke is a Python task execution tool that provides convenient shortcuts for common commands. All tasks are defined in `tasks.py`.

### Available Tasks

#### 1. **start** - Launch the Application
```bash
poetry run invoke start
```
- Starts the Laihdutanyt GUI application
- Opens login window
- Use this for normal application usage

**When to use:**
- Every time you want to use the app
- After making code changes (restart terminal first)
- For demonstration purposes

---

#### 2. **test** - Run All Tests
```bash
poetry run invoke test
```
- Runs all tests in `tests/` directory
- Uses pytest
- Shows verbose output

**Output example:**
```
🧪 Running tests...
tests/test_user_service.py::test_register_user PASSED
tests/test_user_service.py::test_authenticate_user PASSED
======================== 2 passed in 0.5s ========================
```

**When to use:**
- After making code changes
- Before committing code
- To verify everything works

---

#### 3. **coverage** - Test Coverage Report
```bash
poetry run invoke coverage
```
- Runs tests with coverage analysis
- Generates HTML report in `htmlcov/`
- Shows coverage percentage in terminal

**Output example:**
```
📊 Running tests with coverage...
---------- coverage: platform linux, python 3.11.x -----------
Name                              Stmts   Miss  Cover
-----------------------------------------------------
src/services/user_service.py         45      2    96%
src/repositories/user_repository     30      0   100%
-----------------------------------------------------
TOTAL                               275     15    95%

✅ Coverage report generated in htmlcov/index.html
```

**View HTML report:**
```bash
# Linux/Ubuntu
xdg-open htmlcov/index.html

# Windows
start htmlcov/index.html

# macOS
open htmlcov/index.html
```

**When to use:**
- To check which code is tested
- Before course submission (need good coverage)
- When writing new tests

---

#### 4. **lint** - Code Quality Check
```bash
poetry run invoke lint
```
- Runs pylint on all source code
- Checks for code quality issues
- Reports style violations

**Output example:**
```
🔍 Running pylint...
************* Module src.services.user_service
src/services/user_service.py:45:0: C0301: Line too long (120/100) (line-too-long)
src/services/user_service.py:60:0: R0913: Too many arguments (6/5) (too-many-arguments)

Your code has been rated at 9.50/10
```

**Common pylint issues:**
- `C0301: Line too long` - Break long lines
- `R0913: Too many arguments` - Refactor to use fewer parameters
- `W0612: Unused variable` - Remove or use the variable

**When to use:**
- Before committing code
- To maintain code quality
- When refactoring

---

#### 5. **init-db** - Initialize Database
```bash
poetry run invoke init-db
```
- Creates/recreates `src/data/laihdutanyt.db`
- Creates all necessary tables
- **WARNING:** Deletes existing data!

**When to use:**
- First-time setup
- After database corruption
- To reset to clean state
- When schema changes

**⚠️ Caution:** This will delete all your data!

---

#### 6. **clean** - Clean Generated Files
```bash
poetry run invoke clean
```
- Removes `.pytest_cache/`
- Removes `htmlcov/`
- Removes `.coverage` file
- Removes `__pycache__` directories

**When to use:**
- Before creating a distribution
- When facing import issues
- To free up disk space
- Before pushing to Git

---

#### 7. **check** - Run All Quality Checks
```bash
poetry run invoke check
```
- Runs test + coverage + lint
- Comprehensive quality check
- Takes longer but thorough

**When to use:**
- Before major commits
- Before course submission
- Weekly code quality checks

---

#### 8. **lint-services** - Lint Only Services
```bash
poetry run invoke lint-services
```
- Runs pylint only on `src/services/`
- Faster than full lint
- Focus on business logic quality

**When to use:**
- When working on service layer
- Quick quality check
- During development

---

#### 9. **install** - Install Dependencies
```bash
poetry run invoke install
```
- Runs `poetry install`
- Installs all dependencies from lock file
- Creates/updates virtual environment

**When to use:**
- After cloning repository
- After `pyproject.toml` changes
- When dependencies are missing

---

#### 10. **update** - Update Dependencies
```bash
poetry run invoke update
```
- Updates all packages to latest compatible versions
- Updates `poetry.lock`

**When to use:**
- Monthly maintenance
- Security updates
- After major changes

---

#### 11. **help-tasks** - Show Task Help
```bash
poetry run invoke help-tasks
```
- Shows all available tasks
- Displays usage examples
- Quick reference guide

---

## Daily Workflows

### Workflow 1: Regular Usage (Just Using the App)

```bash
# Start the application
poetry run invoke start

# That's it! Use the GUI normally.
```

### Workflow 2: Making Small Changes

```bash
# 1. Make your code changes in editor

# 2. Test your changes
poetry run invoke test

# 3. If tests pass, run the app to see changes
# (Restart terminal first on Windows)
poetry run invoke start
```

### Workflow 3: Adding New Feature

```bash
# 1. Create feature branch (if using Git)
git checkout -b feature/new-feature

# 2. Make code changes

# 3. Write tests for new feature
# Edit tests/test_*.py

# 4. Run tests
poetry run invoke test

# 5. Check coverage
poetry run invoke coverage

# 6. Check code quality
poetry run invoke lint

# 7. If all pass, commit
git add .
git commit -m "Add new feature"

# 8. Test the feature in GUI
poetry run invoke start
```

---

## Development Workflow

### Daily Development Cycle

```bash
# Morning: Pull latest changes
git pull origin main
poetry install  # In case dependencies changed

# Development loop:
# 1. Make changes
# 2. poetry run invoke test
# 3. Fix any failures
# 4. Repeat

# Before lunch: Quick quality check
poetry run invoke lint-services

# End of day: Full check
poetry run invoke check

# If all passes: Commit
git add .
git commit -m "Daily progress"
git push
```

### Testing Workflow

```bash
# Write a new test
# Edit tests/test_something.py

# Run just that test
poetry run pytest tests/test_something.py -v

# Run all tests
poetry run invoke test

# Check coverage
poetry run invoke coverage

# View detailed coverage
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html      # Windows
```

### Before Submitting Assignment

```bash
# 1. Full quality check
poetry run invoke check

# 2. Clean up temporary files
poetry run invoke clean

# 3. Reinitialize database for clean demo
poetry run invoke init-db

# 4. Import sample data
poetry run python src/scripts/import_foods.py
poetry run python src/scripts/import_activities.py

# 5. Test the application thoroughly
poetry run invoke start
# - Test all features
# - Take screenshots
# - Verify no errors

# 6. Generate final coverage report
poetry run invoke coverage

# 7. Update documentation
# - Update tuntikirjanpito.md
# - Update changelog.md
# - Check user_instructions.md

# 8. Create submission package
# (See DELIVERY_READY.md)
```

---

## Troubleshooting

### Issue: "invoke: command not found"

**Solution:**
```bash
# Make sure you're using poetry run
poetry run invoke start

# Or activate the shell first
poetry shell
invoke start
```

### Issue: "No module named 'invoke'"

**Solution:**
```bash
# Reinstall dependencies
poetry install
```

### Issue: "python: command not found"

**Solution:**
```bash
# Use python3 explicitly
poetry run python3 src/main.py

# Or configure Poetry to use Python 3.11
poetry env use python3.11
poetry install
```

### Issue: Changes not taking effect

**Solution:**
```bash
# 1. Close the application completely
# 2. Kill any Python processes (Windows)
taskkill /F /IM python.exe

# 3. Restart terminal
# 4. Run again
poetry run invoke start
```

### Issue: "Database is locked"

**Solution:**
```bash
# Close all instances of the app
# Remove lock file
rm src/data/laihdutanyt.db-shm
rm src/data/laihdutanyt.db-wal

# Restart app
poetry run invoke start
```

### Issue: Tests fail after changes

**Solution:**
```bash
# 1. Read the error message carefully
poetry run invoke test

# 2. Run specific test for details
poetry run pytest tests/test_failing.py -vv

# 3. Check if database needs reset
poetry run invoke init-db

# 4. Check if imports are correct
poetry run invoke clean
poetry install
```

---

## Shortcuts and Tips

### Shorter Command: Use `inv` instead of `invoke`

```bash
# These are equivalent:
poetry run invoke start
poetry run inv start

# Shorter version works for all tasks:
poetry run inv test
poetry run inv coverage
poetry run inv lint
```

### Quick Test-Fix Loop

```bash
# Run tests continuously (requires pytest-watch)
poetry add --group dev pytest-watch
poetry run ptw tests/
```

### Check What's Installed

```bash
# List all packages
poetry show

# Check specific package
poetry show pytest

# Show outdated packages
poetry show --outdated
```

### Virtual Environment Location

```bash
# Show environment info
poetry env info

# Show environment path
poetry env info --path

# List all environments
poetry env list
```

---

## Configuration File (pyproject.toml)

The `pyproject.toml` file configures the entire project:

```toml
[tool.poetry]
name = "laihdutanyt"
version = "2.2.0"
description = "Weight loss tracking application"
authors = ["Your Name"]

[tool.poetry.dependencies]
python = "^3.11"
sqlalchemy = "^2.0"
invoke = "^2.0"
# ... more dependencies

[tool.poetry.group.dev.dependencies]
pytest = "^7.4"
pytest-cov = "^4.1"
pylint = "^3.0"
# ... dev dependencies
```

**Key sections:**
- `dependencies` - Required packages
- `dev-dependencies` - Development tools
- `scripts` - Custom commands
- `tool.pytest` - Pytest configuration
- `tool.coverage` - Coverage configuration

---

## Sample Data Import

### Import Foods from CSV

```bash
poetry run python src/scripts/import_foods.py
```

**CSV Format (`src/data/sample_foods.csv`):**
```csv
name,calories_per_portion,carbs_per_portion,protein_per_portion,fat_per_portion
Apple,52,14,0.3,0.2
Banana,89,23,1.1,0.3
```

### Import Activities from CSV

```bash
poetry run python src/scripts/import_activities.py
```

**CSV Format (`src/data/sample_activities.csv`):**
```csv
name,calories_per_activity
Running,300
Cycling,250
```

---

## Quick Reference Card

```bash
# Common Commands
poetry run inv start          # Launch app
poetry run inv test           # Run tests
poetry run inv coverage       # Test + coverage
poetry run inv lint           # Check quality
poetry run inv init-db        # Reset database
poetry run inv clean          # Clean files
poetry run inv check          # Full quality check

# Shortcuts
poetry run inv --list         # Show all tasks
poetry run inv --help start   # Task help
poetry shell                  # Enter environment
exit                          # Leave environment

# Development
poetry install                # Install deps
poetry add <package>          # Add package
poetry show                   # List packages
poetry update                 # Update all
```

---

**Last Updated:** December 21, 2025
**Poetry Version:** 1.7+
**Invoke Version:** 2.0+
