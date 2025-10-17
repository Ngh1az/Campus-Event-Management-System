"""
User Service - Handles all user-related business logic
"""

import json
import os
from models.user import User


class UserService:
    def __init__(self, data_file="users.json"):
        self.data_file = data_file
        self.users = []
        self.load_users()

    def load_users(self):
        """Load users from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.users = [User.from_dict(u) for u in data]
            except Exception as e:
                print(f"Error loading users: {e}")
                self.users = []
        else:
            self.users = []

    def save_users(self):
        """Save users to JSON file"""
        with open(self.data_file, "w", encoding="utf-8") as f:
            data = [u.to_dict() for u in self.users]
            json.dump(data, f, indent=2, ensure_ascii=False)

    def authenticate(self, username, password, role):
        """Authenticate a user with role"""
        for user in self.users:
            if (
                user.username == username
                and user.password == password
                and user.role == role
            ):
                return user
        return None

    def authenticate_without_role(self, username, password):
        """Authenticate a user without role - system determines role automatically"""
        for user in self.users:
            if user.username == username and user.password == password:
                return user
        return None

    def get_user(self, username):
        """Get user by username"""
        for user in self.users:
            if user.username == username:
                return user
        return None

    def create_user(self, username, password, role, email=None, full_name=None):
        """Create a new user"""
        if self.get_user(username):
            raise ValueError("Username already exists")

        user = User(username, password, role, email, full_name)
        self.users.append(user)
        self.save_users()
        return user

    def update_user(self, username, password=None, email=None, full_name=None):
        """Update user information"""
        user = self.get_user(username)
        if not user:
            raise ValueError("User not found")

        if password:
            user.password = password
        if email:
            user.email = email
        if full_name:
            user.full_name = full_name

        self.save_users()
        return user

    def register_event(self, username, event_id):
        """Register user for an event"""
        user = self.get_user(username)
        if not user:
            raise ValueError("User not found")

        if event_id in user.registered_events:
            raise ValueError("Already registered for this event")

        user.registered_events.append(event_id)
        self.save_users()
        return True

    def unregister_event(self, username, event_id):
        """Unregister user from an event"""
        user = self.get_user(username)
        if not user:
            raise ValueError("User not found")

        if event_id not in user.registered_events:
            raise ValueError("Not registered for this event")

        user.registered_events.remove(event_id)
        self.save_users()
        return True
