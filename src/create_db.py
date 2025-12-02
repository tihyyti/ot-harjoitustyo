
# Week 5: Refactoroitu, aiemmin generoitu koodi alkaa
# New fields in user table and sample activity data insertion
"""
Create SQLite database and insert test data for laihdutanyt app.
python3 create_db.py
This script creates schema and inserts a test user and test admin and one example food.
"""
import os
import sqlite3
import uuid
import hashlib

DB_DIR = os.path.join(os.path.dirname(__file__), "data")
DB_PATH = os.path.join(DB_DIR, "laihdutanyt.db")

SCHEMA = """
PRAGMA foreign_keys = ON;

-- USER
CREATE TABLE IF NOT EXISTS "user" (
    user_id TEXT PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    salt TEXT NOT NULL,
    weight REAL,
    length REAL,
    age INTEGER,
    activity_level INTEGER,
    allergies TEXT,
    kcal_min REAL,
    kcal_max REAL,
    weight_loss_target REAL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- ADMIN (separate table for admin accounts)
CREATE TABLE IF NOT EXISTS admin (
    admin_id TEXT PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT NOT NULL,
    salt TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- FOOD
CREATE TABLE IF NOT EXISTS food (
    food_id TEXT PRIMARY KEY,
    name TEXT,
    kcal_per_portion REAL,
    carbs_per_portion REAL,
    protein_per_portion REAL,
    fat_per_portion REAL
);

-- FOODLOG
CREATE TABLE IF NOT EXISTS foodlog (
    log_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    food_id TEXT NOT NULL,
    date TEXT NOT NULL,
    portion_size_g REAL,
    FOREIGN KEY(user_id) REFERENCES "user"(user_id) ON DELETE CASCADE,
    FOREIGN KEY(food_id) REFERENCES food(food_id) ON DELETE SET NULL
);

-- ACTIVITY (catalog)
CREATE TABLE IF NOT EXISTS activity (
    activity_id TEXT PRIMARY KEY,
    name TEXT,
    unit TEXT,
    kcal_per_unit REAL
);

-- ACTIVITYLOG
CREATE TABLE IF NOT EXISTS activitylog (
    log_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    activity_id TEXT NOT NULL,
    date TEXT NOT NULL,
    activity_count REAL,
    kcal_burned REAL,
    FOREIGN KEY(user_id) REFERENCES "user"(user_id) ON DELETE CASCADE,
    FOREIGN KEY(activity_id) REFERENCES activity(activity_id) ON DELETE SET NULL
);

-- STATISTICS (aggregated)
CREATE TABLE IF NOT EXISTS statistics (
    stats_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    date TEXT NOT NULL,
    total_kcal_consumed REAL,
    total_weight REAL,
    weight_change REAL,
    FOREIGN KEY(user_id) REFERENCES "user"(user_id) ON DELETE CASCADE
);
"""

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def _hash_password(password: str, salt: bytes, iterations: int = 100_000) -> str:
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return dk.hex()

def create_db(path: str = DB_PATH, insert_test: bool = True):
    ensure_dir(os.path.dirname(path))
    conn = sqlite3.connect(path)
    try:
        cur = conn.cursor()
        cur.executescript(SCHEMA)
        conn.commit()
        print(f"Database created/updated at: {path}")

        if insert_test:
            # Insert demo admin and demo user if not exists, and one example food
            # test credentials:
            test_username = "user"
            test_password = "pass"
            test_admin = "admin"
            test_admin_pw = "apass"

            # Check and insert test user
            cur.execute('SELECT 1 FROM "user" WHERE username = ?', (test_username,))
            if not cur.fetchone():
                user_id = str(uuid.uuid4())
                salt = os.urandom(16)
                pwd_hash = _hash_password(test_password, salt)
                cur.execute("""
                    INSERT INTO "user" (
                        user_id, username, password_hash, salt, weight, length, age, activity_level, allergies, kcal_min, kcal_max, weight_loss_target
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)
                """, (user_id, test_username, pwd_hash, salt.hex(), 80.0, 175.0, 35, 2, "Citrus", 1500, 2500, 5))
                print(f"Inserted test user: username='{test_username}', password='{test_password}'")

            # Check and insert test admin
            cur.execute("SELECT 1 FROM admin WHERE username = ?", (test_admin,))
            if not cur.fetchone():
                admin_id = str(uuid.uuid4())
                salt = os.urandom(16)
                pwd_hash = _hash_password(test_admin_pw, salt)
                cur.execute("""
                    INSERT INTO admin (admin_id, username, password_hash, salt)
                    VALUES (?, ?, ?, ?)
                """, (admin_id, test_admin, pwd_hash, salt.hex()))
                print(f"Inserted test admin: username='{test_admin}', password='{test_admin_pw}'")

            # Insert a sample food row
            cur.execute("SELECT 1 FROM food WHERE name = ?", ("Apple",))
            if not cur.fetchone():
                food_id = str(uuid.uuid4())
                cur.execute("""
                    INSERT INTO food (food_id, name, kcal_per_portion, carbs_per_portion, protein_per_portion, fat_per_portion)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (food_id, "Apple", 52.0, 14.0, 0.3, 0.2))
                print("Inserted sample food: Apple")
                
            # Insert a sample activity row
            cur.execute("SELECT 1 FROM activity WHERE name = ?", ("walking",))
            if not cur.fetchone():
                activity_id = str(uuid.uuid4())
                cur.execute("""
                    INSERT INTO activity (activity_id, name, kcal_per_unit)
                    VALUES (?, ?, ?)
                """, (activity_id, "walking", 30.0))
                print("Inserted sample activity: walking")

            conn.commit()
    finally:
        conn.close()

if __name__ == "__main__":
    create_db()
    
# Refactoroitu, aiemmin generoitu koodi päättyy