# modifioitu, aiemmin generoitu koodi alkaa (food -> activity)
"""
ActivityRepository; SQLite-repo for Activity-entity.
Methods:
- find_all()
- find_by_name(name)
- find_by_id(activity_id)
- create(activity_dict)  # returns inserted row as dict
"""
import sqlite3
import uuid
from typing import List, Optional, Dict


class ActivityRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def find_all(self) -> List[Dict]:
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM Activity ORDER BY name")
            return [dict(r) for r in cur.fetchall()]

    def find_by_name(self, name: str) -> List[Dict]:
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT * FROM Activity WHERE name LIKE ? ORDER BY name", (f"%{name}%",)
            )
            return [dict(r) for r in cur.fetchall()]

    def find_by_id(self, activity_id: str) -> Optional[Dict]:
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM Activity WHERE activity_id = ?", (activity_id,))
            row = cur.fetchone()
            return dict(row) if row else None

    def create(self, name: str, unit: str, kcal_per_unit: float = 0.0) -> Dict:
        activity_id = str(uuid.uuid4())
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO Activity (activity_id, name, unit, kcal_per_unit)
                VALUES (?, ?, ?,?)
            """,
                (activity_id, name, unit, kcal_per_unit),
            )
            conn.commit()
        return self.find_by_id(activity_id)

    # modifioitu, aiemmin generoitu koodi päättyy
