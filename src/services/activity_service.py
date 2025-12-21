# activity_service.py
# Business logic for activity and activity logging operations

from typing import List, Dict
from datetime import date
import sqlite3
from repositories.activity_repository import ActivityRepository
from repositories.activitylog_repository import ActivityLogRepository

class ActivityService:
    """Service layer for activity-related business logic"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.activity_repo = ActivityRepository(db_path)
        self.activitylog_repo = ActivityLogRepository(db_path)
    
    def get_all_activities(self) -> List[Dict]:
        """Get all available activities"""
        return self.activity_repo.find_all()
    
    def get_activity_display_list(self) -> List[str]:
        """Get formatted activity list for UI dropdown (name|id format)"""
        activities = self.activity_repo.find_all()
        # Return dict with display name and internal ID mapping
        # For now, keep name|id format for backward compatibility with parsing logic
        return [f"{a['name']}|{a['activity_id']}" for a in activities]
    
    def get_activity_name_only_list(self) -> List[str]:
        """Get activity names only (without IDs) for display"""
        activities = self.activity_repo.find_all()
        return [a['name'] for a in activities]
    
    def get_activity_id_by_name(self, activity_name: str) -> str:
        """Get activity ID by name"""
        activities = self.activity_repo.find_all()
        for activity in activities:
            if activity['name'] == activity_name:
                return activity['activity_id']
        raise ValueError(f"Activity '{activity_name}' not found")
    
    def log_activity(self, user_id: str, activity_selection: str, activity_count: float, date_str: str):
        """Log an activity entry for a user"""
        # Parse activity_id from selection string
        try:
            activity_id = activity_selection.split("|", 1)[1]
        except (IndexError, AttributeError):
            raise ValueError("Invalid activity selection format")
        
        # Validate count
        if activity_count <= 0:
            raise ValueError("Activity count must be greater than zero")
        
        # Calculate calories burned
        activity = self.activity_repo.find_by_id(activity_id)
        kcal_burned = (activity_count / 1000.0) * activity.get("kcal_per_unit", 0)
        
        # Create log entry
        return self.activitylog_repo.create_log(user_id, activity_id, date_str, activity_count, kcal_burned)
    
    def get_user_activity_logs(self, user_id: str, date_str: str) -> List[Dict]:
        """Get activity logs for a specific user and date"""
        return self.activitylog_repo.find_by_user_and_date(user_id, date_str)
    
    def get_all_user_activity_logs(self, user_id: str) -> List[Dict]:
        """Get all activity logs for a user"""
        return self.activitylog_repo.find_all_for_user(user_id)
    
    def get_daily_activity_totals(self, user_id: str) -> List[Dict]:
        """Get aggregated daily activity totals with date highlighting"""
        today = date.today().isoformat()
        
        conn = sqlite3.connect(self.db_path)
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT al.date AS date,
                       SUM(COALESCE(al.kcal_burned, 0.0)) AS total_calories,
                       COUNT(*) AS entries
                FROM activitylog al
                WHERE al.user_id = ?
                GROUP BY al.date
                ORDER BY al.date DESC
            """, (user_id,))
            
            results = []
            for date_str, total_cal, entries in cur.fetchall():
                # Determine time category
                if date_str < today:
                    category = 'past'
                    display_date = date_str
                elif date_str == today:
                    category = 'today'
                    display_date = f"{date_str} 📍 TODAY"
                else:
                    category = 'future'
                    display_date = f"{date_str} 🔮 PLANNED"

                results.append({
                    'date': display_date,
                    'total_kcal_burned': f"{total_cal:.1f}",
                    'entries': entries,
                    'category': category
                })
            
            return results
        finally:
            conn.close()
    
    def update_activity_log(self, log_id: str, activity_count: int, date_str: str):
        """Update an existing activity log entry"""
        conn = sqlite3.connect(self.db_path)
        try:
            cur = conn.cursor()
            cur.execute(
                "UPDATE activitylog SET activity_count = ?, date = ? WHERE log_id = ?",
                (activity_count, date_str, log_id)
            )
            conn.commit()
        finally:
            conn.close()
    
    def delete_activity_log(self, log_id: str):
        """Delete an activity log entry"""
        conn = sqlite3.connect(self.db_path)
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM activitylog WHERE log_id = ?", (log_id,))
            conn.commit()
        finally:
            conn.close()
    
    def get_activity_logs_by_date(self, user_id: str, date_str: str):
        """Get formatted activity logs for a specific date"""
        logs = self.activitylog_repo.find_by_user_and_date(user_id, date_str)
        formatted_logs = []
        for log in logs:
            name = log.get('name') or '?'
            count = int(log.get('activity_count') or 0)
            kcal_burned = float(log.get('kcal_burned') or 0)
            # Return formatted string with better spacing for display
            # Using wider spacing between fields for better readability
            formatted_logs.append(f"{name:<35} x{count:<4}     {kcal_burned:>6.2f} kcal burned")
        return formatted_logs
    
    def get_all_activity_logs(self, user_id: str):
        """Get all activity logs for a user"""
        logs = self.activitylog_repo.find_all_for_user(user_id)
        formatted_logs = []
        for log in logs:
            formatted_logs.append({
                'date': log.get('date'),
                'name': log.get('name') or '?',
                'count': int(log.get('activity_count') or 0),
                'kcal_burned': float(log.get('kcal_burned') or 0),
                'log_id': log.get('log_id')
            })
        return formatted_logs
