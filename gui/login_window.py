import customtkinter as ctk
from tkinter import messagebox
from database.services import DatabaseService

class LoginWindow:
    def __init__(self):
        self.db_service = DatabaseService()
        self.setup_window()
        self.create_widgets()
        
    def setup_window(self):
        # Set appearance
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("Employee Management System - Login")
        self.root.geometry("500x650")
        self.root.resizable(False, False)
        
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.root.winfo_screenheight() // 2) - (650 // 2)
        self.root.geometry(f"500x650+{x}+{y}")
    
    def create_widgets(self):
        # Main container
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=40, pady=30)
        
        # Logo and title section
        ctk.CTkLabel(
            main_frame,
            text="👤",
            font=ctk.CTkFont(size=70)
        ).pack(pady=(20, 10))
        
        ctk.CTkLabel(
            main_frame,
            text="Employee Management System",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=(0, 5))
        
        ctk.CTkLabel(
            main_frame,
            text="Please login to continue",
            font=ctk.CTkFont(size=13),
            text_color="gray"
        ).pack(pady=(0, 30))
        
        # Login form
        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(fill="x", pady=20)
        
        # Username
        ctk.CTkLabel(
            form_frame,
            text="Username",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        ).pack(fill="x", padx=25, pady=(20, 5))
        
        self.username_entry = ctk.CTkEntry(
            form_frame,
            height=45,
            placeholder_text="Enter your username",
            font=ctk.CTkFont(size=13)
        )
        self.username_entry.pack(fill="x", padx=25, pady=(0, 15))
        
        # Password
        ctk.CTkLabel(
            form_frame,
            text="Password",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        ).pack(fill="x", padx=25, pady=(5, 5))
        
        self.password_entry = ctk.CTkEntry(
            form_frame,
            height=45,
            placeholder_text="Enter your password",
            show="*",
            font=ctk.CTkFont(size=13)
        )
        self.password_entry.pack(fill="x", padx=25, pady=(0, 20))
        
        # Login button - bright and visible
        login_btn = ctk.CTkButton(
            form_frame,
            text="LOGIN",
            command=self.login,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            corner_radius=8
        )
        login_btn.pack(fill="x", padx=25, pady=(10, 20))
        
        # Bind Enter key
        self.root.bind('<Return>', lambda event: self.login())
        
        # Focus on username
        self.username_entry.focus()
    
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        user = self.db_service.authenticate_user(username, password)
        
        if user:
            self.root.destroy()
            # Import here to avoid circular imports
            from gui.main_window import MainWindow
            app = MainWindow(user)
            app.run()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password. Please try again.")
            self.password_entry.delete(0, 'end')
    
    def run(self):
        self.root.mainloop()