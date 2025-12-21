"""
Migration script to add dietary_period table for experimental period tracking.
This allows users to annotate time periods with dietary experiments/protocols.

Run with: poetry run python src/migrations/add_dietary_periods.py
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / 'data' / 'laihdutanyt.db'


def add_dietary_periods_table():
    """Add dietary_period table to database"""
    print("Adding dietary_period table...")
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Create dietary_period table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS dietary_period (
            period_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT,
            period_name TEXT NOT NULL,
            description TEXT,
            protocol_type TEXT,
            notes TEXT,
            is_active INTEGER DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES "user"(user_id) ON DELETE CASCADE
        )
    """)
    
    # Create index for efficient queries
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_dietary_period_user_dates 
        ON dietary_period(user_id, start_date, end_date)
    """)
    
    conn.commit()
    conn.close()
    
    print("✓ dietary_period table created successfully!")
    print("✓ Index created for efficient date range queries")


def verify_table():
    """Verify the table was created correctly"""
    print("\nVerifying table structure...")
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Check table exists
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='dietary_period'")
    if cur.fetchone():
        print("  ✓ dietary_period table exists")
    else:
        print("  ✗ dietary_period table NOT found")
        return False
    
    # Check columns
    cur.execute("PRAGMA table_info(dietary_period)")
    columns = [row[1] for row in cur.fetchall()]
    
    required_columns = [
        'period_id', 'user_id', 'start_date', 'end_date', 
        'period_name', 'description', 'protocol_type', 'notes',
        'is_active', 'created_at'
    ]
    
    for col in required_columns:
        if col in columns:
            print(f"  ✓ Column '{col}' exists")
        else:
            print(f"  ✗ Column '{col}' missing")
    
    conn.close()
    print("\n✓ Verification complete!")
    return True


if __name__ == '__main__':
    print("=" * 60)
    print("Adding Dietary Period Tracking")
    print("=" * 60)
    
    add_dietary_periods_table()
    verify_table()
    
    print("\n" + "=" * 60)
    print("✓ Migration complete!")
    print("=" * 60)
    print("\nExamples of period_name:")
    print("  - 'No Evening Eating After 7pm'")
    print("  - 'Weekend-Only Evening Meals'")
    print("  - 'Morning Emphasis Protocol'")
    print("  - 'Low-Carb Experiment'")
    print("  - 'Intermittent Fasting 16:8'")
