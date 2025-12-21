"""
Database migration: Add weightlog table and enhance statistics table
Version: 2.1.0
Date: 2025-12-20

This migration adds:
1. weightlog table for tracking weight measurements
2. Additional columns to statistics table for nutrients
3. Indexes for performance
"""

import sqlite3
import os

def migrate_database(db_path: str):
    """Apply migration to add weightlog and enhance statistics"""
    
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        
        print("Starting database migration to v2.1...")
        
        # Check if weightlog table exists
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='weightlog'")
        if not cur.fetchone():
            print("  Creating weightlog table...")
            cur.execute("""
                CREATE TABLE weightlog (
                    log_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    date TEXT NOT NULL,
                    weight REAL NOT NULL,
                    notes TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES "user"(user_id) ON DELETE CASCADE
                )
            """)
            
            # Create index for weightlog
            cur.execute("""
                CREATE INDEX idx_weightlog_user_date 
                ON weightlog(user_id, date DESC)
            """)
            print("  ✓ weightlog table created")
        else:
            print("  ✓ weightlog table already exists")
        
        # Check and add columns to statistics table if they don't exist
        cur.execute("PRAGMA table_info(statistics)")
        existing_columns = {row[1] for row in cur.fetchall()}
        
        new_columns = {
            'total_kcal_burned': 'REAL DEFAULT 0.0',
            'net_kcal': 'REAL DEFAULT 0.0',
            'total_carbs_g': 'REAL DEFAULT 0.0',
            'total_protein_g': 'REAL DEFAULT 0.0',
            'total_fat_g': 'REAL DEFAULT 0.0',
            'food_entries_count': 'INTEGER DEFAULT 0',
            'activity_entries_count': 'INTEGER DEFAULT 0'
        }
        
        for col_name, col_type in new_columns.items():
            if col_name not in existing_columns:
                print(f"  Adding column {col_name} to statistics...")
                cur.execute(f"ALTER TABLE statistics ADD COLUMN {col_name} {col_type}")
                print(f"  ✓ Column {col_name} added")
            else:
                print(f"  ✓ Column {col_name} already exists")
        
        # Create unique index on statistics if it doesn't exist
        cur.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_statistics_user_date'")
        if not cur.fetchone():
            print("  Creating index on statistics...")
            try:
                cur.execute("""
                    CREATE UNIQUE INDEX idx_statistics_user_date 
                    ON statistics(user_id, date)
                """)
                print("  ✓ Index idx_statistics_user_date created")
            except sqlite3.IntegrityError:
                print("  ! Warning: Duplicate entries exist, skipping unique index")
        else:
            print("  ✓ Index idx_statistics_user_date already exists")
        
        conn.commit()
        print("✓ Migration completed successfully!")
        
    except Exception as e:
        conn.rollback()
        print(f"✗ Migration failed: {e}")
        raise
    finally:
        conn.close()

def verify_migration(db_path: str):
    """Verify that migration was successful"""
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        
        print("\nVerifying migration...")
        
        # Check weightlog table
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='weightlog'")
        assert cur.fetchone(), "weightlog table not found"
        print("  ✓ weightlog table exists")
        
        # Check statistics columns
        cur.execute("PRAGMA table_info(statistics)")
        columns = {row[1] for row in cur.fetchall()}
        
        required_columns = {
            'total_kcal_burned', 'net_kcal', 
            'total_carbs_g', 'total_protein_g', 'total_fat_g',
            'food_entries_count', 'activity_entries_count'
        }
        
        for col in required_columns:
            assert col in columns, f"Column {col} not found in statistics"
        print(f"  ✓ All {len(required_columns)} new columns exist in statistics")
        
        print("✓ Migration verification passed!")
        
    finally:
        conn.close()

if __name__ == "__main__":
    # Get database path
    DB_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
    DB_PATH = os.path.join(DB_DIR, "laihdutanyt.db")
    
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}")
        print("Please run create_db.py first")
        exit(1)
    
    # Run migration
    migrate_database(DB_PATH)
    
    # Verify
    verify_migration(DB_PATH)
    
    print("\n✓ Database is ready for v2.1!")
