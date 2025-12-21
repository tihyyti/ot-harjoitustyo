"""
Dietary Period Management View - Interface for tracking dietary experiments
Uses DietaryPeriodService for all business logic
"""

import tkinter as tk
from tkinter import messagebox, ttk
from datetime import date, datetime
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from services.dietary_period_service import DietaryPeriodService

# Constants
BTN_VIEW_DETAILS = "View Details"


class PeriodCreateFrame(tk.Frame):
    """Period creation form with suggested protocols"""
    
    def __init__(self, master, period_service: 'DietaryPeriodService', user_id: str, 
                 dashboard=None):
        super().__init__(master)
        self.period_service = period_service
        self.user_id = user_id
        self.dashboard = dashboard  # Reference to main dashboard for refresh
        
        # Form variables
        self.period_name_var = tk.StringVar()
        self.start_date_var = tk.StringVar(value=date.today().strftime('%Y-%m-%d'))
        self.end_date_var = tk.StringVar()
        self.protocol_type_var = tk.StringVar(value="custom")
        self.description_var = tk.StringVar()
        
        # Get suggested protocols
        self.suggested_protocols = self.period_service.get_suggested_protocols()
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the UI components"""
        # Title
        tk.Label(
            self, text="Create New Dietary Period", 
            font=("Arial", 13, "bold"), fg="#1565c0"
        ).pack(pady=10)
        
        # Form frame
        form_frame = tk.Frame(self)
        form_frame.pack(fill="x", padx=15, pady=5)
        
        # Period name
        tk.Label(form_frame, text="Period Name:", font=("Arial", 12)).grid(
            row=0, column=0, sticky="w", padx=5, pady=5
        )
        tk.Entry(
            form_frame, textvariable=self.period_name_var, 
            width=35, font=("Arial", 12)
        ).grid(row=0, column=1, padx=5, pady=5)
        
        # Protocol type dropdown
        tk.Label(form_frame, text="Protocol Type:", font=("Arial", 12)).grid(
            row=1, column=0, sticky="w", padx=5, pady=5
        )
        
        protocol_types = [
            "custom", "time_restricted", "meal_timing", 
            "intermittent_fasting", "low_carb", "calorie_cycling",
            "portion_control", "food_elimination"
        ]
        protocol_cb = ttk.Combobox(
            form_frame, textvariable=self.protocol_type_var,
            values=protocol_types, width=32, font=("Arial", 11), state="readonly"
        )
        protocol_cb.grid(row=1, column=1, padx=5, pady=5)
        
        # Start date
        tk.Label(form_frame, text="Start Date:", font=("Arial", 11)).grid(
            row=2, column=0, sticky="w", padx=5, pady=5
        )
        tk.Entry(
            form_frame, textvariable=self.start_date_var, 
            width=15, font=("Arial", 11)
        ).grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        # End date (optional)
        tk.Label(form_frame, text="End Date (optional):", font=("Arial", 11)).grid(
            row=3, column=0, sticky="w", padx=5, pady=5
        )
        tk.Entry(
            form_frame, textvariable=self.end_date_var, 
            width=15, font=("Arial", 11)
        ).grid(row=3, column=1, sticky="w", padx=5, pady=5)
        
        # Description
        tk.Label(form_frame, text="Description:", font=("Arial", 11)).grid(
            row=4, column=0, sticky="nw", padx=5, pady=5
        )
        desc_text = tk.Text(form_frame, width=35, height=3, font=("Arial", 10))
        desc_text.grid(row=4, column=1, padx=5, pady=5)
        self.desc_text = desc_text
        
        # Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)
        
        tk.Button(
            button_frame, text="Create Period", command=self._on_create,
            font=("Arial", 12, "bold"), bg="#4caf50", fg="white", width=15
        ).pack(side="left", padx=5)
        
        tk.Button(
            button_frame, text="Clear Form", command=self._clear_form,
            font=("Arial", 12), bg="#e3f2fd", width=15
        ).pack(side="left", padx=5)
        
        # Suggested protocols section
        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=10)
        
        tk.Label(
            self, text="💡 Suggested Protocols (Click to Use)", 
            font=("Arial", 11, "bold"), fg="#2e7d32"
        ).pack(pady=5)
        
        # Scrollable frame for suggestions
        suggestions_canvas = tk.Canvas(self, height=150)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=suggestions_canvas.yview)
        suggestions_frame = tk.Frame(suggestions_canvas)
        
        suggestions_canvas.create_window((0, 0), window=suggestions_frame, anchor="nw")
        suggestions_canvas.configure(yscrollcommand=scrollbar.set)
        
        suggestions_canvas.pack(side="left", fill="both", expand=True, padx=10)
        scrollbar.pack(side="right", fill="y")
        
        # Add suggested protocols
        for protocol in self.suggested_protocols:
            self._add_protocol_suggestion(suggestions_frame, protocol)
        
        suggestions_frame.update_idletasks()
        suggestions_canvas.configure(scrollregion=suggestions_canvas.bbox("all"))
    
    def _add_protocol_suggestion(self, parent, protocol):
        """Add a protocol suggestion button"""
        frame = tk.Frame(parent, relief="raised", borderwidth=1, bg="#e8f5e9")
        frame.pack(fill="x", padx=5, pady=3)
        
        # Protocol info
        info_frame = tk.Frame(frame, bg="#e8f5e9")
        info_frame.pack(fill="x", padx=5, pady=3)
        
        tk.Label(
            info_frame, text=protocol["name"],
            font=("Arial", 12, "bold"), bg="#e8f5e9", anchor="w"
        ).pack(fill="x")
        
        tk.Label(
            info_frame, text=protocol["description"],
            font=("Arial", 12), bg="#e8f5e9", anchor="w", wraplength=400
        ).pack(fill="x")
        
        duration_text = protocol.get('example_duration', 'flexible')
        tk.Label(
            info_frame, text=f"Suggested duration: {duration_text}",
            font=("Arial", 11, "italic"), bg="#e8f5e9", fg="#666", anchor="w"
        ).pack(fill="x")
        
        # Use button
        tk.Button(
            frame, text="Use This", 
            command=lambda p=protocol: self._use_suggestion(p),
            font=("Arial", 12), bg="#66bb6a", fg="white"
        ).pack(pady=3)
    
    def _use_suggestion(self, protocol):
        """Fill form with suggested protocol"""
        self.period_name_var.set(protocol["name"])
        self.protocol_type_var.set(protocol["type"])
        self.desc_text.delete("1.0", tk.END)
        self.desc_text.insert("1.0", protocol["description"])
        
        # Calculate end date if duration provided
        # Duration is a string like "2-3 weeks", convert to days
        duration_str = protocol.get("example_duration", "")
        if duration_str:
            # Extract first number and convert weeks to days
            # "2-3 weeks" -> 14 days, "1 month" -> 30 days
            from datetime import timedelta
            
            if "week" in duration_str.lower():
                # Extract first number from range like "2-3"
                weeks = int(duration_str.split()[0].split('-')[0])
                duration_days = weeks * 7
            elif "month" in duration_str.lower():
                duration_days = 30
            else:
                duration_days = 14  # default
            
            start = datetime.strptime(self.start_date_var.get(), "%Y-%m-%d")
            end = start + timedelta(days=duration_days)
            self.end_date_var.set(end.strftime("%Y-%m-%d"))
        
        messagebox.showinfo(
            "Template Loaded", 
            f"'{protocol['name']}' template loaded!\nYou can modify the details before creating."
        )
    
    def _on_create(self):
        """Handle create period button click"""
        period_name = self.period_name_var.get().strip()
        start_date_str = self.start_date_var.get().strip()
        end_date_str = self.end_date_var.get().strip() or None
        protocol_type = self.protocol_type_var.get()
        description = self.desc_text.get("1.0", tk.END).strip() or None
        
        if not period_name:
            messagebox.showerror("Error", "Please enter a period name")
            return
        
        if not start_date_str:
            messagebox.showerror("Error", "Please enter a start date")
            return
        
        result = self.period_service.create_period(
            user_id=self.user_id,
            period_name=period_name,
            start_date=start_date_str,
            end_date=end_date_str,
            protocol_type=protocol_type,
            description=description
        )
        
        if result["success"]:
            messagebox.showinfo("Success", result["message"])
            if self.dashboard:
                self.dashboard.refresh_periods()
            self._clear_form()
        else:
            messagebox.showerror("Error", result["message"])
    
    def _clear_form(self):
        """Clear all form fields"""
        self.period_name_var.set("")
        self.start_date_var.set(date.today().strftime('%Y-%m-%d'))
        self.end_date_var.set("")
        self.protocol_type_var.set("custom")
        self.desc_text.delete("1.0", tk.END)


class PeriodListFrame(tk.Frame):
    """Display active and completed periods"""
    
    def __init__(self, master, period_service: 'DietaryPeriodService', user_id: str, dashboard=None):
        super().__init__(master)
        self.period_service = period_service
        self.user_id = user_id
        self.dashboard = dashboard  # Reference to parent dashboard
        
        self._setup_ui()
        self.refresh()
    
    def _setup_ui(self):
        """Setup the UI components"""
        # Title
        tk.Label(
            self, text="Your Dietary Periods", 
            font=("Arial", 13, "bold"), fg="#1565c0"
        ).pack(pady=10)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Active periods tab
        self.active_frame = tk.Frame(self.notebook)
        self.notebook.add(self.active_frame, text="📍 Active Periods")
        
        # Completed periods tab
        self.completed_frame = tk.Frame(self.notebook)
        self.notebook.add(self.completed_frame, text="✓ Completed Periods")
        
        # Setup active periods tree
        self._setup_active_tree()
        
        # Setup completed periods tree
        self._setup_completed_tree()
        
        # Button frame
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)
        
        tk.Button(
            button_frame, text="Refresh", command=self.refresh,
            font=("Arial", 12), bg="#e3f2fd", width=15
        ).pack(side="left", padx=5)
    
    def _setup_active_tree(self):
        """Setup the active periods treeview"""
        # Info label
        tk.Label(
            self.active_frame, 
            text="Active periods will appear in your weight log",
            font=("Arial", 11, "italic"), fg="#666"
        ).pack(pady=5)
        
        # Tree frame
        tree_frame = tk.Frame(self.active_frame)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Treeview
        columns = ("name", "type", "start", "duration")
        self.active_tree = ttk.Treeview(
            tree_frame, columns=columns, show="headings", height=8
        )
        
        self.active_tree.heading("name", text="Period Name")
        self.active_tree.heading("type", text="Type")
        self.active_tree.heading("start", text="Start Date")
        self.active_tree.heading("duration", text="Duration")
        
        self.active_tree.column("name", width=200)
        self.active_tree.column("type", width=120)
        self.active_tree.column("start", width=70)
        self.active_tree.column("duration", width=60)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(
            tree_frame, orient="vertical", command=self.active_tree.yview
        )
        self.active_tree.configure(yscrollcommand=scrollbar.set)
        
        self.active_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Context menu
        self.active_tree.bind("<Button-3>", self._show_active_context_menu)
        
        # Double-click to open weight logging
        self.active_tree.bind("<Double-Button-1>", self._open_weight_logging)
        
        # Buttons
        btn_frame = tk.Frame(self.active_frame)
        btn_frame.pack(pady=5)
        
        tk.Button(
            btn_frame, text="End Period", command=self._end_selected_period,
            font=("Arial", 12), bg="#ff9800", fg="white", width=15
        ).pack(side="left", padx=5)
        
        tk.Button(
            btn_frame, text=BTN_VIEW_DETAILS, command=self._view_period_details,
            font=("Arial", 12), bg="#2196f3", fg="white", width=15
        ).pack(side="left", padx=5)
    
    def _setup_completed_tree(self):
        """Setup the completed periods treeview"""
        # Info label
        tk.Label(
            self.completed_frame, 
            text="View effectiveness and history of past periods",
            font=("Arial", 11, "italic"), fg="#666"
        ).pack(pady=5)
        
        # Tree frame
        tree_frame = tk.Frame(self.completed_frame)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Treeview
        columns = ("name", "type", "dates", "duration", "effectiveness")
        self.completed_tree = ttk.Treeview(
            tree_frame, columns=columns, show="headings", height=8
        )
        
        self.completed_tree.heading("name", text="Period Name")
        self.completed_tree.heading("type", text="Type")
        self.completed_tree.heading("dates", text="Period")
        self.completed_tree.heading("duration", text="Days")
        self.completed_tree.heading("effectiveness", text="Result")
        
        self.completed_tree.column("name", width=180)
        self.completed_tree.column("type", width=120)
        self.completed_tree.column("dates", width=150)
        self.completed_tree.column("duration", width=60)
        self.completed_tree.column("effectiveness", width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(
            tree_frame, orient="vertical", command=self.completed_tree.yview
        )
        self.completed_tree.configure(yscrollcommand=scrollbar.set)
        
        self.completed_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Context menu
        self.completed_tree.bind("<Button-3>", self._show_completed_context_menu)
        
        # Button
        tk.Button(
            self.completed_frame, text=BTN_VIEW_DETAILS, 
            command=self._view_completed_period_details,
            font=("Arial", 12), bg="#2196f3", fg="white", width=15
        ).pack(pady=5)
    
    def refresh(self):
        """Refresh both period lists"""
        self._refresh_active()
        self._refresh_completed()
    
    def _refresh_active(self):
        """Refresh active periods list"""
        # Clear existing
        for item in self.active_tree.get_children():
            self.active_tree.delete(item)
        
        # Get active periods - returns List[Dict] directly
        periods = self.period_service.get_active_periods(self.user_id)
        
        if not periods:
            return
        
        # Populate tree
        for period in periods:
            # Calculate duration
            start = datetime.strptime(period["start_date"], "%Y-%m-%d")
            duration = (datetime.now() - start).days
            duration_text = f"{duration} days"
            
            self.active_tree.insert(
                "", "end",
                values=(
                    period["period_name"],
                    period["protocol_type"],
                    period["start_date"],
                    duration_text
                ),
                tags=(period["period_id"],)
            )
    
    def _refresh_completed(self):
        """Refresh completed periods list"""
        # Clear existing
        for item in self.completed_tree.get_children():
            self.completed_tree.delete(item)
        
        # Get all periods - returns List[Dict] directly
        periods = self.period_service.get_all_periods(self.user_id)
        
        if not periods:
            return
        
        # Filter completed and populate tree
        for period in periods:
            if period["is_active"]:
                continue
            
            # Calculate duration
            if period["end_date"]:
                start = datetime.strptime(period["start_date"], "%Y-%m-%d")
                end = datetime.strptime(period["end_date"], "%Y-%m-%d")
                duration = (end - start).days
                date_range = f"{period['start_date']} to {period['end_date']}"
            else:
                duration = "N/A"
                date_range = period["start_date"]
            
            # Get effectiveness
            effectiveness = "No data"
            summary = self.period_service.get_period_summary(period["period_id"])
            if summary and summary.get("weight_change"):
                weight_data = summary["weight_change"]
                effectiveness = f"{weight_data['change']:+.1f} kg"
            
            self.completed_tree.insert(
                "", "end",
                values=(
                    period["period_name"],
                    period["protocol_type"],
                    date_range,
                    duration,
                    effectiveness
                ),
                tags=(period["period_id"],)
            )
    
    def _show_active_context_menu(self, event):
        """Show context menu for active periods"""
        item = self.active_tree.identify_row(event.y)
        if item:
            self.active_tree.selection_set(item)
            menu = tk.Menu(self, tearoff=0)
            menu.add_command(label="End Period", command=self._end_selected_period)
            menu.add_command(label=BTN_VIEW_DETAILS, command=self._view_period_details)
            menu.post(event.x_root, event.y_root)
    
    def _show_completed_context_menu(self, event):
        """Show context menu for completed periods"""
        item = self.completed_tree.identify_row(event.y)
        if item:
            self.completed_tree.selection_set(item)
            menu = tk.Menu(self, tearoff=0)
            menu.add_command(label=BTN_VIEW_DETAILS, command=self._view_completed_period_details)
            menu.add_command(label="Delete Period", command=self._delete_completed_period)
            menu.post(event.x_root, event.y_root)
    
    def _end_selected_period(self):
        """End the selected active period"""
        selection = self.active_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a period to end")
            return
        
        item = selection[0]
        period_id = self.active_tree.item(item, "tags")[0]
        period_name = self.active_tree.item(item, "values")[0]
        
        confirm = messagebox.askyesno(
            "Confirm End Period",
            f"End the period '{period_name}'?\n\nEnd date will be set to today."
        )
        
        if confirm:
            result = self.period_service.end_period(
                period_id, date.today().strftime('%Y-%m-%d')
            )
            
            if result["success"]:
                messagebox.showinfo("Success", result["message"])
                # Refresh the period lists to show period moved to completed
                self.refresh()
            else:
                messagebox.showerror("Error", result["message"])
    
    def _open_weight_logging(self, event=None):
        """Open weight logging dashboard (double-click handler)"""
        if not self.dashboard or not self.dashboard.app:
            messagebox.showinfo(
                "Info",
                "Weight logging can be accessed from the main menu (Button 5)"
            )
            return
        
        # Call the main app to open weight logging
        try:
            self.dashboard.app.button_pressed(5)  # Button 5 is weight logging
        except Exception as e:
            messagebox.showerror("Error", f"Could not open weight logging: {str(e)}")
    
    def _view_period_details(self):
        """View details of selected active period"""
        selection = self.active_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a period to view")
            return
        
        item = selection[0]
        period_id = self.active_tree.item(item, "tags")[0]
        self._show_period_details(period_id)
    
    def _view_completed_period_details(self):
        """View details of selected completed period"""
        selection = self.completed_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a period to view")
            return
        
        item = selection[0]
        period_id = self.completed_tree.item(item, "tags")[0]
        self._show_period_details(period_id)
    
    def _show_period_details(self, period_id):
        """Show detailed information about a period"""
        summary_result = self.period_service.get_period_summary(period_id)
        
        if not summary_result:
            messagebox.showerror("Error", "Could not load period details")
            return
        
        summary = summary_result
        
        # Create details window
        details_win = tk.Toplevel(self)
        details_win.title(f"Period Details - {summary['period_name']}")
        details_win.geometry("500x700")
        
        # Title
        tk.Label(
            details_win, text=summary["period_name"],
            font=("Arial", 14, "bold"), fg="#1565c0"
        ).pack(pady=10)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(details_win)
        notebook.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Tab 1: Overview
        overview_frame = tk.Frame(notebook)
        notebook.add(overview_frame, text="Overview")
        
        overview_text = tk.Text(overview_frame, wrap="word", font=("Arial", 12))
        overview_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Format details
        status_text = '✓ Completed' if not summary.get('is_active', True) else '📍 Active'
        if summary.get('is_ongoing'):
            status_text += ' (Ongoing)'
        
        details_content = f"""
Period Information:
━━━━━━━━━━━━━━━━━━━

Type: {summary.get('protocol_type', 'custom')}
Start Date: {summary['start_date']}
End Date: {summary.get('end_date', 'Ongoing')}
Status: {status_text}
Duration: {summary['duration_days']} days

Description:
{summary.get('description', 'No description provided')}

Effectiveness Results:
━━━━━━━━━━━━━━━━━━━━━━

"""
        
        weight_data = summary.get('weight_change')
        if weight_data:
            details_content += f"Start Weight: {weight_data['start_weight']:.1f} kg\n"
            details_content += f"End Weight: {weight_data['end_weight']:.1f} kg\n"
            details_content += f"Total Change: {weight_data['change']:+.1f} kg\n"
            details_content += f"Average Weekly: {weight_data['change_per_week']:+.2f} kg/week\n"
        else:
            details_content += "No weight data available for this period\n"
        
        if summary.get('notes'):
            details_content += f"\nNotes:\n{summary['notes']}\n"
        
        overview_text.insert("1.0", details_content)
        overview_text.config(state="disabled")
        
        # Tab 2: Weight Logs
        logs_frame = tk.Frame(notebook)
        notebook.add(logs_frame, text="Weight Logs")
        
        # Get weight logs for this period
        from services.weightlog_service import WeightLogService
        weight_service = WeightLogService(self.period_service.db_path)
        
        # Get all logs during period date range
        all_logs = weight_service.get_weight_history(self.user_id)
        
        # Filter logs within period date range
        period_logs = []
        for log in all_logs:
            log_date = log['date']
            if log_date >= summary['start_date']:
                if summary.get('end_date'):
                    if log_date <= summary['end_date']:
                        period_logs.append(log)
                else:
                    period_logs.append(log)
        
        # Display logs in treeview
        tk.Label(
            logs_frame, 
            text=f"Weight entries during this period ({len(period_logs)} total)",
            font=("Arial", 12, "bold")
        ).pack(pady=5)
        
        # Create treeview
        tree_frame = tk.Frame(logs_frame)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        columns = ("date", "weight", "notes")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        tree.heading("date", text="Date")
        tree.heading("weight", text="Weight (kg)")
        tree.heading("notes", text="Notes")
        
        tree.column("date", width=120)
        tree.column("weight", width=100)
        tree.column("notes", width=300)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Populate tree
        for log in period_logs:
            notes = log.get('notes', '') or ''
            tree.insert("", "end", values=(
                log['date'],
                f"{log['weight']:.1f}",
                notes
            ))
        
        if not period_logs:
            tk.Label(
                logs_frame,
                text="No weight logs found for this period",
                font=("Arial", 11, "italic"), fg="#999"
            ).pack(pady=10)
        
        # Close button
        tk.Button(
            details_win, text="Close", command=details_win.destroy,
            font=("Arial", 12), bg="#e3f2fd", width=15
        ).pack(pady=10)
    
    def _delete_completed_period(self):
        """Delete a completed period"""
        selection = self.completed_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        period_id = self.completed_tree.item(item, "tags")[0]
        period_name = self.completed_tree.item(item, "values")[0]
        
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Permanently delete the period '{period_name}'?\n\nThis cannot be undone."
        )
        
        if confirm:
            result = self.period_service.delete_period(self.user_id, period_id)
            
            if result["success"]:
                messagebox.showinfo("Success", result["message"])
                self.refresh()
            else:
                messagebox.showerror("Error", result["message"])


class DashboardPeriods(tk.Toplevel):
    """Main dietary period management dashboard"""
    
    def __init__(self, parent, period_service: 'DietaryPeriodService',
                 username: str, user_id: str, app=None):
        super().__init__(parent)
        self.title(f"Dietary Period Tracking - {username}")
        self.geometry("1050x700")
        
        self.period_service = period_service
        self.user_id = user_id
        self.username = username
        self.app = app  # Store reference to main app for opening weight logging
        
        # Main container with paned window
        paned = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashwidth=5)
        paned.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left side - Create period
        left_frame = tk.Frame(paned, relief="raised", borderwidth=2)
        paned.add(left_frame, width=500)
        
        self.create_frame = PeriodCreateFrame(left_frame, period_service, user_id, 
                                              dashboard=self)
        self.create_frame.pack(fill="both", expand=True)
        
        # Right side - Period list
        right_frame = tk.Frame(paned, relief="raised", borderwidth=2)
        paned.add(right_frame, width=500)
        
        self.list_frame = PeriodListFrame(right_frame, period_service, user_id, dashboard=self)
        self.list_frame.pack(fill="both", expand=True)
        
        # Bottom button frame
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)
        
        tk.Button(
            button_frame, text="Close", command=self.destroy,
            font=("Arial", 11), bg="#ffebee", width=15
        ).pack()
    
    def refresh_periods(self):
        """Refresh the period list"""
        self.list_frame.refresh()
