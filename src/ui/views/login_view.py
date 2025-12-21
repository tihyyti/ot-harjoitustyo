"""
Login View - User and Admin Authentication
Handles user registration, user login, and admin login
"""

import tkinter as tk
from tkinter import messagebox
from services import UserService, AdminService


class LoginFrame(tk.Frame):
    """Main login frame with user/admin authentication"""
    
    def __init__(self, master, user_service: UserService, admin_service: AdminService, 
                 on_user_login, on_admin_login):
        super().__init__(master)
        self.user_service = user_service
        self.admin_service = admin_service
        self.on_user_login = on_user_login
        self.on_admin_login = on_admin_login
        self._build()

    def _build(self):
        """Build the login UI"""
        # Center the frame content
        self.pack(expand=True)
        
        # Header frame with consistent styling
        header_frame = tk.Frame(self, bg="#e8f4f8", relief="ridge", borderwidth=2)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        tk.Label(header_frame, text="Laihdutanyt Login", 
                font=("Arial", 16, "bold"), bg="#e8f4f8").pack(pady=10)
        
        tk.Label(self, text="Username", font=("Arial", 12)).grid(
            row=1, column=0, sticky="e", padx=10, pady=8)
        tk.Label(self, text="Password", font=("Arial", 12)).grid(
            row=2, column=0, sticky="e", padx=10, pady=8)

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        tk.Entry(self, textvariable=self.username_var, font=("Arial", 12), width=20).grid(
            row=1, column=1, padx=10, pady=8, sticky="w")
        tk.Entry(self, textvariable=self.password_var, show="*", font=("Arial", 12), width=20).grid(
            row=2, column=1, padx=10, pady=8, sticky="w")

        button_frame = tk.Frame(self)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(button_frame, text="User Login", command=self._on_user_login, 
                  font=("Arial", 12), width=11, bg="#90caf9").pack(side="left", padx=5)
        tk.Button(button_frame, text="Admin Login", command=self._on_admin_login, 
                  font=("Arial", 12), width=11, bg="#ffcc80").pack(side="left", padx=5)
        
        tk.Button(self, text="Register New User", command=self._on_open_register, 
                  font=("Arial", 11), width=20).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Application description panel
        desc_frame = tk.Frame(self, relief="solid", borderwidth=1, bg="#fffef0")
        desc_frame.grid(row=5, column=0, columnspan=2, padx=15, pady=15, sticky="ew")
        
        tk.Label(
            desc_frame, 
            text="📊 Laihdutanyt - Comprehensive Weight Loss Tracker",
            font=("Arial", 11, "bold"), bg="#fffef0", fg="#1565c0"
        ).pack(pady=(8, 3))
        
        desc_text = (
            "Track your weight, food intake, and physical activities.\n"
            "Monitor dietary periods and analyze their effectiveness.\n\n"
            "✓ Food & Activity Logging\n"
            "✓ Weight Tracking with Period Annotations\n"
            "✓ Daily Totals & Analytics\n"
            "✓ 8 Dietary Protocol Templates\n\n"
            "⚠ Demo Version: Admin features are placeholder stubs"
        )
        
        tk.Label(
            desc_frame,
            text=desc_text,
            font=("Arial", 9), bg="#fffef0", fg="#333",
            justify="left", anchor="w"
        ).pack(padx=10, pady=(0, 8))

    def _on_user_login(self):
        """Handle user login"""
        username = self.username_var.get().strip()
        password = self.password_var.get()
        
        if not username or not password:
            messagebox.showwarning("Missing info", "Please fill username and password.")
            return
        
        if self.user_service.authenticate_user(username, password):
            messagebox.showinfo("Success", f"Logged in: {username}")
            self.on_user_login(username)
        else:
            messagebox.showerror("Error", "User login failed. Check credentials.")

    def _on_admin_login(self):
        """Handle admin login"""
        username = self.username_var.get().strip()
        password = self.password_var.get()
        
        if not username or not password:
            messagebox.showwarning("Missing info", "Please fill username and password.")
            return
        
        if self.admin_service.authenticate_admin(username, password):
            messagebox.showinfo("Success", f"Admin logged in: {username}")
            self.on_admin_login(username)
        else:
            messagebox.showerror("Error", "Admin login failed. Check credentials.")

    def _on_open_register(self):
        """Open registration window"""
        RegisterWindow(self.master, self.user_service)


class RegisterWindow(tk.Toplevel):
    """User registration window with validation and placeholders"""
    
    def __init__(self, master, user_service: UserService):
        super().__init__(master)
        self.user_service = user_service
        self.title("Register New User")
        self.geometry("400x550")
        self._build()

    def _create_entry_with_placeholder(self, parent, row, textvariable, placeholder, show=None):
        """Create an entry with placeholder text"""
        entry = tk.Entry(parent, textvariable=textvariable, width=25, font=("Arial", 11))
        if show:
            entry.config(show=show)
        entry.grid(row=row, column=1, padx=5, pady=5, sticky="w")
        
        # Add placeholder functionality
        def on_focus_in(event):
            if textvariable.get() == placeholder:
                textvariable.set("")
                entry.config(fg='black')
        
        def on_focus_out(event):
            if textvariable.get() == "":
                textvariable.set(placeholder)
                entry.config(fg='gray')
        
        # Set initial placeholder
        if not textvariable.get():
            textvariable.set(placeholder)
            entry.config(fg='gray')
        
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        
        return entry

    def _build(self):
        """Build the registration form with placeholders and validation"""
        # Title
        title_frame = tk.Frame(self, bg="#e8f4f8", relief="ridge", borderwidth=2)
        title_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        tk.Label(title_frame, text="Create New User Account", 
                font=("Arial", 16, "bold"), bg="#e8f4f8").pack(pady=10)
        
        # Instructions
        info_label = tk.Label(self, text="* Required fields", font=("Arial", 10, "italic"), fg="red")
        info_label.grid(row=1, column=0, columnspan=2, pady=5)
        
        # Admin note
        admin_note = tk.Label(
            self, 
            text="ℹ️ Note: This creates a regular user account.\nAdmin accounts are managed separately in the database.",
            font=("Arial", 9, "italic"), fg="#1565c0", justify="center"
        )
        admin_note.grid(row=1, column=0, columnspan=2, pady=(25, 5), sticky="n")
        
        # Create form variables
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

        # Form fields with labels and placeholders
        row = 2
        
        # Username *
        tk.Label(self, text="Username *", font=("Arial", 11)).grid(row=row, column=0, sticky="e", padx=5, pady=5)
        self._create_entry_with_placeholder(self, row, self.username_var, "e.g., john_doe")
        row += 1
        
        # Password *
        tk.Label(self, text="Password *", font=("Arial", 11)).grid(row=row, column=0, sticky="e", padx=5, pady=5)
        self._create_entry_with_placeholder(self, row, self.password_var, "Min 4 characters", show="*")
        row += 1
        
        # Weight
        tk.Label(self, text="Weight (kg)", font=("Arial", 11)).grid(row=row, column=0, sticky="e", padx=5, pady=5)
        self._create_entry_with_placeholder(self, row, self.weight_var, "e.g., 70.5")
        row += 1
        
        # Length
        tk.Label(self, text="Height (cm)", font=("Arial", 11)).grid(row=row, column=0, sticky="e", padx=5, pady=5)
        self._create_entry_with_placeholder(self, row, self.length_var, "e.g., 175")
        row += 1
        
        # Age
        tk.Label(self, text="Age", font=("Arial", 11)).grid(row=row, column=0, sticky="e", padx=5, pady=5)
        self._create_entry_with_placeholder(self, row, self.age_var, "e.g., 30")
        row += 1
        
        # Activity Level
        tk.Label(self, text="Activity Level", font=("Arial", 11)).grid(row=row, column=0, sticky="e", padx=5, pady=5)
        self._create_entry_with_placeholder(self, row, self.activity_level_var, "1-5 (1=low, 5=high)")
        row += 1
        
        # Allergies
        tk.Label(self, text="Allergies", font=("Arial", 11)).grid(row=row, column=0, sticky="e", padx=5, pady=5)
        self._create_entry_with_placeholder(self, row, self.allergies_var, "e.g., nuts, dairy")
        row += 1
        
        # Kcal Min
        tk.Label(self, text="Daily Kcal Min", font=("Arial", 11)).grid(row=row, column=0, sticky="e", padx=5, pady=5)
        self._create_entry_with_placeholder(self, row, self.kcal_min_var, "e.g., 1500")
        row += 1
        
        # Kcal Max
        tk.Label(self, text="Daily Kcal Max", font=("Arial", 11)).grid(row=row, column=0, sticky="e", padx=5, pady=5)
        self._create_entry_with_placeholder(self, row, self.kcal_max_var, "e.g., 2000")
        row += 1
        
        # Weight Loss Target
        tk.Label(self, text="Target Weight (kg)", font=("Arial", 11)).grid(row=row, column=0, sticky="e", padx=5, pady=5)
        self._create_entry_with_placeholder(self, row, self.weight_loss_target_var, "e.g., 65.0")
        row += 1
        
        # Buttons
        button_frame = tk.Frame(self)
        button_frame.grid(row=row, column=0, columnspan=2, pady=20)
        
        tk.Button(button_frame, text="Create User", command=self._on_create, 
                 font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", width=15).pack(side="left", padx=5)
        tk.Button(button_frame, text="Cancel", command=self.destroy, 
                 font=("Arial", 12), bg="#d0d0d0", width=15).pack(side="left", padx=5)

    def _get_value_or_none(self, var, placeholder):
        """Get value from StringVar, ignoring placeholder text"""
        value = var.get().strip()
        if value == placeholder or value == "":
            return None
        return value

    def _on_create(self):
        """Handle user creation with comprehensive validation"""
        # Get username and password (ignore placeholders)
        username = self._get_value_or_none(self.username_var, "e.g., john_doe")
        password_raw = self.password_var.get()
        password = None if password_raw == "Min 4 characters" or not password_raw else password_raw
        
        # Validate required fields
        if not username:
            messagebox.showwarning("Missing Info", "Username is required.")
            return
        
        if not password or len(password) < 4:
            messagebox.showwarning("Missing Info", "Password is required (minimum 4 characters).")
            return

        # Parse and validate numeric fields
        try:
            # Weight validation
            weight_str = self._get_value_or_none(self.weight_var, "e.g., 70.5")
            if weight_str:
                weight = float(weight_str)
                if weight <= 0:
                    messagebox.showerror("Validation Error", "Weight must be a positive number.")
                    return
                if weight > 500:
                    messagebox.showerror("Validation Error", "Weight seems unrealistic (max 500 kg).")
                    return
            else:
                weight = None
            
            # Length/Height validation
            length_str = self._get_value_or_none(self.length_var, "e.g., 175")
            if length_str:
                length = float(length_str)
                if length <= 0:
                    messagebox.showerror("Validation Error", "Height must be a positive number.")
                    return
                if length < 50 or length > 300:
                    messagebox.showerror("Validation Error", "Height must be between 50-300 cm.")
                    return
            else:
                length = None
            
            # Age validation
            age_str = self._get_value_or_none(self.age_var, "e.g., 30")
            if age_str:
                age = int(age_str)
                if age <= 0:
                    messagebox.showerror("Validation Error", "Age must be a positive number.")
                    return
                if age < 10 or age > 120:
                    messagebox.showerror("Validation Error", "Age must be between 10-120 years.")
                    return
            else:
                age = None
            
            # Activity level validation
            activity_str = self._get_value_or_none(self.activity_level_var, "1-5 (1=low, 5=high)")
            if activity_str:
                activity_level = int(activity_str)
                if activity_level < 1 or activity_level > 5:
                    messagebox.showerror("Validation Error", "Activity level must be between 1 and 5.")
                    return
            else:
                activity_level = None
            
            # Kcal Min validation
            kcal_min_str = self._get_value_or_none(self.kcal_min_var, "e.g., 1500")
            if kcal_min_str:
                kcal_min = int(kcal_min_str)
                if kcal_min <= 0:
                    messagebox.showerror("Validation Error", "Daily Kcal Min must be positive.")
                    return
                if kcal_min < 500 or kcal_min > 10000:
                    messagebox.showerror("Validation Error", "Daily Kcal Min should be between 500-10000.")
                    return
            else:
                kcal_min = None
            
            # Kcal Max validation
            kcal_max_str = self._get_value_or_none(self.kcal_max_var, "e.g., 2000")
            if kcal_max_str:
                kcal_max = int(kcal_max_str)
                if kcal_max <= 0:
                    messagebox.showerror("Validation Error", "Daily Kcal Max must be positive.")
                    return
                if kcal_max < 500 or kcal_max > 10000:
                    messagebox.showerror("Validation Error", "Daily Kcal Max should be between 500-10000.")
                    return
            else:
                kcal_max = None
            
            # Validate kcal_min < kcal_max
            if kcal_min and kcal_max and kcal_min >= kcal_max:
                messagebox.showerror("Validation Error", "Daily Kcal Min must be less than Daily Kcal Max.")
                return
            
            # Weight loss target validation
            target_str = self._get_value_or_none(self.weight_loss_target_var, "e.g., 65.0")
            if target_str:
                weight_loss_target = float(target_str)
                if weight_loss_target <= 0:
                    messagebox.showerror("Validation Error", "Target weight must be a positive number.")
                    return
                if weight_loss_target > 500:
                    messagebox.showerror("Validation Error", "Target weight seems unrealistic (max 500 kg).")
                    return
            else:
                weight_loss_target = None
                
        except ValueError as e:
            messagebox.showerror("Validation Error", 
                               "Please enter valid numbers in all numeric fields.\n\n" +
                               "Weight, Height, Target: decimal numbers\n" +
                               "Age, Activity Level, Kcal: whole numbers")
            return

        # Get allergies
        allergies = self._get_value_or_none(self.allergies_var, "e.g., nuts, dairy")

        # Use service layer to register user
        try:
            user = self.user_service.register_user(
                username=username,
                password=password,
                weight=weight,
                length=length,
                age=age,
                activity_level=activity_level,
                allergies=allergies,
                kcal_min=kcal_min,
                kcal_max=kcal_max,
                weight_loss_target=weight_loss_target
            )
            messagebox.showinfo("Success!", f"User '{user.username}' has been created successfully!\n\nYou can now log in.")
            self.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
