
# modifioitu generoitu koodi alkaa 
# Week 4: added manually new features:
# - activities handling + UI
# - activitieslog handling + UI
# - testing and corrections
"""
laihdutanyt_v1.py 
Tkinter with:
 - Food CRUD
 - Food Logging UI
 - Import Foods (CSV)
 - Activity CRUD
 - Activity Logging
 - View All Logs window with Edit/Delete functionality
"""

import os
import tkinter as tk
from tkinter import messagebox, filedialog, ttk, simpledialog
import importlib
from datetime import date

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
        tk.Label(self, text="Login", font=("Arial", 18)).grid(row=0, column=0, columnspan=2, pady=5)
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
        tk.Label(self, text="Create new user", font=("Arial", 18)).grid(row=0, column=0, columnspan=2, pady=5)
        tk.Label(self, text="Username").grid(row=1, column=0, sticky="e")
        tk.Label(self, text="Password").grid(row=2, column=0, sticky="e")
        tk.Label(self, text="Weight (kg)").grid(row=3, column=0, sticky="e")
        tk.Label(self, text="Length (cm)").grid(row=4, column=0, sticky="e")
        tk.Label(self, text="Age (kg)").grid(row=5, column=0, sticky="e")

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.weight_var = tk.StringVar()
        self.length_var = tk.StringVar()
        self.age_var = tk.StringVar()

        tk.Entry(self, textvariable=self.username_var).grid(row=1, column=1)
        tk.Entry(self, textvariable=self.password_var, show="*").grid(row=2, column=1)
        tk.Entry(self, textvariable=self.weight_var).grid(row=3, column=1)
        tk.Entry(self, textvariable=self.length_var).grid(row=4, column=1)
        tk.Entry(self, textvariable=self.age_var).grid(row=5, column=1)

        tk.Button(self, text="Create user", command=self._on_create).grid(row=4, column=0, columnspan=2, pady=10)

    def _on_create(self):
        username = self.username_var.get().strip()
        password = self.password_var.get()
        weight = None
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

        if not username or not password:
            messagebox.showwarning("Missing info", "Enter username and password.")
            return

        existing = self.user_repo.find_by_username(username)
        if existing:
            messagebox.showerror("Error", "Username already taken.")
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
        self.log_repo = FoodLogRepository(db_path)
        self._build()
        self.refresh_foods()
        self.refresh_logs()

    def _build(self):
        topframe = tk.Frame(self)
        topframe.pack(fill="x", padx=5, pady=5)

        tk.Label(topframe, text="Add food log").grid(row=0, column=0, columnspan=4)

        tk.Label(topframe, text="Food").grid(row=1, column=0, sticky="e")
        tk.Label(topframe, text="Portion (g)").grid(row=1, column=2, sticky="e")
        tk.Label(topframe, text="Date (YYYY-MM-DD)").grid(row=2, column=0, sticky="e")

        self.food_var = tk.StringVar()
        self.portion_var = tk.StringVar(value="100")
        self.date_var = tk.StringVar(value=date.today().isoformat())

        self.food_cb = ttk.Combobox(topframe, textvariable=self.food_var, state="readonly", width=40)
        self.food_cb.grid(row=1, column=1, padx=5, pady=2)
        tk.Entry(topframe, textvariable=self.portion_var, width=10).grid(row=1, column=3, padx=5)
        tk.Entry(topframe, textvariable=self.date_var, width=15).grid(row=2, column=1, padx=5)

        tk.Button(topframe, text="Add Log", command=self._on_add).grid(row=3, column=0, columnspan=4, pady=8)

        # logs list
        self.logs_list = tk.Listbox(self, height=8)
        self.logs_list.pack(fill="both", expand=True, padx=5, pady=5)

    def refresh_foods(self):
        foods = self.food_repo.find_all()
        display = [f"{f['name']}|{f['food_id']}" for f in foods]
        self.food_cb["values"] = display
        if display:
            self.food_cb.current(0)

    def refresh_logs(self):
        self.logs_list.delete(0, tk.END)
        rows = self.log_repo.find_by_user_and_date(self.user_id, self.date_var.get())
        for r in rows:
            name = r.get("name") or "?"
            portion = r.get("portion_size_g") or 0
            cal_per = r.get("calories_per_portion") or 0
            total_cal = (portion / 100.0) * cal_per
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
        self.log_repo.create_log(self.user_id, food_id, date_str, portion)
        messagebox.showinfo("Saved", "Food log saved.")
        self.refresh_logs()

class AllLogsWindow(tk.Toplevel):
    """Window to view, edit, and delete all logs for the logged-in user."""
    def __init__(self, master, db_path: str, user_id: str):
        super().__init__(master)
        self.db_path = db_path
        self.user_id = user_id
        self.food_repo = FoodRepository(db_path)
        self.log_repo = FoodLogRepository(db_path)
        self.title("All Food Logs")
        self.geometry("700x400")
        self._build()
        self.refresh()

    def _build(self):
        top = tk.Frame(self)
        top.pack(fill="x", padx=5, pady=5)
        tk.Label(top, text="All logs for user", font=("Arial", 14)).pack(side="left")
        self.search_var = tk.StringVar()
        tk.Entry(top, textvariable=self.search_var, width=30).pack(side="right")
        tk.Button(top, text="Refresh", command=self.refresh).pack(side="right", padx=5)

        # Treeview with columns: date, food name, portion, calories
        columns = ("date", "food", "portion", "calories", "log_id")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("date", text="Date")
        self.tree.heading("food", text="Food")
        self.tree.heading("portion", text="Portion (g)")
        self.tree.heading("calories", text="Calories")
        # log_id column hidden
        self.tree.column("log_id", width=0, stretch=False)
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        btnframe = tk.Frame(self)
        btnframe.pack(fill="x", pady=5)
        tk.Button(btnframe, text="Edit selected", command=self._on_edit).pack(side="left", padx=5)
        tk.Button(btnframe, text="Delete selected", command=self._on_delete).pack(side="left", padx=5)
        tk.Button(btnframe, text="Close", command=self.destroy).pack(side="right", padx=5)

    def refresh(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        rows = self.log_repo.find_all_for_user(self.user_id)
        for r in rows:
            cal_per = r.get("calories_per_portion") or 0.0
            portion = r.get("portion") or 0.0
            total_cal = (portion / 100.0) * cal_per
            self.tree.insert("", "end", values=(r.get("date"), r.get("name"), f"{total_cal:.1f}", f"{total_cal:.1f}", r.get("log_id")))

    def _selected_log(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select row", "Please select a log row first.")
            return None
        vals = self.tree.item(sel[0], "values")
        # values: (date, food, portion, calories, log_id)
        return {
            "date": vals[0],
            "food": vals[1],
            "portion": vals[2],
            "calories": vals[3],
            "log_id": vals[4]
        }

    def _on_edit(self):
        sel = self._selected_log()
        if not sel:
            return
        # Prompt for new portion and date
        new_portion = simpledialog.askstring("Edit portion", f"Portion (g) for {sel['food']} on {sel['date']}:", initialvalue=sel["portion"], parent=self)
        if new_portion is None:
            return
        try:
            new_portion_val = float(new_portion)
        except ValueError:
            messagebox.showwarning("Invalid", "Portion must be numeric.")
            return
        new_date = simpledialog.askstring("Edit date", "Date (YYYY-MM-DD):", initialvalue=sel["date"], parent=self)
        if new_date is None:
            return
        # Update in DB
        try:
            with self.log_repo._conn() as conn:
                cur = conn.cursor()
                cur.execute("UPDATE foodlog SET portion_size_g = ?, date = ? WHERE log_id = ?", (new_portion_val, new_date, sel["log_id"]))
                conn.commit()
            messagebox.showinfo("Updated", "Log updated.")
            self.refresh()
        except Exception as e:
            messagebox.showerror("Error", f"Could not update log: {e}")

    def _on_delete(self):
        sel = self._selected_log()
        if not sel:
            return
        if not messagebox.askyesno("Confirm", f"Delete log for {sel['food']} on {sel['date']}?"):
            return
        try:
            with self.log_repo._conn() as conn:
                cur = conn.cursor()
                cur.execute("DELETE FROM foodlog WHERE log_id = ?", (sel["log_id"],))
                conn.commit()
            messagebox.showinfo("Deleted", "Log deleted.")
            self.refresh()
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete log: {e}")

# Activity ----------------------
class ActivityLogFrame(tk.Frame):
    def __init__(self, master, db_path: str, user_id: str):
        super().__init__(master)
        self.db_path = db_path
        self.user_id = user_id
        self.activity_repo = ActivityRepository(db_path)
        self.log_repo = ActivityLogRepository(db_path)
        self._build()
        self.refresh_activities()
        self.refresh_logs()

    def _build(self):
        topframe = tk.Frame(self)
        topframe.pack(fill="x", padx=5, pady=5)

        tk.Label(topframe, text="Add activity log").grid(row=0, column=0, columnspan=4)

        tk.Label(topframe, text="Activity").grid(row=1, column=0, sticky="e")
        tk.Label(topframe, text="Unit (steps)").grid(row=1, column=2, sticky="e")
        tk.Label(topframe, text="Date (YYYY-MM-DD)").grid(row=2, column=1, sticky="e")

        self.activity_var = tk.StringVar()
        self.unit_var = tk.StringVar(value="100")
        self.date_var = tk.StringVar(value=date.today().isoformat())

        self.activity_cb = ttk.Combobox(topframe, textvariable=self.activity_var, state="readonly", width=16)
        self.activity_cb.grid(row=1, column=1, padx=5, pady=2)
        tk.Entry(topframe, textvariable=self.unit_var, width=10).grid(row=1, column=3, padx=5)
        tk.Entry(topframe, textvariable=self.date_var, width=15).grid(row=2, column=1, padx=5)

        tk.Button(topframe, text="Add Log", command=self._on_add).grid(row=3, column=0, columnspan=4, pady=8)

        # logs list
        self.logs_list = tk.Listbox(self, height=8)
        self.logs_list.pack(fill="both", expand=True, padx=5, pady=5)

    def refresh_activities(self):
        activities = self.activity_repo.find_all()
        display = [f"{f['name']}|{f['activity_id']}" for f in activities]
        self.activity_cb["values"] = display
        if display:
            self.activity_cb.current(0)

    def refresh_logs(self):
        self.logs_list.delete(0, tk.END)
        rows = self.activitylog_repo.find_by_user_and_date(self.user_id, self.date_var.get())
        for r in rows:
            name = r.get("name") or "?"
            unit = r.get("units") or 0
            cal_per = r.get("calories_per_unit") or 0
            total_cal = (unit) * cal_per
            self.logs_list.insert(tk.END, f"{r['date']} - {name} {unit}g ({total_cal:.1f} kcal)")

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
            unit = float(self.unit_var.get())
        except ValueError:
            messagebox.showwarning("Invalid unit", "Unit must be integer.")
            return
        date_str = self.date_var.get().strip()
        self.activitylog_repo.create_log(self.user_id, activity_id, date_str, unit, activity_count)
        messagebox.showinfo("Saved", "Activity log saved.")
        self.refresh_logs()
        
class AllLogsWindow(tk.Toplevel):
    """Window to view, edit, and delete all logs for the logged-in user."""
    def __init__(self, master, db_path: str, user_id: str):
        super().__init__(master)
        self.db_path = db_path
        self.user_id = user_id
        self.activity_repo = ActivityRepository(db_path)
        self.log_repo = ActivityLogRepository(db_path)
        self.title("All Activity Logs")
        self.geometry("700x400")
        self._build()
        self.refresh()

    def _build(self):
        top = tk.Frame(self)
        top.pack(fill="x", padx=5, pady=5)
        tk.Label(top, text="All logs for user", font=("Arial", 18)).pack(side="left")
        self.search_var = tk.StringVar()
        tk.Entry(top, textvariable=self.search_var, width=30).pack(side="right")
        tk.Button(top, text="Refresh", command=self.refresh).pack(side="right", padx=5)

        # Treeview with columns: date, activity name, unit, calories_per_unit
        columns = ("date", "activity", "unit", "calories_per_unit", "log_id")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("date", text="Date")
        self.tree.heading("activity", text="Activity")
        self.tree.heading("unit", text="Unit (steps)")
        self.tree.heading("calories_per_unit", text="Calories per unit")
        # log_id column hidden
        self.tree.column("log_id", width=0, stretch=False)
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        btnframe = tk.Frame(self)
        btnframe.pack(fill="x", pady=5)
        tk.Button(btnframe, text="Edit selected", command=self._on_edit).pack(side="left", padx=5)
        tk.Button(btnframe, text="Delete selected", command=self._on_delete).pack(side="left", padx=5)
        tk.Button(btnframe, text="Close", command=self.destroy).pack(side="right", padx=5)

    def refresh(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        rows = self.log_repo.find_all_for_user(self.user_id)
        for r in rows:
            cal_per = r.get("calories_burned_per_unit") or 0.0
            unit = r.get("unit") or 0.0
            total_cal = (unit) * cal_per
            self.tree.insert("", "end", values=(r.get("date"), r.get("name"), f"{unit}", f"{total_cal:.1f}", r.get("log_id")))

    def _selected_log(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select row", "Please select a log row first.")
            return None
        vals = self.tree.item(sel[0], "values")
        # values: (date, activity, unit, calories_burned, log_id)
        return {
            "date": vals[0],
            "activity": vals[1],
            "unit": vals[2],
            "calories_burned": vals[3],
            "log_id": vals[4]
        }

    def _on_edit(self):
        sel = self._selected_log()
        if not sel:
            return
        # Prompt for new unit and date
        new_unit = simpledialog.askstring("Edit unit", f"Unit for {sel['activity']} on {sel['date']}:", initialvalue=sel["unit"], parent=self)
        if new_unit is None:
            return
        try:
            new_unit_val = float(new_unit)
        except ValueError:
            messagebox.showwarning("Invalid", "Unit must be integer.")
            return
        new_date = simpledialog.askstring("Edit date", "Date (YYYY-MM-DD):", initialvalue=sel["date"], parent=self)
        if new_date is None:
            return
        # Update in DB
        try:
            with self.log_repo._conn() as conn:
                cur = conn.cursor()
                cur.execute("UPDATE activitylog SET unit_size = ?, date = ? WHERE log_id = ?", (new_unit_val, new_date, sel["log_id"]))
                conn.commit()
            messagebox.showinfo("Updated", "Log updated.")
            self.refresh()
        except Exception as e:
            messagebox.showerror("Error", f"Could not update log: {e}")

    def _on_delete(self):
        sel = self._selected_log()
        if not sel:
            return
        if not messagebox.askyesno("Confirm", f"Delete log for {sel['activity']} on {sel['date']}?"):
            return
        try:
            with self.log_repo._conn() as conn:
                cur = conn.cursor()
                cur.execute("DELETE FROM activitylog WHERE log_id = ?", (sel["log_id"],))
                conn.commit()
            messagebox.showinfo("Deleted", "Log deleted.")
            self.refresh()
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete log: {e}")

class Dashboard_food(tk.Frame):
    def __init__(self, master, username: str, db_path: str, user_id: str):
        super().__init__(master)
        self.username = username
        self.user_id = user_id
        tk.Label(self, text=f"Welcome, {username}", font=("Arial", 18)).pack(pady=10)
        # Food logging UI
        fl = FoodLogFrame(self, db_path, user_id)
        fl.pack(expand=True, fill="both")
        tk.Button(self, text="View All Logs", command=lambda: AllLogsWindow(self, db_path, user_id)).pack(pady=5)
        
class Dashboard_activity(tk.Frame):
    def __init__(self, master, username: str, db_path: str, user_id: str):
        super().__init__(master)
        self.username = username
        self.user_id = user_id
        tk.Label(self, text=f"Welcome, {username}", font=("Arial", 18)).pack(pady=10)
        # Activity logging UI
        fl = ActivityLogFrame(self, db_path, user_id)
        fl.pack(expand=True, fill="both")
        tk.Button(self, text="View All Logs", command=lambda: AllLogsWindow(self, db_path, user_id)).pack(pady=5)

class App(tk.Tk):
    def __init__(self, db_path):
        super().__init__()
        self.title("Laihdutanyt - v1")
        self.geometry("800x600")
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


    def _on_package_project(self):
        try:
            # call packaging script
            pkg_script = os.path.join(os.path.dirname(__file__), "scripts", "package_project.sh")
            if not os.path.exists(pkg_script):
                messagebox.showwarning("Not found", "Packaging script not found.")
                return
            # ask for output dir
            outdir = filedialog.askdirectory(title="Select output folder for package")
            if not outdir:
                return
            # run packaging script
            import subprocess
            subprocess.check_call([pkg_script, outdir])
            messagebox.showinfo("Packaged", f"Project packaged to {outdir}")
        except Exception as e:
            messagebox.showerror("Package error", f"Packaging failed: {e}")

    def _build_login(self):
        self.login_frame = LoginFrame(self, self.user_repo, self._on_login_success)
        self.login_frame.pack(expand=True, fill="both")

    def _on_login_success(self, username):
        # fetch user object to get user_id
        user = self.user_repo.find_by_username(username)
        if not user:
            messagebox.showerror("Error", "User record not found after login.")
            return
        self.login_frame.pack_forget()
        self.dashboard_food = Dashboard_food(self, username, self.db_path, user.user_id)
        self.dashboard_food.pack(expand=True, fill="both")
        self.dashboard_activity = Dashboard_activity(self, username, self.db_path, user.user_id)
        self.dashboard_activity.pack(expand=True, fill="both")

def main():
    if not os.path.exists(DB_PATH):
        messagebox.showerror("Missing database", f"Database not found: {DB_PATH}\nRun create_db.py first.")
        return
    app = App(DB_PATH)
    app.mainloop()

if __name__ == "__main__":
    main()
	
# modifioitu generoitu koodi päättyy