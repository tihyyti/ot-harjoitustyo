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
        
        tk.Label(self, text="Login", font=("Arial", 18)).grid(
            row=0, column=0, columnspan=2, pady=20)
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
    """User registration window"""
    
    def __init__(self, master, user_service: UserService):
        super().__init__(master)
        self.user_service = user_service
        self.title("Register")
        self._build()

    def _build(self):
        """Build the registration form"""
        tk.Label(self, text="Create new user", font=("Arial", 15)).grid(
            row=0, column=0, columnspan=2, pady=12)
        
        # Create form labels
        labels = [
            "Username", "Password", "Weight (kg)", "Length (cm)", "Age",
            "Activity Level", "Allergies", "Kcal Min", "Kcal Max", "Weight Loss Target"
        ]
        for i, label in enumerate(labels, start=1):
            tk.Label(self, text=label).grid(row=i, column=0, sticky="e", padx=5, pady=3)

        # Create form entry variables
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

        # Create form entries
        tk.Entry(self, textvariable=self.username_var).grid(row=1, column=1, padx=5, pady=3)
        tk.Entry(self, textvariable=self.password_var, show="*").grid(row=2, column=1, padx=5, pady=3)
        tk.Entry(self, textvariable=self.weight_var).grid(row=3, column=1, padx=5, pady=3)
        tk.Entry(self, textvariable=self.length_var).grid(row=4, column=1, padx=5, pady=3)
        tk.Entry(self, textvariable=self.age_var).grid(row=5, column=1, padx=5, pady=3)
        tk.Entry(self, textvariable=self.activity_level_var).grid(row=6, column=1, padx=5, pady=3)
        tk.Entry(self, textvariable=self.allergies_var).grid(row=7, column=1, padx=5, pady=3)
        tk.Entry(self, textvariable=self.kcal_min_var).grid(row=8, column=1, padx=5, pady=3)
        tk.Entry(self, textvariable=self.kcal_max_var).grid(row=9, column=1, padx=5, pady=3)
        tk.Entry(self, textvariable=self.weight_loss_target_var).grid(row=10, column=1, padx=5, pady=3)
        
        tk.Button(self, text="Create user", command=self._on_create).grid(
            row=11, column=0, columnspan=2, pady=12)

    def _on_create(self):
        """Handle user creation with validation"""
        username = self.username_var.get().strip()
        password = self.password_var.get()
        
        if not username or not password:
            messagebox.showwarning("Missing info", "Username and password are required.")
            return

        # Parse and validate numeric fields
        try:
            weight = float(self.weight_var.get().strip()) if self.weight_var.get().strip() else None
            length = float(self.length_var.get().strip()) if self.length_var.get().strip() else None
            age = int(self.age_var.get().strip()) if self.age_var.get().strip() else None
            activity_level = int(self.activity_level_var.get().strip()) if self.activity_level_var.get().strip() else None
            kcal_min = int(self.kcal_min_var.get().strip()) if self.kcal_min_var.get().strip() else None
            kcal_max = int(self.kcal_max_var.get().strip()) if self.kcal_max_var.get().strip() else None
            weight_loss_target = float(self.weight_loss_target_var.get().strip()) if self.weight_loss_target_var.get().strip() else None
        except ValueError as e:
            messagebox.showerror("Validation Error", f"Invalid numeric value: {e}")
            return

        allergies = self.allergies_var.get().strip() if self.allergies_var.get().strip() else None

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
            messagebox.showinfo("Done", f"User created: {user.username}")
            self.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
