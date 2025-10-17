import tkinter as tk
from tkinter import messagebox
from services.user_service import UserService


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Campus Event Management - Login")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.root.winfo_screenheight() // 2) - (300 // 2)
        self.root.geometry(f"400x300+{x}+{y}")

        self.user_service = UserService()

        # Header
        header = tk.Label(
            root,
            text="Campus Event Management System",
            font=("Arial", 14, "bold"),
            fg="#2c3e50",
        )
        header.pack(pady=20)

        # Form frame
        form_frame = tk.Frame(root)
        form_frame.pack(pady=30)

        tk.Label(form_frame, text="Username:", font=("Arial", 10)).grid(
            row=0, column=0, sticky="e", padx=10, pady=12
        )
        self.username_entry = tk.Entry(form_frame, width=25, font=("Arial", 10))
        self.username_entry.grid(row=0, column=1, pady=12)
        self.username_entry.focus()

        tk.Label(form_frame, text="Password:", font=("Arial", 10)).grid(
            row=1, column=0, sticky="e", padx=10, pady=12
        )
        self.password_entry = tk.Entry(
            form_frame, show="●", width=25, font=("Arial", 10)
        )
        self.password_entry.grid(row=1, column=1, pady=12)

        # Login button
        login_btn = tk.Button(
            root,
            text="Login",
            command=self.login,
            bg="#3498db",
            fg="white",
            font=("Arial", 11, "bold"),
            width=20,
            height=1,
            cursor="hand2",
        )
        login_btn.pack(pady=15)

        # Bind Enter key
        self.root.bind("<Return>", lambda e: self.login())

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning(
                "Input Error", "Please enter both username and password!"
            )
            return

        # Authenticate without role - let the system determine the role
        user = self.user_service.authenticate_without_role(username, password)

        if user:
            messagebox.showinfo(
                "Success", f"Welcome {username}!\nLogged in as: {user.role}"
            )
            self.open_dashboard(user)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password!")

    def open_dashboard(self, user):
        """Open the appropriate dashboard based on user role"""
        self.root.destroy()

        new_root = tk.Tk()

        if user.role == "Admin":
            from ui.admin_ui import AdminWindow

            AdminWindow(new_root, user)
        elif user.role == "Organizer":
            from ui.organizer_ui import OrganizerWindow

            OrganizerWindow(new_root, user)
        else:  # Student or Visitor
            from ui.student_ui import StudentWindow

            StudentWindow(new_root, user)

        new_root.mainloop()
