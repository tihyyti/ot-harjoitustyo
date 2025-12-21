# Laihdutanyt Application - New Features

## What's New in Release Version 2.1

## Main improvements

Added time dimension to UI for clarity - users see past vs. future at a glance.
Admin system enables improved coaching workflows.
Constraint management ensures safe recommendations.
AI-ready architecture supports future machine learning features.
Intuitive, adaptive "cards-based UI" with a consistent color usage.

**The application is now a versatile diet/fitness management system 
suitable for both personal use and coaching!**

### 1. Time Dimension Feature 
**Current Date Highlighting in Dashboards**

The Daily Food Totals and Daily Activity Totals dashboards now intelligently highlight dates:

- **Past dates** (white background): Historical data you've already logged
- **TODAY** (yellow highlight with bold text): Current day's data stands out clearly
- **PLANNED** (light green background): Future meal and activity plans

This creates a clear visual split between:
1. **Historical Facts**: What user have actually eaten and done.
2. **Future Plans**: User's diet and activity schedule going forward.

**Functionality:**
- Each row in the Daily Totals view is automatically colored based on its date
- Today's row is always highlighted in yellow with bold font
- Future plans appear in a light green color
- Makes it easy to distinguish past performance from future goals.

### 2. Admin Panel
**Administrative Interface**

An admin system for diet/fitness coaching:

#### Login System:
- **User Login** button (blue): For regular users
- **Admin Login** button (orange): For administrators/coaches
- Test admin credentials: username=`admin`, password=`apass`

#### Admin Dashboard Features:

**Tab 1: User Management**
- View all registered users in a sortable table
- See user details: weight, targets, calorie goals, activity levels, allergies
- Access to user progress tracking
- Refresh button to update user list

**Tab 2: Recommendations**
- Create personalized diet/exercise recommendations for users
- Recommendation types:
  - Diet Plan
  - Exercise Plan
  - Combined Plan
  - Weight Loss Methods
  - Maintenance Plan
- Custom calorie targets (min/max)
- Suggested activities text area
- Notes field for detailed instructions
- Recommendations are saved to database and linked to specific users

**Tab 3: Constraints & Health**
- Track user health constraints and limitations
- Constraint types:
  - Allergies
  - Disabilities
  - Medical Conditions
  - Dietary Restrictions
  - Injuries
- Severity levels: Low, Moderate, High, Critical
- Essential for future AI-aware meal planning and activity recommendations
- Ensures recommendations respect user limitations

**Tab 4: AI Trainer**
- Placeholder for future AI integration
- Examples of planned features:
  - Automated meal plan generation
  - Smart exercise recommendations
  - Predictive weight loss trajectory
  - Coaching in natural language
  - Constraint-aware planning
  - Progress tracking with adaptive goals
  - External links integration e.g.:
    - https://www.ruokavirasto.fi/elintarvikkeet/terveytta-edistava-ruokavalio/ravitsemus--ja-ruokasuositukset/

- Ready for custom AI models.

### 3. Database Enhancements

**New Tables:**

-- Recommendations table
CREATE TABLE recommendation (
    recommendation_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    admin_id TEXT,
    recommendation_type TEXT,
    title TEXT,
    description TEXT,
    target_kcal_min REAL,
    target_kcal_max REAL,
    suggested_activities TEXT,
    notes TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'active',
    FOREIGN KEY(user_id) REFERENCES user(user_id),
    FOREIGN KEY(admin_id) REFERENCES admin(admin_id)
);

-- User constraints table
CREATE TABLE user_constraint (
    constraint_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    constraint_type TEXT,
    description TEXT,
    severity TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES user(user_id)
);

**New Repository:**
- `AdminRepository` in `repositories/admin_repository.py`
- Handles admin authentication and management
- Password hashing with PBKDF2-HMAC-SHA256

### 4. UI/UX Improvements

**Visual Enhancements:**
- Date indicators: today and planned
- Color-coded admin panel
- Tab-based admin interface
- Consistent Arial font sizing
- Improved color scheme:
  - Admin header: Orange (#ff9800)
  - Past data: White
  - Current day: Yellow (#ffffcc)
  - Future plans: Light green (#e8f5e9)

**Navigation:**
- Separate login buttons for users and admins
- Admin logout returns to login screen
- Breadcrumb-style navigation in admin panel

### 5. Innovations

**Why These Features Are Innovative:**

1. **Time-Aware UI**: Automatically distinguishes historical data from future plans without user intervention

2. **Dual-Mode System**: Single application serves both end-users (dieters) and coaches/admins.

3. **Constraint Management**: Proactive health consideration - tracks allergies and disabilities for safe recommendations

4. **AI-Ready Architecture**: Pre-built structure for future machine learning integration e.g. for:
   - Constraint-aware recommendations
   - Historical data aggregation for ML training
   - Placeholder for NLP coaching interface

5. **Coaching Tools**: Enables dietitians/trainers to manage multiple clients from one interface.

##6.Future Enhancements

6. **Next Steps for AI Integration:**

- Connect to some AI-provider API to get recommendations in natural language.
- Implement TensorFlow model for weight prediction
- Add automated meal plan generator
- Create activity suggestion engine
- Build progress visualization charts
- Add user notification system for admin recommendations

## 7. Technical Details## How to Use

### As a User

1. Click "User Login" button
2. Login with your credentials (test: user/pass)
3. Use dashboards as before
4. Notice today's date highlighted in yellow in totals view
5. Add future dates for meal planning. They appear in green.

### As an Admin

1. Click "Admin Login" button
2. Login with admin credentials (admin/apass)
3. Explore the 4 tabs:
   - Manage users
   - Create recommendations
   - Track health constraints
   - Preview of future AI features
4. Click "Logout" to return to login screen

**Files Modified:**
- `Laihdutanyt_v2.py`: Main application (+450 lines of admin code)
- `create_db.py`: Added recommendation and constraint tables
- `models.py`: No changes needed (using dict-based queries)

**Files Added:**
- `repositories/admin_repository.py`: Admin authentication and management

**Dependencies:**
- No new external dependencies
- Uses built-in tkinter, ttk, sqlite3, hashlib, uuid

