"""
Event Service - Handles all event-related business logic
"""

import json
import os
from models.event import Event
from datetime import datetime


class EventService:
    def __init__(self, data_file="data/events.json"):
        self.data_file = data_file
        self.events = []
        self.load_events()

    def load_events(self):
        """Load events from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.events = [Event.from_dict(e) for e in data]
            except Exception as e:
                print(f"Error loading events: {e}")
                self.events = []
        else:
            self.events = []

    def save_events(self):
        """Save events to JSON file"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, "w", encoding="utf-8") as f:
            data = [e.to_dict() for e in self.events]
            json.dump(data, f, indent=2, ensure_ascii=False)

    def get_all_events(self):
        """Get all events"""
        self.load_events()
        return self.events

    def get_event_by_id(self, event_id):
        """Get event by ID"""
        for event in self.events:
            if event.id == event_id:
                return event
        return None

    def create_event(
        self, name, date, capacity, location=None, description=None, organizer=None
    ):
        """Create a new event"""
        # Validate inputs
        if not name or not date:
            raise ValueError("Name and date are required")

        try:
            capacity = int(capacity)
            if capacity <= 0:
                raise ValueError("Capacity must be positive")
        except ValueError:
            raise ValueError("Capacity must be a valid number")

        # Validate date format
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")

        # Generate new ID
        new_id = max([e.id for e in self.events], default=0) + 1

        # Create event
        event = Event(new_id, name, date, capacity, location, description, organizer)
        self.events.append(event)
        self.save_events()
        return event

    def update_event(
        self,
        event_id,
        name=None,
        date=None,
        capacity=None,
        location=None,
        description=None,
    ):
        """Update an existing event"""
        event = self.get_event_by_id(event_id)
        if not event:
            raise ValueError("Event not found")

        if name:
            event.name = name
        if date:
            try:
                datetime.strptime(date, "%Y-%m-%d")
                event.date = date
            except ValueError:
                raise ValueError("Date must be in YYYY-MM-DD format")
        if capacity is not None:
            try:
                capacity = int(capacity)
                if capacity < len(event.attendees):
                    raise ValueError(
                        f"Capacity cannot be less than current attendees ({len(event.attendees)})"
                    )
                event.capacity = capacity
            except ValueError as e:
                raise ValueError(str(e))
        if location is not None:
            event.location = location
        if description is not None:
            event.description = description

        self.save_events()
        return event

    def delete_event(self, event_id):
        """Delete an event"""
        event = self.get_event_by_id(event_id)
        if not event:
            raise ValueError("Event not found")

        self.events = [e for e in self.events if e.id != event_id]
        self.save_events()
        return True

    def register_attendee(self, event_id, username):
        """Register an attendee for an event"""
        event = self.get_event_by_id(event_id)
        if not event:
            raise ValueError("Event not found")

        event.add_attendee(username)
        self.save_events()
        return True

    def unregister_attendee(self, event_id, username):
        """Unregister an attendee from an event"""
        event = self.get_event_by_id(event_id)
        if not event:
            raise ValueError("Event not found")

        event.remove_attendee(username)
        self.save_events()
        return True

    def search_events(self, keyword=None, date=None):
        """Search events by keyword or date"""
        results = self.events

        if keyword:
            keyword = keyword.lower()
            results = [
                e
                for e in results
                if keyword in e.name.lower()
                or (e.description and keyword in e.description.lower())
                or (e.location and keyword in e.location.lower())
            ]

        if date:
            results = [e for e in results if e.date == date]

        return results

    def get_events_by_organizer(self, organizer):
        """Get all events organized by a specific organizer"""
        return [e for e in self.events if e.organizer == organizer]

    def get_user_registered_events(self, username):
        """Get all events a user is registered for"""
        return [e for e in self.events if username in e.attendees]

    def get_statistics(self):
        """Get event statistics"""
        if not self.events:
            return {
                "total_events": 0,
                "total_attendees": 0,
                "average_attendance": 0,
                "highest_attendance": None,
                "lowest_attendance": None,
                "full_events": 0,
            }

        total_attendees = sum(len(e.attendees) for e in self.events)
        events_with_attendees = [e for e in self.events if e.attendees]

        highest = (
            max(self.events, key=lambda e: len(e.attendees))
            if events_with_attendees
            else None
        )
        lowest = (
            min(events_with_attendees, key=lambda e: len(e.attendees))
            if events_with_attendees
            else None
        )

        return {
            "total_events": len(self.events),
            "total_attendees": total_attendees,
            "average_attendance": (
                total_attendees / len(self.events) if self.events else 0
            ),
            "highest_attendance": (
                {"name": highest.name, "attendees": len(highest.attendees)}
                if highest
                else None
            ),
            "lowest_attendance": (
                {"name": lowest.name, "attendees": len(lowest.attendees)}
                if lowest
                else None
            ),
            "full_events": len([e for e in self.events if e.is_full()]),
        }

    def export_to_csv(self, filename="reports/events_report.csv"):
        """Export events to CSV file"""
        import csv

        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "ID",
                    "Name",
                    "Date",
                    "Capacity",
                    "Attendees",
                    "Available Slots",
                    "Location",
                    "Organizer",
                ]
            )

            for event in self.events:
                writer.writerow(
                    [
                        event.id,
                        event.name,
                        event.date,
                        event.capacity,
                        len(event.attendees),
                        event.available_slots(),
                        event.location or "",
                        event.organizer or "",
                    ]
                )

        return filename
