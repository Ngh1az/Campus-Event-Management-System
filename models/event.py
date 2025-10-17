"""
Event Model - Represents campus events
"""

from datetime import datetime


class Event:
    def __init__(
        self,
        event_id,
        name,
        date,
        capacity,
        location=None,
        description=None,
        organizer=None,
    ):
        self.id = event_id
        self.name = name
        self.date = date  # Format: YYYY-MM-DD
        self.capacity = capacity
        self.location = location
        self.description = description
        self.organizer = organizer  # Username of organizer
        self.attendees = []  # List of attendee usernames

    def to_dict(self):
        """Convert event object to dictionary for JSON storage"""
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date,
            "capacity": self.capacity,
            "location": self.location,
            "description": self.description,
            "organizer": self.organizer,
            "attendees": self.attendees,
        }

    @staticmethod
    def from_dict(data):
        """Create event object from dictionary"""
        event = Event(
            data.get("id"), data.get("name"), data.get("date"), data.get("capacity")
        )
        event.location = data.get("location")
        event.description = data.get("description")
        event.organizer = data.get("organizer")
        event.attendees = data.get("attendees", [])
        return event

    def is_full(self):
        """Check if event has reached capacity"""
        return len(self.attendees) >= self.capacity

    def available_slots(self):
        """Return number of available slots"""
        return self.capacity - len(self.attendees)

    def add_attendee(self, username):
        """Add an attendee to the event"""
        if self.is_full():
            raise ValueError("Event is full")
        if username in self.attendees:
            raise ValueError("User already registered")
        self.attendees.append(username)

    def remove_attendee(self, username):
        """Remove an attendee from the event"""
        if username not in self.attendees:
            raise ValueError("User not registered")
        self.attendees.remove(username)

    def validate_date(self):
        """Validate if event date is in the future"""
        try:
            event_date = datetime.strptime(self.date, "%Y-%m-%d")
            return event_date >= datetime.now()
        except ValueError:
            return False

    def __str__(self):
        return f"{self.name} on {self.date} ({len(self.attendees)}/{self.capacity})"
