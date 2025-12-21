"""
Activity Dashboard View - Activity logging interface
Uses ActivityService for all business logic
"""

import tkinter as tk
from tkinter import messagebox, ttk
from datetime import date
from typing import TYPE_CHECKING

""" from services.activity_service import ActivityService
from services.user_service import UserService """

from services import ActivityService, UserService

if TYPE_CHECKING:
    from ui.app import LaihdutanytApp


class ActivityLogFrame(tk.Frame):
    """Activity logging form component"""
    
    def __init__(self, master, activity_service: ActivityService, user_id: str):
        super().__init__(master)
        self.activity_service = activity_service
        self.user_id = user_id
        
        # Date input
        self.date_var = tk.StringVar(value=date.today().strftime('%Y-%m-%d'))
        
        # Activity dropdown
        self.activity_var = tk.StringVar()
        
        # Count input
        self.count_var = tk.IntVar(value=1)
        
        # Logs list with improved spacing
        self.logs_list = tk.Listbox(self, height=12, font=("Arial", 12))
        
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
        
        tk.Button(topframe, text="Add Activity", command=self._add_activity, font=("Arial", 11, "bold"), bg="#4CAF50").grid(row=3, column=0, columnspan=2, pady=10)
        
        # Today's logs section
        tk.Label(self, text="Today's Activity Log", font=("Arial", 12, "bold")).pack(pady=5)
        
        # Add calculation info
        calc_info = tk.Label(self, text="📊 Calories burned calculated per 1000 units (e.g., steps)", 
                            font=("Arial", 9, "italic"), fg="#1976d2")
        calc_info.pack()
        
        # Add info about future events
        info_label = tk.Label(self, text="ℹ️ Future planned activities will appear in 'View All Activity Logs'", 
                             font=("Arial", 9, "italic"), fg="#555")
        info_label.pack()
        
        self.logs_list.pack(fill="both", expand=True, padx=10, pady=5)
    
    def _load_activity_list(self):
        """Load available activities into dropdown"""
        # Load names only for clean display
        display_names = self.activity_service.get_activity_name_only_list()
        self.activity_cb['values'] = display_names
        if display_names:
            self.activity_cb.current(0)
    
    def _load_todays_logs(self):
        """Load today's activity logs"""
        self.logs_list.delete(0, tk.END)
        today = date.today().strftime('%Y-%m-%d')
        logs = self.activity_service.get_activity_logs_by_date(self.user_id, today)
        
        if not logs:
            self.logs_list.insert(tk.END, "No activities logged for today")
            return
        
        for log_text in logs:
            self.logs_list.insert(tk.END, log_text)
    
    def _add_activity(self):
        """Add new activity log with smart feedback"""
        from datetime import date as date_class
        
        activity_name = self.activity_var.get().strip()
        count = self.count_var.get()
        date_str = self.date_var.get()
        
        if not activity_name:
            messagebox.showwarning("Input Required", "Please select an activity", parent=self)
            return
        
        try:
            # Get activity ID by name
            activity_id = self.activity_service.get_activity_id_by_name(activity_name)
            
            # Log activity using ID (create selection string for compatibility)
            activity_selection = f"{activity_name}|{activity_id}"
            self.activity_service.log_activity(self.user_id, activity_selection, count, date_str)
            
            # Show feedback only for future dates
            today = date_class.today().strftime('%Y-%m-%d')
            if date_str > today:
                messagebox.showinfo("Planned!", 
                                  f"{activity_name} scheduled for {date_str}\n\nView in 'All Activity Logs'", 
                                  parent=self)
            
            self._load_todays_logs()
            
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self)


class Dashboard_activity(tk.Toplevel):
    """Main Activity Dashboard window"""
    
    def __init__(self, master: 'LaihdutanytApp', user_service: UserService,
                 activity_service: ActivityService, username: str, user_id: str):
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
        
        tk.Button(nav_frame, text="← Back to Main Menu", command=self._back_to_menu, 
                 font=("Arial", 12), bg="#d0d0d0").pack(side="left", padx=5)
        tk.Button(nav_frame, text="View All Activity Logs", command=self._open_all_logs, 
                 font=("Arial", 12), bg="#a5d6a7").pack(side="right", padx=5)
        
        # Activity logging frame
        self.activity_frame = ActivityLogFrame(self, activity_service, user_id)
        self.activity_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    def _back_to_menu(self):
        self.destroy()
    
    def _open_all_logs(self):
        """Open all activity logs window"""
        from ui.views.logs_view import AllActivityLogsWindow
        AllActivityLogsWindow(self, self.activity_service, self.user_id)
