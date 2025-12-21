# Poetry and Invoke Setup Guide

## 📦 Step 1: Install Poetry

If you don't have Poetry installed yet:

### Windows (PowerShell):
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

### Alternative - Using pip:
```powershell
pip install poetry
```

### Verify Installation:
```powershell
poetry --version
```

---

## 🔧 Step 2: Install Project Dependencies

Once Poetry is installed:

```powershell
# Navigate to project root
cd c:\ot-harjoitustyo_local\ot-harjoitustyo5\ot-harjoitustyo

# Install all dependencies (including dev dependencies)
poetry install

# Or update existing ones
poetry update
```

---

## 🚀 Step 3: Using Invoke Tasks

After running `poetry install`, you can use these commands:

### Basic Commands:

```powershell
# Start the application
poetry run invoke start

# Run tests
poetry run invoke test

# Run tests with coverage
poetry run invoke coverage

# Run linting
poetry run invoke lint
```

### Shortcuts:
You can use `inv` instead of `invoke`:
```powershell
poetry run inv test
poetry run inv coverage
```

---

## 📋 Available Tasks

### Application:
- `poetry run invoke start` - Start the Laihdutanyt application
- `poetry run invoke init-db` - Initialize/recreate database

### Testing:
- `poetry run invoke test` - Run all tests
- `poetry run invoke coverage` - Run tests with coverage report
- `poetry run invoke coverage-report` - Generate HTML coverage report

### Code Quality:
- `poetry run invoke lint` - Run pylint on all source code
- `poetry run invoke lint-services` - Lint only the services layer
- `poetry run invoke check` - Run tests + coverage + lint (all checks)

### Maintenance:
- `poetry run invoke clean` - Clean up __pycache__ and coverage files
- `poetry run invoke install` - Install dependencies
- `poetry run invoke update` - Update dependencies

### Help:
- `poetry run invoke --list` - List all available tasks
- `poetry run invoke --help <task>` - Get help for a specific task
- `poetry run invoke help-tasks` - Show detailed task descriptions

---

## 🧪 Creating Tests

### Test File Structure:
```
tests/
├── conftest.py              # Test configuration
├── test_user_service.py     # User service tests
├── test_food_service.py     # Food service tests (create this)
└── test_activity_service.py # Activity service tests (create this)
```

### Example Test:
```python
# tests/test_food_service.py
import pytest
from services.food_service import FoodService

def test_get_food_display_list(temp_db):
    service = FoodService(temp_db)
    foods = service.get_food_display_list()
    assert isinstance(foods, list)
```

### Running Tests:
```powershell
# Run all tests
poetry run pytest

# Run specific test file
poetry run pytest tests/test_user_service.py

# Run with verbose output
poetry run pytest -v

# Run with coverage
poetry run pytest --cov=src

# Generate HTML coverage report
poetry run pytest --cov=src --cov-report=html
# Then open: htmlcov/index.html
```

---

## 📊 Coverage Reports

After running `poetry run invoke coverage`:
1. Terminal shows coverage summary
2. HTML report generated in `htmlcov/` folder
3. Open `htmlcov/index.html` in browser for detailed view

---

## 🎯 Recommended Workflow

### Daily Development:
```powershell
# 1. Start development
poetry shell  # Activate virtual environment

# 2. Run tests frequently
poetry run inv test

# 3. Check coverage before commit
poetry run inv coverage

# 4. Lint your code
poetry run inv lint-services
```

### Before Git Commit:
```powershell
# Run all checks
poetry run inv check

# If all pass, commit your changes
git add .
git commit -m "Your commit message"
```

---

## 🔍 Troubleshooting

### Poetry not recognized?
- Restart your terminal/PowerShell
- Check if Poetry is in PATH: `$env:Path`
- Try: `python -m poetry` instead of `poetry`

### Import errors in tests?
- Make sure you ran `poetry install`
- Check that `tests/conftest.py` exists
- Verify `pyproject.toml` has `pythonpath = ["src"]`

### Invoke not working?
- Install it: `poetry add --group dev invoke`
- Make sure `tasks.py` is in project root
- Use full command: `poetry run invoke test`

---

## 📚 Additional Tools (Optional)

### Add Code Formatter (Black):
```powershell
poetry add --group dev black
```

Then format code:
```powershell
poetry run black src/
```

### Add Type Checker (mypy):
```powershell
poetry add --group dev mypy
```

Then check types:
```powershell
poetry run mypy src/
```

---

## ✅ Quick Start Checklist

- [ ] Install Poetry
- [ ] Run `poetry install` in project directory
- [ ] Test with: `poetry run invoke --list`
- [ ] Run first test: `poetry run invoke test`
- [ ] Generate coverage: `poetry run invoke coverage`
- [ ] View coverage report in browser
- [ ] Start application: `poetry run invoke start`

---

## 🎓 Learning Resources

- Poetry Docs: https://python-poetry.org/docs/
- Invoke Docs: https://www.pyinvoke.org/
- pytest Docs: https://docs.pytest.org/
- pytest-cov: https://pytest-cov.readthedocs.io/

---

Good luck with testing and coverage! 🚀
