"""
DietaryPeriodRepository: SQLite repository for DietaryPeriod entity.

Allows users to mark experimental periods with dietary protocols/restrictions.
Examples:
- "No evening eating after 7pm" (3 weeks)
- "Weekend-only evening meals" (1 month)
- "Morning emphasis protocol" (2 weeks)

Methods:
- find_all(user_id) - Get all periods for a user
- find_active(user_id) - Get currently active periods
- find_by_date(user_id, date) - Get periods containing a specific date
- create(...) - Create new period
- end_period(period_id, end_date) - Mark period as ended
- update(...) - Update period details
- delete(period_id) - Delete period
"""
import sqlite3
import uuid
from typing import List, Optional, Dict
from datetime import datetime, date


class DietaryPeriodRepository:
    """Repository for dietary period database operations"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _conn(self):
        """Create database connection with row factory"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def find_all(self, user_id: str) -> List[Dict]:
        """
        Get all dietary periods for a user, ordered by start_date descending.
        
        Args:
            user_id: The user's ID
            
        Returns:
            List of period dictionaries
        """
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT period_id, user_id, start_date, end_date, period_name,
                       description, protocol_type, notes, is_active, created_at
                FROM dietary_period
                WHERE user_id = ?
                ORDER BY start_date DESC, created_at DESC
            """, (user_id,))
            return [dict(r) for r in cur.fetchall()]

    def find_active(self, user_id: str) -> List[Dict]:
        """
        Get currently active periods (end_date is NULL or in future).
        
        Args:
            user_id: The user's ID
            
        Returns:
            List of active period dictionaries
        """
        today = date.today().isoformat()
        
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT period_id, user_id, start_date, end_date, period_name,
                       description, protocol_type, notes, is_active, created_at
                FROM dietary_period
                WHERE user_id = ? 
                  AND is_active = 1
                  AND (end_date IS NULL OR end_date >= ?)
                ORDER BY start_date DESC
            """, (user_id, today))
            return [dict(r) for r in cur.fetchall()]

    def find_by_date(self, user_id: str, check_date: str) -> List[Dict]:
        """
        Get all periods that contain a specific date.
        
        Args:
            user_id: The user's ID
            check_date: Date to check (YYYY-MM-DD format)
            
        Returns:
            List of periods containing this date
        """
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT period_id, user_id, start_date, end_date, period_name,
                       description, protocol_type, notes, is_active, created_at
                FROM dietary_period
                WHERE user_id = ?
                  AND start_date <= ?
                  AND (end_date IS NULL OR end_date >= ?)
                ORDER BY start_date DESC
            """, (user_id, check_date, check_date))
            return [dict(r) for r in cur.fetchall()]

    def find_by_id(self, period_id: str) -> Optional[Dict]:
        """
        Get a specific period by ID.
        
        Args:
            period_id: The period ID
            
        Returns:
            Period dictionary or None
        """
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT period_id, user_id, start_date, end_date, period_name,
                       description, protocol_type, notes, is_active, created_at
                FROM dietary_period
                WHERE period_id = ?
            """, (period_id,))
            row = cur.fetchone()
            return dict(row) if row else None

    def create(self, user_id: str, start_date: str, period_name: str,
               description: Optional[str] = None, protocol_type: Optional[str] = None,
               notes: Optional[str] = None, end_date: Optional[str] = None) -> Dict:
        """
        Create a new dietary period.
        
        Args:
            user_id: The user's ID
            start_date: Start date (YYYY-MM-DD)
            period_name: Name/title of the period
            description: Detailed description
            protocol_type: Type category (e.g., 'time_restricted', 'food_restricted')
            notes: Additional notes
            end_date: Optional end date (NULL = ongoing)
            
        Returns:
            The created period as dictionary
        """
        period_id = str(uuid.uuid4())
        created_at = datetime.now().isoformat()
        
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO dietary_period 
                (period_id, user_id, start_date, end_date, period_name, 
                 description, protocol_type, notes, is_active, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, ?)
            """, (period_id, user_id, start_date, end_date, period_name,
                  description, protocol_type, notes, created_at))
            conn.commit()
        
        return {
            'period_id': period_id,
            'user_id': user_id,
            'start_date': start_date,
            'end_date': end_date,
            'period_name': period_name,
            'description': description,
            'protocol_type': protocol_type,
            'notes': notes,
            'is_active': 1,
            'created_at': created_at
        }

    def end_period(self, period_id: str, end_date: str) -> bool:
        """
        Mark a period as ended by setting end_date.
        
        Args:
            period_id: The period ID
            end_date: End date (YYYY-MM-DD)
            
        Returns:
            True if successful
        """
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                UPDATE dietary_period
                SET end_date = ?
                WHERE period_id = ?
            """, (end_date, period_id))
            conn.commit()
            return cur.rowcount > 0

    def update(self, period_id: str, **kwargs) -> bool:
        """
        Update period details.
        
        Args:
            period_id: The period ID
            **kwargs: Fields to update (period_name, description, protocol_type, notes, etc.)
            
        Returns:
            True if successful
        """
        # Build dynamic UPDATE query
        allowed_fields = ['period_name', 'description', 'protocol_type', 'notes', 
                         'start_date', 'end_date', 'is_active']
        
        updates = []
        values = []
        
        for field, value in kwargs.items():
            if field in allowed_fields:
                updates.append(f"{field} = ?")
                values.append(value)
        
        if not updates:
            return False
        
        values.append(period_id)
        
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute(f"""
                UPDATE dietary_period
                SET {', '.join(updates)}
                WHERE period_id = ?
            """, values)
            conn.commit()
            return cur.rowcount > 0

    def delete(self, period_id: str) -> bool:
        """
        Delete a dietary period.
        
        Args:
            period_id: The period ID
            
        Returns:
            True if successful
        """
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM dietary_period WHERE period_id = ?", (period_id,))
            conn.commit()
            return cur.rowcount > 0

    def deactivate(self, period_id: str) -> bool:
        """
        Deactivate a period without deleting it.
        
        Args:
            period_id: The period ID
            
        Returns:
            True if successful
        """
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                UPDATE dietary_period
                SET is_active = 0
                WHERE period_id = ?
            """, (period_id,))
            conn.commit()
            return cur.rowcount > 0
