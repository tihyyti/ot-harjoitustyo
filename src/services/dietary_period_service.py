"""
DietaryPeriodService: Business logic for dietary period tracking.

Allows users to experiment with different dietary protocols and track
which periods correlate with better weight loss results.

Examples:
- "No Evening Eating After 7pm" (3 weeks trial)
- "Weekend-Only Evening Meals" (1 month experiment)
- "Morning Emphasis - Breakfast 40%, Lunch 40%, Dinner 20%"
- "Intermittent Fasting 16:8"
- "Low-Carb Experiment"
"""

from typing import List, Dict, Optional
from datetime import datetime, date
from repositories.dietary_period_repository import DietaryPeriodRepository


class DietaryPeriodService:
    """Service layer for dietary period management"""
    
    # Predefined protocol types
    PROTOCOL_TYPES = [
        'time_restricted',      # e.g., no eating after 7pm
        'meal_timing',          # e.g., morning emphasis
        'food_restricted',      # e.g., low-carb, no sugar
        'intermittent_fasting', # e.g., 16:8, 5:2
        'portion_control',      # e.g., smaller portions
        'food_combination',     # e.g., protein with every meal
        'custom'                # user-defined
    ]
    
    # Common error messages
    ERROR_PERIOD_NOT_FOUND = 'Period not found'
    
    # Common durations
    DURATION_2_3_WEEKS = '2-3 weeks'
    DURATION_3_4_WEEKS = '3-4 weeks'
    DURATION_2_4_WEEKS = '2-4 weeks'
    DURATION_1_MONTH = '1 month'
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.period_repo = DietaryPeriodRepository(db_path)
    
    def create_period(self, user_id: str, start_date: str, period_name: str,
                     description: Optional[str] = None, protocol_type: Optional[str] = None,
                     notes: Optional[str] = None, end_date: Optional[str] = None) -> Dict:
        """
        Create a new dietary experiment period.
        
        Args:
            user_id: The user's ID
            start_date: Start date (YYYY-MM-DD)
            period_name: Name of the experiment (e.g., "No Evening Eating")
            description: Detailed description
            protocol_type: Type from PROTOCOL_TYPES or custom
            notes: Additional notes
            end_date: Optional end date (leave None for ongoing)
            
        Returns:
            Dictionary with success status and created period
        """
        # Validate start date
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
        except ValueError:
            return {'success': False, 'error': 'Invalid start date format. Use YYYY-MM-DD'}
        
        # Validate end date if provided
        if end_date:
            try:
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
                if end_date_obj < start_date_obj:
                    return {'success': False, 'error': 'End date must be after start date'}
            except ValueError:
                return {'success': False, 'error': 'Invalid end date format. Use YYYY-MM-DD'}
        
        # Validate period name
        if not period_name or len(period_name.strip()) == 0:
            return {'success': False, 'error': 'Period name is required'}
        
        # Create the period
        try:
            period = self.period_repo.create(
                user_id=user_id,
                start_date=start_date,
                period_name=period_name.strip(),
                description=description,
                protocol_type=protocol_type,
                notes=notes,
                end_date=end_date
            )
            return {'success': True, 'period': period, 'message': 'Period created successfully'}
        except Exception as e:
            return {'success': False, 'error': f'Database error: {str(e)}'}
    
    def get_all_periods(self, user_id: str) -> List[Dict]:
        """Get all dietary periods for a user (descending order)"""
        return self.period_repo.find_all(user_id)
    
    def get_active_periods(self, user_id: str) -> List[Dict]:
        """Get currently active/ongoing periods"""
        return self.period_repo.find_active(user_id)
    
    def get_periods_for_date(self, user_id: str, check_date: str) -> List[Dict]:
        """Get all periods that were active on a specific date"""
        return self.period_repo.find_by_date(user_id, check_date)
    
    def end_period(self, period_id: str, end_date: Optional[str] = None) -> Dict:
        """
        Mark a period as ended.
        
        Args:
            period_id: The period ID
            end_date: End date (defaults to today if None)
            
        Returns:
            Dictionary with success status
        """
        if not end_date:
            end_date = date.today().isoformat()
        
        # Validate date
        try:
            datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            return {'success': False, 'error': 'Invalid date format. Use YYYY-MM-DD'}
        
        # Get period to validate
        period = self.period_repo.find_by_id(period_id)
        if not period:
            return {'success': False, 'error': self.ERROR_PERIOD_NOT_FOUND}
        
        # Check end date is not before start date
        if end_date < period['start_date']:
            return {'success': False, 'error': 'End date cannot be before start date'}
        
        success = self.period_repo.end_period(period_id, end_date)
        
        if success:
            return {'success': True, 'message': f'Period ended on {end_date}'}
        else:
            return {'success': False, 'error': 'Failed to end period'}
    
    def update_period(self, period_id: str, **kwargs) -> Dict:
        """
        Update period details.
        
        Args:
            period_id: The period ID
            **kwargs: Fields to update
            
        Returns:
            Dictionary with success status
        """
        # Get period to verify it exists
        period = self.period_repo.find_by_id(period_id)
        if not period:
            return {'success': False, 'error': self.ERROR_PERIOD_NOT_FOUND}
        
        success = self.period_repo.update(period_id, **kwargs)
        
        if success:
            return {'success': True, 'message': 'Period updated successfully'}
        else:
            return {'success': False, 'error': 'No changes made'}
    
    def delete_period(self, period_id: str) -> Dict:
        """Delete a dietary period"""
        success = self.period_repo.delete(period_id)
        
        if success:
            return {'success': True, 'message': 'Period deleted successfully'}
        else:
            return {'success': False, 'error': self.ERROR_PERIOD_NOT_FOUND}
    
    def get_period_summary(self, period_id: str) -> Optional[Dict]:
        """
        Get comprehensive summary of a dietary period including effectiveness.
        
        Returns:
            Dictionary with period info, duration, and weight loss during period
        """
        from services.weightlog_service import WeightLogService
        
        period = self.period_repo.find_by_id(period_id)
        if not period:
            return None
        
        # Calculate duration
        start = datetime.strptime(period['start_date'], '%Y-%m-%d').date()
        
        if period['end_date']:
            end = datetime.strptime(period['end_date'], '%Y-%m-%d').date()
            is_ongoing = False
        else:
            end = date.today()
            is_ongoing = True
        
        duration_days = (end - start).days + 1
        
        # Get weight change during this period
        weight_service = WeightLogService(self.db_path)
        
        start_weight = weight_service.get_weight_on_date(period['user_id'], period['start_date'])
        end_weight = weight_service.get_weight_on_date(period['user_id'], 
                                                       period['end_date'] if period['end_date'] else end.isoformat())
        
        weight_change = None
        if start_weight and end_weight:
            weight_change = {
                'start_weight': start_weight,
                'end_weight': end_weight,
                'change': end_weight - start_weight,
                'change_per_week': ((end_weight - start_weight) / duration_days) * 7 if duration_days > 0 else 0
            }
        
        return {
            **period,
            'duration_days': duration_days,
            'is_ongoing': is_ongoing,
            'weight_change': weight_change
        }
    
    def get_suggested_protocols(self) -> List[Dict]:
        """
        Get list of suggested dietary protocols with descriptions.
        """
        return [
            {
                'type': 'time_restricted',
                'name': 'No Evening Eating After 7pm',
                'description': 'Stop eating after 7pm to allow 12+ hour fasting overnight',
                'example_duration': self.DURATION_2_4_WEEKS
            },
            {
                'type': 'meal_timing',
                'name': 'Morning Emphasis',
                'description': 'Front-load calories: 40% breakfast, 40% lunch, 20% dinner',
                'example_duration': self.DURATION_3_4_WEEKS
            },
            {
                'type': 'time_restricted',
                'name': 'Weekend-Only Evening Meals',
                'description': 'Light dinners weekdays, normal dinners on weekends',
                'example_duration': self.DURATION_1_MONTH
            },
            {
                'type': 'intermittent_fasting',
                'name': 'Intermittent Fasting 16:8',
                'description': 'Eat within 8-hour window (e.g., 12pm-8pm)',
                'example_duration': self.DURATION_2_3_WEEKS
            },
            {
                'type': 'food_restricted',
                'name': 'Low-Carb Experiment',
                'description': 'Reduce carbohydrates, increase protein and healthy fats',
                'example_duration': self.DURATION_3_4_WEEKS
            },
            {
                'type': 'portion_control',
                'name': 'Smaller Portions',
                'description': 'Reduce all portion sizes by 20-30%',
                'example_duration': self.DURATION_2_3_WEEKS
            },
            {
                'type': 'food_combination',
                'name': 'Protein With Every Meal',
                'description': 'Include protein source at every meal for satiety',
                'example_duration': self.DURATION_3_4_WEEKS
            },
            {
                'type': 'food_elimination',
                'name': 'Climate Friendly & Animal Protection Diet',
                'description': 'Plant-based meals prioritizing local, seasonal ingredients with minimal animal products for environmental and ethical benefits',
                'example_duration': self.DURATION_3_4_WEEKS
            }
        ]
