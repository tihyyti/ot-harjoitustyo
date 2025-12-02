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
"""
laihdutanyt_v1.py 
Tkinter with:
 - Import Foods (CSV)
 - Import Activities (CSV)
 - Main Button-menu
 - Food Logging Dashboard
 - Activity Logging Dashboard
 - View Foods and Activities All Logs windows with Edit/Delete functionality
"""

import os
import tkinter as tk
from tkinter import messagebox, filedialog, ttk, simpledialog
import importlib
from datetime import date
from typing import Optional

from repositories.user_repository import UserRepository
from repositories.food_repository import FoodRepository
from repositories.foodlog_repository import FoodLogRepository
from repositories.activity_repository import ActivityRepository
from repositories.activitylog_repository import ActivityLogRepository

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "data", "laihdutanyt.db")

class LoginFrame(tk.Frame):
    def __init__(self, master, user_repo: UserRepository, on_login_success):
        super().__init__(master)
        self.user_repo = user_repo
        self.on_login_success = on_login_success
        self._build()

    def _build(self):
        tk.Label(self, text="Login", font=("Arial", 18)).grid(row=0, column=0, columnspan=2, pady=8)
        tk.Label(self, text="Username").grid(row=1, column=0, sticky="e")
        tk.Label(self, text="Password").grid(row=2, column=0, sticky="e")

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        tk.Entry(self, textvariable=self.username_var).grid(row=1, column=1)
        tk.Entry(self, textvariable=self.password_var, show="*").grid(row=2, column=1)

        tk.Button(self, text="Login", command=self._on_login).grid(row=3, column=0, pady=10)
        tk.Button(self, text="Register", command=self._on_open_register).grid(row=3, column=1)

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
            messagebox.showerror("Error", "Login failed. Check credentials.")

    def _on_open_register(self):
        RegisterWindow(self.master, self.user_repo)

class RegisterWindow(tk.Toplevel):
    def __init__(self, master, user_repo: UserRepository):
        super().__init__(master)
        self.user_repo = user_repo
        self.title("Register")
        self._build()

    def _build(self):
        tk.Label(self, text="Create new user", font=("Arial", 18)).grid(row=0, column=0, columnspan=2, pady=8)
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
        tk.Button(self, text="Create user", command=self._on_create).grid(row=11, column=0, columnspan=2, pady=8)

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
        
        user = self.user_repo.create_user(username, password, weight=weight)
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
        topframe.pack(fill="x", padx=5, pady=8)

        tk.Label(topframe, text="Food").grid(row=0, column=0, sticky="w")
        tk.Label(topframe, text="Portion(g)").grid(row=1, column=0, sticky="w")
        tk.Label(topframe, text="YYYY-MM-DD").grid(row=2, column=0, sticky="w")

        self.food_var = tk.StringVar()
        self.portion_var = tk.StringVar(value="100") # 1 portion = 100 g
        self.date_var = tk.StringVar(value=date.today().isoformat())

        self.food_cb = ttk.Combobox(topframe, textvariable=self.food_var, state="readonly", width=20)
        self.food_cb.grid(row=0, column=1, padx=5, pady=8, sticky="e")
        tk.Entry(topframe, textvariable=self.portion_var, width=10).grid(row=1, column=1, padx=5, pady=8, sticky="e")
        tk.Entry(topframe, textvariable=self.date_var, width=15).grid(row=2, column=1, padx=5, pady=8, sticky="e")

        tk.Button(topframe, text="Add to Log", command=self._on_add).grid(row=3, column=0, columnspan=4, pady=8)

        # logs list
        self.logs_list = tk.Listbox(self, height=8)
        self.logs_list.pack(fill="both", expand=True, padx=5, pady=8)

    def refresh_foods(self):
        foods = self.food_repo.find_all()
        display = [f"{f['name']}|{f['food_id']}" for f in foods]
        #display = [f"{f['name']}" for f in foods]
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
        self.geometry("700x900")
        self._build()
        self.refresh_foods()  # Call refresh_foods instead of refresh

    def _build(self):
        topframe = tk.Frame(self)
        topframe.pack(fill="x", padx=5, pady=8)
        tk.Label(topframe, text="All logs for user", font=("Arial", 18)).pack(side="left")
        self.search_var = tk.StringVar()
        tk.Entry(topframe, textvariable=self.search_var, width=30).pack(side="right")
        tk.Button(topframe, text="Refresh", command=self.refresh_foods, font=("Arial", 14)).pack(side="right", padx=5)

        # Treeview with columns: date, food name, portion, kcal
        columns = ("date", "food", "portion", "kcal", "log_id")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("date", text="Date")
        self.tree.heading("food", text="Food")
        self.tree.heading("portion", text="Portion (g)")
        self.tree.heading("kcal", text="Kcal")
        # log_id column hidden
        self.tree.column("log_id", width=0, stretch=False)
        self.tree.pack(fill="both", expand=True, padx=5, pady=8)

        btnframe = tk.Frame(self)
        btnframe.pack(fill="x", pady=8)
        tk.Button(btnframe, text="Edit selected", command=self._on_edit, font=("Arial", 14)).pack(side="left", padx=5)
        tk.Button(btnframe, text="Delete selected", command=self._on_delete, font=("Arial", 14)).pack(side="left", padx=5)
        tk.Button(btnframe, text="Close", command=self.destroy, font=("Arial", 14)).pack(side="right", padx=5)

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
    def __init__(self, master, username: str, db_path: str, user_id: str):
        super().__init__(master)
        self.title(f"Welcome to Food Dashboard - {username}")
        self.geometry("700x900")
        self.username = username
        self.user_id = user_id
        self.db_path = db_path
        
        # Add header and button to view all logs with bigger fonts
        header_frame = tk.Frame(self)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(header_frame, text=f"Food Dashboard - {username}", font=("Arial", 18)).pack(side="left")
        tk.Button(header_frame, text="View All Food Logs", 
                 command=self._open_all_logs_window, 
                 font=("Arial", 16)).pack(side="right")
        
        # Food logging UI
        fl = FoodLogFrame(self, db_path, user_id)
        fl.pack(expand=True, fill="both")
    
    def _open_all_logs_window(self):
        AllFoodLogsWindow(self, self.db_path, self.user_id)

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
        topframe.pack(fill="x", padx=5, pady=8)

        tk.Label(topframe, text="Activity").grid(row=0, column=0, sticky="w")
        tk.Label(topframe, text="Act. Count").grid(row=1, column=0, sticky="w")
        tk.Label(topframe, text="YYYY-MM-DD").grid(row=2, column=0, sticky="w")

        self.activity_var = tk.StringVar()
        self.activity_count_var = tk.StringVar(value="100")
        self.date_var = tk.StringVar(value=date.today().isoformat())

        self.activity_cb = ttk.Combobox(topframe, textvariable=self.activity_var, state="readonly", width=20)
        self.activity_cb.grid(row=0, column=1, padx=5, pady=8, sticky="e")
        tk.Entry(topframe, textvariable=self.activity_count_var, width=10).grid(row=1, column=1, padx=5, pady=8, sticky="e")
        tk.Entry(topframe, textvariable=self.date_var, width=15).grid(row=2, column=1, padx=5, pady=8, sticky="e")

        tk.Button(topframe, text="Add to activity Log", command=self._on_add).grid(row=3, column=0, columnspan=4, pady=8)

        # logs list
        self.logs_list = tk.Listbox(self, height=8)
        self.logs_list.pack(fill="both", expand=True, padx=5, pady=8)

    def refresh_activities(self):
        activities = self.activity_repo.find_all()
        display = [f"{a['name']}|{a['activity_id']}" for a in activities]
        #display = [f"{a['name']}" for a in activities]
        self.activity_cb["values"] = display
        if display:
            self.activity_cb.current(0)

    def refresh_logs(self):
        self.logs_list.delete(0, tk.END)
        rows = self.activitylog_repo.find_by_user_and_date(self.user_id, self.date_var.get())
        for r in rows:
            name = r.get("name") or "?"
            act_count = int(r.get("activity_count") or 0)
            cal_per = int(r.get("kcal_per_unit") or 0)
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
        self.geometry("700x900")
        self._build()
        self.refresh_activities()

    def _build(self):
        # Create the top frame first
        topframe = tk.Frame(self)
        topframe.pack(fill="x", padx=5, pady=8)
        
        tk.Label(topframe, text="All Activity Logs", font=("Arial", 18)).pack(side="left")
        self.search_var = tk.StringVar()
        tk.Entry(topframe, textvariable=self.search_var, width=30).pack(side="right")
        tk.Button(topframe, text="Refresh", command=self.refresh_activities, font=("Arial", 14)).pack(side="right", padx=5)
        
        # Create treeview with columns
        columns = ("date", "activity_id", "activity_count", "kcal_burned", "log_id")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse")
        
        # Set headings
        self.tree.heading("date", text="Date")
        self.tree.heading("activity_id", text="Activity")
        self.tree.heading("activity_count", text="Activity Count")
        self.tree.heading("kcal_burned", text="Kcal burned")

        # Set column properties, including text alignment
        for col in columns:
            if col != "log_id":
                self.tree.column(col, anchor='w')

        # log_id column hidden
        self.tree.column("log_id", width=0, stretch=False)
        self.tree.pack(fill="both", expand=True, padx=5, pady=8)

        # Button frame
        btnframe = tk.Frame(self)
        btnframe.pack(fill="x", pady=8)

        tk.Button(btnframe, text="Edit selected", command=self._on_edit, font=("Arial", 14)).pack(side="left", padx=5)
        tk.Button(btnframe, text="Delete selected", command=self._on_delete, font=("Arial", 14)).pack(side="left", padx=5)
        tk.Button(btnframe, text="Close", command=self.destroy, font=("Arial", 14)).pack(side="right", padx=5)

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
    def __init__(self, master, username: str, db_path: str, user_id: str):
        super().__init__(master)
        self.title(f"Welcome to Activity Dashboard - {username}")
        self.geometry("700x900")
        self.username = username
        self.user_id = user_id
        self.db_path = db_path
        
        # Add header and button to view all logs with bigger fonts
        header_frame = tk.Frame(self)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(header_frame, text=f"Activity Dashboard - {username}", font=("Arial", 18)).pack(side="left")
        tk.Button(header_frame, text="View All Activity Logs", 
                 command=self._open_all_logs_window, 
                 font=("Arial", 16)).pack(side="right")

        # Activity logging UI
        al = ActivityLogFrame(self, db_path, user_id)
        al.pack(expand=True, fill="both")
    
    def _open_all_logs_window(self):
        AllActivityLogsWindow(self, self.db_path, self.user_id)

class App(tk.Tk):
    def __init__(self, db_path):
        super().__init__()
        self.title("Laihdutanyt - v1")
        self.geometry("450x300")
        self.db_path = db_path
        self.user_repo = UserRepository(db_path)
        self.food_repo = FoodRepository(db_path)
        self.foodlog_repo = FoodLogRepository(db_path)
        self.activity_repo = ActivityRepository(db_path)
        self.activitylog_repo = ActivityLogRepository(db_path)
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
        self.login_frame = LoginFrame(self, self.user_repo, self._on_login_success)
        self.login_frame.pack(expand=True, fill="both")

    def _on_login_success(self, username):
        # fetch user object to get user_id
        user = self.user_repo.find_by_username(username)
        if not user:
            messagebox.showerror("Error", "User record not found after login.")
            return
        # Store user information for dashboard use
        self.current_username = username
        self.current_user_id = user.user_id  # or user['user_id'] depending on your user object structure
        self.login_frame.pack_forget()
        self._build_dashboard()
        
    def _build_dashboard(self):
        self.switch = 0  # Initialize switch variable
        # Add title label with bigger font
        tk.Label(self, text=f"Welcome, {self.current_username}!", font=("Arial", 18)).pack(pady=20)
        
        # Button to view food logs with bigger font
        tk.Button(self, text="View Food Logs",
                  command=lambda: self.button_pressed(1), font=("Arial", 16)).pack(pady=10)
        # Button to view activity logs with bigger font  
        tk.Button(self, text="View Activity Logs",
                  command=lambda: self.button_pressed(2), font=("Arial", 16)).pack(pady=10)

    def button_pressed(self, button_id):
        self.switch = button_id  # Update the switch variable
        print(f"Button {self.switch} pressed")
        # Call the corresponding window methods
        if self.switch == 1:
            Dashboard_food(self, self.current_username, self.db_path, self.current_user_id)
        elif self.switch == 2:
            Dashboard_activity(self, self.current_username, self.db_path, self.current_user_id)

def main():
    if not os.path.exists(DB_PATH):
        messagebox.showerror("Missing database", f"Database not found: {DB_PATH}\nRun create_db.py first.")
        return
    app = App(DB_PATH)
    app.mainloop()

if __name__ == "__main__":
    main()
	
# Refactoroitu, alussa generoitu koodi päättyy