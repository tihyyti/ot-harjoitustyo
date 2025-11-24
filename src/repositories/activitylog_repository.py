# generoitu koodi alkaa
"""
activitylogRepository: SQLite-repos for food logs.
Methods:
- create_log(user_id, activity_id, date, activity_count, calories_burned)
- find_by_user_and_date(user_id, date)
- find_all_for_user(user_id)
"""
import sqlite3
import uuid
from typing import List, Dict, Optional


class ActivityLogRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def create_log(
        self,
        user_id: str,
        activity_id: str,
        date: str,
        activity_count: float,
        calories_burned: float,
    ) -> Dict:
        log_id = str(uuid.uuid4())
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO activitylog (log_id, user_id, activity_id, date, activity_count, calories_burned)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (log_id, user_id, activity_id, date, activity_count, calories_burned),
            )
            conn.commit()
        return self.find_by_id(log_id)

    def find_by_id(self, log_id: str) -> Optional[Dict]:
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM activitylog WHERE log_id = ?", (log_id,))
            row = cur.fetchone()
            return dict(row) if row else None

    def find_by_user_and_date(self, user_id: str, date: str) -> List[Dict]:
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT fl.*, f.name, f.calories_per_portion FROM activitylog fl JOIN food f ON fl.food_id = f.food_id WHERE fl.user_id = ? AND fl.date = ? ORDER BY fl.date",
                (user_id, date),
            )
            return [dict(r) for r in cur.fetchall()]

    def find_all_for_user(self, user_id: str) -> List[Dict]:
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT fl.*, f.name, f.calories_per_portion FROM activitylog fl JOIN food f ON fl.food_id = f.food_id WHERE fl.user_id = ? ORDER BY fl.date DESC",
                (user_id,),
            )
            return [dict(r) for r in cur.fetchall()]

        # generoitu koodi päättyy
