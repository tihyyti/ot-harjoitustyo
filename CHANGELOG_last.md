# Changelog

All notable changes to the Laihdutanyt-project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

## [2.1.0] - 2025-12-20

### Added
- **Weight Tracking Feature**
  - New `weightlog` database table for tracking weight measurements over time
  - "Log Weight" button in main dashboard
  - Weight history display showing last 5 measurements
  - Weekly weight change calculation and display
  - Weight tracking repository and service layer

- **Basic Statistics Dashboard**
  - Daily calorie summary (consumed, burned, net balance)
  - Basic nutrient totals (carbohydrates, protein, fat in grams)
  - Visual status indicators (green/yellow/red for goal adherence)
  - "Within goal" status display
  - StatisticsService for calculation logic

- **Enhanced Database Schema**
  - Added columns to `statistics` table: `total_kcal_burned`, `net_kcal`, `total_carbs_g`, `total_protein_g`, `total_fat_g`
  - Added indexes for improved query performance
  - Database migration script (`src/migrations/migrate_to_v2_1.py`)

- **Demo Data Generation**
  - Comprehensive 30-day demo data generator script
  - Realistic food logs (2-4 meals per day)
  - Realistic activity logs (1-2 activities per day)
  - Weekly weight measurements showing gradual weight loss
  - Automated daily statistics calculation

- **Documentation**
  - Comprehensive requirements specification v3 (`statistics_requirements_v3.md`)
  - Enhanced ERD diagram (`enhanced_ERD_v3.mmd`)
  - 5 detailed sequence diagrams for core use cases
  - Ubuntu installation guide
  - Testing guide
  - MVP release plan documentation

- **Development Tools**
  - Updated Poetry invoke tasks for common operations
  - Database migration command
  - Demo data generation command
  - Linting and formatting commands

### Changed
- **Calorie Calculation Display**
  - Added unit labels to dashboards ("per 100g" for food, "per 1000 units" for activities)
  - Improved formatting with consistent Arial 12 font
  - Enhanced spacing and column alignment in logs

- **User Interface Improvements**
  - Login header styled consistently with other dashboards
  - Registration window narrowed and better centered
  - Smart feedback messages (only for future dates)
  - Info notes about viewing future events
  - Added logout button to main dashboard

- **Code Quality**
  - Refactored service layer for better separation of concerns
  - Improved error handling and validation
  - Enhanced code comments and docstrings
  - Fixed lint warnings

- **Database Queries**
  - Optimized SQL queries in FoodService and ActivityService
  - Removed incorrect multiplication in calorie calculations
  - Added proper GROUP BY clauses for aggregations

### Fixed
- **Display Issues**
  - Fixed raw dictionary display in daily dashboards (was showing dict objects)
  - Fixed Treeview style name conflicts between windows
  - Removed invalid Listbox parameters (spacing1/spacing3)

- **Calculation Bugs**
  - Fixed SQL query that was double-counting activity calories
  - Fixed inverted date categorization logic (< for past, > for future)
  - Corrected net calorie calculation formula

- **Validation Issues**
  - Added comprehensive registration form validation
  - Prevented negative number inputs
  - Added range checks (weight, height, age, activity level)
  - Cross-field validation (kcal_min < kcal_max)

- **UI/UX Issues**
  - Fixed placeholder text implementation in registration form
  - Improved focus handling in input fields
  - Better error messages with specific guidance

## [2.0.0] - 2025-12-15

### Added
- Initial refactored version with layered architecture
- Separate UI, Service, and Repository layers
- Tkinter-based desktop application
- SQLite database backend
- User authentication system
- Food and activity logging
- Daily totals views
- Admin dashboard (basic)

### Changed
- Complete refactoring from monolithic to layered architecture
- Improved code organization and modularity
- Better separation of concerns

## [1.0.0] - 2025-11-30

### Added
- Initial prototype version
- Basic food tracking
- Simple calorie calculations
- Monolithic architecture

---

## Versioning Guide

- **MAJOR** version when made incompatible API changes or major feature rewrites
- **MINOR** version when added functionality in a backwards-compatible manner
- **PATCH** version when made backwards-compatible bug fixes

## Categories

- **Added** for new features
- **Changed** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** in case of vulnerabilities
