"""
Demo script showing dietary period tracking and enhanced weight logging features.
Run with: poetry run python src/scripts/demo_period_tracking.py
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.dietary_period_service import DietaryPeriodService
from services.weightlog_service import WeightLogService

DB_PATH = Path(__file__).parent.parent / 'data' / 'laihdutanyt.db'

def demo_period_tracking():
    """Demonstrate dietary period tracking features"""
    print("=" * 70)
    print(" Dietary Period Tracking & Enhanced Weight Logging Demo")
    print("=" * 70)
    
    period_service = DietaryPeriodService(str(DB_PATH))
    weight_service = WeightLogService(str(DB_PATH))
    
    # Use demo user (you'll need to adjust this to actual user_id)
    test_user = "test-user-123"
    
    print("\n1️⃣  SUGGESTED DIETARY PROTOCOLS")
    print("-" * 70)
    suggestions = period_service.get_suggested_protocols()
    
    for i, protocol in enumerate(suggestions, 1):
        print(f"\n{i}. {protocol['name']}")
        print(f"   Type: {protocol['type']}")
        print(f"   Description: {protocol['description']}")
        print(f"   Suggested duration: {protocol['example_duration']}")
    
    print("\n\n2️⃣  CREATE A NEW DIETARY PERIOD")
    print("-" * 70)
    
    # Calculate start date (10 days ago)
    start_date = (datetime.now() - timedelta(days=10)).date().isoformat()
    
    result = period_service.create_period(
        user_id=test_user,
        start_date=start_date,
        period_name="No Evening Eating After 7pm",
        description="Stop eating after 7pm to allow 12+ hour overnight fasting",
        protocol_type="time_restricted",
        notes="Testing this approach for 3 weeks"
    )
    
    if result['success']:
        print(f"✅ Period created successfully!")
        print(f"   Period ID: {result['period']['period_id']}")
        print(f"   Name: {result['period']['period_name']}")
        print(f"   Started: {result['period']['start_date']}")
        print(f"   Status: Ongoing")
        period_id = result['period']['period_id']
    else:
        print(f"❌ Failed: {result['error']}")
        return
    
    print("\n\n3️⃣  WEIGHT HISTORY WITH WEEK NUMBERS & PERIOD ANNOTATIONS")
    print("-" * 70)
    
    history = weight_service.get_weight_history_with_weeks(
        user_id=test_user,
        days=30,
        include_periods=True
    )
    
    if not history:
        print("ℹ️  No weight logs found for this user")
        print("   (Demo data generator created logs for a different user)")
        return
    
    print(f"\nShowing {len(history)} weight log entries (descending order):\n")
    
    current_week = None
    for log in history[:15]:  # Show first 15 entries
        # Week separator
        if log['is_week_start']:
            print("\n" + "=" * 70)
            print(f"  {log['week_label']} (Week starts: {log['week_start_date']})")
            print("=" * 70)
        
        # Date and weight (bold if week start)
        bold_start = "**" if log['is_week_start'] else "  "
        bold_end = "**" if log['is_week_start'] else ""
        
        print(f"{bold_start}{log['date']}  {log['weight']} kg{bold_end}", end="")
        if log.get('notes'):
            print(f"  ({log['notes']})", end="")
        print()
        
        # Period markers (START/END)
        for marker in log.get('period_markers', []):
            print(f"    {marker}")
        
        # Active periods
        if log.get('has_periods'):
            for period_name in log['active_periods']:
                print(f"    📍 {period_name}")
    
    print("\n\n4️⃣  PERIOD SUMMARY & EFFECTIVENESS")
    print("-" * 70)
    
    summary = period_service.get_period_summary(period_id)
    
    if summary:
        print(f"\nPeriod: {summary['period_name']}")
        print(f"Duration: {summary['duration_days']} days")
        print(f"Status: {'Ongoing' if summary['is_ongoing'] else 'Completed'}")
        
        if summary['weight_change']:
            wc = summary['weight_change']
            print(f"\nWeight Change:")
            print(f"  Start weight: {wc['start_weight']} kg ({summary['start_date']})")
            print(f"  Current weight: {wc['end_weight']} kg")
            print(f"  Total change: {wc['change']:+.1f} kg")
            print(f"  Per week: {wc['change_per_week']:+.2f} kg/week")
            
            if wc['change'] < 0:
                print(f"  ✅ Successfully losing weight during this period!")
            elif wc['change'] > 0:
                print(f"  ⚠️  Gaining weight during this period")
            else:
                print(f"  ➖ Weight stable during this period")
        else:
            print("\nℹ️  Not enough weight data to calculate effectiveness")
    
    print("\n\n5️⃣  ACTIVE PERIODS")
    print("-" * 70)
    
    active = period_service.get_active_periods(test_user)
    
    if active:
        print(f"\n{len(active)} active period(s):\n")
        for period in active:
            print(f"🟢 {period['period_name']}")
            print(f"   Started: {period['start_date']}")
            if period['description']:
                print(f"   Description: {period['description']}")
    else:
        print("\nNo active periods")
    
    print("\n\n6️⃣  WEEK INFO HELPER")
    print("-" * 70)
    
    from services.weightlog_service import get_week_info
    
    today = datetime.now().date().isoformat()
    week_info = get_week_info(today)
    
    print(f"\nToday ({today}):")
    print(f"  Week number: {week_info['week_number']}")
    print(f"  Week starts: {week_info['week_start_date']} (Monday)")
    print(f"  Year: {week_info['year']}")
    print(f"  Label: {week_info['week_label']}")
    
    print("\n" + "=" * 70)
    print("✅ Demo complete!")
    print("=" * 70)
    print("\nKey Features Demonstrated:")
    print("  ✅ Dietary period creation with validation")
    print("  ✅ Weight history with week numbering")
    print("  ✅ Period annotations on weight logs")
    print("  ✅ Period start/end markers (▶/⏹)")
    print("  ✅ Descending order (most recent first)")
    print("  ✅ Week start indication for bold formatting")
    print("  ✅ Period effectiveness tracking")
    print("  ✅ Suggested protocol templates")

if __name__ == '__main__':
    try:
        demo_period_tracking()
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
