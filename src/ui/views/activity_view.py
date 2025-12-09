"""
Activity Dashboard View - Activity logging interface
Uses ActivityService for all business logic
"""

import tkinter as tk
from tkinter import messagebox, ttk
from datetime import date
from typing import TYPE_CHECKING

from services.activity_service import ActivityService
from services.user_service import UserService

if TYPE_CHECKING:
    from ui.app import LaihdutanytApp


class ActivityLogFrame(tk.Frame):
    """Activity logging form component"""
    
    def __init__(self, master, activity_service: ActivityService, user_id: str):
        super().__init__(master)
        self.activity_service = activity_service
        self.user_id = user_id
        
        # Date input
        self.date_var = tk.StringVar(value=date.today().strftime("%Y-%m-%d"))
        
        # Activity dropdown
        self.activity_var = tk.StringVar()
        
        # Count input
        self.count_var = tk.IntVar(value=1)
        
        # Logs list
        self.logs_list = tk.Listbox(self, height=10, font=("Arial", 10))
        
        self._setup_ui()
        self._load_activity_list()
        self._load_todays_logs()
    
    def _setup_ui(self):
        """Setup the UI components"""
        topframe = tk.Frame(self)
        topframe.pack(fill="x", padx=10, pady=10)
        
        tk.Label(topframe, text="Activity", font=("Arial", 11)).grid(row=0, column=0, sticky="w", padx=5)
        self.activity_cb = ttk.Combobox(topframe, textvariable=self.activity_var, width=30, font=("Arial", 11))
        self.activity_cb.grid(row=0, column=1, padx=5)
        
        tk.Label(topframe, text="Count", font=("Arial", 11)).grid(row=1, column=0, sticky="w", padx=5)
        tk.Spinbox(topframe, from_=1, to=100, textvariable=self.count_var, width=10, font=("Arial", 11)).grid(row=1, column=1, sticky="w", padx=5)
        
        tk.Label(topframe, text="Date (YYYY-MM-DD)", font=("Arial", 11)).grid(row=2, column=0, sticky="w", padx=5)
        tk.Entry(topframe, textvariable=self.date_var, width=15, font=("Arial", 11)).grid(row=2, column=1, sticky="w", padx=5)
        
        tk.Button(topframe, text="Add Activity", command=self._add_activity, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", padx=20, pady=5).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Today activities list
        listframe = tk.Frame(self)
        listframe.pack(fill="both", expand=True, padx=10, pady=5)
        
        tk.Label(listframe, text="Today Activity Log:", font=("Arial", 12, "bold")).pack(anchor="w")
        
        self.logs_list.pack(fill="both", expand=True, pady=5)
    
    def _load_activity_list(self):
        """Load available activities into dropdown"""
        activities = self.activity_service.get_activity_display_list()
        self.activity_cb["values"] = activities
        if activities:
            self.activity_cb.current(0)
    
    def _load_todays_logs(self):
        """Load today activity logs"""
        self.logs_list.delete(0, tk.END)
        today = date.today().strftime("%Y-%m-%d")
        logs = self.activity_service.get_activity_logs_by_date(self.user_id, today)
        
        for log in logs:
            self.logs_list.insert(tk.END, log)
    
    def _add_activity(self):
        """Add new activity log"""
        activity_str = self.activity_var.get()
        count = self.count_var.get()
        date_str = self.date_var.get()
        
        if not activity_str:
            messagebox.showwarning("Warning", "Please select an activity")
            return
        
        try:
            self.activity_service.log_activity(self.user_id, activity_str, count, date_str)
            messagebox.showinfo("Success", f"Added {count}x {activity_str} for {date_str}")
            self._load_todays_logs()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add activity: {str(e)}")


class Dashboard_activity(tk.Toplevel):
    """Main Activity Dashboard window"""
    
    def __init__(self, master: "LaihdutanytApp", user_service: UserService, activity_service: ActivityService, username: str, user_id: str):
        super().__init__(master)
        self.title(f"Activity Dashboard - {username}")
        self.master = master
        self.username = username
        self.user_id = user_id
        self.activity_service = activity_service
        
        # Get user info
        user_summary = user_service.get_user_summary(username)
        
        # User info header
        info_frame = tk.Frame(self, bg="#e8f8e8", relief="ridge", borderwidth=2)
        info_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(info_frame, text=f"Daily Activities - {username}", font=("Arial", 16, "bold"), bg="#e8f8e8").pack(pady=5)
        
        info_text = f"Weight: {user_summary['weight']}kg | Activity Level: {user_summary['activity_level']} | Target: {user_summary['target']}kg"
        tk.Label(info_frame, text=info_text, font=("Arial", 11), bg="#e8f8e8").pack(pady=5)
        
        # Navigation buttons
        nav_frame = tk.Frame(self)
        nav_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Button(nav_frame, text="Back to Main Menu", command=self._back_to_menu, font=("Arial", 12), bg="#d0d0d0").pack(side="left", padx=5)
        tk.Button(nav_frame, text="View All Activity Logs", command=self._open_all_logs, font=("Arial", 12), bg="#a5d6a7").pack(side="right", padx=5)
        
        # Activity logging frame
        self.activity_frame = ActivityLogFrame(self, activity_service, user_id)
        self.activity_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    def _back_to_menu(self):
        self.destroy()
    
    def _open_all_logs(self):
        """Open all activity logs window"""
        from ui.views.logs_view import AllActivityLogsWindow
        AllActivityLogsWindow(self, self.activity_service, self.user_id)
