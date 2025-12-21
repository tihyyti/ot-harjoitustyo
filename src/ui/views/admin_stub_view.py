"""
Admin View Stub - Placeholder for Future Admin Features
This is a demonstration stub showing planned admin functionality
"""

import tkinter as tk
from tkinter import messagebox, ttk


class AdminStubWindow(tk.Toplevel):
    """Admin interface stub showing planned features"""
    
    def __init__(self, parent, admin_username: str):
        super().__init__(parent)
        self.admin_username = admin_username
        self.title(f"Admin Panel - {admin_username} (Demo Stub)")
        
        # Calculate 80% of screen height
        screen_height = self.winfo_screenheight()
        window_height = int(screen_height * 0.8)
        self.geometry(f"900x{window_height}")
        
        self._build()
    
    def _build(self):
        """Build the admin stub UI"""
        # Header
        header_frame = tk.Frame(self, bg="#ffebee", relief="ridge", borderwidth=2)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(
            header_frame,
            text="⚠ Admin Panel - Demonstration Stub",
            font=("Arial", 16, "bold"), bg="#ffebee", fg="#c62828"
        ).pack(pady=10)
        
        tk.Label(
            header_frame,
            text=f"Logged in as: {self.admin_username}",
            font=("Arial", 11), bg="#ffebee", fg="#333"
        ).pack(pady=(0, 10))
        
        # Info panel
        info_frame = tk.Frame(self, relief="solid", borderwidth=1, bg="#fff8e1")
        info_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        tk.Label(
            info_frame,
            text="📋 This is a Demonstration Stub",
            font=("Arial", 13, "bold"), bg="#fff8e1", fg="#f57c00"
        ).pack(pady=15)
        
        info_text = (
            "This admin panel is a placeholder showing planned functionality.\n"
            "The following features are designed but not yet implemented:\n\n"
            "🔹 User Management\n"
            "   • View all registered users\n"
            "   • Reset user passwords\n"
            "   • Delete inactive accounts\n"
            "   • View user statistics\n\n"
            "🔹 System Configuration\n"
            "   • Configure dietary protocol templates\n"
            "   • Set global calorie ranges\n"
            "   • Manage food and activity databases\n"
            "   • Export system reports\n\n"
            "🔹 Coaching Features\n"
            "   • View client progress dashboards\n"
            "   • Send messages to users\n"
            "   • Create custom meal plans\n"
            "   • Schedule check-ins\n\n"
            "🔹 Analytics\n"
            "   • System-wide statistics\n"
            "   • Popular foods and activities\n"
            "   • Success rate metrics\n"
            "   • Data export for analysis\n\n"
            "💡 Note: In self-service mode, regular users can manage their own accounts."
        )
        
        tk.Label(
            info_frame,
            text=info_text,
            font=("Arial", 10), bg="#fff8e1", fg="#333",
            justify="left", anchor="w"
        ).pack(padx=20, pady=10)
        
        # Planned features list
        features_frame = tk.LabelFrame(self, text="Planned Admin Features", font=("Arial", 12, "bold"))
        features_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Treeview for features (height will expand to fill available space)
        columns = ("feature", "status", "priority")
        tree = ttk.Treeview(features_frame, columns=columns, show="headings", height=12)
        
        tree.heading("feature", text="Feature")
        tree.heading("status", text="Status")
        tree.heading("priority", text="Priority")
        
        tree.column("feature", width=400)
        tree.column("status", width=150)
        tree.column("priority", width=100)
        
        # Add sample features
        features = [
            ("User Management Dashboard", "Planned", "High"),
            ("Password Reset Tool", "Planned", "High"),
            ("Food Database Editor", "Planned", "Medium"),
            ("Activity Database Editor", "Planned", "Medium"),
            ("Client Progress Viewer", "Planned", "High"),
            ("System Reports Export", "Planned", "Low"),
            ("Custom Protocol Templates", "Planned", "Medium"),
            ("Bulk User Import", "Planned", "Low"),
        ]
        
        for feature, status, priority in features:
            tree.insert("", "end", values=(feature, status, priority))
        
        scrollbar = ttk.Scrollbar(features_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y", pady=5)
        
        # Button frame
        button_frame = tk.Frame(self)
        button_frame.pack(pady=15)
        
        tk.Button(
            button_frame,
            text="📖 View Documentation",
            command=self._show_documentation,
            font=("Arial", 11), bg="#2196f3", fg="white", width=20
        ).pack(side="left", padx=5)
        
        tk.Button(
            button_frame,
            text="Close Window",
            command=self.destroy,
            font=("Arial", 11), bg="#d0d0d0", width=15
        ).pack(side="left", padx=5)
    
    def _show_documentation(self):
        """Show documentation about admin features"""
        doc_text = (
            "ADMIN FEATURE ROADMAP\n"
            "==================================================\n\n"
            "Phase 1 - User Management (High Priority)\n"
            "• List all users with registration dates\n"
            "• View individual user statistics\n"
            "• Password reset capability\n"
            "• Account deletion with data cleanup\n\n"
            "Phase 2 - Database Management (Medium Priority)\n"
            "• Food database CRUD operations\n"
            "• Activity database CRUD operations\n"
            "• Bulk import from CSV\n"
            "• Data validation tools\n\n"
            "Phase 3 - Coaching Tools (High Priority)\n"
            "• Client progress dashboard\n"
            "• Weight trend visualization\n"
            "• Dietary period effectiveness reports\n"
            "• Custom recommendations engine\n\n"
            "Phase 4 - Analytics (Low Priority)\n"
            "• System-wide statistics\n"
            "• Popular foods/activities reports\n"
            "• Success rate calculations\n"
            "• Data export for external analysis\n\n"
            "CURRENT VERSION:\n"
            "The application operates in self-service mode where\n"
            "users manage their own data independently. This is\n"
            "suitable for personal use or small groups.\n\n"
            "FUTURE VERSIONS:\n"
            "Admin features will enable professional coaches and\n"
            "nutritionists to manage multiple clients efficiently."
        )
        
        # Create documentation window
        doc_win = tk.Toplevel(self)
        doc_win.title("Admin Feature Documentation")
        doc_win.geometry("700x600")
        
        text_widget = tk.Text(doc_win, wrap="word", font=("Courier", 10))
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        
        text_widget.insert("1.0", doc_text)
        text_widget.config(state="disabled")
        
        tk.Button(
            doc_win, text="Close", command=doc_win.destroy,
            font=("Arial", 11), bg="#d0d0d0", width=15
        ).pack(pady=10)
