# Laihdutanyt Application - Technical Architecture

##  Architecture Overview

The Laihdutanyt application follows a **layered architecture** pattern with clear separation of concerns:

```
┌─────────────────────────────────────────────────┐
│         Presentation Layer (UI)                  │
│  - Login/Register Views                          │
│  - Dashboard Views (Food, Activity, Totals)     │
│  - Admin Panel Views                             │
│  - UI Components (Frames, Dialogs)              │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│         Business Logic Layer (Services)          │
│  - UserService                                   │
│  - FoodService                                   │
│  - ActivityService                               │
│  - AdminService                                  │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│         Data Access Layer (Repositories)         │
│  - UserRepository                                │
│  - FoodRepository                                │
│  - ActivityRepository                            │
│  - FoodLogRepository                             │
│  - ActivityLogRepository                         │
│  - AdminRepository                               │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│         Data Layer (Database)                    │
│  - SQLite Database (laihdutanyt.db)             │
│  - Tables: user, food, activity, foodlog,       │
│    activitylog, admin, recommendation,          │
│    user_constraint                               │
└─────────────────────────────────────────────────┘
```

##  Project Structure

```
ot-harjoitustyo/
├── src/
│   ├── Laihdutanyt_v2.py          # Legacy monolithic file (to be deprecated)
│   ├── main.py                     # NEW: Application entry point
│   │
│   ├── ui/                         # NEW: Presentation layer
│   │   ├── __init__.py
│   │   ├── app.py                 # Main application window & orchestration
│   │   ├── views/                 # Individual view modules
│   │   │   ├── __init__.py
│   │   │   ├── login_view.py     # Login and registration
│   │   │   ├── main_menu_view.py # User dashboard menu
│   │   │   ├── food_view.py      # Food logging dashboard
│   │   │   ├── activity_view.py  # Activity logging dashboard
│   │   │   ├── food_totals_view.py     # Daily food totals
│   │   │   ├── activity_totals_view.py # Daily activity totals
│   │   │   ├── admin_view.py     # Admin panel
│   │   │   └── logs_view.py      # All logs viewer
│   │   └── components/            # Reusable UI components
│   │       ├── __init__.py
│   │       ├── food_log_frame.py # Food logging form
│   │       └── activity_log_frame.py # Activity logging form
│   │
│   ├── services/                   # NEW: Business logic layer
│   │   ├── __init__.py
│   │   ├── user_service.py        # User management logic
│   │   ├── food_service.py        # Food & logging logic
│   │   ├── activity_service.py    # Activity & logging logic
│   │   └── admin_service.py       # Admin operations logic
│   │
│   ├── repositories/               # Data access layer
│   │   ├── models.py              # Data models (User, Food, Activity)
│   │   ├── user_repository.py
│   │   ├── food_repository.py
│   │   ├── foodlog_repository.py
│   │   ├── activity_repository.py
│   │   ├── activitylog_repository.py
│   │   └── admin_repository.py
│   │
│   ├── scripts/                    # Utility scripts
│   │   ├── aggregate_daily_foods_totals.py
│   │   ├── aggregate_daily_activities_totals.py
│   │   ├── import_foods.py
│   │   └── import_activities.py
│   │
│   ├── data/                       # Database files
│   │   ├── laihdutanyt.db
│   │   ├── sample_foods.csv
│   │   └── sample_activities.csv
│   │
│   └── create_db.py               # Database schema creation
│
└── dokumentaatio/                  # Documentation
    ├── architecture.md            # THIS FILE
    ├── architecture_diagram.mmd   # Mermaid diagram
    └── ...
```

##  Layer Responsibilities

### 1. Presentation Layer (UI)

**Purpose**: Handle all user interface concerns - display, user input, visual feedback

**Responsibilities**:
- Render UI elements (windows, forms, tables)
- Capture user input events
- Display data to users
- Navigate between views
- Window management (positioning, sizing, hide/show)

**Key Principles**:
-  NO business logic
-  NO direct database access
-  Calls service layer for data operations
-  Displays data provided by services

**Example**:
```python
# Good: UI calls service
def _on_login(self):
    if self.user_service.authenticate_user(username, password):
        self.show_dashboard()

# Bad: UI contains business logic
def _on_login(self):
    user = self.user_repo.find_by_username(username)
    if user and self._verify_password(password, user.salt):  # Business logic in UI!
        ...
```

### 2. Business Logic Layer (Services)

**Purpose**: Implement business rules, validation, and data transformation

**Responsibilities**:
- Validate user input
- Enforce business rules
- Coordinate between repositories
- Transform data for UI presentation
- Handle complex operations (aggregations, calculations)

**Key Principles**:
-  NO UI code (no tkinter imports)
-  Uses repositories for data access
-  Returns clean data structures (dicts, lists)
-  Raises exceptions for errors

**Example Services**:
- `UserService`: Authentication, registration, user profile management
- `FoodService`: Food logging, daily totals calculation, CRUD operations
- `ActivityService`: Activity logging, calorie burning calculations
- `AdminService`: Recommendations, constraints, user management

### 3. Data Access Layer (Repositories)

**Purpose**: Abstract database operations and provide clean data access interface

**Responsibilities**:
- Execute SQL queries
- Map database rows to data models
- Handle database connections
- Provide CRUD operations
- Return dataclass instances or dictionaries

**Key Principles**:
-  NO business logic
-  NO UI code
-  One repository per entity
-  Returns data models or dicts

### 4. Data Layer (Database)

**Purpose**: Persist application data

**Database**: SQLite (laihdutanyt.db)

**Tables**:
- `user`: User accounts and profiles
- `admin`: Administrator accounts
- `food`: Food catalog
- `activity`: Activity catalog
- `foodlog`: User food entries
- `activitylog`: User activity entries
- `recommendation`: Admin recommendations
- `user_constraint`: User health constraints

##  Component Diagram (Mermaid)

```mermaid
graph TB
    subgraph "Presentation Layer"
        LoginView[Login View]
        MainMenu[Main Menu View]
        FoodView[Food Dashboard]
        ActivityView[Activity Dashboard]
        FoodTotalsView[Food Totals View]
        ActivityTotalsView[Activity Totals View]
        AdminView[Admin Panel]
        LogsView[Logs Viewer]
    end
    
    subgraph "Business Logic Layer"
        UserService[User Service]
        FoodService[Food Service]
        ActivityService[Activity Service]
        AdminService[Admin Service]
    end
    
    subgraph "Data Access Layer"
        UserRepo[User Repository]
        FoodRepo[Food Repository]
        ActivityRepo[Activity Repository]
        FoodLogRepo[FoodLog Repository]
        ActivityLogRepo[ActivityLog Repository]
        AdminRepo[Admin Repository]
    end
    
    subgraph "Data Layer"
        DB[(SQLite Database)]
    end
    
    %% UI to Services
    LoginView --> UserService
    LoginView --> AdminService
    MainMenu --> UserService
    FoodView --> FoodService
    ActivityView --> ActivityService
    FoodTotalsView --> FoodService
    ActivityTotalsView --> ActivityService
    AdminView --> AdminService
    LogsView --> FoodService
    LogsView --> ActivityService
    
    %% Services to Repositories
    UserService --> UserRepo
    FoodService --> FoodRepo
    FoodService --> FoodLogRepo
    ActivityService --> ActivityRepo
    ActivityService --> ActivityLogRepo
    AdminService --> AdminRepo
    AdminService --> UserRepo
    
    %% Repositories to Database
    UserRepo --> DB
    FoodRepo --> DB
    ActivityRepo --> DB
    FoodLogRepo --> DB
    ActivityLogRepo --> DB
    AdminRepo --> DB
    
    style LoginView fill:#90caf9
    style MainMenu fill:#90caf9
    style FoodView fill:#90caf9
    style ActivityView fill:#90caf9
    style FoodTotalsView fill:#90caf9
    style ActivityTotalsView fill:#90caf9
    style AdminView fill:#ff9800
    style LogsView fill:#90caf9
    
    style UserService fill:#4caf50
    style FoodService fill:#4caf50
    style ActivityService fill:#4caf50
    style AdminService fill:#ff9800
    
    style UserRepo fill:#9c27b0
    style FoodRepo fill:#9c27b0
    style ActivityRepo fill:#9c27b0
    style FoodLogRepo fill:#9c27b0
    style ActivityLogRepo fill:#9c27b0
    style AdminRepo fill:#9c27b0
    
    style DB fill:#f44336
```

##  Data Flow Example: User Logs Food

```mermaid
sequenceDiagram
    participant User
    participant FoodView
    participant FoodService
    participant FoodRepo
    participant FoodLogRepo
    participant Database
    
    User->>FoodView: Select food, enter portion
    FoodView->>FoodView: Validate input (UI level)
    FoodView->>FoodService: log_food(user_id, food_selection, portion, date)
    FoodService->>FoodService: Parse food_id from selection
    FoodService->>FoodService: Validate portion > 0
    FoodService->>FoodLogRepo: create_log(user_id, food_id, date, portion)
    FoodLogRepo->>Database: INSERT INTO foodlog
    Database-->>FoodLogRepo: Success
    FoodLogRepo-->>FoodService: Log entry created
    FoodService-->>FoodView: Success
    FoodView->>FoodView: Refresh log display
    FoodView->>User: Show "Food logged!" message
```

##  Class Diagram (Simplified)

```mermaid
classDiagram
    class App {
        -user_service: UserService
        -food_service: FoodService
        -activity_service: ActivityService
        -admin_service: AdminService
        +__init__(db_path)
        +run()
    }
    
    class UserService {
        -user_repo: UserRepository
        +authenticate_user(username, password)
        +register_user(username, password, **data)
        +get_user_summary(username)
    }
    
    class FoodService {
        -food_repo: FoodRepository
        -foodlog_repo: FoodLogRepository
        +get_all_foods()
        +log_food(user_id, food, portion, date)
        +get_daily_totals(user_id)
    }
    
    class ActivityService {
        -activity_repo: ActivityRepository
        -activitylog_repo: ActivityLogRepository
        +get_all_activities()
        +log_activity(user_id, activity, count, date)
        +get_daily_totals(user_id)
    }
    
    class AdminService {
        -admin_repo: AdminRepository
        -user_repo: UserRepository
        +authenticate_admin(username, password)
        +create_recommendation(username, details)
        +add_constraint(username, constraint)
    }
    
    class UserRepository {
        -db_path: str
        +find_by_username(username)
        +create_user(username, password, **data)
        +authenticate(username, password)
    }
    
    class FoodRepository {
        -db_path: str
        +find_all()
        +find_by_id(food_id)
    }
    
    class FoodLogRepository {
        -db_path: str
        +create_log(user_id, food_id, date, portion)
        +find_by_user_and_date(user_id, date)
        +find_all_for_user(user_id)
    }
    
    App --> UserService
    App --> FoodService
    App --> ActivityService
    App --> AdminService
    
    UserService --> UserRepository
    FoodService --> FoodRepository
    FoodService --> FoodLogRepository
    ActivityService --> ActivityRepository
    ActivityService --> ActivityLogRepository
    AdminService --> AdminRepository
    AdminService --> UserRepository
```

##  Design Patterns Used

### 1. **Layered Architecture**
- Clear separation between UI, business logic, and data access
- Each layer depends only on the layer below it
- Changes in one layer don't affect others

### 2. **Repository Pattern**
- Abstracts data access logic
- Provides collection-like interface for data entities
- Makes it easy to swap database implementation

### 3. **Service Layer Pattern**
- Encapsulates business logic
- Coordinates between multiple repositories
- Provides clean API for UI layer

### 4. **Model-View Pattern** (simplified MVC)
- Models: Dataclasses in `repositories/models.py`
- Views: UI components in `ui/views/`
- Implicit controller: Service layer coordinates operations

### 5. **Dependency Injection**
- Services receive db_path in constructor
- Easy to test with mock databases
- Clear dependencies

## 🔧 Benefits of This Architecture

### Maintainability
-  Each module has single responsibility
-  Easy to locate code (login logic → login_view.py)
-  Changes are isolated

### Testability
-  Business logic separated from UI
-  Services can be tested without UI
-  Repositories can use test database

### Scalability
-  Easy to add new features (new service/view)
-  Can replace UI framework (tkinter → Qt/web)
-  Can replace database (SQLite → PostgreSQL)

### Collaboration
-  Multiple developers can work on different layers
-  Clear interfaces between components
-  Less merge conflicts

### Reusability
-  Services can be used by different UIs (desktop, web, mobile)
-  Repositories abstract database details
-  UI components can be reused

##  Migration Plan

### Phase 1: Service Layer (Current)
 Create service classes
 Move business logic from UI to services
 Services use existing repositories

### Phase 2: UI Refactoring (Next)
 Extract views from monolithic file
 Create separate view modules
 Update views to use services

### Phase 3: Component Extraction (Future)
 Extract reusable UI components
 Create component library
 Standardize UI patterns

### Phase 4: Testing (Future)
 Unit tests for services
 Integration tests for repositories
 UI tests for views

##  Coding Guidelines

### Service Layer
```python
#  Good: Clean service method
def log_food(self, user_id: str, food_selection: str, portion_g: float, date_str: str):
    food_id = self._parse_food_id(food_selection)
    self._validate_portion(portion_g)
    return self.foodlog_repo.create_log(user_id, food_id, date_str, portion_g)

#  Bad: Service with UI code
def log_food(self):
    food = self.food_dropdown.get()  # UI dependency!
    messagebox.showinfo("Success", "Logged!")  # UI code!
```

### UI Layer
```python
#  Good: UI delegates to service
def _on_log_food(self):
    try:
        self.food_service.log_food(self.user_id, selection, portion, date)
        messagebox.showinfo("Success", "Food logged!")
        self.refresh_display()
    except ValueError as e:
        messagebox.showerror("Error", str(e))

#  Bad: UI contains business logic
def _on_log_food(self):
    food_id = self.selection.split("|")[1]  # Business logic!
    if portion <= 0:  # Validation logic!
        return
    # Direct database access!
    conn = sqlite3.connect(self.db_path)
    ...
```

### Repository Layer
```python
#  Good: Clean data access
def find_by_username(self, username: str) -> Optional[User]:
    with self._conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM user WHERE username = ?", (username,))
        row = cur.fetchone()
        return self._row_to_user(row) if row else None

#  Bad: Repository with business logic
def find_and_validate_user(self, username: str, password: str):  # Too much logic!
    user = self.find_by_username(username)
    if user and self._check_password(password):  # Validation logic!
        return user
```

##  References

- [Martin Fowler - Service Layer](https://martinfowler.com/eaaCatalog/serviceLayer.html)
- [Repository Pattern](https://martinfowler.com/eaaCatalog/repository.html)
- [Layered Architecture](https://en.wikipedia.org/wiki/Multitier_architecture)

---

**Document Version**: 1.0  
**Last Updated**: December 9, 2025  
**Author**: In co-operation with Claude 4.5 AI
