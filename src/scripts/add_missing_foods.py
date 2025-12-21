"""
Add missing foods needed for demo data generation.
Based on requirements section 5.2.1
"""
import sqlite3
import uuid
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / 'data' / 'laihdutanyt.db'

# Foods from requirements v3, section 5.2.1 that are missing
MISSING_FOODS = [
    {
        'name': 'Whole Wheat Bread (slice)',
        'kcal_per_portion': 69,
        'carbs_per_portion': 12,
        'protein_per_portion': 3.6,
        'fat_per_portion': 1.1
    },
    {
        'name': 'Salmon (100g)',
        'kcal_per_portion': 206,
        'carbs_per_portion': 0,
        'protein_per_portion': 22,
        'fat_per_portion': 13
    },
    {
        'name': 'Broccoli',
        'kcal_per_portion': 55,
        'carbs_per_portion': 11,
        'protein_per_portion': 3.7,
        'fat_per_portion': 0.6
    },
    {
        'name': 'Rice (cooked)',
        'kcal_per_portion': 130,
        'carbs_per_portion': 28,
        'protein_per_portion': 2.7,
        'fat_per_portion': 0.3
    },
    {
        'name': 'Almonds (30g)',
        'kcal_per_portion': 170,
        'carbs_per_portion': 6,
        'protein_per_portion': 6,
        'fat_per_portion': 15
    }
]

def add_missing_foods():
    """Add missing foods to the database"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    print("Adding missing foods to database...")
    
    for food in MISSING_FOODS:
        # Check if food already exists
        cur.execute("SELECT name FROM food WHERE name = ?", (food['name'],))
        if cur.fetchone():
            print(f"  ⏭️  {food['name']} already exists")
            continue
        
        # Add food
        food_id = str(uuid.uuid4())
        cur.execute("""
            INSERT INTO food (food_id, name, kcal_per_portion, 
                            carbs_per_portion, protein_per_portion, fat_per_portion)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            food_id,
            food['name'],
            food['kcal_per_portion'],
            food['carbs_per_portion'],
            food['protein_per_portion'],
            food['fat_per_portion']
        ))
        print(f"  ✅ Added {food['name']} ({food['kcal_per_portion']} kcal)")
    
    conn.commit()
    conn.close()
    
    print("\n✓ All missing foods added successfully!")

if __name__ == '__main__':
    add_missing_foods()
