# week4: modifioitu generoitu koodi alkaa
"""
import_activities.py path/to/sample_activities.csv
CSV import tool to add activities into the SQLite 'activity' table.
CSV format (header):
name,calories_per_activity,
"""
import csv
import os
import sys
import uuid
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "laihdutanyt.db")

def import_csv(csv_path: str, db_path: str = DB_PATH):
    if not os.path.exists(csv_path):
        print("CSV file not found:", csv_path)
        return
    if not os.path.exists(db_path):
        print("Database not found:", db_path, "create_db.py first.")
        return

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    inserted = 0
    with open(csv_path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            name = row.get("name")
            try:
                # Support both old and new CSV formats
                calories = float(row.get("calories_per_activity") or row.get("kcal_per_unit") or 0.0)
            except ValueError:
                print("Skipping invalid row:", row)
                continue

            activity_id = str(uuid.uuid4())
            # Use correct column name: kcal_per_unit (not calories_per_activity)
            cur.execute("""
                INSERT INTO activity (activity_id, name, kcal_per_unit)
                VALUES (?, ?, ?)
            """, (activity_id, name, calories))
            inserted += 1

    conn.commit()
    conn.close()
    print(f"Imported {inserted} activities into {db_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: import_activities.py sample_activities.csv")
        sys.exit(1)
    import_csv(sys.argv[1])
# week4: modifioitu generoitu koodi loppuu
