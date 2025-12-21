"""
WeightLogRepository: SQLite repository for WeightLog entity.

Methods:
- find_all(user_id) - Get all weight logs for a user
- find_by_id(log_id) - Get a specific weight log by ID
- find_by_date_range(user_id, start_date, end_date) - Get weight logs in date range
- find_latest(user_id) - Get the most recent weight log for a user
- create(user_id, date, weight, notes) - Create a new weight log entry
- update(log_id, weight, notes) - Update an existing weight log
- delete(log_id) - Delete a weight log entry
"""
import sqlite3
import uuid
from typing import List, Optional, Dict
from datetime import datetime


class WeightLogRepository:
    """Repository for weight log database operations"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _conn(self):
        """Create database connection with row factory"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def find_all(self, user_id: str) -> List[Dict]:
        """
        Get all weight logs for a user, ordered by date descending.
        
        Args:
            user_id: The user's ID
            
        Returns:
            List of weight log dictionaries
        """
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT log_id, user_id, date, weight, notes, created_at
                FROM weightlog
                WHERE user_id = ?
                ORDER BY date DESC, created_at DESC
            """, (user_id,))
            return [dict(r) for r in cur.fetchall()]

    def find_by_id(self, log_id: str) -> Optional[Dict]:
        """
        Get a specific weight log by ID.
        
        Args:
            log_id: The weight log ID
            
        Returns:
            Weight log dictionary or None if not found
        """
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT log_id, user_id, date, weight, notes, created_at
                FROM weightlog
                WHERE log_id = ?
            """, (log_id,))
            row = cur.fetchone()
            return dict(row) if row else None

    def find_by_date_range(self, user_id: str, start_date: str, end_date: str) -> List[Dict]:
        """
        Get weight logs for a user within a date range.
        
        Args:
            user_id: The user's ID
            start_date: Start date (YYYY-MM-DD format)
            end_date: End date (YYYY-MM-DD format)
            
        Returns:
            List of weight log dictionaries
        """
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT log_id, user_id, date, weight, notes, created_at
                FROM weightlog
                WHERE user_id = ? AND date BETWEEN ? AND ?
                ORDER BY date DESC
            """, (user_id, start_date, end_date))
            return [dict(r) for r in cur.fetchall()]

    def find_latest(self, user_id: str) -> Optional[Dict]:
        """
        Get the most recent weight log for a user.
        
        Args:
            user_id: The user's ID
            
        Returns:
            Weight log dictionary or None if no logs exist
        """
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT log_id, user_id, date, weight, notes, created_at
                FROM weightlog
                WHERE user_id = ?
                ORDER BY date DESC, created_at DESC
                LIMIT 1
            """, (user_id,))
            row = cur.fetchone()
            return dict(row) if row else None

    def find_by_date(self, user_id: str, date: str) -> Optional[Dict]:
        """
        Get weight log for a specific date.
        
        Args:
            user_id: The user's ID
            date: Date (YYYY-MM-DD format)
            
        Returns:
            Weight log dictionary or None if not found
        """
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT log_id, user_id, date, weight, notes, created_at
                FROM weightlog
                WHERE user_id = ? AND date = ?
                ORDER BY created_at DESC
                LIMIT 1
            """, (user_id, date))
            row = cur.fetchone()
            return dict(row) if row else None

    def create(self, user_id: str, date: str, weight: float, notes: Optional[str] = None) -> Dict:
        """
        Create a new weight log entry.
        
        Args:
            user_id: The user's ID
            date: Date of measurement (YYYY-MM-DD format)
            weight: Weight in kg
            notes: Optional notes about the measurement
            
        Returns:
            The created weight log as a dictionary
        """
        log_id = str(uuid.uuid4())
        created_at = datetime.now().isoformat()
        
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO weightlog (log_id, user_id, date, weight, notes, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (log_id, user_id, date, weight, notes, created_at))
            conn.commit()
        
        return {
            'log_id': log_id,
            'user_id': user_id,
            'date': date,
            'weight': weight,
            'notes': notes,
            'created_at': created_at
        }

    def update(self, log_id: str, weight: float, notes: Optional[str] = None) -> bool:
        """
        Update an existing weight log entry.
        
        Args:
            log_id: The weight log ID
            weight: New weight value in kg
            notes: Updated notes
            
        Returns:
            True if update successful, False if log not found
        """
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                UPDATE weightlog
                SET weight = ?, notes = ?
                WHERE log_id = ?
            """, (weight, notes, log_id))
            conn.commit()
            return cur.rowcount > 0

    def delete(self, log_id: str) -> bool:
        """
        Delete a weight log entry.
        
        Args:
            log_id: The weight log ID
            
        Returns:
            True if deletion successful, False if log not found
        """
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM weightlog WHERE log_id = ?", (log_id,))
            conn.commit()
            return cur.rowcount > 0

    def count_logs(self, user_id: str) -> int:
        """
        Count total weight logs for a user.
        
        Args:
            user_id: The user's ID
            
        Returns:
            Number of weight log entries
        """
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM weightlog WHERE user_id = ?", (user_id,))
            return cur.fetchone()[0]
