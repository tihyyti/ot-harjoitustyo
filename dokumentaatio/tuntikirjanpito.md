# Työaikakirjanpito

| päivä | aika | mitä tein  |
| :----:|:-----| :----------|
| 03.11.| 3    | Tutustuminen harj.työn ohjeisiin ja GIT-repon sekä tiedostojen alustustoimet |
| 04.11.| 8    | Työkalujen valinta (Python 3.10 ja Tkinter, Chubli environment), alustava vaatimusten määrittely|
| 11.11 | 7    | Vaatimusmäärittely, usecaset ja storyt, UI-kaavio, ERD-diagrammi, Chubblin ja lokaalikoneen tiedostosiirron opettelu||
| 18.11 | 10   | Added food and foodlog sql-tabless and model classes plus their processing in Laihdutanyt_v1
| 25.11.| 19   | Added activity and activitylog sql-tables and model classes, their processing in Laihdutanyt_v1
|       |      |plus import activities-script, created new laihdutanyt.db. 
|       |       Testing of all pending.
| 02.12.| 25   | Components implemented and tested:
                - User Registration and Log-in
                - Main button-menu
                - Food and Activity Dashboards with data-entry logging
                - Food and Activity Loggings viewing windows with Edit/Delete/Close functionality
                - Usability testing of implemented parts
                Docs updated: User instructions
| 07.12.|  7   |    - Use-case-testing and refactoring of all UI continued to 
                      managed "Card-UI" for multiple screens and usage patterns  (laptop + 2nd display)
                    - Daily Food and Activities totals UI-panels implemented and tested
| 08.12.| 11   |Admin/Coach usecases implemented and tested: 
                    - User Management
                    - Create Recommendations
                    - Track health constraints
                    - Preview of future AI features
| 09.12. | 11   | Admin-db-table, Docs updated: User instructions, Architecture refactoring into layered structure with the help of AI/Claude, Laihdutanyt release 2_1 Requirements Specification updated, changelog.md updated, 
| 21.12. | 32   | ### For Release v2.1 Features (New Backend Services)

Requirement setting, design, testing and delivery planning and validation, final delivery.

#### 1. **Weight Logging UI** 
**Backend Ready:** WeightLogService, WeightLogRepository
**UI Needed:**
- Weight log entry form (date, weight, notes)
- Weight history list with week numbers
- Weight trend visualization (optional)
- "Log Weight" button in main dashboard

#### 2. **Dietary Period Management UI** 
**Backend Ready:** DietaryPeriodService, DietaryPeriodRepository
**UI Needed:**
- Period creation form
- Active periods list
- Period effectiveness summary
- Suggested protocols selector
- Integration with weight log display

#### 3. **Statistics Dashboard** 
**Backend Ready:** StatisticsService (not yet created, but data model ready)
**UI Needed:**
- Daily nutrient breakdown
- Weekly progress reports
- Monthly summaries
- Charts and visualizations

#### 4. **Enhanced Weight Log Display** 
**Backend Ready:** `get_weight_history_with_weeks()` method
**UI Features Needed:**
- Week numbering (bold week starts)
- Period annotations (📍 indicators)
- Period start/end markers (▶/⏹)
- Descending order display