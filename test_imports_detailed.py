import sys
import traceback
sys.path.insert(0, 'src')

print("Testing imports step by step...")

try:
    print("1. Importing tkinter...")
    import tkinter as tk
    from tkinter import messagebox, ttk
    print("✅ tkinter OK")
    
    print("2. Importing datetime...")
    from datetime import date
    print("✅ datetime OK")
    
    print("3. Importing typing...")
    from typing import TYPE_CHECKING
    print("✅ typing OK")
    
    print("4. Importing ActivityService...")
    from services.activity_service import ActivityService
    print("✅ ActivityService OK")
    
    print("5. Importing UserService...")
    from services.user_service import UserService
    print("✅ UserService OK")
    
    print("6. Now importing full activity_view module...")
    import ui.views.activity_view as av
    print("✅ activity_view imported")
    print("   Classes found:", [x for x in dir(av) if not x.startswith('_')])
    
except Exception as e:
    print(f"❌ Error at step: {e}")
    traceback.print_exc()
