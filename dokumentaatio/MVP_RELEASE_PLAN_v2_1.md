# Laihdutanyt v2.1 - MVP Release Plan

##  Release Objective

**Focus:** Demonstrate excellent software engineering practices, documentation, and testing methodology  
**Timeline:** 1 day implementation  
**Priority:** Process & Quality > Feature Richness  
**Target:** Linux (Ubuntu) deployment with Poetry

---

##  Release Scope: v2.1 "Statistics Core"

###  MUST HAVE (Core MVP)

#### 1. Database Enhancements
- [x] Create `weightlog` table for weight tracking
- [x] Add basic nutrient columns to `statistics` table
- [x] Improve demo data with 30-day sample logs

#### 2. Weight Tracking Feature
- [ ] "Log Weight" button in main dashboard
- [ ] Simple weight entry form (date, weight)
- [ ] Display last 5 weight entries
- [ ] Calculate weekly weight change

#### 3. Basic Statistics Dashboard
- [ ] Daily calorie summary (consumed, burned, net)
- [ ] Basic nutrient totals (carbs, protein, fat in grams)
- [ ] Simple text-based progress indicators
- [ ] "Within goal" status (green/yellow/red indicator)

#### 4. Demo Data & Testing
- [ ] Generate 30 days of realistic sample data
- [ ] Unit tests for WeightLogService (>80% coverage)
- [ ] Unit tests for StatisticsService (>80% coverage)
- [ ] Integration test: Complete user workflow

#### 5. Documentation (Critical!)
- [x] Requirements specification (v3)
- [x] ERD diagram (enhanced_ERD_v3.mmd)
- [x] Sequence diagrams (5 use cases)
- [ ] User instructions for v2.1
- [ ] Ubuntu installation guide
- [ ] CHANGELOG.md
- [ ] RELEASE_NOTES_v2.1.md
- [ ] Architecture document update
- [ ] Testing documentation

#### 6. Poetry & Development Tools
- [ ] Update `pyproject.toml` dependencies
- [ ] Poetry invoke tasks for common operations
- [ ] Coverage reporting configuration
- [ ] Linting and formatting setup

---

###  OUT OF SCOPE (Future: v2.2+)

- Charts and graphs (matplotlib)
- Weekly/monthly reports
- Coach features
- Dietary plan management
- PDF export
- Advanced UI widgets
- AI recommendations

---

## ️ Implementation Plan (Today)

### Phase 1: Database & Infrastructure (2 hours)

**Tasks:**
1. Update `src/create_db.py` with new schema
2. Create migration script for existing databases
3. Generate comprehensive demo data (30 days)
4. Create database seeding script

**Deliverables:**
- `src/migrations/add_weightlog_and_stats.py`
- `src/scripts/generate_demo_data.py`
- Updated `src/create_db.py`

---

### Phase 2: Core Services (2 hours)

**Tasks:**
1. Create `src/repositories/weightlog_repository.py`
2. Create `src/services/weightlog_service.py`
3. Create `src/services/statistics_service.py` (basic version)
4. Write unit tests for all services

**Deliverables:**
- 3 new service/repository files
- `tests/test_weightlog_service.py`
- `tests/test_statistics_service.py`
- Test coverage >80%

---

### Phase 3: UI Implementation (3 hours)

**Tasks:**
1. Add "Log Weight" button to main dashboard
2. Create simple weight log form
3. Add statistics summary card to dashboard
4. Create basic statistics view (text-based)
5. Update existing views with calorie info labels

**Deliverables:**
- `src/ui/views/weight_log_view.py`
- `src/ui/views/statistics_simple_view.py`
- Updated `src/ui/app.py`

---

### Phase 4: Testing & Validation (2 hours)

**Tasks:**
1. Write integration tests
2. Run coverage report
3. Manual testing on Ubuntu VM
4. Fix critical bugs

**Deliverables:**
- `tests/test_integration_statistics.py`
- Coverage report (target: >75%)
- Bug fixes committed

---

### Phase 5: Documentation (2 hours)

**Tasks:**
1. Write Ubuntu installation guide
2. Write user instructions for v2.1
3. Create CHANGELOG.md
4. Create RELEASE_NOTES_v2.1.md
5. Update architecture documentation
6. Document testing process

**Deliverables:**
- `dokumentaatio/UBUNTU_INSTALLATION.md`
- `dokumentaatio/user_instructions_v2.1.md`
- `CHANGELOG.md`
- `dokumentaatio/RELEASE_NOTES_v2.1.md`
- `dokumentaatio/TESTING_GUIDE.md`

---

### Phase 6: Poetry & Automation (1 hour)

**Tasks:**
1. Update `pyproject.toml` with new dependencies
2. Create `tasks.py` with Poetry invoke commands
3. Configure pytest and coverage
4. Add pre-commit hooks (optional)

**Deliverables:**
- Updated `pyproject.toml`
- Updated `tasks.py` with new commands
- `.coveragerc` configuration

---

##  Detailed Task Breakdown

### Database Schema Changes

```sql
-- 1. Create weightlog table
CREATE TABLE IF NOT EXISTS weightlog (
    log_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    date TEXT NOT NULL,
    weight REAL NOT NULL,
    notes TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES "user"(user_id) ON DELETE CASCADE
);

-- 2. Enhance statistics table (add columns)
ALTER TABLE statistics ADD COLUMN total_kcal_burned REAL DEFAULT 0.0;
ALTER TABLE statistics ADD COLUMN net_kcal REAL DEFAULT 0.0;
ALTER TABLE statistics ADD COLUMN total_carbs_g REAL DEFAULT 0.0;
ALTER TABLE statistics ADD COLUMN total_protein_g REAL DEFAULT 0.0;
ALTER TABLE statistics ADD COLUMN total_fat_g REAL DEFAULT 0.0;

-- 3. Create unique index
CREATE UNIQUE INDEX IF NOT EXISTS idx_statistics_user_date 
ON statistics(user_id, date);

-- 4. Create index for weight logs
CREATE INDEX IF NOT EXISTS idx_weightlog_user_date 
ON weightlog(user_id, date DESC);
```

---

### Demo Data Requirements

**30-Day Sample Data for Test User:**
- Daily food logs (2-4 meals per day)
- Daily activity logs (1-2 activities per day)
- Weekly weight logs (4 entries over 30 days)
- Variety of foods (breakfast, lunch, dinner, snacks)
- Variety of activities (walking, running, cycling)

**Script:** `src/scripts/generate_demo_data.py`
```python
def generate_30_days_demo_data(user_id: str):
    """Generate realistic 30-day sample data"""
    # For each day in last 30 days:
    #   - Add 2-4 food logs (breakfast, lunch, dinner, snacks)
    #   - Add 1-2 activity logs (varied activities)
    #   - Calculate and save daily statistics
    # Every 7 days:
    #   - Add weight log entry (gradual weight loss)
```

---

### Poetry Invoke Tasks

**Required `tasks.py` commands:**

```python
from invoke import task

@task
def lint(c):
    """Run linting (pylint)"""
    c.run("poetry run pylint src/", pty=True)

@task
def format_check(c):
    """Check code formatting"""
    c.run("poetry run black --check src/ tests/", pty=True)

@task
def format_fix(c):
    """Fix code formatting"""
    c.run("poetry run black src/ tests/", pty=True)

@task
def init_db(c):
    """Initialize database with demo data"""
    c.run("poetry run python src/create_db.py", pty=True)

@task
def generate_demo(c):
    """Generate 30-day demo data"""
    c.run("poetry run python src/scripts/generate_demo_data.py", pty=True)

@task
def run(c):
    """Run the application"""
    c.run("poetry run python src/main.py", pty=True)

@task
def clean(c):
    """Clean generated files"""
    c.run("rm -rf .pytest_cache __pycache__ .coverage htmlcov", pty=True)

@task
def all_checks(c):
    """Run all quality checks"""
    format_check(c)
    lint(c)
    coverage(c)
```

---

## 🧪 Testing Requirements

### Unit Tests (Target: >80% coverage)

**test_weightlog_service.py:**
- `test_log_weight_success()`
- `test_log_weight_invalid_weight()`
- `test_get_weight_history()`
- `test_calculate_weekly_change()`

**test_statistics_service.py:**
- `test_get_daily_summary()`
- `test_calculate_nutrient_breakdown()`
- `test_calculate_calorie_balance()`

### Integration Tests

**test_integration_statistics.py:**
- `test_complete_workflow_food_to_stats()`
- `test_complete_workflow_activity_to_stats()`
- `test_weight_tracking_workflow()`

### Manual Testing Checklist
- [ ] User can log in
- [ ] User can log food and see updated calories
- [ ] User can log activity and see burned calories
- [ ] User can log weight
- [ ] Statistics dashboard shows correct totals
- [ ] Nutrient calculations are accurate
- [ ] Application handles errors gracefully
- [ ] Application runs on Ubuntu without issues

---

## 📚 Documentation Deliverables

### 1. UBUNTU_INSTALLATION.md
**Contents:**
- Prerequisites (Python 3.10+, Poetry)
- Installation steps
- Database initialization
- Running the application
- Troubleshooting

### 2. user_instructions_v2.1.md
**Contents:**
- Overview of v2.1 features
- How to log weight
- How to view statistics
- Understanding calorie calculations
- FAQ

### 3. CHANGELOG.md
**Format:**
```markdown
# Changelog

## [2.1.0] - 2025-12-20

### Added
- Weight tracking feature
- Basic statistics dashboard
- Daily nutrient breakdown
- 30-day demo data generation
- Comprehensive test suite

### Changed
- Enhanced database schema
- Improved calorie calculation display
- Updated user dashboard layout

### Fixed
- Date categorization logic
- SQL query optimization
```

### 4. RELEASE_NOTES_v2.1.md
**Contents:**
- Release highlights
- New features description
- Known limitations
- Upgrade instructions
- Breaking changes (if any)

### 5. TESTING_GUIDE.md
**Contents:**
- How to run tests
- How to generate coverage report
- Test data setup
- Writing new tests
- CI/CD considerations

---

## 📊 Quality Metrics

**Target Metrics for v2.1:**
- ✅ Test coverage: >75%
- ✅ Pylint score: >8.0/10
- ✅ All critical bugs fixed
- ✅ Documentation complete
- ✅ Works on Ubuntu 22.04 LTS
- ✅ Poetry commands functional

---

## 🚀 Deployment Checklist

### Pre-Release
- [ ] All tests passing
- [ ] Coverage >75%
- [ ] Pylint score >8.0
- [ ] Documentation complete
- [ ] Demo data generated
- [ ] Ubuntu installation tested

### Release Package
- [ ] Tag version: `git tag v2.1.0`
- [ ] Create release branch
- [ ] Package with Poetry: `poetry build`
- [ ] Verify installation from scratch

### Post-Release
- [ ] Update main README.md
- [ ] Archive old documentation
- [ ] Plan v2.2 features

---

## 🎓 Evaluation Criteria Alignment

### 1. Architecture & Design (Weight: 30%)
- ✅ Clean layered architecture (UI → Service → Repository)
- ✅ ERD diagram (enhanced_ERD_v3.mmd)
- ✅ Sequence diagrams (5 use cases)
- ✅ Clear separation of concerns

### 2. Documentation (Weight: 25%)
- ✅ Requirements specification (v3)
- ✅ Architecture documentation
- ✅ User instructions
- ✅ Installation guide
- ✅ Testing guide
- ✅ Code comments

### 3. Testing (Weight: 20%)
- ✅ Unit tests (>80% coverage target)
- ✅ Integration tests
- ✅ Test documentation
- ✅ Coverage reporting

### 4. Development Process (Weight: 15%)
- ✅ Version control (Git)
- ✅ Poetry dependency management
- ✅ Invoke task automation
- ✅ Code quality tools (pylint, black)
- ✅ Changelog maintenance

### 5. Functionality (Weight: 10%)
- ✅ Core features working
- ✅ Error handling
- ✅ User-friendly interface
- ✅ Data persistence

---

## 🔄 Risk Mitigation

### Risk 1: Time Constraint
**Mitigation:** 
- Keep UI simple (text-based, no charts)
- Focus on core statistics only
- Defer advanced features to v2.2

### Risk 2: Ubuntu Compatibility
**Mitigation:**
- Test early on Ubuntu VM
- Use standard Python libraries
- Document dependencies clearly

### Risk 3: Test Coverage
**Mitigation:**
- Start with service layer tests (highest value)
- Use pytest fixtures for common setup
- Focus on critical paths first

---

## 📝 Success Criteria

**v2.1 is successful if:**
1. ✅ User can track weight over time
2. ✅ User can view daily calorie and nutrient summary
3. ✅ Application runs on Ubuntu with Poetry
4. ✅ Test coverage >75%
5. ✅ All documentation complete
6. ✅ Demo data provides realistic testing scenario
7. ✅ Poetry invoke commands work correctly
8. ✅ Installation process is clear and documented

---

## 🎯 Next Release Preview: v2.2

**Future Features (Not in v2.1):**
- Weekly progress report with charts
- Weight trend visualization (matplotlib)
- Goal adherence percentage
- Enhanced statistics view
- Export data functionality

---

**Document Version:** 1.0  
**Date:** 2025-12-20  
**Status:** Implementation Ready  
**Estimated Effort:** 12 hours (1 day with focus)
