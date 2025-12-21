"""
Weight Logging View - Weight tracking interface with period annotations
Uses WeightLogService and DietaryPeriodService for all business logic
"""

import tkinter as tk
from tkinter import messagebox, ttk
from datetime import date, datetime
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from services.weightlog_service import WeightLogService
    from services.dietary_period_service import DietaryPeriodService


class WeightLogFrame(tk.Frame):
    """Weight logging form component"""
    
    def __init__(self, master, weightlog_service: 'WeightLogService', user_id: str, 
                 dashboard=None, dietary_period_service=None):
        super().__init__(master)
        self.weightlog_service = weightlog_service
        self.dietary_period_service = dietary_period_service
        self.user_id = user_id
        self.dashboard = dashboard
        
        # Date input
        self.date_var = tk.StringVar(value=date.today().strftime('%Y-%m-%d'))
        
        # Weight input
        self.weight_var = tk.DoubleVar(value=70.0)
        
        # Notes input
        self.notes_var = tk.StringVar()
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the UI components"""
        topframe = tk.Frame(self)
        topframe.pack(fill="x", padx=10, pady=10)
        
        # Show active periods info
        if self.dietary_period_service:
            active_periods = self.dietary_period_service.get_active_periods(self.user_id)
            if active_periods:
                period_names = [p['period_name'] for p in active_periods]
                # Limit display if too many periods (show first 3 + count)
                if len(period_names) > 3:
                    display_names = ', '.join(period_names[:3])
                    info_text = f"📍 Active Periods ({len(period_names)}): {display_names}... (+{len(period_names)-3} more)"
                else:
                    info_text = f"📍 Active Periods: {', '.join(period_names)}"
                tk.Label(topframe, text=info_text, font=("Arial", 12, "bold"), 
                        fg="#2e7d32", wraplength=850, justify="left").grid(
                    row=0, column=0, columnspan=2, sticky="w", padx=5, pady=(0, 10)
                )
        
        # Weight input
        tk.Label(topframe, text="Weight (kg)", font=("Arial", 11)).grid(
            row=1, column=0, sticky="w", padx=5, pady=5
        )
        weight_entry = tk.Entry(
            topframe, textvariable=self.weight_var, width=10, font=("Arial", 11)
        )
        weight_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        # Date input
        tk.Label(topframe, text="Date", font=("Arial", 11)).grid(
            row=2, column=0, sticky="w", padx=5, pady=5
        )
        tk.Entry(topframe, textvariable=self.date_var, width=15, font=("Arial", 11)).grid(
            row=2, column=1, sticky="w", padx=5, pady=5
        )
        
        # Notes input
        tk.Label(topframe, text="Notes", font=("Arial", 11)).grid(
            row=3, column=0, sticky="w", padx=5, pady=5
        )
        notes_entry = tk.Entry(
            topframe, textvariable=self.notes_var, width=30, font=("Arial", 11)
        )
        notes_entry.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        
        # Add button
        tk.Button(
            topframe, text="Log Weight", command=self._on_add, 
            font=("Arial", 11, "bold"), bg="#90caf9", width=20
        ).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Info label
        info_label = tk.Label(
            self, 
            text="💡 Weight is logged with week numbers and period annotations",
            font=("Arial", 11, "italic"), fg="#555"
        )
        info_label.pack(pady=5)
    
    def _on_add(self):
        """Handle add weight button click"""
        try:
            weight = self.weight_var.get()
            date_str = self.date_var.get()
            notes = self.notes_var.get().strip() or None
            
            result = self.weightlog_service.log_weight(
                user_id=self.user_id,
                date_str=date_str,
                weight=weight,
                notes=notes
            )
            
            if result["success"]:
                messagebox.showinfo("Success", result["message"])
                # Notify parent to refresh history
                if self.dashboard:
                    self.dashboard.refresh_history()
                # Clear notes but keep weight for next entry
                self.notes_var.set("")
            else:
                error_msg = result.get("message") or result.get("error", "Unknown error")
                messagebox.showerror("Error", error_msg)
                
        except tk.TclError:
            messagebox.showerror("Error", "Please enter a valid weight value")


class WeightHistoryFrame(tk.Frame):
    """Weight history display with week numbers and period annotations"""
    
    def __init__(self, master, weightlog_service: 'WeightLogService', 
                 dietary_period_service: Optional['DietaryPeriodService'], user_id: str):
        super().__init__(master)
        self.weightlog_service = weightlog_service
        self.dietary_period_service = dietary_period_service
        self.user_id = user_id
        
        self._setup_ui()
        self.refresh()
    
    def _setup_ui(self):
        """Setup the UI components"""
        # Title
        tk.Label(
            self, text="Weight History with Periods", 
            font=("Arial", 12, "bold")
        ).pack(pady=5)
        
        # Summary info
        self.summary_label = tk.Label(
            self, text="Loading...", 
            font=("Arial", 11), fg="#2e7d32"
        )
        self.summary_label.pack(pady=2)
        
        # Create frame for treeview with scrollbar
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Create treeview
        columns = ("date", "week", "weight", "change", "periods")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        # Column headings
        self.tree.heading("date", text="Date")
        self.tree.heading("week", text="Week")
        self.tree.heading("weight", text="Weight (kg)")
        self.tree.heading("change", text="Change")
        self.tree.heading("periods", text="Periods")
        
        # Column widths - narrowed left columns to give more space for periods
        self.tree.column("date", width=85)
        self.tree.column("week", width=80)
        self.tree.column("weight", width=75)
        self.tree.column("change", width=70)
        self.tree.column("periods", width=450)  # More space for multiple period names
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Context menu for delete
        self.tree.bind("<Button-3>", self._show_context_menu)
        
        # Legend
        legend_frame = tk.Frame(self)
        legend_frame.pack(pady=5)
        
        tk.Label(
            legend_frame, 
            text="📍 = Active Period  |  ▶ = Period Start  |  ⏹ = Period End",
            font=("Arial", 11, "italic"), fg="#555"
        ).pack()
    
    def refresh(self):
        """Refresh the weight history display"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get weight history with weeks and periods
        history = self.weightlog_service.get_weight_history_with_weeks(
            user_id=self.user_id,
            days=365  # Get full year of data
        )
        
        if not history:
            self.summary_label.config(text="No weight entries yet")
            return
        
        # Calculate summary statistics
        total_entries = len(history)
        current_weight = history[0]["weight"]  # Most recent (first in descending order)
        
        # Get progress summary from service
        progress_result = self.weightlog_service.get_progress_summary(self.user_id)
        
        if progress_result.get("has_data"):
            summary_text = (
                f"📊 Total Entries: {total_entries} | "
                f"Current: {progress_result.get('current_weight', current_weight):.1f} kg"
            )
            
            # Add weekly change if available
            weekly = progress_result.get("weekly_change")
            if weekly and isinstance(weekly, dict):
                summary_text += f" | Weekly: {weekly.get('weight_change', 0):+.2f} kg"
            
            # Add monthly change if available
            monthly = progress_result.get("monthly_change")
            if monthly and isinstance(monthly, dict):
                summary_text += f" | Monthly: {monthly.get('weight_change', 0):+.2f} kg"
        else:
            summary_text = f"📊 Total Entries: {total_entries} | Current: {current_weight:.1f} kg"
        
        self.summary_label.config(text=summary_text)
        
        # Populate tree
        for entry in history:
            # Get current week for formatting
            current_week = entry.get("week_number")
            
            # Format date
            log_date = entry["date"]
            
            # Format week info
            week_info = ""
            if entry.get("is_week_start"):
                week_info = f"★ Week {current_week}"
            else:
                week_info = f"Week {current_week}"
            
            # Format weight
            weight = f"{entry['weight']:.1f}"
            
            # Format change
            change = ""
            if entry.get("weight_change") is not None:
                weight_change = entry["weight_change"]
                change = f"{weight_change:+.1f} kg"
            
            # Format periods - use period_markers which contains formatted strings
            periods_text = ""
            if entry.get("period_markers"):
                periods_text = " | ".join(entry["period_markers"])
            
            # Insert with tag for week starts and store log_id
            tags = ("week_start",) if entry.get("is_week_start") else ()
            
            self.tree.insert(
                "", "end", 
                values=(log_date, week_info, weight, change, periods_text),
                tags=(entry["log_id"], *tags)  # Store log_id in tags
            )
        
        # Configure tag for week starts (bold)
        self.tree.tag_configure("week_start", font=("Arial", 11, "bold"))
    
    def _show_context_menu(self, event):
        """Show context menu for delete option"""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            menu = tk.Menu(self, tearoff=0)
            menu.add_command(label="Delete Entry", command=self._delete_selected)
            menu.post(event.x_root, event.y_root)
    
    def _delete_selected(self):
        """Delete the selected weight entry"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.tree.item(item, "values")
        tags = self.tree.item(item, "tags")
        log_date = values[0]
        log_id = tags[0]  # First tag is the log_id
        
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Delete weight entry from {log_date}?"
        )
        
        if confirm:
            result = self.weightlog_service.delete_weight_log(log_id)
            
            if result["success"]:
                messagebox.showinfo("Success", result["message"])
                self.refresh()
            else:
                error_msg = result.get("message") or result.get("error", "Unknown error")
                messagebox.showerror("Error", error_msg)


class DashboardWeight(tk.Toplevel):
    """Main weight logging dashboard window"""
    
    def __init__(self, parent, weightlog_service: 'WeightLogService',
                 dietary_period_service: Optional['DietaryPeriodService'],
                 username: str, user_id: str):
        super().__init__(parent)
        self.title(f"Weight Tracking - {username}")
        self.geometry("1050x700")
        
        self.weightlog_service = weightlog_service
        self.dietary_period_service = dietary_period_service
        self.user_id = user_id
        
        # Main container
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="🏋️ Weight Tracking Dashboard",
            font=("Arial", 16, "bold"), fg="#1565c0"
        )
        title_label.pack(pady=10)
        
        # Input form at top
        self.log_frame = WeightLogFrame(
            main_frame, weightlog_service, user_id, 
            dashboard=self, dietary_period_service=dietary_period_service
        )
        self.log_frame.pack(fill="x", pady=10)
        
        # Separator
        ttk.Separator(main_frame, orient="horizontal").pack(fill="x", pady=10)
        
        # History display below
        self.history_frame = WeightHistoryFrame(
            main_frame, weightlog_service, dietary_period_service, user_id
        )
        self.history_frame.pack(fill="both", expand=True)
        
        # Button frame at bottom
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        tk.Button(
            button_frame, text="Refresh", command=self.refresh_history,
            font=("Arial", 11), bg="#e3f2fd", width=15
        ).pack(side="left", padx=5)
        
        tk.Button(
            button_frame, text="Close", command=self.destroy,
            font=("Arial", 11), bg="#ffebee", width=15
        ).pack(side="left", padx=5)
    
    def refresh_history(self):
        """Refresh the weight history display"""
        if hasattr(self, 'history_frame'):
            self.history_frame.refresh()
