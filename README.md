# Campus Event Management System

A comprehensive event management system for campus with role-based access control.

## Features

### Role-Based Access Control

- **Admin**: Full control over all events and system
- **Organizer**: Manage attendees for their events
- **Student/Visitor**: Search and register for events

### Core Functionalities

1. **Event Management**

   - Create, update, and delete events
   - Track event capacity and availability
   - Input validation for dates and capacities

2. **Attendee Registration**

   - Register for events with capacity checks
   - Prevent duplicate registrations
   - View registered events

3. **Statistics & Reporting**

   - Total attendees across all events
   - Events with highest/lowest attendance
   - Export reports to CSV

4. **Data Persistence**
   - JSON-based storage for users and events
   - Automatic data saving on changes

## Installation

### Requirements

- Python 3.8 or higher
- tkinter (usually included with Python)

### Setup

1. Clone or download the project
2. Install dependencies (if any):

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## Usage

### Login Credentials

- **Admin**:

  - Username: `admin`
  - Password: `123`
  - Role: Admin

- **Organizer**:

  - Username: `john`
  - Password: `123`
  - Role: Organizer

- **Student**:
  - Username: `anna` or `mike`
  - Password: `123`
  - Role: Student

### Admin Dashboard

- Create new events with details
- Update existing events
- Delete events
- View all attendees
- Export statistics to CSV
- View real-time statistics

### Organizer Dashboard

- View events assigned to them
- Manage attendee registrations
- View event details and attendees

### Student Dashboard

- Search for available events
- Register for events
- View registered events
- Unregister from events
- View detailed event information

## Project Structure

```
python/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── users.json             # User data storage
├── models/                # Data models
│   ├── __init__.py
│   ├── user.py           # User model
│   └── event.py          # Event model
├── services/             # Business logic
│   ├── __init__.py
│   ├── user_service.py   # User management
│   └── event_service.py  # Event management
├── ui/                   # User interface
│   ├── login_ui.py       # Login window
│   ├── admin_ui.py       # Admin dashboard
│   ├── organizer_ui.py   # Organizer dashboard
│   └── student_ui.py     # Student dashboard
├── data/                 # Data storage
│   └── events.json       # Event data
└── reports/              # Generated reports
```

## Code Quality

### OOP Principles

- **Encapsulation**: Models encapsulate data and behavior
- **Abstraction**: Service layer abstracts business logic
- **Separation of Concerns**: Clear separation between UI, business logic, and data

### Design Patterns

- **Model-View-Controller**: Separation of data (models), logic (services), and presentation (UI)
- **Service Layer Pattern**: Business logic centralized in service classes
- **Repository Pattern**: Data access abstracted through services

### Features Implemented

✅ Role-based access control
✅ Event CRUD operations
✅ Attendee registration with capacity management
✅ Duplicate registration prevention
✅ Search functionality
✅ Statistics and analytics
✅ CSV export
✅ Data persistence (JSON)
✅ Input validation
✅ Error handling
✅ User-friendly interface

### Bonus Features

- 🎨 Modern, colorful UI with proper layouts
- 🔍 Advanced search functionality
- 📊 Real-time statistics dashboard
- 📝 Detailed event descriptions
- 🏢 Location tracking
- 👤 Organizer assignment
- 📧 User profile with email
- ✅ Double-click to view details
- 🔄 Auto-refresh after actions

## Screenshots

### Login Screen

Professional login interface with role selection

### Admin Dashboard

- Complete event management
- Statistics panel
- Export functionality

### Organizer Dashboard

- View assigned events
- Manage registrations
- View attendee lists

### Student Dashboard

- Search and filter events
- Register/unregister
- View event details

## Error Handling

- Input validation for all forms
- Capacity checks for registrations
- Duplicate prevention
- File error handling
- User-friendly error messages

## Future Enhancements

- Email notifications
- Calendar integration
- QR code for check-in
- Event categories and tags
- Rating and feedback system
- Photo gallery for events
- Multi-language support

## Author

Campus Event Management System v1.0

## License

Educational Project - Free to use and modify
