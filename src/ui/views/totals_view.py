"""
Daily Totals Views - Food and Activity daily aggregations
Uses services for business logic with date highlighting
"""

import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

from services import FoodService, ActivityService, UserService

if TYPE_CHECKING:
    from ui.app import LaihdutanytApp


class Dashboard_daily_foods_totals(tk.Toplevel):
    """Daily Food Totals Dashboard with date highlighting"""
    
    def __init__(self, master: 'LaihdutanytApp', user_service: UserService,
                 food_service: FoodService, username: str, user_id: str):
        super().__init__(master)
        self.title(f"Daily Food Totals - {username}")
        self.master = master
        self.username = username
        self.user_id = user_id
        self.food_service = food_service
        
        # Get user info
        user_summary = user_service.get_user_summary(username)
        
        # User info header
        info_frame = tk.Frame(self, bg="#e8f4f8", relief="ridge", borderwidth=2)
        info_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(info_frame, text=f"Daily Food Totals - {username}", font=("Arial", 16, "bold"), bg="#e8f4f8").pack(pady=5)
        
        info_text = f"Weight: {user_summary['weight']}kg | Target: {user_summary['target']}kg | Daily Goal: {user_summary['kcal_min']}-{user_summary['kcal_max']} kcal"
        tk.Label(info_frame, text=info_text, font=("Arial", 11), bg="#e8f4f8").pack(pady=5)
        
        # Navigation buttons
        nav_frame = tk.Frame(self)
        nav_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Button(nav_frame, text="← Back to Main Menu", command=self._back_to_menu, 
                 font=("Arial", 12), bg="#d0d0d0").pack(side="left", padx=5)
        tk.Button(nav_frame, text="Refresh", command=self.refresh_totals, 
                 font=("Arial", 12), bg="#90caf9").pack(side="right", padx=5)
        
        # Treeview styling
        style = ttk.Style()
        style.configure("Custom.Treeview", font=("Arial", 11), rowheight=25)
        style.configure("Custom.Treeview.Heading", font=("Arial", 12, "bold"))
        
        # Create treeview
        columns = ("date", "total_kcal", "entries")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse", style="Custom.Treeview")
        self.tree.heading("date", text="Date")
        self.tree.heading("total_kcal", text="Total Calories (kcal)")
        self.tree.heading("entries", text="# of Entries")
        
        self.tree.column("date", width=180, anchor="center")  # Wider for "📍 TODAY"
        self.tree.column("total_kcal", width=180, anchor="center")
        self.tree.column("entries", width=120, anchor="center")
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configure tags for date highlighting
        self.tree.tag_configure('past', background='white')
        self.tree.tag_configure('today', background='#ffffcc', font=("Arial", 11, "bold"))
        self.tree.tag_configure('future', background='#e8f5e9')
        
        self.refresh_totals()
    
    def _back_to_menu(self):
        self.destroy()
    
    def refresh_totals(self):
        """Refresh totals using service layer with date categorization"""
        for r in self.tree.get_children():
            self.tree.delete(r)
        
        # Get data from service (includes date categorization)
        totals = self.food_service.get_daily_food_totals(self.user_id)
        
        for item in totals:
            self.tree.insert("", "end", values=(item['date'], item['total_kcal'], item['entries']), 
                           tags=(item['category'],))


class Dashboard_daily_activities_totals(tk.Toplevel):
    """Daily Activity Totals Dashboard with date highlighting"""
    
    def __init__(self, master: 'LaihdutanytApp', user_service: UserService,
                 activity_service: ActivityService, username: str, user_id: str):
        super().__init__(master)
        self.title(f"Daily Activity Totals - {username}")
        self.master = master
        self.username = username
        self.user_id = user_id
        self.activity_service = activity_service
        
        # Get user info
        user_summary = user_service.get_user_summary(username)
        
        # User info header
        info_frame = tk.Frame(self, bg="#e8f8e8", relief="ridge", borderwidth=2)
        info_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(info_frame, text=f"Daily Activity Totals - {username}", font=("Arial", 16, "bold"), bg="#e8f8e8").pack(pady=5)
        
        info_text = f"Weight: {user_summary['weight']}kg | Activity Level: {user_summary['activity_level']} | Target: {user_summary['target']}kg"
        tk.Label(info_frame, text=info_text, font=("Arial", 11), bg="#e8f8e8").pack(pady=5)
        
        # Navigation buttons
        nav_frame = tk.Frame(self)
        nav_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Button(nav_frame, text="← Back to Main Menu", command=self._back_to_menu, 
                 font=("Arial", 12), bg="#d0d0d0").pack(side="left", padx=5)
        tk.Button(nav_frame, text="Refresh", command=self.refresh_totals, 
                 font=("Arial", 12), bg="#a5d6a7").pack(side="right", padx=5)
        
        # Treeview styling
        style = ttk.Style()
        style.configure("Activity.Treeview", font=("Arial", 11), rowheight=25)
        style.configure("Activity.Treeview.Heading", font=("Arial", 12, "bold"))
        
        # Create treeview
        columns = ("date", "total_kcal_burned", "entries")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse", style="Activity.Treeview")
        self.tree.heading("date", text="Date")
        self.tree.heading("total_kcal_burned", text="Calories Burned (kcal)")
        self.tree.heading("entries", text="Activities")
        
        self.tree.column("date", width=180, anchor="center")  # Wider for "📍 TODAY"
        self.tree.column("total_kcal_burned", width=200, anchor="center")
        self.tree.column("entries", width=120, anchor="center")
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configure tags
        self.tree.tag_configure('past', background='white')
        self.tree.tag_configure('today', background='#ffffcc', font=("Arial", 11, "bold"))
        self.tree.tag_configure('future', background='#e8f5e9')
        
        self.refresh_totals()
    
    def _back_to_menu(self):
        self.destroy()
    
    def refresh_totals(self):
        """Refresh totals using service layer with date categorization"""
        for r in self.tree.get_children():
            self.tree.delete(r)
        
        # Get data from service (includes date categorization)
        totals = self.activity_service.get_daily_activity_totals(self.user_id)
        
        for item in totals:
            self.tree.insert("", "end", values=(item['date'], item['total_kcal'], item['entries']), 
                           tags=(item['category'],))
