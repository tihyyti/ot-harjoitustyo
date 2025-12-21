
### ot-harjoitustyo

# Ohjelmistotekniikka, harjoitustyö

## Systeemikuvaukset:

**Laihdutanyt — Requirements Specification (v2)**

**Application Name:** laihdutanyt.

**Application overview:**  
UI is implemented by Tkinter/Python and database is SQLite. Application type is Desktop — no WEB UI is allowed.

**Functional overview:**  
The application requires a description and definition of a weekly weight loss program at a monthly level. 
The daily amount of calories from food and drink is recorded per portion and it is estimated based on the ingredients contained.
Snacks in particular are recorded in the memory for the purpose of making a change! Calorie consumption is estimated using e.g. some existing mobile phone and/or a wristwatch application that measures exercises (there are many of those on the market). The program compiles and displays statistics to enhance weight management, however, without sacrificing well-being.

The core functionality of the application can be also used to track the user's behavioral preferences to be able it 
to identify and prompt the user to give up some harmful habits, such as e.g. excessive snacking and evening eating. 
This extension however will be implemented only if there is enough excessive time for it.

**Functional Requirements Specification for Diet Program Application**

**1. Introduction**  
This document outlines the functional requirements for a diet program application designed for both users and administrators. 
The application will track calorie intake, consumption, weight loss, and user dietary constraints.

**2. User Stories**

**2.1 User Stories for main users:**  
- As a user, I want to log my daily food intake, so that I can track my calorie consumption.  
- As a user, I want to see my daily, weekly, and monthly calorie consumption and nutrient intake statistics to evaluate my dietary habits.  
- As a user, I want to set my calorie goals (minimum and maximum) to align my diet with my weight loss goals.  
- As a user, I want to record my allergies and dietary restrictions (e.g., lactose intolerance).  
- As a user, I want to achieve weekly and monthly weight loss targets to see my progress.

**2.2 User Stories for administrators: Future implementation**  
- As an admin, I want to manage user accounts, allowing me to add, deactivate, or modify user information.  
- As an admin, I want to manage dietary constraints, including creating, editing, and deleting guidelines regarding minimum and maximum calorie intakes.  
- As an admin, I want to generate reports that summarize user statistics and progress toward their weight loss goals.

**3. Functional Requirements**

**3.1 User Management**

**Registration/Login:**  
Users should register and log in to access their profiles.

**Profile Management:**  
Users can update personal information, including weight, length, age, activity level, allergies, kcal_min, kcal_max, 
weight_loss_target.

**3.2 Diet Tracking**  

**Food Intake Logging:**  
Users can log their daily food consumption.

Each food item must have the following attributes:
- Name
- Portion Size (in grams)
- Calories per portion
- Carbohydrates, Protein, Fat (in grams)

**3.3 Activity Tracking**  

**Activity Logging:**  
Users can log their daily activities.

Each food item must have the following attributes:
- Name
- Date, 
- Activity_count (as steps), 
- Calories_burned (kilo-calories consumed)

**3.4 Nutrient Tracking and Analysis**

**Daily Nutrient and Calorie Summary:**  
Users can view a breakdown of daily nutrient and calorie consumption. 
Summary of energy got from nutrients (total calories consumed from carbohydrates, proteins, and fats).

**Weekly/Monthly Reports:**  
Users can view weekly and monthly statistics of calorie consumption and nutrient intake. 
Users can view weight change over specified periods (weekly and monthly).

**3.5 Goals and Constraints**

Users can set:
- Calorie intake goals: Minimum and maximum calories (Daily)
- Calorie consumption goals: Minimum and maximum calories consumed (Daily)
- Weekly/Monthly weight-loss targets.

**3.6 Allergy Management**  
Users can input their allergies and dietary restrictions. 
The application should make food recommendations based on these preferences.

**4. Entities and Database Tables**

**Entity — Attributes:**  
- **User:** user_id (PRIMARY KEY), username, password, weight, height, age, activity_level, allergies, calorie_min, calorie_max, weight_loss_target  
- **Food:** food_id (PRIMARY KEY), name, calories_per_portion, carbs_per_portion, protein_per_portion, fat_per_portion  
- **FoodLog:** log_id (PRIMARY KEY), user_id (FOREIGN KEY), food_id (FOREIGN KEY), date, portion_size (grams)
- **ActivityLog:** log_id (PRIMARY KEY), user_id (FOREIGN KEY), activity_id (FOREIGN KEY), date, activity_count (as steps), activity_level (calories consumed)  
- **Statistics:** user_id (PRIMARY KEY), date, total_calories_consumed, total_weight, weight_change  
- **Admin:** admin_id (PRIMARY KEY), username, password

**5. User Interface (Tkinter)**

Done:
**Login Window:** For user registration and authentication.  
**Welcome Button-menu:** Dashboard Selection Buttons-menu.  
**Food Logging Dashboard:** Functions to add consumed food items and view their nutrient details.  
**Activity Logging Dashboard:** Functions to add activity-items and view their energy-consumption details. 
**View All Food Logs :** Functions to list and edit consumed food items and view their calories.  
**View All Activity Logs:** Functions to list and edit activities logged and view their calories burned.
**Weight logging:** Daily logging and weekly weight loss statistics.
**Dietary Periods and experimenting:** User can test different periodical diets and 
combine them for most suitable personal diet.

Pending:
**Statistics Screen:** Charts for weekly and monthly views of food-intake, activity and weight progress.  
**Admin Dashboard:** For managing user accounts, diet template mix, dietary constraints, and generating reports.

**6. Constraints**

**Daily Calorie Constraints:** User's dietary guide to minimum and maximum calorie intakes.  
**Weight-Loss Goals:** Users must reach their weekly and monthly weight-loss targets.  
**Allergy and Dietary Restrictions:** Food recommendations and constraints.


