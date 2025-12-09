"""
Laihdutanyt Application - Main Entry Point
Refactored version with layered architecture
"""

import os
from tkinter import messagebox
from ui.app import LaihdutanytApp

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "data", "laihdutanyt.db")

def main():
    """Main entry point for the application"""
    if not os.path.exists(DB_PATH):
        messagebox.showerror(
            "Missing database",
            f"Database not found: {DB_PATH}\nRun create_db.py first."
        )
        return
    
    app = LaihdutanytApp(DB_PATH)
    app.mainloop()

if __name__ == "__main__":
    main()
