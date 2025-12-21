"""
Logs View - All food and activity logs viewers with edit/delete
Uses services for business logic
"""

import tkinter as tk
from tkinter import messagebox, ttk, simpledialog

from services import FoodService, ActivityService


class AllFoodLogsWindow(tk.Toplevel):
    """View, edit, and delete all food logs"""
    
    def __init__(self, master, food_service: FoodService, user_id: str):
        super().__init__(master)
        self.food_service = food_service
        self.user_id = user_id
        self.title("All Food Logs")
        self.geometry("500x700")  # Narrower width to match other windows
        self._build()
        self.refresh_logs()

    def _build(self):
        topframe = tk.Frame(self)
        topframe.pack(fill="x", padx=5, pady=12)
        
        tk.Label(topframe, text="All Food Logs", font=("Arial", 15)).pack(side="left")
        tk.Button(topframe, text="Refresh", command=self.refresh_logs, font=("Arial", 15)).pack(side="right", padx=5)
        
        style = ttk.Style()
        style.configure("FoodLogs.Treeview", font=("Arial", 12), rowheight=25)
        style.configure("FoodLogs.Treeview.Heading", font=("Arial", 12, "bold"))
        
        columns = ("date", "food", "portion", "kcal", "log_id")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse", style="FoodLogs.Treeview")
        
        self.tree.heading("date", text="Date")
        self.tree.heading("food", text="Food")
        self.tree.heading("portion", text="Portion (g)")
        self.tree.heading("kcal", text="Calories")
        
        self.tree.column("date", width=85, anchor='center')
        self.tree.column("food", width=170, anchor='center')
        self.tree.column("portion", width=75, anchor='center')
        self.tree.column("kcal", width=75, anchor='center')
        self.tree.column("log_id", width=0, stretch=False)
        
        self.tree.pack(fill="both", expand=True, padx=5, pady=12)

        btnframe = tk.Frame(self)
        btnframe.pack(fill="x", pady=12)
        tk.Button(btnframe, text="Edit selected", command=self._on_edit, font=("Arial", 15)).pack(side="left", padx=5)
        tk.Button(btnframe, text="Delete selected", command=self._on_delete, font=("Arial", 15)).pack(side="left", padx=5)
        tk.Button(btnframe, text="Close", command=self.destroy, font=("Arial", 15)).pack(side="right", padx=5)

    def refresh_logs(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        
        logs = self.food_service.get_all_food_logs(self.user_id)
        for log in logs:
            self.tree.insert("", "end", values=(
                log['date'], log['name'], log['portion'], 
                f"{log['calories']:.1f}", log['log_id']
            ))

    def _selected_log(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select row", "Please select a log row first.")
            return None
        vals = self.tree.item(sel[0], "values")
        return {"date": vals[0], "food": vals[1], "portion": vals[2], "kcal": vals[3], "log_id": vals[4]}

    def _on_edit(self):
        sel = self._selected_log()
        if not sel:
            return
        new_portion = simpledialog.askstring("Edit portion", f"Portion(g) for {sel['food']} on {sel['date']}:", initialvalue=sel["portion"], parent=self)
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
        try:
            self.food_service.update_food_log(sel["log_id"], new_portion_val, new_date)
            messagebox.showinfo("Updated", "Log updated.")
            self.refresh_logs()
        except Exception as e:
            messagebox.showerror("Error", f"Could not update log: {e}")

    def _on_delete(self):
        sel = self._selected_log()
        if not sel:
            return
        if not messagebox.askyesno("Confirm", f"Delete log for {sel['food']} on {sel['date']}?"):
            return
        try:
            self.food_service.delete_food_log(sel["log_id"])
            messagebox.showinfo("Deleted", "Log deleted.")
            self.refresh_logs()
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete log: {e}")


class AllActivityLogsWindow(tk.Toplevel):
    """View, edit, and delete all activity logs"""
    
    def __init__(self, master, activity_service: ActivityService, user_id: str):
        super().__init__(master)
        self.activity_service = activity_service
        self.user_id = user_id
        self.title("All Activity Logs")
        self.geometry("500x700")  # Narrower width to match other windows
        self._build()
        self.refresh_logs()

    def _build(self):
        topframe = tk.Frame(self)
        topframe.pack(fill="x", padx=5, pady=12)
        
        tk.Label(topframe, text="All Activity Logs", font=("Arial", 15)).pack(side="left")
        tk.Button(topframe, text="Refresh", command=self.refresh_logs, font=("Arial", 15)).pack(side="right", padx=5)
        
        style = ttk.Style()
        style.configure("ActivityLogs.Treeview", font=("Arial", 12), rowheight=25)
        style.configure("ActivityLogs.Treeview.Heading", font=("Arial", 12, "bold"))
        
        columns = ("date", "activity", "count", "kcal", "log_id")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse", style="ActivityLogs.Treeview")
        
        self.tree.heading("date", text="Date")
        self.tree.heading("activity", text="Activity")
        self.tree.heading("count", text="Count")
        self.tree.heading("kcal", text="Kcal Burned")
        
        self.tree.column("date", width=85, anchor='center')
        self.tree.column("activity", width=170, anchor='center')
        self.tree.column("count", width=75, anchor='center')
        self.tree.column("kcal", width=75, anchor='center')
        self.tree.column("log_id", width=0, stretch=False)
        
        self.tree.pack(fill="both", expand=True, padx=5, pady=12)

        btnframe = tk.Frame(self)
        btnframe.pack(fill="x", pady=12)
        tk.Button(btnframe, text="Edit selected", command=self._on_edit, font=("Arial", 15)).pack(side="left", padx=5)
        tk.Button(btnframe, text="Delete selected", command=self._on_delete, font=("Arial", 15)).pack(side="left", padx=5)
        tk.Button(btnframe, text="Close", command=self.destroy, font=("Arial", 15)).pack(side="right", padx=5)

    def refresh_logs(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        
        logs = self.activity_service.get_all_activity_logs(self.user_id)
        for log in logs:
            self.tree.insert("", "end", values=(
                log['date'], log['name'], log['count'],
                f"{log['kcal_burned']:.1f}", log['log_id']
            ))

    def _selected_log(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select row", "Please select a log row first.")
            return None
        vals = self.tree.item(sel[0], "values")
        return {"date": vals[0], "activity": vals[1], "count": vals[2], "kcal": vals[3], "log_id": vals[4]}

    def _on_edit(self):
        sel = self._selected_log()
        if not sel:
            return
        new_count = simpledialog.askstring("Edit count", f"Count for {sel['activity']} on {sel['date']}:", initialvalue=sel["count"], parent=self)
        if new_count is None:
            return
        try:
            new_count_val = int(new_count)
        except ValueError:
            messagebox.showwarning("Invalid", "Count must be integer.")
            return
        new_date = simpledialog.askstring("Edit date", "YYYY-MM-DD:", initialvalue=sel["date"], parent=self)
        if new_date is None:
            return
        try:
            self.activity_service.update_activity_log(sel["log_id"], new_count_val, new_date)
            messagebox.showinfo("Updated", "Log updated.")
            self.refresh_logs()
        except Exception as e:
            messagebox.showerror("Error", f"Could not update log: {e}")

    def _on_delete(self):
        sel = self._selected_log()
        if not sel:
            return
        if not messagebox.askyesno("Confirm", f"Delete log for {sel['activity']} on {sel['date']}?"):
            return
        try:
            self.activity_service.delete_activity_log(sel["log_id"])
            messagebox.showinfo("Deleted", "Log deleted.")
            self.refresh_logs()
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete log: {e}")
