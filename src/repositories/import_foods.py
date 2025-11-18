# generoitu koodi alkaa
"""
import_foods.py path/to/sample_foods.csv
CSV import tool to add foods into the SQLite 'food' table.
CSV format (header):
name,calories_per_portion,carbs_per_portion,protein_per_portion,fat_per_portion
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
                calories = float(row.get("calories_per_portion") or 0.0)
                carbs = float(row.get("carbs_per_portion") or 0.0)
                protein = float(row.get("protein_per_portion") or 0.0)
                fat = float(row.get("fat_per_portion") or 0.0)
            except ValueError:
                print("Skipping invalid row:", row)
                continue

            food_id = str(uuid.uuid4())
            cur.execute("""
                INSERT INTO food (food_id, name, calories_per_portion, carbs_per_portion, protein_per_portion, fat_per_portion)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (food_id, name, calories, carbs, protein, fat))
            inserted += 1

    conn.commit()
    conn.close()
    print(f"Imported {inserted} foods into {db_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: import_foods.py sample_foods.csv")
        sys.exit(1)
    import_csv(sys.argv[1])
    # generoitu koodi päättyy