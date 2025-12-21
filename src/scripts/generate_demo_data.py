"""
Generate realistic 30-day demo data for testing
Version: 2.1.0
Date: 2025-12-20

Generates:
- Daily food logs (2-4 meals per day)
- Daily activity logs (1-2 activities)
- Weekly weight logs (showing gradual weight loss)
- Daily statistics records
"""

import sqlite3
import uuid
import os
from datetime import date, timedelta
import random

DB_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
DB_PATH = os.path.join(DB_DIR, "laihdutanyt.db")

# Sample meals with realistic portions
BREAKFAST_OPTIONS = [
    ('Boiled Egg', 100),
    ('Banana', 120),
    ('Greek Yogurt', 150),
    ('Whole Wheat Bread (slice)', 30),
]

LUNCH_OPTIONS = [
    ('Chicken Breast', 150),
    ('Rice (cooked)', 200),
    ('Broccoli', 100),
    ('Salmon (100g)', 120),
]

DINNER_OPTIONS = [
    ('Chicken Breast', 180),
    ('Rice (cooked)', 150),
    ('Broccoli', 120),
    ('Salmon (100g)', 150),
]

SNACK_OPTIONS = [
    ('Apple', 150),
    ('Banana', 120),
    ('Almonds (30g)', 30),
    ('Greek Yogurt', 100),
]

ACTIVITY_OPTIONS = [
    ('Walking', 5000),   # 5000 steps
    ('Running', 3000),   # 3000 steps
    ('Cycling', 30),     # 30 minutes
    ('Weight Training', 45),  # 45 minutes
]

def get_user_id(conn):
    """Get test user ID"""
    cur = conn.cursor()
    cur.execute('SELECT user_id FROM "user" WHERE username = ?', ('user',))
    row = cur.fetchone()
    if not row:
        raise Exception("Test user 'user' not found. Run create_db.py first.")
    return row[0]

def get_food_id(conn, food_name):
    """Get food ID by name"""
    cur = conn.cursor()
    cur.execute('SELECT food_id FROM food WHERE name = ?', (food_name,))
    row = cur.fetchone()
    return row[0] if row else None

def get_activity_id(conn, activity_name):
    """Get activity ID by name"""
    cur = conn.cursor()
    cur.execute('SELECT activity_id FROM activity WHERE name = ?', (activity_name,))
    row = cur.fetchone()
    return row[0] if row else None

def get_food_details(conn, food_id):
    """Get food nutritional details"""
    cur = conn.cursor()
    cur.execute('''
        SELECT kcal_per_portion, carbs_per_portion, protein_per_portion, fat_per_portion
        FROM food WHERE food_id = ?
    ''', (food_id,))
    return cur.fetchone()

def get_activity_details(conn, activity_id):
    """Get activity calorie details"""
    cur = conn.cursor()
    cur.execute('SELECT kcal_per_unit FROM activity WHERE activity_id = ?', (activity_id,))
    row = cur.fetchone()
    return row[0] if row else 0.0

def log_food(conn, user_id, food_name, portion_g, date_str):
    """Log a food entry"""
    food_id = get_food_id(conn, food_name)
    if not food_id:
        print(f"  ! Warning: Food '{food_name}' not found, skipping")
        return None
    
    log_id = str(uuid.uuid4())
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO foodlog (log_id, user_id, food_id, date, portion_size_g)
        VALUES (?, ?, ?, ?, ?)
    ''', (log_id, user_id, food_id, date_str, portion_g))
    
    return {
        'food_id': food_id,
        'portion_g': portion_g
    }

def log_activity(conn, user_id, activity_name, count, date_str):
    """Log an activity entry"""
    activity_id = get_activity_id(conn, activity_name)
    if not activity_id:
        print(f"  ! Warning: Activity '{activity_name}' not found, skipping")
        return None
    
    # Calculate calories burned
    kcal_per_unit = get_activity_details(conn, activity_id)
    kcal_burned = (count / 1000.0) * kcal_per_unit
    
    log_id = str(uuid.uuid4())
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO activitylog (log_id, user_id, activity_id, date, activity_count, kcal_burned)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (log_id, user_id, activity_id, date_str, count, kcal_burned))
    
    return kcal_burned

def log_weight(conn, user_id, weight, date_str, notes=""):
    """Log a weight measurement"""
    log_id = str(uuid.uuid4())
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO weightlog (log_id, user_id, date, weight, notes)
        VALUES (?, ?, ?, ?, ?)
    ''', (log_id, user_id, date_str, weight, notes))

def calculate_daily_stats(conn, user_id, date_str):
    """Calculate and store daily statistics"""
    cur = conn.cursor()
    
    # Calculate food stats
    cur.execute('''
        SELECT 
            SUM((fl.portion_size_g / 100.0) * f.kcal_per_portion) as total_kcal,
            SUM((fl.portion_size_g / 100.0) * f.carbs_per_portion) as total_carbs,
            SUM((fl.portion_size_g / 100.0) * f.protein_per_portion) as total_protein,
            SUM((fl.portion_size_g / 100.0) * f.fat_per_portion) as total_fat,
            COUNT(*) as food_count
        FROM foodlog fl
        JOIN food f ON fl.food_id = f.food_id
        WHERE fl.user_id = ? AND fl.date = ?
    ''', (user_id, date_str))
    
    food_stats = cur.fetchone()
    total_kcal_consumed = food_stats[0] or 0.0
    total_carbs = food_stats[1] or 0.0
    total_protein = food_stats[2] or 0.0
    total_fat = food_stats[3] or 0.0
    food_count = food_stats[4] or 0
    
    # Calculate activity stats
    cur.execute('''
        SELECT SUM(kcal_burned), COUNT(*)
        FROM activitylog
        WHERE user_id = ? AND date = ?
    ''', (user_id, date_str))
    
    activity_stats = cur.fetchone()
    total_kcal_burned = activity_stats[0] or 0.0
    activity_count = activity_stats[1] or 0
    
    # Calculate net calories
    net_kcal = total_kcal_consumed - total_kcal_burned
    
    # Insert or update statistics
    stats_id = str(uuid.uuid4())
    cur.execute('''
        INSERT OR REPLACE INTO statistics 
        (stats_id, user_id, date, total_kcal_consumed, total_kcal_burned, net_kcal,
         total_carbs_g, total_protein_g, total_fat_g, 
         food_entries_count, activity_entries_count)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (stats_id, user_id, date_str, total_kcal_consumed, total_kcal_burned, net_kcal,
          total_carbs, total_protein, total_fat, food_count, activity_count))

def generate_demo_data():
    """Generate 30 days of realistic demo data"""
    
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}")
        print("Please run create_db.py first")
        return
    
    conn = sqlite3.connect(DB_PATH)
    try:
        user_id = get_user_id(conn)
        print(f"Generating 30-day demo data for user: {user_id}")
        
        # Starting weight and target weight loss
        current_weight = 80.0  # kg
        weekly_weight_loss = 0.5  # kg per week
        daily_weight_loss = weekly_weight_loss / 7
        
        # Generate data for last 30 days
        today = date.today()
        
        for days_ago in range(30, -1, -1):
            current_date = today - timedelta(days=days_ago)
            date_str = current_date.isoformat()
            
            print(f"\nGenerating data for {date_str}...")
            
            # Breakfast (always)
            breakfast = random.choice(BREAKFAST_OPTIONS)
            log_food(conn, user_id, breakfast[0], breakfast[1], date_str)
            print(f"  + Breakfast: {breakfast[0]} ({breakfast[1]}g)")
            
            # Lunch (always)
            lunch_items = random.sample(LUNCH_OPTIONS, 2)
            for item, portion in lunch_items:
                log_food(conn, user_id, item, portion, date_str)
            print(f"  + Lunch: {lunch_items[0][0]}, {lunch_items[1][0]}")
            
            # Dinner (always)
            dinner_items = random.sample(DINNER_OPTIONS, 2)
            for item, portion in dinner_items:
                log_food(conn, user_id, item, portion, date_str)
            print(f"  + Dinner: {dinner_items[0][0]}, {dinner_items[1][0]}")
            
            # Snacks (70% of days)
            if random.random() < 0.7:
                snack = random.choice(SNACK_OPTIONS)
                log_food(conn, user_id, snack[0], snack[1], date_str)
                print(f"  + Snack: {snack[0]}")
            
            # Activities (80% of days, 1-2 activities)
            if random.random() < 0.8:
                num_activities = random.choice([1, 1, 2])  # More likely to do 1 activity
                activities = random.sample(ACTIVITY_OPTIONS, num_activities)
                for activity_name, count in activities:
                    kcal = log_activity(conn, user_id, activity_name, count, date_str)
                    if kcal:
                        print(f"  + Activity: {activity_name} ({count} units, {kcal:.1f} kcal)")
            
            # Log weight weekly (every 7 days)
            if days_ago % 7 == 0:
                current_weight -= (7 * daily_weight_loss)
                log_weight(conn, user_id, round(current_weight, 1), date_str, 
                          f"Week {30 - days_ago} measurement")
                print(f"  + Weight logged: {current_weight:.1f} kg")
            
            # Calculate and store daily statistics
            calculate_daily_stats(conn, user_id, date_str)
            print(f"  ✓ Daily statistics calculated")
        
        conn.commit()
        print("\n" + "="*50)
        print("✓ Demo data generation completed!")
        print("="*50)
        print(f"\nGenerated:")
        
        # Summary statistics
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM foodlog WHERE user_id = ?', (user_id,))
        food_count = cur.fetchone()[0]
        
        cur.execute('SELECT COUNT(*) FROM activitylog WHERE user_id = ?', (user_id,))
        activity_count = cur.fetchone()[0]
        
        cur.execute('SELECT COUNT(*) FROM weightlog WHERE user_id = ?', (user_id,))
        weight_count = cur.fetchone()[0]
        
        cur.execute('SELECT COUNT(*) FROM statistics WHERE user_id = ?', (user_id,))
        stats_count = cur.fetchone()[0]
        
        print(f"  - {food_count} food log entries")
        print(f"  - {activity_count} activity log entries")
        print(f"  - {weight_count} weight log entries")
        print(f"  - {stats_count} daily statistics records")
        
    except Exception as e:
        conn.rollback()
        print(f"\n✗ Error generating demo data: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    generate_demo_data()
