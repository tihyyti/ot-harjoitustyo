# generoitu koodi alkaa
"""
FoodRepository; SQLite-repo for Food-entity.
Methods:
- find_all()
- find_by_name(name)
- find_by_id(food_id)
- create(food_dict)  # returns inserted row as dict
"""
import sqlite3
import uuid
from typing import List, Optional, Dict

class FoodRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def find_all(self) -> List[Dict]:
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM food ORDER BY name")
            return [dict(r) for r in cur.fetchall()]

    def find_by_name(self, name: str) -> List[Dict]:
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM food WHERE name LIKE ? ORDER BY name", (f"%{name}%",))
            return [dict(r) for r in cur.fetchall()]

    def find_by_id(self, food_id: str) -> Optional[Dict]:
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM food WHERE food_id = ?", (food_id,))
            row = cur.fetchone()
            return dict(row) if row else None

    def create(self, name: str, calories_per_portion: float, carbs: float = 0.0, protein: float = 0.0, fat: float = 0.0) -> Dict:
        food_id = str(uuid.uuid4())
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO food (food_id, name, calories_per_portion, carbs_per_portion, protein_per_portion, fat_per_portion)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (food_id, name, calories_per_portion, carbs, protein, fat))
            conn.commit()
        return self.find_by_id(food_id)
    # generoitu koodi päättyy