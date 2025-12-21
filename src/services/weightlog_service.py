"""
WeightLogService: Business logic for weight tracking operations.

Handles:
- Weight logging with validation
- Weight history retrieval with week numbering
- Weight trend calculations
- Progress tracking against goals
- Dietary period annotations for log entries
"""

from typing import List, Dict, Optional
from datetime import datetime, timedelta
from repositories.weightlog_repository import WeightLogRepository
from repositories.user_repository import UserRepository


def get_week_info(date_str: str) -> Dict:
    """
    Get week number and week start date for a given date.
    
    Args:
        date_str: Date in YYYY-MM-DD format
        
    Returns:
        Dictionary with week_number, week_start_date, year
    """
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    
    # ISO week date: week starts on Monday
    iso_calendar = date_obj.isocalendar()
    week_number = iso_calendar[1]
    year = iso_calendar[0]
    
    # Calculate Monday of this week (Monday = 0 in weekday())
    days_since_monday = date_obj.weekday()
    week_start = date_obj - timedelta(days=days_since_monday)
    
    return {
        'week_number': week_number,
        'week_start_date': week_start.isoformat(),
        'year': year,
        'week_label': f"Week {week_number}, {year}"
    }


class WeightLogService:
    """Service layer for weight tracking business logic"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.weightlog_repo = WeightLogRepository(db_path)
        self.user_repo = UserRepository(db_path)
    
    def log_weight(self, user_id: str, date_str: str, weight: float, notes: Optional[str] = None) -> Dict:
        """
        Log a weight measurement for a user with validation.
        
        Args:
            user_id: The user's ID
            date_str: Date of measurement (YYYY-MM-DD format)
            weight: Weight in kg
            notes: Optional notes about the measurement
            
        Returns:
            Dictionary with success status and created log or error message
        """
        # Validate weight value
        if weight <= 0:
            return {'success': False, 'error': 'Weight must be greater than zero'}
        
        if weight > 500:  # Sanity check
            return {'success': False, 'error': 'Weight value seems unrealistic (max 500 kg)'}
        
        # Validate date format
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            return {'success': False, 'error': 'Invalid date format. Use YYYY-MM-DD'}
        
        # Check if date is not in future
        today = datetime.now().date()
        log_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        if log_date > today:
            return {'success': False, 'error': 'Cannot log weight for future dates'}
        
        # Create the weight log
        try:
            log = self.weightlog_repo.create(user_id, date_str, weight, notes)
            return {'success': True, 'log': log, 'message': 'Weight logged successfully'}
        except Exception as e:
            return {'success': False, 'error': f'Database error: {str(e)}'}
    
    def get_weight_history(self, user_id: str, days: int = 30) -> List[Dict]:
        """
        Get weight history for a user for the last N days.
        
        Args:
            user_id: The user's ID
            days: Number of days to look back (default: 30)
            
        Returns:
            List of weight log dictionaries, ordered by date descending
        """
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        
        return self.weightlog_repo.find_by_date_range(
            user_id,
            start_date.isoformat(),
            end_date.isoformat()
        )
    
    def get_all_weight_history(self, user_id: str) -> List[Dict]:
        """
        Get complete weight history for a user.
        
        Args:
            user_id: The user's ID
            
        Returns:
            List of all weight log dictionaries
        """
        return self.weightlog_repo.find_all(user_id)
    
    def get_latest_weight(self, user_id: str) -> Optional[float]:
        """
        Get the most recent weight measurement for a user.
        
        Args:
            user_id: The user's ID
            
        Returns:
            Weight in kg or None if no logs exist
        """
        latest = self.weightlog_repo.find_latest(user_id)
        return latest['weight'] if latest else None
    
    def get_weight_on_date(self, user_id: str, date_str: str) -> Optional[float]:
        """
        Get weight measurement on a specific date.
        
        Args:
            user_id: The user's ID
            date_str: Date (YYYY-MM-DD format)
            
        Returns:
            Weight in kg or None if no log exists for that date
        """
        log = self.weightlog_repo.find_by_date(user_id, date_str)
        return log['weight'] if log else None
    
    def calculate_weight_change(self, user_id: str, days_back: int = 7) -> Optional[Dict]:
        """
        Calculate weight change over a period.
        
        Args:
            user_id: The user's ID
            days_back: Number of days to look back (default: 7 for weekly)
            
        Returns:
            Dictionary with weight change info or None if insufficient data
        """
        history = self.get_weight_history(user_id, days=days_back + 1)
        
        if len(history) < 2:
            return None
        
        # Get most recent weight
        current_weight = history[0]['weight']
        current_date = history[0]['date']
        
        # Find weight from N days ago (or closest available)
        start_weight = history[-1]['weight']
        start_date = history[-1]['date']
        
        weight_change = current_weight - start_weight
        change_percentage = (weight_change / start_weight) * 100 if start_weight > 0 else 0
        
        # Determine trend
        if weight_change < 0:
            trend = 'losing'
        elif weight_change > 0:
            trend = 'gaining'
        else:
            trend = 'stable'
        
        return {
            'current_weight': current_weight,
            'current_date': current_date,
            'start_weight': start_weight,
            'start_date': start_date,
            'weight_change': weight_change,
            'change_percentage': change_percentage,
            'days_elapsed': days_back,
            'trend': trend
        }
    
    def get_progress_summary(self, user_id: str) -> Dict:
        """
        Get comprehensive weight progress summary.
        
        Args:
            user_id: The user's ID
            
        Returns:
            Dictionary with current weight, weekly/monthly changes, and goal progress
        """
        latest_weight = self.get_latest_weight(user_id)
        
        if not latest_weight:
            return {
                'has_data': False,
                'message': 'No weight logs found. Start tracking your weight!'
            }
        
        # Calculate weekly change
        weekly_change = self.calculate_weight_change(user_id, days_back=7)
        
        # Calculate monthly change
        monthly_change = self.calculate_weight_change(user_id, days_back=30)
        
        # Calculate goal progress
        goal_progress = None
        # Removed goal tracking as UserRepository doesn't have find_by_id method
        # Would need to implement this differently to get user's starting weight and target
        
        return {
            'has_data': True,
            'current_weight': latest_weight,
            'weekly_change': weekly_change,
            'monthly_change': monthly_change,
            'goal_progress': goal_progress,
            'total_logs': self.weightlog_repo.count_logs(user_id)
        }
    
    def update_weight_log(self, log_id: str, weight: float, notes: Optional[str] = None) -> Dict:
        """
        Update an existing weight log entry.
        
        Args:
            log_id: The weight log ID
            weight: New weight value in kg
            notes: Updated notes
            
        Returns:
            Dictionary with success status and message
        """
        # Validate weight
        if weight <= 0:
            return {'success': False, 'error': 'Weight must be greater than zero'}
        
        if weight > 500:
            return {'success': False, 'error': 'Weight value seems unrealistic (max 500 kg)'}
        
        # Update the log
        success = self.weightlog_repo.update(log_id, weight, notes)
        
        if success:
            return {'success': True, 'message': 'Weight log updated successfully'}
        else:
            return {'success': False, 'error': 'Weight log not found'}
    
    def delete_weight_log(self, log_id: str) -> Dict:
        """
        Delete a weight log entry.
        
        Args:
            log_id: The weight log ID
            
        Returns:
            Dictionary with success status and message
        """
        success = self.weightlog_repo.delete(log_id)
        
        if success:
            return {'success': True, 'message': 'Weight log deleted successfully'}
        else:
            return {'success': False, 'error': 'Weight log not found'}
    
    def get_weight_trend_data(self, user_id: str, days: int = 30) -> Dict:
        """
        Get formatted weight trend data for charting.
        
        Args:
            user_id: The user's ID
            days: Number of days to include (default: 30)
            
        Returns:
            Dictionary with dates and weights for plotting
        """
        history = self.get_weight_history(user_id, days=days)
        
        if not history:
            return {'dates': [], 'weights': [], 'has_data': False}
        
        # Sort by date ascending for chronological plotting
        history.sort(key=lambda x: x['date'])
        
        dates = [log['date'] for log in history]
        weights = [log['weight'] for log in history]
        
        return {
            'dates': dates,
            'weights': weights,
            'has_data': True,
            'count': len(history)
        }
    
    def _find_periods_for_date(self, log_date: str, periods: List[Dict]) -> tuple:
        """
        Helper: Find periods containing a date and detect start/end markers.
        
        Returns:
            Tuple of (active_period_names, period_markers)
        """
        active_periods = []
        period_markers = []
        
        for period in periods:
            # Check if log date falls within period
            in_period_start = period['start_date'] <= log_date
            in_period_end = (period['end_date'] is None or period['end_date'] >= log_date)
            
            if in_period_start and in_period_end:
                active_periods.append(period['period_name'])
                
                # Mark period start/end
                if period['start_date'] == log_date:
                    period_markers.append(f"▶ START: {period['period_name']}")
                if period['end_date'] == log_date:
                    period_markers.append(f"⏹ END: {period['period_name']}")
        
        return (active_periods, period_markers)
    
    def get_weight_history_with_weeks(self, user_id: str, days: int = 30, 
                                      include_periods: bool = True) -> List[Dict]:
        """
        Get weight history with week numbering and optional dietary period annotations.
        Entries are returned in DESCENDING order (most recent first).
        
        Args:
            user_id: The user's ID
            days: Number of days to look back (default: 30)
            include_periods: Include dietary period annotations (default: True)
            
        Returns:
            List of dictionaries with weight log + week info + period markers
        """
        from repositories.dietary_period_repository import DietaryPeriodRepository
        
        # Get weight history (already in descending order)
        history = self.get_weight_history(user_id, days)
        
        if not history:
            return []
        
        # Get active dietary periods if requested
        periods = []
        if include_periods:
            period_repo = DietaryPeriodRepository(self.db_path)
            periods = period_repo.find_all(user_id)
        
        # Enrich each log entry
        enriched_history = []
        current_week = None
        
        for log in history:
            # Add week information
            week_info = get_week_info(log['date'])
            
            # Mark if this is the first entry of a new week
            is_week_start = (current_week != week_info['week_number'])
            current_week = week_info['week_number']
            
            # Find periods containing this date
            active_periods, period_markers = self._find_periods_for_date(log['date'], periods)
            
            enriched_entry = {
                **log,
                'week_number': week_info['week_number'],
                'week_start_date': week_info['week_start_date'],
                'week_label': week_info['week_label'],
                'year': week_info['year'],
                'is_week_start': is_week_start,
                'active_periods': active_periods,
                'period_markers': period_markers,
                'has_periods': len(active_periods) > 0
            }
            
            enriched_history.append(enriched_entry)
        
        return enriched_history
