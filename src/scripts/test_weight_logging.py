"""
Quick test script to verify WeightLogRepository and WeightLogService work correctly.
Run with: poetry run python src/scripts/test_weight_logging.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from repositories.weightlog_repository import WeightLogRepository
from services.weightlog_service import WeightLogService
from datetime import datetime, timedelta

DB_PATH = Path(__file__).parent.parent / 'data' / 'laihdutanyt.db'

def test_weight_logging():
    """Test weight logging functionality"""
    print("=" * 60)
    print("Testing Weight Logging System")
    print("=" * 60)
    
    # Initialize services
    weightlog_repo = WeightLogRepository(str(DB_PATH))
    weightlog_service = WeightLogService(str(DB_PATH))
    
    # Use the demo user (assuming user_id from demo data)
    test_user_id = "test-user-123"  # This should be replaced with actual user_id
    
    print("\n1. Testing Weight Log Creation...")
    today = datetime.now().date().isoformat()
    result = weightlog_service.log_weight(
        user_id=test_user_id,
        date_str=today,
        weight=75.5,
        notes="Morning weight after breakfast"
    )
    
    if result['success']:
        print(f"   ✅ Weight logged successfully!")
        print(f"   Log ID: {result['log'].get('log_id')}")
    else:
        print(f"   ❌ Failed: {result.get('error')}")
    
    print("\n2. Testing Get Latest Weight...")
    latest_weight = weightlog_service.get_latest_weight(test_user_id)
    if latest_weight:
        print(f"   ✅ Latest weight: {latest_weight} kg")
    else:
        print(f"   ℹ️  No weight logs found for user")
    
    print("\n3. Testing Weight History...")
    history = weightlog_service.get_weight_history(test_user_id, days=30)
    print(f"   ✅ Found {len(history)} weight logs in last 30 days")
    
    if history:
        print(f"\n   Recent entries:")
        for log in history[:5]:  # Show first 5
            print(f"   - {log['date']}: {log['weight']} kg" + 
                  (f" ({log['notes']})" if log.get('notes') else ""))
    
    print("\n4. Testing Weight Change Calculation...")
    weekly_change = weightlog_service.calculate_weight_change(test_user_id, days_back=7)
    if weekly_change:
        print(f"   ✅ Weekly change calculated:")
        print(f"   - Current: {weekly_change['current_weight']} kg ({weekly_change['current_date']})")
        print(f"   - Previous: {weekly_change['start_weight']} kg ({weekly_change['start_date']})")
        print(f"   - Change: {weekly_change['weight_change']:+.1f} kg ({weekly_change['change_percentage']:+.1f}%)")
        print(f"   - Trend: {weekly_change['trend'].upper()}")
    else:
        print(f"   ℹ️  Insufficient data for weekly change calculation")
    
    print("\n5. Testing Progress Summary...")
    summary = weightlog_service.get_progress_summary(test_user_id)
    if summary['has_data']:
        print(f"   ✅ Progress summary generated:")
        print(f"   - Current weight: {summary['current_weight']} kg")
        print(f"   - Total logs: {summary['total_logs']}")
        
        if summary.get('goal_progress'):
            goal = summary['goal_progress']
            print(f"   - Goal: Lose {goal['target_loss']} kg")
            print(f"   - Progress: {goal['actual_loss']:.1f} kg ({goal['progress_percentage']:.1f}%)")
    else:
        print(f"   ℹ️  {summary['message']}")
    
    print("\n6. Testing Repository Methods...")
    print(f"   - Total logs count: {weightlog_repo.count_logs(test_user_id)}")
    
    latest_log = weightlog_repo.find_latest(test_user_id)
    if latest_log:
        print(f"   - Latest log date: {latest_log['date']}")
        print(f"   - Latest log weight: {latest_log['weight']} kg")
    
    print("\n" + "=" * 60)
    print("✅ Weight Logging System Tests Complete!")
    print("=" * 60)

if __name__ == '__main__':
    try:
        test_weight_logging()
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
