"""
Invoke tasks for Laihdutanyt project
Run with: poetry run invoke <task-name>
Plan made by Claude AI 4.5, 
but never implemented because of tight time constraints, 
testing in practise done manually, especially UI-testing and code reviews.
"""

from invoke import task

@task
def start(ctx):
    """Start the application"""
    print(" Starting Laihdutanyt application...")
    ctx.run("python src/main.py", pty=False)

@task
def test(ctx):
    """Run all tests"""
    print(" Running tests...")
    ctx.run("pytest tests/ -v", pty=False)

@task
def coverage(ctx):
    """Run tests with coverage report"""
    print(" Running tests with coverage...")
    ctx.run("pytest tests/ --cov=src --cov-report=html --cov-report=term", pty=False)
    print("\n Coverage report generated in htmlcov/index.html")

@task
def coverage_report(ctx):
    """Generate coverage report (after running coverage)"""
    print(" Generating coverage report...")
    ctx.run("pytest tests/ --cov=src --cov-report=html", pty=False)
    print(" Open htmlcov/index.html in your browser")

@task
def lint(ctx):
    """Run pylint on source code"""
    print(" Running pylint...")
    ctx.run("pylint src/", pty=False)

@task
def lint_services(ctx):
    """Run pylint only on services"""
    print(" Linting services...")
    ctx.run("pylint src/services/", pty=False)

@task
def format_check(ctx):
    """Check code formatting (if you add black later)"""
    print(" Checking code format...")
    print("️  Install black first: poetry add --group dev black")
    # ctx.run("black --check src/", pty=False)

@task
def clean(ctx):
    """Clean up generated files"""
    print("🧹 Cleaning up...")
    ctx.run("rm -rf .pytest_cache", warn=True, pty=False)
    ctx.run("rm -rf htmlcov", warn=True, pty=False)
    ctx.run("rm -rf .coverage", warn=True, pty=False)
    ctx.run("rm -rf src/__pycache__", warn=True, pty=False)
    ctx.run("rm -rf src/*/__pycache__", warn=True, pty=False)
    ctx.run("rm -rf src/*/*/__pycache__", warn=True, pty=False)
    print(" Cleanup complete!")

@task
def init_db(ctx):
    """Initialize/recreate the database"""
    print(" Initializing database...")
    ctx.run("python src/create_db.py", pty=False)
    print(" Database initialized!")

@task(pre=[test, coverage, lint])
def check(ctx):
    """Run all checks: tests, coverage, and linting"""
    print("\n All checks passed!")

@task
def install(ctx):
    """Install all dependencies"""
    print(" Installing dependencies...")
    ctx.run("poetry install", pty=False)
    print(" Dependencies installed!")

@task
def update(ctx):
    """Update dependencies"""
    print("⬆️  Updating dependencies...")
    ctx.run("poetry update", pty=False)
    print(" Dependencies updated!")

@task
def help_tasks(ctx):
    """Show available tasks"""
    print("""
 Available Invoke Tasks:

Basic Commands:
  poetry run invoke start              - Start the application
  poetry run invoke test               - Run all tests
  poetry run invoke coverage           - Run tests with coverage
  poetry run invoke lint               - Run pylint on all code
  
Database:
  poetry run invoke init-db            - Initialize/recreate database
  
Quality Checks:
  poetry run invoke check              - Run tests + coverage + lint
  poetry run invoke lint-services      - Lint only services layer
  poetry run invoke coverage-report    - Generate HTML coverage report
  
Maintenance:
  poetry run invoke clean              - Clean up generated files
  poetry run invoke install            - Install dependencies
  poetry run invoke update             - Update dependencies

