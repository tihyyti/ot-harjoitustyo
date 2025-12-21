# Refactoroitu, alussa generoitu koodi alkaa 

# Week 4: added manually new features:
# - activities handling + UI
# - activitieslog handling + UI
# - testing and corrections

# Week 5: added manually new features:
# - All UI functions and mental model refactored
# - UI and Database tested together
# - Components implemented: Main button-menu
#   Food and Activity Dashboards and data logging
#   Food and Activity Loggings viewing windows with Edit/Delete functionality

# Week 6: added new edited features:
#
#

"""
laihdutanyt_v2.py 
Tkinter with:
 - Import Foods (CSV)
 - Import Activities (CSV)
 - Main Button-menu
 - Food Logging Dashboard
 - Activity Logging Dashboard
 - Daily Food Totals Dashboard
 - Daily Activity Totals Dashboard
 - View Foods and Activities All Logs windows with Edit/Delete functionality
"""

import os
import tkinter as tk
from tkinter import messagebox, filedialog, ttk, simpledialog
import importlib
import sqlite3
from datetime import date, datetime
import uuid
from typing import Optional

from repositories.user_repository import UserRepository
from repositories.food_repository import FoodRepository
from repositories.foodlog_repository import FoodLogRepository
from repositories.activity_repository import ActivityRepository
from repositories.activitylog_repository import ActivityLogRepository
from repositories.admin_repository import AdminRepository

from scripts.aggregate_daily_foods_totals import aggregate_daily_foods_totals
from scripts.aggregate_daily_activities_totals import aggregate_daily_activities_totals

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "data", "laihdutanyt.db")

class LoginFrame(tk.Frame):
    def __init__(self, master, user_repo: UserRepository, admin_repo: AdminRepository, on_login_success, on_admin_login_success):
        super().__init__(master)
        self.user_repo = user_repo
        self.admin_repo = admin_repo
        self.on_login_success = on_login_success
        self.on_admin_login_success = on_admin_login_success
        self._build()

    def _build(self):
        # Center the frame content
        self.pack(expand=True)
        
        tk.Label(self, text="Login", font=("Arial", 18)).grid(row=0, column=0, columnspan=2, pady=20)
        tk.Label(self, text="Username", font=("Arial", 12)).grid(row=1, column=0, sticky="e", padx=10, pady=8)
        tk.Label(self, text="Password", font=("Arial", 12)).grid(row=2, column=0, sticky="e", padx=10, pady=8)

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        tk.Entry(self, textvariable=self.username_var, font=("Arial", 12), width=20).grid(row=1, column=1, padx=10, pady=8, sticky="w")
        tk.Entry(self, textvariable=self.password_var, show="*", font=("Arial", 12), width=20).grid(row=2, column=1, padx=10, pady=8, sticky="w")

        button_frame = tk.Frame(self)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(button_frame, text="User Login", command=self._on_login, font=("Arial", 12), width=11, bg="#90caf9").pack(side="left", padx=5)
        tk.Button(button_frame, text="Admin Login", command=self._on_admin_login, font=("Arial", 12), width=11, bg="#ffcc80").pack(side="left", padx=5)
        
        tk.Button(self, text="Register New User", command=self._on_open_register, font=("Arial", 11), width=20).grid(row=4, column=0, columnspan=2, pady=10)

    def _on_login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get()
        if not username or not password:
            messagebox.showwarning("Missing info", "Please fill username and password.")
            return
        ok = self.user_repo.authenticate(username, password)
        if ok:
            messagebox.showinfo("Success", f"Logged in: {username}")
            self.on_login_success(username)
        else:
            messagebox.showerror("Error", "User login failed. Check credentials.")

    def _on_admin_login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get()
        if not username or not password:
            messagebox.showwarning("Missing info", "Please fill username and password.")
            return
        ok = self.admin_repo.verify_password(username, password)
        if ok:
            messagebox.showinfo("Success", f"Admin logged in: {username}")
            self.on_admin_login_success(username)
        else:
            messagebox.showerror("Error", "Admin login failed. Check credentials.")

    def _on_open_register(self):
        RegisterWindow(self.master, self.user_repo)

class RegisterWindow(tk.Toplevel):
    def __init__(self, master, user_repo: UserRepository):
        super().__init__(master)
        self.user_repo = user_repo
        self.title("Register")
        self._build()

    def _build(self):
        tk.Label(self, text="Create new user", font=("Arial", 15)).grid(row=0, column=0, columnspan=2, pady=12)
        tk.Label(self, text="Username").grid(row=1, column=0, sticky="e")
        tk.Label(self, text="Password").grid(row=2, column=0, sticky="e")
        tk.Label(self, text="Weight (kg)").grid(row=3, column=0, sticky="e")
        tk.Label(self, text="Length (cm)").grid(row=4, column=0, sticky="e")
        tk.Label(self, text="Age").grid(row=5, column=0, sticky="e")
        tk.Label(self, text="Activity Level").grid(row=6, column=0, sticky="e")
        tk.Label(self, text="Allergies").grid(row=7, column=0, sticky="e")
        tk.Label(self, text="Kcal Min").grid(row=8, column=0, sticky="e")
        tk.Label(self, text="Kcal Max").grid(row=9, column=0, sticky="e")
        tk.Label(self, text="Weight Loss Target").grid(row=10, column=0, sticky="e")

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.weight_var = tk.StringVar()
        self.length_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.activity_level_var = tk.StringVar()
        self.allergies_var = tk.StringVar()
        self.kcal_min_var = tk.StringVar()
        self.kcal_max_var = tk.StringVar()
        self.weight_loss_target_var = tk.StringVar()

        tk.Entry(self, textvariable=self.username_var).grid(row=1, column=1)
        tk.Entry(self, textvariable=self.password_var, show="*").grid(row=2, column=1)
        tk.Entry(self, textvariable=self.weight_var).grid(row=3, column=1)
        tk.Entry(self, textvariable=self.length_var).grid(row=4, column=1)
        tk.Entry(self, textvariable=self.age_var).grid(row=5, column=1)
        tk.Entry(self, textvariable=self.activity_level_var).grid(row=6, column=1)
        tk.Entry(self, textvariable=self.allergies_var).grid(row=7, column=1)
        tk.Entry(self, textvariable=self.kcal_min_var).grid(row=8, column=1)
        tk.Entry(self, textvariable=self.kcal_max_var).grid(row=9, column=1)
        tk.Entry(self, textvariable=self.weight_loss_target_var).grid(row=10, column=1)
        tk.Button(self, text="Create user", command=self._on_create).grid(row=11, column=0, columnspan=2, pady=12)

    def _on_create(self):
        username = self.username_var.get().strip()
        password = self.password_var.get()
        weight = self.weight_var.get()
        length = self.length_var.get()
        age = self.age_var.get()
        activity_level = self.activity_level_var.get()
        allergies = self.allergies_var.get()
        kcal_min = self.kcal_min_var.get()
        kcal_max = self.kcal_max_var.get()
        weight_loss_target = self.weight_loss_target_var.get()

        existing = self.user_repo.find_by_username(username)
        if existing:
            messagebox.showerror("Error", "Username already taken.")
            return

        try:
            if self.weight_var.get().strip():
                weight = float(self.weight_var.get().strip())
        except ValueError:
            messagebox.showwarning("Error", "Weight must be numeric.")
            return
        
        try:
            if self.length_var.get().strip():
                length = float(self.length_var.get().strip())
        except ValueError:
            messagebox.showwarning("Error", "Length must be numeric.")
            return
        
        try:
            if self.age_var.get().strip():
                age = float(self.age_var.get().strip())
        except ValueError:
            messagebox.showwarning("Error", "Age must be integer.")
            return
        
        try:
            if self.activity_level_var.get().strip():
                activity_level = float(self.activity_level_var.get().strip())
        except ValueError:
            messagebox.showwarning("Error", "Enter activity level 1 =young, 2 =middle-aged, 3 =senior, 4 =elderly.")
            return
        
        try:
            if self.allergies_var.get().strip():
                allergies = self.allergies_var.get().strip()            
        except ValueError:
            messagebox.showwarning("Error", "allergies must be string.")
            return
        
        try:
            if self.kcal_min_var.get().strip():
                kcal_min = float(self.kcal_min_var.get().strip())
        except ValueError:
            messagebox.showwarning("Error", "kcal_min must be integer.")
            return
        
        try:
            if self.kcal_max_var.get().strip():
                kcal_max = float(self.kcal_max_var.get().strip())
        except ValueError:
            messagebox.showwarning("Error", "kcal_max must be integer.")
            return
        
        try:
            if self.weight_loss_target_var.get().strip():
                weight_loss_target = float(self.weight_loss_target_var.get().strip())
        except ValueError:
            messagebox.showwarning("Error", "weight loss target must be numeric.")
            return
        
        user = self.user_repo.create_user(username, password, weight=weight, length=length, age=age, activity_level=activity_level, allergies=allergies, kcal_min=kcal_min, kcal_max=kcal_max, weight_loss_target=weight_loss_target)
        messagebox.showinfo("Done", f"User created: {user.username}")
        self.destroy()

class FoodLogFrame(tk.Frame):
    def __init__(self, master, db_path: str, user_id: str):
        super().__init__(master)
        self.db_path = db_path
        self.user_id = user_id
        self.food_repo = FoodRepository(db_path)
        self.foodlog_repo = FoodLogRepository(db_path)
        self._build()
        self.refresh_foods()
        self.refresh_logs()

    def _build(self):
        topframe = tk.Frame(self)
        topframe.pack(fill="x", padx=5, pady=12)

        tk.Label(topframe, text="Food", font=("Arial", 11)).grid(row=0, column=0, sticky="w", padx=5)
        tk.Label(topframe, text="Portion(g)", font=("Arial", 11)).grid(row=1, column=0, sticky="w", padx=5)
        tk.Label(topframe, text="YYYY-MM-DD", font=("Arial", 11)).grid(row=2, column=0, sticky="w", padx=5)

        self.food_var = tk.StringVar()
        self.portion_var = tk.StringVar(value="100") # 1 portion = 100 g
        self.date_var = tk.StringVar(value=date.today().isoformat())

        # Create custom font for combobox and entries
        self.food_cb = ttk.Combobox(topframe, textvariable=self.food_var, state="readonly", width=20, font=("Arial", 11))
        self.food_cb.grid(row=0, column=1, padx=5, pady=8, sticky="e")
        tk.Entry(topframe, textvariable=self.portion_var, width=12, font=("Arial", 11)).grid(row=1, column=1, padx=5, pady=8, sticky="e")
        tk.Entry(topframe, textvariable=self.date_var, width=15, font=("Arial", 11)).grid(row=2, column=1, padx=5, pady=8, sticky="e")

        tk.Button(topframe, text="Add to Food Log", command=self._on_add, font=("Arial", 11)).grid(row=3, column=0, columnspan=4, pady=12)

        # logs list with larger font
        self.logs_list = tk.Listbox(self, height=8, font=("Arial", 11))
        self.logs_list.pack(fill="both", expand=True, padx=5, pady=12)

    def refresh_foods(self):
        foods = self.food_repo.find_all()
        display = [f"{f['name']}|{f['food_id']}" for f in foods]
        self.food_cb["values"] = display
        if display:
            self.food_cb.current(0)

    def refresh_logs(self):
        self.logs_list.delete(0, tk.END)
        rows = self.foodlog_repo.find_by_user_and_date(self.user_id, self.date_var.get())
        for r in rows:
            name = r.get("name") or "?"
            portion = int(r.get("portion_size_g") or 100)
            cal_per = int(r.get("kcal_per_portion") or 0)
            total_cal = float((portion / 100.0) * cal_per)
            self.logs_list.insert(tk.END, f"{r['date']} - {name} {portion}g ({total_cal:.1f} kcal)")

    def _on_add(self):
        sel = self.food_var.get()
        if not sel:
            messagebox.showwarning("Select food", "Please select a food.")
            return
        # food string is name|food_id
        try:
            food_id = sel.split("|", 1)[1]
        except Exception:
            messagebox.showerror("Error", "Invalid food selection.")
            return
        try:
            portion = float(self.portion_var.get())
        except ValueError:
            messagebox.showwarning("Invalid portion", "Portion must be numeric.")
            return
        date_str = self.date_var.get().strip()
        self.foodlog_repo.create_log(self.user_id, food_id, date_str, portion)
        messagebox.showinfo("Saved", "Food log saved.")
        self.refresh_logs()

class AllFoodLogsWindow(tk.Toplevel):
    """Window to view, edit, and delete all logs for the logged-in user."""
    def __init__(self, master, db_path: str, user_id: str):
        super().__init__(master)
        self.db_path = db_path
        self.user_id = user_id
        self.food_repo = FoodRepository(db_path)
        self.foodlog_repo = FoodLogRepository(db_path)
        self.title("All Food Logs")
        # Geometry will be set by App class
        self._build()
        self.refresh_foods()  # Call refresh_foods instead of refresh

    def _build(self):
        topframe = tk.Frame(self)
        topframe.pack(fill="x", padx=5, pady=12)
        tk.Label(topframe, text="All Food Logs", font=("Arial", 15)).pack(side="left")
        self.search_var = tk.StringVar()
        tk.Entry(topframe, textvariable=self.search_var, width=30).pack(side="right")
        tk.Button(topframe, text="Refresh", command=self.refresh_foods, font=("Arial", 15)).pack(side="right", padx=5)

        # Configure ttk.Style for Treeview
        style = ttk.Style()
        style.configure("FoodLogs.Treeview", font=("Arial", 11), rowheight=25)
        style.configure("FoodLogs.Treeview.Heading", font=("Arial", 12, "bold"))

        # Treeview with columns: date, food name, portion, kcal
        columns = ("date", "food", "portion", "kcal", "log_id")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse", style="FoodLogs.Treeview")
        self.tree.heading("date", text="Date")
        self.tree.heading("food", text="Food")
        self.tree.heading("portion", text="Portion(g)")
        self.tree.heading("kcal", text="Kcal")
        
        # Set column widths
        self.tree.column("date", width=100, anchor="center")
        self.tree.column("food", width=200, anchor="center")
        self.tree.column("portion", width=100, anchor="center")
        self.tree.column("kcal", width=80, anchor="center")
        
        # log_id column hidden
        self.tree.column("log_id", width=0, stretch=False)
        self.tree.pack(fill="both", expand=True, padx=5, pady=12)

        btnframe = tk.Frame(self)
        btnframe.pack(fill="x", pady=12)
        tk.Button(btnframe, text="Edit selected", command=self._on_edit, font=("Arial", 15)).pack(side="left", padx=5)
        tk.Button(btnframe, text="Delete selected", command=self._on_delete, font=("Arial", 15)).pack(side="left", padx=5)
        tk.Button(btnframe, text="Close", command=self.destroy, font=("Arial", 15)).pack(side="right", padx=5)

    def refresh_foods(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        rows = self.foodlog_repo.find_all_for_user(self.user_id)
        for r in rows:
            cal_per = int(r.get("kcal_per_portion") or 0.0)
            portion = int(r.get("portion_size_g") or 0.0)
            total_cal = float((portion/100) * cal_per) # portion = 100 g
            self.tree.insert("", "end", values=(r.get("date"), r.get("name"), f"{portion:.1f}", f"{total_cal:.1f}", r.get("log_id")))

    def _selected_log(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select row", "Please select a log row first.")
            return None
        vals = self.tree.item(sel[0], "values")
        # values: (date, food, portion, kcal, log_id)
        return {
            "date": vals[0],
            "food": vals[1],
            "portion": vals[2],
            "kcal": vals[3],
            "log_id": vals[4]
        }

    def _on_edit(self):
        sel = self._selected_log()
        if not sel:
            return
        # Prompt for new portion and date
        new_portion = simpledialog.askstring("Edit portion", f"Portion (100g) for {sel['food']} on {sel['date']}:", initialvalue=sel["portion"], parent=self)
        if new_portion is None:
            return
        try:
            new_portion_val = float(new_portion)
        except ValueError:
            messagebox.showwarning("Invalid", "Portion must be numeric.")
            return
        new_date = simpledialog.askstring("Edit date", "YYYY-MM-DD:", initialvalue=sel["date"], parent=self)
        if new_date is None:
            return
        # Update in DB
        try:
            with self.foodlog_repo._conn() as conn:
                cur = conn.cursor()
                cur.execute("UPDATE foodlog SET portion_size_g = ?, date = ? WHERE log_id = ?", (new_portion_val, new_date, sel["log_id"]))
                conn.commit()
            messagebox.showinfo("Updated", "Log updated.")
            self.refresh_foods()
        except Exception as e:
            messagebox.showerror("Error", f"Could not update log: {e}")

    def _on_delete(self):
        sel = self._selected_log()
        if not sel:
            return
        if not messagebox.askyesno("Confirm", f"Delete log for {sel['food']} on {sel['date']}?"):
            return
        try:
            with self.foodlog_repo._conn() as conn:
                cur = conn.cursor()
                cur.execute("DELETE FROM foodlog WHERE log_id = ?", (sel["log_id"],))
                conn.commit()
            messagebox.showinfo("Deleted", "Log deleted.")
            self.refresh_foods()
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete log: {e}")   
class Dashboard_food(tk.Toplevel):
    def __init__(self, master, user_repo: UserRepository, username: str, db_path: str, user_id: str):
        super().__init__(master)
        self.title(f"Food Dashboard - {username}")
        # Geometry will be set by App class
        self.db_path = db_path
        self.user_repo = user_repo
        self.username = username
        self.user_id = user_id
        self.master = master
        
        # Fetch the actual user object to get user data
        user = user_repo.find_by_username(username)
        if user:
            self.weight = user.weight
            self.length = user.length
            self.age = user.age
            self.activity_level = user.activity_level
            self.allergies = user.allergies
            self.kcal_min = user.kcal_min
            self.kcal_max = user.kcal_max
            self.weight_loss_target = user.weight_loss_target
        
        # User info header
        info_frame = tk.Frame(self, bg="#e8f4f8", relief="ridge", borderwidth=2)
        info_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(info_frame, text=f"{username}", font=("Arial", 16, "bold"), bg="#e8f4f8").pack(pady=5)
        
        info_text = f"Weight: {self.weight}kg | Target: {self.weight_loss_target}kg | Daily Goal: {self.kcal_min}-{self.kcal_max} kcal"
        tk.Label(info_frame, text=info_text, font=("Arial", 11), bg="#e8f4f8").pack(pady=5)
        
        tk.Label(info_frame, text=f"{date.today().strftime('%Y-%m-%d')}", font=("Arial", 11), bg="#e8f4f8").pack(pady=5)
        
        # Navigation buttons frame
        nav_frame = tk.Frame(self)
        nav_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Button(nav_frame, text="← Back to Main Menu", command=self._back_to_menu, 
                 font=("Arial", 12), bg="#d0d0d0").pack(side="left", padx=5)
        tk.Button(nav_frame, text="View All Food Logs", command=self._open_all_logs_window, 
                 font=("Arial", 12), bg="#90caf9").pack(side="right", padx=5)
        
        # Food logging UI
        fl = FoodLogFrame(self, db_path, user_id)
        fl.pack(expand=True, fill="both", padx=10, pady=10)
    
    def _back_to_menu(self):
        self.destroy()
    
    def _open_all_logs_window(self):
        # Check if window already exists
        if hasattr(self.master, 'open_windows'):
            if self.master.open_windows['all_food_logs'] is None or not self.master.open_windows['all_food_logs'].winfo_exists():
                positions = self.master._calculate_window_positions()
                win = AllFoodLogsWindow(self, self.db_path, self.user_id)
                x, y = positions['all_food_logs']
                win.geometry(f"435x700+{x}+{y}")
                self.master.open_windows['all_food_logs'] = win
            else:
                self.master.open_windows['all_food_logs'].lift()
        else:
            AllFoodLogsWindow(self, self.db_path, self.user_id)
        
    def aggregate_foods_totals(self):
        aggregate_daily_foods_totals(self, self.db_path, self.user_id)

    def aggregate_activities_totals(self):
        AllFoodLogsWindow(self, self.db_path, self.user_id)    
class Dashboard_daily_foods_totals(tk.Toplevel):
    def __init__(self, master, user_repo: UserRepository, username: str, db_path: str, user_id: str):
        super().__init__(master)
        self.title(f"Daily Food Totals - {username}")
        # Geometry will be set by App class
        self.db_path = db_path
        self.user_repo = user_repo
        self.username = username
        self.user_id = user_id
        self.master = master
        
        # Fetch the actual user object to get user data
        user = user_repo.find_by_username(username)
        if user:
            self.weight = user.weight
            self.length = user.length
            self.age = user.age
            self.activity_level = user.activity_level
            self.allergies = user.allergies
            self.kcal_min = user.kcal_min
            self.kcal_max = user.kcal_max
            self.weight_loss_target = user.weight_loss_target

        # User info header
        info_frame = tk.Frame(self, bg="#e8f4f8", relief="ridge", borderwidth=2)
        info_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(info_frame, text=f"Daily Food Totals - {username}", font=("Arial", 16, "bold"), bg="#e8f4f8").pack(pady=5)
        
        info_text = f"Weight: {self.weight}kg | Target: {self.weight_loss_target}kg | Daily Goal: {self.kcal_min}-{self.kcal_max} kcal"
        tk.Label(info_frame, text=info_text, font=("Arial", 11), bg="#e8f4f8").pack(pady=5)
        
        # Navigation buttons frame
        nav_frame = tk.Frame(self)
        nav_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Button(nav_frame, text="← Back to Main Menu", command=self._back_to_menu, 
                 font=("Arial", 12), bg="#d0d0d0").pack(side="left", padx=5)
        tk.Button(nav_frame, text="Refresh", command=self.refresh_totals, 
                 font=("Arial", 12), bg="#90caf9").pack(side="right", padx=5)
        
        # Configure treeview style for larger fonts
        style = ttk.Style()
        style.configure("Custom.Treeview", font=("Arial", 11), rowheight=25)
        style.configure("Custom.Treeview.Heading", font=("Arial", 12, "bold"))
        
        # Create treeview for daily totals
        columns = ("date", "total_kcal", "entries")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse", style="Custom.Treeview")
        self.tree.heading("date", text="Date")
        self.tree.heading("total_kcal", text="Total Calories (kcal)")
        self.tree.heading("entries", text="# of Entries")
        
        # Set column widths
        self.tree.column("date", width=120, anchor="center")
        self.tree.column("total_kcal", width=180, anchor="center")
        self.tree.column("entries", width=120, anchor="center")
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Load the data
        self.refresh_totals()
    
    def _back_to_menu(self):
        self.destroy()
    
    def refresh_totals(self):
        # Clear existing rows
        for r in self.tree.get_children():
            self.tree.delete(r)
        
        # Get today's date for highlighting
        today = date.today().isoformat()
        
        # Configure tags for date-based styling
        self.tree.tag_configure('past', background='white')
        self.tree.tag_configure('today', background='#ffffcc', font=("Arial", 11, "bold"))  # Yellow highlight
        self.tree.tag_configure('future', background='#e8f5e9')  # Light green for planned meals
        
        # Get aggregated data from database
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT fl.date AS date,
                       SUM( (fl.portion_size_g / 100.0) * COALESCE(f.kcal_per_portion, 0.0) ) AS total_calories,
                       COUNT(*) AS entries
                FROM foodlog fl
                LEFT JOIN food f ON fl.food_id = f.food_id
                WHERE fl.user_id = ?
                GROUP BY fl.date
                ORDER BY fl.date DESC
            """, (self.user_id,))
            rows = cur.fetchall()
            for date_str, total_cal, entries in rows:
                # Determine tag based on date
                if date_str < today:
                    tag = 'past'
                    status = ""
                elif date_str == today:
                    tag = 'today'
                    status = " 📍 TODAY"
                else:
                    tag = 'future'
                    status = " 🔮 PLANNED"
                
                self.tree.insert("", "end", values=(date_str + status, f"{total_cal:.1f}", entries), tags=(tag,))
        finally:
            conn.close()
        
    def _open_all_logs_window(self):
        AllFoodLogsWindow(self, self.db_path, self.user_id)
        
    def aggregate_foods_totals(self):
        aggregate_daily_foods_totals(self, self.db_path, self.user_id)

    def aggregate_activities_totals(self):
        AllFoodLogsWindow(self, self.db_path, self.user_id)  

class Dashboard_daily_activities_totals(tk.Toplevel):
    def __init__(self, master, user_repo: UserRepository, username: str, db_path: str, user_id: str):
        super().__init__(master)
        self.title(f"Daily Activity Totals - {username}")
        # Geometry will be set by App class
        self.db_path = db_path
        self.user_repo = user_repo
        self.username = username
        self.user_id = user_id
        self.master = master
        
        # Fetch the actual user object to get user data
        user = user_repo.find_by_username(username)
        if user:
            self.weight = user.weight
            self.length = user.length
            self.age = user.age
            self.activity_level = user.activity_level
            self.allergies = user.allergies
            self.kcal_min = user.kcal_min
            self.kcal_max = user.kcal_max
            self.weight_loss_target = user.weight_loss_target

        # User info header
        info_frame = tk.Frame(self, bg="#e8f8e8", relief="ridge", borderwidth=2)
        info_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(info_frame, text=f"Daily Activity Totals - {username}", font=("Arial", 16, "bold"), bg="#e8f8e8").pack(pady=5)
        
        info_text = f"Weight: {self.weight}kg | Activity Level: {self.activity_level} | Target: {self.weight_loss_target}kg"
        tk.Label(info_frame, text=info_text, font=("Arial", 11), bg="#e8f8e8").pack(pady=5)
        
        # Navigation buttons frame
        nav_frame = tk.Frame(self)
        nav_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Button(nav_frame, text="← Back to Main Menu", command=self._back_to_menu, 
                 font=("Arial", 12), bg="#d0d0d0").pack(side="left", padx=5)
        tk.Button(nav_frame, text="Refresh", command=self.refresh_totals, 
                 font=("Arial", 12), bg="#a5d6a7").pack(side="right", padx=5)
        
        # Configure treeview style for larger fonts
        style = ttk.Style()
        style.configure("Activity.Treeview", font=("Arial", 11), rowheight=25)
        style.configure("Activity.Treeview.Heading", font=("Arial", 12, "bold"))
        
        # Create treeview for daily totals
        columns = ("date", "total_kcal_burned", "entries")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse", style="Activity.Treeview")
        self.tree.heading("date", text="Date")
        self.tree.heading("total_kcal_burned", text="Calories Burned (kcal)")
        self.tree.heading("entries", text="Activities")
        
        # Set column widths
        self.tree.column("date", width=120, anchor="center")
        self.tree.column("total_kcal_burned", width=200, anchor="center")
        self.tree.column("entries", width=120, anchor="center")
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Load the data
        self.refresh_totals()
    
    def _back_to_menu(self):
        self.destroy()
    
    def refresh_totals(self):
        # Clear existing rows
        for r in self.tree.get_children():
            self.tree.delete(r)
        
        # Get today's date for highlighting
        today = date.today().isoformat()
        
        # Configure tags for date-based styling
        self.tree.tag_configure('past', background='white')
        self.tree.tag_configure('today', background='#ffffcc', font=("Arial", 11, "bold"))  # Yellow highlight
        self.tree.tag_configure('future', background='#e8f5e9')  # Light green for planned activities
        
        # Get aggregated data from database
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT al.date AS date,
                       SUM( (al.activity_count / 1000.0) * COALESCE(al.kcal_burned, 0.0) ) AS total_calories,
                       COUNT(*) AS entries
                FROM activitylog al
                LEFT JOIN activity a ON al.activity_id = a.activity_id
                WHERE al.user_id = ?
                GROUP BY al.date
                ORDER BY al.date DESC
            """, (self.user_id,))
            rows = cur.fetchall()
            for date_str, total_cal, entries in rows:
                # Determine tag based on date
                if date_str < today:
                    tag = 'past'
                    status = ""
                elif date_str == today:
                    tag = 'today'
                    status = " 📍 TODAY"
                else:
                    tag = 'future'
                    status = " 🔮 PLANNED"
                
                self.tree.insert("", "end", values=(date_str + status, f"{total_cal:.1f}", entries), tags=(tag,))
        finally:
            conn.close()
    
    def _open_all_logs_window(self):
        AllActivityLogsWindow(self, self.db_path, self.user_id)
        
    def aggregate_activities_totals(self):
        aggregate_daily_activities_totals(self, self.db_path, self.user_id)

# Activity ---------------------- Activity
class ActivityLogFrame(tk.Frame):
    def __init__(self, master, db_path: str, user_id: str):
        super().__init__(master)
        self.db_path = db_path
        self.user_id = user_id
        self.activity_repo = ActivityRepository(db_path)
        self.activitylog_repo = ActivityLogRepository(db_path)
        self._build()
        self.refresh_activities()
        self.refresh_logs()

    def _build(self):
        topframe = tk.Frame(self)
        topframe.pack(fill="x", padx=5, pady=12)

        tk.Label(topframe, text="Activity", font=("Arial", 11)).grid(row=0, column=0, sticky="w", padx=5)
        tk.Label(topframe, text="Act. Count", font=("Arial", 11)).grid(row=1, column=0, sticky="w", padx=5)
        tk.Label(topframe, text="YYYY-MM-DD", font=("Arial", 11)).grid(row=2, column=0, sticky="w", padx=5)

        self.activity_var = tk.StringVar()
        self.activity_count_var = tk.StringVar(value="100")
        self.date_var = tk.StringVar(value=date.today().isoformat())

        self.activity_cb = ttk.Combobox(topframe, textvariable=self.activity_var, state="readonly", width=20, font=("Arial", 11))
        self.activity_cb.grid(row=0, column=1, padx=5, pady=8, sticky="e")
        tk.Entry(topframe, textvariable=self.activity_count_var, width=12, font=("Arial", 11)).grid(row=1, column=1, padx=5, pady=8, sticky="e")
        tk.Entry(topframe, textvariable=self.date_var, width=15, font=("Arial", 11)).grid(row=2, column=1, padx=5, pady=8, sticky="e")

        tk.Button(topframe, text="Add to activity Log", command=self._on_add, font=("Arial", 11)).grid(row=3, column=0, columnspan=4, pady=12)

        # logs list with larger font
        self.logs_list = tk.Listbox(self, height=8, font=("Arial", 11))
        self.logs_list.pack(fill="both", expand=True, padx=5, pady=12)

    def refresh_activities(self):
        activities = self.activity_repo.find_all()
        display = [f"{a['name']}|{a['activity_id']}" for a in activities]
        self.activity_cb["values"] = display
        if display:
            self.activity_cb.current(0)

    def refresh_logs(self):
        self.logs_list.delete(0, tk.END)
        rows = self.activitylog_repo.find_by_user_and_date(self.user_id, self.date_var.get())
        for r in rows:
            name = r.get("name") or "?"
            act_count = int(r.get("activity_count") or 0)
            cal_per = int(r.get("kcal_burned") or 0)
            total_cal = float(act_count * cal_per/1000) # cal_per in kcal
            self.logs_list.insert(tk.END, f"{r['date']} - {name} {act_count} ({total_cal:.1f} kcal)")

    def _on_add(self):
        sel = self.activity_var.get()
        if not sel:
            messagebox.showwarning("Select activity", "Please select a activity.")
            return
        # activity string is name|activity_id
        try:
            activity_id = sel.split("|", 1)[1]
        except Exception:
            messagebox.showerror("Error", "Invalid activity selection.")
            return
        try:
            activity_count = float(self.activity_count_var.get())
        except ValueError:
            messagebox.showwarning("Invalid activity_count", "Activity_count must be integer.")
            return
        
        date_str = self.date_var.get().strip()
        activ_count = float(self.activity_count_var.get())
        kcal_burned = (activ_count/1000) * self.activity_repo.find_by_id(activity_id).get("kcal_per_unit", 0)

        self.activitylog_repo.create_log(self.user_id, activity_id, date_str, activ_count, kcal_burned)
        messagebox.showinfo("Saved", "Activity log saved.")
        self.refresh_logs()
        
class AllActivityLogsWindow(tk.Toplevel):
    """Window to view, edit, and delete all logs for the logged-in user."""
    def __init__(self, master, db_path: str, user_id: str):
        super().__init__(master)
        self.db_path = db_path
        self.user_id = user_id
        self.activity_repo = ActivityRepository(db_path)
        self.activitylog_repo = ActivityLogRepository(db_path)
        self.title("All Activity Logs")
        # Geometry will be set by App class
        self._build()
        self.refresh_activities()

    def _build(self):
        # Create the top frame first
        topframe = tk.Frame(self)
        topframe.pack(fill="x", padx=5, pady=12)
        
        tk.Label(topframe, text="All Activity Logs", font=("Arial", 15)).pack(side="left")
        self.search_var = tk.StringVar()
        tk.Entry(topframe, textvariable=self.search_var, width=30).pack(side="right")
        tk.Button(topframe, text="Refresh", command=self.refresh_activities, font=("Arial", 15)).pack(side="right", padx=5)
        
        # Configure ttk.Style for Treeview
        style = ttk.Style()
        style.configure("ActivityLogs.Treeview", font=("Arial", 11), rowheight=25)
        style.configure("ActivityLogs.Treeview.Heading", font=("Arial", 12, "bold"))
        
        # Create treeview with columns
        columns = ("date", "activity_id", "activity_count", "kcal_burned", "log_id")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse", style="ActivityLogs.Treeview")
        
        # Set headings
        self.tree.heading("date", text="Date")
        self.tree.heading("activity_id", text="Activity")
        self.tree.heading("activity_count", text="Activity Count")
        self.tree.heading("kcal_burned", text="Kcal burned")

        # Set column widths and alignment
        self.tree.column("date", width=100, anchor='center')
        self.tree.column("activity_id", width=200, anchor='center')
        self.tree.column("activity_count", width=120, anchor='center')
        self.tree.column("kcal_burned", width=100, anchor='center')

        # log_id column hidden
        self.tree.column("log_id", width=0, stretch=False)
        self.tree.pack(fill="both", expand=True, padx=5, pady=12)

        # Button frame
        btnframe = tk.Frame(self)
        btnframe.pack(fill="x", pady=12)

        tk.Button(btnframe, text="Edit selected", command=self._on_edit, font=("Arial", 15)).pack(side="left", padx=5)
        tk.Button(btnframe, text="Delete selected", command=self._on_delete, font=("Arial", 15)).pack(side="left", padx=5)
        tk.Button(btnframe, text="Close", command=self.destroy, font=("Arial", 15)).pack(side="right", padx=5)

    def refresh_activities(self):  
        # Clear existing rows
        for r in self.tree.get_children():
            self.tree.delete(r)
        
        # Fetch and populate new data
        rows = self.activitylog_repo.find_all_for_user(self.user_id)
        for r in rows:
            cal_per = float(r.get("kcal_burned") or 0.0)
            activi_count = int(r.get("activity_count") or 0.0)
            total_cal = float(activi_count * cal_per)
            self.tree.insert("", "end", values=(r.get("date"), r.get("name"), f"{activi_count}", f"{total_cal:.1f}", r.get("log_id")))

    def _selected_log(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select row", "Please select a log row first.")
            return None
        vals = self.tree.item(sel[0], "values")
        # values: (date, activity, activity_count, kcal_burned, log_id)
        return {
            "date": vals[0],
            "activity": vals[1],
            "activi_count": vals[2],
            "total_cal": vals[3],
            "log_id": vals[4]
        }

    def _on_edit(self):
        sel = self._selected_log()
        if not sel:
            return
        # Prompt for new activity_count and date
        new_activity_count = simpledialog.askstring("Edit activity count", f"Activity Count for {sel['activity']} on {sel['date']}:", initialvalue=sel["activi_count"], parent=self)
        if new_activity_count is None:
            return
        try:
            new_activity_count_val = int(new_activity_count)
        except ValueError:
            messagebox.showwarning("Invalid", "Activity Count must be integer.")
            return
        new_date = simpledialog.askstring("Edit date", "YYYY-MM-DD:", initialvalue=sel["date"], parent=self)
        if new_date is None:
            return
        # Update in DB
        try:
            with self.activitylog_repo._conn() as conn:
                cur = conn.cursor()
                cur.execute("UPDATE activitylog SET activity_count = ?, date = ? WHERE log_id = ?", (new_activity_count_val, new_date, sel["log_id"]))
                conn.commit()
            messagebox.showinfo("Updated", "Log updated.")
            self.refresh_activities()
        except Exception as e:
            messagebox.showerror("Error", f"Could not update log: {e}")

    def _on_delete(self):
        sel = self._selected_log()
        if not sel:
            return
        if not messagebox.askyesno("Confirm", f"Delete log for {sel['activity']} on {sel['date']}?"):
            return
        try:
            with self.activitylog_repo._conn() as conn:
                cur = conn.cursor()
                cur.execute("DELETE FROM activitylog WHERE log_id = ?", (sel["log_id"],))
                conn.commit()
            messagebox.showinfo("Deleted", "Log deleted.")
            self.refresh_activities()
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete log: {e}")
            
class Dashboard_activity(tk.Toplevel):
    def __init__(self, master, user_repo: UserRepository, username: str, db_path: str, user_id: str):
        super().__init__(master)
        self.title(f"Activity Dashboard - {username}")
        # Geometry will be set by App class
        self.db_path = db_path
        self.user_repo = user_repo
        self.username = username
        self.user_id = user_id
        self.master = master
        
        # Fetch the actual user object to get user data
        user = user_repo.find_by_username(username)
        if user:
            self.weight = user.weight
            self.length = user.length
            self.age = user.age
            self.activity_level = user.activity_level
            self.allergies = user.allergies
            self.kcal_min = user.kcal_min
            self.kcal_max = user.kcal_max
            self.weight_loss_target = user.weight_loss_target

        # User info header
        info_frame = tk.Frame(self, bg="#e8f8e8", relief="ridge", borderwidth=2)
        info_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(info_frame, text=f"{username}", font=("Arial", 16, "bold"), bg="#e8f8e8").pack(pady=5)
        
        info_text = f"Weight: {self.weight}kg | Activity Level: {self.activity_level} | Target: {self.weight_loss_target}kg"
        tk.Label(info_frame, text=info_text, font=("Arial", 11), bg="#e8f8e8").pack(pady=5)
        
        tk.Label(info_frame, text=f"📅 {date.today().strftime('%Y-%m-%d')}", font=("Arial", 11), bg="#e8f8e8").pack(pady=5)
        
        # Navigation buttons frame
        nav_frame = tk.Frame(self)
        nav_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Button(nav_frame, text="← Back to Main Menu", command=self._back_to_menu, 
                 font=("Arial", 12), bg="#d0d0d0").pack(side="left", padx=5)
        tk.Button(nav_frame, text="View All Activity Logs", command=self._open_all_logs_window, 
                 font=("Arial", 12), bg="#a5d6a7").pack(side="right", padx=5)

        # Activity logging UI
        al = ActivityLogFrame(self, db_path, user_id)
        al.pack(expand=True, fill="both", padx=10, pady=10)
    
    def _back_to_menu(self):
        self.destroy()
    
    def _open_all_logs_window(self):
        # Check if window already exists
        if hasattr(self.master, 'open_windows'):
            if self.master.open_windows['all_activity_logs'] is None or not self.master.open_windows['all_activity_logs'].winfo_exists():
                positions = self.master._calculate_window_positions()
                win = AllActivityLogsWindow(self, self.db_path, self.user_id)
                x, y = positions['all_activity_logs']
                win.geometry(f"435x700+{x}+{y}")
                self.master.open_windows['all_activity_logs'] = win
            else:
                self.master.open_windows['all_activity_logs'].lift()
        else:
            AllActivityLogsWindow(self, self.db_path, self.user_id)

class App(tk.Tk):
    def __init__(self, db_path):
        super().__init__()
        self.title("Laihdutanyt_v2")
        self.geometry("350x700")
        self.db_path = db_path
        self.user_repo = UserRepository(db_path)
        self.admin_repo = AdminRepository(db_path)
        self.user_id = None
        self.food_repo = FoodRepository(db_path)
        self.foodlog_repo = FoodLogRepository(db_path)
        self.activity_repo = ActivityRepository(db_path)
        self.activitylog_repo = ActivityLogRepository(db_path)
        
        # Track open dashboard windows
        self.open_windows = {
            'food_dashboard': None,
            'activity_dashboard': None,
            'daily_food_totals': None,
            'daily_activity_totals': None,
            'all_food_logs': None,
            'all_activity_logs': None
        }
        
        # Track window visibility state for hide/show toggle
        self.windows_hidden = False
        
        self._build_login()
        self._build_menu()

    def _build_menu(self):
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Import Foods (CSV)", command=self._on_import_foods)
        filemenu.add_command(label="Import Activities (CSV)", command=self._on_import_activities)
        #filemenu.add_command(label="Package Project", command=self._on_package_project)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.destroy)
        menubar.add_cascade(label="File", menu=filemenu)
        self.config(menu=menubar)

    def _on_import_foods(self):
        filename = filedialog.askopenfilename(title="Select foods CSV", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if not filename:
            return
        try:
            mod = importlib.import_module("scripts.import_foods.py")
            mod.import_csv(filename, self.db_path)
            messagebox.showinfo("Import complete", f"Imported foods from {os.path.basename(filename)}")
        except Exception as e:
            messagebox.showerror("Import error", f"Import failed: {e}")
            
    def _on_import_activities(self):
        filename = filedialog.askopenfilename(title="Select activities CSV", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if not filename:
            return
        try:
            mod = importlib.import_module("scripts.import_activities.py")
            mod.import_csv(filename, self.db_path)
            messagebox.showinfo("Import complete", f"Imported activities from {os.path.basename(filename)}")
        except Exception as e:
            messagebox.showerror("Import error", f"Import failed: {e}")

    def _build_login(self):
        self.login_frame = LoginFrame(self, self.user_repo, self.admin_repo, self._on_login_success, self._on_admin_login_success)
        self.login_frame.pack(expand=True, fill="both")

    def _on_login_success(self, username):
        # fetch user object to get user_id
        user = self.user_repo.find_by_username(username)
        if not user:
            messagebox.showerror("Error", "User record not found after login.")
            return
        # Store user information for dashboard use
        self.current_username = username
        self.current_user_id = user.user_id
        self.login_frame.pack_forget()
        self._build_dashboard()
    
    def _on_admin_login_success(self, admin_username):
        # Admin logged in - show admin dashboard
        self.current_admin_username = admin_username
        self.login_frame.pack_forget()
        self._build_admin_dashboard()
        
    def _build_dashboard(self):
        self.switch = 0  # Initialize switch variable
        
        # Make main menu window always on top and resizable
        self.attributes('-topmost', True)
        self.resizable(True, True)
        
        # Add title label with bigger font
        tk.Label(self, text=f"Welcome, {self.current_username}!", font=("Arial", 15)).pack(pady=15)
        
        # Button to view food logs with bigger font
        tk.Button(self, text="View Food Logs",
                  command=lambda: self.button_pressed(1), font=("Arial", 15)).pack(pady=14)
        # Button to view activity logs with bigger font  
        tk.Button(self, text="View Activity Logs",
                  command=lambda: self.button_pressed(2), font=("Arial", 15)).pack(pady=14)
        # Button to view food logs with bigger font
        tk.Button(self, text="View Daily Foods Totals",
                  command=lambda: self.button_pressed(3), font=("Arial", 15)).pack(pady=14)
        # Button to view activity logs with bigger font  
        tk.Button(self, text="View Daily Activities Totals",
                  command=lambda: self.button_pressed(4), font=("Arial", 15)).pack(pady=14)
        
        # Window management buttons frame
        mgmt_frame = tk.Frame(self)
        mgmt_frame.pack(pady=5)
        
        # Special "Organize Windows" button with distinctive styling
        tk.Button(mgmt_frame, text="📐 Grid Layout", 
                  command=self._organize_all_windows, 
                  font=("Arial", 13, "bold"), 
                  bg="#FFD700",  # Gold color for visibility
                  fg="#000000",  # Black text
                  relief="raised",
                  borderwidth=2,
                  width=14).pack(side="left", padx=3)
        
        # Cascade layout button for small screens
        tk.Button(mgmt_frame, text="📚 Cascade", 
                  command=self._cascade_all_windows, 
                  font=("Arial", 13, "bold"), 
                  bg="#87CEEB",  # Sky blue
                  fg="#000000",
                  relief="raised",
                  borderwidth=2,
                  width=12).pack(side="left", padx=3)
        
        # Hide/Show toggle button
        self.hide_show_btn = tk.Button(mgmt_frame, text="👁 Hide All", 
                  command=self._toggle_hide_show_windows, 
                  font=("Arial", 13, "bold"), 
                  bg="#FFA500",  # Orange
                  fg="#000000",
                  relief="raised",
                  borderwidth=2,
                  width=12)
        self.hide_show_btn.pack(side="left", padx=3)

    def _calculate_window_positions(self):
        """Calculate window positions for grid layout, preferring larger secondary display"""
        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Try to detect if there's a secondary monitor and position windows there
        # Get the main window's current position
        self.update_idletasks()  # Ensure geometry is up to date
        main_x = self.winfo_x()
        main_y = self.winfo_y()
        
        # Detect if main window is on secondary display (typically positioned beyond primary screen width)
        # If main window is beyond x=1920 (common laptop width), likely on secondary display
        on_secondary = main_x > 1920 or main_x < -100
        
        # Window dimensions
        dashboard_width = 435
        dashboard_height = 750
        
        # Calculate positions for grid layout
        # If on secondary display, use main window's screen position as reference
        # Otherwise, try to position on the rightmost screen (secondary monitor)
        if on_secondary:
            # Use current screen, position relative to main window
            gap = 10
            start_x = main_x + 350 + gap  # Start after main menu
            start_y = main_y
        else:
            # Try to position on secondary display (typically starts at primary width)
            # Common laptop widths: 1366, 1920
            # Assume secondary display starts after primary
            gap = 10
            # Try to detect secondary monitor by checking if screen width suggests dual monitors
            if screen_width > 3000:  # Dual monitor setup detected
                # Position on the right half (secondary monitor)
                start_x = 1920 + 20  # Start on secondary monitor (assuming 1920px laptop)
                start_y = 20
            else:
                # Single monitor or can't detect, position after main menu
                start_x = 370
                start_y = 20
        
        positions = {
            'food_dashboard': (start_x, start_y),
            'daily_food_totals': (start_x + dashboard_width + gap, start_y),
            'activity_dashboard': (start_x + 2 * (dashboard_width + gap), start_y),
            'daily_activity_totals': (start_x + 3 * (dashboard_width + gap), start_y),
            'all_food_logs': (start_x, start_y + dashboard_height + gap),
            'all_activity_logs': (start_x + 2 * (dashboard_width + gap), start_y + dashboard_height + gap)
        }
        
        return positions

    def _organize_all_windows(self):
        """Open all dashboard windows at once and arrange them in grid layout"""
        positions = self._calculate_window_positions()
        
        # Open or reposition Food Dashboard
        if self.open_windows['food_dashboard'] is None or not self.open_windows['food_dashboard'].winfo_exists():
            win = Dashboard_food(self, self.user_repo, self.current_username, self.db_path, self.current_user_id)
            x, y = positions['food_dashboard']
            win.geometry(f"435x700+{x}+{y}")
            self.open_windows['food_dashboard'] = win
        else:
            # Deiconify if minimized, then reposition
            self.open_windows['food_dashboard'].deiconify()
            x, y = positions['food_dashboard']
            self.open_windows['food_dashboard'].geometry(f"435x700+{x}+{y}")
            self.open_windows['food_dashboard'].lift()
        
        # Open or reposition Daily Food Totals
        if self.open_windows['daily_food_totals'] is None or not self.open_windows['daily_food_totals'].winfo_exists():
            win = Dashboard_daily_foods_totals(self, self.user_repo, self.current_username, self.db_path, self.current_user_id)
            x, y = positions['daily_food_totals']
            win.geometry(f"435x700+{x}+{y}")
            self.open_windows['daily_food_totals'] = win
        else:
            # Deiconify if minimized, then reposition
            self.open_windows['daily_food_totals'].deiconify()
            x, y = positions['daily_food_totals']
            self.open_windows['daily_food_totals'].geometry(f"435x700+{x}+{y}")
            self.open_windows['daily_food_totals'].lift()
        
        # Open or reposition Activity Dashboard
        if self.open_windows['activity_dashboard'] is None or not self.open_windows['activity_dashboard'].winfo_exists():
            win = Dashboard_activity(self, self.user_repo, self.current_username, self.db_path, self.current_user_id)
            x, y = positions['activity_dashboard']
            win.geometry(f"435x700+{x}+{y}")
            self.open_windows['activity_dashboard'] = win
        else:
            # Deiconify if minimized, then reposition
            self.open_windows['activity_dashboard'].deiconify()
            x, y = positions['activity_dashboard']
            self.open_windows['activity_dashboard'].geometry(f"435x700+{x}+{y}")
            self.open_windows['activity_dashboard'].lift()
        
        # Open or reposition Daily Activity Totals
        if self.open_windows['daily_activity_totals'] is None or not self.open_windows['daily_activity_totals'].winfo_exists():
            win = Dashboard_daily_activities_totals(self, self.user_repo, self.current_username, self.db_path, self.current_user_id)
            x, y = positions['daily_activity_totals']
            win.geometry(f"435x700+{x}+{y}")
            self.open_windows['daily_activity_totals'] = win
        else:
            # Deiconify if minimized, then reposition
            self.open_windows['daily_activity_totals'].deiconify()
            x, y = positions['daily_activity_totals']
            self.open_windows['daily_activity_totals'].geometry(f"435x700+{x}+{y}")
            self.open_windows['daily_activity_totals'].lift()
        
        # Open or reposition All Food Logs
        if self.open_windows['all_food_logs'] is None or not self.open_windows['all_food_logs'].winfo_exists():
            # Get reference to food dashboard to pass as master
            if self.open_windows['food_dashboard'] and self.open_windows['food_dashboard'].winfo_exists():
                win = AllFoodLogsWindow(self.open_windows['food_dashboard'], self.db_path, self.current_user_id)
                x, y = positions['all_food_logs']
                win.geometry(f"435x700+{x}+{y}")
                self.open_windows['all_food_logs'] = win
        else:
            # Deiconify if minimized, then reposition
            self.open_windows['all_food_logs'].deiconify()
            x, y = positions['all_food_logs']
            self.open_windows['all_food_logs'].geometry(f"435x700+{x}+{y}")
            self.open_windows['all_food_logs'].lift()
        
        # Open or reposition All Activity Logs
        if self.open_windows['all_activity_logs'] is None or not self.open_windows['all_activity_logs'].winfo_exists():
            # Get reference to activity dashboard to pass as master
            if self.open_windows['activity_dashboard'] and self.open_windows['activity_dashboard'].winfo_exists():
                win = AllActivityLogsWindow(self.open_windows['activity_dashboard'], self.db_path, self.current_user_id)
                x, y = positions['all_activity_logs']
                win.geometry(f"435x700+{x}+{y}")
                self.open_windows['all_activity_logs'] = win
        else:
            # Deiconify if minimized, then reposition
            self.open_windows['all_activity_logs'].deiconify()
            x, y = positions['all_activity_logs']
            self.open_windows['all_activity_logs'].geometry(f"435x700+{x}+{y}")
            self.open_windows['all_activity_logs'].lift()
        
        # No messagebox - user sees what's happening!

    def _cascade_all_windows(self):
        """Arrange windows in cascade layout with visible titles - perfect for small screens"""
        # Get main window position as starting point
        self.update_idletasks()
        main_x = self.winfo_x()
        main_y = self.winfo_y()
        
        # Start position - next to main menu
        start_x = main_x + 360
        start_y = main_y
        
        # Cascade offset - enough to show title bar (30px) and a bit of content
        cascade_offset_x = 30
        cascade_offset_y = 35  # Slightly larger to show title clearly
        
        # Window order for cascading (most important on top)
        window_order = [
            'food_dashboard',
            'daily_food_totals', 
            'activity_dashboard',
            'daily_activity_totals',
            'all_food_logs',
            'all_activity_logs'
        ]
        
        current_x = start_x
        current_y = start_y
        
        for i, window_key in enumerate(window_order):
            window = self.open_windows[window_key]
            
            if window is None or not window.winfo_exists():
                # Create window if it doesn't exist
                if window_key == 'food_dashboard':
                    window = Dashboard_food(self, self.user_repo, self.current_username, self.db_path, self.current_user_id)
                    self.open_windows[window_key] = window
                elif window_key == 'daily_food_totals':
                    window = Dashboard_daily_foods_totals(self, self.user_repo, self.current_username, self.db_path, self.current_user_id)
                    self.open_windows[window_key] = window
                elif window_key == 'activity_dashboard':
                    window = Dashboard_activity(self, self.user_repo, self.current_username, self.db_path, self.current_user_id)
                    self.open_windows[window_key] = window
                elif window_key == 'daily_activity_totals':
                    window = Dashboard_daily_activities_totals(self, self.user_repo, self.current_username, self.db_path, self.current_user_id)
                    self.open_windows[window_key] = window
                elif window_key == 'all_food_logs':
                    if self.open_windows['food_dashboard'] and self.open_windows['food_dashboard'].winfo_exists():
                        window = AllFoodLogsWindow(self.open_windows['food_dashboard'], self.db_path, self.current_user_id)
                        self.open_windows[window_key] = window
                elif window_key == 'all_activity_logs':
                    if self.open_windows['activity_dashboard'] and self.open_windows['activity_dashboard'].winfo_exists():
                        window = AllActivityLogsWindow(self.open_windows['activity_dashboard'], self.db_path, self.current_user_id)
                        self.open_windows[window_key] = window
            
            if window and window.winfo_exists():
                # Deiconify if minimized
                window.deiconify()
                # Position in cascade
                window.geometry(f"435x700+{current_x}+{current_y}")
                # Don't lift - keep in cascade order
                # Increment position for next window
                current_x += cascade_offset_x
                current_y += cascade_offset_y
        
        # Update hidden state
        self.windows_hidden = False
        self.hide_show_btn.config(text="👁 Hide All")

    def _toggle_hide_show_windows(self):
        """Toggle between hiding all windows and showing them"""
        if self.windows_hidden:
            # Show all windows
            for window_key, window in self.open_windows.items():
                if window and window.winfo_exists():
                    window.deiconify()
                    window.lift()
            self.windows_hidden = False
            self.hide_show_btn.config(text="👁 Hide All")
        else:
            # Hide all windows (iconify/minimize them)
            for window_key, window in self.open_windows.items():
                if window and window.winfo_exists():
                    window.iconify()
            self.windows_hidden = True
            self.hide_show_btn.config(text="👁 Show All")

    def button_pressed(self, button_id):
        self.switch = button_id  # Update the switch variable
        print(f"Button {self.switch} pressed")
        
        positions = self._calculate_window_positions()
        
        # Call the corresponding window methods with position
        if self.switch == 1:
            if self.open_windows['food_dashboard'] is None or not self.open_windows['food_dashboard'].winfo_exists():
                win = Dashboard_food(self, self.user_repo, self.current_username, self.db_path, self.current_user_id)
                x, y = positions['food_dashboard']
                win.geometry(f"435x700+{x}+{y}")
                self.open_windows['food_dashboard'] = win
            else:
                self.open_windows['food_dashboard'].lift()
                
        elif self.switch == 2:
            if self.open_windows['activity_dashboard'] is None or not self.open_windows['activity_dashboard'].winfo_exists():
                win = Dashboard_activity(self, self.user_repo, self.current_username, self.db_path, self.current_user_id)
                x, y = positions['activity_dashboard']
                win.geometry(f"435x700+{x}+{y}")
                self.open_windows['activity_dashboard'] = win
            else:
                self.open_windows['activity_dashboard'].lift()
                
        elif self.switch == 3:
            if self.open_windows['daily_food_totals'] is None or not self.open_windows['daily_food_totals'].winfo_exists():
                win = Dashboard_daily_foods_totals(self, self.user_repo, self.current_username, self.db_path, self.current_user_id)
                x, y = positions['daily_food_totals']
                win.geometry(f"435x700+{x}+{y}")
                self.open_windows['daily_food_totals'] = win
            else:
                self.open_windows['daily_food_totals'].lift()
                
        elif self.switch == 4:
            if self.open_windows['daily_activity_totals'] is None or not self.open_windows['daily_activity_totals'].winfo_exists():
                win = Dashboard_daily_activities_totals(self, self.user_repo, self.current_username, self.db_path, self.current_user_id)
                x, y = positions['daily_activity_totals']
                win.geometry(f"435x700+{x}+{y}")
                self.open_windows['daily_activity_totals'] = win
            else:
                self.open_windows['daily_activity_totals'].lift()
    
    def _build_admin_dashboard(self):
        """Build admin interface for managing users and recommendations"""
        self.geometry("1050x700")
        self.title(f"Admin Panel - {self.current_admin_username}")
        
        # Admin header
        header = tk.Frame(self, bg="#ff9800", relief="ridge", borderwidth=3)
        header.pack(fill="x", padx=10, pady=10)
        tk.Label(header, text=f"🔐 ADMIN PANEL - {self.current_admin_username}", 
                font=("Arial", 18, "bold"), bg="#ff9800", fg="white").pack(pady=10)
        
        # Tab control for different admin functions
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tab 1: User Management
        user_mgmt_frame = tk.Frame(notebook)
        notebook.add(user_mgmt_frame, text="👤 User Management")
        self._build_user_management_tab(user_mgmt_frame)
        
        # Tab 2: Recommendations
        recommendations_frame = tk.Frame(notebook)
        notebook.add(recommendations_frame, text="💡 Recommendations")
        self._build_recommendations_tab(recommendations_frame)
        
        # Tab 3: Constraints & Health
        constraints_frame = tk.Frame(notebook)
        notebook.add(constraints_frame, text="🏥 Constraints & Health")
        self._build_constraints_tab(constraints_frame)
        
        # Tab 4: AI Trainer (Future Hook)
        ai_frame = tk.Frame(notebook)
        notebook.add(ai_frame, text="🤖 AI Trainer (Coming Soon)")
        self._build_ai_trainer_tab(ai_frame)
        
        # Logout button at bottom
        tk.Button(self, text="Logout", command=self._admin_logout, 
                 font=("Arial", 12), bg="#f44336", fg="white", width=15).pack(pady=10)
    
    def _build_user_management_tab(self, parent):
        """Build user management interface"""
        tk.Label(parent, text="Registered Users", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Treeview for users
        style = ttk.Style()
        style.configure("Users.Treeview", font=("Arial", 11), rowheight=25)
        style.configure("Users.Treeview.Heading", font=("Arial", 12, "bold"))
        
        columns = ("username", "weight", "target", "kcal_min", "kcal_max", "activity_level", "allergies")
        self.users_tree = ttk.Treeview(parent, columns=columns, show="headings", style="Users.Treeview")
        
        self.users_tree.heading("username", text="Username")
        self.users_tree.heading("weight", text="Weight(kg)")
        self.users_tree.heading("target", text="Target(kg)")
        self.users_tree.heading("kcal_min", text="Kcal Min")
        self.users_tree.heading("kcal_max", text="Kcal Max")
        self.users_tree.heading("activity_level", text="Activity")
        self.users_tree.heading("allergies", text="Allergies")
        
        self.users_tree.column("username", width=120)
        self.users_tree.column("weight", width=80, anchor="center")
        self.users_tree.column("target", width=80, anchor="center")
        self.users_tree.column("kcal_min", width=80, anchor="center")
        self.users_tree.column("kcal_max", width=80, anchor="center")
        self.users_tree.column("activity_level", width=80, anchor="center")
        self.users_tree.column("allergies", width=200)
        
        self.users_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Buttons
        btn_frame = tk.Frame(parent)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="🔄 Refresh", command=self._refresh_users, 
                 font=("Arial", 11), width=12).pack(side="left", padx=5)
        tk.Button(btn_frame, text="📊 View User Progress", command=self._view_user_progress, 
                 font=("Arial", 11), width=18).pack(side="left", padx=5)
        
        # Load users
        self._refresh_users()
    
    def _build_recommendations_tab(self, parent):
        """Build recommendations interface"""
        tk.Label(parent, text="Create Personalized Recommendation", 
                font=("Arial", 16, "bold")).pack(pady=10)
        
        # User selection
        user_frame = tk.Frame(parent)
        user_frame.pack(fill="x", padx=20, pady=10)
        tk.Label(user_frame, text="Select User:", font=("Arial", 12)).pack(side="left", padx=5)
        
        self.selected_user_var = tk.StringVar()
        self.user_dropdown = ttk.Combobox(user_frame, textvariable=self.selected_user_var, 
                                          state="readonly", width=25, font=("Arial", 11))
        self.user_dropdown.pack(side="left", padx=5)
        
        # Recommendation details
        details_frame = tk.LabelFrame(parent, text="Recommendation Details", font=("Arial", 12, "bold"))
        details_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        tk.Label(details_frame, text="Type:", font=("Arial", 11)).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.rec_type_var = tk.StringVar(value="diet_plan")
        types = ["diet_plan", "exercise_plan", "combined", "weight_loss_strategy", "maintenance"]
        ttk.Combobox(details_frame, textvariable=self.rec_type_var, values=types, 
                    state="readonly", width=25, font=("Arial", 11)).grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        tk.Label(details_frame, text="Title:", font=("Arial", 11)).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.rec_title_var = tk.StringVar()
        tk.Entry(details_frame, textvariable=self.rec_title_var, width=40, font=("Arial", 11)).grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="w")
        
        tk.Label(details_frame, text="Target Kcal Min:", font=("Arial", 11)).grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.rec_kcal_min_var = tk.StringVar()
        tk.Entry(details_frame, textvariable=self.rec_kcal_min_var, width=15, font=("Arial", 11)).grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        tk.Label(details_frame, text="Target Kcal Max:", font=("Arial", 11)).grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.rec_kcal_max_var = tk.StringVar()
        tk.Entry(details_frame, textvariable=self.rec_kcal_max_var, width=15, font=("Arial", 11)).grid(row=3, column=1, padx=5, pady=5, sticky="w")
        
        tk.Label(details_frame, text="Suggested Activities:", font=("Arial", 11)).grid(row=4, column=0, sticky="ne", padx=5, pady=5)
        self.rec_activities_text = tk.Text(details_frame, height=4, width=40, font=("Arial", 11))
        self.rec_activities_text.grid(row=4, column=1, columnspan=2, padx=5, pady=5, sticky="w")
        
        tk.Label(details_frame, text="Notes:", font=("Arial", 11)).grid(row=5, column=0, sticky="ne", padx=5, pady=5)
        self.rec_notes_text = tk.Text(details_frame, height=6, width=40, font=("Arial", 11))
        self.rec_notes_text.grid(row=5, column=1, columnspan=2, padx=5, pady=5, sticky="w")
        
        # Save button
        tk.Button(parent, text="💾 Save Recommendation", command=self._save_recommendation, 
                 font=("Arial", 12, "bold"), bg="#4caf50", fg="white", width=20).pack(pady=10)
        
        # Load users for dropdown
        self._refresh_recommendation_users()
    
    def _build_constraints_tab(self, parent):
        """Build constraints management interface"""
        tk.Label(parent, text="User Constraints & Health Information", 
                font=("Arial", 16, "bold")).pack(pady=10)
        
        # User selection
        user_frame = tk.Frame(parent)
        user_frame.pack(fill="x", padx=20, pady=10)
        tk.Label(user_frame, text="Select User:", font=("Arial", 12)).pack(side="left", padx=5)
        
        self.constraint_user_var = tk.StringVar()
        self.constraint_user_dropdown = ttk.Combobox(user_frame, textvariable=self.constraint_user_var, 
                                                     state="readonly", width=25, font=("Arial", 11))
        self.constraint_user_dropdown.pack(side="left", padx=5)
        tk.Button(user_frame, text="Load Constraints", command=self._load_user_constraints,
                 font=("Arial", 11)).pack(side="left", padx=10)
        
        # Constraints list
        list_frame = tk.LabelFrame(parent, text="Current Constraints", font=("Arial", 12, "bold"))
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        style = ttk.Style()
        style.configure("Constraints.Treeview", font=("Arial", 11), rowheight=25)
        
        columns = ("type", "description", "severity")
        self.constraints_tree = ttk.Treeview(list_frame, columns=columns, show="headings", style="Constraints.Treeview")
        
        self.constraints_tree.heading("type", text="Type")
        self.constraints_tree.heading("description", text="Description")
        self.constraints_tree.heading("severity", text="Severity")
        
        self.constraints_tree.column("type", width=150)
        self.constraints_tree.column("description", width=400)
        self.constraints_tree.column("severity", width=100, anchor="center")
        
        self.constraints_tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Add new constraint
        add_frame = tk.LabelFrame(parent, text="Add New Constraint", font=("Arial", 11, "bold"))
        add_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(add_frame, text="Type:", font=("Arial", 11)).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.constraint_type_var = tk.StringVar(value="allergy")
        types = ["allergy", "disability", "medical_condition", "dietary_restriction", "injury"]
        ttk.Combobox(add_frame, textvariable=self.constraint_type_var, values=types, 
                    state="readonly", width=20, font=("Arial", 11)).grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        tk.Label(add_frame, text="Description:", font=("Arial", 11)).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.constraint_desc_var = tk.StringVar()
        tk.Entry(add_frame, textvariable=self.constraint_desc_var, width=50, font=("Arial", 11)).grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        tk.Label(add_frame, text="Severity:", font=("Arial", 11)).grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.constraint_severity_var = tk.StringVar(value="moderate")
        severities = ["low", "moderate", "high", "critical"]
        ttk.Combobox(add_frame, textvariable=self.constraint_severity_var, values=severities, 
                    state="readonly", width=15, font=("Arial", 11)).grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        tk.Button(add_frame, text="➕ Add Constraint", command=self._add_constraint, 
                 font=("Arial", 11), bg="#2196f3", fg="white").grid(row=3, column=1, padx=5, pady=10, sticky="w")
        
        # Load users for dropdown
        self._refresh_constraint_users()
    
    def _build_ai_trainer_tab(self, parent):
        """Placeholder for future AI trainer integration"""
        info_frame = tk.Frame(parent, bg="#e3f2fd", relief="ridge", borderwidth=2)
        info_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        tk.Label(info_frame, text="🤖 AI Personal Trainer", 
                font=("Arial", 20, "bold"), bg="#e3f2fd").pack(pady=20)
        
        tk.Label(info_frame, text="Future AI-Powered Features:", 
                font=("Arial", 14, "bold"), bg="#e3f2fd").pack(pady=10)
        
        features = [
            "🔹 Automated meal plan generation based on user preferences",
            "🔹 Smart exercise recommendations using machine learning",
            "🔹 Predictive weight loss trajectory analysis",
            "🔹 Natural language recommendations",
            "🔹 Constraint-aware planning (allergies, disabilities)",
            "🔹 Progress tracking and adaptive goal adjustment",
            "🔹 Integration with external fitness APIs",
            "🔹 Personalized coaching based on historical data"
        ]
        
        for feature in features:
            tk.Label(info_frame, text=feature, font=("Arial", 12), bg="#e3f2fd", 
                    anchor="w").pack(anchor="w", padx=40, pady=5)
        
        tk.Label(info_frame, text="\n💡 This module will integrate with OpenAI, TensorFlow,\nor other AI frameworks for intelligent recommendations", 
                font=("Arial", 11, "italic"), bg="#e3f2fd", fg="#666").pack(pady=20)
        
        # Placeholder for API configuration
        api_frame = tk.LabelFrame(info_frame, text="API Configuration (Placeholder)", 
                                  font=("Arial", 11, "bold"), bg="#e3f2fd")
        api_frame.pack(padx=40, pady=10, fill="x")
        
        tk.Label(api_frame, text="OpenAI API Key:", bg="#e3f2fd").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(api_frame, width=40, state="disabled").grid(row=0, column=1, padx=5, pady=5)
        
        tk.Button(api_frame, text="Connect AI Service", state="disabled", 
                 font=("Arial", 11)).grid(row=1, column=1, padx=5, pady=10, sticky="w")
    
    # Admin helper methods
    def _refresh_users(self):
        """Refresh user list in admin panel"""
        for row in self.users_tree.get_children():
            self.users_tree.delete(row)
        
        conn = sqlite3.connect(self.db_path)
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT username, weight, weight_loss_target, kcal_min, kcal_max, activity_level, allergies
                FROM user
                ORDER BY username
            """)
            for row in cur.fetchall():
                self.users_tree.insert("", "end", values=row)
        finally:
            conn.close()
    
    def _view_user_progress(self):
        """View detailed progress for selected user"""
        selection = self.users_tree.selection()
        if not selection:
            messagebox.showwarning("Select User", "Please select a user first.")
            return
        
        username = self.users_tree.item(selection[0])['values'][0]
        messagebox.showinfo("User Progress", f"Detailed progress view for {username}\n\n(Feature to be implemented:\n- Weight tracking chart\n- Calorie consumption trends\n- Activity completion rate)")
    
    def _refresh_recommendation_users(self):
        """Refresh user list for recommendations dropdown"""
        conn = sqlite3.connect(self.db_path)
        try:
            cur = conn.cursor()
            cur.execute("SELECT username FROM user ORDER BY username")
            usernames = [row[0] for row in cur.fetchall()]
            self.user_dropdown['values'] = usernames
            if usernames:
                self.user_dropdown.current(0)
        finally:
            conn.close()
    
    def _save_recommendation(self):
        """Save recommendation to database"""
        username = self.selected_user_var.get()
        if not username:
            messagebox.showwarning("Select User", "Please select a user.")
            return
        
        # Get user_id
        user = self.user_repo.find_by_username(username)
        if not user:
            messagebox.showerror("Error", "User not found.")
            return
        
        # Get admin_id
        admin = self.admin_repo.find_by_username(self.current_admin_username)
        
        rec_id = str(uuid.uuid4())
        rec_type = self.rec_type_var.get()
        title = self.rec_title_var.get().strip()
        kcal_min = self.rec_kcal_min_var.get().strip()
        kcal_max = self.rec_kcal_max_var.get().strip()
        activities = self.rec_activities_text.get("1.0", tk.END).strip()
        notes = self.rec_notes_text.get("1.0", tk.END).strip()
        
        if not title:
            messagebox.showwarning("Missing Title", "Please provide a recommendation title.")
            return
        
        try:
            kcal_min_val = float(kcal_min) if kcal_min else None
            kcal_max_val = float(kcal_max) if kcal_max else None
        except ValueError:
            messagebox.showerror("Invalid Input", "Calorie values must be numeric.")
            return
        
        conn = sqlite3.connect(self.db_path)
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO recommendation 
                (recommendation_id, user_id, admin_id, recommendation_type, title, description, 
                 target_kcal_min, target_kcal_max, suggested_activities, notes, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'active')
            """, (rec_id, user.user_id, admin.admin_id if admin else None, rec_type, title, "", 
                  kcal_min_val, kcal_max_val, activities, notes))
            conn.commit()
            messagebox.showinfo("Success", f"Recommendation '{title}' saved for user {username}!")
            
            # Clear form
            self.rec_title_var.set("")
            self.rec_kcal_min_var.set("")
            self.rec_kcal_max_var.set("")
            self.rec_activities_text.delete("1.0", tk.END)
            self.rec_notes_text.delete("1.0", tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save recommendation: {e}")
        finally:
            conn.close()
    
    def _refresh_constraint_users(self):
        """Refresh user list for constraints dropdown"""
        conn = sqlite3.connect(self.db_path)
        try:
            cur = conn.cursor()
            cur.execute("SELECT username FROM user ORDER BY username")
            usernames = [row[0] for row in cur.fetchall()]
            self.constraint_user_dropdown['values'] = usernames
            if usernames:
                self.constraint_user_dropdown.current(0)
        finally:
            conn.close()
    
    def _load_user_constraints(self):
        """Load constraints for selected user"""
        username = self.constraint_user_var.get()
        if not username:
            messagebox.showwarning("Select User", "Please select a user first.")
            return
        
        user = self.user_repo.find_by_username(username)
        if not user:
            return
        
        # Clear existing items
        for row in self.constraints_tree.get_children():
            self.constraints_tree.delete(row)
        
        conn = sqlite3.connect(self.db_path)
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT constraint_type, description, severity
                FROM user_constraint
                WHERE user_id = ?
                ORDER BY severity DESC, constraint_type
            """, (user.user_id,))
            for row in cur.fetchall():
                self.constraints_tree.insert("", "end", values=row)
        finally:
            conn.close()
    
    def _add_constraint(self):
        """Add new constraint for selected user"""
        username = self.constraint_user_var.get()
        if not username:
            messagebox.showwarning("Select User", "Please select a user first.")
            return
        
        user = self.user_repo.find_by_username(username)
        if not user:
            return
        
        constraint_type = self.constraint_type_var.get()
        description = self.constraint_desc_var.get().strip()
        severity = self.constraint_severity_var.get()
        
        if not description:
            messagebox.showwarning("Missing Description", "Please provide a description.")
            return
        
        constraint_id = str(uuid.uuid4())
        
        conn = sqlite3.connect(self.db_path)
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO user_constraint 
                (constraint_id, user_id, constraint_type, description, severity)
                VALUES (?, ?, ?, ?, ?)
            """, (constraint_id, user.user_id, constraint_type, description, severity))
            conn.commit()
            messagebox.showinfo("Success", f"Constraint added for {username}")
            
            # Clear form and reload
            self.constraint_desc_var.set("")
            self._load_user_constraints()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add constraint: {e}")
        finally:
            conn.close()
    
    def _admin_logout(self):
        """Logout admin and return to login screen"""
        # Clear admin data
        self.current_admin_username = None
        
        # Destroy all widgets
        for widget in self.winfo_children():
            widget.destroy()
        
        # Reset geometry and rebuild login
        self.geometry("350x700")
        self._build_login()

def main():
    if not os.path.exists(DB_PATH):
        messagebox.showerror("Missing database", f"Database not found: {DB_PATH}\nRun create_db.py first.")
        return
    app = App(DB_PATH)
    app.mainloop()

if __name__ == "__main__":
    main()
	
# Refactoroitu, alussa generoitu koodi päättyy