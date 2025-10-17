"""
User Model - Represents users with different roles
"""


class User:
    def __init__(self, username, password, role, email=None, full_name=None):
        self.username = username
        self.password = password
        self.role = role  # Admin, Organizer, Student
        self.email = email
        self.full_name = full_name
        self.registered_events = []  # List of event IDs

    def to_dict(self):
        """Convert user object to dictionary for JSON storage"""
        return {
            "username": self.username,
            "password": self.password,
            "role": self.role,
            "email": self.email,
            "full_name": self.full_name,
            "registered_events": self.registered_events,
        }

    @staticmethod
    def from_dict(data):
        """Create user object from dictionary"""
        user = User(data.get("username"), data.get("password"), data.get("role"))
        user.email = data.get("email")
        user.full_name = data.get("full_name")
        user.registered_events = data.get("registered_events", [])
        return user

    def can_manage_events(self):
        """Check if user can create/update/delete events"""
        return self.role == "Admin"

    def can_manage_attendees(self):
        """Check if user can manage attendees"""
        return self.role in ["Admin", "Organizer"]

    def can_register_events(self):
        """Check if user can register for events"""
        return self.role in ["Student", "Visitor"]

    def __str__(self):
        return f"{self.username} ({self.role})"
