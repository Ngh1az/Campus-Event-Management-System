"""
Student UI - Interface for students/visitors
"""

import tkinter as tk
from tkinter import messagebox, ttk
from services.event_service import EventService
from services.user_service import UserService


class StudentWindow:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.root.title(f"Student Dashboard - {user.username}")
        self.root.geometry("1000x650")

        self.event_service = EventService()
        self.user_service = UserService()

        # Header
        header_frame = tk.Frame(root, bg="#3498db", height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text=f"Welcome, {user.username}!",
            font=("Arial", 16, "bold"),
            bg="#3498db",
            fg="white",
        ).pack(side=tk.LEFT, padx=20, pady=15)

        tk.Button(
            header_frame,
            text="Logout",
            command=self.logout,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
        ).pack(side=tk.RIGHT, padx=20)

        # Main container
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Left panel - All Events
        left_frame = tk.LabelFrame(
            main_frame, text="Available Events", font=("Arial", 12, "bold")
        )
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Search bar
        search_frame = tk.Frame(left_frame)
        search_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(search_frame, text="Search:", font=("Arial", 10)).pack(
            side=tk.LEFT, padx=5
        )
        self.search_entry = tk.Entry(search_frame, font=("Arial", 10), width=25)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(
            search_frame,
            text="Search",
            command=self.search_events,
            bg="#3498db",
            fg="white",
        ).pack(side=tk.LEFT, padx=2)
        tk.Button(
            search_frame,
            text="Clear",
            command=self.load_all_events,
            bg="#95a5a6",
            fg="white",
        ).pack(side=tk.LEFT, padx=2)

        # All events treeview
        tree_frame = tk.Frame(left_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        scrollbar = tk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        columns = ("ID", "Name", "Date", "Location", "Available")
        self.all_events_tree = ttk.Treeview(
            tree_frame, columns=columns, show="headings", yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.all_events_tree.yview)

        self.all_events_tree.heading("ID", text="ID")
        self.all_events_tree.heading("Name", text="Event Name")
        self.all_events_tree.heading("Date", text="Date")
        self.all_events_tree.heading("Location", text="Location")
        self.all_events_tree.heading("Available", text="Available Slots")

        self.all_events_tree.column("ID", width=40, anchor="center")
        self.all_events_tree.column("Name", width=200)
        self.all_events_tree.column("Date", width=100, anchor="center")
        self.all_events_tree.column("Location", width=120)
        self.all_events_tree.column("Available", width=100, anchor="center")

        self.all_events_tree.pack(fill=tk.BOTH, expand=True)
        self.all_events_tree.bind("<Double-1>", self.view_event_details)

        # Action buttons
        btn_frame = tk.Frame(left_frame)
        btn_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        tk.Button(
            btn_frame,
            text="Register for Event",
            command=self.register_event,
            bg="#27ae60",
            fg="white",
            font=("Arial", 10, "bold"),
            width=20,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="View Details",
            command=self.view_event_details,
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            width=20,
        ).pack(side=tk.LEFT, padx=5)

        # Right panel - My Registrations
        right_frame = tk.LabelFrame(
            main_frame, text="My Registered Events", font=("Arial", 12, "bold")
        )
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # My events treeview
        my_tree_frame = tk.Frame(right_frame)
        my_tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        my_scrollbar = tk.Scrollbar(my_tree_frame)
        my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        my_columns = ("ID", "Name", "Date", "Location")
        self.my_events_tree = ttk.Treeview(
            my_tree_frame,
            columns=my_columns,
            show="headings",
            yscrollcommand=my_scrollbar.set,
        )
        my_scrollbar.config(command=self.my_events_tree.yview)

        self.my_events_tree.heading("ID", text="ID")
        self.my_events_tree.heading("Name", text="Event Name")
        self.my_events_tree.heading("Date", text="Date")
        self.my_events_tree.heading("Location", text="Location")

        self.my_events_tree.column("ID", width=40, anchor="center")
        self.my_events_tree.column("Name", width=150)
        self.my_events_tree.column("Date", width=90, anchor="center")
        self.my_events_tree.column("Location", width=100)

        self.my_events_tree.pack(fill=tk.BOTH, expand=True)

        # My events action buttons
        my_btn_frame = tk.Frame(right_frame)
        my_btn_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        tk.Button(
            my_btn_frame,
            text="Unregister",
            command=self.unregister_event,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            width=18,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            my_btn_frame,
            text="Refresh",
            command=self.load_my_events,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 10, "bold"),
            width=18,
        ).pack(side=tk.LEFT, padx=5)

        # Load data
        self.load_all_events()
        self.load_my_events()

    def load_all_events(self):
        """Load and display all available events"""
        for i in self.all_events_tree.get_children():
            self.all_events_tree.delete(i)

        events = self.event_service.get_all_events()
        for event in events:
            # Only show events with available slots
            if event.available_slots() > 0:
                self.all_events_tree.insert(
                    "",
                    "end",
                    values=(
                        event.id,
                        event.name,
                        event.date,
                        event.location or "-",
                        f"{event.available_slots()} / {event.capacity}",
                    ),
                )

    def search_events(self):
        """Search events by keyword"""
        keyword = self.search_entry.get().strip()
        if not keyword:
            self.load_all_events()
            return

        for i in self.all_events_tree.get_children():
            self.all_events_tree.delete(i)

        events = self.event_service.search_events(keyword=keyword)
        for event in events:
            if event.available_slots() > 0:
                self.all_events_tree.insert(
                    "",
                    "end",
                    values=(
                        event.id,
                        event.name,
                        event.date,
                        event.location or "-",
                        f"{event.available_slots()} / {event.capacity}",
                    ),
                )

    def load_my_events(self):
        """Load and display user's registered events"""
        for i in self.my_events_tree.get_children():
            self.my_events_tree.delete(i)

        events = self.event_service.get_user_registered_events(self.user.username)
        for event in events:
            self.my_events_tree.insert(
                "",
                "end",
                values=(event.id, event.name, event.date, event.location or "-"),
            )

    def register_event(self):
        """Register for selected event"""
        selected = self.all_events_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an event to register.")
            return

        item = self.all_events_tree.item(selected[0])
        event_id = item["values"][0]
        event_name = item["values"][1]

        if messagebox.askyesno(
            "Confirm Registration", f"Do you want to register for '{event_name}'?"
        ):
            try:
                self.event_service.register_attendee(event_id, self.user.username)
                self.user_service.register_event(self.user.username, event_id)
                messagebox.showinfo(
                    "Success", f"Successfully registered for '{event_name}'!"
                )
                self.load_all_events()
                self.load_my_events()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def unregister_event(self):
        """Unregister from selected event"""
        selected = self.my_events_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an event to unregister.")
            return

        item = self.my_events_tree.item(selected[0])
        event_id = item["values"][0]
        event_name = item["values"][1]

        if messagebox.askyesno(
            "Confirm Unregistration", f"Do you want to unregister from '{event_name}'?"
        ):
            try:
                self.event_service.unregister_attendee(event_id, self.user.username)
                self.user_service.unregister_event(self.user.username, event_id)
                messagebox.showinfo(
                    "Success", f"Successfully unregistered from '{event_name}'!"
                )
                self.load_all_events()
                self.load_my_events()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def view_event_details(self, event=None):
        """View detailed information about an event"""
        selected = self.all_events_tree.selection()
        if not selected:
            return

        item = self.all_events_tree.item(selected[0])
        event_id = item["values"][0]
        event = self.event_service.get_event_by_id(event_id)

        if not event:
            messagebox.showerror("Error", "Event not found!")
            return

        # Create details window
        details_win = tk.Toplevel(self.root)
        details_win.title(f"Event Details - {event.name}")
        details_win.geometry("500x500")
        details_win.transient(self.root)
        details_win.resizable(False, False)

        # Header
        header = tk.Frame(details_win, bg="#3498db", height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(
            header,
            text=event.name,
            font=("Arial", 14, "bold"),
            bg="#3498db",
            fg="white",
        ).pack(pady=10)

        # Content
        content_frame = tk.Frame(details_win)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        info_items = [
            ("📅 Date:", event.date),
            ("📍 Location:", event.location or "Not specified"),
            ("👥 Capacity:", f"{event.capacity} people"),
            ("✅ Registered:", f"{len(event.attendees)} people"),
            ("🎯 Available:", f"{event.available_slots()} slots"),
            ("👤 Organizer:", event.organizer or "N/A"),
        ]

        for label, value in info_items:
            frame = tk.Frame(content_frame)
            frame.pack(fill=tk.X, pady=5)
            tk.Label(
                frame, text=label, font=("Arial", 10, "bold"), width=15, anchor="w"
            ).pack(side=tk.LEFT)
            tk.Label(frame, text=value, font=("Arial", 10), anchor="w").pack(
                side=tk.LEFT
            )

        # Description
        tk.Label(
            content_frame,
            text="📝 Description:",
            font=("Arial", 10, "bold"),
            anchor="w",
        ).pack(fill=tk.X, pady=(15, 5))

        desc_frame = tk.Frame(content_frame, relief=tk.SUNKEN, borderwidth=1)
        desc_frame.pack(fill=tk.BOTH, expand=True)

        desc_text = tk.Text(
            desc_frame, font=("Arial", 9), wrap=tk.WORD, height=8, bg="#f8f9fa"
        )
        desc_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        desc_text.insert("1.0", event.description or "No description provided")
        desc_text.config(state=tk.DISABLED)

        # Action buttons
        btn_frame = tk.Frame(details_win)
        btn_frame.pack(pady=15)

        if self.user.username not in event.attendees and not event.is_full():
            tk.Button(
                btn_frame,
                text="Register Now",
                command=lambda: self.quick_register(event_id, event.name, details_win),
                bg="#27ae60",
                fg="white",
                font=("Arial", 10, "bold"),
                width=15,
            ).pack(side=tk.LEFT, padx=5)
        elif self.user.username in event.attendees:
            tk.Label(
                btn_frame,
                text="✓ You are registered for this event",
                font=("Arial", 10, "bold"),
                fg="#27ae60",
            ).pack(side=tk.LEFT, padx=5)
        else:
            tk.Label(
                btn_frame,
                text="⚠ Event is full",
                font=("Arial", 10, "bold"),
                fg="#e74c3c",
            ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="Close",
            command=details_win.destroy,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 10, "bold"),
            width=15,
        ).pack(side=tk.LEFT, padx=5)

    def quick_register(self, event_id, event_name, window):
        """Quick register from details window"""
        try:
            self.event_service.register_attendee(event_id, self.user.username)
            self.user_service.register_event(self.user.username, event_id)
            messagebox.showinfo(
                "Success", f"Successfully registered for '{event_name}'!"
            )
            window.destroy()
            self.load_all_events()
            self.load_my_events()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def logout(self):
        """Logout and return to login screen"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()
            root = tk.Tk()
            from ui.login_ui import LoginWindow

            LoginWindow(root)
            root.mainloop()
