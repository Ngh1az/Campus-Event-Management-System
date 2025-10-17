"""
Organizer UI - Interface for event organizers
"""

import tkinter as tk
from tkinter import messagebox, ttk
from services.event_service import EventService
from services.user_service import UserService


class OrganizerWindow:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.root.title(f"Organizer Dashboard - {user.username}")
        self.root.geometry("900x600")

        self.event_service = EventService()
        self.user_service = UserService()

        # Header
        header_frame = tk.Frame(root, bg="#16a085", height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text=f"Organizer Dashboard - {user.username}",
            font=("Arial", 16, "bold"),
            bg="#16a085",
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

        # Events list
        events_frame = tk.LabelFrame(
            main_frame, text="My Events", font=("Arial", 12, "bold")
        )
        events_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview
        tree_frame = tk.Frame(events_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        columns = (
            "ID",
            "Name",
            "Date",
            "Location",
            "Capacity",
            "Registered",
            "Available",
        )
        self.tree = ttk.Treeview(
            tree_frame, columns=columns, show="headings", yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree.yview)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Event Name")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Location", text="Location")
        self.tree.heading("Capacity", text="Capacity")
        self.tree.heading("Registered", text="Registered")
        self.tree.heading("Available", text="Available")

        self.tree.column("ID", width=40, anchor="center")
        self.tree.column("Name", width=200)
        self.tree.column("Date", width=100, anchor="center")
        self.tree.column("Location", width=120)
        self.tree.column("Capacity", width=80, anchor="center")
        self.tree.column("Registered", width=80, anchor="center")
        self.tree.column("Available", width=80, anchor="center")

        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<Double-1>", self.view_event_details)

        # Action buttons
        btn_frame = tk.Frame(events_frame)
        btn_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        tk.Button(
            btn_frame,
            text="View Attendees",
            command=self.view_attendees,
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            width=18,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="Manage Registrations",
            command=self.manage_registrations,
            bg="#9b59b6",
            fg="white",
            font=("Arial", 10, "bold"),
            width=18,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="Refresh",
            command=self.populate_table,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 10, "bold"),
            width=18,
        ).pack(side=tk.LEFT, padx=5)

        # Load data
        self.populate_table()

    def populate_table(self):
        """Load and display organizer's events"""
        for i in self.tree.get_children():
            self.tree.delete(i)

        events = self.event_service.get_events_by_organizer(self.user.username)
        for event in events:
            self.tree.insert(
                "",
                "end",
                values=(
                    event.id,
                    event.name,
                    event.date,
                    event.location or "-",
                    event.capacity,
                    len(event.attendees),
                    event.available_slots(),
                ),
            )

        if not events:
            messagebox.showinfo(
                "Info",
                "You have no events yet. Contact admin to create events for you.",
            )

    def view_event_details(self, event=None):
        """View detailed information about an event"""
        selected = self.tree.selection()
        if not selected:
            return

        item = self.tree.item(selected[0])
        event_id = item["values"][0]
        event = self.event_service.get_event_by_id(event_id)

        if not event:
            messagebox.showerror("Error", "Event not found!")
            return

        details = f"""
Event Details:
─────────────────────────
Name: {event.name}
Date: {event.date}
Location: {event.location or 'Not specified'}
Capacity: {event.capacity}
Registered: {len(event.attendees)}
Available: {event.available_slots()}

Description:
{event.description or 'No description provided'}

Attendees ({len(event.attendees)}):
{', '.join(event.attendees) if event.attendees else 'No attendees yet'}
"""
        messagebox.showinfo("Event Details", details)

    def view_attendees(self):
        """View attendees for selected event"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an event.")
            return

        item = self.tree.item(selected[0])
        event_id = item["values"][0]
        event = self.event_service.get_event_by_id(event_id)

        if not event:
            messagebox.showerror("Error", "Event not found!")
            return

        # Create attendees window
        attendees_win = tk.Toplevel(self.root)
        attendees_win.title(f"Attendees - {event.name}")
        attendees_win.geometry("500x400")
        attendees_win.transient(self.root)

        tk.Label(
            attendees_win,
            text=f"Attendees for: {event.name}",
            font=("Arial", 12, "bold"),
        ).pack(pady=10)

        tk.Label(
            attendees_win,
            text=f"Total: {len(event.attendees)} / {event.capacity}",
            font=("Arial", 10),
        ).pack()

        # Listbox with scrollbar
        frame = tk.Frame(attendees_win)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(frame, font=("Arial", 10), yscrollcommand=scrollbar.set)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)

        if event.attendees:
            for i, attendee in enumerate(event.attendees, 1):
                listbox.insert(tk.END, f"{i}. {attendee}")
        else:
            listbox.insert(tk.END, "No attendees registered yet")

    def manage_registrations(self):
        """Manage attendee registrations for selected event"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an event.")
            return

        item = self.tree.item(selected[0])
        event_id = item["values"][0]
        event = self.event_service.get_event_by_id(event_id)

        if not event:
            messagebox.showerror("Error", "Event not found!")
            return

        # Create management window
        manage_win = tk.Toplevel(self.root)
        manage_win.title(f"Manage Registrations - {event.name}")
        manage_win.geometry("500x500")
        manage_win.transient(self.root)

        tk.Label(
            manage_win, text=f"Manage: {event.name}", font=("Arial", 12, "bold")
        ).pack(pady=10)

        tk.Label(
            manage_win,
            text=f"Registered: {len(event.attendees)} / {event.capacity}",
            font=("Arial", 10),
        ).pack()

        # Attendee list
        list_frame = tk.LabelFrame(
            manage_win, text="Current Attendees", font=("Arial", 10, "bold")
        )
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(
            list_frame, font=("Arial", 10), yscrollcommand=scrollbar.set
        )
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.config(command=listbox.yview)

        def refresh_list():
            listbox.delete(0, tk.END)
            event = self.event_service.get_event_by_id(event_id)
            if event and event.attendees:
                for attendee in event.attendees:
                    listbox.insert(tk.END, attendee)

        refresh_list()

        # Action buttons
        btn_frame = tk.Frame(manage_win)
        btn_frame.pack(pady=10)

        def remove_attendee():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning(
                    "Warning", "Please select an attendee to remove."
                )
                return

            username = listbox.get(selection[0])

            if messagebox.askyesno("Confirm", f"Remove {username} from this event?"):
                try:
                    self.event_service.unregister_attendee(event_id, username)
                    self.user_service.unregister_event(username, event_id)
                    messagebox.showinfo("Success", "Attendee removed successfully!")
                    refresh_list()
                    self.populate_table()
                except ValueError as e:
                    messagebox.showerror("Error", str(e))

        tk.Button(
            btn_frame,
            text="Remove Selected Attendee",
            command=remove_attendee,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            width=25,
        ).pack(pady=5)

        tk.Button(
            btn_frame,
            text="Close",
            command=manage_win.destroy,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 10, "bold"),
            width=25,
        ).pack(pady=5)

    def logout(self):
        """Logout and return to login screen"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()
            root = tk.Tk()
            from ui.login_ui import LoginWindow

            LoginWindow(root)
            root.mainloop()
