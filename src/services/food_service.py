# food_service.py
# Business logic for food and food logging operations

from typing import List, Dict, Optional
from datetime import date
import sqlite3
from repositories.food_repository import FoodRepository
from repositories.foodlog_repository import FoodLogRepository

class FoodService:
    """Service layer for food-related business logic"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.food_repo = FoodRepository(db_path)
        self.foodlog_repo = FoodLogRepository(db_path)
    
    def get_all_foods(self) -> List[Dict]:
        """Get all available foods"""
        return self.food_repo.find_all()
    
    def get_food_display_list(self) -> List[str]:
        """Get formatted food list for UI dropdown (name only, id stored internally)"""
        foods = self.food_repo.find_all()
        # Return dict with display name and internal ID mapping
        # For now, keep name|id format for backward compatibility with parsing logic
        return [f"{f['name']}|{f['food_id']}" for f in foods]
    
    def get_food_name_only_list(self) -> List[str]:
        """Get food names only (without IDs) for display"""
        foods = self.food_repo.find_all()
        return [f['name'] for f in foods]
    
    def get_food_id_by_name(self, food_name: str) -> str:
        """Get food ID by name"""
        foods = self.food_repo.find_all()
        for food in foods:
            if food['name'] == food_name:
                return food['food_id']
        raise ValueError(f"Food '{food_name}' not found")
    
    def log_food(self, user_id: str, food_selection: str, portion_g: float, date_str: str):
        """Log a food entry for a user"""
        # Parse food_id from selection string (format: name|food_id)
        try:
            food_id = food_selection.split("|", 1)[1]
        except (IndexError, AttributeError):
            raise ValueError("Invalid food selection format")
        
        # Validate portion
        if portion_g <= 0:
            raise ValueError("Portion must be greater than zero")
        
        # Create log entry
        return self.foodlog_repo.create_log(user_id, food_id, date_str, portion_g)
    
    def get_user_food_logs(self, user_id: str, date_str: str) -> List[Dict]:
        """Get food logs for a specific user and date"""
        return self.foodlog_repo.find_by_user_and_date(user_id, date_str)
    
    def get_all_user_food_logs(self, user_id: str) -> List[Dict]:
        """Get all food logs for a user"""
        return self.foodlog_repo.find_all_for_user(user_id)
    
    def get_daily_food_totals(self, user_id: str) -> List[Dict]:
        """Get aggregated daily food totals with date highlighting"""
        today = date.today().isoformat()
        
        conn = sqlite3.connect(self.db_path)
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT fl.date AS date,
                       SUM( (fl.portion_size_g / 100) * COALESCE(f.kcal_per_portion, 0.0) ) AS total_calories,
                       COUNT(*) AS entries
                FROM foodlog fl
                LEFT JOIN food f ON fl.food_id = f.food_id
                WHERE fl.user_id = ?
                GROUP BY fl.date
                ORDER BY fl.date DESC
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
                    'total_kcal': f"{total_cal:.1f}",
                    'entries': entries,
                    'category': category
                })
            
            return results
        finally:
            conn.close()
    
    def update_food_log(self, log_id: str, portion_g: float, date_str: str):
        """Update an existing food log entry"""
        conn = sqlite3.connect(self.db_path)
        try:
            cur = conn.cursor()
            cur.execute(
                "UPDATE foodlog SET portion_size_g = ?, date = ? WHERE log_id = ?",
                (portion_g, date_str, log_id)
            )
            conn.commit()
        finally:
            conn.close()
    
    def delete_food_log(self, log_id: str):
        """Delete a food log entry"""
        conn = sqlite3.connect(self.db_path)
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM foodlog WHERE log_id = ?", (log_id,))
            conn.commit()
        finally:
            conn.close()
    
    def get_food_logs_by_date(self, user_id: str, date_str: str):
        """Get formatted food logs for a specific date"""
        logs = self.foodlog_repo.find_by_user_and_date(user_id, date_str)
        formatted_logs = []
        for log in logs:
            name = log.get("name") or "?"
            portion = int(log.get("portion_size_g") or 100)
            cal_per = int(log.get("kcal_per_portion") or 0)
            total_cal = float((portion / 100.0) * cal_per)
            # Return formatted string with better spacing for display
            # Using wider spacing between fields for better readability
            formatted_logs.append(f"{name:<35} {portion:>5}g      {total_cal:>6.1f} kcal")
        return formatted_logs
    
    def get_all_food_logs(self, user_id: str):
        """Get all food logs for a user"""
        logs = self.foodlog_repo.find_all_for_user(user_id)
        formatted_logs = []
        for log in logs:
            name = log.get("name") or "?"
            portion = int(log.get("portion_size_g") or 100)
            cal_per = int(log.get("kcal_per_portion") or 0)
            total_cal = float((portion / 100.0) * cal_per)
            formatted_logs.append({
                'date': log['date'],
                'name': name,
                'portion': portion,
                'calories': total_cal,
                'log_id': log['log_id']
            })
        return formatted_logs
