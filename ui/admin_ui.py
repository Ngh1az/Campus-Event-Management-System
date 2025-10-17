import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from services.event_service import EventService
from services.user_service import UserService


class AdminWindow:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.root.title(f"Admin Dashboard - {user.username}")
        self.root.geometry("1000x700")

        self.event_service = EventService()
        self.user_service = UserService()

        # Header
        header_frame = tk.Frame(root, bg="#2c3e50", height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="Admin - Event Management System",
            font=("Arial", 16, "bold"),
            bg="#2c3e50",
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

        # Left panel - Event list
        left_frame = tk.LabelFrame(
            main_frame, text="Events List", font=("Arial", 12, "bold")
        )
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Search bar
        search_frame = tk.Frame(left_frame)
        search_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(search_frame, text="Search:", font=("Arial", 10)).pack(
            side=tk.LEFT, padx=5
        )
        self.search_entry = tk.Entry(search_frame, font=("Arial", 10), width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(
            search_frame,
            text="Search",
            command=self.search_events,
            bg="#3498db",
            fg="white",
        ).pack(side=tk.LEFT, padx=5)
        tk.Button(
            search_frame,
            text="Clear",
            command=self.populate_table,
            bg="#95a5a6",
            fg="white",
        ).pack(side=tk.LEFT)

        # Treeview
        tree_frame = tk.Frame(left_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

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

        # Right panel - Actions
        right_frame = tk.Frame(main_frame, width=300)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        right_frame.pack_propagate(False)

        # Add Event Form
        form_frame = tk.LabelFrame(
            right_frame, text="Add New Event", font=("Arial", 11, "bold")
        )
        form_frame.pack(fill=tk.X, pady=(0, 15))

        tk.Label(form_frame, text="Event Name:", font=("Arial", 9)).pack(
            anchor="w", padx=10, pady=(10, 0)
        )
        self.name_entry = tk.Entry(form_frame, font=("Arial", 10), width=28)
        self.name_entry.pack(padx=10, pady=(0, 5))

        tk.Label(form_frame, text="Date (YYYY-MM-DD):", font=("Arial", 9)).pack(
            anchor="w", padx=10
        )
        self.date_entry = tk.Entry(form_frame, font=("Arial", 10), width=28)
        self.date_entry.pack(padx=10, pady=(0, 5))

        tk.Label(form_frame, text="Capacity:", font=("Arial", 9)).pack(
            anchor="w", padx=10
        )
        self.capacity_entry = tk.Entry(form_frame, font=("Arial", 10), width=28)
        self.capacity_entry.pack(padx=10, pady=(0, 5))

        tk.Label(form_frame, text="Location:", font=("Arial", 9)).pack(
            anchor="w", padx=10
        )
        self.location_entry = tk.Entry(form_frame, font=("Arial", 10), width=28)
        self.location_entry.pack(padx=10, pady=(0, 5))

        tk.Label(form_frame, text="Description:", font=("Arial", 9)).pack(
            anchor="w", padx=10
        )
        self.desc_text = tk.Text(form_frame, font=("Arial", 9), width=28, height=3)
        self.desc_text.pack(padx=10, pady=(0, 10))

        tk.Button(
            form_frame,
            text="Add Event",
            command=self.add_event,
            bg="#27ae60",
            fg="white",
            font=("Arial", 10, "bold"),
            width=25,
        ).pack(pady=(0, 10))

        # Action Buttons
        actions_frame = tk.LabelFrame(
            right_frame, text="Actions", font=("Arial", 11, "bold")
        )
        actions_frame.pack(fill=tk.X, pady=(0, 15))

        tk.Button(
            actions_frame,
            text="Update Selected Event",
            command=self.update_event,
            bg="#3498db",
            fg="white",
            font=("Arial", 9, "bold"),
            width=30,
        ).pack(padx=10, pady=(10, 5))

        tk.Button(
            actions_frame,
            text="Delete Selected Event",
            command=self.delete_event,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 9, "bold"),
            width=30,
        ).pack(padx=10, pady=5)

        tk.Button(
            actions_frame,
            text="View Attendees",
            command=self.view_attendees,
            bg="#9b59b6",
            fg="white",
            font=("Arial", 9, "bold"),
            width=30,
        ).pack(padx=10, pady=5)

        tk.Button(
            actions_frame,
            text="Export to CSV",
            command=self.export_csv,
            bg="#16a085",
            fg="white",
            font=("Arial", 9, "bold"),
            width=30,
        ).pack(padx=10, pady=(5, 10))

        # Statistics
        stats_frame = tk.LabelFrame(
            right_frame, text="Statistics", font=("Arial", 11, "bold")
        )
        stats_frame.pack(fill=tk.BOTH, expand=True)

        self.stats_label = tk.Label(
            stats_frame, text="", font=("Arial", 9), justify=tk.LEFT, anchor="nw"
        )
        self.stats_label.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Load data
        self.populate_table()
        self.update_statistics()

    def populate_table(self):
        """Load and display all events"""
        for i in self.tree.get_children():
            self.tree.delete(i)

        events = self.event_service.get_all_events()
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

        self.update_statistics()

    def search_events(self):
        """Search events by keyword"""
        keyword = self.search_entry.get().strip()
        if not keyword:
            self.populate_table()
            return

        for i in self.tree.get_children():
            self.tree.delete(i)

        events = self.event_service.search_events(keyword=keyword)
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

    def add_event(self):
        """Add a new event"""
        name = self.name_entry.get().strip()
        date = self.date_entry.get().strip()
        capacity = self.capacity_entry.get().strip()
        location = self.location_entry.get().strip()
        description = self.desc_text.get("1.0", tk.END).strip()

        try:
            event = self.event_service.create_event(
                name, date, capacity, location, description, self.user.username
            )
            messagebox.showinfo(
                "Success", f"Event '{event.name}' created successfully!"
            )

            # Clear form
            self.name_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)
            self.capacity_entry.delete(0, tk.END)
            self.location_entry.delete(0, tk.END)
            self.desc_text.delete("1.0", tk.END)

            self.populate_table()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def update_event(self):
        """Update selected event"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an event to update.")
            return

        item = self.tree.item(selected[0])
        event_id = item["values"][0]
        event = self.event_service.get_event_by_id(event_id)

        # Create update dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Update Event")
        dialog.geometry("400x400")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Event Name:", font=("Arial", 10)).pack(pady=(20, 0))
        name_entry = tk.Entry(dialog, font=("Arial", 10), width=40)
        name_entry.insert(0, event.name)
        name_entry.pack(pady=5)

        tk.Label(dialog, text="Date (YYYY-MM-DD):", font=("Arial", 10)).pack()
        date_entry = tk.Entry(dialog, font=("Arial", 10), width=40)
        date_entry.insert(0, event.date)
        date_entry.pack(pady=5)

        tk.Label(dialog, text="Capacity:", font=("Arial", 10)).pack()
        capacity_entry = tk.Entry(dialog, font=("Arial", 10), width=40)
        capacity_entry.insert(0, str(event.capacity))
        capacity_entry.pack(pady=5)

        tk.Label(dialog, text="Location:", font=("Arial", 10)).pack()
        location_entry = tk.Entry(dialog, font=("Arial", 10), width=40)
        location_entry.insert(0, event.location or "")
        location_entry.pack(pady=5)

        def save_update():
            try:
                self.event_service.update_event(
                    event_id,
                    name_entry.get().strip(),
                    date_entry.get().strip(),
                    (
                        int(capacity_entry.get().strip())
                        if capacity_entry.get().strip()
                        else None
                    ),
                    location_entry.get().strip(),
                )
                messagebox.showinfo("Success", "Event updated successfully!")
                dialog.destroy()
                self.populate_table()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        tk.Button(
            dialog,
            text="Save Changes",
            command=save_update,
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            width=20,
        ).pack(pady=20)

    def delete_event(self):
        """Delete selected event"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an event to delete.")
            return

        item = self.tree.item(selected[0])
        event_id = item["values"][0]
        event_name = item["values"][1]

        if messagebox.askyesno(
            "Confirm Delete", f"Are you sure you want to delete '{event_name}'?"
        ):
            try:
                self.event_service.delete_event(event_id)
                messagebox.showinfo("Success", "Event deleted successfully!")
                self.populate_table()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def view_event_details(self, event=None):
        """View detailed information about an event"""
        selected = self.tree.selection()
        if not selected:
            return

        item = self.tree.item(selected[0])
        event_id = item["values"][0]
        event = self.event_service.get_event_by_id(event_id)

        details = f"""
Event Details:
─────────────────────────
Name: {event.name}
Date: {event.date}
Location: {event.location or 'Not specified'}
Capacity: {event.capacity}
Registered: {len(event.attendees)}
Available: {event.available_slots()}
Organizer: {event.organizer or 'N/A'}

Description:
{event.description or 'No description provided'}

Attendees:
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
            for attendee in event.attendees:
                listbox.insert(tk.END, attendee)
        else:
            listbox.insert(tk.END, "No attendees registered yet")

    def export_csv(self):
        """Export events to CSV"""
        try:
            filename = self.event_service.export_to_csv()
            messagebox.showinfo("Success", f"Report exported to:\n{filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")

    def update_statistics(self):
        """Update statistics display"""
        stats = self.event_service.get_statistics()

        stats_text = f"""
Total Events: {stats['total_events']}
Total Attendees: {stats['total_attendees']}
Avg Attendance: {stats['average_attendance']:.1f}
Full Events: {stats['full_events']}

Highest Attendance:
  {stats['highest_attendance']['name'] if stats['highest_attendance'] else 'N/A'}
  ({stats['highest_attendance']['attendees']} attendees) if stats['highest_attendance'] else ''

Lowest Attendance:
  {stats['lowest_attendance']['name'] if stats['lowest_attendance'] else 'N/A'}
  ({stats['lowest_attendance']['attendees']} attendees) if stats['lowest_attendance'] else ''
"""
        self.stats_label.config(text=stats_text)

    def logout(self):
        """Logout and return to login screen"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()
            root = tk.Tk()
            from ui.login_ui import LoginWindow

            LoginWindow(root)
            root.mainloop()
