"""
Main Applicati    def __init__(self, db_path: str):
        super().__init__()
        self.title("Laihdutanyt - Weight Loss Tracker")
        self.geometry("420x750")  # Increased height for description panel
        self.db_path = db_path
        
        # Position main menu at left edge of screen by default
        self.geometry("420x750+10+50")  # x=10 (left edge), y=50 (top margin)
        
        # Initialize servicesow - Application Orchestrator
Manages window lifecycle, navigation, and view coordination
"""

import os
import tkinter as tk
from tkinter import messagebox, filedialog
import importlib

from services import UserService, FoodService, ActivityService, AdminService
from services.weightlog_service import WeightLogService
from services.dietary_period_service import DietaryPeriodService
from ui.views.login_view import LoginFrame


class LaihdutanytApp(tk.Tk):
    """Main application window and orchestrator"""
    
    def __init__(self, db_path: str):
        super().__init__()
        self.title("Laihdutanyt - Weight Loss Tracker")
        self.geometry("420x600")  # Increased height for description panel
        self.db_path = db_path
        
        # Initialize services
        self.user_service = UserService(db_path)
        self.food_service = FoodService(db_path)
        self.activity_service = ActivityService(db_path)
        self.admin_service = AdminService(db_path)
        self.weightlog_service = WeightLogService(db_path)
        self.dietary_period_service = DietaryPeriodService(db_path)
        
        # Current user state
        self.current_username = None
        self.current_user_id = None
        self.current_admin_username = None
        
        # Track open dashboard windows
        self.open_windows = {
            'food_dashboard': None,
            'activity_dashboard': None,
            'daily_food_totals': None,
            'daily_activity_totals': None,
            'all_food_logs': None,
            'all_activity_logs': None,
            'weight_dashboard': None,
            'periods_dashboard': None
        }
        
        # Window visibility state for hide/show toggle
        self.windows_hidden = False
        
        # Build UI
        self._build_menu()
        self._build_login()

    def _build_menu(self):
        """Build the application menu bar"""
        menubar = tk.Menu(self)
        
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Import Foods (CSV)", command=self._on_import_foods)
        filemenu.add_command(label="Import Activities (CSV)", command=self._on_import_activities)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.destroy)
        menubar.add_cascade(label="File", menu=filemenu)
        
        self.config(menu=menubar)

    def _on_import_foods(self):
        """Import foods from CSV file"""
        filename = filedialog.askopenfilename(
            title="Select foods CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not filename:
            return
        
        try:
            mod = importlib.import_module("scripts.import_foods")
            mod.import_csv(filename, self.db_path)
            messagebox.showinfo("Import complete", 
                              f"Imported foods from {os.path.basename(filename)}")
        except Exception as e:
            messagebox.showerror("Import error", f"Import failed: {e}")

    def _on_import_activities(self):
        """Import activities from CSV file"""
        filename = filedialog.askopenfilename(
            title="Select activities CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not filename:
            return
        
        try:
            mod = importlib.import_module("scripts.import_activities")
            mod.import_csv(filename, self.db_path)
            messagebox.showinfo("Import complete", 
                              f"Imported activities from {os.path.basename(filename)}")
        except Exception as e:
            messagebox.showerror("Import error", f"Import failed: {e}")

    def _build_login(self):
        """Build and show the login frame"""
        self.login_frame = LoginFrame(
            self,
            self.user_service,
            self.admin_service,
            self._on_user_login_success,
            self._on_admin_login_success
        )
        self.login_frame.pack(expand=True, fill="both")

    def _on_user_login_success(self, username: str):
        """Handle successful user login"""
        # Get user details from service
        user = self.user_service.get_user(username)
        if not user:
            messagebox.showerror("Error", "User record not found after login.")
            return
        
        # Store user information
        self.current_username = username
        self.current_user_id = user.user_id
        
        # Switch to user dashboard
        self.login_frame.pack_forget()
        self._build_user_dashboard()
        
        # Auto-open input dashboards on startup
        self.after(300, self._open_input_dashboards)

    def _on_admin_login_success(self, admin_username: str):
        """Handle successful admin login"""
        self.current_admin_username = admin_username
        
        # Switch to admin dashboard
        self.login_frame.pack_forget()
        self._build_admin_dashboard()

    def _build_user_dashboard(self):
        """Build the main user dashboard with button menu"""
        # Make main menu window always on top and resizable
        self.attributes('-topmost', True)
        self.resizable(True, True)
        
        # Clear any existing content
        for widget in self.winfo_children():
            widget.destroy()
        
        # Welcome label
        tk.Label(self, text=f"Welcome, {self.current_username}!", 
                font=("Arial", 15)).pack(pady=15)
        
        # Dashboard buttons
        tk.Button(self, text="View Food Logs",
                 command=lambda: self.button_pressed(1), 
                 font=("Arial", 15)).pack(pady=14)
        
        tk.Button(self, text="View Activity Logs",
                 command=lambda: self.button_pressed(2), 
                 font=("Arial", 15)).pack(pady=14)
        
        tk.Button(self, text="View Daily Foods Totals",
                 command=lambda: self.button_pressed(3), 
                 font=("Arial", 15)).pack(pady=14)
        
        tk.Button(self, text="View Daily Activities Totals",
                 command=lambda: self.button_pressed(4), 
                 font=("Arial", 15)).pack(pady=14)
        
        tk.Button(self, text="🏋️ Log Weight ⇅",
                 command=lambda: self.button_pressed(5), 
                 font=("Arial", 15), bg="#90caf9").pack(pady=14)
        
        tk.Button(self, text="📅 Manage Periods ⇅",
                 command=lambda: self.button_pressed(6), 
                 font=("Arial", 15), bg="#a5d6a7").pack(pady=14)
        
        # Window management buttons frame
        mgmt_frame = tk.Frame(self)
        mgmt_frame.pack(pady=5)
        
        tk.Button(mgmt_frame, text="� Dashboard Inputs", 
                 command=self._open_input_dashboards, 
                 font=("Arial", 13, "bold"), 
                 bg="#FFD700",
                 fg="#000000",
                 relief="raised",
                 borderwidth=2,
                 width=16).pack(side="left", padx=3)
        
        tk.Button(mgmt_frame, text="📚 Cascade", 
                 command=self._cascade_all_windows, 
                 font=("Arial", 13, "bold"), 
                 bg="#87CEEB",
                 fg="#000000",
                 relief="raised",
                 borderwidth=2,
                 width=12).pack(side="left", padx=3)
        
        self.hide_show_btn = tk.Button(mgmt_frame, text="👁 Hide All", 
                 command=self._toggle_hide_show_windows, 
                 font=("Arial", 13, "bold"), 
                 bg="#FFA500",
                 fg="#000000",
                 relief="raised",
                 borderwidth=2,
                 width=12)
        self.hide_show_btn.pack(side="left", padx=3)
        
        # Logout button
        tk.Button(self, text="🚪 Logout", 
                 command=self._logout, 
                 font=("Arial", 14, "bold"), 
                 bg="#FF6B6B",
                 fg="white",
                 relief="raised",
                 borderwidth=2,
                 width=20).pack(pady=15)

    def _logout(self):
        """Logout and return to login screen"""
        # Close all open dashboard windows
        for key, window in self.open_windows.items():
            if window and window.winfo_exists():
                window.destroy()
            self.open_windows[key] = None
        
        # Clear user data
        self.current_username = None
        self.current_user_id = None
        self.current_admin_username = None
        
        # Reset window attributes
        self.attributes('-topmost', False)
        self.geometry("420x600")
        
        # Clear dashboard
        for widget in self.winfo_children():
            widget.destroy()
        
        # Return to login
        self._build_login()

    def button_pressed(self, button_number: int):
        """Handle dashboard button presses"""
        positions = self._calculate_window_positions()
        
        # Adaptive window size based on screen height
        screen_height = self.winfo_screenheight()
        if screen_height < 1000:
            # Laptop screen
            win_height = min(700, screen_height - 150)
        else:
            win_height = 850
        win_width = 520
        
        if button_number == 1:
            # Food Dashboard
            if self.open_windows['food_dashboard'] is None or not self.open_windows['food_dashboard'].winfo_exists():
                from ui.views.food_view import Dashboard_food
                win = Dashboard_food(self, self.user_service, self.food_service, self.current_username, self.current_user_id)
                x, y = positions[1]  # Use numeric key
                win.geometry(f"{win_width}x{win_height}+{x}+{y}")
                self.open_windows['food_dashboard'] = win
            else:
                self.open_windows['food_dashboard'].lift()
        
        elif button_number == 2:
            # Activity Dashboard
            if self.open_windows['activity_dashboard'] is None or not self.open_windows['activity_dashboard'].winfo_exists():
                from ui.views.activity_view import Dashboard_activity
                win = Dashboard_activity(self, self.user_service, self.activity_service, self.current_username, self.current_user_id)
                x, y = positions[2]  # Use numeric key
                win.geometry(f"{win_width}x{win_height}+{x}+{y}")
                self.open_windows['activity_dashboard'] = win
            else:
                self.open_windows['activity_dashboard'].lift()
        
        elif button_number == 3:
            # Daily Food Totals
            if self.open_windows['daily_food_totals'] is None or not self.open_windows['daily_food_totals'].winfo_exists():
                from ui.views.totals_view import Dashboard_daily_foods_totals
                win = Dashboard_daily_foods_totals(self, self.user_service, self.food_service, self.current_username, self.current_user_id)
                x, y = positions[3]  # Use numeric key
                win.geometry(f"{win_width}x{win_height}+{x}+{y}")
                self.open_windows['daily_food_totals'] = win
            else:
                self.open_windows['daily_food_totals'].lift()
        
        elif button_number == 4:
            # Daily Activity Totals
            if self.open_windows['daily_activity_totals'] is None or not self.open_windows['daily_activity_totals'].winfo_exists():
                from ui.views.totals_view import Dashboard_daily_activities_totals
                win = Dashboard_daily_activities_totals(self, self.user_service, self.activity_service, self.current_username, self.current_user_id)
                x, y = positions[4]  # Use numeric key
                win.geometry(f"{win_width}x{win_height}+{x}+{y}")
                self.open_windows['daily_activity_totals'] = win
            else:
                self.open_windows['daily_activity_totals'].lift()
        
        elif button_number == 5:
            # Weight Logging Dashboard - Toggle expand/shrink
            try:
                if self.open_windows['weight_dashboard'] and self.open_windows['weight_dashboard'].winfo_exists():
                    win = self.open_windows['weight_dashboard']
                    current_geometry = win.geometry()
                    
                    # Check if currently minimized (card size ~500x400)
                    if '500' in current_geometry:
                        # Expand to full size
                        win.geometry("1050x750")
                    else:
                        # Shrink to card size
                        win.geometry("500x400")
                    
                    win.lift()
                    win.deiconify()
                    return
            except (KeyError, AttributeError, tk.TclError):
                pass
            
            # Create new window only if doesn't exist
            from ui.views.weight_view import DashboardWeight
            win = DashboardWeight(
                self, 
                self.weightlog_service, 
                self.dietary_period_service,
                self.current_username, 
                self.current_user_id
            )
            # Position relative to main window, like other dashboards
            x, y = positions.get(5, (self.winfo_x() + 10, self.winfo_y() + 50))
            win.geometry(f"1050x750+{x}+{y}")
            self.open_windows['weight_dashboard'] = win
        
        elif button_number == 6:
            # Dietary Period Management Dashboard - Toggle expand/shrink
            try:
                if self.open_windows['periods_dashboard'] and self.open_windows['periods_dashboard'].winfo_exists():
                    win = self.open_windows['periods_dashboard']
                    current_geometry = win.geometry()
                    
                    # Check if currently minimized (card size ~500x400)
                    if '500' in current_geometry:
                        # Expand to full size
                        win.geometry("1050x750")
                    else:
                        # Shrink to card size
                        win.geometry("500x400")
                    
                    win.lift()
                    win.deiconify()
                    return
            except (KeyError, AttributeError, tk.TclError):
                pass
            
            # Create new window only if doesn't exist
            from ui.views.period_view import DashboardPeriods
            win = DashboardPeriods(
                self,
                self.dietary_period_service,
                self.current_username,
                self.current_user_id,
                app=self  # Pass app reference for double-click navigation
            )
            # Position relative to main window, like other dashboards
            x, y = positions.get(6, (self.winfo_x() + 10, self.winfo_y() + 100))
            win.geometry(f"1050x750+{x}+{y}")
            self.open_windows['periods_dashboard'] = win

    def _open_all_food_logs_window(self):
        """Open the All Food Logs window programmatically"""
        if self.open_windows['all_food_logs'] is None or not self.open_windows['all_food_logs'].winfo_exists():
            from ui.views.logs_view import AllFoodLogsWindow
            win = AllFoodLogsWindow(self, self.food_service, self.current_user_id)
            self.open_windows['all_food_logs'] = win
        else:
            self.open_windows['all_food_logs'].lift()
    
    def _open_all_activity_logs_window(self):
        """Open the All Activity Logs window programmatically"""
        if self.open_windows['all_activity_logs'] is None or not self.open_windows['all_activity_logs'].winfo_exists():
            from ui.views.logs_view import AllActivityLogsWindow
            win = AllActivityLogsWindow(self, self.activity_service, self.current_user_id)
            self.open_windows['all_activity_logs'] = win
        else:
            self.open_windows['all_activity_logs'].lift()

    def _open_input_dashboards(self):
        """Open daily input dashboards (Food, Activity, Weight, Periods) in organized layout"""
        positions = self._calculate_window_positions()
        
        # Get adaptive window size
        screen_height = self.winfo_screenheight()
        if screen_height < 1000:
            win_height = min(700, screen_height - 150)
        else:
            win_height = 850
        win_width = 520
        
        # Open only the 4 input dashboards
        for i in [1, 2, 5, 6]:  # Food, Activity, Weight, Periods
            self.button_pressed(i)
        
        # Position them in grid layout
        # Input Dashboard mapping: Food/Activity on RIGHT (3-4), Weight/Periods on LEFT (1-2)
        input_window_map = {
            'periods_dashboard': 1,      # Top-left
            'weight_dashboard': 2,       # Bottom-left
            'food_dashboard': 3,         # Top-right
            'activity_dashboard': 4,     # Bottom-right
        }
        
        for key, window in self.open_windows.items():
            if window and window.winfo_exists() and key in input_window_map:
                window.deiconify()
                pos_key = input_window_map[key]
                x, y = positions[pos_key]
                
                # Periods and Weight dashboards use larger sizes
                if key == 'periods_dashboard':
                    window.geometry(f"1050x750+{x}+{y}")
                elif key == 'weight_dashboard':
                    window.geometry(f"1050x750+{x}+{y}")
                else:
                    # Food and Activity use card size
                    window.geometry(f"{win_width}x{win_height}+{x}+{y}")
                    
                window.lift()

    def _organize_all_windows(self):
        """Organize all open windows in grid layout"""
        positions = self._calculate_window_positions()
        
        # Get adaptive window size
        screen_height = self.winfo_screenheight()
        if screen_height < 1000:
            win_height = min(700, screen_height - 150)
        else:
            win_height = 850
        win_width = 520
        
        # Open all main dashboards first
        for i in range(1, 7):  # Include weight and periods dashboards
            self.button_pressed(i)
        
        # Also open the "All Logs" windows programmatically
        self._open_all_food_logs_window()
        self._open_all_activity_logs_window()
        
        # Reposition them in grid using NEW LAYOUT mapping
        # Periods/Weight on LEFT (1-2), Foods/Activities on RIGHT (3-4), Totals (5-6)
        window_map = {
            'periods_dashboard': 1,      # Top-left
            'weight_dashboard': 2,       # Bottom-left
            'food_dashboard': 3,         # Top-right
            'activity_dashboard': 4,     # Bottom-right
            'daily_food_totals': 5,      # Below on left
            'daily_activity_totals': 6,  # Below on right
            'all_food_logs': 7,          # Far below on left
            'all_activity_logs': 8       # Far below on right
        }
        
        for key, window in self.open_windows.items():
            if window and window.winfo_exists() and key in window_map:
                window.deiconify()
                pos_key = window_map[key]
                x, y = positions[pos_key]
                
                # Periods and Weight dashboards use larger sizes
                if key == 'periods_dashboard':
                    window.geometry(f"1050x750+{x}+{y}")
                elif key == 'weight_dashboard':
                    window.geometry(f"1050x750+{x}+{y}")
                else:
                    # Standard dashboards use card size
                    window.geometry(f"{win_width}x{win_height}+{x}+{y}")
                    
                window.lift()

    def _cascade_all_windows(self):
        """Arrange all open windows in cascade layout"""
        self.update_idletasks()
        
        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Calculate window size based on screen
        if screen_height < 1000:
            # Laptop screen - use smaller windows
            win_height = min(700, screen_height - 150)
        else:
            win_height = 850
        win_width = 520
        
        # Start position - near top-left with margin from main window
        main_x = self.winfo_x()
        main_y = self.winfo_y()
        start_x = main_x + 360
        start_y = 30  # Start from top
        offset = 35
        
        # Open all main dashboards if not open
        for i in range(1, 7):  # Include weight (5) and periods (6) dashboards
            self.button_pressed(i)
        
        # Also open the "All Logs" windows
        self._open_all_food_logs_window()
        self._open_all_activity_logs_window()
        
        # Cascade them
        current_x, current_y = start_x, start_y
        for window in self.open_windows.values():
            if window and window.winfo_exists():
                window.deiconify()
                window.geometry(f"{win_width}x{win_height}+{current_x}+{current_y}")
                current_x += offset
                current_y += offset

    def _toggle_hide_show_windows(self):
        """Toggle visibility of all dashboard windows"""
        if self.windows_hidden:
            for window in self.open_windows.values():
                if window and window.winfo_exists():
                    window.deiconify()
                    window.lift()
            self.windows_hidden = False
            self.hide_show_btn.config(text="👁 Hide All")
        else:
            for window in self.open_windows.values():
                if window and window.winfo_exists():
                    window.iconify()
            self.windows_hidden = True
            self.hide_show_btn.config(text="👁 Show All")

    def _build_admin_dashboard(self):
        """Build the admin dashboard with stub window and logout option"""
        # Clear any existing content
        for widget in self.winfo_children():
            widget.destroy()
        
        # Make window bigger for better visibility
        self.geometry("500x420+10+50")
        self.attributes('-topmost', True)
        
        # Header frame with transparent background
        header_frame = tk.Frame(self, bg="#ffebee", relief="flat")
        header_frame.pack(fill="x", pady=(10, 5))
        
        # Welcome label in header
        tk.Label(header_frame, text=f"👤 Admin: {self.current_admin_username}", 
                font=("Arial", 16, "bold"), fg="#c62828", bg="#ffebee").pack(pady=10)
        
        # Info section
        info_frame = tk.Frame(self, bg="#fff8e1", relief="solid", borderwidth=1)
        info_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(info_frame, text="⚠ Admin Panel - Demonstration Mode", 
                font=("Arial", 11, "bold"), fg="#f57c00", bg="#fff8e1").pack(pady=(10, 5))
        
        tk.Label(info_frame, 
                text="Admin features are placeholder stubs\nshowing planned functionality for future versions.", 
                font=("Arial", 10, "italic"), fg="#555", bg="#fff8e1", justify="center").pack(pady=(0, 10))
        
        # Admin stub button
        tk.Button(self, text="📋 View Admin Features Roadmap",
                 command=self._open_admin_stub, 
                 font=("Arial", 13, "bold"), bg="#ffcc80",
                 width=32, height=2).pack(pady=15)
        
        # Additional info
        tk.Label(self, 
                text="💡 Current version operates in self-service mode\nwhere users manage their own data independently.", 
                font=("Arial", 9, "italic"), fg="#666", justify="center").pack(pady=5)
        
        # Separator
        tk.Frame(self, height=2, bg="#ddd").pack(fill="x", padx=20, pady=15)
        
        # Logout button
        tk.Button(self, text="🚪 Logout / Back to Login", 
                 command=self._logout, 
                 font=("Arial", 14, "bold"), 
                 bg="#FF6B6B",
                 fg="white",
                 relief="raised",
                 borderwidth=3,
                 width=32,
                 height=2).pack(pady=10)
    
    def _open_admin_stub(self):
        """Open the admin stub window"""
        from ui.views.admin_stub_view import AdminStubWindow
        AdminStubWindow(self, self.current_admin_username)
    
    def _calculate_window_positions(self):
        """Calculate window positions for grid layout
        Returns dict with positions for each dashboard"""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Assume extended display is to the right if total width > 2000px
        is_extended_display = screen_width > 2000
        
        window_width = 520
        window_height = 850
        
        if is_extended_display:
            # Position on extended display (typically starts at primary screen width)
            # Assuming primary screen is 1920px or similar, use right portion
            primary_width = 1920  # Common laptop screen width
            if screen_width < 3000:
                primary_width = screen_width // 2  # If total < 3000, split evenly
            
            # Start on the extended display with some margin
            start_x = primary_width + 100
            start_y = 50
            
            # Check extended display height (assume same as primary)
            if (window_height * 2) > screen_height:
                window_height = min(850, (screen_height - 100) // 2)
        else:
            # Single screen - position windows so they fit
            if (window_height * 2) > screen_height:
                window_height = min(850, (screen_height - 100) // 2)
            
            # Center horizontally, but start from top with small margin
            start_x = max(0, (screen_width - (window_width * 2)) // 2)
            start_y = 30  # Small top margin
        
        # Calculate grid positions
        # NEW LAYOUT: Periods/Weight on LEFT (positions 1-2), Foods/Activities on RIGHT (positions 3-4), Totals (5-6)
        # Positions 7-8 for the "All Logs" windows further below
        # Grid is independent of menu position
        positions = {
            1: (start_x, start_y),  # Top-left: Periods Dashboard
            2: (start_x, start_y + window_height),  # Bottom-left: Weight Dashboard
            3: (start_x + window_width, start_y),  # Top-right: Food Dashboard
            4: (start_x + window_width, start_y + window_height),  # Bottom-right: Activity Dashboard
            5: (start_x, start_y + window_height * 2 + 50),  # Food Totals - below on left
            6: (start_x + window_width, start_y + window_height * 2 + 50),  # Activity Totals - below on right
            7: (start_x, start_y + window_height * 3 + 100),  # All Food Logs - far below on left
            8: (start_x + window_width, start_y + window_height * 3 + 100)  # All Activity Logs - far below on right
        }
        
        return positions

