"""
Food Dashboard View - Food logging interface
Uses FoodService for all business logic
"""

import tkinter as tk
from tkinter import messagebox, ttk
from datetime import date
from typing import TYPE_CHECKING

from services import FoodService, UserService

if TYPE_CHECKING:
    from ui.app import LaihdutanytApp


class FoodLogFrame(tk.Frame):
    """Food logging form component"""
    
    def __init__(self, master, food_service: FoodService, user_id: str):
        super().__init__(master)
        self.food_service = food_service
        self.user_id = user_id
        
        # Date input
        self.date_var = tk.StringVar(value=date.today().strftime('%Y-%m-%d'))
        
        # Food dropdown
        self.food_var = tk.StringVar()
        
        # Portion input
        self.portion_var = tk.DoubleVar(value=100.0)
        
        # Logs list with improved spacing
        self.logs_list = tk.Listbox(self, height=10, font=("Arial", 12))
        
        self._setup_ui()
        self._load_food_list()
        self._load_todays_logs()
    
    def _setup_ui(self):
        """Setup the UI components"""
        topframe = tk.Frame(self)
        topframe.pack(fill="x", padx=10, pady=10)
        
        tk.Label(topframe, text="Food", font=("Arial", 11)).grid(row=0, column=0, sticky="w", padx=5)
        self.food_cb = ttk.Combobox(topframe, textvariable=self.food_var, width=30, font=("Arial", 11))
        self.food_cb.grid(row=0, column=1, padx=5)
        
        tk.Label(topframe, text="Portion (g)", font=("Arial", 11)).grid(row=1, column=0, sticky="w", padx=5)
        tk.Entry(topframe, textvariable=self.portion_var, width=10, font=("Arial", 11)).grid(row=1, column=1, sticky="w", padx=5)
        
        tk.Label(topframe, text="Date", font=("Arial", 11)).grid(row=2, column=0, sticky="w", padx=5)
        tk.Entry(topframe, textvariable=self.date_var, width=15, font=("Arial", 11)).grid(row=2, column=1, sticky="w", padx=5)
        
        tk.Button(topframe, text="Add Food", command=self._on_add, font=("Arial", 11), bg="#90caf9").grid(row=3, column=0, columnspan=2, pady=10)

        # Today's logs section
        tk.Label(self, text="Today's Food Log", font=("Arial", 12, "bold")).pack(pady=5)
        
        # Add calculation info
        calc_info = tk.Label(self, text="📊 Calories calculated per 100g portions", 
                            font=("Arial", 9, "italic"), fg="#2e7d32")
        calc_info.pack()
        
        # Add info about future events
        info_label = tk.Label(self, text="ℹ️ Future planned meals will appear in 'View All Food Logs'", 
                             font=("Arial", 9, "italic"), fg="#555")
        info_label.pack()
        
        self.logs_list.pack(fill="both", expand=True, padx=10, pady=5)
    
    def _load_food_list(self):
        """Load food list from service"""
        # Load names only for clean display
        display_names = self.food_service.get_food_name_only_list()
        self.food_cb["values"] = display_names
        if display_names:
            self.food_cb.current(0)
    
    def _load_todays_logs(self):
        """Load today's logs using service"""
        self.logs_list.delete(0, tk.END)
        date_str = self.date_var.get()
        logs = self.food_service.get_food_logs_by_date(self.user_id, date_str)
        
        if not logs:
            self.logs_list.insert(tk.END, "No foods logged for this date")
            return
        
        for log_text in logs:
            self.logs_list.insert(tk.END, log_text)
    
    def _on_add(self):
        """Handle add food button with smart feedback"""
        from datetime import date as date_class
        
        try:
            food_name = self.food_var.get().strip()
            portion = self.portion_var.get()
            date_str = self.date_var.get()
            
            if not food_name:
                messagebox.showwarning("Input Required", "Please select a food", parent=self)
                return
            
            # Get food ID by name
            food_id = self.food_service.get_food_id_by_name(food_name)
            
            # Log food using ID (create selection string for compatibility)
            food_selection = f"{food_name}|{food_id}"
            self.food_service.log_food(self.user_id, food_selection, portion, date_str)
            
            # Show feedback only for future dates
            today = date_class.today().strftime('%Y-%m-%d')
            if date_str > today:
                messagebox.showinfo("Planned!", 
                                  f"{food_name} scheduled for {date_str}\n\nView in 'All Food Logs'", 
                                  parent=self)
            
            self._load_todays_logs()
            
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self)


class Dashboard_food(tk.Toplevel):
    """Main Food Dashboard window"""
    
    def __init__(self, master: 'LaihdutanytApp', user_service: UserService,
                 food_service: FoodService, username: str, user_id: str):
        super().__init__(master)
        self.title(f"Food Dashboard - {username}")
        self.master = master
        self.username = username
        self.user_id = user_id
        self.food_service = food_service
        
        # Get user info
        user_summary = user_service.get_user_summary(username)
        
        # User info header
        info_frame = tk.Frame(self, bg="#e8f4f8", relief="ridge", borderwidth=2)
        info_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(info_frame, text=f"Daily Food Intake - {username}", font=("Arial", 16, "bold"), bg="#e8f4f8").pack(pady=5)
        
        info_text = f"Weight: {user_summary['weight']}kg | Target: {user_summary['target']}kg | Daily Goal: {user_summary['kcal_min']}-{user_summary['kcal_max']} kcal"
        tk.Label(info_frame, text=info_text, font=("Arial", 11), bg="#e8f4f8").pack(pady=5)
        
        # Navigation buttons
        nav_frame = tk.Frame(self)
        nav_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Button(nav_frame, text="← Back to Main Menu", command=self._back_to_menu, 
                 font=("Arial", 12), bg="#d0d0d0").pack(side="left", padx=5)
        tk.Button(nav_frame, text="View All Food Logs", command=self._open_all_logs, 
                 font=("Arial", 12), bg="#90caf9").pack(side="right", padx=5)
        
        # Food logging frame
        self.food_frame = FoodLogFrame(self, food_service, user_id)
        self.food_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    def _back_to_menu(self):
        self.destroy()
    
    def _open_all_logs(self):
        """Open all food logs window"""
        from ui.views.logs_view import AllFoodLogsWindow
        AllFoodLogsWindow(self, self.food_service, self.user_id)
