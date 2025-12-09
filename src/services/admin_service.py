# admin_service.py
# Business logic for admin operations

from typing import List, Dict, Optional
import sqlite3
import uuid
from repositories.admin_repository import AdminRepository
from repositories.user_repository import UserRepository

class AdminService:
    """Service layer for admin-related business logic"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.admin_repo = AdminRepository(db_path)
        self.user_repo = UserRepository(db_path)
    
    def authenticate_admin(self, username: str, password: str) -> bool:
        """Authenticate an admin user"""
        return self.admin_repo.verify_password(username, password)
    
    def get_all_users_summary(self) -> List[tuple]:
        """Get summary of all users for admin dashboard"""
        conn = sqlite3.connect(self.db_path)
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT username, weight, weight_loss_target, kcal_min, kcal_max, activity_level, allergies
                FROM user
                ORDER BY username
            """)
            return cur.fetchall()
        finally:
            conn.close()
    
    def create_recommendation(self, username: str, admin_username: str, 
                            rec_type: str, title: str, kcal_min: Optional[float], 
                            kcal_max: Optional[float], activities: str, notes: str):
        """Create a recommendation for a user"""
        # Get user_id
        user = self.user_repo.find_by_username(username)
        if not user:
            raise ValueError("User not found")
        
        # Get admin_id
        admin = self.admin_repo.find_by_username(admin_username)
        
        rec_id = str(uuid.uuid4())
        
        conn = sqlite3.connect(self.db_path)
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO recommendation 
                (recommendation_id, user_id, admin_id, recommendation_type, title, description, 
                 target_kcal_min, target_kcal_max, suggested_activities, notes, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'active')
            """, (rec_id, user.user_id, admin.admin_id if admin else None, rec_type, title, "", 
                  kcal_min, kcal_max, activities, notes))
            conn.commit()
            return rec_id
        finally:
            conn.close()
    
    def get_user_constraints(self, username: str) -> List[tuple]:
        """Get all constraints for a specific user"""
        user = self.user_repo.find_by_username(username)
        if not user:
            return []
        
        conn = sqlite3.connect(self.db_path)
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT constraint_type, description, severity
                FROM user_constraint
                WHERE user_id = ?
                ORDER BY severity DESC, constraint_type
            """, (user.user_id,))
            return cur.fetchall()
        finally:
            conn.close()
    
    def add_user_constraint(self, username: str, constraint_type: str, 
                          description: str, severity: str):
        """Add a constraint for a user"""
        user = self.user_repo.find_by_username(username)
        if not user:
            raise ValueError("User not found")
        
        constraint_id = str(uuid.uuid4())
        
        conn = sqlite3.connect(self.db_path)
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO user_constraint 
                (constraint_id, user_id, constraint_type, description, severity)
                VALUES (?, ?, ?, ?, ?)
            """, (constraint_id, user.user_id, constraint_type, description, severity))
            conn.commit()
            return constraint_id
        finally:
            conn.close()
    
    def get_usernames_list(self) -> List[str]:
        """Get list of all usernames"""
        conn = sqlite3.connect(self.db_path)
        try:
            cur = conn.cursor()
            cur.execute("SELECT username FROM user ORDER BY username")
            return [row[0] for row in cur.fetchall()]
        finally:
            conn.close()
