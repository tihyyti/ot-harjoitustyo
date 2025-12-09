# Generoitu koodi alkaa
"""
scripts/aggregate_totals.py
CLI: Print aggregated daily totals (calories) for a user.
Usage:
    python3 scripts/aggregate_totals.py username [--db path_to_db]

Example:
    python3 scripts/aggregate_totals.py demo
"""
import sqlite3
import os
import sys
import argparse
from typing import Optional

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DEFAULT_DB = os.path.join(BASE_DIR, "data", "laihdutanyt.db")

def find_user_id(conn: sqlite3.Connection, username: str) -> Optional[str]:
    cur = conn.cursor()
    cur.execute('SELECT user_id FROM "user" WHERE username = ?', (username,))
    row = cur.fetchone()
    return row[0] if row else None

def aggregate_daily_foods_totals(conn: sqlite3.Connection, user_id: str):
    """
    Aggregates calories per date for given user_id.
    Calculation: total_calories = sum( (portion_size_g / 100.0) * calories_per_portion )
    """
    cur = conn.cursor()
    cur.execute("""
        SELECT fl.date AS date,
               SUM( (fl.portion_size_g / 100.0) * COALESCE(f.kcal_per_portion, 0.0) ) AS total_calories,
               COUNT(*) AS entries
        FROM foodlog fl
        LEFT JOIN food f ON fl.food_id = f.food_id
        WHERE fl.user_id = ?
        GROUP BY fl.date
        ORDER BY fl.date DESC
    """, (user_id,))
    return cur.fetchall()

def main(argv=None):
    parser = argparse.ArgumentParser(description="\nAggregate daily calorie totals for a user")
    parser.add_argument("username", help="username (e.g. demo)")
    parser.add_argument("--db", help="path to SQLite DB", default=DEFAULT_DB)
    args = parser.parse_args(argv)

    if not os.path.exists(args.db):
        print(f"Database not found: {args.db}\nRun create_db.py first.")
        sys.exit(1)

    conn = sqlite3.connect(args.db)
    try:
        user_id = find_user_id(conn, args.username)
        if not user_id:
            print(f"User not found: {args.username}")
            sys.exit(1)
        rows = aggregate_daily_totals(conn, user_id)
        if not rows:
            print(f"No food logs for user '{args.username}'.")
            return
        print(f"Daily totals for user '{args.username}':")
        print("{:12s}  {:10s}  {:8s}".format("\nDate", "Calories (kcal)", "Entries"))
        print("-" * 38)
        for date, total_calories, entries in rows:
            print(f"{date:12s}  {total_calories:10.1f}  {entries:8d}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
    # Generoitu koodi päättyy