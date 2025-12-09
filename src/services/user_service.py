# user_service.py
# Business logic for user operations

from typing import Optional
from repositories.user_repository import UserRepository
from datetime import date

class UserService:
    """Service layer for user-related business logic"""
    
    def __init__(self, db_path: str):
        self.user_repo = UserRepository(db_path)
    
    def authenticate_user(self, username: str, password: str) -> bool:
        """Authenticate a user with username and password"""
        return self.user_repo.authenticate(username, password)
    
    def register_user(self, username: str, password: str, **user_data):
        """Register a new user with provided data"""
        # Validate required fields
        if not username or not password:
            raise ValueError("Username and password are required")
        
        # Check if user already exists
        existing_user = self.user_repo.find_by_username(username)
        if existing_user:
            raise ValueError(f"Username '{username}' already exists")
        
        # Create user
        return self.user_repo.create_user(username, password, **user_data)
    
    def get_user(self, username: str):
        """Get user by username"""
        return self.user_repo.find_by_username(username)
    
    def get_user_summary(self, username: str) -> dict:
        """Get formatted user summary for display"""
        user = self.user_repo.find_by_username(username)
        if not user:
            return None
        
        return {
            'user_id': user.user_id,
            'username': user.username,
            'weight': user.weight,
            'target': user.weight_loss_target,
            'kcal_min': user.kcal_min,
            'kcal_max': user.kcal_max,
            'activity_level': user.activity_level,
            'allergies': user.allergies,
            'current_date': date.today().strftime('%Y-%m-%d')
        }
    
    def get_all_users(self):
        """Get all registered users (for admin)"""
        return self.user_repo.find_all()
